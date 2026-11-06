"""Playtest: a new player solves the first levels using only mouse and keyboard events.

This is the end-to-end check for milestone 2: level select, brief, editor,
saving, building the circuit, running tests, unlocking and persistence.
"""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.game_app import GameApp  # noqa: E402
from nandsim.gui.saves import SaveStore  # noqa: E402
from nandsim.gui.textbuffer import Pos  # noqa: E402
from nandsim.testing import load_levels  # noqa: E402

CTRL = pygame.KMOD_CTRL

NOT = "CHIP Not {\n    IN in;\n    OUT out;\n    PARTS:\n    Nand(a=in, b=in, out=out);\n}\n"
AND_WRONG = "CHIP And {\n    IN a, b;\n    OUT out;\n    PARTS:\n    Nand(a=a, b=b, out=out);\n}\n"


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def keydown(app: GameApp, key: int, mod: int = 0) -> None:
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode=""))


def type_text(app: GameApp, text: str) -> None:
    for ch in text:
        if ch == "\n":
            keydown(app, pygame.K_RETURN)
        else:
            app.handle(pygame.event.Event(pygame.TEXTINPUT, text=ch))


def replace_all(app: GameApp, text: str) -> None:
    """Select everything and paste `text`, as a player pasting a whole chip would."""
    assert app.editor is not None
    app.editor.clipboard.put(text)
    keydown(app, pygame.K_a, CTRL)
    keydown(app, pygame.K_v, CTRL)


def click(app: GameApp, pos: tuple[int, int]) -> None:
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))


def click_level(app: GameApp, name: str) -> None:
    app.render(pygame.Surface(app.size))  # lays out the sidebar rows
    rect = next(r for r, lv in app._rows if lv.name == name)
    click(app, rect.center)


def new_app(save: Path) -> GameApp:
    return GameApp(SaveStore(load_levels(), save), size=(1440, 860))


def test_new_player_solves_not_and_and(tmp_path: Path) -> None:
    save = tmp_path / "save"
    app = new_app(save)
    shots = tmp_path / "shots"
    shots.mkdir()

    # A fresh game opens Not, with its starting text and no error shouted at the player.
    assert app.game.current.name == "Not"
    assert app.editor is not None and app.editor.focused
    assert app.editor.buffer.text == app.game.current.stub.read_text()
    assert not app.show_errors and app.editor.error is None
    app.screenshot(shots / "1-fresh.png")

    # Locked levels can't be opened; the sidebar says why.
    click_level(app, "Or")
    assert app.game.current.name == "Not"
    assert app.notice == "Or is locked: solve Not, And first."

    # Write Not and run the tests with Ctrl+Enter.
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=app.editor.rect.center, button=1))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=app.editor.rect.center, button=1))
    replace_all(app, NOT)
    keydown(app, pygame.K_RETURN, CTRL)
    report = app.game.report
    assert report is not None and report.passed, report
    assert report.lines == ["Unlocked: And"]
    assert app.session.snapshot is not None and len(app.session.snapshot.view.parts) == 1
    app.screenshot(shots / "2-not-solved.png")

    # The circuit still responds to clicks with the sidebar on the left.
    b = app.session.snapshot.layout.boxes[("in", "in")]
    click(app, app.screen_of((b.x + b.w / 2, b.y + b.h / 2)))
    assert app.session.inputs["in"] == 0 and app.session.sim is not None
    assert app.session.sim.get("out") == 1

    # Open And: a wrong first attempt, run from the button, lists the failing rows.
    click_level(app, "And")
    assert app.game.current.name == "And" and not app.show_errors
    replace_all(app, AND_WRONG)
    click(app, app.button_rect.center)
    report = app.game.report
    assert report is not None and not report.passed
    assert report.summary == "4 of 4 checks failed"
    assert report.lines[0].startswith("test line ") and "(inputs a=0 b=0)" in report.lines[0]
    app.screenshot(shots / "3-and-failing.png")

    # Fix it in place by typing: put the Nand's output on a wire, then add a Not.
    buf = app.editor.buffer
    line = next(i for i, t in enumerate(buf.lines) if "Nand" in t)
    buf.select_word_at(Pos(line, buf.lines[line].rindex("out") + 1))  # the last "out"
    type_text(app, "n")
    keydown(app, pygame.K_END)
    type_text(app, "\nNot(in=n, out=out);")
    assert buf.lines[line + 1] == "    Not(in=n, out=out);"  # auto-indented
    keydown(app, pygame.K_s, CTRL)  # save first: the circuit shows the fix
    assert app.session.error is None
    keydown(app, pygame.K_RETURN, CTRL)
    report = app.game.report
    assert report is not None and report.passed and report.lines == ["Unlocked: Or"]
    app.screenshot(shots / "4-and-solved.png")
    for name in ("1-fresh", "2-not-solved", "3-and-failing", "4-and-solved"):
        assert (shots / f"{name}.png").stat().st_size > 0

    # Quit and come back: progress and code are still there, and the game opens Or.
    again = new_app(save)
    assert again.game.store.solved == {"Not", "And"}
    assert again.game.current.name == "Or"
    click_level(again, "And")
    assert again.editor is not None and "Not(in=n, out=out);" in again.editor.buffer.text


def test_switching_levels_never_loses_unsaved_text(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    replace_all(app, NOT)
    keydown(app, pygame.K_RETURN, CTRL)
    type_text(app, "\n// a note")  # unsaved
    click_level(app, "And")
    click_level(app, "Not")
    assert app.editor is not None and app.editor.buffer.text.rstrip().endswith("// a note")


def test_errors_appear_after_first_save(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    replace_all(app, "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, c=in, out=out); }")
    assert not app.show_errors
    keydown(app, pygame.K_s, CTRL)
    assert app.show_errors
    assert app.editor is not None and app.editor.error is not None
    assert "Nand has no pin 'c'" in app.editor.error.message
