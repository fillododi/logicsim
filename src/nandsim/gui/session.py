"""A running chip in the GUI: load, simulate, navigate, reload. Pure Python, no pygame.

The session owns the flattened simulation of the top chip and a *view path*
(`Mux`, `Mux/Or#4`, ...) saying which level of the hierarchy is on screen. On
reload, an HDL error never replaces the running circuit: the session keeps the
last version that compiled and remembers the error so the GUI can show it.

A chip with DFFs has a clock: `step` runs one whole cycle (tick and tock), and
`advance` runs as many cycles as the speed asks for while `running`. A reload keeps
the DFFs' values and the cycle count only if every DFF still sits in the same place
in the hierarchy (`Reg2/Bit#1/DFF#5`); otherwise the clock starts over.

`builtins` says whether DFF parts run as the built-in flip-flop (the default) or
as the player's own DFF chip, latches and all, which can then be opened.

Given a `program` and a chip with the 4004's bus pins, the session puts the test
runner's MCS-4 memories on the bus, the way a CPU level's `.tst` does: every step
goes through them, and a reset of the clock reloads the program and holds the CPU's
`reset` for 64 clocks, so the next step is A1 of address 0.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from nandsim.gui.layout import Layout, Style, layout
from nandsim.gui.model import ChipView, PartView, build_view, child_path, parent_path
from nandsim.hdl import ChipDef, HdlError
from nandsim.netlist import STAND_INS, ChipLibrary, Netlist, Primitive, elaborate
from nandsim.sim import Simulator
from nandsim.testing import BUS_PINS, Mcs4, check_pins

# Returns the top chip's name and the library to find it and its parts in.
Loader = Callable[[], tuple[str, ChipLibrary]]

SPEEDS = (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)  # clock rates offered, in cycles/s
DEFAULT_SPEED = 5
FRAME_BUDGET = 0.03  # seconds of clocking per frame at most, so the window stays responsive
RESET_CLOCKS = 64  # how long a reset of the clock holds a CPU's reset pin: 8 cycles


@dataclass
class Snapshot:
    """What is on screen: the current level's view and its layout."""

    view: ChipView
    layout: Layout


class ChipSession:
    def __init__(
        self, loader: Loader, style: Style | None = None, program: list[int] | None = None
    ) -> None:
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
        self.running = False
        self.speed = DEFAULT_SPEED
        self._owed = 0.0  # cycles due but not yet run, while running
        self.builtins = True  # DFF parts run as the built-in flip-flop
        # B can switch: a DFF part sits under the chip, and the player's DFF HDL exists.
        self.can_switch = False
        self.program = program  # ROM bytes for a CPU's memories, from address 0
        self.memories: Mcs4 | None = None  # attached when the chip has the bus pins
        self.bus_problem: str | None = None  # the first, as the test runner reports it

    # ---- loading -------------------------------------------------------

    def reload(self) -> bool:
        """(Re)build from the loader. On error keep the old circuit and set `error`."""
        try:
            name, lib = self.loader()
            lib.builtins = self.builtins  # the loader's library is fresh: set before lookups
            top = lib.resolve_top(name)
            if isinstance(top, Primitive):
                raise HdlError(f"'{name}' is a primitive; open a chip built from parts", None)
            netlist = elaborate(top, lib)
        except HdlError as e:
            self.error = e
            return False
        except OSError as e:
            self.error = HdlError(f"cannot read chip: {e}", None)
            return False
        old = self.sim
        self.netlist, self.lib, self.error = netlist, lib, None
        self.can_switch = _uses_stand_in(top, lib) and all(lib.has_hdl(s) for s in STAND_INS)
        self.sim = Simulator(netlist)
        carried = self._carry_clock(old, self.sim)
        kept = {}
        for pin, nets in netlist.inputs.items():
            v = self.inputs.get(pin)
            kept[pin] = v if v is None or v < (1 << len(nets)) else None
        self.inputs = kept
        for pin, v in self.inputs.items():
            self.sim.set(pin, v)
        self.sim.eval()
        self._attach(top.name, carried)
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

    def drives(self, pin: str) -> bool:
        """Whether the memories drive this input, so the player can't set it."""
        return self.memories is not None and pin == "din"

    def set_input(self, pin: str, value: int | None) -> None:
        assert self.sim is not None
        if self.drives(pin):
            return
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

    # ---- built-in parts --------------------------------------------------

    def toggle_builtins(self) -> str | None:
        """Switch DFF parts between the built-in flip-flop and the player's own DFF.

        Returns None if the chip rebuilt, else why not, for the player; then nothing
        changes. The clock starts over, since the DFFs are no longer the same ones.
        A chip that doesn't build is refused up front, so a failure here is the DFF's.
        """
        if not self.can_switch:
            return "There is no DFF of yours to switch to in this chip."
        if self.error is not None:
            return "Fix the errors in your chip first: B switches only a chip that builds."
        self.builtins = not self.builtins
        if self.reload():
            return None
        why = self.error.message if self.error is not None else "it doesn't build"
        self.builtins = not self.builtins
        self.error = None  # a failed reload leaves the running circuit as it was
        if self.builtins:
            return f"Your DFF doesn't build, so DFF parts stay built-in: {why}"
        return f"The chip doesn't build with the built-in DFF: {why}"

    # ---- the clock -------------------------------------------------------

    @property
    def has_clock(self) -> bool:
        """Whether the chip has DFFs or reads `clock`, so the clock does something."""
        return self.sim is not None and self.sim.clocked

    @property
    def cycle(self) -> int:
        return self.sim.cycle if self.sim is not None else 0

    def step(self) -> None:
        """One whole clock cycle: tick, then tock (through the memories, if attached)."""
        assert self.sim is not None
        m = self.memories
        if m is not None:
            self.sim.refresh()
            period = m.period()
            problem = m.tick()
            if problem is not None and self.bus_problem is None:
                self.bus_problem = f"at {period}: {problem}"
        self.sim.tick()
        self.sim.tock()
        if m is not None:
            m.tock()

    def reset_clock(self) -> None:
        """DFFs back to undefined and the cycle to 0. The inputs keep their values."""
        assert self.sim is not None
        self.sim.reset()
        for pin, v in self.inputs.items():
            self.sim.set(pin, v)
        self.sim.eval()
        self.running = False
        self._owed = 0.0
        if self.memories is not None:
            self._restart()

    def toggle_run(self) -> None:
        self.running = not self.running and self.has_clock
        self._owed = 0.0

    def change_speed(self, delta: int) -> None:
        """Move `delta` notches along SPEEDS, stopping at either end."""
        i = SPEEDS.index(self.speed) + delta
        self.speed = SPEEDS[max(0, min(len(SPEEDS) - 1, i))]

    def advance(self, dt: float, budget: float = FRAME_BUDGET) -> int:
        """While running, run the cycles `dt` seconds are worth; return how many ran.

        If the chip is too slow for the speed, run for `budget` seconds and drop the
        rest, so the clock falls behind instead of freezing the window.
        """
        if not self.running or self.sim is None:
            return 0
        self._owed += dt * self.speed
        due = int(self._owed + 1e-9)  # 0.2 s at 5/s is 0.999…: still one whole cycle
        self._owed = max(0.0, self._owed - due)
        start = time.perf_counter()
        done = 0
        while done < due:
            self.step()
            done += 1
            if time.perf_counter() - start > budget:
                self._owed = 0.0
                break
        return done

    # ---- the MCS-4 memories ----------------------------------------------

    def _attach(self, chip: str, carried: bool) -> None:
        """Put the memories on the bus if there is a program and the chip has the pins."""
        assert self.sim is not None
        if self.program is None or not _has_bus(self.sim, chip):
            self.memories = None
            return
        if carried and self.memories is not None:
            self.memories.sim = self.sim  # same DFFs, same memories: carry on
            self.memories.drive_bus()
            return
        self._restart()

    def _restart(self) -> None:
        """Fresh memories with the program, then the CPU held in reset for 64 clocks."""
        sim = self.sim
        assert sim is not None and self.program is not None
        m = Mcs4(sim, {name: name for name in BUS_PINS})
        m.rom[: len(self.program)] = self.program
        self.memories, self.bus_problem = m, None
        if self.inputs.get("test") is None:
            self.set_input("test", 0)
        self.set_input("reset", 1)
        m.drive_bus()
        for _ in range(RESET_CLOCKS):
            self.step()
        self.set_input("reset", 0)
        sim.eval()
        m.drive_bus()
        sim.cycle = 0

    def _carry_clock(self, old: Simulator | None, new: Simulator) -> bool:
        """Move the clock's state from `old` into the rebuilt `new`, if it still means the same.

        Part paths are numbered by position (`Bit#2`), so a part added or removed
        renumbers the DFFs after it. State carries only when every DFF sits where it
        did; otherwise every DFF starts undefined, the count restarts and the clock
        pauses, as after a reset. A value is never shown on the wrong DFF.
        """
        same = old is not None and old.dff_count > 0 and old.dff_paths == new.dff_paths
        if same:
            assert old is not None
            value, known = old.dff_state()
            new.load_dff_state(np.arange(new.dff_count), value, known)
            new.cycle = old.cycle
        else:
            self.running = False
            self._owed = 0.0
        return same

    def known_fraction(self, nets: tuple[int, ...] | list[int]) -> float:
        assert self.sim is not None
        idx = np.asarray(nets, dtype=np.int64)
        return float(self.sim.known[idx].mean()) if len(idx) else 1.0


def _has_bus(sim: Simulator, chip: str) -> bool:
    """Whether the chip has every 4004 bus pin, of the right width and direction."""
    try:
        check_pins(sim, chip, {name: (name, None) for name in BUS_PINS})  # type: ignore[misc]
    except HdlError:
        return False
    return True


def _uses_stand_in(top: ChipDef, lib: ChipLibrary) -> bool:
    """Whether a DFF part sits anywhere below `top`, as the primitive or as HDL."""
    seen: set[str] = set()
    todo = [top]
    while todo:
        chip = todo.pop()
        for part in chip.parts:
            if part.chip in STAND_INS:
                return True
            if part.chip in seen:
                continue
            seen.add(part.chip)
            target = lib.resolve(part.chip)
            if not isinstance(target, Primitive):
                todo.append(target)
    return False


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
