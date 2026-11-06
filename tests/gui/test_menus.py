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
    assert labels(app) == ["Resume", "Replay the tour", "Main menu", "Reset game…", "Quit"]
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
