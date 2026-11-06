"""Elaboration: resolves a chip hierarchy into a flat netlist of primitives."""

from nandsim.netlist.elaborate import elaborate
from nandsim.netlist.library import ChipLibrary, Interface, interface_of
from nandsim.netlist.netlist import FALSE_NET, TRUE_NET, GateArrays, LevelOp, Netlist
from nandsim.netlist.primitives import PRIMITIVES, Primitive

__all__ = [
    "FALSE_NET",
    "PRIMITIVES",
    "TRUE_NET",
    "ChipLibrary",
    "GateArrays",
    "Interface",
    "LevelOp",
    "Netlist",
    "Primitive",
    "elaborate",
    "interface_of",
]
