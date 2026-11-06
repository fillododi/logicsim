"""`.tst` parser and runner tests, against a tiny data root built in a temp dir."""

from __future__ import annotations

from pathlib import Path

import pytest

from nandsim.hdl import HdlError
from nandsim.testing import Impl, parse_tst, run_tst
from nandsim.testing.tst import EvalStep, ExpectStep, SetStep

NOT_STUB = "CHIP Not { IN in; OUT out; PARTS: }"
NOT_REF = "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }"
NOT_TST = """\
chip Not
// truth table
table in | out
    0 | 1
    1 | 0
end
"""


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / "chips" / "g").mkdir(parents=True)
    (tmp_path / "reference" / "g").mkdir(parents=True)
    (tmp_path / "chips" / "levels.toml").write_text(
        '[[level]]\nname = "Not"\ngroup = "g"\nparts = ["Nand"]\n'
    )
    (tmp_path / "chips" / "g" / "Not.hdl").write_text(NOT_STUB)
    (tmp_path / "chips" / "g" / "Not.tst").write_text(NOT_TST)
    (tmp_path / "reference" / "g" / "Not.hdl").write_text(NOT_REF)
    return tmp_path


def save(tmp_path: Path, text: str) -> Impl:
    d = tmp_path / "save"
    d.mkdir(exist_ok=True)
    (d / "Not.hdl").write_text(text)
    return Impl("save", d)


# ---- parsing --------------------------------------------------------------


def test_table_expands_to_set_eval_expect() -> None:
    s = parse_tst(NOT_TST, "Not.tst")
    assert s.chip == "Not"
    kinds = [type(st) for st in s.steps]
    assert kinds == [SetStep, EvalStep, ExpectStep] * 2
    exp = s.steps[2]
    assert isinstance(exp, ExpectStep)
    assert (exp.pos.line, exp.context) == (4, "in=0")


@pytest.mark.parametrize(
    ("text", "width", "bits"),
    [("13", 8, 13), ("0b1101", 8, 13), ("0x0D", 8, 13), ("-1", 8, 255), ("-128", 8, 128)],
)
def test_value_bases(text: str, width: int, bits: int) -> None:
    s = parse_tst(f"chip X\nset a {text}\n", "X.tst")
    step = s.steps[0]
    assert isinstance(step, SetStep)
    assert step.value.encode(width, "a") == bits


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("set a 1\n", "X.tst:1:1: error: a test must start with 'chip <Name>'"),
        ("chip X\nset a\n", "X.tst:2:1: error: usage: set <pin> <value>"),
        ("chip X\nset a 0xZZ\n", "X.tst:2:7: error: '0xZZ' is not a value: use decimal (5, -1), "
         "binary (0b101) or hex (0x1F)"),
        ("chip X\nset a *\n",
         "X.tst:2:7: error: '*' (don't care) is only allowed in expected values"),
        ("chip X\ntable a b | o\n 0 | 1\nend\n",
         "X.tst:3:2: error: table row has 1 input and 1 output values; the header has 2 and 1"),
        ("chip X\ntable a | o\n 0 1\nend\n",
         "X.tst:3:2: error: table row needs '|' between inputs and outputs"),
        ("chip X\ntable a | o\n 0 | 1\n", "X.tst:2:1: error: table is never closed: missing 'end'"),
        ("chip X\ntick\n", "X.tst:2:1: error: 'tick' is for sequential chips, which arrive in "
         "milestone 7"),
        ("chip X\nfrob\n", "X.tst:2:1: error: unknown command 'frob' (expected chip, table, set, "
         "eval, expect)"),
        ("// nothing\n", "X.tst:1:1: error: empty test: it must start with 'chip <Name>'"),
    ],
)  # fmt: skip
def test_parse_errors(text: str, message: str) -> None:
    with pytest.raises(HdlError) as exc:
        parse_tst(text, "X.tst")
    assert str(exc.value) == message


def test_value_too_wide() -> None:
    s = parse_tst("chip X\nset a 2\n", "X.tst")
    step = s.steps[0]
    assert isinstance(step, SetStep)
    with pytest.raises(HdlError, match="X.tst:2:7: error: 2 does not fit in 1-bit pin 'a'"):
        step.value.encode(1, "a")


# ---- running --------------------------------------------------------------


def test_reference_passes(root: Path) -> None:
    r = run_tst(root / "chips" / "g" / "Not.tst", Impl("reference"), root)
    assert r.passed, (r.error, r.failures)
    assert r.checks == 2


def test_wrong_implementation_reports_line(root: Path, tmp_path: Path) -> None:
    impl = save(tmp_path, "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=false, out=out); }")
    r = run_tst(root / "chips" / "g" / "Not.tst", impl, root)
    assert r.error is None
    assert [str(f) for f in r.failures] == [
        f"{root}/chips/g/Not.tst:5:9: out: expected 0, got 1 (inputs in=1)"
    ]


def test_undefined_output(root: Path, tmp_path: Path) -> None:
    impl = save(tmp_path, NOT_REF)
    tst = tmp_path / "u.tst"
    tst.write_text("chip Not\neval\nexpect out 0b1\nexpect out 1\n")
    r = run_tst(tst, impl, root)
    assert [f.message for f in r.failures] == [
        "out: expected 0b1, got 0bx",
        "out: expected 1, got undefined",
    ]


def test_empty_stub_fails_cleanly(root: Path, tmp_path: Path) -> None:
    r = run_tst(root / "chips" / "g" / "Not.tst", save(tmp_path, NOT_STUB), root)
    assert r.error is not None
    assert r.error.message == "output pin 'out' of Not is not connected"


def test_interface_must_match_stub(root: Path, tmp_path: Path) -> None:
    impl = save(tmp_path, "CHIP Not { IN x; OUT out; PARTS: Nand(a=x, b=x, out=out); }")
    r = run_tst(root / "chips" / "g" / "Not.tst", impl, root)
    assert r.error is not None
    assert r.error.message == (
        "Not must keep the level's pins (IN in; OUT out) but declares IN x; OUT out"
    )


def test_only_allowed_parts(root: Path, tmp_path: Path) -> None:
    (tmp_path / "save").mkdir()
    (tmp_path / "save" / "Buf.hdl").write_text(
        "CHIP Buf { IN in; OUT out; PARTS: Nand(a=in, b=in, out=n); Nand(a=n, b=n, out=out); }"
    )
    impl = save(tmp_path, "CHIP Not { IN in; OUT out; PARTS: Buf(in=in, out=b);"
                          " Nand(a=b, b=b, out=out); }")  # fmt: skip
    r = run_tst(root / "chips" / "g" / "Not.tst", impl, root)
    assert r.error is not None
    assert str(r.error).endswith(
        "1:35: error: 'Buf' is not allowed in this level; Not may use: Nand"
    )


def test_missing_save(root: Path, tmp_path: Path) -> None:
    r = run_tst(root / "chips" / "g" / "Not.tst", Impl("save", tmp_path / "empty"), root)
    assert r.error is not None
    assert r.error.message == f"no implementation of 'Not' found in {tmp_path / 'empty'}"


def test_set_on_output_and_unknown_pin(root: Path, tmp_path: Path) -> None:
    impl = save(tmp_path, NOT_REF)
    tst = tmp_path / "bad.tst"
    tst.write_text("chip Not\nset out 1\n")
    r = run_tst(tst, impl, root)
    assert r.error is not None
    assert r.error.message == "'out' is not an input of Not: use 'expect' to check outputs"
    tst.write_text("chip Not\nexpect nope 1\n")
    r = run_tst(tst, impl, root)
    assert r.error is not None
    assert r.error.message == "'nope' is not a pin of Not"


def test_dont_care_counts_but_never_fails(root: Path, tmp_path: Path) -> None:
    tst = tmp_path / "dc.tst"
    tst.write_text("chip Not\nexpect out *\n")
    r = run_tst(tst, Impl("reference"), root)
    assert r.passed and r.checks == 1
