"""Each tip is pinned to a real build error, so rewording an error can't silently drop its tip."""

from __future__ import annotations

import pytest

from nandsim.gui.tips import tip_for
from nandsim.netlist import ChipLibrary
from nandsim.testing import find_level, parse_tst, run_script

NOT = find_level("Not")
assert NOT is not None


def build_error(parts: str, pins: str = "IN in; OUT out;", head: str = "CHIP Not") -> str:
    src = f"{head} {{ {pins} PARTS: {parts} }}"
    lib = ChipLibrary([NOT.root / "reference"], sources={"Not": (src, "Not.hdl")})
    result = run_script(parse_tst(NOT.tst.read_text(), "Not.tst"), lib, NOT)
    assert result.error is not None, "expected a build error"
    return result.error.message


CASES = [
    (
        build_error(""),
        "Every OUT pin needs a driver: end a part with out=out, or write out = <signal>;",
    ),
    (
        build_error("Nand(a=in, out=out);"),
        "Every input of a part needs a value: add b=<signal> inside Nand(...). "
        "A signal can be a pin, a wire, true or false.",
    ),
    (
        build_error("Nand(a=in, c=in, out=out);"),
        "In Nand(pin=signal), the left side is one of Nand's own pins (a, b, out); "
        "the right side is a signal of your chip.",
    ),
    (
        build_error("Not(in=in, out=out);"),
        "A chip can't be built from itself: use the smaller parts listed in the brief.",
    ),
    (
        build_error("And(a=in, b=in, out=out);"),
        "Only the parts in the brief and your exported chips can be used here. "
        "Names are case-sensitive.",
    ),
    (
        build_error("Nand(a=in, b=x, out=out);"),
        "To read the wire 'x', some part must write it first (out=x). Check the spelling too.",
    ),
    (
        build_error("Nand(a=in, b=in, out=out); Nand(a=in, b=in, out=out);"),
        "A signal has exactly one source. Send the second output to a new wire name.",
    ),
    (
        build_error("Nand(a=in, b=y, out=y); Nand(a=y, b=y, out=out);"),
        "A signal can't depend on itself without a DFF in between. "
        "Follow the wires in the message to find the cycle.",
    ),
    (
        build_error("Nand(a=in, b=in, out=out);", pins="IN in[2]; OUT out;"),
        "Keep the IN and OUT lines as the level gave them: the tests rely on them.",
    ),
    (
        build_error("Nand(a=in, b=in, out=in);"),
        "Inputs are set from outside the chip. Drive an OUT pin or a new wire instead.",
    ),
    (
        build_error("Nand(a=in, b=in, out=out);", head="CHIP Nott"),
        "The name after CHIP must be the level's chip: CHIP Not {",
    ),
    (build_error("Nand(a=in, b=in, out=out)"), "Every part and connection ends with ';'."),
    (
        build_error("Nand(a=in, b=in, out=out);", head="chip Not"),
        "HDL keywords are uppercase: CHIP, IN, OUT, PARTS.",
    ),
]


@pytest.mark.parametrize(("message", "tip"), CASES, ids=[c[0][:40] for c in CASES])
def test_tip_for_real_errors(message: str, tip: str) -> None:
    assert tip_for(message) == tip


def test_missing_colon_and_brace_are_real_errors() -> None:
    lib = ChipLibrary(
        [NOT.root / "reference"],
        sources={"Not": ("CHIP Not { IN in; OUT out; PARTS Nand(a=in, b=in, out=out); }", "x")},
    )
    script = parse_tst(NOT.tst.read_text(), "Not.tst")
    err = run_script(script, lib, NOT).error
    assert err is not None and tip_for(err.message) == (
        "Write PARTS: with a colon before the first part."
    )
    lib = ChipLibrary(
        [NOT.root / "reference"],
        sources={"Not": ("CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out);", "x")},
    )
    err = run_script(script, lib, NOT).error
    assert err is not None and tip_for(err.message) == (
        "Each '{' needs a matching '}': close the chip after the last part."
    )


def test_no_tip_for_unusual_errors() -> None:
    assert tip_for("something nobody has seen before") is None


def bus_error(level: str, pins: str, parts: str) -> str:
    """The build error a player gets in a bus level."""
    lv = find_level(level)
    assert lv is not None
    src = f"CHIP {level} {{ {pins} PARTS: {parts} }}"
    lib = ChipLibrary([lv.root / "reference"], sources={level: (src, f"{level}.hdl")})
    result = run_script(parse_tst(lv.tst.read_text(), f"{level}.tst"), lib, lv)
    assert result.error is not None, "expected a build error"
    return result.error.message


NOT4 = "IN in[4]; OUT out[4];"
MUX8 = "IN a[8], b[8], sel; OUT out[8];"
BUS_CASES = [
    (
        bus_error("Not4", NOT4, "Not(in=in, out=out);"),
        "Not's pin in takes 1 bit but its signal has 4. A slice picks bits out of a bus, "
        "like in[0] or in[0..3]; a 1-bit part handles a bus one bit at a time.",
    ),
    (
        bus_error("Not4", NOT4, "Not(in=in[0], out=out[0..1]); out[2..3] = in[2..3];"),
        "Not's pin out takes 1 bit but its signal has 2. A slice picks bits out of a bus, "
        "like out[0] or out[0..3]; a 1-bit part handles a bus one bit at a time.",
    ),
    (
        bus_error("Not4", NOT4, "out = in[0];"),
        "In out = in[0], the left side has 4 bits and the right side 1. "
        "Slice them so the widths match, like out[0..3] = in[4..7];",
    ),
    (
        bus_error("Not4", NOT4, "Not(in=in[4], out=out[0]); out[1..3] = in[1..3];"),
        "Bits are counted from 0, so in has bits 0..3: the last one is the width minus 1.",
    ),
    (
        bus_error("Not4", NOT4, "Not(in=in[0], out=out[0]); out[1..2] = in[1..2];"),
        "Every bit of an OUT bus needs a driver, and nothing drives bit 3 of out yet. "
        "Drive each bit with a part (out=out[i]) or a connection (out[i] = ...).",
    ),
    (
        bus_error(
            "Mux8",
            MUX8,
            "Mux4(a[0..1]=a[0..1], b=b[0..3], sel=sel, out=out[0..3]); out[4..7] = a[4..7];",
        ),
        "Every bit of Mux4's a needs a value, and nothing connects bits 2..3 yet. "
        "Connect a whole (a=signal) or cover every bit with slices.",
    ),
]


@pytest.mark.parametrize(("message", "tip"), BUS_CASES, ids=[c[0][:40] for c in BUS_CASES])
def test_tip_for_bus_errors(message: str, tip: str) -> None:
    assert tip_for(message) == tip
