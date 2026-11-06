"""What the circuit view shows at one level of the hierarchy. Pure Python, no pygame.

The simulation runs on the flattened netlist, but the player looks at one chip at
a time: its pins, its parts and the wires between them. A `ChipView` is that
picture for a hierarchy path such as `Xor` or `Xor/And#2`, with every pin and
wire mapped to the nets that colour it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from nandsim.hdl import ChipDef, Const, PinRef, SourcePos
from nandsim.netlist import FALSE_NET, TRUE_NET, ChipLibrary, Netlist, Primitive, interface_of

EndKind = Literal["input", "output", "part", "const"]


@dataclass(frozen=True)
class PinView:
    name: str
    width: int
    nets: tuple[int, ...]


@dataclass(frozen=True)
class PartView:
    """One part inside the viewed chip. `index` is 1-based, as in wire paths (`And#2`)."""

    index: int
    chip: str
    path: str
    inputs: tuple[PinView, ...]
    outputs: tuple[PinView, ...]
    primitive: bool
    pos: SourcePos

    @property
    def label(self) -> str:
        return self.chip


@dataclass(frozen=True)
class Endpoint:
    """One end of a wire: a chip pin, a part pin, or a constant.

    `part` is the part index for kind "part"; `bits` is the slice used, or None for
    the whole pin.
    """

    kind: EndKind
    pin: str
    part: int | None = None
    bits: tuple[int, int] | None = None

    def __str__(self) -> str:
        sl = "" if self.bits is None else f"[{self.bits[0]}..{self.bits[1]}]"
        where = f"#{self.part}." if self.part is not None else ""
        return f"{where}{self.pin}{sl}"


@dataclass(frozen=True)
class Edge:
    """A wire from a signal source to a part input or a chip output.

    `nets` are the bits the wire carries, LSB first; `label` is how the signal is
    written in the HDL (`n`, `a[0..3]`, `true`).
    """

    src: Endpoint
    dst: Endpoint
    nets: tuple[int, ...]
    label: str


@dataclass(frozen=True)
class ChipView:
    path: str
    chip: str
    inputs: tuple[PinView, ...]
    outputs: tuple[PinView, ...]
    parts: tuple[PartView, ...]
    edges: tuple[Edge, ...]
    wires: dict[str, tuple[int, ...]]  # internal wires of this chip, by name

    def part(self, index: int) -> PartView:
        return self.parts[index - 1]


def child_path(path: str, part: PartView) -> str | None:
    """The path to open when the player clicks a part; None for primitives."""
    return None if part.primitive else part.path


def parent_path(path: str) -> str | None:
    return path.rsplit("/", 1)[0] if "/" in path else None


def breadcrumbs(path: str) -> list[tuple[str, str]]:
    """[(label, path)] from the top chip down, e.g. Xor > And#2."""
    segs = path.split("/")
    return [(seg, "/".join(segs[: i + 1])) for i, seg in enumerate(segs)]


def resolve_path(netlist: Netlist, lib: ChipLibrary, path: str) -> ChipDef:
    """The chip definition shown at `path`. Raises KeyError for a path that doesn't exist."""
    segs = path.split("/")
    if segs[0] != netlist.top:
        raise KeyError(path)
    chip = lib.resolve(netlist.top)
    for seg in segs[1:]:
        name, _, num = seg.partition("#")
        assert isinstance(chip, ChipDef)
        i = int(num) if num.isdigit() else 0
        if not 1 <= i <= len(chip.parts) or chip.parts[i - 1].chip != name:
            raise KeyError(path)
        chip = lib.resolve(name)
        if isinstance(chip, Primitive):
            raise KeyError(path)
    assert isinstance(chip, ChipDef)
    return chip


def build_view(netlist: Netlist, lib: ChipLibrary, path: str) -> ChipView:
    """The picture of the chip at `path` (e.g. `Xor` or `Xor/And#2`)."""
    chip = resolve_path(netlist, lib, path)
    wires = netlist.wires

    def pin(name: str, width: int, prefix: str) -> PinView:
        return PinView(name, width, tuple(wires[f"{prefix}/{name}"]))

    parts: list[PartView] = []
    for i, part in enumerate(chip.parts, start=1):
        target = lib.resolve(part.chip)
        iface = interface_of(target)
        ppath = f"{path}/{part.chip}#{i}"
        parts.append(
            PartView(
                index=i,
                chip=part.chip,
                path=ppath,
                inputs=tuple(pin(n, w, ppath) for n, w in iface.inputs.items()),
                outputs=tuple(pin(n, w, ppath) for n, w in iface.outputs.items()),
                primitive=isinstance(target, Primitive),
                pos=part.pos,
            )
        )

    # Which part output pin drives each bit of each internal wire / chip output.
    drivers: dict[str, list[Endpoint | None]] = {}
    pin_names = {p.name for p in chip.inputs + chip.outputs}
    for i, part in enumerate(chip.parts, start=1):
        iface = interface_of(lib.resolve(part.chip))
        for c in part.connections:
            if c.inner.name not in iface.outputs or not isinstance(c.outer, PinRef):
                continue
            nets = wires[f"{path}/{c.outer.name}"]
            slot = drivers.setdefault(c.outer.name, [None] * len(nets))
            lo, hi = _span(c.outer, len(nets))
            ilo, ihi = _span(c.inner, iface.outputs[c.inner.name])
            for k in range(hi - lo + 1):
                slot[lo + k] = Endpoint("part", c.inner.name, i, (ilo + k, ilo + k))

    edges: list[Edge] = []

    def sources(ref: PinRef) -> list[tuple[Endpoint, tuple[int, int]]]:
        """Group the referenced bits by the endpoint that drives them."""
        if chip.is_input(ref.name):
            nets = wires[f"{path}/{ref.name}"]
            lo, hi = _span(ref, len(nets))
            bits = None if ref.lo is None else (lo, hi)
            return [(Endpoint("input", ref.name, bits=bits), (lo, hi))]
        nets = wires[f"{path}/{ref.name}"]
        lo, hi = _span(ref, len(nets))
        slot = drivers.get(ref.name, [None] * len(nets))
        groups: list[tuple[Endpoint, tuple[int, int]]] = []
        for b in range(lo, hi + 1):
            d = slot[b]
            if d is None:
                continue
            key = Endpoint(d.kind, d.pin, d.part)
            if groups and groups[-1][0] == key and groups[-1][1][1] == b - 1:
                groups[-1] = (key, (groups[-1][1][0], b))
            else:
                groups.append((key, (b, b)))
        return groups

    for i, part in enumerate(chip.parts, start=1):
        iface = interface_of(lib.resolve(part.chip))
        for c in part.connections:
            if c.inner.name not in iface.inputs:
                continue
            ilo, ihi = _span(c.inner, iface.inputs[c.inner.name])
            dst = Endpoint("part", c.inner.name, i, None if c.inner.lo is None else (ilo, ihi))
            if isinstance(c.outer, Const):
                net = TRUE_NET if c.outer.value else FALSE_NET
                edges.append(
                    Edge(
                        Endpoint("const", str(c.outer)), dst, (net,) * (ihi - ilo + 1), str(c.outer)
                    )
                )
                continue
            for src, (lo, hi) in sources(c.outer):
                src_full = _with_bits(src, drivers, c.outer, lo, hi)
                nets = tuple(wires[f"{path}/{c.outer.name}"][lo : hi + 1])
                edges.append(Edge(src_full, dst, nets, str(c.outer)))

    for o in chip.outputs:
        whole = PinRef(o.name, None, None, o.pos)
        for src, (lo, hi) in sources(whole):
            src_full = _with_bits(src, drivers, whole, lo, hi)
            dst = Endpoint(
                "output", o.name, bits=None if (lo, hi) == (0, o.width - 1) else (lo, hi)
            )
            nets = tuple(wires[f"{path}/{o.name}"][lo : hi + 1])
            edges.append(Edge(src_full, dst, nets, o.name))

    widths = {(pv.index, p.name): p.width for pv in parts for p in pv.inputs + pv.outputs}
    edges = [Edge(_whole(e.src, widths), _whole(e.dst, widths), e.nets, e.label) for e in edges]
    internal = {name: tuple(wires[f"{path}/{name}"]) for name in drivers if name not in pin_names}
    return ChipView(
        path=path,
        chip=chip.name,
        inputs=tuple(pin(p.name, p.width, path) for p in chip.inputs),
        outputs=tuple(pin(p.name, p.width, path) for p in chip.outputs),
        parts=tuple(parts),
        edges=tuple(edges),
        wires=internal,
    )


def _span(ref: PinRef, width: int) -> tuple[int, int]:
    if ref.lo is None or ref.hi is None:
        return 0, width - 1
    return ref.lo, ref.hi


def _with_bits(
    src: Endpoint,
    drivers: dict[str, list[Endpoint | None]],
    ref: PinRef,
    lo: int,
    hi: int,
) -> Endpoint:
    """Attach the driver-side bit range to a grouped source endpoint."""
    if src.kind != "part":
        return src
    first, last = drivers[ref.name][lo], drivers[ref.name][hi]
    assert first is not None and last is not None and first.bits and last.bits
    return Endpoint("part", src.pin, src.part, (first.bits[0], last.bits[1]))


def _whole(e: Endpoint, widths: dict[tuple[int, str], int]) -> Endpoint:
    """Drop a part endpoint's bit range when it covers the whole pin."""
    if e.kind == "part" and e.bits is not None and e.part is not None:
        if e.bits == (0, widths[(e.part, e.pin)] - 1):
            return Endpoint(e.kind, e.pin, e.part, None)
    return e
