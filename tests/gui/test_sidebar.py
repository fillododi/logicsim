"""The sidebar's level list: groups that open and close, driven headless."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.game_app import ROW_H, GameApp, clamp_scroll, scroll_into_view  # noqa: E402
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


# ---- a list taller than its room scrolls -------------------------------------------


def test_scroll_helpers() -> None:
    assert clamp_scroll(-5, 500, 200) == 0
    assert clamp_scroll(400, 500, 200) == 300
    assert clamp_scroll(50, 100, 200) == 0  # everything fits
    assert scroll_into_view(0, 260, 26, 200) == 86  # below: just enough to show it
    assert scroll_into_view(100, 52, 26, 200) == 52  # above: up to its top
    assert scroll_into_view(100, 150, 26, 200) == 100  # already shown


def at_and(tmp_path: Path) -> GameApp:
    """Gates under way: Not is solved, so Buses opens too, below And."""
    levels = {lv.name: lv for lv in load_levels()}
    store = SaveStore(load_levels(), tmp_path / "save")
    for name in ("Wire", "Hello", "Not"):
        store.save(levels[name], levels[name].reference.read_text())
        store.mark_solved(levels[name])
    app = GameApp(store, size=(1440, 860))
    app.tour.skip()
    app.open_level(levels["And"])
    app.render(pygame.Surface(app.size))
    return app


def wheel(app: GameApp, y: int) -> None:
    app.handle(pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=y))
    app.render(pygame.Surface(app.size))


def test_the_list_leaves_room_for_the_brief(tmp_path: Path) -> None:
    app = at_and(tmp_path)
    assert app.expanded == {"01_gates", "02_buses"}  # 3 headers and 19 levels
    assert not app.brief_cut  # And's brief, one of the longest, is drawn to its last line
    assert app.list_rect.height % ROW_H == 0 and app.list_rect.height >= 5 * ROW_H
    assert "And" in shown(app) and "DMux8Way" not in shown(app)


def test_a_tiny_window_keeps_five_rows_and_cuts_the_brief(tmp_path: Path) -> None:
    app = at_and(tmp_path)
    app.size = (1000, 420)
    app.render(pygame.Surface(app.size))
    assert app.list_rect.height == 5 * ROW_H and app.brief_cut
    assert "And" in shown(app)  # the current level stays in sight


def test_the_wheel_scrolls_the_list_and_stops_at_its_ends(tmp_path: Path) -> None:
    app = at_and(tmp_path)
    app.mouse = app.list_rect.center
    first = shown(app)
    wheel(app, -2)  # down two rows
    assert app.list_scroll == 2 * ROW_H and shown(app) != first
    wheel(app, -100)
    assert shown(app)[-1] == "DMux8Way"  # the last row, and no further
    wheel(app, 100)
    assert app.list_scroll == 0 and app._group_rows[0][1] == "00_tutorial"


def test_scrolled_out_rows_are_not_clickable(tmp_path: Path) -> None:
    app = at_and(tmp_path)
    app.mouse = app.list_rect.center
    wheel(app, -100)
    assert all(app.list_rect.contains(r) for r, _ in app._rows + app._group_rows)
    click(app, (app.list_rect.centerx, app.list_rect.bottom + 4))  # just below the list
    assert app.game.current.name == "And"


def test_the_wheel_elsewhere_still_zooms(tmp_path: Path) -> None:
    app = at_and(tmp_path)
    app.mouse = (round(app.canvas_area[0]) + 50, round(app.canvas_area[1]) + 50)
    scale = app.cam.scale
    wheel(app, 1)
    assert app.list_scroll == 0 and app.cam.scale != scale


def test_opening_a_level_scrolls_it_into_view(tmp_path: Path) -> None:
    levels = load_levels()
    store = SaveStore(levels, tmp_path / "save")
    for lv in levels:
        store.mark_solved(lv)
    app = GameApp(store, size=(1440, 860))
    app.tour.skip()
    app.open_level(next(lv for lv in levels if lv.name == "Not"))
    app.expanded |= {"02_buses"}  # the player opened Buses below Gates
    app.render(pygame.Surface(app.size))
    assert "DMux8Way" not in shown(app)
    app.open_level(next(lv for lv in levels if lv.name == "DMux8Way"))
    app.render(pygame.Surface(app.size))
    assert "DMux8Way" in shown(app)
