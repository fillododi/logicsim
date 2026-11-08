"""Built-in DFF parts: marked on the canvas, and switchable back to the player's own DFF."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402
from pathlib import Path  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.app import BUILTIN_HELP, ViewerApp  # noqa: E402
from nandsim.gui.session import ChipSession, file_loader  # noqa: E402
from nandsim.netlist import ChipLibrary, Primitive  # noqa: E402

REF = Path(__file__).parents[2] / "reference"
BIT = """CHIP Bit { IN in, load; OUT out; PARTS:
    Mux(a=prev, b=in, sel=load, out=d);
    DFF(in=d, out=prev, out=out); }"""


@pytest.fixture(scope="module", autouse=True)
def display() -> Iterator[None]:
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


@pytest.fixture
def chips(tmp_path: Path) -> Path:
    """Bit beside the reference chips it needs, the DFF chain from NAND included."""
    for group, names in {
        "01_gates": ("Not", "And", "Or", "Mux"),
        "04_seq": ("SRLatch", "DLatch", "DFF"),
    }.items():
        for name in names:
            (tmp_path / f"{name}.hdl").write_text((REF / group / f"{name}.hdl").read_text())
    (tmp_path / "Bit.hdl").write_text(BIT)
    return tmp_path


def session(chips: Path, name: str = "Bit") -> ChipSession:
    s = ChipSession(file_loader(chips / f"{name}.hdl", [chips]))
    assert s.reload()
    return s


def dff_part(s: ChipSession):
    assert s.snapshot is not None
    return next(p for p in s.snapshot.view.parts if p.chip == "DFF")


# ---- the library -------------------------------------------------------------


def test_library_resolves_dff_parts_as_hdl_only_with_builtins_off(chips: Path) -> None:
    on = ChipLibrary([chips])
    assert isinstance(on.resolve("DFF"), Primitive) and on.is_builtin("DFF")
    off = ChipLibrary([chips], builtins=False)
    assert not isinstance(off.resolve("DFF"), Primitive) and not off.is_builtin("DFF")
    assert not on.is_builtin("Mux") and not on.is_builtin("Nand")


def test_without_hdl_a_dff_part_stays_built_in(tmp_path: Path) -> None:
    lib = ChipLibrary([tmp_path], builtins=False)
    assert isinstance(lib.resolve("DFF"), Primitive) and lib.is_builtin("DFF")


# ---- the session -------------------------------------------------------------


def test_dff_parts_are_marked_built_in(chips: Path) -> None:
    s = session(chips)
    p = dff_part(s)
    assert p.primitive and p.builtin and p.label == "DFF (built-in)"
    assert s.can_switch and s.builtins


def test_switching_to_your_dff_opens_its_latches_and_keeps_results(chips: Path) -> None:
    s = session(chips)
    assert s.toggle_builtins() is None and not s.builtins
    p = dff_part(s)
    assert not p.primitive and not p.builtin and p.label == "DFF"
    assert s.sim is not None and s.sim.dff_count == 0 and s.sim.reads_clock
    for v in (1, 0, 1):  # the player's DFF stores and holds like the built-in one
        s.set_input("in", v)
        s.set_input("load", 1)
        s.step()
        assert s.sim.get("out") == v
        s.set_input("in", 1 - v)
        s.set_input("load", 0)
        s.step()
        assert s.sim.get("out") == v
    s.goto(p.path)  # inside the DFF: its two latches, and inside those, the SR latch
    assert s.snapshot is not None
    assert [q.chip for q in s.snapshot.view.parts] == ["DLatch", "Not", "DLatch"]
    s.goto(f"{p.path}/DLatch#1")
    assert "SRLatch" in [q.chip for q in s.snapshot.view.parts]
    assert s.toggle_builtins() is None and s.builtins and dff_part(s).builtin


def test_a_broken_dff_keeps_the_built_in_one_without_rebuilding(chips: Path) -> None:
    (chips / "DFF.hdl").write_text("CHIP DFF { IN in; OUT out; PARTS: Nope(in=in, out=out); }")
    s = session(chips)
    sim = s.sim
    why = s.toggle_builtins()
    assert why == "Your DFF doesn't build, so DFF parts stay built-in: unknown chip 'Nope'"
    assert s.builtins and s.error is None and dff_part(s).builtin
    assert s.sim is sim  # the running circuit was never replaced


def test_a_chip_that_doesnt_build_is_refused_and_the_dff_not_blamed(chips: Path) -> None:
    s = session(chips)
    (chips / "Bit.hdl").write_text(BIT.replace("Mux(", "Muxx("))
    assert not s.reload() and s.error is not None  # the last good circuit stays
    why = s.toggle_builtins()
    assert why == "Fix the errors in your chip first: B switches only a chip that builds."
    assert s.builtins and s.error is not None  # the chip's own error is still shown


def test_without_your_dff_there_is_nothing_to_switch(tmp_path: Path) -> None:
    """A save from before the DFF level, or a folder without DFF.hdl: parts stay built-in."""
    (tmp_path / "Bit.hdl").write_text(
        "CHIP Bit { IN in, load; OUT out; PARTS: Nand(a=in, b=load, out=x); DFF(in=x, out=out); }"
    )
    s = ChipSession(file_loader(tmp_path / "Bit.hdl", [tmp_path]))
    assert s.reload() and not s.can_switch and dff_part(s).builtin
    assert s.toggle_builtins() == "There is no DFF of yours to switch to in this chip."
    assert s.builtins


def test_chips_without_a_dff_part_have_nothing_to_switch(chips: Path) -> None:
    assert not session(chips, "Mux").can_switch
    assert not session(chips, "DFF").can_switch  # the DFF level itself is always yours


def test_reg_of_bits_finds_the_dff_two_levels_down(chips: Path) -> None:
    (chips / "Reg2.hdl").write_text(
        "CHIP Reg2 { IN in[2], load; OUT out[2]; PARTS:"
        " Bit(in=in[0], load=load, out=out[0]); Bit(in=in[1], load=load, out=out[1]); }"
    )
    assert session(chips, "Reg2").can_switch


# ---- the app -------------------------------------------------------------------


def press(app: ViewerApp, k: int, mod: int = 0) -> None:
    app.handle(pygame.event.Event(pygame.KEYDOWN, key=k, mod=mod, unicode=""))


def test_b_switches_and_the_help_and_header_say_so(chips: Path) -> None:
    app = ViewerApp(session(chips), size=(1100, 600))
    app.render(pygame.Surface(app.size))
    assert BUILTIN_HELP in app.help_text
    press(app, pygame.K_b)
    assert not app.session.builtins
    assert app.notice == "DFF parts now run as your own DFF: click one to see its latches."
    app.render(pygame.Surface(app.size))  # the header note draws without trouble
    press(app, pygame.K_b, pygame.KMOD_CTRL)  # not with a modifier
    assert not app.session.builtins
    press(app, pygame.K_b)
    assert app.session.builtins
    assert app.notice == "DFF parts run as the built-in flip-flop again: faster, same results."


def test_the_viewer_draws_the_notice(chips: Path) -> None:
    app = ViewerApp(session(chips), size=(1100, 600))
    x, y, w, _ = app.canvas_area
    area = pygame.Rect(int(x), int(y), int(w), 40)  # under the header, where it goes
    before = pygame.Surface(app.size)
    app.render(before)
    press(app, pygame.K_b)
    press(app, pygame.K_b)  # back to the same circuit, so only the notice differs
    after = pygame.Surface(app.size)
    app.render(after)
    assert app.notice is not None
    assert pygame.image.tobytes(before.subsurface(area), "RGB") != pygame.image.tobytes(
        after.subsurface(area), "RGB"
    )


def test_hover_follows_the_new_layout_after_b(chips: Path) -> None:
    app = ViewerApp(session(chips), size=(1100, 600))
    app.render(pygame.Surface(app.size))
    snap = app.session.snapshot
    assert snap is not None
    i = next(p.index for p in snap.view.parts if p.chip == "DFF")
    b = snap.layout.boxes[("part", i)]
    app.mouse = app.screen_of((b.x + b.w / 2, b.y + b.h / 2))
    app.hover.node = ("part", 99)  # stale on purpose: B must recompute it
    press(app, pygame.K_b)
    new = app.session.snapshot
    assert new is not None and new is not snap
    assert app.hover.node == ("part", i)  # the mouse is over the new DFF box


def test_a_narrow_window_drops_the_header_note_rather_than_overlap(chips: Path) -> None:
    app = ViewerApp(session(chips), size=(700, 400))
    press(app, pygame.K_b)
    app.session.goto(f"Bit/DFF#{dff_part(app.session).index}/DLatch#1")
    app.render(pygame.Surface(app.size))  # the crumbs fill the header: no note, no crash
    assert app._crumbs  # the breadcrumbs are still there to click


def test_the_game_keeps_the_choice_from_level_to_level(tmp_path: Path) -> None:
    from nandsim.gui.game_app import GameApp
    from nandsim.gui.saves import SaveStore
    from nandsim.testing import load_levels

    levels = load_levels()
    by = {lv.name: lv for lv in levels}
    store = SaveStore(levels, tmp_path / "save")
    for lv in levels[: [x.name for x in levels].index("Register8")]:
        store.save(lv, lv.reference.read_text())  # tests may read the reference
        store.mark_solved(lv)
    app = GameApp(store, size=(1440, 860))
    app.tour.skip()
    app.open_level(by["Bit"])
    assert app.session.can_switch and app.session.builtins
    app.editor.focused = False
    press(app, pygame.K_b)
    assert not app.session.builtins and dff_part(app.session).label == "DFF"
    app.open_level(by["Register4"])
    assert not app.session.builtins and app.session.can_switch


def test_b_does_nothing_without_a_dff_part(chips: Path) -> None:
    app = ViewerApp(session(chips, "Mux"), size=(1100, 600))
    assert BUILTIN_HELP not in app.help_text
    press(app, pygame.K_b)
    assert app.session.builtins and app.notice is None
