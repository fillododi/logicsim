"""Brief rendering tests, on the shipped briefs and on edge cases."""

from __future__ import annotations

from nandsim.gui.brief import brief_lines
from nandsim.testing import load_levels


def test_mux_brief() -> None:
    mux = next(lv for lv in load_levels() if lv.name == "Mux")
    lines = brief_lines(mux.brief.read_text(), 32)
    assert lines[0] == ("Mux", "title")
    table = [t for t, k in lines if k == "table"]
    assert table[0].split() == ["a", "b", "sel", "out"]
    assert len(table) == 9  # header + 8 rows, separator dropped
    assert all(len(t) <= 32 for t, _ in lines)
    assert any(k == "bold" and t.startswith("Hint:") for t, k in lines)
    assert not any("**" in t or "`" in t for t, _ in lines)


def test_every_brief_renders() -> None:
    for lv in load_levels():
        assert brief_lines(lv.brief.read_text(), 28)


def test_blank_lines_collapse() -> None:
    assert brief_lines("a\n\n\n\nb\n\n", 20) == [("a", "text"), ("", "blank"), ("b", "text")]
