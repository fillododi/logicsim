"""Layout tests: geometric invariants on every level, a large chip, feedback, crossings."""

from __future__ import annotations

import time

import pytest

from nandsim.gui.layout import Layout, crossings, layout
from nandsim.gui.model import ChipView, build_view
from nandsim.hdl import parse
from nandsim.netlist import elaborate
from nandsim.testing import Impl, load_levels

PAIR = "CHIP Pair { IN a, b; OUT x, y; PARTS: Not(in=a, out=x); Not(in=b, out=y); }"


def view_of(src_or_name: str) -> ChipView:
    lib = Impl("reference").library()
    lib.sources["Pair"] = (PAIR, "Pair.hdl")
    if src_or_name.startswith("CHIP"):
        top = parse(src_or_name, "T.hdl")
        lib.sources[top.name] = (src_or_name, "T.hdl")
    else:
        top = lib.resolve(src_or_name)
    nl = elaborate(top, lib)
    return build_view(nl, lib, nl.top)


def big_chip(n: int = 16) -> str:
    """A 16-bit adder-like chip: 64 parts, a long carry chain, wide fan-out."""
    parts = []
    for i in range(n):
        carry = "false" if i == 0 else f"c{i - 1}"
        parts += [
            f"Xor(a=a[{i}], b=b[{i}], out=x{i});",
            f"Xor(a=x{i}, b={carry}, out=o[{i}]);",
            f"And(a=x{i}, b={carry}, out=p{i});",
            f"Or(a=p{i}, b=a[{i}], out=c{i});" if i < n - 1 else f"Or(a=p{i}, b=a[{i}], out=co);",
        ]
    body = " ".join(parts)
    return f"CHIP Big {{ IN a[{n}], b[{n}]; OUT o[{n}], co; PARTS: {body} }}"


FORWARD = "CHIP Fw { IN a; OUT o; PARTS: Not(in=p, out=o); Not(in=a, out=p); }"
# A real part-level cycle without a combinational loop: each Pair passes one bit
# to the other on independent paths.
CYCLE = (
    "CHIP Cy { IN i, j; OUT o1, o2; PARTS: Pair(a=i, b=t, x=s, y=o1); Pair(a=s, b=j, x=o2, y=t); }"
)


def check_invariants(view: ChipView, lay: Layout) -> None:
    boxes = [b for k, b in lay.boxes.items() if k[0] != "dummy"]
    for i, a in enumerate(boxes):  # no overlapping nodes
        for b in boxes[i + 1 :]:
            overlap = a.x < b.right and b.x < a.right and a.y < b.bottom and b.y < a.bottom
            assert not overlap, (a.key, b.key)
    for b in boxes:  # everything inside the canvas
        assert 0 <= b.x and b.right <= lay.width and 0 <= b.y and b.bottom <= lay.height
    ins = [lay.boxes[("in", p.name)] for p in view.inputs]
    outs = [lay.boxes[("out", p.name)] for p in view.outputs]
    parts = [lay.boxes[("part", p.index)] for p in view.parts]
    for p in parts:
        assert all(i.right < p.x for i in ins) and all(p.right < o.x for o in outs)
    for r in lay.routes:
        pts = r.points
        if not pts:
            assert r.edge.src.kind == "const" and r.label_at is not None
            continue
        for (x1, y1), (x2, y2) in zip(pts, pts[1:], strict=False):
            assert x1 == x2 or y1 == y2, f"diagonal segment in {r.edge}"


@pytest.mark.parametrize("name", [lv.name for lv in load_levels()])
def test_every_level_lays_out(name: str) -> None:
    v = view_of(name)
    check_invariants(v, layout(v))


def test_endpoints_meet_pin_anchors() -> None:
    v = view_of("Mux")
    lay = layout(v)
    for r in lay.routes:
        src = lay.boxes[("in", r.edge.src.pin)] if r.edge.src.kind == "input" else None
        if src is not None:
            assert r.points[0] == src.anchors[("out", r.edge.src.pin)]
        if r.edge.dst.kind == "part":
            dst = lay.boxes[("part", r.edge.dst.part)]
            assert r.points[-1] == dst.anchors[("in", r.edge.dst.pin)]


def test_large_chip_is_fast_and_valid() -> None:
    v = view_of(big_chip())
    assert len(v.parts) == 64
    t0 = time.perf_counter()
    lay = layout(v)
    elapsed = time.perf_counter() - t0
    check_invariants(v, lay)
    assert elapsed < 1.0, f"layout took {elapsed:.2f}s"


def test_deterministic() -> None:
    v = view_of(big_chip(4))
    a, b = layout(v), layout(v)
    assert [r.points for r in a.routes] == [r.points for r in b.routes]


def test_ordering_removes_avoidable_crossings() -> None:
    # Declared part order puts the part fed by `b` above the one fed by `a`,
    # which would cross both the input and the output wires.
    v = view_of("CHIP T { IN a, b; OUT x, y; PARTS: Not(in=b, out=y); Not(in=a, out=x); }")
    lay = layout(v)
    assert lay.layers[1] == [("part", 2), ("part", 1)]
    assert crossings(lay) == 0


def test_channel_tracks_avoid_crossings() -> None:
    # With channel tracks sorted by y, Xor's wires crossed 4 times.
    for name in ("Xor", "And", "Or"):
        assert crossings(layout(view_of(name))) == 0, name


def test_large_chip_has_few_crossings() -> None:
    # Measured 2537 with tracks sorted by y, 944 with cost-ordered tracks.
    assert crossings(layout(view_of(big_chip()))) < 1100


def test_part_level_cycle_is_drawn_as_feedback() -> None:
    v = view_of(CYCLE)
    lay = layout(v)
    check_invariants(v, lay)
    fb = [r for r in lay.routes if r.feedback]
    assert len(fb) == 1
    assert fb[0].edge.label == "t"


def test_forward_reference_is_not_feedback() -> None:
    v = view_of(FORWARD)
    lay = layout(v)
    check_invariants(v, lay)
    assert not any(r.feedback for r in lay.routes)


def test_direct_connections_lay_out() -> None:
    v = view_of(
        "CHIP D { IN a, b; OUT o, k, n; PARTS: o = a; k = false; g: Nand(a=a, b=b); n = g.out; }"
    )
    lay = layout(v)
    check_invariants(v, lay)
    assert any(r.edge.src.kind == "input" and r.edge.dst.kind == "output" for r in lay.routes)
