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
        "Only the parts listed in the brief can be used here. Names are case-sensitive.",
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
