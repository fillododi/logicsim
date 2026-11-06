"""Typing a value for an input pin: the field's rules, then the canvas, driven headless."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.app import ViewerApp  # noqa: E402
from nandsim.gui.game_app import GameApp  # noqa: E402
from nandsim.gui.saves import SaveStore  # noqa: E402
from nandsim.gui.session import ChipSession, file_loader  # noqa: E402
from nandsim.gui.valuefield import ValueField  # noqa: E402
from nandsim.testing import load_levels  # noqa: E402

WIDE = "CHIP Wide { IN a[4], pc[12], en; OUT out[4], next[12], on; PARTS: "
WIDE += "out = a; next = pc; on = en; }"


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


# ---- the field on its own -----------------------------------------------------


def test_the_field_keeps_only_characters_a_value_can_have() -> None:
    f = ValueField("a", 4)
    f.type("0x1 F;z")
    assert f.text == "0x1F"
    f.backspace()
    assert f.text == "0x1"
    f.backspace(everything=True)
    assert f.empty


def test_the_field_reads_tst_values() -> None:
    f = ValueField("pc", 12)
    f.type("0xabc")
    assert f.value() == 0xABC and f.error == ""
    f = ValueField("a", 4)
    f.type("-1")
    assert f.value() == 0xF


def test_a_bad_value_explains_itself_until_the_player_types_again() -> None:
    f = ValueField("a", 4)
    f.type("16")
    assert f.value() is None
    assert f.error == f.hint == "16 does not fit in 4-bit pin 'a'"
    f.backspace()
    assert f.error == "" and f.hint.startswith("e.g.")


# ---- on the canvas ------------------------------------------------------------


def make_app(tmp_path: Path) -> ViewerApp:
    (tmp_path / "Wide.hdl").write_text(WIDE)
    s = ChipSession(file_loader(tmp_path / "Wide.hdl", [tmp_path]))
    assert s.reload()
    app = ViewerApp(s, size=(1100, 600))
    app.render(pygame.Surface(app.size))
    return app


def hover(app: ViewerApp, pin: str) -> None:
    assert app.session.snapshot is not None
    b = app.session.snapshot.layout.boxes[("in", pin)]
    pos = app.screen_of((b.x + b.w / 2, b.y + b.h / 2))
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))


def press(app: ViewerApp, key: int, char: str = "", mod: int = 0) -> None:
    """A key as pygame delivers it: KEYDOWN, then TEXTINPUT for a printable character."""
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode=char))
    if char:
        app.handle(pygame.event.Event(pygame.TEXTINPUT, text=char))


def type_text(app: ViewerApp, text: str) -> None:
    for c in text:
        press(app, pygame.key.key_code(c) if c.isalnum() else pygame.K_MINUS, c)


def test_typing_a_digit_over_a_bus_input_sets_its_value(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    hover(app, "pc")
    type_text(app, "0xABC")
    assert app.value_field is not None and app.value_field.text == "0xABC"
    assert app.hex_mode and app.session.inputs.get("a") is None  # "x" was typed, not a shortcut
    press(app, pygame.K_RETURN)
    assert app.value_field is None
    assert app.session.inputs["pc"] == 0xABC
    assert app.session.sim is not None and app.session.sim.get("next") == 0xABC


def test_enter_opens_an_empty_field_and_empty_enter_changes_nothing(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    hover(app, "a")
    press(app, pygame.K_RETURN)
    assert app.value_field is not None and app.value_field.pin == "a"
    press(app, pygame.K_RETURN)
    assert app.value_field is None and app.session.inputs.get("a") is None


def test_a_value_too_wide_keeps_the_field_open(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    hover(app, "a")
    type_text(app, "-9")
    press(app, pygame.K_RETURN)
    assert app.value_field is not None
    assert app.value_field.error == "-9 does not fit in 4-bit pin 'a'"
    app.render(pygame.Surface(app.size))  # draws the error without trouble
    press(app, pygame.K_BACKSPACE, mod=pygame.KMOD_CTRL)
    type_text(app, "-8")
    press(app, pygame.K_RETURN)
    assert app.session.inputs["a"] == 0b1000


def test_escape_or_a_click_cancels(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    hover(app, "en")
    type_text(app, "1")
    press(app, pygame.K_ESCAPE)
    assert app.value_field is None and app.session.inputs.get("en") is None
    assert app.session.path == "Wide"  # Esc closed the field; it didn't go up a level
    type_text(app, "1")
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(5, 5), button=1))
    assert app.value_field is None and app.session.inputs.get("en") is None


def test_keys_away_from_an_input_keep_their_shortcuts(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=(5, 5), rel=(0, 0), buttons=(0, 0, 0)))
    press(app, pygame.K_1, "1")
    assert app.value_field is None
    press(app, pygame.K_h, "h")
    assert not app.hex_mode


def test_in_the_game_esc_closes_the_field_before_the_menu(tmp_path: Path) -> None:
    levels = {lv.name: lv for lv in load_levels()}
    store = SaveStore(load_levels(), tmp_path / "save")
    store.save(levels["Not"], levels["Not"].reference.read_text())
    app = GameApp(store, size=(1440, 860))
    app.tour.skip()
    app.open_level(levels["Not"])
    assert app.editor is not None
    app.editor.focused = False  # keys go to the canvas, as after a click on it
    app.render(pygame.Surface(app.size))
    hover(app, "in")
    type_text(app, "1")
    press(app, pygame.K_ESCAPE)
    assert app.value_field is None and app.menus == []
    type_text(app, "1")
    press(app, pygame.K_RETURN)
    assert app.session.inputs["in"] == 1
    assert "toggle" in app.sounds.played  # a typed value sounds like a click on the pin
