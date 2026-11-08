"""Elaboration: resolves a chip hierarchy into a flat netlist of primitives."""

from nandsim.netlist.elaborate import elaborate
from nandsim.netlist.levelize import net_names
from nandsim.netlist.library import ChipLibrary, Interface, interface_of
from nandsim.netlist.netlist import (
    CLOCK_NET,
    FALSE_NET,
    FIXED_NETS,
    SIGNAL_NETS,
    TRUE_NET,
    GateArrays,
    Level,
    LevelOp,
    Netlist,
)
from nandsim.netlist.primitives import PRIMITIVES, Primitive

__all__ = [
    "CLOCK_NET",
    "FALSE_NET",
    "FIXED_NETS",
    "PRIMITIVES",
    "SIGNAL_NETS",
    "TRUE_NET",
    "ChipLibrary",
    "GateArrays",
    "Interface",
    "Level",
    "LevelOp",
    "Netlist",
    "Primitive",
    "elaborate",
    "interface_of",
    "net_names",
]
