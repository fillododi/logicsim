"""Every shipped level is complete and consistent, its reference passes, its stub fails cleanly."""

from __future__ import annotations

import pytest

from nandsim.netlist import PRIMITIVES, ChipLibrary
from nandsim.testing import Impl, Level, load_levels, parse_tst, run_script, run_tst

LEVELS = load_levels()


def test_levels_exist() -> None:
    names = [lv.name for lv in LEVELS][:8]
    assert names == ["Wire", "Hello", "Not", "And", "Or", "Xor", "Mux", "DMux"]


@pytest.mark.parametrize("level", LEVELS, ids=lambda lv: lv.name)
def test_level_files_and_parts(level: Level) -> None:
    for path in (level.stub, level.brief, level.tst, level.reference):
        assert path.is_file(), f"missing {path}"
    unlocked = set(PRIMITIVES) | {lv.name for lv in LEVELS[: LEVELS.index(level)]}
    assert set(level.parts) <= unlocked, f"{level.name} allows parts not unlocked yet"


@pytest.mark.parametrize("level", LEVELS, ids=lambda lv: lv.name)
def test_reference_passes(level: Level) -> None:
    result = run_tst(level.tst, Impl("reference"))
    assert result.passed, (str(result.error), [str(f) for f in result.failures])


@pytest.mark.parametrize("level", LEVELS, ids=lambda lv: lv.name)
def test_empty_stub_fails_cleanly(level: Level) -> None:
    script = parse_tst(level.tst.read_text(), str(level.tst))
    lib = ChipLibrary(
        [level.root / "reference"], sources={level.name: (level.stub.read_text(), str(level.stub))}
    )
    result = run_script(script, lib, level)
    assert result.error is not None
    assert result.error.message.endswith("is not connected")
