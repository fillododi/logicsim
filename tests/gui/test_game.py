"""Game rules: statuses, unlocking, building and testing with the player's own chips."""

from __future__ import annotations

from pathlib import Path

import pytest

from nandsim.gui.game import GameState, group_label
from nandsim.gui.saves import SaveStore
from nandsim.testing import Level, load_levels

LEVELS = {lv.name: lv for lv in load_levels()}


def solution(name: str) -> str:
    # Tests may read the reference; the game code never does.
    return LEVELS[name].reference.read_text()


@pytest.fixture
def game(tmp_path: Path) -> GameState:
    g = GameState(SaveStore(load_levels(), tmp_path / "save"))
    assert g.select(LEVELS["Not"])  # most tests here are about the first real gate
    return g


def test_new_game_starts_at_the_tutorial(tmp_path: Path) -> None:
    game = GameState(SaveStore(load_levels(), tmp_path / "save"))
    assert game.current.name == "Wire"
    r = game.run_tests(solution("Wire"))
    assert r.passed and r.lines == []  # no later level uses Wire, so nothing new unlocks
    assert GameState(game.store).current.name == "Hello"
    assert game.select(LEVELS["Hello"]) and game.run_tests(solution("Hello")).passed
    assert GameState(game.store).current.name == "Not"


def test_not_is_open_without_the_tutorial(game: GameState) -> None:
    assert game.current.name == "Not"
    assert game.status(LEVELS["Not"]) == "open"
    assert game.status(LEVELS["And"]) == "locked"
    assert game.missing(LEVELS["Or"]) == ["Not", "And"]
    assert not game.select(LEVELS["And"])
    assert game.text() == LEVELS["Not"].stub.read_text()


def test_empty_stub_does_not_build(game: GameState) -> None:
    r = game.run_tests(game.text())
    assert not r.passed and r.summary == "Doesn't build"
    assert r.lines[0].endswith("output pin 'out' of Not is not connected")
    assert r.lines[1] == (
        "Tip: Every OUT pin needs a driver: end a part with out=out, or write out = <signal>;"
    )


def test_wrong_solution_lists_failing_rows(game: GameState) -> None:
    wrong = solution("Not").replace("b=in", "b=false")
    r = game.run_tests(wrong)
    assert not r.passed and r.summary == "1 of 2 checks failed"
    assert r.lines == ["test line 5: out: expected 0, got 1 (inputs in=1)"]
    assert game.status(LEVELS["Not"]) == "open"


def test_a_loop_that_never_settles_is_named_with_a_tip(game: GameState) -> None:
    # y = Nand(in, y): with in=1 it is a Not wired to itself.
    looped = "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=y, out=y, out=out); }"
    r = game.run_tests(looped)
    assert not r.passed and r.summary == "1 of 2 checks failed"
    assert r.lines == [
        "test line 5: out: expected 0, got undefined (inputs in=1, a loop didn't settle: y)",
        "Tip: A wire that feeds back into itself must come to rest, but y kept flipping, "
        "like a Not wired to its own input. A wire that never settles shows as undefined.",
    ]


def test_solving_unlocks_and_uses_the_players_chips(game: GameState) -> None:
    r = game.run_tests(solution("Not"))
    assert r.passed and r.summary == "All 2 checks passed"
    assert r.lines == ["Unlocked: And, Not4"]  # Not4 widens Not
    assert game.status(LEVELS["Not"]) == "solved"
    game.save(solution("Not"))
    assert game.select(LEVELS["And"])
    assert game.run_tests(solution("And")).passed  # And uses the player's saved Not
    game.save(solution("And"))
    # Break the saved Not: And now fails, because it is built from the player's Not.
    game.select(LEVELS["Not"])
    game.save("CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=false, out=out); }")
    game.select(LEVELS["And"])
    assert not game.run_tests(solution("And")).passed
    assert game.status(LEVELS["And"]) == "solved"  # solved is sticky


def test_part_not_allowed(game: GameState) -> None:
    game.run_tests(solution("Not"))
    game.save(solution("Not"))
    r = game.run_tests(
        "CHIP Not { IN in; OUT out; PARTS: Not(in=in, out=out); }"
    )  # using itself is not allowed (and circular)
    assert not r.passed and r.summary == "Doesn't build"


def test_loader_builds_last_saved_text(game: GameState) -> None:
    name, lib = game.loader()()
    assert name == "Not" and lib.resolve("Not").parts == ()
    game.save(solution("Not"))
    _, lib = game.loader()()
    assert len(lib.resolve("Not").parts) == 1


def test_resumes_past_the_furthest_solved_level(tmp_path: Path) -> None:
    store = SaveStore(load_levels(), tmp_path / "save")
    for name in ("Not", "And"):  # the tutorial was skipped
        store.mark_solved(LEVELS[name])
    assert GameState(store).current.name == "Or"


def fake_store(tmp_path: Path) -> SaveStore:
    """Four groups and no files: grouping and unlocking only read names and parts."""
    root = tmp_path / "data"
    levels = [
        Level("Wire", "00_tutorial", (), root),
        Level("Not", "01_gates", ("Nand",), root),
        Level("And", "01_gates", ("Nand", "Not"), root),
        Level("Not4", "02_buses", ("Not",), root),
        Level("Add4", "03_arith", ("Not4",), root),
    ]
    return SaveStore(levels, tmp_path / "save")


def test_groups_keep_the_level_order(tmp_path: Path) -> None:
    game = GameState(fake_store(tmp_path))
    assert [(g, [lv.name for lv in lvs]) for g, lvs in game.groups()] == [
        ("00_tutorial", ["Wire"]),
        ("01_gates", ["Not", "And"]),
        ("02_buses", ["Not4"]),
        ("03_arith", ["Add4"]),
    ]
    assert group_label("00_tutorial") == "Tutorial" and group_label("02_buses") == "Buses"
    assert group_label("03_arith") == "Arithmetic"


def test_default_groups_are_the_current_one_and_the_next_with_work(tmp_path: Path) -> None:
    game = GameState(fake_store(tmp_path))
    lv = {lv.name: lv for lv in game.levels}
    assert game.current.name == "Wire"
    assert game.default_expanded() == {"00_tutorial", "01_gates"}  # Not is open from the start
    assert game.select(lv["Not"])
    assert game.default_expanded() == {"01_gates"}  # Not4 is still locked
    game.store.mark_solved(lv["Not"])
    assert game.default_expanded() == {"01_gates", "02_buses"}
    game.store.mark_solved(lv["Not4"])
    # Buses has nothing left to do, so Arithmetic takes its place: never more than two groups.
    assert game.default_expanded() == {"01_gates", "03_arith"}
