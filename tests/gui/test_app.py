"""Viewer tests, driven headless with real pygame events as a player would produce them."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.app import FOOTER, HEADER, HELP_PAD, HELP_SIZE, SEP, ViewerApp, wrap_items  # noqa: E402
from nandsim.gui.session import ChipSession, FileWatcher, file_loader  # noqa: E402

REF = Path(__file__).parents[2] / "reference" / "01_gates"


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


@pytest.fixture
def chips(tmp_path: Path) -> Path:
    for name in ("Not", "And", "Or", "Mux"):
        (tmp_path / f"{name}.hdl").write_text((REF / f"{name}.hdl").read_text())
    return tmp_path


def make_app(chips: Path) -> ViewerApp:
    s = ChipSession(file_loader(chips / "Mux.hdl", [chips]))
    assert s.reload()
    return ViewerApp(s, size=(1100, 600), watcher=FileWatcher([chips]))


def click(app: ViewerApp, pos: tuple[int, int], button: int = 1) -> None:
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button))


def center_of(app: ViewerApp, key: tuple) -> tuple[int, int]:
    assert app.session.snapshot is not None
    b = app.session.snapshot.layout.boxes[key]
    return app.screen_of((b.x + b.w / 2, b.y + b.h / 2))


def key(app: ViewerApp, k: int) -> None:
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode=""))


def test_click_inputs_drives_simulation(chips: Path) -> None:
    app = make_app(chips)
    for pin in ("a", "b", "sel"):
        click(app, center_of(app, ("in", pin)))
    assert app.session.inputs == {"a": 0, "b": 0, "sel": 0}
    click(app, center_of(app, ("in", "b")))
    click(app, center_of(app, ("in", "sel")))
    assert app.session.sim is not None and app.session.sim.get("out") == 1
    click(app, center_of(app, ("in", "b")), button=3)  # right-click counts down: 1 -> 0
    assert app.session.sim.get("out") == 0
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=center_of(app, ("in", "a")),
                                  rel=(0, 0), buttons=(0, 0, 0)))  # fmt: skip
    key(app, pygame.K_x)
    assert app.session.inputs["a"] is None


def test_open_part_breadcrumb_and_back(chips: Path) -> None:
    app = make_app(chips)
    click(app, center_of(app, ("part", 4)))
    assert app.session.path == "Mux/Or#4"
    click(app, center_of(app, ("in", "a")))  # inner inputs are driven by the parent
    assert app.session.inputs.get("a") is None
    surf = pygame.Surface(app.size)
    app.render(surf)  # lays out the breadcrumbs
    crumb_rect = app._crumbs[0][0]
    click(app, crumb_rect.center)
    assert app.session.path == "Mux"
    click(app, center_of(app, ("part", 4)))
    key(app, pygame.K_BACKSPACE)
    assert app.session.path == "Mux"


def test_zoom_pan_fit_and_hex_toggle(chips: Path) -> None:
    app = make_app(chips)
    scale = app.cam.scale
    app.handle(pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=2, flipped=False))
    assert app.cam.scale > scale
    ox = app.cam.ox
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(500, HEADER + 5), button=1))
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=(560, HEADER + 5), rel=(60, 0),
                                  buttons=(1, 0, 0)))  # fmt: skip
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(560, HEADER + 5), button=1))
    assert app.cam.ox == ox + 60
    key(app, pygame.K_f)
    assert app.cam.scale == pytest.approx(scale)
    assert app.hex_mode
    key(app, pygame.K_h)
    assert not app.hex_mode


def test_hot_reload_shows_error_then_recovers(chips: Path, tmp_path: Path) -> None:
    app = make_app(chips)
    good = (chips / "Mux.hdl").read_text()
    (chips / "Mux.hdl").write_text(good.replace("Or(a=x, b=y, out=out);", "Or(a=x, out=out);"))
    os.utime(chips / "Mux.hdl", ns=(1, 1))
    app.tick(now=1000.0)
    assert app.session.error is not None
    assert "input pin 'b' of Or is not connected" in str(app.session.error)
    app.screenshot(tmp_path / "error.png")  # renders the banner without crashing
    assert (tmp_path / "error.png").stat().st_size > 0
    (chips / "Mux.hdl").write_text(good)
    os.utime(chips / "Mux.hdl", ns=(2, 2))
    app.tick(now=1001.0)
    assert app.session.error is None


def test_screenshot_of_every_level(tmp_path: Path) -> None:
    for name in ("Not", "And", "Or", "Xor", "Mux", "DMux"):
        s = ChipSession(file_loader(REF / f"{name}.hdl"))
        assert s.reload(), s.error
        app = ViewerApp(s, size=(900, 500))
        app.screenshot(tmp_path / f"{name}.png")
        assert (tmp_path / f"{name}.png").stat().st_size > 0


def test_wrap_items_breaks_between_items_first() -> None:
    def fits(s: str) -> bool:
        return len(s) <= 12

    assert wrap_items(["ab", "cd", "efg hij klm nop", "longerthan12", "r"], fits) == [
        f"ab{SEP}cd",
        "efg hij klm",  # an item too long for a line wraps between its words
        "nop",
        "longerthan12",  # a word too long for any line is kept whole rather than cut
        "r",
    ]
    assert wrap_items(["ab", "cd"], lambda s: True) == [f"ab{SEP}cd"]


def _words(s: str) -> list[str]:
    return [w for w in s.split() if w != "·"]


@pytest.mark.parametrize("width", [1280, 900, 640, 420])
def test_help_line_fits_the_window(chips: Path, width: int) -> None:
    app = make_app(chips)
    app.size = (width, 600)
    font = app.fonts.get(HELP_SIZE)
    lines = app.help_lines()
    assert _words(" ".join(lines)) == _words(app.help_text)  # nothing lost
    assert all(font.size(line)[0] <= width - 2 * HELP_PAD for line in lines)
    assert app.footer_height >= len(lines) * font.get_linesize()
    assert app.canvas_area[3] == 600 - HEADER - app.footer_height
    if width >= 1280:
        assert len(lines) == 1 and app.footer_height == FOOTER
    else:
        assert len(lines) > 1
    app.render(pygame.Surface(app.size))
