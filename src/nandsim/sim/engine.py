"""Three-valued, levelized simulation of a `Netlist` with vectorized numpy.

Each net has two boolean planes: `known` (is the value defined?) and `value`
(meaningful only where known; kept False elsewhere). NAND follows Kleene logic:
a known 0 on any input forces a known 1, even if the other input is undefined.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from nandsim.netlist import FALSE_NET, TRUE_NET, Netlist

Planes = tuple[np.ndarray, np.ndarray]  # (value, known)


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
        self.value = np.zeros(netlist.num_nets, dtype=bool)
        self.known = np.zeros(netlist.num_nets, dtype=bool)
        self.known[[FALSE_NET, TRUE_NET]] = True
        self.value[TRUE_NET] = True

    # ---- inputs and outputs -------------------------------------------

    def set(self, pin: str, value: int | None) -> None:
        """Set a top-level input. `None` makes it undefined. Bit 0 is the LSB."""
        nets = self._pin(pin, self.netlist.inputs, "input")
        idx = np.asarray(nets, dtype=np.int64)
        if value is None:
            self.known[idx] = False
            self.value[idx] = False
            return
        width = len(nets)
        if not 0 <= value < (1 << width):
            raise ValueError(f"value {value} does not fit in {width}-bit input '{pin}'")
        bits = (value >> np.arange(width)) & 1
        self.value[idx] = bits.astype(bool)
        self.known[idx] = True

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
        for level in self.netlist.levels:
            for op in level:
                ins = [(value[i], known[i]) for i in op.inputs]
                outs = EVALUATORS[op.kind](ins)
                for idx, (v, k) in zip(op.outputs, outs, strict=True):
                    value[idx] = v
                    known[idx] = k

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
