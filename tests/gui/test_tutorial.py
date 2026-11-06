"""The guided tour's data, progress file, event matching and bubble placement (no pygame)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from nandsim.gui.tutorial import Step, Tour, load_steps, paragraphs, place_bubble
from nandsim.testing import load_levels

STEPS = load_steps()


def test_shipped_tour_is_valid() -> None:
    names = {lv.name for lv in load_levels()}
    assert STEPS[0].id == "welcome" and STEPS[0].level == "Hello"
    for s in STEPS:
        assert s.level is None or s.level in names, s.id
        if s.anchor.startswith("level:"):
            assert s.anchor.removeprefix("level:") in names, s.id
        if s.until.startswith("open_level:"):
            assert s.until.removeprefix("open_level:") in names, s.id
    hello = next(s for s in STEPS if s.id == "write")
    assert "    Nand(a=a, b=b, out=out);" in hello.text  # the tutorial level's one-line answer


def small_tour(tmp_path: Path) -> Tour:
    steps = [
        Step("hi", "Hello there.", "levels", "next", "Hello"),
        Step("go", "Open Not.", "level:Not", "open_level:Not", "Hello"),
        Step("not", "Not's brief.", "brief", "save", "Not"),
        Step("any", "Anywhere.", "canvas", "next"),
    ]
    return Tour(steps, tmp_path / "tutorial.json")


def test_steps_advance_on_their_own_event(tmp_path: Path) -> None:
    tour = small_tour(tmp_path)
    assert tour.current is not None and tour.current.id == "hi"
    assert not tour.event("Hello", "save")  # not this step's action
    assert tour.event("Hello", "next")
    assert tour.position(tour.steps[1]) == (2, 4)
    assert not tour.event("Hello", "open_level", "And")  # a different level
    assert tour.event("Hello", "open_level", "Not")
    # "not" belongs to Not: hidden, and deaf, while another level is open.
    assert tour.visible("And") is None and not tour.event("And", "save")
    assert tour.visible("Not") is not None and tour.event("Not", "save")
    assert tour.visible("Or") is not None  # no level: shows anywhere
    assert tour.event("Or", "next")
    assert tour.current is None


def test_progress_survives_a_restart(tmp_path: Path) -> None:
    tour = small_tour(tmp_path)
    tour.event("Hello", "next")
    again = small_tour(tmp_path)
    assert again.current is not None and again.current.id == "go"
    data = json.loads((tmp_path / "tutorial.json").read_text())
    assert data == {"version": 1, "seen": ["hi"], "skipped": False}


def test_skip_and_replay(tmp_path: Path) -> None:
    tour = small_tour(tmp_path)
    tour.event("Hello", "next")
    tour.skip()
    assert tour.current is None and small_tour(tmp_path).current is None
    tour.replay()
    assert tour.current is not None and tour.current.id == "hi"
    assert small_tour(tmp_path).current == tour.current


def test_unreadable_progress_is_kept_aside(tmp_path: Path) -> None:
    (tmp_path / "tutorial.json").write_text("{not json")
    tour = small_tour(tmp_path)
    assert tour.current is not None and tour.current.id == "hi"
    assert tour.warning is not None and "tutorial.json.bad" in tour.warning
    assert (tmp_path / "tutorial.json.bad").read_text() == "{not json"


@pytest.mark.parametrize(
    ("entry", "message"),
    [
        ('anchor = "levels"\nuntil = "next"\ntext = "x"', "step 1 (no id): missing 'id'"),
        ('id = "a"\nanchor = "sky"\nuntil = "next"\ntext = "x"', "unknown anchor 'sky'"),
        ('id = "a"\nanchor = "pin:"\nuntil = "next"\ntext = "x"', "unknown anchor 'pin:'"),
        ('id = "a"\nanchor = "canvas"\nuntil = "dance"\ntext = "x"', "unknown 'until' event"),
        ('id = "a"\nanchor = "canvas"\nuntil = "next:Not"\ntext = "x"', "'next:Not'"),
        ('id = "a"\nanchor = "canvas"\nuntil = "next"\ntext = "  "', "step 1 (a): empty text"),
    ],
)
def test_bad_tour_data_names_the_step(tmp_path: Path, entry: str, message: str) -> None:
    p = tmp_path / "tutorial.toml"
    p.write_text(f"[[step]]\n{entry}\n")
    with pytest.raises(ValueError, match=message.replace("(", r"\(").replace(")", r"\)")):
        load_steps(p)


def test_duplicate_ids_are_rejected(tmp_path: Path) -> None:
    p = tmp_path / "tutorial.toml"
    one = '[[step]]\nid = "a"\nanchor = "canvas"\nuntil = "next"\ntext = "x"\n'
    p.write_text(one + one)
    with pytest.raises(ValueError, match="step 2 .a.: duplicate id 'a'"):
        load_steps(p)


def test_paragraphs_and_code() -> None:
    text = "First line\njoined.\n\nType:\n\n    Nand(a=a, b=b, out=out);\n\nThen save."
    assert paragraphs(text) == [
        ("First line joined.", False),
        ("Type:", False),
        ("Nand(a=a, b=b, out=out);", True),
        ("Then save.", False),
    ]


def test_bubble_sits_beside_its_anchor() -> None:
    bounds = (0, 0, 1000, 800)
    # Room on the right: goes there, vertically centred on the anchor.
    assert place_bubble((100, 300, 50, 20), (200, 100), bounds) == (164, 260, 200, 100)
    # Anchor at the right edge: goes to the left.
    assert place_bubble((900, 300, 90, 20), (200, 100), bounds) == (686, 260, 200, 100)
    # A wide anchor: goes below it.
    assert place_bubble((0, 100, 1000, 40), (200, 100), bounds) == (400, 154, 200, 100)
    # No anchor: centred.
    assert place_bubble(None, (200, 100), bounds) == (400, 350, 200, 100)


def test_bubble_never_leaves_the_window() -> None:
    bounds = (0, 0, 400, 300)
    x, y, w, h = place_bubble((0, 0, 400, 300), (200, 100), bounds)  # anchor fills it all
    assert 0 <= x and x + w <= 400 and 0 <= y and y + h <= 300
