"""Game rules: statuses, unlocking, building and testing with the player's own chips."""

from __future__ import annotations

from pathlib import Path

import pytest

from nandsim.gui.game import GameState
from nandsim.gui.saves import SaveStore
from nandsim.testing import load_levels

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
    assert game.current.name == "Hello"
    r = game.run_tests(solution("Hello"))
    assert r.passed and r.lines == []  # no later level uses Hello, so nothing new unlocks
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


def test_solving_unlocks_and_uses_the_players_chips(game: GameState) -> None:
    r = game.run_tests(solution("Not"))
    assert r.passed and r.summary == "All 2 checks passed"
    assert r.lines == ["Unlocked: And"]
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
