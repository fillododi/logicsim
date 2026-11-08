"""The latch and flip-flop levels: wrong versions fail them, and the DFF stand-in is exact."""

from __future__ import annotations

import numpy as np
import pytest

from nandsim.hdl import parse
from nandsim.netlist import ChipLibrary, elaborate
from nandsim.sim import Simulator
from nandsim.testing import find_level, parse_tst, run_script

REF = find_level("DFF")
assert REF is not None
REFERENCE = REF.root / "reference"


def run(name: str, body: str) -> tuple[bool, list[str]]:
    """Run level `name`'s test on a player chip with these PARTS."""
    level = find_level(name)
    assert level is not None
    stub = level.stub.read_text()
    src = stub.replace("PARTS:", "PARTS:\n" + body)
    lib = ChipLibrary([REFERENCE], sources={name: (src, f"{name}.hdl")})
    result = run_script(parse_tst(level.tst.read_text(), level.tst.name), lib, level)
    assert result.error is None, str(result.error)
    return result.passed, [f.message for f in result.failures]


WRONG = [
    ("SRLatch", "Not(in=reset, out=out);"),  # forgets when neither is set
    ("SRLatch", "Nand(a=reset, b=q, out=out); Not(in=set, out=ns); Nand(a=ns, b=out, out=q);"),
    ("DLatch", "And(a=in, b=load, out=out);"),  # no memory at all
    ("DLatch", "Not(in=in, out=n); And(a=in, b=load, out=r); And(a=n, b=load, out=s);"
     " SRLatch(set=s, reset=r, out=out);"),  # set and reset swapped
    ("DFF", "DLatch(in=in, load=clock, out=out);"),  # open while clock is 1
    ("DFF", "Not(in=clock, out=low); DLatch(in=in, load=low, out=out);"),  # open while 0
    ("DFF", "Not(in=clock, out=low); DLatch(in=in, load=low, out=m);"
     " DLatch(in=m, load=clock, out=out);"),  # phases swapped: changes at the tick
    ("DFF", "DLatch(in=in, load=true, out=m); DLatch(in=m, load=true, out=out);"),
]  # fmt: skip


@pytest.mark.parametrize(
    ("name", "body"), WRONG, ids=[f"{n}-{i}" for i, (n, _) in enumerate(WRONG)]
)
def test_wrong_versions_fail(name: str, body: str) -> None:
    passed, failures = run(name, body)
    assert not passed and failures


def test_the_dff_level_builds_the_players_chip_not_the_primitive() -> None:
    """Testing DFF uses the player's HDL; a DFF part elsewhere is the primitive."""
    passed, _ = run("DFF", "DLatch(in=in, load=true, out=out);")
    assert not passed  # the primitive would have passed
    lib = ChipLibrary([REFERENCE])
    top = lib.resolve_top("DFF")
    assert not isinstance(top, type(lib.resolve("DFF")))


def both() -> Simulator:
    """The reference DFF (renamed) beside the DFF primitive, on the same input."""
    text = (REFERENCE / "04_seq" / "DFF.hdl").read_text().replace("CHIP DFF", "CHIP LatchDFF")
    top = "CHIP T { IN in; OUT a, b; PARTS: LatchDFF(in=in, out=a); DFF(in=in, out=b); }"
    lib = ChipLibrary([REFERENCE], sources={"LatchDFF": (text, "LatchDFF.hdl")})
    return Simulator(elaborate(parse(top, "T.hdl"), lib))


@pytest.mark.parametrize("seed", range(4))
def test_dff_primitive_equals_the_latch_dff(seed: int) -> None:
    """The stand-in rule: the primitive and the HDL DFF agree at every point a test sees.

    Random steps: set in, tick, tock and eval, in any order a .tst can write them,
    so inputs change both mid-cycle and while the clock is low.
    """
    s = both()
    rng = np.random.default_rng(seed)
    for step in rng.integers(0, 4, size=400).tolist():
        if step == 0:
            s.set("in", int(rng.integers(0, 2)))
        elif step == 1 and not s.mid_cycle:
            s.tick()
        elif step == 2 and s.mid_cycle:
            s.tock()
        else:
            s.eval() if not s.mid_cycle else None
        assert s.get("a") == s.get("b"), f"seed {seed}, cycle {s.cycle}"
