"""Editor widget and editor+viewer tests, driven headless with real pygame events."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.app import ViewerApp  # noqa: E402
from nandsim.gui.editor import EditorWidget  # noqa: E402
from nandsim.gui.session import ChipSession, FileWatcher, file_loader  # noqa: E402
from nandsim.gui.textbuffer import Pos, TextBuffer  # noqa: E402
from nandsim.gui.theme import Fonts  # noqa: E402

REF = Path(__file__).parents[2] / "reference" / "01_gates"
CTRL = pygame.KMOD_CTRL


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def keydown(target: EditorWidget | ViewerApp, key: int, mod: int = 0) -> str | None:
    return target.handle(pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode=""))


def type_text(target: EditorWidget | ViewerApp, text: str) -> None:
    for ch in text:
        if ch == "\n":
            keydown(target, pygame.K_RETURN)
        else:
            target.handle(pygame.event.Event(pygame.TEXTINPUT, text=ch))


def widget(text: str = "") -> EditorWidget:
    return EditorWidget(TextBuffer(text), Fonts(), pygame.Rect(0, 0, 500, 300))


def test_typing_keys_and_shortcuts() -> None:
    ed = widget()
    type_text(ed, "CHIP X {\nIN a;\n}")
    assert ed.buffer.text == "CHIP X {\n    IN a;\n}"
    keydown(ed, pygame.K_z, CTRL)
    assert ed.buffer.text != "CHIP X {\n    IN a;\n}"
    keydown(ed, pygame.K_y, CTRL)
    keydown(ed, pygame.K_a, CTRL)
    keydown(ed, pygame.K_SLASH, CTRL)
    assert ed.buffer.lines[0].startswith("// CHIP")
    assert keydown(ed, pygame.K_s, CTRL) == "save"


def test_copy_paste_round_trip() -> None:
    ed = widget("Nand(a=a, b=b, out=out);")
    ed.buffer.select_word_at(Pos(0, 1))
    keydown(ed, pygame.K_c, CTRL)
    keydown(ed, pygame.K_END)
    keydown(ed, pygame.K_v, CTRL)
    assert ed.buffer.text.endswith(";Nand")


def test_mouse_click_places_cursor_and_drag_selects() -> None:
    ed = widget("abcdef\nghijkl")
    x, y = ed.screen_of(Pos(1, 2))
    ed.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(x, y + 2), button=1))
    assert ed.buffer.cursor == Pos(1, 2)
    x2, y2 = ed.screen_of(Pos(1, 5))
    ed.handle(
        pygame.event.Event(pygame.MOUSEMOTION, pos=(x2, y2 + 2), rel=(0, 0), buttons=(1, 0, 0))
    )
    ed.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(x2, y2 + 2), button=1))
    assert ed.buffer.selected_text() == "ijk"


def test_scrolls_to_keep_cursor_visible() -> None:
    ed = widget("\n".join(f"line {i}" for i in range(200)))
    keydown(ed, pygame.K_END, CTRL)
    assert ed.scroll_line > 150
    keydown(ed, pygame.K_HOME, CTRL)
    assert ed.scroll_line == 0


def test_render_with_selection_and_error() -> None:
    from nandsim.gui.editor import EditorError

    ed = widget("CHIP X { IN a; OUT o; PARTS: Nand(a=a, c=a, out=o); }")
    ed.buffer.select_word_at(Pos(0, 1))
    ed.set_error(EditorError(Pos(0, 40), "Nand has no pin 'c'"))
    surf = pygame.Surface((500, 300))
    ed.render(surf)  # must not raise


# ---- editor inside the viewer ----------------------------------------------


@pytest.fixture
def work(tmp_path: Path) -> Path:
    for name in ("Not", "And", "Or"):
        (tmp_path / f"{name}.hdl").write_text((REF / f"{name}.hdl").read_text())
    (tmp_path / "Mux.hdl").write_text(
        "CHIP Mux {\n    IN a, b, sel;\n    OUT out;\n    PARTS:\n}\n"
    )
    return tmp_path


def make_app(work: Path) -> ViewerApp:
    path = work / "Mux.hdl"
    s = ChipSession(file_loader(path, [work]))
    s.reload()
    return ViewerApp(s, size=(1200, 700), watcher=FileWatcher([work]), edit_path=path)


def test_write_a_chip_in_the_editor(work: Path, tmp_path: Path) -> None:
    app = make_app(work)
    ed = app.editor
    assert ed is not None and ed.focused
    # The empty stub doesn't compile: the error points into the file being edited.
    assert app.session.error is not None and ed.error is not None
    assert ed.error.pos == Pos(2, 8)  # "out" on line 3
    ed.buffer.set_cursor(Pos(3, 10))  # end of "    PARTS:"
    type_text(app, "\nNot(in=sel, out=ns);\nAnd(a=a, b=ns, out=x);\nAnd(a=b, b=sel, ou=y);")
    type_text(app, "\nOr(a=x, b=y, out=out);")
    assert ed.buffer.dirty
    keydown(app, pygame.K_s, CTRL)
    assert not ed.buffer.dirty
    assert ed.error is not None and "And has no pin 'ou'" in ed.error.message
    assert ed.error.pos.line == 6
    app.screenshot(tmp_path / "editor-error.png")
    # Fix the typo with the keyboard: go to the word, select it, retype.
    ed.buffer.select_word_at(ed.error.pos)
    type_text(app, "out")
    keydown(app, pygame.K_s, CTRL)
    assert ed.error is None and app.session.error is None
    assert app.session.snapshot is not None and len(app.session.snapshot.view.parts) == 4
    for pin, v in (("a", 1), ("b", 0), ("sel", 0)):
        app.session.set_input(pin, v)
    assert app.session.sim is not None and app.session.sim.get("out") == 1
    assert (work / "Mux.hdl").read_text() == ed.buffer.text


def test_canvas_keys_only_when_editor_unfocused(work: Path) -> None:
    app = make_app(work)
    assert app.editing
    type_text(app, "h")  # typed into the editor, not the hex toggle
    assert app.hex_mode and app.editor is not None and "h" in app.editor.buffer.text
    keydown(app, pygame.K_ESCAPE)  # leave the editor
    assert not app.editing
    keydown(app, pygame.K_h)
    assert not app.hex_mode


def test_external_change_reloads_clean_buffer_only(work: Path) -> None:
    app = make_app(work)
    assert app.editor is not None
    (work / "Mux.hdl").write_text((REF / "Mux.hdl").read_text())
    os.utime(work / "Mux.hdl", ns=(1, 1))
    app.tick(now=1000.0)
    assert app.editor.buffer.text == (REF / "Mux.hdl").read_text()
    assert app.session.error is None
    type_text(app, "X")  # now dirty: a second external change must not clobber it
    (work / "Mux.hdl").write_text("garbage")
    os.utime(work / "Mux.hdl", ns=(2, 2))
    app.tick(now=1001.0)
    assert app.editor.buffer.text.startswith("X") or "X" in app.editor.buffer.text


# ---- horizontal scrolling --------------------------------------------------------

LONG = "short\n" + "x" * 200 + "\nend" + "\n" * 60


def press(ed: EditorWidget, pos: tuple[int, int]) -> None:
    ed.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))


def test_no_scrollbar_when_every_line_fits() -> None:
    ed = widget("CHIP A { }")
    assert ed.hbar() is None and ed.max_scroll_x == 0
    ed.scroll_cols(10)
    assert ed.scroll_x == 0


def test_sideways_wheel_and_shift_wheel_scroll_within_the_longest_line() -> None:
    ed = widget(LONG)
    ed.wheel(1, 0)  # a trackpad's sideways swipe
    assert ed.scroll_x == 6 * ed.char_w
    pygame.key.set_mods(pygame.KMOD_SHIFT)
    try:
        ed.wheel(0, -1)  # Shift + wheel down: further right
        assert ed.scroll_x == 12 * ed.char_w
        ed.wheel(0, 1)
        assert ed.scroll_x == 6 * ed.char_w and ed.scroll_line == 0
    finally:
        pygame.key.set_mods(0)
    ed.scroll_cols(10_000)
    assert ed.scroll_x == ed.max_scroll_x  # the end of the longest line, not beyond
    ed.wheel(0, -1)  # without Shift the wheel still scrolls lines
    assert ed.scroll_x == ed.max_scroll_x and ed.scroll_line == 3


def test_the_scrollbar_drags_and_jumps() -> None:
    ed = widget(LONG)
    bar = ed.hbar()
    assert bar is not None
    track, thumb = bar
    assert track.bottom == ed.rect.bottom and thumb.x == track.x
    assert ed.visible_lines == (300 - 8) // ed.line_h  # the bar takes its strip
    press(ed, thumb.center)
    ed.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=(track.right + 50, thumb.centery)))
    assert ed.scroll_x == ed.max_scroll_x  # dragged past the end: clamped
    ed.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(track.right, 0)))
    assert not ed.dragging
    cursor = ed.buffer.cursor
    press(ed, (track.x + 2, track.centery))  # on the track, at its left end
    assert ed.scroll_x == 0 and ed.buffer.cursor == cursor  # not a click in the text
    ed.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(track.x, 0)))


def test_the_view_comes_back_when_the_long_line_goes() -> None:
    ed = widget(LONG)
    ed.scroll_cols(10_000)
    ed.buffer.set_text("short")
    ed.render(pygame.Surface((500, 300)))
    assert ed.scroll_x == 0 and ed.hbar() is None


def test_the_app_routes_the_wheel_and_the_bar_drag(tmp_path: Path) -> None:
    hdl = tmp_path / "Wide.hdl"
    hdl.write_text("// " + "wide " * 80 + "\n" + (REF / "Not.hdl").read_text().split("\n", 1)[1])
    s = ChipSession(file_loader(hdl))
    s.reload()
    app = ViewerApp(s, size=(1000, 700), edit_path=hdl)
    assert app.editor is not None
    ed = app.editor
    app.mouse = ed.rect.center
    app.handle(pygame.event.Event(pygame.MOUSEWHEEL, x=2, y=0))
    assert ed.scroll_x == 12 * ed.char_w
    bar = ed.hbar()
    assert bar is not None
    track, thumb = bar
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=thumb.center))
    drag = {"pos": (track.right, thumb.centery), "rel": (1, 0), "buttons": (1, 0, 0)}
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, drag))
    assert ed.scroll_x == ed.max_scroll_x  # the drag stayed with the editor, not the canvas
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(track.right, thumb.centery)))
    assert not ed.dragging
