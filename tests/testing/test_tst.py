"""`.tst` parser and runner tests, against a tiny data root built in a temp dir."""

from __future__ import annotations

from pathlib import Path

import pytest

from nandsim.hdl import HdlError
from nandsim.netlist import ChipLibrary
from nandsim.testing import Impl, exported_chips, load_levels, parse_pin_value, parse_tst, run_tst
from nandsim.testing.runner import run_script
from nandsim.testing.tst import EvalStep, ExpectStep, SetStep, TickStep, TockStep

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
        ("chip X\ntick 2\n", "X.tst:2:1: error: usage: tick"),
        ("chip X\ntock now\n", "X.tst:2:1: error: usage: tock"),
        ("chip X\nfrob\n", "X.tst:2:1: error: unknown command 'frob' (expected chip, table, set, "
         "eval, tick, tock, expect, attach, rom, ram, ramstatus)"),
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


def test_dff_needs_the_level_to_allow_it(root: Path, tmp_path: Path) -> None:
    impl = save(tmp_path, "CHIP Not { IN in; OUT out; PARTS: DFF(in=in, out=out); }")
    r = run_tst(root / "chips" / "g" / "Not.tst", impl, root)
    assert r.error is not None
    assert str(r.error).endswith(
        "1:35: error: 'DFF' is not allowed in this level; Not may use: Nand"
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


BUF = "CHIP Buf { IN in; OUT out; PARTS: Nand(a=in, b=in, out=n); Nand(a=n, b=n, out=out); }"


def test_exported_chips_are_allowed_in_any_level(root: Path, tmp_path: Path) -> None:
    exports = tmp_path / "save-exports"
    exports.mkdir()
    (exports / "Buf.hdl").write_text(BUF)
    impl = save(tmp_path, "CHIP Not { IN in; OUT out; PARTS: Buf(in=in, out=b);"
                          " Nand(a=b, b=b, out=out); }")  # fmt: skip
    assert impl.exported(root) == ["Buf"]
    r = run_tst(root / "chips" / "g" / "Not.tst", impl, root)
    assert r.passed, r.error
    # The reference never sees the player's exports.
    assert Impl("reference").exported(root) == []


def test_not_allowed_message_lists_exported_chips(root: Path, tmp_path: Path) -> None:
    exports = tmp_path / "save-exports"
    exports.mkdir()
    (exports / "Buf.hdl").write_text(BUF)
    impl = save(tmp_path, "CHIP Not { IN in; OUT out; PARTS: Or(a=in, b=in, out=out); }")
    r = run_tst(root / "chips" / "g" / "Not.tst", impl, root)
    assert r.error is not None
    assert r.error.message == "'Or' is not allowed in this level; Not may use: Nand, Buf"


def test_exported_chips_skip_names_that_cannot_be_their_own_chip(
    root: Path, tmp_path: Path
) -> None:
    exports = tmp_path / "x"
    exports.mkdir()
    for name in ["Buf", "aBuf", "Not", "Nand", "DFF", "PARTS", "true", "2Fast", "My-Chip"]:
        (exports / f"{name}.hdl").write_text("")
    (exports / "notes.txt").write_text("")
    (exports / "Sub.hdl").mkdir()
    assert exported_chips(exports, load_levels(root)) == ["aBuf", "Buf"]
    assert exported_chips(tmp_path / "missing", load_levels(root)) == []


@pytest.mark.parametrize(
    ("text", "width", "expected"),
    [("13", 4, 13), ("-1", 4, 0xF), ("0b1010", 4, 10), ("0xABC", 12, 0xABC), (" 0x0d ", 8, 13)],
)
def test_typed_pin_values_use_the_tst_syntax(text: str, width: int, expected: int) -> None:
    assert parse_pin_value(text, width, "a") == expected


@pytest.mark.parametrize(
    ("text", "width", "message"),
    [
        ("16", 4, "16 does not fit in 4-bit pin 'a'"),
        ("-9", 4, "-9 does not fit in 4-bit pin 'a'"),
        ("0xG", 4, "'0xG' is not a value: use decimal (5, -1), binary (0b101) or hex (0x1F)"),
        ("*", 4, "'*' is not a value: use decimal (5, -1), binary (0b101) or hex (0x1F)"),
    ],
)
def test_typed_pin_values_report_tst_messages(text: str, width: int, message: str) -> None:
    with pytest.raises(HdlError) as e:
        parse_pin_value(text, width, "a")
    assert e.value.message == message


# A one-bit register: Mux(prev, in, load) feeding a DFF whose output loops back.
BIT = """CHIP Bit { IN in, load; OUT out; PARTS:
    Nand(a=load, b=load, out=nl); Nand(a=prev, b=nl, out=x);
    Nand(a=in, b=load, out=y); Nand(a=x, b=y, out=d);
    DFF(in=d, out=prev, out=out); }"""


def run_bit(tst: str) -> list[str]:
    lib = ChipLibrary(sources={"Bit": (BIT, "Bit.hdl")})
    result = run_script(parse_tst(tst, "Bit.tst"), lib, None)
    assert result.error is None
    return [str(f) for f in result.failures]


def test_tick_and_tock_parse_to_steps() -> None:
    s = parse_tst("chip X\ntick\ntock // a full cycle\n", "X.tst")
    assert [type(step) for step in s.steps] == [TickStep, TockStep]


def test_sequential_script_passes() -> None:
    tst = """chip Bit
set in 1
set load 1
tick
tock
expect out 1
set in 0
set load 0
tick
tock
expect out 1
"""
    assert run_bit(tst) == []


def test_clocked_failures_name_the_cycle() -> None:
    tst = """chip Bit
set in 1
set load 1
tick
expect out 1
tock
expect out 0
table in load | out
    0 1 | 0
end
"""
    assert run_bit(tst) == [
        "Bit.tst:5:1: out: expected 1, got undefined (cycle 0 after tick)",
        "Bit.tst:7:1: out: expected 0, got 1 (cycle 1)",
        "Bit.tst:9:11: out: expected 0, got 1 (inputs in=0 load=1, cycle 1)",
    ]
