"""Chip lookup: maps a chip name to its primitive or its parsed HDL definition."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nandsim.hdl import ChipDef, HdlError, SourcePos, parse
from nandsim.netlist.primitives import PRIMITIVES, Primitive


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
    """

    def __init__(
        self,
        search_dirs: list[Path] | None = None,
        sources: dict[str, tuple[str, str]] | None = None,
    ) -> None:
        self.search_dirs = list(search_dirs or [])
        self.sources = dict(sources or {})
        self._cache: dict[str, ChipDef] = {}

    def find_file(self, name: str) -> Path | None:
        for d in self.search_dirs:
            for path in sorted(d.rglob(f"{name}.hdl")):
                return path
        return None

    def resolve(self, name: str, used_at: SourcePos | None = None) -> ChipDef | Primitive:
        if name in PRIMITIVES:
            return PRIMITIVES[name]
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
