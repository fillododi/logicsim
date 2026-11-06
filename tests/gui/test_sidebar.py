"""The sidebar's level list: groups that open and close, driven headless."""

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


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def new_app(tmp_path: Path) -> GameApp:
    app = GameApp(SaveStore(load_levels(), tmp_path / "save"), size=(1440, 860))
    app.render(pygame.Surface(app.size))
    return app


def click(app: GameApp, pos: tuple[int, int]) -> None:
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))
    app.render(pygame.Surface(app.size))


def header(app: GameApp, group: str) -> pygame.Rect:
    return next(r for r, g in app._group_rows if g == group)


def shown(app: GameApp) -> list[str]:
    return [lv.name for _, lv in app._rows]


def test_a_new_game_shows_the_tutorial_and_the_gates(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    assert [g for _, g in app._group_rows] == ["00_tutorial", "01_gates", "02_buses"]
    # Buses stays folded: none of its levels is open before Not is solved.
    assert shown(app) == [lv.name for lv in load_levels() if lv.group != "02_buses"]


def test_a_header_click_closes_and_reopens_its_group(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    click(app, header(app, "01_gates").center)
    assert shown(app) == ["Wire", "Hello"]
    assert app.game.current.name == "Wire"  # a header is not a level
    click(app, header(app, "01_gates").center)
    assert "DMux" in shown(app)


def test_rows_below_a_closed_group_move_up(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    gates = header(app, "01_gates").y
    click(app, header(app, "00_tutorial").center)
    assert header(app, "01_gates").y < gates
    assert shown(app)[0] == "Not"


def test_opening_a_level_in_another_group_closes_the_old_one(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    click(app, next(r for r, lv in app._rows if lv.name == "Not").center)
    assert app.game.current.name == "Not"
    assert app.expanded == {"01_gates"}
    assert "Wire" not in shown(app)


def test_the_players_choice_lasts_until_the_group_changes(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    click(app, header(app, "00_tutorial").center)
    app.render(pygame.Surface(app.size))
    assert app.expanded == {"01_gates"}  # redrawing doesn't undo it


def test_a_level_in_a_closed_group_anchors_on_its_header(tmp_path: Path) -> None:
    app = new_app(tmp_path)
    hello = next(r for r, lv in app._rows if lv.name == "Hello")
    assert app.anchor_rect("level:Hello") == hello
    click(app, header(app, "00_tutorial").center)
    assert app.anchor_rect("level:Hello") == header(app, "00_tutorial")
    levels = app.anchor_rect("levels")
    assert levels is not None and levels.contains(header(app, "00_tutorial"))
