"""The flat, bit-level netlist that elaboration produces and the engine runs.

Every signal bit is a *net*, an integer index into the engine's value arrays.
Net 0 is constant false, net 1 constant true and net 2 the clock, which the
engine drives. Gates are stored per primitive kind as index arrays, one array
per primitive pin, never as objects.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

import numpy as np

FALSE_NET = 0
TRUE_NET = 1
CLOCK_NET = 2
FIXED_NETS = 3  # every chip's nets start with these, then come its input pins
SIGNAL_NETS = {"false": FALSE_NET, "true": TRUE_NET, "clock": CLOCK_NET}  # by HDL name


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
    """One vectorized step: evaluate the listed gates of one kind together.

    In a loop level, `loop[g]` numbers the feedback loop that gate g belongs to,
    counting from 0 within the level.
    """

    kind: str
    inputs: list[np.ndarray]
    outputs: list[np.ndarray]
    loop: np.ndarray | None = None


@dataclass
class Level:
    """Gates that depend only on earlier levels, and on each other in a loop level.

    A plain level is evaluated once. A loop level holds feedback loops, gates that
    depend on their own outputs: the engine evaluates it in rounds, one gate delay
    each, until nothing changes. `loops` is how many separate loops it holds.
    """

    ops: list[LevelOp]
    loops: int = 0

    @property
    def is_loop(self) -> bool:
        return self.loops > 0


@dataclass
class Netlist:
    """A fully elaborated chip, ready to simulate.

    `inputs` and `outputs` map the top chip's pins to their nets, bit 0 first.
    `wires` maps every pin and internal wire at every level of the hierarchy,
    e.g. `Xor/n` or `Xor/Nand#2/out`, to its nets so the GUI can show them.
    `levels` is the combinational evaluation order, feedback loops included.
    `gate_paths[kind][g]` is where gate g of a kind sits in the hierarchy, e.g.
    `Bit/DFF#5`, in `gates` order. Both are read-only and may be computed on demand:
    a large RAM has over a million wire paths.
    """

    top: str
    num_nets: int
    gates: dict[str, GateArrays]
    inputs: dict[str, list[int]]
    outputs: dict[str, list[int]]
    wires: Mapping[str, list[int]]
    levels: list[Level] = field(default_factory=list)
    gate_paths: Mapping[str, list[str]] = field(default_factory=dict)

    @property
    def gate_count(self) -> int:
        return sum(g.count for g in self.gates.values())

    @property
    def reads_clock(self) -> bool:
        """Whether a gate or an output reads the clock net, so tick and tock change it."""
        if any(CLOCK_NET in nets for nets in self.outputs.values()):
            return True
        return any(bool((col == CLOCK_NET).any()) for g in self.gates.values() for col in g.inputs)
