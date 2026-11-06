"""Save store tests: stubs as starting text, atomic saves, sticky progress, unlocking."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from nandsim.gui.saves import SaveStore
from nandsim.testing import Impl, load_levels, run_tst

LEVELS = {lv.name: lv for lv in load_levels()}


@pytest.fixture
def store(tmp_path: Path) -> SaveStore:
    return SaveStore(load_levels(), tmp_path / "save")


def test_new_player_sees_stub_and_only_first_level_unlocked(store: SaveStore) -> None:
    assert store.load(LEVELS["Not"]) == LEVELS["Not"].stub.read_text()
    assert not store.has_save(LEVELS["Not"])
    unlocked = [lv.name for lv in store.levels if store.is_unlocked(lv)]
    assert unlocked == ["Hello", "Not"]  # the tutorial is optional


def test_save_round_trip_and_cli_compatible(store: SaveStore) -> None:
    not_ref = LEVELS["Not"].reference.read_text()
    store.save(LEVELS["Not"], not_ref)
    assert store.load(LEVELS["Not"]) == not_ref
    assert not list(store.root.glob("*.tmp"))
    # The CLI's --impl save reads the same directory.
    assert run_tst(LEVELS["Not"].tst, Impl("save", store.root)).passed


def test_solving_unlocks_dependents_and_persists(store: SaveStore, tmp_path: Path) -> None:
    store.mark_solved(LEVELS["Not"])
    assert store.is_unlocked(LEVELS["And"])
    assert not store.is_unlocked(LEVELS["Or"])  # needs And too
    store.mark_solved(LEVELS["And"])
    assert store.is_unlocked(LEVELS["Or"])
    again = SaveStore(load_levels(), store.root)
    assert again.solved == {"Not", "And"}
    data = json.loads((store.root / "progress.json").read_text())
    assert data == {"version": 1, "solved": ["And", "Not"]}


def test_unreadable_progress_is_kept_aside_not_fatal(tmp_path: Path) -> None:
    root = tmp_path / "save"
    root.mkdir()
    (root / "progress.json").write_text("{not json")
    s = SaveStore(load_levels(), root)
    assert s.solved == frozenset()
    assert s.warning is not None and "progress.json.bad" in s.warning
    assert (root / "progress.json.bad").read_text() == "{not json"


def test_library_prefers_unsaved_editor_text(store: SaveStore) -> None:
    store.save(LEVELS["Not"], "CHIP Not { IN in; OUT out; PARTS: }")
    lib = store.library(LEVELS["Not"], LEVELS["Not"].reference.read_text())
    chip = lib.resolve("Not")
    assert len(chip.parts) == 1  # the editor text, not the empty saved file
    assert store.library().resolve("Not").parts == ()
