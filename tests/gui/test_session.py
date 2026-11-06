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
