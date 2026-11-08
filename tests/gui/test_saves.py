"""Save store tests: stubs as starting text, atomic saves, sticky progress, unlocking."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import pytest

from nandsim.gui.saves import SaveStore
from nandsim.hdl import HdlError
from nandsim.testing import Impl, Level, load_levels, run_tst

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


NOT_AS_BUF = (
    "CHIP Not {\n    IN in;\n    OUT out;\n    PARTS:\n"
    "    Not(in=in, out=n);\n    Not(in=n, out=out);\n}"
)


def solve_not(store: SaveStore) -> None:
    store.save(LEVELS["Not"], LEVELS["Not"].reference.read_text())
    store.mark_solved(LEVELS["Not"])


def test_exported_chip_is_renamed_and_joins_the_library(store: SaveStore) -> None:
    assert store.exports == store.root.parent / "save-exports"
    assert store.exported() == [] and not store.exports.exists()
    solve_not(store)
    text = store.prepare_export("Buf", NOT_AS_BUF)
    assert text == NOT_AS_BUF.replace("CHIP Not", "CHIP Buf")  # only the name changes
    path = store.export("Buf", text)
    assert path == store.exports / "Buf.hdl" and path.read_text() == text
    assert store.exported() == ["Buf"]
    assert store.library().resolve("Buf").name == "Buf"


def test_reset_moves_exported_chips_to_the_backup_too(store: SaveStore) -> None:
    store.exports.mkdir(parents=True)
    (store.exports / "Buf.hdl").write_text("CHIP Buf {}")
    (store.exports / "notes.txt").write_text("mine")  # the folder ends up empty
    assert store.has_progress()  # exported chips alone are something to lose
    dest = store.reset(now=datetime(2026, 11, 6, 20, 0, 0))
    assert dest is not None
    assert sorted(p.name for p in (dest / "exports").iterdir()) == ["Buf.hdl", "notes.txt"]
    assert list(store.exports.iterdir()) == [] and store.exported() == []
    assert not store.has_progress()
    with pytest.raises(HdlError, match="unknown chip 'Buf'"):
        store.library().resolve("Buf")


def test_delete_export_moves_it_to_a_backup(store: SaveStore) -> None:
    solve_not(store)
    store.export("Buf", store.prepare_export("Buf", NOT_AS_BUF))
    store.export("Two", "CHIP Two { IN in; OUT out; PARTS: Buf(in=in, out=out); }")
    when = datetime(2026, 11, 6, 20, 0, 0)
    gone = store.delete_export("Two", now=when)
    assert gone == store.backups / "2026-11-06_200000" / "exports" / "Two.hdl"
    assert gone.read_text().startswith("CHIP Two")  # kept, not destroyed
    assert store.exported() == ["Buf"]
    gone = store.delete_export("Buf", now=when)  # same second: a folder of its own
    assert gone == store.backups / "2026-11-06_200000-2" / "exports" / "Buf.hdl"
    assert store.exported() == [] and store.has_progress()  # Not is still saved


def test_users_of_finds_saved_and_exported_chips_that_use_a_chip(store: SaveStore) -> None:
    solve_not(store)
    store.export("Buf", store.prepare_export("Buf", NOT_AS_BUF))
    store.export("Two", "CHIP Two { IN in; OUT out; PARTS: Buf(in=in, out=out); }")
    store.save(LEVELS["And"], "CHIP And { IN a, b; OUT out; PARTS: Buf(in=a, out=out); }")
    store.save(LEVELS["Or"], "CHIP Or { broken")  # doesn't parse: skipped
    assert store.users_of("Buf") == ["And", "Two"]
    assert store.users_of("Not") == ["Buf"]
    assert store.users_of("Two") == []


@pytest.mark.parametrize(
    ("name", "problem"),
    [
        ("", "Type a name for the chip."),
        ("2Fast", "A chip name starts with a letter and has only letters, digits and _."),
        ("My Chip", "A chip name starts with a letter and has only letters, digits and _."),
        ("PARTS", "PARTS is a word of the HDL. Pick another name."),
        ("Nand", "Nand is a built-in chip. Pick another name."),
        ("DFF", "DFF is a built-in chip. Pick another name."),
        ("Xor", "Xor is a level's chip. Pick another name, like MyXor."),
    ],
)
def test_export_names_that_are_taken_or_invalid(store: SaveStore, name: str, problem: str) -> None:
    assert store.name_problem(name) == problem
    with pytest.raises(ValueError, match=f"^{re.escape(problem)}$"):
        store.prepare_export(name, NOT_AS_BUF)
    assert store.name_problem("my_Chip2") is None


DFF_CHIP = "CHIP Delay {\n    IN in;\n    OUT out;\n    PARTS:\n    DFF(in=in, out=out);\n}"
NO_DFF_YET = "It uses DFF, which no level you have unlocked allows yet."


def test_export_refuses_dff_until_a_level_allows_it(store: SaveStore) -> None:
    # No level lists DFF yet, so it can't reach levels through an exported chip.
    with pytest.raises(ValueError, match=f"^{re.escape(NO_DFF_YET)}$"):
        store.prepare_export("Delay", DFF_CHIP)
    # Hidden one level down, inside a saved chip, it is still found.
    store.save(LEVELS["Not"], DFF_CHIP.replace("Delay", "Not"))
    with pytest.raises(ValueError, match=f"^{re.escape(NO_DFF_YET)}$"):
        store.prepare_export("Buf", NOT_AS_BUF)


def test_export_may_use_dff_once_a_level_listing_it_is_unlocked(tmp_path: Path) -> None:
    levels = load_levels()
    bit = Level("Bit", "04_seq", ("Nand", "DFF", "Not"), levels[0].root)
    store = SaveStore([*levels, bit], tmp_path / "save")
    with pytest.raises(ValueError, match=f"^{re.escape(NO_DFF_YET)}$"):
        store.prepare_export("Delay", DFF_CHIP)  # Bit still needs Not
    solve_not(store)
    with pytest.raises(ValueError, match=f"^{re.escape(NO_DFF_YET)}$"):
        store.prepare_export("Delay", DFF_CHIP)  # and the player's own DFF
    store.mark_solved(next(lv for lv in levels if lv.name == "DFF"))
    assert store.prepare_export("Delay", DFF_CHIP) == DFF_CHIP


def test_export_needs_a_chip_that_builds(store: SaveStore) -> None:
    # Not isn't saved yet: the editor's positions are kept in the message.
    with pytest.raises(ValueError, match=r"^It doesn't build yet: line 5:5: unknown chip 'Not'$"):
        store.prepare_export("Buf", NOT_AS_BUF)
    with pytest.raises(ValueError, match=r"^It doesn't build yet: line 1:6: expected a chip name"):
        store.prepare_export("Buf", "CHIP {")
    solve_not(store)
    loop = NOT_AS_BUF.replace("Not(in=n", "Buf(in=n")  # Buf would contain itself
    with pytest.raises(ValueError, match="^It doesn't build yet: .*Buf"):
        store.prepare_export("Buf", loop)
