"""Session and camera tests: inputs, navigation, reload keeping the last good circuit."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from nandsim.gui.camera import Camera, box_at, route_at
from nandsim.gui.session import ChipSession, FileWatcher, file_loader

REF = Path(__file__).parents[2] / "reference"


@pytest.fixture
def mux(tmp_path: Path) -> tuple[ChipSession, Path]:
    d = tmp_path / "chips"
    d.mkdir()
    for name in ("Not", "And", "Or", "Mux"):
        (d / f"{name}.hdl").write_text((REF / "01_gates" / f"{name}.hdl").read_text())
    s = ChipSession(file_loader(d / "Mux.hdl"))
    assert s.reload()
    return s, d


def out(s: ChipSession) -> int | None:
    assert s.sim is not None
    return s.sim.get("out")


def test_inputs_start_undefined_and_toggle(mux: tuple[ChipSession, Path]) -> None:
    s, _ = mux
    assert out(s) is None
    s.toggle("a")  # undefined -> 0
    s.toggle("b")
    s.toggle("sel")
    assert s.inputs == {"a": 0, "b": 0, "sel": 0} and out(s) == 0
    s.toggle("a")  # 0 -> 1
    assert out(s) == 1


def test_mux_is_defined_when_unselected_input_is_undefined(mux: tuple[ChipSession, Path]) -> None:
    s, _ = mux
    s.set_input("a", 1)
    s.set_input("sel", 0)  # b stays undefined, but is not selected
    assert out(s) == 1


def test_navigation_keeps_simulated_values(mux: tuple[ChipSession, Path]) -> None:
    s, _ = mux
    s.set_input("a", 1)
    s.set_input("b", 0)
    s.set_input("sel", 0)
    assert s.snapshot is not None
    or_part = s.snapshot.view.part(4)
    assert s.open(or_part) and s.path == "Mux/Or#4" and not s.at_top
    assert s.snapshot.view.chip == "Or"
    a_pin = s.snapshot.view.inputs[0]
    assert s.value(a_pin.nets) == 1  # Or's a = And(a, not sel) = 1
    nand = s.snapshot.view.part(3)
    assert not s.open(nand)  # primitives don't open
    assert s.up() and s.path == "Mux" and not s.up()


def test_reload_error_keeps_last_good_circuit(mux: tuple[ChipSession, Path]) -> None:
    s, d = mux
    s.set_input("a", 1)
    s.set_input("sel", 0)
    s.goto("Mux/Or#4")
    good = s.netlist
    (d / "Mux.hdl").write_text("CHIP Mux { IN a, b, sel; OUT out; PARTS: Or(a=a, out=out); }")
    assert not s.reload()
    assert s.error is not None and "input pin 'b' of Or is not connected" in str(s.error)
    assert s.netlist is good and s.path == "Mux/Or#4" and out(s) == 1


def test_reload_keeps_inputs_and_nearest_valid_path(mux: tuple[ChipSession, Path]) -> None:
    s, d = mux
    s.set_input("a", 1)
    s.set_input("sel", 0)
    s.goto("Mux/Or#4")
    # Remove the Or part: the view falls back to the top chip; inputs survive.
    (d / "Mux.hdl").write_text("CHIP Mux { IN a, b, sel; OUT out; PARTS: And(a=a, b=a, out=out); }")
    assert s.reload() and s.error is None
    assert s.path == "Mux" and s.inputs["a"] == 1 and out(s) == 1


def test_file_watcher(tmp_path: Path) -> None:
    f = tmp_path / "X.hdl"
    f.write_text("a")
    w = FileWatcher([tmp_path])
    assert not w.changed()
    f.write_text("bb")
    os.utime(f, ns=(1, 1))
    assert w.changed() and not w.changed()


def test_camera_zoom_keeps_point_fixed_and_hit_tests(mux: tuple[ChipSession, Path]) -> None:
    s, _ = mux
    assert s.snapshot is not None
    lay = s.snapshot.layout
    cam = Camera()
    cam.fit(lay, (0, 40, 800, 560))
    anchor = (400.0, 300.0)
    before = cam.to_layout(anchor)
    cam.zoom_at(anchor, 1.7)
    after = cam.to_layout(anchor)
    assert abs(before[0] - after[0]) < 1e-9 and abs(before[1] - after[1]) < 1e-9
    b = lay.boxes[("part", 4)]
    assert box_at(lay, (b.x + 2, b.y + 2)) == ("part", 4)
    first = lay.routes[0].points[0]
    assert route_at(lay, (first[0] + 1, first[1] + 2), 4) is not None


# ---- the clock -------------------------------------------------------------

BIT = """CHIP Bit { IN in, load; OUT out; PARTS:
    Nand(a=load, b=load, out=nl); Nand(a=prev, b=nl, out=x);
    Nand(a=in, b=load, out=y); Nand(a=x, b=y, out=d);
    DFF(in=d, out=prev, out=out); }"""
REG2 = """CHIP Reg2 { IN in[2], load; OUT out[2]; PARTS:
    Bit(in=in[0], load=load, out=out[0]);
    Bit(in=in[1], load=load, out=out[1]); }"""


@pytest.fixture
def bit(tmp_path: Path) -> tuple[ChipSession, Path]:
    (tmp_path / "Bit.hdl").write_text(BIT)
    s = ChipSession(file_loader(tmp_path / "Bit.hdl"))
    assert s.reload()
    return s, tmp_path / "Bit.hdl"


def load_bit(s: ChipSession, value: int) -> None:
    s.set_input("in", value)
    s.set_input("load", 1)
    s.step()
    s.set_input("load", 0)


def test_only_chips_with_dffs_have_a_clock(
    mux: tuple[ChipSession, Path], bit: tuple[ChipSession, Path]
) -> None:
    assert not mux[0].has_clock
    mux[0].toggle_run()
    assert not mux[0].running  # nothing to run
    assert bit[0].has_clock


def test_step_runs_one_cycle_and_reset_keeps_inputs(bit: tuple[ChipSession, Path]) -> None:
    s, _ = bit
    s.set_input("in", 1)
    s.set_input("load", 1)
    assert out(s) is None and s.cycle == 0
    s.step()
    assert out(s) == 1 and s.cycle == 1
    s.reset_clock()
    assert out(s) is None and s.cycle == 0
    assert s.inputs == {"in": 1, "load": 1}
    assert s.sim is not None and s.sim.get("load") == 1  # still applied after the reset
    s.step()
    assert out(s) == 1


def test_running_advances_with_time_at_the_chosen_speed(bit: tuple[ChipSession, Path]) -> None:
    s, _ = bit
    assert s.advance(1.0) == 0  # paused
    s.toggle_run()
    assert s.running and s.speed == 5
    assert s.advance(0.1) == 0  # half a cycle owed
    assert s.advance(0.1) == 1
    assert s.advance(1.0) == 5 and s.cycle == 6
    assert s.advance(10.2 - 10.0) == 1  # 0.999… cycles owed by float error is still one
    s.change_speed(+1)
    assert s.speed == 10
    s.change_speed(-99)
    assert s.speed == 1
    s.change_speed(+99)
    assert s.speed == 1000
    s.reset_clock()
    assert not s.running


def test_a_slow_chip_falls_behind_instead_of_freezing(bit: tuple[ChipSession, Path]) -> None:
    s, _ = bit
    s.toggle_run()
    # A minute owed and no time to spend: one cycle runs and the rest is dropped.
    assert s.advance(60.0, budget=0.0) == 1
    assert s.advance(0.0) == 0


def test_reload_keeps_dff_state_only_when_the_dffs_are_the_same(tmp_path: Path) -> None:
    (tmp_path / "Bit.hdl").write_text(BIT)
    top = tmp_path / "Reg2.hdl"
    top.write_text(REG2)
    s = ChipSession(file_loader(top, [tmp_path]))
    assert s.reload()
    s.set_input("in", 2)
    s.set_input("load", 1)
    s.step()
    s.set_input("load", 0)
    s.set_input("in", 0)
    assert out(s) == 2 and s.cycle == 1

    top.write_text(REG2.replace("PARTS:", "PARTS:\n    // stored bits"))
    assert s.reload()
    assert out(s) == 2 and s.cycle == 1  # the same two DFFs: state and count kept
    s.toggle_run()

    # A new first part renumbers both Bits (#2, #3). Their old numbers mean other
    # DFFs now, so nothing carries over: no bit may show its neighbour's value.
    top.write_text(REG2.replace("PARTS:", "PARTS:\n    Nand(a=load, b=load, out=unused);"))
    assert s.reload()
    assert s.sim is not None and s.sim.get_bits("out") == [None, None]
    assert s.cycle == 0 and not s.running


def test_cycle_count_restarts_when_no_state_carries(bit: tuple[ChipSession, Path]) -> None:
    s, path = bit
    load_bit(s, 1)
    path.write_text("CHIP Bit { IN in, load; OUT out; PARTS: Nand(a=in, b=load, out=out); }")
    assert s.reload() and s.cycle == 0  # no DFFs at all
    path.write_text(BIT)
    assert s.reload()
    assert s.cycle == 0 and out(s) is None  # DFFs again, but fresh ones


def test_reload_with_an_error_keeps_the_clock(bit: tuple[ChipSession, Path]) -> None:
    s, path = bit
    load_bit(s, 1)
    s.toggle_run()
    path.write_text("CHIP Bit {")
    assert not s.reload()
    assert s.running and out(s) == 1 and s.cycle == 1


def test_reload_to_a_chip_without_dffs_stops_the_clock(bit: tuple[ChipSession, Path]) -> None:
    s, path = bit
    s.toggle_run()
    path.write_text("CHIP Bit { IN in, load; OUT out; PARTS: Nand(a=in, b=load, out=out); }")
    assert s.reload()
    assert not s.has_clock and not s.running
