"""Elaboration: flattens a chip hierarchy into a bit-level `Netlist` of primitives.

Each chip output bit and internal wire bit first gets a *placeholder* net. When a
part's output is connected to it, the placeholder is aliased to the part's real
output net; all aliases are resolved once at the end. This lets parts appear in
any order in PARTS, as in hardware.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from nandsim.hdl import Assign, ChipDef, Const, HdlError, Part, PinRef, SourcePos
from nandsim.netlist.levelize import levelize
from nandsim.netlist.library import ChipLibrary, Interface, interface_of
from nandsim.netlist.netlist import FALSE_NET, TRUE_NET, GateArrays, Netlist
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
    def __init__(self, lib: ChipLibrary) -> None:
        self.lib = lib
        self.next_net = 2
        self.gate_in: dict[str, list[list[int]]] = {}
        self.gate_out: dict[str, list[list[int]]] = {}
        self.gate_pos: dict[str, list[SourcePos]] = {}
        self.gate_paths: dict[str, list[str]] = {}
        self.alias: dict[int, int] = {}
        self.wires: dict[str, list[int]] = {}
        self.stack: list[str] = []

    def nets(self, n: int) -> list[int]:
        start = self.next_net
        self.next_net += n
        return list(range(start, start + n))

    # ---- instantiation -------------------------------------------------

    def instantiate(
        self,
        target: ChipDef | Primitive,
        path: str,
        in_nets: dict[str, list[int]],
        top_pos: SourcePos | None,
    ) -> dict[str, list[int]]:
        if isinstance(target, Primitive):
            return self._primitive(target, path, in_nets, top_pos)
        return self._chip(target, path, in_nets, top_pos)

    def _primitive(
        self,
        prim: Primitive,
        path: str,
        in_nets: dict[str, list[int]],
        top_pos: SourcePos | None,
    ) -> dict[str, list[int]]:
        kind = prim.name
        if kind not in self.gate_in:
            self.gate_in[kind] = [[] for _ in prim.inputs]
            self.gate_out[kind] = [[] for _ in prim.outputs]
            self.gate_pos[kind] = []
            self.gate_paths[kind] = []
        outs = {p: self.nets(1) for p in prim.outputs}
        for k, p in enumerate(prim.inputs):
            self.gate_in[kind][k].append(in_nets[p][0])
            self.wires[f"{path}/{p}"] = in_nets[p]
        for k, p in enumerate(prim.outputs):
            self.gate_out[kind][k].append(outs[p][0])
            self.wires[f"{path}/{p}"] = outs[p]
        assert top_pos is not None
        self.gate_pos[kind].append(top_pos)
        self.gate_paths[kind].append(path)
        return outs

    def _chip(
        self,
        chip: ChipDef,
        path: str,
        in_nets: dict[str, list[int]],
        top_pos: SourcePos | None,
    ) -> dict[str, list[int]]:
        self.stack.append(chip.name)
        scope = _Scope(chip, signals=dict(in_nets))
        for o in chip.outputs:
            scope.signals[o.name] = self.nets(o.width)
            scope.driven[o.name] = [None] * o.width

        # Pass 1: resolve every part and create the internal wires its outputs drive.
        resolved: list[tuple[ChipDef | Primitive, Interface]] = []
        for part in chip.parts:
            if part.chip in self.stack:
                chain = " -> ".join([*self.stack, part.chip])
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
            self._part(scope, part, target, iface, f"{path}/{part.chip}#{index}", top_pos)
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

        for name, nets in scope.signals.items():
            self.wires[f"{path}/{name}"] = nets
        self.stack.pop()
        return {o.name: scope.signals[o.name] for o in chip.outputs}

    def _part(
        self,
        scope: _Scope,
        part: Part,
        target: ChipDef | Primitive,
        iface: Interface,
        path: str,
        top_pos: SourcePos | None,
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

        ready = {p: [n for n in bits if n is not None] for p, bits in pin_nets.items()}
        outs = self.instantiate(target, path, ready, top_pos or part.pos)
        for inner, outer, lo, hi in outputs:
            self._bind(scope, part, inner, outer, outs[inner.name][lo : hi + 1])
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
            return [TRUE_NET if outer.value else FALSE_NET] * width
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
                        f"the width of new wire '{t.name}' can't come from a constant; "
                        f"connect the constant to a pin instead",
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
                f"output pin '{inner}' of {part.chip} cannot be connected to a constant",
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


def elaborate(top: ChipDef, lib: ChipLibrary) -> Netlist:
    """Flatten `top` and everything it uses into a levelized netlist.

    Raises `HdlError` for wiring mistakes (unknown chip or pin, wrong width,
    double drivers, unconnected pins, circular chip dependencies) and for
    combinational loops.
    """
    b = _Builder(lib)
    in_nets = {p.name: b.nets(p.width) for p in top.inputs}
    out_nets = b._chip(top, top.name, in_nets, None)
    mapping = b.resolve_map()

    def remap(nets: list[int]) -> list[int]:
        return [int(n) for n in mapping[np.asarray(nets, dtype=np.int64)]] if nets else []

    gates = {
        kind: GateArrays(
            inputs=[mapping[np.asarray(col, dtype=np.int64)] for col in b.gate_in[kind]],
            outputs=[np.asarray(col, dtype=np.int64) for col in b.gate_out[kind]],
        )
        for kind in b.gate_in
    }
    wires = {path: remap(nets) for path, nets in b.wires.items()}
    netlist = Netlist(
        top=top.name,
        num_nets=b.next_net,
        gates=gates,
        inputs={k: remap(v) for k, v in in_nets.items()},
        outputs={k: remap(v) for k, v in out_nets.items()},
        wires=wires,
        gate_paths=b.gate_paths,
    )
    netlist.levels = levelize(netlist, PRIMITIVES, b.gate_pos, top.pos)
    return netlist
