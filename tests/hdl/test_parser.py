"""Parser tests: valid chips parse to the expected AST; every syntax error is positioned."""

from __future__ import annotations

import pytest

from nandsim.hdl import Const, HdlError, PinRef, parse

XOR = """\
// Xor from four NANDs
CHIP Xor {
    IN a, b;
    OUT out;
    PARTS:
    Nand(a=a, b=b, out=n);
    Nand(a=a, b=n, out=x);
    Nand(a=n, b=b, out=y);
    Nand(a=x, b=y, out=out);
}
"""


def test_parse_xor() -> None:
    chip = parse(XOR, "Xor.hdl")
    assert chip.name == "Xor"
    assert (chip.pos.line, chip.pos.col) == (2, 1)
    assert chip.name_pos is not None and (chip.name_pos.line, chip.name_pos.col) == (2, 6)
    assert [p.name for p in chip.inputs] == ["a", "b"]
    assert [p.name for p in chip.outputs] == ["out"]
    assert len(chip.parts) == 4
    first = chip.parts[0]
    assert first.chip == "Nand"
    assert (first.pos.line, first.pos.col) == (6, 5)
    assert [str(c.inner) + "=" + str(c.outer) for c in first.connections] == [
        "a=a",
        "b=b",
        "out=n",
    ]


def test_buses_slices_constants() -> None:
    chip = parse(
        """CHIP B { IN a[8], s; OUT o[8], top;
        PARTS: /* block
        comment */ Foo(in=a[0..3], x=a[7], y=true, z=false, out[0..7]=o, out[7]=top); }""",
        "B.hdl",
    )
    assert chip.inputs[0].width == 8
    assert chip.outputs[1].width == 1
    conns = chip.parts[0].connections
    assert conns[0].outer == PinRef("a", 0, 3, conns[0].outer.pos)
    assert conns[1].outer == PinRef("a", 7, 7, conns[1].outer.pos)
    assert isinstance(conns[2].outer, Const) and conns[2].outer.value is True
    assert isinstance(conns[3].outer, Const) and conns[3].outer.value is False
    assert conns[4].inner == PinRef("out", 0, 7, conns[4].inner.pos)


def test_empty_parts_and_no_inputs() -> None:
    chip = parse("CHIP Stub { OUT out; PARTS: }", "Stub.hdl")
    assert chip.inputs == () and chip.parts == ()


@pytest.mark.parametrize(
    ("src", "message"),
    [
        (
            "CHIP X { IN a; OUT o; PARTS: Nand(a=a b=a, out=o); }",
            "X.hdl:1:39: error: expected ',' or ')', found 'b'",
        ),
        (
            "CHIP X { IN a, a; OUT o; PARTS: }",
            "X.hdl:1:16: error: pin 'a' is already declared at line 1",
        ),
        (
            "CHIP X { IN a[0]; OUT o; PARTS: }",
            "X.hdl:1:15: error: bus 'a' must be at least 1 bit wide",
        ),
        (
            "CHIP X { IN a[8]; OUT o; PARTS: Not(in=a[7..2], out=o); }",
            "X.hdl:1:45: error: slice a[7..2] is reversed: write [2..7]",
        ),
        (
            "CHIP X { IN a; OUT o; PARTS: Not(in=a, out=o) }",
            "X.hdl:1:47: error: expected ';', found '}'",
        ),
        (
            "CHIP X { IN a; OUT o; Not(in=a, out=o); }",
            "X.hdl:1:23: error: expected 'PARTS:', found 'Not'",
        ),
        (
            "CHIP X { IN a; OUT o; PARTS: Not(in=a, out=o);",
            "X.hdl:1:47: error: expected '}' to close the chip, found end of file",
        ),
        (
            "CHIP X { IN a; OUT o; PARTS: } extra",
            "X.hdl:1:32: error: unexpected 'extra' after the end of the chip",
        ),
        ("CHIP X { IN a$; }", "X.hdl:1:14: error: unexpected character '$'"),
        ("CHIP X { /* never closed", "X.hdl:1:10: error: comment is never closed: missing '*/'"),
        ("CHIP X {\n  IN true;\n}", "X.hdl:2:6: error: expected a pin name, found 'true'"),
        ("chip X {}", "X.hdl:1:1: error: expected 'CHIP', found 'chip'"),
    ],
)
def test_syntax_errors(src: str, message: str) -> None:
    with pytest.raises(HdlError) as exc:
        parse(src, "X.hdl")
    assert str(exc.value) == message
