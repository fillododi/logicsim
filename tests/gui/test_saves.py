"""Save store tests: stubs as starting text, atomic saves, sticky progress, unlocking."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from nandsim.gui.saves import SaveStore
from nandsim.hdl import HdlError
from nandsim.testing import Impl, load_levels, run_tst

LEVELS = {lv.name: lv for lv in load_levels()}


@pytest.fixture
def store(tmp_path: Path) -> SaveStore:
    return SaveStore(load_levels(), tmp_path / "save")


def test_new_player_sees_stub_and_only_first_level_unlocked(store: SaveStore) -> None:
    assert store.load(LEVELS["Not"]) == LEVELS["Not"].stub.read_text()
    assert not store.has_save(LEVELS["Not"])
    unlocked = [lv.name for lv in store.levels if store.is_unlocked(lv)]
    assert unlocked == ["Wire", "Hello", "Not"]  # the tutorial is optional


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


def test_reset_moves_everything_to_a_backup(store: SaveStore) -> None:
    assert not store.has_progress()
    assert store.reset() is None  # nothing to back up: nothing is created
    assert not store.backups.exists()

    not_ref = LEVELS["Not"].reference.read_text()
    store.save(LEVELS["Not"], not_ref)
    store.mark_solved(LEVELS["Not"])
    (store.root / "tutorial.json").write_text("{}")
    assert store.has_progress()

    when = datetime(2026, 11, 6, 15, 30, 12)
    dest = store.reset(now=when)
    assert dest == store.root.parent / "save-backups" / "2026-11-06_153012"
    assert sorted(p.name for p in dest.iterdir()) == ["Not.hdl", "progress.json", "tutorial.json"]
    assert (dest / "Not.hdl").read_text() == not_ref  # nothing is lost
    assert not store.has_progress() and store.solved == frozenset()
    assert store.load(LEVELS["Not"]) == LEVELS["Not"].stub.read_text()
    assert SaveStore(load_levels(), store.root).solved == frozenset()  # on disk too
    # The library searches the save dir recursively: the backup must not be found there.
    with pytest.raises(HdlError, match="unknown chip 'Not'"):
        store.library().resolve("Not")

    store.save(LEVELS["Not"], "again")
    assert store.reset(now=when) == store.backups / "2026-11-06_153012-2"


def test_chip_files_live_beside_the_saves_and_survive_a_reset(store: SaveStore) -> None:
    assert store.exports == store.root.parent / "save-exports"
    assert store.chip_files() == []  # no folder yet: nothing to list, nothing created
    assert not store.exports.exists()

    text = LEVELS["Not"].reference.read_text()
    path = store.export(LEVELS["Not"], text)
    assert path == store.exports / "Not.hdl" and store.read_chip_file(path) == text
    store.export(LEVELS["Not"], "newer")  # exporting again replaces the file
    assert store.read_chip_file(path) == "newer"

    store.save(LEVELS["Not"], text)
    store.reset()
    assert store.chip_files() == [path]  # a reset only moves the save directory
    # The library never sees exported files: only saves count as the player's chips.
    with pytest.raises(HdlError, match="unknown chip 'Not'"):
        store.library().resolve("Not")


def test_chip_files_list_the_level_first_and_skip_other_files(store: SaveStore) -> None:
    store.exports.mkdir(parents=True)
    for name in ["and.hdl", "Mux.hdl", "Xor.hdl", "notes.txt", "Not.hdl.tmp"]:
        (store.exports / name).write_text("x")
    (store.exports / "sub.hdl").mkdir()
    assert [p.name for p in store.chip_files()] == ["and.hdl", "Mux.hdl", "Xor.hdl"]
    assert [p.name for p in store.chip_files("Xor")] == ["Xor.hdl", "and.hdl", "Mux.hdl"]


def test_unreadable_chip_file_is_a_message_not_a_crash(store: SaveStore) -> None:
    store.exports.mkdir(parents=True)
    binary = store.exports / "Blob.hdl"
    binary.write_bytes(b"\xff\xfe\x00")
    with pytest.raises(ValueError, match="^Blob.hdl isn't a text file$"):
        store.read_chip_file(binary)
    with pytest.raises(ValueError, match="^couldn't read Gone.hdl: "):
        store.read_chip_file(store.exports / "Gone.hdl")
