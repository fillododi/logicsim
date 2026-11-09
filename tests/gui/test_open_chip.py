"""Opening one of the player's exported chips from the sidebar, to read and change it."""

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
from nandsim.testing import load_levels  # noqa: E402

CTRL = pygame.KMOD_CTRL
BUF = "CHIP Buf {{ IN in; OUT out; PARTS: Nand(a=in, b=in, out=n); Nand(a=n, b=n, out=out); }}"
USER = "CHIP UsesBuf {{ IN in; OUT out; PARTS: {name}(in=in, out=out); }}"


@pytest.fixture(autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    yield
    pygame.quit()


def new_app(tmp_path: Path) -> GameApp:
    store = SaveStore(load_levels(), tmp_path / "save")
    store.export("Buf", BUF.format())
    store.export("Other", BUF.format().replace("CHIP Buf", "CHIP Other"))
    store.export("UsesBuf", USER.format(name="Buf"))
    app = GameApp(store, size=(1440, 860))
    app.render(pygame.Surface(app.size))
    return app


def draw(app: GameApp) -> None:
    app.render(pygame.Surface(app.size))


def click(app: GameApp, pos: tuple[int, int]) -> None:
    app.mouse = pos
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos))
    draw(app)


def chip_row(app: GameApp, name: str) -> pygame.Rect:
    return next(r for r, n in app._chip_open_rows if n == name)


def level_row(app: GameApp, name: str) -> pygame.Rect:
    return next(r for r, lv in app._rows if lv.name == name)


def keydown(app: GameApp, key: int, mod: int = 0) -> None:
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode=""))
    draw(app)


def test_a_click_on_a_chip_opens_it_in_the_editor(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    level = app.game.current
    click(app, chip_row(app, "Buf").center)
    assert app.game.chip == "Buf" and app.game.current is level  # the level stays current
    assert app.editor is not None and app.editor.buffer.text == BUF.format()
    assert app.edit_path == app.game.store.export_path("Buf")
    assert app.session.error is None and app.session.path == "Buf"
    assert app._brief_layout()[0][0] == "Buf"
    assert any("Used by UsesBuf" in line for line, *_ in app._brief_layout())


def test_the_x_still_deletes_rather_than_opens(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    x = next(r for r, n in app._chip_rows if n == "Buf")
    assert not chip_row(app, "Buf").colliderect(x)
    click(app, x.center)
    assert app.game.chip is None and app.menus and app.menus[-1].title == "Delete Buf?"


def test_ctrl_s_saves_the_chip_to_its_export_file(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    level_file = app.game.store.path(app.game.current)
    click(app, chip_row(app, "Buf").center)
    assert app.editor is not None
    new = "// edited\n" + BUF.format()
    app.editor.buffer.select_all()
    app.editor.buffer.insert(new)
    keydown(app, pygame.K_s, CTRL)
    assert app.game.store.export_path("Buf").read_text() == new
    assert not level_file.exists()  # the level's save is untouched
    assert app.session.error is None


def test_a_click_on_the_level_goes_back_to_it(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    level = app.game.current
    stub = app.editor.buffer.text if app.editor else ""
    click(app, chip_row(app, "Buf").center)
    click(app, level_row(app, level.name).center)
    assert app.game.chip is None and app.game.current is level
    assert app.editor is not None and app.editor.buffer.text == stub
    assert app.edit_path == app.game.store.path(level)


def test_unsaved_work_is_saved_to_where_it_belongs(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    assert app.editor is not None
    level = app.game.current
    app.editor.buffer.insert("// mine\n")
    click(app, chip_row(app, "Buf").center)
    assert "// mine" in app.game.store.path(level).read_text()  # the level's own file
    app.editor.buffer.insert("// in buf\n")
    click(app, chip_row(app, "Other").center)
    assert "// in buf" in app.game.store.export_path("Buf").read_text()
    assert "// in buf" not in app.game.store.path(level).read_text()


def test_run_tests_on_a_chip_saves_it_and_says_it_has_none(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    click(app, chip_row(app, "Buf").center)
    assert app.editor is not None
    app.editor.buffer.insert("// saved by the run\n")
    keydown(app, pygame.K_RETURN, CTRL)
    report = app.game.report
    assert report is not None and report.summary == "Buf has no tests"
    assert "// saved by the run" in app.game.store.export_path("Buf").read_text()
    assert app.game.current.name not in app.game.store.solved


def test_deleting_the_open_chip_goes_back_to_the_level(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    click(app, chip_row(app, "Buf").center)
    app.delete_chip("Buf")
    draw(app)
    assert app.game.chip is None and "Buf" not in app._exported
    assert app.edit_path == app.game.store.path(app.game.current)


def test_the_tour_waits_while_a_chip_is_open(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    assert app.bubble is not None  # the tour's welcome
    click(app, chip_row(app, "Buf").center)
    assert app.bubble is None
    seen = set(app.tour.seen)
    keydown(app, pygame.K_s, CTRL)  # a build here isn't the level's build
    assert app.tour.seen == seen
    click(app, level_row(app, app.game.current.name).center)
    assert app.bubble is not None
