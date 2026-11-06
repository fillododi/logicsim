"""Menu tests: the title screen, the Esc pause menu and resetting the game, driven headless."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.game_app import GameApp  # noqa: E402
from nandsim.gui.menu import BACK, Menu, MenuItem  # noqa: E402
from nandsim.gui.saves import SaveStore  # noqa: E402
from nandsim.gui.theme import Fonts  # noqa: E402
from nandsim.testing import load_levels  # noqa: E402

LEVELS = {lv.name: lv for lv in load_levels()}


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def new_app(save: Path, title: bool = False) -> GameApp:
    app = GameApp(SaveStore(load_levels(), save), size=(1280, 800), title_screen=title)
    app.render(pygame.Surface(app.size))
    return app


def key(app: GameApp, k: int) -> None:
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode=""))
    app.render(pygame.Surface(app.size))


def type_text(app: GameApp, text: str) -> None:
    app.handle(pygame.event.Event(pygame.TEXTINPUT, text=text))


def click_item(app: GameApp, label: str) -> None:
    menu = app.menus[-1]
    i = next(i for i, it in enumerate(menu.items) if it.label == label)
    pos = menu.rects[i].center
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))
    app.render(pygame.Surface(app.size))


def labels(app: GameApp) -> list[str]:
    return [it.label for it in app.menus[-1].items]


def test_menu_keyboard_and_mouse() -> None:
    m = Menu("T", [MenuItem("A", "a"), MenuItem("B", "b"), MenuItem("C", "c")])
    surf = pygame.Surface((800, 600))
    m.draw(surf, Fonts(), surf.get_rect())
    down = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
    up = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode="")
    enter = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="")
    esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    assert m.handle(down) is None and m.selected == 1
    assert m.handle(up) is None and m.handle(up) is None and m.selected == 2  # wraps
    assert m.handle(enter) == "c"
    assert m.handle(esc) == BACK
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=m.rects[0].center, button=1)
    assert m.handle(click) == "a"
    miss = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(1, 1), button=1)
    assert m.handle(miss) is None


def test_title_screen_plays_and_esc_does_not_leave_it(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save", title=True)
    assert app.on_title and labels(app) == ["Play", "Quit"]  # nothing to reset yet
    assert not app.editing
    key(app, pygame.K_ESCAPE)
    assert app.on_title  # nowhere to go back to
    type_text(app, "x")  # keys never reach the editor behind the menu
    assert app.editor is not None and not app.editor.buffer.dirty
    key(app, pygame.K_RETURN)
    assert not app.on_title and app.menus == [] and app.editing


def test_title_offers_continue_and_reset_once_started(tmp_path: Path) -> None:
    save = tmp_path / "save"
    SaveStore(load_levels(), save).save(LEVELS["Wire"], "CHIP Wire {}")
    app = new_app(save, title=True)
    assert labels(app) == ["Continue", "Reset game…", "Quit"]


def test_esc_pauses_from_the_editor_and_resume_restores_focus(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    assert app.editing
    key(app, pygame.K_ESCAPE)
    assert app.menus and app.menus[0].title == "Paused" and not app.editing
    assert labels(app) == [
        "Resume",
        "Replay the tour",
        "Export this chip",
        "Import a chip…",
        "Main menu",
        "Reset game…",
        "Quit",
    ]
    key(app, pygame.K_ESCAPE)  # Esc again resumes
    assert app.menus == [] and app.editing


def test_main_menu_and_back(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    key(app, pygame.K_ESCAPE)
    click_item(app, "Main menu")
    assert app.on_title and app.menus[0].title == "NAND Sim"
    click_item(app, "Play")
    assert not app.on_title and app.menus == []


def test_quit_keeps_unsaved_text(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    type_text(app, "// mine\n")
    assert app.editor is not None and app.editor.buffer.dirty
    key(app, pygame.K_ESCAPE)
    click_item(app, "Quit")
    assert app.quit_requested
    app.before_quit()  # what run() does on its way out
    assert (tmp_path / "save" / "Wire.hdl").read_text() == app.editor.buffer.text


def test_reset_needs_confirmation_and_cancel_keeps_everything(tmp_path: Path) -> None:
    save = tmp_path / "save"
    store = SaveStore(load_levels(), save)
    store.save(LEVELS["Wire"], LEVELS["Wire"].reference.read_text())
    store.mark_solved(LEVELS["Wire"])
    app = new_app(save)
    key(app, pygame.K_ESCAPE)
    click_item(app, "Reset game…")
    assert app.menus[-1].title == "Reset the game?"
    assert labels(app)[app.menus[-1].selected] == "Cancel"  # Enter by mistake is harmless
    key(app, pygame.K_RETURN)
    assert app.menus[-1].title == "Paused"
    assert app.game.store.solved == {"Wire"} and (save / "Wire.hdl").is_file()


def test_reset_starts_over_and_keeps_a_backup(tmp_path: Path) -> None:
    save = tmp_path / "save"
    store = SaveStore(load_levels(), save)
    for name in ("Wire", "Hello", "Not"):
        store.save(LEVELS[name], LEVELS[name].reference.read_text())
        store.mark_solved(LEVELS[name])
    app = new_app(save)
    app.tour.skip()
    assert app.game.current.name == "And"
    type_text(app, "// unsaved")
    key(app, pygame.K_ESCAPE)
    click_item(app, "Reset game…")
    click_item(app, "Reset the game")

    assert app.menus == [] and app.editing
    assert app.game.current.name == "Wire" and app.game.store.solved == frozenset()
    assert app.editor is not None
    assert app.editor.buffer.text == LEVELS["Wire"].stub.read_text()
    assert not app.tour.skipped and app.tour.current is not None  # the tour starts over
    assert app.game.status(LEVELS["And"]) == "locked"
    assert sorted(p.name for p in save.iterdir()) == []  # the unsaved text was not written
    (backup,) = (tmp_path / "save-backups").iterdir()
    assert {"Wire.hdl", "Hello.hdl", "Not.hdl", "progress.json", "tutorial.json"} <= {
        p.name for p in backup.iterdir()
    }
    assert app.notice is not None and backup.name in app.notice


def test_reset_from_the_title_screen(tmp_path: Path) -> None:
    save = tmp_path / "save"
    SaveStore(load_levels(), save).save(LEVELS["Wire"], "CHIP Wire {}")
    app = new_app(save, title=True)
    click_item(app, "Reset game…")
    click_item(app, "Reset the game")
    assert not app.on_title and app.menus == [] and app.editing
    assert not app.game.store.has_progress()


def test_help_line_names_the_menu_key(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    assert app.help_text.startswith("Esc: menu  ·  F1: tour")
    assert "Esc: back" not in app.help_text  # the editor's Esc item doesn't apply in the game


# ---- chip files --------------------------------------------------------------


def test_export_writes_the_editor_text_and_asks_before_replacing(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    assert app.editor is not None
    type_text(app, "// v1\n")  # unsaved text is exported as the player sees it
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip")
    path = tmp_path / "save-exports" / "Wire.hdl"
    assert path.read_text() == app.editor.buffer.text
    assert app.menus == [] and app.editing and app.notice is not None
    assert app.notice.startswith("Exported Wire to ")
    assert app.editor.buffer.dirty  # exporting is not saving the level

    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip")  # same text: nothing to confirm
    assert app.menus == []

    type_text(app, "// v2\n")
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip")
    assert app.menus[-1].title == "Replace Wire.hdl?"
    assert labels(app)[app.menus[-1].selected] == "Cancel"
    key(app, pygame.K_RETURN)
    assert app.menus[-1].title == "Paused" and "v2" not in path.read_text()
    click_item(app, "Export this chip")
    click_item(app, "Replace it")
    assert path.read_text() == app.editor.buffer.text and app.menus == []


def test_import_with_no_files_says_where_to_put_them(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    key(app, pygame.K_ESCAPE)
    click_item(app, "Import a chip…")
    assert labels(app) == ["Back"] and "save-exports" in app.menus[-1].message
    click_item(app, "Back")
    assert app.menus[-1].title == "Paused"


def test_import_is_unsaved_undoable_text_until_saved_or_tested(tmp_path: Path) -> None:
    save = tmp_path / "save"
    store = SaveStore(load_levels(), save)
    answer = LEVELS["Wire"].reference.read_text()
    store.export(LEVELS["Wire"], answer)
    store.export(LEVELS["Not"], "CHIP Not {}")
    app = new_app(save)
    assert app.editor is not None
    before = app.editor.buffer.text
    key(app, pygame.K_ESCAPE)
    click_item(app, "Import a chip…")
    assert app.menus[-1].title == "Import into Wire"
    assert labels(app) == ["Wire.hdl  (this level)", "Not.hdl", "Back"]
    click_item(app, "Wire.hdl  (this level)")
    assert app.menus == [] and app.editing
    assert app.editor.buffer.text == answer and app.editor.buffer.dirty
    assert app.notice is not None and app.notice.startswith("Imported Wire.hdl")
    # Importing alone neither saves nor solves the level.
    assert not (save / "Wire.hdl").exists() and "Wire" not in app.game.store.solved

    app.editor.buffer.undo()
    assert app.editor.buffer.text == before
    app.editor.buffer.redo()
    app.run_tests()
    assert "Wire" in app.game.store.solved and (save / "Wire.hdl").read_text() == answer


def test_import_pages_through_many_files_and_reports_bad_ones(tmp_path: Path) -> None:
    save = tmp_path / "save"
    exports = tmp_path / "save-exports"
    exports.mkdir()
    for i in range(10):
        (exports / f"C{i}.hdl").write_text(f"// {i}")
    (exports / "Bad.hdl").write_bytes(b"\xff\xfe")
    app = new_app(save)
    key(app, pygame.K_ESCAPE)
    click_item(app, "Import a chip…")
    assert labels(app)[0] == "Bad.hdl" and labels(app)[-2:] == ["Next page", "Back"]
    assert "Page 1 of 2." in app.menus[-1].message
    click_item(app, "Next page")
    assert labels(app) == [
        "C5.hdl",
        "C6.hdl",
        "C7.hdl",
        "C8.hdl",
        "C9.hdl",
        "Previous page",
        "Back",
    ]
    click_item(app, "Back")  # back from any page returns to the pause menu
    assert app.menus[-1].title == "Paused"
    click_item(app, "Import a chip…")
    text = app.editor.buffer.text if app.editor else ""
    click_item(app, "Bad.hdl")
    assert app.notice == "Couldn't import: Bad.hdl isn't a text file"
    assert app.editor is not None and app.editor.buffer.text == text
