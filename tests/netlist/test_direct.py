"""Direct connections: `out = a;` statements and reading labelled parts as `g1.out`."""

from __future__ import annotations

import itertools

import pytest

from nandsim.hdl import HdlError, parse
from nandsim.netlist import ChipLibrary, elaborate
from nandsim.sim import Simulator

NOT = "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }"
PAIR = "CHIP Pair { IN a, b; OUT x, y; PARTS: Not(in=a, out=x); Not(in=b, out=y); }"


def sim(src: str) -> Simulator:
    lib = ChipLibrary(sources={"Not": (NOT, "Not.hdl"), "Pair": (PAIR, "Pair.hdl")})
    return Simulator(elaborate(parse(src, "T.hdl"), lib))


def run(s: Simulator, **inputs: int) -> Simulator:
    for k, v in inputs.items():
        s.set(k, v)
    s.eval()
    return s


def test_input_straight_to_output_and_constants() -> None:
    s = sim("CHIP T { IN a, b[4]; OUT o, swapped[4], one, zeros[3]; PARTS:"
            " o = a; swapped[0..1] = b[2..3]; swapped[2..3] = b[0..1];"
            " one = true; zeros = false; }")  # fmt: skip
    run(s, a=1, b=0b0110)
    assert s.get("o") == 1
    assert s.get("swapped") == 0b1001
    assert (s.get("one"), s.get("zeros")) == (1, 0)
    assert s.netlist.gate_count == 0  # connections are wires, not gates


def test_labelled_parts_connect_directly() -> None:
    s = sim("CHIP T { IN a, b; OUT out; PARTS: g1: Nand(a=a, b=b); Not(in=g1.out, out=out); }")
    for a, b in itertools.product((0, 1), repeat=2):
        assert run(s, a=a, b=b).get("out") == (a & b)


def test_label_may_be_used_before_its_part_and_with_slices() -> None:
    s = sim("CHIP T { IN a, b; OUT o[2], y; PARTS:"
            " o[0] = p.x; o[1] = p.y; Not(in=p.y, out=y); p: Pair(a=a, b=b); }")  # fmt: skip
    assert run(s, a=1, b=0).get("o") == 0b10
    assert s.get("y") == 0


def test_connections_chain_through_new_wires() -> None:
    s = sim("CHIP T { IN a; OUT o; PARTS: o = w2; w2 = w1; w1 = a; }")
    assert run(s, a=1).get("o") == 1


def test_output_can_feed_a_part_and_another_output() -> None:
    s = sim("CHIP T { IN a; OUT o, copy; PARTS: Not(in=a, out=o); copy = o; }")
    assert run(s, a=0).get("copy") == 1


ERRORS = [
    (
        "CHIP T { IN a; OUT o; PARTS: a = o; o = true; }",
        "T.hdl:1:30: error: 'a' is an input pin of T: it cannot be assigned",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: o = a; o = true; }",
        "T.hdl:1:37: error: 'o' is already driven by the connection at line 1",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: Not(in=a, out=o); o = a; }",
        "T.hdl:1:48: error: 'o' is already driven by Not at line 1",
    ),
    (
        "CHIP T { IN a[2]; OUT o; PARTS: o = a; }",
        "T.hdl:1:37: error: width mismatch: 'o' has 1 bit but 'a' has 2",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: o = w; }",
        "T.hdl:1:34: error: 'w' is not a pin of T and nothing drives a wire with that name",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: w = true; o = w; }",
        "T.hdl:1:34: error: the width of new wire 'w' can't come from a constant; "
        "connect the constant to a pin instead",
    ),
    (
        "CHIP T { IN a; OUT o, p; PARTS: o = p; p = o; }",
        "T.hdl:1:40: error: 'p' would be driven only by itself: assignments form a loop "
        "with nothing driving it",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: o = g.out; }",
        "T.hdl:1:34: error: no part is labelled 'g' in T",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: g: Not(in=a); o = g.in; }",
        "T.hdl:1:48: error: 'g.in' is an input pin of Not: only a part's outputs can be read "
        "this way",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: g: Not(in=a); o = g.q; }",
        "T.hdl:1:48: error: Not has no pin 'q' (its pins are: in, out)",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: g: Not(in=a); g.out = a; o = g.out; }",
        "T.hdl:1:44: error: 'g.out' is driven by part 'g' and cannot be assigned",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: g: Not(in=a, out=o); h: Not(in=a, out=g.out); }",
        "T.hdl:1:68: error: 'g.out' is driven by part 'g' and cannot be driven again",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: g: Not(in=a, out=o);\n g: Not(in=a); }",
        "T.hdl:2:2: error: label 'g' is already used at line 1",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: a: Not(in=a, out=o); }",
        "T.hdl:1:30: error: label 'a' is also a pin of T; use another name",
    ),
    (
        "CHIP T { IN a; OUT o; PARTS: o Not(in=a); }",
        "T.hdl:1:32: error: expected '(' for a part, ':' after a label, or '=' to connect, "
        "found 'Not'",
    ),
]


@pytest.mark.parametrize(("src", "message"), ERRORS)
def test_errors(src: str, message: str) -> None:
    with pytest.raises(HdlError) as exc:
        sim(src)
    assert str(exc.value) == message
