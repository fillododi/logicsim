"""Playtest of the guided tour: a new player follows every bubble with real events.

Checks that each step completes on the action it explains, that bubbles never
cover what they point at, and that skip, F1 replay and restarts behave.
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
from nandsim.gui.guide import Bubble  # noqa: E402
from nandsim.gui.saves import SaveStore  # noqa: E402
from nandsim.gui.textbuffer import Pos  # noqa: E402
from nandsim.testing import load_levels  # noqa: E402

CTRL = pygame.KMOD_CTRL
NOT = "CHIP Not {\n    IN in;\n    OUT out;\n    PARTS:\n    Nand(a=in, b=in, out=out);\n}\n"
AND = (
    "CHIP And {\n    IN a, b;\n    OUT out;\n    PARTS:\n"
    "    Nand(a=a, b=b, out=n);\n    Not(in=n, out=out);\n}\n"
)


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


def click(app: GameApp, pos: tuple[int, int]) -> None:
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))


def step_id(app: GameApp) -> str | None:
    step = app.tour.current
    return step.id if step else None


def shown(app: GameApp) -> Bubble | None:
    """Render a frame and return the bubble on screen, checking it leaves its anchor visible."""
    app.render(pygame.Surface(app.size))
    step = app.tour.visible(app.game.current.name)
    if step is None:
        assert app.bubble is None
        return None
    b = app.bubble
    assert b is not None
    anchor = app.anchor_rect(step.anchor)
    assert anchor is not None, step.anchor
    if anchor.width * anchor.height < app.size[0] * app.size[1] // 4:  # small enough to dodge
        assert not b.rect.colliderect(anchor), f"bubble covers its anchor in step {step.id}"
    w, h = app.size
    assert b.rect.left >= 0 and b.rect.top >= 0 and b.rect.right <= w and b.rect.bottom <= h
    return b


def press_next(app: GameApp) -> None:
    b = shown(app)
    assert b is not None and b.next is not None
    click(app, b.next.center)


def click_level(app: GameApp, name: str) -> None:
    """Click a level in the sidebar, first opening its group if it's closed, as a player would."""
    app.render(pygame.Surface(app.size))
    if all(lv.name != name for _, lv in app._rows):
        group = next(lv.group for lv in app.game.levels if lv.name == name)
        click(app, next(r for r, g in app._group_rows if g == group).center)
        app.render(pygame.Surface(app.size))
    click(app, next(r for r, lv in app._rows if lv.name == name).center)


def new_app(save: Path) -> GameApp:
    return GameApp(SaveStore(load_levels(), save), size=(1440, 860))


def test_new_player_follows_the_tour(tmp_path: Path) -> None:
    save = tmp_path / "save"
    shots = tmp_path / "shots"
    shots.mkdir()
    app = new_app(save)
    assert app.game.current.name == "Wire" and step_id(app) == "welcome"
    app.screenshot(shots / "1-welcome.png")
    press_next(app)
    assert step_id(app) == "brief"
    press_next(app)

    # Wire, "connect": click at the end of PARTS:, type the connection, Ctrl+S.
    assert step_id(app) == "connect"
    b = shown(app)
    assert b is not None and b.next is None  # completed by doing it, not by a button
    anchor = app.anchor_rect("line:PARTS:")
    assert app.editor is not None and anchor is not None and app.editor.rect.contains(anchor)
    assert b.rect.right <= app.editor.rect.x  # never over the text being typed
    app.screenshot(shots / "2-connect.png")
    click(app, (app.editor.rect.right - 20, anchor.centery))  # past the end of the line
    assert app.editor.buffer.cursor == Pos(5, len("    PARTS:"))
    type_text(app, "\nout = in;")
    keydown(app, pygame.K_s, CTRL)
    assert app.session.error is None and step_id(app) == "circuit"
    press_next(app)

    # "toggle": click the input; the output follows it.
    assert step_id(app) == "toggle"
    shown(app)
    pin = app.anchor_rect("pin:in")
    assert pin is not None
    click(app, pin.center)
    assert app.session.inputs["in"] == 0 and step_id(app) == "run"  # undefined → 0 first
    click(app, pin.center)
    assert app.session.sim is not None and app.session.sim.get("out") == 1
    app.screenshot(shots / "3-wire.png")

    # "run": the Run tests button solves Wire; then open Hello from the list.
    shown(app)
    click(app, app.button_rect.center)
    assert app.game.report is not None and app.game.report.passed
    assert step_id(app) == "to_hello"
    shown(app)
    click_level(app, "Hello")
    assert app.game.current.name == "Hello" and step_id(app) == "nand"
    press_next(app)

    # Hello, "write": the first part, typed under PARTS: the same way.
    assert step_id(app) == "write"
    b = shown(app)
    anchor = app.anchor_rect("line:PARTS:")
    assert b is not None and anchor is not None and b.rect.right <= app.editor.rect.x
    click(app, (app.editor.rect.right - 20, anchor.centery))
    type_text(app, "\nNand(a=a, b=b, out=out);")
    keydown(app, pygame.K_s, CTRL)
    assert app.session.error is None and step_id(app) == "output"
    app.screenshot(shots / "4-nand.png")
    press_next(app)

    # Hello, "type_value": click an empty spot of the circuit, point at b, type 1, Enter.
    assert step_id(app) == "type_value"
    b = shown(app)
    assert b is not None and b.next is None
    canvas = pygame.Rect(*(round(v) for v in app.canvas_area))
    spot = (canvas.x + 10, canvas.bottom - 10)
    assert not b.rect.collidepoint(spot)
    click(app, spot)
    assert not app.editor.focused
    pin_b = app.anchor_rect("pin:b")
    assert pin_b is not None
    app.handle(pygame.event.Event(pygame.MOUSEMOTION, pos=pin_b.center, rel=(0, 0),
                                  buttons=(0, 0, 0)))  # fmt: skip
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1, mod=0, unicode="1"))
    app.handle(pygame.event.Event(pygame.TEXTINPUT, text="1"))
    b = shown(app)
    assert b is not None and app.field_rect is not None
    assert not b.rect.colliderect(app.field_rect)  # the value being typed stays readable
    app.screenshot(shots / "4b-type-value.png")
    keydown(app, pygame.K_RETURN)
    assert app.session.inputs["b"] == 1 and step_id(app) == "run_hello"
    assert "toggle" in app.sounds.played

    # The keys now go to the circuit, so the tests run from the button.
    shown(app)
    click(app, app.button_rect.center)
    assert step_id(app) == "unlocked"
    shown(app)
    click_level(app, "Not")
    assert app.game.current.name == "Not" and step_id(app) == "on_your_own"
    press_next(app)
    assert step_id(app) == "replay"
    press_next(app)

    # "wires" waits for And: nothing shows in Not.
    assert step_id(app) == "wires" and shown(app) is None
    app.editor.clipboard.put(NOT)
    keydown(app, pygame.K_a, CTRL)
    keydown(app, pygame.K_v, CTRL)
    keydown(app, pygame.K_RETURN, CTRL)
    click_level(app, "And")
    assert app.game.current.name == "And" and step_id(app) == "wires"
    b = shown(app)
    assert b is not None and app.anchor_rect("line:PARTS:") != app.editor_rect
    app.screenshot(shots / "5-wires.png")
    app.editor.clipboard.put(AND)
    keydown(app, pygame.K_a, CTRL)
    keydown(app, pygame.K_v, CTRL)
    keydown(app, pygame.K_s, CTRL)
    assert step_id(app) == "see_wire"
    shown(app)
    wire = app._wire_rect()
    canvas = pygame.Rect(*(round(v) for v in app.canvas_area))
    assert wire is not None and canvas.contains(wire) and app.anchor_rect("wire") == wire
    app.screenshot(shots / "6-see-wire.png")
    press_next(app)
    assert step_id(app) == "open_part"
    shown(app)
    part = app.anchor_rect("part")
    assert part is not None
    app.screenshot(shots / "7-open-part.png")
    click(app, part.center)  # the Not part, not the Nand
    assert app.session.path == "And/Not#2" and step_id(app) == "back_up"
    shown(app)
    keydown(app, pygame.K_BACKSPACE)  # the canvas click took focus off the editor
    assert app.session.path == "And" and step_id(app) == "export"

    # "export": Esc, Export this chip as…, keep the suggested name, Enter.
    shown(app)
    keydown(app, pygame.K_ESCAPE)
    app.render(pygame.Surface(app.size))
    menu = app.menus[-1]
    item = next(i for i, it in enumerate(menu.items) if it.label == "Export this chip as…")
    click(app, menu.rects[item].center)
    assert app.menus[-1].text == "MyAnd"
    keydown(app, pygame.K_RETURN)
    assert app.menus == [] and (save.parent / "save-exports" / "MyAnd.hdl").is_file()
    assert step_id(app) == "your_chips"
    b = shown(app)  # pointing at the new "Your chips" list
    assert b is not None and app.anchor_rect("chips") is not None
    app.screenshot(shots / "8-your-chips.png")
    press_next(app)
    assert step_id(app) == "done"
    press_next(app)
    # The tour's last steps wait for SRLatch, the first level with memory.
    assert step_id(app) == "memory" and shown(app) is None
    for p in shots.iterdir():
        assert p.stat().st_size > 0

    # Restarting remembers how far the tour got; F1 replays it from the first tutorial level.
    again = new_app(save)
    assert step_id(again) == "memory"
    keydown(again, pygame.K_F1)
    assert again.game.current.name == "Wire" and step_id(again) == "welcome"


def test_skip_hides_the_tour_for_good(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    b = shown(app)
    assert b is not None
    click(app, b.skip.center)
    assert app.tour.current is None and shown(app) is None
    assert new_app(tmp_path / "save").tour.current is None


def test_bubble_swallows_clicks(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    b = shown(app)
    assert b is not None
    focused = app.editor is not None and app.editor.focused
    click(app, (b.rect.x + 5, b.rect.bottom - 5))  # on the bubble, off its buttons
    assert step_id(app) == "welcome"
    assert app.editor is not None and app.editor.focused == focused


def test_f1_works_while_typing(tmp_path: Path) -> None:
    app = new_app(tmp_path / "save")
    press_next(app)
    assert app.editor is not None and app.editor.focused
    keydown(app, pygame.K_F1)
    assert step_id(app) == "welcome"


def bubble_id(app: GameApp) -> str | None:
    step = app.tour.visible(app.game.current.name)
    return step.id if step else None


def paste(app: GameApp, text: str) -> None:
    assert app.editor is not None
    app.editor.clipboard.put(text)
    keydown(app, pygame.K_a, CTRL)
    keydown(app, pygame.K_v, CTRL)


def test_leaving_the_tutorial_early_keeps_the_tour_going(tmp_path: Path) -> None:
    # Review finding: opening Not mid-tutorial used to hide every later bubble.
    app = new_app(tmp_path / "save")
    click_level(app, "Not")
    assert bubble_id(app) == "on_your_own" and shown(app) is not None
    click_level(app, "Wire")
    assert bubble_id(app) == "welcome"  # the tutorial picks up where it was left


def test_solving_before_the_run_bubble_still_counts(tmp_path: Path) -> None:
    # Review finding: a Ctrl+Enter solve during the "circuit" bubble was lost.
    app = new_app(tmp_path / "save")
    press_next(app)
    press_next(app)
    paste(app, "CHIP Wire {\n    IN in;\n    OUT out;\n    PARTS:\n    out = in;\n}\n")
    keydown(app, pygame.K_RETURN, CTRL)  # builds and solves at once
    assert bubble_id(app) == "circuit"
    press_next(app)
    pin = app.anchor_rect("pin:in")
    assert pin is not None
    click(app, pin.center)  # "toggle"; "run" is already done, so the next bubble is "to_hello"
    assert bubble_id(app) == "to_hello"


def test_a_drag_ending_on_the_bubble_still_ends(tmp_path: Path) -> None:
    # Review finding: the bubble swallowed the release of an editor text selection.
    app = new_app(tmp_path / "save")
    b = shown(app)
    assert b is not None and app.editor is not None
    start = app.editor.rect.center
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start, button=1))
    for pos in (b.rect.center, (b.rect.x + 4, b.rect.y + 4)):
        motion = pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(1, 0, 0))
        app.handle(motion)
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=b.rect.center, button=1))
    assert not app.editor._dragging
    # A press that starts on the bubble keeps its release to itself.
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=b.rect.center, button=1))
    assert app._bubble_press
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=app.editor.rect.center, button=1))
    assert not app._bubble_press and not app.editor._dragging


def test_wheel_and_hover_over_the_bubble_leave_the_canvas_alone(tmp_path: Path) -> None:
    # Review findings: the wheel zoomed the circuit under the bubble, and a hover stayed on.
    from nandsim.gui.canvas import Hover

    app = new_app(tmp_path / "save")
    b = shown(app)
    assert b is not None
    app.hover = Hover(("in", "a"), None)
    app.handle(
        pygame.event.Event(pygame.MOUSEMOTION, pos=b.rect.center, rel=(0, 0), buttons=(0, 0, 0))
    )
    assert app.hover == Hover()
    scale = app.cam.scale
    app.handle(pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=1))
    assert app.cam.scale == scale


def test_both_unreadable_files_are_reported(tmp_path: Path) -> None:
    # Review finding: a progress warning used to hide the tutorial warning.
    save = tmp_path / "save"
    save.mkdir()
    (save / "progress.json").write_text("{bad")
    (save / "tutorial.json").write_text("{bad")
    app = new_app(save)
    assert app.notice is not None
    assert "progress.json.bad" in app.notice and "tutorial.json.bad" in app.notice


def test_memory_levels_introduce_loops_and_the_clock(tmp_path: Path) -> None:
    """SRLatch asks for a first chip with memory; DFF for a chip with the clock, then a step."""
    levels = load_levels()
    by_name = {lv.name: lv for lv in levels}
    store = SaveStore(levels, tmp_path / "save")
    for lv in levels[: [x.name for x in levels].index("SRLatch")]:
        store.save(lv, lv.reference.read_text())
        store.mark_solved(lv)
    app = GameApp(store, size=(1440, 860))
    memory = {"memory", "flipflop", "clock"}
    app.tour.seen.update(s.id for s in app.tour.steps if s.id not in memory)

    def build(name: str) -> None:
        assert app.editor is not None
        app.editor.buffer.select_all()
        app.editor.buffer.insert(by_name[name].reference.read_text())
        keydown(app, pygame.K_s, CTRL)
        assert app.session.error is None

    app.open_level(by_name["SRLatch"])
    assert step_id(app) == "memory" and shown(app) is not None
    build("SRLatch")
    assert step_id(app) == "flipflop" and shown(app) is None  # waits for the DFF level
    for name in ("SRLatch", "DLatch"):
        store.save(by_name[name], by_name[name].reference.read_text())
        store.mark_solved(by_name[name])
    app.open_level(by_name["DFF"])
    assert step_id(app) == "flipflop" and shown(app) is not None
    assert app.anchor_rect("clock") is None  # the stub doesn't read the clock yet
    build("DFF")
    assert step_id(app) == "clock"
    b = shown(app)  # beside the clock panel, not over it
    assert b is not None and app.anchor_rect("clock") is not None
    app.clock("step")
    assert app.tour.current is None and shown(app) is None
