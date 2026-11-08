"""Three-valued, levelized simulation of a `Netlist` with vectorized numpy.

Each net has two boolean planes: `known` (is the value defined?) and `value`
(meaningful only where known; kept False elsewhere). NAND follows Kleene logic:
a known 0 on any input forces a known 1, even if the other input is undefined.

A plain level is evaluated once. A loop level (feedback loops, such as a latch
made of NANDs) is evaluated in rounds: every gate of the level reads the values
of the round before, as if each gate took one delay, until a round changes
nothing. A loop still changing after `MAX_ROUNDS` (or twice its size, if smaller)
oscillates: its nets go undefined and settle again from there, which always ends,
because from undefined Kleene logic can only learn values, never flip them.

The clock is net 2, readable from HDL as `clock`. It is 0 at power-on. `tick`
evaluates, latches every DFF's input, then raises the clock and evaluates again;
`tock` puts the latched values on the DFF outputs, lowers the clock and evaluates,
so a DFF gives `out(t) = in(t-1)`, and so does a flip-flop built from latches that
takes `in` while the clock is 1 and shows it while the clock is 0. DFFs start
undefined.

`tick` skips its first evaluation when nothing changed since the last one (no
`set`, `tock`, `reset` or `load_dff_state`): a step in the GUI or a `.tst` that
ticks right after a tock then costs one evaluation instead of two, or none for a
chip that doesn't read the clock. Write nets only through these methods, or the
skip can miss a change.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from nandsim.netlist import CLOCK_NET, FALSE_NET, PRIMITIVES, TRUE_NET, Level, Netlist

Planes = tuple[np.ndarray, np.ndarray]  # (value, known)

MAX_ROUNDS = 1000  # rounds a loop level may take to settle before it counts as oscillating


def _nand(ins: list[Planes]) -> list[Planes]:
    (va, ka), (vb, kb) = ins
    known = (ka & kb) | (ka & ~va) | (kb & ~vb)
    value = ~(va & vb) & known
    return [(value, known)]


# Combinational evaluators, keyed like the primitive table.
EVALUATORS: dict[str, Callable[[list[Planes]], list[Planes]]] = {"Nand": _nand}


class Simulator:
    """Holds the state of every net and evaluates the netlist level by level."""

    def __init__(self, netlist: Netlist) -> None:
        self.netlist = netlist
        # Every primitive marked sequential (levelization leaves them all out) is a
        # D flip-flop: one input latched on tick, one output updated on tock.
        kinds = [k for k in netlist.gates if PRIMITIVES[k].sequential]
        clocked = [netlist.gates[k] for k in kinds]
        self._dff_paths = [p for k in kinds for p in netlist.gate_paths.get(k, [])]
        empty = np.zeros(0, dtype=np.int64)
        self._dff_in = np.concatenate([g.inputs[0] for g in clocked]) if clocked else empty
        self._dff_out = np.concatenate([g.outputs[0] for g in clocked]) if clocked else empty
        self.reads_clock = netlist.reads_clock
        self.reset()

    # ---- inputs and outputs -------------------------------------------

    def set(self, pin: str, value: int | None) -> None:
        """Set a top-level input. `None` makes it undefined. Bit 0 is the LSB."""
        nets = self._pin(pin, self.netlist.inputs, "input")
        idx = np.asarray(nets, dtype=np.int64)
        if value is None:
            self.known[idx] = False
            self.value[idx] = False
            self._stale = True
            return
        width = len(nets)
        if not 0 <= value < (1 << width):
            raise ValueError(f"value {value} does not fit in {width}-bit input '{pin}'")
        bits = (value >> np.arange(width)) & 1
        self.value[idx] = bits.astype(bool)
        self.known[idx] = True
        self._stale = True

    def get(self, pin: str) -> int | None:
        """Read a top-level output (or input) as an integer; `None` if any bit is undefined."""
        nets = self.netlist.outputs.get(pin) or self._pin(pin, self.netlist.inputs, "pin")
        return self._read(nets)

    def get_bits(self, pin: str) -> list[int | None]:
        """Per-bit view of a top-level pin, LSB first; `None` for undefined bits."""
        nets = self.netlist.outputs.get(pin) or self._pin(pin, self.netlist.inputs, "pin")
        return [int(self.value[n]) if self.known[n] else None for n in nets]

    def wire(self, path: str) -> int | None:
        """Read any wire in the hierarchy, e.g. `Xor/n` or `Xor/Nand#2/out`."""
        nets = self.netlist.wires.get(path)
        if nets is None:
            raise KeyError(f"no wire '{path}'")
        return self._read(nets)

    # ---- evaluation ----------------------------------------------------

    def eval(self) -> None:
        """Propagate inputs through all combinational logic, one vectorized step per level."""
        value, known = self.value, self.known
        unsettled: list[np.ndarray] = []
        for level in self.netlist.levels:
            if level.is_loop:
                bad = self._settle(level)
                if bad is not None:
                    unsettled.append(bad)
                continue
            for op in level.ops:
                ins = [(value[i], known[i]) for i in op.inputs]
                outs = EVALUATORS[op.kind](ins)
                for idx, (v, k) in zip(op.outputs, outs, strict=True):
                    value[idx] = v
                    known[idx] = k
        self.unsettled = np.concatenate(unsettled) if unsettled else np.zeros(0, np.int64)
        self._stale = False

    def tick(self) -> None:
        """First half of a clock cycle: evaluate, every DFF latches its input, clock rises."""
        if self._stale:
            self.eval()
        self._latch_value = self.value[self._dff_in]
        self._latch_known = self.known[self._dff_in]
        self.value[CLOCK_NET] = True
        if self.reads_clock:
            self.eval()
        self.mid_cycle = True

    def tock(self) -> None:
        """Second half: DFF outputs take the values latched at the last tick, clock falls.

        Before any tick the latches hold undefined, so a lone tock leaves DFFs undefined.
        """
        self.value[self._dff_out] = self._latch_value
        self.known[self._dff_out] = self._latch_known
        self.value[CLOCK_NET] = False
        self.eval()
        self.cycle += 1
        self.mid_cycle = False

    def reset(self) -> None:
        """Back to power-on: every input, wire and DFF undefined, clock 0, cycle 0."""
        self.value = np.zeros(self.netlist.num_nets, dtype=bool)
        self.known = np.zeros(self.netlist.num_nets, dtype=bool)
        self.known[[FALSE_NET, TRUE_NET, CLOCK_NET]] = True
        self.value[TRUE_NET] = True
        self._latch_value = np.zeros(len(self._dff_out), dtype=bool)
        self._latch_known = np.zeros(len(self._dff_out), dtype=bool)
        self.cycle = 0  # completed clock cycles (tocks) since power-on
        self._stale = True  # nets may not match the inputs: the next tick must evaluate
        self.mid_cycle = False  # True between a tick and its tock
        self.unsettled = np.zeros(0, np.int64)  # nets a loop left undefined at the last eval

    @property
    def clocked(self) -> bool:
        """Whether the clock does anything: the chip has DFFs or reads `clock`."""
        return self.dff_count > 0 or self.reads_clock

    @property
    def dff_count(self) -> int:
        """How many DFFs the clock updates."""
        return len(self._dff_out)

    @property
    def dff_paths(self) -> list[str]:
        """Where each DFF sits in the hierarchy, e.g. `Reg2/Bit#1/DFF#5`, in clock order."""
        return list(self._dff_paths)

    @property
    def dff_outputs(self) -> np.ndarray:
        """The output net of each DFF, in the order `dff_state` uses."""
        return self._dff_out.copy()

    def dff_state(self) -> Planes:
        """What every DFF outputs now, as (value, known) copies in `dff_outputs` order."""
        return self.value[self._dff_out], self.known[self._dff_out]

    def load_dff_state(self, which: np.ndarray, value: np.ndarray, known: np.ndarray) -> None:
        """Make DFFs `which` (indices into `dff_outputs`) hold these values, latched too.

        For carrying state into a rebuilt chip; call `eval()` afterwards to propagate it.
        """
        nets = self._dff_out[which]
        self.value[nets] = value & known
        self.known[nets] = known
        self._latch_value[which] = value & known
        self._latch_known[which] = known
        self._stale = True

    # ---- feedback loops ------------------------------------------------

    def _round(self, level: Level) -> list[np.ndarray] | None:
        """One gate delay over a loop level: every gate reads the previous round.

        Returns, per op, which gates changed their output; None if none did.
        """
        value, known = self.value, self.known
        results = [
            EVALUATORS[op.kind]([(value[i], known[i]) for i in op.inputs]) for op in level.ops
        ]
        masks: list[np.ndarray] = []
        changed = False
        for op, outs in zip(level.ops, results, strict=True):
            mask = np.zeros(len(op.outputs[0]), dtype=bool)
            for idx, (v, k) in zip(op.outputs, outs, strict=True):
                mask |= (value[idx] != v) | (known[idx] != k)
                value[idx] = v
                known[idx] = k
            masks.append(mask)
            changed = changed or bool(mask.any())
        return masks if changed else None

    def _settle(self, level: Level) -> np.ndarray | None:
        """Run a loop level until it settles. Returns the nets of loops that oscillated."""
        gates = sum(len(op.outputs[0]) for op in level.ops)
        masks = None
        for _ in range(min(2 * gates + 4, MAX_ROUNDS)):
            masks = self._round(level)
            if masks is None:
                return None
        assert masks is not None
        bad = np.zeros(level.loops, dtype=bool)
        for op, mask in zip(level.ops, masks, strict=True):
            assert op.loop is not None
            bad[op.loop[mask]] = True
        nets: list[np.ndarray] = []
        for op in level.ops:
            assert op.loop is not None
            sel = bad[op.loop]
            for out in op.outputs:
                nets.append(out[sel])
        lost = np.concatenate(nets)
        self.value[lost] = False
        self.known[lost] = False
        # From undefined every round only adds known values, so this ends.
        for _ in range(len(lost) + 2):
            if self._round(level) is None:
                return lost[~self.known[lost]]
        raise AssertionError("a loop level did not settle from undefined")

    # ---- helpers -------------------------------------------------------

    @staticmethod
    def _pin(pin: str, table: dict[str, list[int]], what: str) -> list[int]:
        nets = table.get(pin)
        if nets is None:
            raise KeyError(f"no {what} '{pin}'")
        return nets

    def _read(self, nets: list[int]) -> int | None:
        idx = np.asarray(nets, dtype=np.int64)
        if not self.known[idx].all():
            return None
        bits = self.value[idx].astype(np.int64)
        return int((bits << np.arange(len(nets), dtype=np.int64)).sum())
