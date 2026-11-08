"""Chip lookup: maps a chip name to its primitive or its parsed HDL definition."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nandsim.hdl import ChipDef, HdlError, SourcePos, parse
from nandsim.netlist.primitives import PRIMITIVES, STAND_INS, Primitive


@dataclass(frozen=True)
class Interface:
    """The pins of any chip, primitive or HDL: name -> width, in declaration order."""

    name: str
    inputs: dict[str, int]
    outputs: dict[str, int]

    def width(self, pin: str) -> int | None:
        return self.inputs.get(pin, self.outputs.get(pin))

    def pin_list(self) -> str:
        return ", ".join([*self.inputs, *self.outputs])


def interface_of(chip: ChipDef | Primitive) -> Interface:
    if isinstance(chip, Primitive):
        return Interface(chip.name, {p: 1 for p in chip.inputs}, {p: 1 for p in chip.outputs})
    return Interface(
        chip.name,
        {p.name: p.width for p in chip.inputs},
        {p.name: p.width for p in chip.outputs},
    )


class ChipLibrary:
    """Finds chips by name: primitives, then in-memory sources, then `.hdl` files.

    `sources` lets the GUI editor (and tests) supply HDL that is not on disk.
    Files are searched as `<dir>/**/<Name>.hdl`, in the order the dirs are given.

    With `builtins` off, a stand-in part (`DFF`) resolves to its HDL wherever some
    exists, so the player can see and open their own flip-flop; without HDL it stays
    the primitive. Set it before the first lookup: elaboration caches per library.
    """

    def __init__(
        self,
        search_dirs: list[Path] | None = None,
        sources: dict[str, tuple[str, str]] | None = None,
        builtins: bool = True,
    ) -> None:
        self.search_dirs = list(search_dirs or [])
        self.sources = dict(sources or {})
        self.builtins = builtins
        self._cache: dict[str, ChipDef] = {}
        self._has_hdl: dict[str, bool] = {}

    def has_hdl(self, name: str) -> bool:
        """Whether some HDL defines `name`, in `sources` or a file.

        Remembered per library, like parsed chips: the GUI asks for every DFF part it
        draws, and a library is rebuilt on every reload anyway.
        """
        if name not in self._has_hdl:
            self._has_hdl[name] = name in self.sources or self.find_file(name) is not None
        return self._has_hdl[name]

    def is_builtin(self, name: str) -> bool:
        """Whether a part with this name runs as a primitive standing in for HDL."""
        return name in STAND_INS and (self.builtins or not self.has_hdl(name))

    def find_file(self, name: str) -> Path | None:
        for d in self.search_dirs:
            for path in sorted(d.rglob(f"{name}.hdl")):
                return path
        return None

    def resolve(self, name: str, used_at: SourcePos | None = None) -> ChipDef | Primitive:
        """A chip used as a part: a primitive wins over HDL of the same name.

        The exception is a stand-in with `builtins` off, if its HDL exists.
        """
        if name in STAND_INS and not self.builtins and self.has_hdl(name):
            return self._load(name, used_at)
        if name in PRIMITIVES:
            return PRIMITIVES[name]
        return self._load(name, used_at)

    def resolve_top(self, name: str, used_at: SourcePos | None = None) -> ChipDef | Primitive:
        """The chip being built, tested or shown: its HDL, if there is any.

        Only a part named `DFF` becomes the primitive; the DFF level itself builds
        the player's latches.
        """
        if name in STAND_INS and self.has_hdl(name):
            return self._load(name, used_at)
        return self.resolve(name, used_at)

    def _load(self, name: str, used_at: SourcePos | None) -> ChipDef:
        if name in self._cache:
            return self._cache[name]
        if name in self.sources:
            text, filename = self.sources[name]
        else:
            path = self.find_file(name)
            if path is None:
                raise HdlError(f"unknown chip '{name}'", used_at)
            text, filename = path.read_text(), str(path)
        chip = parse(text, filename)
        if chip.name != name:
            raise HdlError(f"file for chip '{name}' defines chip '{chip.name}' instead", chip.pos)
        self._cache[name] = chip
        return chip
