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


# ---- DFF and the clock ---------------------------------------------------

DFF = "CHIP T { IN in; OUT out; PARTS: DFF(in=in, out=out); }"


def test_dff_starts_undefined_and_delays_one_cycle() -> None:
    s = sim(DFF)
    s.set("in", 1)
    s.eval()
    assert s.get("out") is None
    s.tick()
    assert s.get("out") is None  # tick only latches
    assert (s.cycle, s.mid_cycle) == (0, True)
    s.set("in", 0)  # changing the input after the tick doesn't reach this cycle
    s.tock()
    assert s.get("out") == 1
    assert (s.cycle, s.mid_cycle) == (1, False)
    s.tick()
    s.tock()
    assert s.get("out") == 0


def test_tock_without_tick_keeps_dffs_undefined() -> None:
    s = sim(DFF)
    s.set("in", 1)
    s.tock()
    assert s.get("out") is None
    assert s.cycle == 1


def test_undefined_input_latches_undefined() -> None:
    s = sim(DFF)
    s.set("in", 1)
    s.tick()
    s.tock()
    s.set("in", None)
    s.tick()
    s.tock()
    assert s.get("out") is None


def test_loop_through_a_dff_is_not_combinational() -> None:
    # A toggle: out flips every cycle once a known value is loaded.
    src = """CHIP T { IN init, load; OUT out; PARTS:
        Not(in=q, out=nq);
        Nand(a=load, b=load, out=nl); Nand(a=nq, b=nl, out=x);
        Nand(a=init, b=load, out=y); Nand(a=x, b=y, out=d);
        DFF(in=d, out=q, out=out); }"""
    s = sim(src)
    s.set("load", 0)
    s.tick()
    s.tock()
    assert s.get("out") is None  # undefined feeds back as undefined
    s.set("init", 1)
    s.set("load", 1)
    s.tick()
    s.tock()
    s.set("load", 0)
    seen = []
    for _ in range(4):
        seen.append(s.get("out"))
        s.tick()
        s.tock()
    assert seen == [1, 0, 1, 0]


def test_shift_register_updates_all_dffs_at_once() -> None:
    src = """CHIP T { IN in; OUT out[4]; PARTS:
        DFF(in=in, out=a, out=out[0]); DFF(in=a, out=b, out=out[1]);
        DFF(in=b, out=c, out=out[2]); DFF(in=c, out=out[3]); }"""
    s = sim(src)
    assert s.dff_count == 4
    for bit in (1, 0, 1, 1):
        s.set("in", bit)
        s.tick()
        s.tock()
    assert s.get("out") == 0b1011  # out[0] holds the last bit shifted in
    assert s.get_bits("out") == [1, 1, 0, 1]
    assert s.wire("T/DFF#4/in") == 0  # the last DFF reads out[2]


def test_reset_returns_to_power_on() -> None:
    s = sim(DFF)
    s.set("in", 1)
    s.tick()
    s.tock()
    s.reset()
    assert (s.get("in"), s.get("out"), s.cycle, s.mid_cycle) == (None, None, 0, False)
    s.tock()  # the latch was cleared too
    assert s.get("out") is None


def test_chip_without_dffs_can_still_be_clocked() -> None:
    s = sim(NOT)
    assert s.dff_count == 0
    s.set("in", 0)
    s.tick()
    s.tock()
    assert s.get("out") == 1


def test_every_sequential_primitive_is_clocked_like_a_dff() -> None:
    # The engine clocks every primitive marked sequential as a D flip-flop, so a new
    # sequential row with another shape must come with its own clock behaviour.
    from nandsim.netlist import PRIMITIVES

    sequential = [p for p in PRIMITIVES.values() if p.sequential]
    assert [p.name for p in sequential] == ["DFF"]
    assert all((p.inputs, p.outputs) == (("in",), ("out",)) for p in sequential)
