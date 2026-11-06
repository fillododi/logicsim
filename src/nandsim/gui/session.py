"""A running chip in the GUI: load, simulate, navigate, reload. Pure Python, no pygame.

The session owns the flattened simulation of the top chip and a *view path*
(`Mux`, `Mux/Or#4`, ...) saying which level of the hierarchy is on screen. On
reload, an HDL error never replaces the running circuit: the session keeps the
last version that compiled and remembers the error so the GUI can show it.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from nandsim.gui.layout import Layout, Style, layout
from nandsim.gui.model import ChipView, PartView, build_view, child_path, parent_path
from nandsim.hdl import HdlError
from nandsim.netlist import ChipLibrary, Netlist, Primitive, elaborate
from nandsim.sim import Simulator

# Returns the top chip's name and the library to find it and its parts in.
Loader = Callable[[], tuple[str, ChipLibrary]]


@dataclass
class Snapshot:
    """What is on screen: the current level's view and its layout."""

    view: ChipView
    layout: Layout


class ChipSession:
    def __init__(self, loader: Loader, style: Style | None = None) -> None:
        self.loader = loader
        self.style = style or Style()
        self.netlist: Netlist | None = None
        self.sim: Simulator | None = None
        self.lib: ChipLibrary | None = None
        self.path: str = ""
        self.snapshot: Snapshot | None = None
        self.error: HdlError | None = None
        self.inputs: dict[str, int | None] = {}
        self._layouts: dict[str, Snapshot] = {}

    # ---- loading -------------------------------------------------------

    def reload(self) -> bool:
        """(Re)build from the loader. On error keep the old circuit and set `error`."""
        try:
            name, lib = self.loader()
            top = lib.resolve(name)
            if isinstance(top, Primitive):
                raise HdlError(f"'{name}' is a primitive; open a chip built from parts", None)
            netlist = elaborate(top, lib)
        except HdlError as e:
            self.error = e
            return False
        except OSError as e:
            self.error = HdlError(f"cannot read chip: {e}", None)
            return False
        self.netlist, self.lib, self.error = netlist, lib, None
        self.sim = Simulator(netlist)
        kept = {}
        for pin, nets in netlist.inputs.items():
            v = self.inputs.get(pin)
            kept[pin] = v if v is None or v < (1 << len(nets)) else None
        self.inputs = kept
        for pin, v in self.inputs.items():
            self.sim.set(pin, v)
        self.sim.eval()
        self._layouts.clear()
        self.goto(self._nearest_valid(self.path or netlist.top))
        return True

    def _nearest_valid(self, path: str) -> str:
        assert self.netlist is not None and self.lib is not None
        p: str | None = path
        while p:
            try:
                build_view(self.netlist, self.lib, p)
                return p
            except KeyError:
                p = parent_path(p)
        return self.netlist.top

    # ---- navigation ----------------------------------------------------

    def goto(self, path: str) -> None:
        assert self.netlist is not None and self.lib is not None
        if path not in self._layouts:
            view = build_view(self.netlist, self.lib, path)
            self._layouts[path] = Snapshot(view, layout(view, self.style))
        self.path = path
        self.snapshot = self._layouts[path]

    def open(self, part: PartView) -> bool:
        target = child_path(self.path, part)
        if target is None:
            return False
        self.goto(target)
        return True

    def up(self) -> bool:
        parent = parent_path(self.path)
        if parent is None:
            return False
        self.goto(parent)
        return True

    @property
    def at_top(self) -> bool:
        return "/" not in self.path

    # ---- inputs and values ---------------------------------------------

    def set_input(self, pin: str, value: int | None) -> None:
        assert self.sim is not None
        self.inputs[pin] = value
        self.sim.set(pin, value)
        self.sim.eval()

    def toggle(self, pin: str, delta: int = 1) -> None:
        """1-bit pins flip; buses count up (or down) and wrap. Undefined starts at 0."""
        assert self.netlist is not None
        width = len(self.netlist.inputs[pin])
        current = self.inputs.get(pin)
        if current is None:
            new = 0 if delta > 0 else (1 << width) - 1
        elif width == 1:
            new = 1 - current
        else:
            new = (current + delta) % (1 << width)
        self.set_input(pin, new)

    def value(self, nets: tuple[int, ...] | list[int]) -> int | None:
        """Integer value of some nets (LSB first), None if any bit is undefined."""
        assert self.sim is not None
        idx = np.asarray(nets, dtype=np.int64)
        if not self.sim.known[idx].all():
            return None
        return int((self.sim.value[idx].astype(np.int64) << np.arange(len(idx))).sum())

    def known_fraction(self, nets: tuple[int, ...] | list[int]) -> float:
        assert self.sim is not None
        idx = np.asarray(nets, dtype=np.int64)
        return float(self.sim.known[idx].mean()) if len(idx) else 1.0


def file_loader(path: Path, search_dirs: list[Path] | None = None) -> Loader:
    """Load the chip in `path`; parts are searched next to it and one level up.

    A fresh library each call, so edited files are re-read on reload.
    """
    dirs = search_dirs or [path.parent, path.parent.parent]

    def load() -> tuple[str, ChipLibrary]:
        text = path.read_text()
        lib = ChipLibrary(dirs, sources={path.stem: (text, str(path))})
        return path.stem, lib

    return load


class FileWatcher:
    """Polls the modification times of every `.hdl` file under some directories."""

    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths
        self._seen = self._scan()

    def _scan(self) -> dict[Path, float]:
        stamps: dict[Path, float] = {}
        for root in self.paths:
            files = [root] if root.is_file() else sorted(root.rglob("*.hdl"))
            for f in files:
                try:
                    stamps[f] = f.stat().st_mtime_ns
                except OSError:
                    pass
        return stamps

    def changed(self) -> bool:
        now = self._scan()
        if now != self._seen:
            self._seen = now
            return True
        return False
