"""Feedback loops and the clock: NAND latches, a flip-flop built from them, oscillation."""

from __future__ import annotations

import random

import numpy as np
import pytest

from nandsim.hdl import parse
from nandsim.netlist import CLOCK_NET, ChipLibrary, elaborate, net_names
from nandsim.sim import Simulator

NOT = "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }"
# Active-low set and reset, as two cross-coupled NANDs.
SRLATCH = """CHIP SRLatch { IN s, r; OUT q, nq; PARTS:
    Nand(a=s, b=nqi, out=qi, out=q);
    Nand(a=r, b=qi, out=nqi, out=nq); }"""
# Follows d while en is 1, holds while en is 0.
DLATCH = """CHIP DLatch { IN d, en; OUT q; PARTS:
    Nand(a=d, b=en, out=s);
    Nand(a=s, b=en, out=r);
    SRLatch(s=s, r=r, q=q); }"""
# Master open while the clock is 1, slave while it is 0: out(t) = in(t-1).
FLIPFLOP = """CHIP FF { IN in; OUT out; PARTS:
    DLatch(d=in, en=clock, q=m);
    Not(in=clock, out=nclk);
    DLatch(d=m, en=nclk, q=out); }"""
BIT = """CHIP Bit { IN in, load; OUT out; PARTS:
    Not(in=load, out=nl);
    Nand(a=in, b=load, out=x); Nand(a=prev, b=nl, out=y); Nand(a=x, b=y, out=next);
    FF(in=next, out=prev, out=out); }"""


def lib() -> ChipLibrary:
    chips = {"Not": NOT, "SRLatch": SRLATCH, "DLatch": DLATCH, "FF": FLIPFLOP, "Bit": BIT}
    return ChipLibrary(sources={k: (v, f"{k}.hdl") for k, v in chips.items()})


def sim(src: str) -> Simulator:
    return Simulator(elaborate(parse(src, "T.hdl"), lib()))


def chip(name: str) -> Simulator:
    return sim(lib().sources[name][0])


# ---- levelization ----------------------------------------------------------


def test_a_latch_is_one_loop_level_after_its_inputs() -> None:
    nl = elaborate(parse(DLATCH, "T.hdl"), lib())
    kinds = [lv.is_loop for lv in nl.levels]
    assert kinds == [False, False, True]  # s, then r, then the two cross-coupled NANDs
    (op,) = nl.levels[2].ops
    assert len(op.outputs[0]) == 2 and nl.levels[2].loops == 1
    assert op.loop is not None and op.loop.tolist() == [0, 0]


def test_separate_loops_share_a_level_but_keep_their_ids() -> None:
    two = """CHIP T { IN s, r; OUT a, b; PARTS:
        SRLatch(s=s, r=r, q=a); SRLatch(s=r, r=s, q=b); }"""
    nl = elaborate(parse(two, "T.hdl"), lib())
    (level,) = [lv for lv in nl.levels if lv.is_loop]
    assert level.loops == 2
    assert sorted(level.ops[0].loop.tolist()) == [0, 0, 1, 1]


def test_gates_after_a_loop_come_in_later_levels() -> None:
    nl = elaborate(
        parse(
            "CHIP T { IN s, r; OUT o; PARTS: SRLatch(s=s, r=r, q=q); Not(in=q, out=o); }", "T.hdl"
        ),
        lib(),
    )  # noqa: E501
    assert [lv.is_loop for lv in nl.levels] == [True, False]


def test_a_gate_reading_itself_is_a_loop() -> None:
    nl = elaborate(
        parse("CHIP T { IN a; OUT o; PARTS: Nand(a=a, b=x, out=x, out=o); }", "T.hdl"), lib()
    )  # noqa: E501
    assert [lv.loops for lv in nl.levels] == [1]


def test_chips_without_loops_level_as_before() -> None:
    nl = elaborate(
        parse("CHIP T { IN a; OUT o; PARTS: Not(in=a, out=x); Not(in=x, out=o); }", "T.hdl"), lib()
    )  # noqa: E501
    assert [lv.is_loop for lv in nl.levels] == [False, False]


# ---- latches ---------------------------------------------------------------


def test_sr_latch_sets_resets_and_holds() -> None:
    s = chip("SRLatch")
    s.set("s", 1)
    s.set("r", 1)
    s.eval()
    assert s.get("q") is None  # nothing has set it yet
    for s_in, r_in, q in [(0, 1, 1), (1, 1, 1), (1, 0, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)]:
        s.set("s", s_in)
        s.set("r", r_in)
        s.eval()
        assert (s.get("q"), s.get("nq")) == (q, 1 - q)
        assert len(s.unsettled) == 0


def test_releasing_set_and_reset_together_goes_undefined() -> None:
    """Both NANDs at 1, released at once: each round flips both, a real race."""
    s = chip("SRLatch")
    s.set("s", 0)
    s.set("r", 0)
    s.eval()
    assert (s.get("q"), s.get("nq")) == (1, 1)
    s.set("s", 1)
    s.set("r", 1)
    s.eval()
    assert s.get("q") is None and s.get("nq") is None
    names = net_names(s.netlist)
    assert sorted(names[int(n)] for n in s.unsettled) == ["nq", "q"]
    s.set("r", 0)  # a reset brings it back
    s.eval()
    assert (s.get("q"), s.get("nq")) == (0, 1)
    assert len(s.unsettled) == 0


def test_d_latch_follows_while_enabled_and_holds_after() -> None:
    s = chip("DLatch")
    for d, en, q in [(1, 1, 1), (0, 1, 0), (1, 0, 0), (0, 0, 0), (1, 1, 1), (0, 0, 1)]:
        s.set("d", d)
        s.set("en", en)
        s.eval()
        assert s.get("q") == q


def test_an_oscillator_goes_undefined_and_the_rest_keeps_its_value() -> None:
    src = """CHIP T { IN en, s, r; OUT o, q; PARTS:
        Nand(a=en, b=x, out=x, out=o); SRLatch(s=s, r=r, q=q); }"""
    s = sim(src)
    s.set("en", 0)
    s.set("s", 0)
    s.set("r", 1)
    s.eval()
    assert (s.get("o"), s.get("q")) == (1, 1)
    s.set("en", 1)  # x = not x: never settles
    s.set("s", 1)
    s.eval()
    assert s.get("o") is None
    assert s.get("q") == 1  # the latch in the same level is untouched
    assert [net_names(s.netlist)[int(n)] for n in s.unsettled] == ["o"]


# ---- the clock -------------------------------------------------------------


def test_clock_is_zero_at_power_on_one_after_tick_zero_after_tock() -> None:
    s = sim("CHIP T { OUT c; PARTS: c = clock; }")
    s.eval()
    assert s.get("c") == 0
    s.tick()
    assert s.get("c") == 1
    s.tock()
    assert s.get("c") == 0
    assert s.clocked and s.dff_count == 0


def test_chips_that_ignore_the_clock_are_not_clocked() -> None:
    s = chip("DLatch")
    assert not s.clocked and not s.netlist.reads_clock


def test_clock_reaches_parts() -> None:
    s = sim("CHIP T { IN in; OUT out; PARTS: FF(in=in, out=out); }")
    assert s.netlist.reads_clock
    assert CLOCK_NET in s.netlist.gates["Nand"].inputs[1].tolist()


def test_flip_flop_from_latches_matches_out_t_equals_in_t_minus_1() -> None:
    s = chip("FF")
    s.set("in", 1)
    s.eval()
    assert s.get("out") is None
    rng = random.Random(4004)
    prev: int | None = None
    for _ in range(40):
        v = rng.randrange(2)
        s.set("in", v)
        s.tick()
        assert s.get("out") == prev  # after tick: still the old value
        s.tock()
        assert s.get("out") == v  # after tock: the new one
        prev = v


def test_bit_from_a_latch_flip_flop_holds_and_loads() -> None:
    """The feedback runs through the whole Bit, so the loop holds Mux and both latches."""
    s = chip("Bit")
    nl = s.netlist
    assert sum(lv.loops for lv in nl.levels) == 1
    rng = random.Random(4004)
    stored: int | None = None
    for _ in range(60):
        v, load = rng.randrange(2), rng.randrange(2)
        s.set("in", v)
        s.set("load", load)
        s.tick()
        assert s.get("out") == stored
        s.tock()
        if load:
            stored = v
        assert s.get("out") == stored
        assert len(s.unsettled) == 0


def test_many_bits_settle_together_in_one_vectorized_level() -> None:
    parts = " ".join(f"Bit(in=in[{i}], load=load, out=out[{i}]);" for i in range(8))
    s = sim(f"CHIP T {{ IN in[8], load; OUT out[8]; PARTS: {parts} }}")
    loop_levels = [lv for lv in s.netlist.levels if lv.is_loop]
    assert len(loop_levels) == 1 and loop_levels[0].loops == 8
    for v in [0x5A, 0xFF, 0x00, 0x81]:
        s.set("in", v)
        s.set("load", 1)
        s.tick()
        s.tock()
        assert s.get("out") == v
    s.set("in", 0x3C)
    s.set("load", 0)
    s.tick()
    s.tock()
    assert s.get("out") == 0x81


def test_reset_undefines_latches() -> None:
    s = chip("FF")
    s.set("in", 1)
    s.tick()
    s.tock()
    assert s.get("out") == 1
    s.reset()
    s.set("in", 0)
    s.eval()
    assert s.get("out") is None
    assert not s.value[CLOCK_NET] and s.known[CLOCK_NET]


@pytest.mark.parametrize("seed", range(3))
def test_latch_flip_flop_agrees_with_the_dff_primitive(seed: int) -> None:
    both = """CHIP T { IN in, load; OUT a, b; PARTS:
        Bit(in=in, load=load, out=a);
        Not(in=load, out=nl);
        Nand(a=in, b=load, out=x); Nand(a=p, b=nl, out=y); Nand(a=x, b=y, out=nx);
        DFF(in=nx, out=p, out=b); }"""
    s = sim(both)
    rng = np.random.default_rng(seed)
    for v, load in rng.integers(0, 2, size=(50, 2)).tolist():
        s.set("in", v)
        s.set("load", load)
        s.tick()
        assert s.get("a") == s.get("b")
        s.tock()
        assert s.get("a") == s.get("b")
