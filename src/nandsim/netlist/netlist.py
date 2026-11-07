"""The flat, bit-level netlist that elaboration produces and the engine runs.

Every signal bit is a *net*, an integer index into the engine's value arrays.
Net 0 is constant false and net 1 is constant true. Gates are stored per
primitive kind as index arrays, one array per primitive pin, never as objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

FALSE_NET = 0
TRUE_NET = 1


@dataclass
class GateArrays:
    """All gates of one primitive kind: `inputs[k][g]` is the net on pin k of gate g."""

    inputs: list[np.ndarray]
    outputs: list[np.ndarray]

    @property
    def count(self) -> int:
        return len(self.outputs[0]) if self.outputs else 0


@dataclass
class LevelOp:
    """One vectorized step: evaluate the listed gates of one kind together."""

    kind: str
    inputs: list[np.ndarray]
    outputs: list[np.ndarray]


@dataclass
class Netlist:
    """A fully elaborated chip, ready to simulate.

    `inputs` and `outputs` map the top chip's pins to their nets, bit 0 first.
    `wires` maps every pin and internal wire at every level of the hierarchy,
    e.g. `Xor/n` or `Xor/Nand#2/out`, to its nets so the GUI can show them.
    `levels` is the combinational evaluation order. `gate_paths[kind][g]` is where
    gate g of a kind sits in the hierarchy, e.g. `Bit/DFF#5`, in `gates` order.
    """

    top: str
    num_nets: int
    gates: dict[str, GateArrays]
    inputs: dict[str, list[int]]
    outputs: dict[str, list[int]]
    wires: dict[str, list[int]]
    levels: list[list[LevelOp]] = field(default_factory=list)
    gate_paths: dict[str, list[str]] = field(default_factory=dict)

    @property
    def gate_count(self) -> int:
        return sum(g.count for g in self.gates.values())
