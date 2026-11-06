"""Syntax tree for one HDL chip definition."""

from __future__ import annotations

from dataclasses import dataclass

from nandsim.hdl.errors import SourcePos


@dataclass(frozen=True)
class PinDecl:
    """An `IN` or `OUT` pin: `a` (width 1) or `a[8]`."""

    name: str
    width: int
    pos: SourcePos


@dataclass(frozen=True)
class PinRef:
    """A reference to a pin or wire, optionally sliced: `a`, `a[3]`, `a[0..7]`.

    `lo` and `hi` are both None for the whole pin; for `a[3]` both are 3.
    `part` is set for a labelled part's output, as in `g1.out` (part "g1", name "out").
    """

    name: str
    lo: int | None
    hi: int | None
    pos: SourcePos
    part: str | None = None

    @property
    def sliced(self) -> bool:
        return self.lo is not None

    @property
    def key(self) -> str:
        """The signal this refers to, without the slice: `a` or `g1.out`."""
        return f"{self.part}.{self.name}" if self.part else self.name

    def __str__(self) -> str:
        if self.lo is None:
            return self.key
        if self.lo == self.hi:
            return f"{self.key}[{self.lo}]"
        return f"{self.key}[{self.lo}..{self.hi}]"


@dataclass(frozen=True)
class Const:
    """The constant `true` or `false`, repeated over every bit it connects to."""

    value: bool
    pos: SourcePos

    def __str__(self) -> str:
        return "true" if self.value else "false"


@dataclass(frozen=True)
class Connection:
    """`inner=outer` inside a part: the part's pin on the left, our signal on the right."""

    inner: PinRef
    outer: PinRef | Const
    pos: SourcePos


@dataclass(frozen=True)
class Part:
    """One use of a chip inside PARTS, e.g. `Nand(a=a, b=b, out=n)` or `g1: Nand(a=a, b=b)`.

    A labelled part's outputs can be read elsewhere as `label.pin`.
    """

    chip: str
    connections: tuple[Connection, ...]
    pos: SourcePos
    label: str | None = None
    label_pos: SourcePos | None = None


@dataclass(frozen=True)
class Assign:
    """A direct connection inside PARTS: `out = a;`, `low[0..3] = g1.out;`, `x = true;`."""

    target: PinRef
    source: PinRef | Const
    pos: SourcePos


@dataclass(frozen=True)
class ChipDef:
    """A whole `CHIP Name { ... }` definition."""

    name: str
    inputs: tuple[PinDecl, ...]
    outputs: tuple[PinDecl, ...]
    parts: tuple[Part, ...]
    pos: SourcePos
    assigns: tuple[Assign, ...] = ()

    def pin(self, name: str) -> PinDecl | None:
        for p in self.inputs + self.outputs:
            if p.name == name:
                return p
        return None

    def is_input(self, name: str) -> bool:
        return any(p.name == name for p in self.inputs)
