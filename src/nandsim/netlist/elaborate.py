"""Elaboration: flattens a chip hierarchy into a bit-level `Netlist` of primitives.

Each distinct chip is compiled once into a `_Template`: its flattened gates and
wires in a numbering of its own, where nets 0 and 1 are the constants, then come
its input bits, then its internal nets. A part is instantiated by giving the
part's internal nets a fresh block in the parent and remapping the part's
template with one numpy index per array, so a chip used 4,000 times in a RAM is
checked and wired once, not 4,000 times. Templates are cached per `ChipLibrary`
and are valid exactly as long as its parse cache.

Inside one chip, each output bit and internal wire bit first gets a *placeholder*
net. When a part's output is connected to it, the placeholder is aliased to the
part's real output net; aliases are resolved, and placeholders dropped, when the
chip's template is finished. This lets parts appear in any order in PARTS, as in
hardware.

`Netlist.wires` and `Netlist.gate_paths` are lazy views over the template tree:
a DataRAM has over a million wire paths, and the GUI looks up a few at a time.
"""

from __future__ import annotations

import weakref
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field

import numpy as np

from nandsim.hdl import Assign, ChipDef, Const, HdlError, Part, PinRef, SourcePos
from nandsim.netlist.levelize import levelize
from nandsim.netlist.library import ChipLibrary, Interface, interface_of
from nandsim.netlist.netlist import (
    CLOCK_NET,
    FALSE_NET,
    FIXED_NETS,
    SIGNAL_NETS,
    TRUE_NET,
    GateArrays,
    Netlist,
)
from nandsim.netlist.primitives import PRIMITIVES, Primitive


@dataclass
class _Driver:
    part: str
    pos: SourcePos


@dataclass
class _Scope:
    """Signals visible inside one chip instance while it is being elaborated."""

    chip: ChipDef
    signals: dict[str, list[int]] = field(default_factory=dict)
    driven: dict[str, list[_Driver | None]] = field(default_factory=dict)
    labels: dict[str, tuple[Part, Interface]] = field(default_factory=dict)


@dataclass
class _Template:
    """One chip, flattened and checked once, in its own net numbering.

    Nets 0, 1 and 2 are false, true and the clock, `3 .. 3 + input_bits - 1` the input pins in
    declaration order, the rest its internal nets (every gate output inside it).
    `parts` maps each part's path segment (`Nand#2`) to the part's template and the
    map from the part's nets to this chip's nets. `wires` holds only this chip's
    own signals, or a primitive's pins. `gate_pos[kind][g]` is the PARTS line that
    holds gate g. All arrays are read-only: templates are shared between netlists.
    """

    name: str
    primitive: bool
    num_nets: int
    input_bits: int
    outputs: dict[str, np.ndarray]
    gates: dict[str, GateArrays]
    gate_pos: dict[str, list[SourcePos]]
    wires: dict[str, np.ndarray]
    parts: dict[str, tuple[_Template, np.ndarray]]
    wire_count: int  # entries in `wires` here and in every part below


def _frozen(a: np.ndarray) -> np.ndarray:
    a.flags.writeable = False
    return a


def _primitive_template(prim: Primitive) -> _Template:
    n_in, n_out = len(prim.inputs), len(prim.outputs)
    ins = [_frozen(np.array([FIXED_NETS + k], dtype=np.int64)) for k in range(n_in)]
    outs = [_frozen(np.array([FIXED_NETS + n_in + k], dtype=np.int64)) for k in range(n_out)]
    pins = dict(zip(prim.inputs, ins, strict=True)) | dict(zip(prim.outputs, outs, strict=True))
    return _Template(
        name=prim.name,
        primitive=True,
        num_nets=FIXED_NETS + n_in + n_out,
        input_bits=n_in,
        outputs=dict(zip(prim.outputs, outs, strict=True)),
        gates={prim.name: GateArrays(inputs=ins, outputs=outs)},
        gate_pos={},  # a primitive is never the top chip: its parent supplies the line
        wires=pins,
        parts={},
        wire_count=len(pins),
    )


_PRIMITIVE_TEMPLATES = {name: _primitive_template(p) for name, p in PRIMITIVES.items()}

# Compiled chips per library, keyed by the identity of the parsed `ChipDef` (the
# library hands out one per name). Weak, so a dropped library drops its templates.
_CACHES: weakref.WeakKeyDictionary[ChipLibrary, dict[int, tuple[ChipDef, _Template]]] = (
    weakref.WeakKeyDictionary()
)


class _Compiler:
    """Builds templates depth first, reusing the library's cache."""

    def __init__(self, lib: ChipLibrary) -> None:
        self.lib = lib
        self.cache = _CACHES.setdefault(lib, {})
        self.stack: list[str] = []  # chips being compiled, outermost first

    def template(self, target: ChipDef | Primitive) -> _Template:
        if isinstance(target, Primitive):
            return _PRIMITIVE_TEMPLATES[target.name]
        hit = self.cache.get(id(target))
        if hit is not None and hit[0] is target:
            return hit[1]
        self.stack.append(target.name)
        try:
            t = _Builder(self, target).build()
        finally:
            self.stack.pop()
        self.cache[id(target)] = (target, t)
        return t


def _bit_ranges(bits: list[int]) -> str:
    """[0, 1, 2, 5] -> '0..2, 5'."""
    out: list[str] = []
    start = prev = bits[0]
    for b in bits[1:] + [-2]:
        if b != prev + 1:
            out.append(str(start) if start == prev else f"{start}..{prev}")
            start = b
        prev = b
    return ", ".join(out)


def _bits(bits: list[int]) -> str:
    return f"bit {bits[0]}" if len(bits) == 1 else f"bits {_bit_ranges(bits)}"


def _verb(bits: list[int]) -> str:
    return "is" if len(bits) == 1 else "are"


class _Builder:
    """Compiles one chip into a `_Template`, given its parts' templates."""

    def __init__(self, compiler: _Compiler, chip: ChipDef) -> None:
        self.compiler = compiler
        self.lib = compiler.lib
        self.chip = chip
        self.next_net = FIXED_NETS
        self.alias: dict[int, int] = {}
        self.parts: list[tuple[str, Part, _Template, np.ndarray]] = []

    def nets(self, n: int) -> list[int]:
        start = self.next_net
        self.next_net += n
        return list(range(start, start + n))

    # ---- the chip ------------------------------------------------------

    def build(self) -> _Template:
        chip = self.chip
        scope = _Scope(chip, signals={p.name: self.nets(p.width) for p in chip.inputs})
        input_bits = self.next_net - FIXED_NETS
        for o in chip.outputs:
            scope.signals[o.name] = self.nets(o.width)
            scope.driven[o.name] = [None] * o.width

        # Pass 1: resolve every part and create the internal wires its outputs drive.
        resolved: list[tuple[ChipDef | Primitive, Interface]] = []
        for part in chip.parts:
            if part.chip in self.compiler.stack:
                chain = " -> ".join([*self.compiler.stack, part.chip])
                raise HdlError(f"circular dependency between chips: {chain}", part.pos)
            target = self.lib.resolve(part.chip, part.pos)
            iface = interface_of(target)
            resolved.append((target, iface))
            if part.label is not None:
                self._add_label(scope, part, iface)
            for c in part.connections:
                width = iface.width(c.inner.name)
                if width is None:
                    raise HdlError(
                        f"{part.chip} has no pin '{c.inner.name}' "
                        f"(its pins are: {iface.pin_list()})",
                        c.inner.pos,
                    )
                lo, hi = self._bounds(c.inner, width, f"pin '{c.inner.name}' of {part.chip}")
                outer = c.outer
                is_new_wire = (
                    c.inner.name in iface.outputs
                    and isinstance(outer, PinRef)
                    and outer.part is None
                    and outer.name not in scope.signals
                )
                if is_new_wire:
                    assert isinstance(outer, PinRef)
                    if outer.sliced:
                        raise HdlError(
                            f"internal wire '{outer.name}' cannot be sliced where it is "
                            f"created; write '{c.inner}={outer.name}'",
                            outer.pos,
                        )
                    scope.signals[outer.name] = self.nets(hi - lo + 1)
                    scope.driven[outer.name] = [None] * (hi - lo + 1)

        self._create_assigned_wires(scope)

        # Pass 2: connect inputs, instantiate each part, bind its outputs, then assignments.
        for index, (part, (target, iface)) in enumerate(
            zip(chip.parts, resolved, strict=True), start=1
        ):
            self._part(scope, part, target, iface, f"{part.chip}#{index}")
        for a in chip.assigns:
            self._assign(scope, a)

        for o in chip.outputs:
            missing = [b for b, d in enumerate(scope.driven[o.name]) if d is None]
            if missing:
                if len(missing) == o.width:
                    msg = f"output pin '{o.name}' of {chip.name} is not connected"
                else:
                    msg = (
                        f"{_bits(missing)} of output pin '{o.name}' "
                        f"of {chip.name} {_verb(missing)} not connected"
                    )
                raise HdlError(msg, o.pos)

        return self._finish(scope, input_bits)

    def _part(
        self,
        scope: _Scope,
        part: Part,
        target: ChipDef | Primitive,
        iface: Interface,
        seg: str,
    ) -> None:
        pin_nets: dict[str, list[int | None]] = {p: [None] * w for p, w in iface.inputs.items()}
        outputs: list[tuple[PinRef, PinRef | Const, int, int]] = []
        for c in part.connections:
            width = iface.width(c.inner.name)
            assert width is not None
            lo, hi = self._bounds(c.inner, width, f"pin '{c.inner.name}' of {part.chip}")
            if c.inner.name in iface.inputs:
                src = self._source(scope, c.outer, hi - lo + 1, c.inner, part.chip)
                bits = pin_nets[c.inner.name]
                for k, net in enumerate(src):
                    if bits[lo + k] is not None:
                        raise HdlError(
                            f"pin '{c.inner}' of {part.chip} is connected more than once",
                            c.inner.pos,
                        )
                    bits[lo + k] = net
            else:
                outputs.append((c.inner, c.outer, lo, hi))

        for pin, bits in pin_nets.items():
            missing = [b for b, n in enumerate(bits) if n is None]
            if missing:
                if len(missing) == len(bits):
                    msg = f"input pin '{pin}' of {part.chip} is not connected"
                else:
                    msg = (
                        f"{_bits(missing)} of input pin '{pin}' "
                        f"of {part.chip} {_verb(missing)} not connected"
                    )
                raise HdlError(msg, part.pos)

        # Instantiate: the part's inputs come from here, its internal nets get a new block.
        sub = self.compiler.template(target)
        inner = sub.num_nets - FIXED_NETS - sub.input_bits
        start = self.next_net
        self.next_net += inner
        ins = [n for bits in pin_nets.values() for n in bits if n is not None]
        net_map = np.concatenate(
            [
                np.array([FALSE_NET, TRUE_NET, CLOCK_NET, *ins], dtype=np.int64),
                np.arange(start, start + inner, dtype=np.int64),
            ]
        )
        self.parts.append((seg, part, sub, net_map))
        outs = {p: net_map[nets].tolist() for p, nets in sub.outputs.items()}

        for inner_ref, outer, lo, hi in outputs:
            self._bind(scope, part, inner_ref, outer, outs[inner_ref.name][lo : hi + 1])
        if part.label is not None:
            for pin, nets in outs.items():
                key = f"{part.label}.{pin}"
                for k, net in enumerate(nets):
                    self.alias[scope.signals[key][k]] = net
                    scope.driven[key][k] = _Driver(part.chip, part.pos)

    # ---- helpers -------------------------------------------------------

    @staticmethod
    def _bounds(ref: PinRef, width: int, what: str) -> tuple[int, int]:
        if ref.lo is None or ref.hi is None:
            return 0, width - 1
        if ref.hi >= width:
            raise HdlError(
                f"{ref} is out of range: {what} has {width} bit{'s' if width > 1 else ''} "
                f"(0..{width - 1})",
                ref.pos,
            )
        return ref.lo, ref.hi

    def _source(
        self, scope: _Scope, outer: PinRef | Const, width: int, inner: PinRef, part: str
    ) -> list[int]:
        return self._read(scope, outer, width, f"pin '{inner}' of {part}")

    def _read(self, scope: _Scope, outer: PinRef | Const, width: int, what: str) -> list[int]:
        """The nets of a signal read by `what`, which has `width` bits."""
        if isinstance(outer, Const):
            return [SIGNAL_NETS[outer.name]] * width
        self._check_part_ref(scope, outer)
        nets = scope.signals.get(outer.key)
        if nets is None:
            raise HdlError(
                f"'{outer.name}' is not a pin of {scope.chip.name} and nothing drives a "
                f"wire with that name",
                outer.pos,
            )
        lo, hi = self._bounds(outer, len(nets), f"'{outer.key}'")
        if hi - lo + 1 != width:
            raise HdlError(
                f"width mismatch: {what} has {width} bit"
                f"{'s' if width > 1 else ''} but '{outer}' has {hi - lo + 1}",
                outer.pos,
            )
        return nets[lo : hi + 1]

    def _check_part_ref(self, scope: _Scope, ref: PinRef) -> None:
        """Errors for `label.pin` references that don't name a labelled part's output."""
        if ref.part is None:
            return
        found = scope.labels.get(ref.part)
        if found is None:
            raise HdlError(f"no part is labelled '{ref.part}' in {scope.chip.name}", ref.pos)
        part, iface = found
        if ref.name in iface.inputs:
            raise HdlError(
                f"'{ref.key}' is an input pin of {part.chip}: only a part's outputs can be "
                f"read this way",
                ref.pos,
            )
        if ref.name not in iface.outputs:
            raise HdlError(
                f"{part.chip} has no pin '{ref.name}' (its pins are: {iface.pin_list()})",
                ref.pos,
            )

    def _add_label(self, scope: _Scope, part: Part, iface: Interface) -> None:
        label = part.label
        assert label is not None
        if label in scope.labels:
            first = scope.labels[label][0]
            raise HdlError(
                f"label '{label}' is already used at line {first.pos.line}", part.label_pos
            )
        if scope.chip.pin(label) is not None:
            raise HdlError(
                f"label '{label}' is also a pin of {scope.chip.name}; use another name",
                part.label_pos,
            )
        scope.labels[label] = (part, iface)
        for pin, width in iface.outputs.items():
            scope.signals[f"{label}.{pin}"] = self.nets(width)
            scope.driven[f"{label}.{pin}"] = [None] * width

    def _create_assigned_wires(self, scope: _Scope) -> None:
        """Create the new internal wires that assignments drive, taking the source's width."""
        pending = [
            a
            for a in scope.chip.assigns
            if a.target.part is None
            and a.target.name not in scope.signals
            and scope.chip.pin(a.target.name) is None
        ]
        while pending:
            progress = False
            for a in list(pending):
                t, src = a.target, a.source
                if t.name in scope.signals:  # created by an earlier assignment this round
                    pending.remove(a)
                    continue
                if t.sliced:
                    raise HdlError(
                        f"internal wire '{t.name}' cannot be sliced where it is created; "
                        f"write '{t.name} = ...'",
                        t.pos,
                    )
                if isinstance(src, Const):
                    raise HdlError(
                        f"the width of new wire '{t.name}' can't come from {src.what}; "
                        f"connect {'the clock' if src.name == 'clock' else 'the constant'} "
                        f"to a pin instead",
                        src.pos,
                    )
                if src.key not in scope.signals:
                    continue  # its source may be created by another assignment
                self._check_part_ref(scope, src)
                lo, hi = self._bounds(src, len(scope.signals[src.key]), f"'{src.key}'")
                scope.signals[t.name] = self.nets(hi - lo + 1)
                scope.driven[t.name] = [None] * (hi - lo + 1)
                pending.remove(a)
                progress = True
            if not progress:
                break  # the remaining sources don't exist; _assign reports them

    def _assign(self, scope: _Scope, a: Assign) -> None:
        t = a.target
        if t.part is not None:
            raise HdlError(f"'{t.key}' is driven by part '{t.part}' and cannot be assigned", t.pos)
        if scope.chip.is_input(t.name):
            raise HdlError(
                f"'{t.name}' is an input pin of {scope.chip.name}: it cannot be assigned", t.pos
            )
        nets = scope.signals.get(t.name)
        if nets is None:  # its source was missing: report that
            self._read(scope, a.source, 1, f"'{t}'")
            raise AssertionError("unreachable")
        lo, hi = self._bounds(t, len(nets), f"'{t.name}'")
        src = self._read(scope, a.source, hi - lo + 1, f"'{t}'")
        driven = scope.driven[t.name]
        for b in range(lo, hi + 1):
            prev = driven[b]
            if prev is not None:
                raise HdlError(
                    f"'{t}' is already driven by {prev.part} at line {prev.pos.line}", t.pos
                )
        for k, net in enumerate(src):
            target = nets[lo + k]
            n = net
            while True:  # an assignment chain must not lead back to its own target
                if n == target:
                    raise HdlError(
                        f"'{t}' would be driven only by itself: assignments form a loop "
                        f"with nothing driving it",
                        t.pos,
                    )
                if n not in self.alias:
                    break
                n = self.alias[n]
            self.alias[target] = net
            driven[lo + k] = _Driver("the connection", a.pos)

    def _bind(
        self,
        scope: _Scope,
        part: Part,
        inner: PinRef,
        outer: PinRef | Const,
        part_nets: list[int],
    ) -> None:
        if isinstance(outer, Const):
            raise HdlError(
                f"output pin '{inner}' of {part.chip} cannot be connected to {outer.what}",
                outer.pos,
            )
        if outer.part is not None:
            raise HdlError(
                f"'{outer.key}' is driven by part '{outer.part}' and cannot be driven again",
                outer.pos,
            )
        if scope.chip.is_input(outer.name):
            raise HdlError(
                f"'{outer.name}' is an input pin of {scope.chip.name}: a part output "
                f"cannot drive it",
                outer.pos,
            )
        nets = scope.signals[outer.name]
        lo, hi = self._bounds(outer, len(nets), f"'{outer.name}'")
        driven = scope.driven[outer.name]
        for b in range(lo, hi + 1):
            prev = driven[b]
            if prev is not None:
                raise HdlError(
                    f"'{outer}' is already driven by {prev.part} at line {prev.pos.line}",
                    outer.pos,
                )
        if hi - lo + 1 != len(part_nets):
            raise HdlError(
                f"width mismatch: pin '{inner}' of {part.chip} has {len(part_nets)} bit"
                f"{'s' if len(part_nets) > 1 else ''} but '{outer}' has {hi - lo + 1}",
                outer.pos,
            )
        for k, net in enumerate(part_nets):
            self.alias[nets[lo + k]] = net
            driven[lo + k] = _Driver(part.chip, part.pos)

    # ---- finish --------------------------------------------------------

    def resolve_map(self) -> np.ndarray:
        """Net -> final net, following placeholder aliases to the real driver."""
        mapping = np.arange(self.next_net, dtype=np.int64)
        if self.alias:
            src = np.fromiter(self.alias.keys(), dtype=np.int64)
            dst = np.fromiter(self.alias.values(), dtype=np.int64)
            mapping[src] = dst
        for _ in range(64):
            nxt = mapping[mapping]
            if np.array_equal(nxt, mapping):
                return mapping
            mapping = nxt
        raise HdlError("internal error: unresolved wire aliases", None)

    def _finish(self, scope: _Scope, input_bits: int) -> _Template:
        """Resolve aliases, renumber without the placeholders, and merge the parts' gates."""
        resolved = self.resolve_map()
        keep = np.unique(resolved)  # sorted: the constants and inputs come first, unaliased
        renumber = np.full(self.next_net, -1, dtype=np.int64)
        renumber[keep] = np.arange(len(keep), dtype=np.int64)
        final = renumber[resolved]
        assert np.array_equal(final[: FIXED_NETS + input_bits], np.arange(FIXED_NETS + input_bits))

        ins: dict[str, list[list[np.ndarray]]] = {}
        outs: dict[str, list[list[np.ndarray]]] = {}
        gate_pos: dict[str, list[SourcePos]] = {}
        parts: dict[str, tuple[_Template, np.ndarray]] = {}
        for seg, part, sub, raw_map in self.parts:
            net_map = _frozen(final[raw_map])
            parts[seg] = (sub, net_map)
            for kind, g in sub.gates.items():
                if kind not in ins:
                    ins[kind] = [[] for _ in g.inputs]
                    outs[kind] = [[] for _ in g.outputs]
                    gate_pos[kind] = []
                for col, acc in zip(g.inputs, ins[kind], strict=True):
                    acc.append(net_map[col])
                for col, acc in zip(g.outputs, outs[kind], strict=True):
                    acc.append(net_map[col])
                gate_pos[kind] += [part.pos] * g.count

        def merged(cols: list[list[np.ndarray]]) -> list[np.ndarray]:
            return [_frozen(np.concatenate(c)) for c in cols]

        wires = {
            name: _frozen(final[np.asarray(nets, dtype=np.int64)])
            for name, nets in scope.signals.items()
        }
        return _Template(
            name=self.chip.name,
            primitive=False,
            num_nets=len(keep),
            input_bits=input_bits,
            outputs={o.name: wires[o.name] for o in self.chip.outputs},
            gates={k: GateArrays(merged(ins[k]), merged(outs[k])) for k in ins},
            gate_pos=gate_pos,
            wires=wires,
            parts=parts,
            wire_count=len(wires) + sum(sub.wire_count for sub, _ in parts.values()),
        )


class WireMap(Mapping[str, list[int]]):
    """`Netlist.wires`: every wire path in the hierarchy -> its nets, looked up on demand.

    A path such as `Xor/Nand#2/out` walks the templates from the top chip and maps
    the wire's nets back up through each part. Iteration lists every path, parts
    before the chip that holds them.
    """

    def __init__(self, top: str, template: _Template) -> None:
        self._top = top
        self._t = template

    def _lookup(self, path: str) -> np.ndarray | None:
        head, _, rest = path.partition("/")
        if head != self._top or not rest:
            return None
        *segs, name = rest.split("/")
        t = self._t
        maps: list[np.ndarray] = []
        for seg in segs:
            entry = t.parts.get(seg)
            if entry is None:
                return None
            t, net_map = entry
            maps.append(net_map)
        nets = t.wires.get(name)
        if nets is None:
            return None
        for net_map in reversed(maps):
            nets = net_map[nets]
        return nets

    def __getitem__(self, path: str) -> list[int]:
        nets = self._lookup(path)
        if nets is None:
            raise KeyError(path)
        return nets.tolist()

    def __contains__(self, path: object) -> bool:
        return isinstance(path, str) and self._lookup(path) is not None

    def __len__(self) -> int:
        return self._t.wire_count

    def __iter__(self) -> Iterator[str]:
        for path, _ in self.walk():
            yield path

    def walk(self) -> Iterator[tuple[str, np.ndarray]]:
        """Every (path, nets) pair, mapping whole templates at once: faster than lookups."""

        def go(
            t: _Template, prefix: str, to_top: np.ndarray | None
        ) -> Iterator[tuple[str, np.ndarray]]:
            for seg, (sub, net_map) in t.parts.items():
                yield from go(
                    sub, f"{prefix}/{seg}", net_map if to_top is None else to_top[net_map]
                )
            for name, nets in t.wires.items():
                yield f"{prefix}/{name}", nets if to_top is None else to_top[nets]

        return go(self._t, self._top, None)


class GatePaths(Mapping[str, list[str]]):
    """`Netlist.gate_paths`: kind -> where each gate sits, e.g. `Bit/DFF#5`, built per kind."""

    def __init__(self, top: str, template: _Template) -> None:
        self._top = top
        self._t = template
        self._done: dict[str, list[str]] = {}

    def __getitem__(self, kind: str) -> list[str]:
        if kind not in self._t.gates:
            raise KeyError(kind)
        if kind not in self._done:
            out: list[str] = []

            def go(t: _Template, prefix: str) -> None:
                if t.primitive:
                    out.append(prefix)
                    return
                for seg, (sub, _) in t.parts.items():
                    if kind in sub.gates:
                        go(sub, f"{prefix}/{seg}")

            go(self._t, self._top)
            self._done[kind] = out
        return self._done[kind]

    def __len__(self) -> int:
        return len(self._t.gates)

    def __iter__(self) -> Iterator[str]:
        return iter(self._t.gates)


def elaborate(top: ChipDef, lib: ChipLibrary) -> Netlist:
    """Flatten `top` and everything it uses into a levelized netlist.

    Raises `HdlError` for wiring mistakes (unknown chip or pin, wrong width,
    double drivers, unconnected pins, circular chip dependencies).
    """
    t = _Compiler(lib).template(top)
    netlist = Netlist(
        top=top.name,
        num_nets=t.num_nets,
        gates={k: GateArrays(list(g.inputs), list(g.outputs)) for k, g in t.gates.items()},
        inputs={p.name: t.wires[p.name].tolist() for p in top.inputs},
        outputs={k: v.tolist() for k, v in t.outputs.items()},
        wires=WireMap(top.name, t),
        gate_paths=GatePaths(top.name, t),
    )
    netlist.levels = levelize(netlist, PRIMITIVES)
    return netlist
