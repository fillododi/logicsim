"""Menu tests: the title screen, the Esc pause menu and resetting the game, driven headless."""

from __future__ import annotations

import json
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
    assert app.on_title and labels(app) == [
        "Play",
        "Sound: On",
        "Volume: 60%",
        "Quit",
    ]  # nothing to reset
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
    assert labels(app) == ["Continue", "Reset game…", "Sound: On", "Volume: 60%", "Quit"]


def test_esc_pauses_from_the_editor_and_resume_restores_focus(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    assert app.editing
    key(app, pygame.K_ESCAPE)
    assert app.menus and app.menus[0].title == "Paused" and not app.editing
    assert labels(app) == [
        "Resume",
        "Replay the tour",
        "Export this chip as…",
        "Main menu",
        "Reset game…",
        "Sound: On",
        "Volume: 60%",
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


# ---- exporting chips ------------------------------------------------------------

BUF = (
    "CHIP Not {\n    IN in;\n    OUT out;\n    PARTS:\n"
    "    Nand(a=in, b=in, out=n);\n    Nand(a=n, b=n, out=out);\n}\n"
)


def field(app: GameApp, text: str) -> None:
    """Clear the dialog's text field and type `text` into it."""
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=pygame.KMOD_CTRL))
    type_text(app, text)
    app.render(pygame.Surface(app.size))


def at_not(tmp_path: Path) -> GameApp:
    """The game open on Not (the tutorial solved), with BUF unsaved in the editor."""
    save = tmp_path / "save"
    store = SaveStore(load_levels(), save)
    for name in ("Wire", "Hello"):
        store.save(LEVELS[name], LEVELS[name].reference.read_text())
        store.mark_solved(LEVELS[name])
    app = new_app(save)
    app.open_level(LEVELS["Not"])
    assert app.editor is not None
    app.editor.buffer.select_all()
    app.editor.buffer.insert(BUF)
    return app


def test_export_names_the_chip_and_any_level_can_use_it(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    assert app.editor is not None
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    dialog = app.menus[-1]
    assert dialog.title == "Export this chip" and dialog.text == "MyNot"  # a suggestion
    key(app, pygame.K_SPACE)  # Space types nothing and presses nothing
    assert app.menus[-1] is dialog and dialog.text == "MyNot"
    field(app, "Buf")
    key(app, pygame.K_RETURN)  # Enter presses Export, the first button
    path = tmp_path / "save-exports" / "Buf.hdl"
    assert path.read_text() == BUF.replace("CHIP Not", "CHIP Buf")
    assert app.menus == [] and app.editing
    assert app.notice == "Exported Buf. Every level can now use it as a part: Buf(...)"
    assert app.editor.buffer.dirty and "CHIP Not" in app.editor.buffer.text  # untouched

    # Not may use only Nand, and now Buf too: a Not made of Bufs passes.
    app.editor.buffer.select_all()
    app.editor.buffer.insert(
        "CHIP Not { IN in; OUT out; PARTS: Buf(in=in, out=b); Nand(a=b, b=b, out=out); }"
    )
    app.run_tests()
    assert app.game.report is not None and app.game.report.passed, app.game.report.lines
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    assert app.menus[-1].text == "Buf"  # the level's last name comes back


def test_export_problems_show_in_the_dialog(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    dialog = app.menus[-1]
    field(app, "Xor")
    click_item(app, "Export")
    assert app.menus[-1] is dialog
    assert dialog.error == "Xor is a level's chip. Pick another name, like MyXor."
    type_text(app, "!2")  # only name characters reach the field; typing clears the error
    assert dialog.text == "Xor2" and dialog.error == ""
    assert app.editor is not None
    app.editor.buffer.insert("oops")  # the editor text no longer builds
    click_item(app, "Export")
    assert dialog.error.startswith("It doesn't build yet: line 8:")
    assert not (tmp_path / "save-exports").exists()
    click_item(app, "Cancel")
    assert app.menus[-1].title == "Paused"


def test_export_asks_before_replacing_a_different_chip(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    assert app.editor is not None
    path = tmp_path / "save-exports" / "Buf.hdl"
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    field(app, "Buf")
    click_item(app, "Export")
    first = path.read_text()
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")  # same text again: nothing to confirm
    click_item(app, "Export")
    assert app.menus == []

    app.editor.buffer.insert("// v2\n")
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    click_item(app, "Export")
    assert app.menus[-1].title == "Replace Buf?"
    assert labels(app)[app.menus[-1].selected] == "Cancel"
    key(app, pygame.K_RETURN)
    assert app.menus[-1].title == "Export this chip" and path.read_text() == first
    click_item(app, "Export")
    click_item(app, "Replace it")
    assert path.read_text().endswith("// v2\n") and app.menus == []


def test_sidebar_lists_exported_chips(tmp_path: Path) -> None:
    exports = tmp_path / "save-exports"
    exports.mkdir()
    (exports / "Buf.hdl").write_text("CHIP Buf {}")
    (exports / "Not.hdl").write_text("CHIP Not {}")  # a level's name: never a chip of yours
    app = new_app(tmp_path / "save")
    assert app._exported == ["Buf"]


def click(app: GameApp, pos: tuple[int, int]) -> None:
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))
    app.render(pygame.Surface(app.size))


def export_buf(app: GameApp) -> None:
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    field(app, "Buf")
    click_item(app, "Export")


def test_delete_button_asks_then_takes_the_chip_out(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    assert app.editor is not None
    export_buf(app)
    assert [name for _, name in app._chip_rows] == ["Buf"]
    # Not now uses Buf: the dialog says so, and Cancel keeps everything.
    app.editor.buffer.select_all()
    app.editor.buffer.insert(
        "CHIP Not { IN in; OUT out; PARTS: Buf(in=in, out=b); Nand(a=b, b=b, out=out); }"
    )
    app.save()
    assert app.session.error is None
    click(app, app._chip_rows[0][0].center)
    dialog = app.menus[-1]
    assert dialog.title == "Delete Buf?" and "Used by Not:" in dialog.message
    assert labels(app)[dialog.selected] == "Cancel"
    key(app, pygame.K_RETURN)
    assert app.menus == [] and (tmp_path / "save-exports" / "Buf.hdl").is_file()

    click(app, app._chip_rows[0][0].center)
    click_item(app, "Delete it")
    assert app.menus == [] and app._exported == [] and app._chip_rows == []
    assert not (tmp_path / "save-exports" / "Buf.hdl").exists()
    backups = list((tmp_path / "save-backups").glob("*/exports/Buf.hdl"))
    assert len(backups) == 1  # moved, not destroyed
    assert app.notice is not None and app.notice.startswith("Deleted Buf. Its file is in ")
    # The circuit on screen used Buf: it is rebuilt, and no longer builds.
    assert app.session.error is not None and "unknown chip 'Buf'" in app.session.error.message


def test_reset_takes_exported_chips_away(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    export_buf(app)
    key(app, pygame.K_ESCAPE)
    click_item(app, "Reset game…")
    assert "the chips you exported" in app.menus[-1].message
    click_item(app, "Reset the game")
    assert app._exported == [] and not list((tmp_path / "save-exports").iterdir())
    assert list((tmp_path / "save-backups").glob("*/exports/Buf.hdl"))
    key(app, pygame.K_ESCAPE)
    click_item(app, "Export this chip as…")
    assert app.menus[-1].text == "MyWire"  # the old export names are forgotten too


# ---- sound ----------------------------------------------------------------------


def test_game_events_play_their_sounds(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    assert app.editor is not None and app.sounds.enabled  # the dummy audio driver
    app.tour.skip()  # its bubble would sit over the canvas
    app.save()  # BUF builds: no error sound
    assert "error" not in app.sounds.played
    snap = app.session.snapshot
    assert snap is not None
    b = snap.layout.boxes[("in", "in")]
    pos = app.screen_of((b.x + b.w / 2, b.y + b.h / 2))
    click(app, pos)  # the first click on the circuit only leaves the editor
    assert "toggle" not in app.sounds.played
    click(app, pos)
    assert app.sounds.played[-1] == "toggle"
    app.run_tests()  # BUF is a buffer, not a Not
    assert app.sounds.played[-1] == "fail"
    app.editor.buffer.select_all()
    app.editor.buffer.insert(LEVELS["Not"].reference.read_text())
    app.run_tests()
    assert app.sounds.played[-1] == "solved"
    app.run_tests()  # already solved: a plain pass
    assert app.sounds.played[-1] == "pass"
    app.editor.buffer.insert("oops")
    app.save()
    assert app.sounds.played[-1] == "error"


def test_menus_tick_blip_and_buzz(tmp_path: Path) -> None:
    app = at_not(tmp_path)
    key(app, pygame.K_ESCAPE)
    assert app.sounds.played[-1] == "select"  # the pause menu opens
    key(app, pygame.K_DOWN)
    assert app.sounds.played[-1] == "move"
    click_item(app, "Export this chip as…")
    assert app.sounds.played[-1] == "select"
    field(app, "Xor")  # typing is silent
    assert app.sounds.played[-1] == "select"
    key(app, pygame.K_RETURN)
    assert app.sounds.played[-1] == "error"  # a refused name
    key(app, pygame.K_ESCAPE)
    assert app.sounds.played[-1] == "back"


def test_sound_and_volume_change_in_place_and_are_remembered(tmp_path: Path) -> None:
    save = tmp_path / "save"
    app = new_app(save)
    key(app, pygame.K_ESCAPE)
    click_item(app, "Volume: 60%")
    assert labels(app)[app.menus[-1].selected] == "Volume: 80%"  # same row, new label
    assert app.sounds.played[-1] == "select" and app.sounds.played.count("select") == 2
    click_item(app, "Volume: 80%")
    click_item(app, "Volume: 100%")
    assert "Volume: 20%" in labels(app)  # wraps around
    click_item(app, "Sound: On")
    assert "Sound: Off" in labels(app) and app.settings.muted
    before = list(app.sounds.played)
    key(app, pygame.K_DOWN)
    key(app, pygame.K_UP)
    assert app.sounds.played == before  # muted: nothing more is played
    settings = json.loads((tmp_path / "save-settings.json").read_text())
    assert settings == {"version": 1, "muted": True, "volume": 0.2}

    again = new_app(save, title=True)  # read back on the next start, on the title screen too
    assert "Sound: Off" in labels(again) and "Volume: 20%" in labels(again)
    click_item(again, "Sound: Off")
    assert again.sounds.played == ["select"]  # unmuting plays the preview
