"""Engine tests: three-valued NAND, propagation through levels, buses, inspection."""

from __future__ import annotations

import itertools

import pytest

from nandsim.hdl import parse
from nandsim.netlist import ChipLibrary, elaborate
from nandsim.sim import Simulator

NOT = "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }"
XOR = """CHIP T { IN a, b; OUT out; PARTS:
    Nand(a=a, b=b, out=n); Nand(a=a, b=n, out=x);
    Nand(a=n, b=b, out=y); Nand(a=x, b=y, out=out); }"""


def sim(src: str) -> Simulator:
    lib = ChipLibrary(sources={"Not": (NOT, "Not.hdl")})
    return Simulator(elaborate(parse(src, "T.hdl"), lib))


NAND = "CHIP T { IN a, b; OUT out; PARTS: Nand(a=a, b=b, out=out); }"


@pytest.mark.parametrize(
    ("a", "b", "out"),
    [
        (0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0),
        (0, None, 1), (None, 0, 1),  # a known 0 forces 1
        (1, None, None), (None, 1, None), (None, None, None),
    ],
)  # fmt: skip
def test_nand_kleene(a: int | None, b: int | None, out: int | None) -> None:
    s = sim(NAND)
    s.set("a", a)
    s.set("b", b)
    s.eval()
    assert s.get("out") == out


def test_inputs_start_undefined() -> None:
    s = sim(NAND)
    s.eval()
    assert s.get("out") is None


def test_xor_truth_table_and_inner_wires() -> None:
    s = sim(XOR)
    for a, b in itertools.product((0, 1), repeat=2):
        s.set("a", a)
        s.set("b", b)
        s.eval()
        assert s.get("out") == a ^ b
        assert s.wire("T/n") == 1 - (a & b)
        assert s.wire("T/Nand#4/out") == a ^ b


def test_bus_round_trip() -> None:
    src = (
        "CHIP T { IN a[8]; OUT o[8]; PARTS: "
        + " ".join(f"Not(in=a[{i}], out=o[{i}]);" for i in range(8))
        + " }"
    )
    s = sim(src)
    for v in (0, 1, 0x5A, 0xFF):
        s.set("a", v)
        s.eval()
        assert s.get("o") == (~v & 0xFF)
        assert s.get_bits("o")[0] == 1 - (v & 1)


def test_partially_undefined_bus() -> None:
    s = sim("CHIP T { IN a, b; OUT o[2]; PARTS: Not(in=a, out=o[0]); Not(in=b, out=o[1]); }")
    s.set("a", 1)
    s.eval()
    assert s.get("o") is None
    assert s.get_bits("o") == [0, None]


def test_constants() -> None:
    s = sim("CHIP T { OUT t, f; PARTS: Nand(a=false, b=true, out=t); Not(in=true, out=f); }")
    s.eval()
    assert (s.get("t"), s.get("f")) == (1, 0)


def test_value_out_of_range() -> None:
    s = sim(NAND)
    with pytest.raises(ValueError, match="does not fit in 1-bit input 'a'"):
        s.set("a", 2)
