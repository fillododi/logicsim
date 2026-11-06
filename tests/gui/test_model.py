"""ChipView tests: parts, wires traced to their drivers, navigation paths."""

from __future__ import annotations

import pytest

from nandsim.gui.model import (
    breadcrumbs,
    build_view,
    child_path,
    parent_path,
)
from nandsim.hdl import parse
from nandsim.netlist import TRUE_NET, ChipLibrary, elaborate
from nandsim.testing import Impl


def ref_view(name: str, path: str | None = None):
    lib = Impl("reference").library()
    nl = elaborate(lib.resolve(name), lib)
    return build_view(nl, lib, path or name), nl


def test_mux_view() -> None:
    v, nl = ref_view("Mux")
    assert [p.chip for p in v.parts] == ["Not", "And", "And", "Or"]
    assert [q.name for q in v.inputs] == ["a", "b", "sel"]
    edges = {(str(e.src), str(e.dst), e.label) for e in v.edges}
    assert ("sel", "#1.in", "sel") in edges
    assert ("#1.out", "#2.b", "nsel") in edges
    assert ("#4.out", "out", "out") in edges
    assert set(v.wires) == {"nsel", "x", "y"}
    # Edge nets are the simulated nets of that signal.
    out_edge = next(e for e in v.edges if e.dst.kind == "output")
    assert list(out_edge.nets) == nl.outputs["out"]


def test_navigation() -> None:
    v, _ = ref_view("Mux")
    sub = v.part(4)
    assert child_path(v.path, sub) == "Mux/Or#4"
    inner, _ = ref_view("Mux", "Mux/Or#4")
    assert inner.chip == "Or"
    assert [p.chip for p in inner.parts] == ["Not", "Not", "Nand"]
    assert parent_path("Mux/Or#4") == "Mux"
    assert parent_path("Mux") is None
    assert breadcrumbs("Mux/Or#4/Nand#3") == [
        ("Mux", "Mux"),
        ("Or#4", "Mux/Or#4"),
        ("Nand#3", "Mux/Or#4/Nand#3"),
    ]
    nand = ref_view("Not")[0].part(1)
    assert nand.primitive and child_path("Not", nand) is None


@pytest.mark.parametrize("path", ["Xor", "Mux/Or#9", "Mux/And#4", "Mux/Or#4/Nand#3"])
def test_bad_paths(path: str) -> None:
    lib = Impl("reference").library()
    nl = elaborate(lib.resolve("Mux"), lib)
    with pytest.raises(KeyError):
        build_view(nl, lib, path)


def test_bus_driven_by_several_parts_and_constants() -> None:
    lib = ChipLibrary(
        sources={
            "Not": ("CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }", "Not.hdl"),
        }
    )
    src = (
        "CHIP T { IN a[2]; OUT o[2], k; PARTS:"
        " Not(in=a[0], out=o[0]); Not(in=a[1], out=o[1]); Nand(a=true, b=o[1], out=k); }"
    )
    lib.sources["T"] = (src, "T.hdl")
    top = parse(src, "T.hdl")
    nl = elaborate(top, lib)
    v = build_view(nl, lib, "T")
    shown = {(str(e.src), str(e.dst)) for e in v.edges}
    assert ("a[0..0]", "#1.in") in shown
    assert ("#1.out", "o[0..0]") in shown and ("#2.out", "o[1..1]") in shown
    assert ("#2.out", "#3.b") in shown
    const = next(e for e in v.edges if e.src.kind == "const")
    assert const.label == "true" and const.nets == (TRUE_NET,)
