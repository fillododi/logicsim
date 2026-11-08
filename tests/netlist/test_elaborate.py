"""Elaboration tests: flattening, aliasing through the hierarchy, and every wiring error."""

from __future__ import annotations

import importlib

import pytest

from nandsim.hdl import HdlError, parse
from nandsim.netlist import CLOCK_NET, FALSE_NET, TRUE_NET, ChipLibrary, elaborate

NOT = "CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }"
AND = "CHIP And { IN a, b; OUT out; PARTS: Nand(a=a, b=b, out=n); Not(in=n, out=out); }"
NOT2 = (
    "CHIP Not2 { IN in[2]; OUT out[2]; PARTS:"
    " Not(in=in[0], out=out[0]); Not(in=in[1], out=out[1]); }"
)


def lib(**extra: str) -> ChipLibrary:
    sources = {"Not": NOT, "And": AND, "Not2": NOT2, **extra}
    return ChipLibrary(sources={k: (v, f"{k}.hdl") for k, v in sources.items()})


def build(src: str, library: ChipLibrary | None = None):
    return elaborate(parse(src, "Top.hdl"), library or lib())


def test_flattens_to_primitives_through_two_levels() -> None:
    nl = build("CHIP Top { IN a, b; OUT o; PARTS: And(a=a, b=b, out=o); }")
    assert nl.gate_count == 2
    assert len(nl.levels) == 2
    # Top output aliases through And's output to the Nand inside Not.
    assert nl.outputs["o"] == nl.wires["Top/And#1/Not#2/out"] == nl.wires["Top/And#1/out"]
    assert nl.wires["Top/And#1/a"] == nl.inputs["a"]


def test_parts_in_any_order_and_constants() -> None:
    nl = build(
        "CHIP Top { IN a; OUT o, t; PARTS: Not(in=x, out=o); Nand(a=a, b=true, out=x);"
        " Nand(a=false, b=false, out=t); }"
    )
    nand_in = nl.gates["Nand"].inputs
    assert TRUE_NET in nand_in[1].tolist() and FALSE_NET in nand_in[0].tolist()
    assert len(nl.levels) == 2


def test_buses_and_reading_own_output() -> None:
    nl = build(
        "CHIP Top { IN a[2]; OUT o[2], echo; PARTS: Not2(in=a, out=o); Not(in=o[1], out=echo); }"
    )
    assert len(nl.outputs["o"]) == 2
    assert nl.wires["Top/Not#2/in"] == [nl.outputs["o"][1]]


def test_unused_part_output_is_allowed() -> None:
    build("CHIP Top { IN a; OUT o; PARTS: Not2(in[0]=a, in[1]=a, out[0]=o); }")


ERRORS = [
    (
        "CHIP Top { IN a; OUT o; PARTS: Foo(in=a, out=o); }",
        "Top.hdl:1:32: error: unknown chip 'Foo'",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Nand(a=a, c=a, out=o); }",
        "Top.hdl:1:42: error: Nand has no pin 'c' (its pins are: a, b, out)",
    ),
    (
        "CHIP Top { IN a[2]; OUT o; PARTS: Not(in=a, out=o); }",
        "Top.hdl:1:42: error: width mismatch: pin 'in' of Not has 1 bit but 'a' has 2",
    ),
    (
        "CHIP Top { IN a[2]; OUT o; PARTS: Not(in=a[2], out=o); }",
        "Top.hdl:1:42: error: a[2] is out of range: 'a' has 2 bits (0..1)",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not2(in[2]=a, out[0]=o); }",
        "Top.hdl:1:37: error: in[2] is out of range: pin 'in' of Not2 has 2 bits (0..1)",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not(in=a, out=a); }",
        "Top.hdl:1:46: error: 'a' is an input pin of Top: a part output cannot drive it",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not(in=a, out=true); }",
        "Top.hdl:1:46: error: output pin 'out' of Not cannot be connected to a constant",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS:\n Not(in=a, out=o);\n Not(in=a, out=o); }",
        "Top.hdl:3:16: error: 'o' is already driven by Not at line 2",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not(in=w, out=o); }",
        "Top.hdl:1:39: error: 'w' is not a pin of Top and nothing drives a wire with that name",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Nand(a=a, out=o); }",
        "Top.hdl:1:32: error: input pin 'b' of Nand is not connected",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not2(in[0]=a, out[0]=o); }",
        "Top.hdl:1:32: error: bit 1 of input pin 'in' of Not2 is not connected",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Nand(a=a, a=a, b=a, out=o); }",
        "Top.hdl:1:42: error: pin 'a' of Nand is connected more than once",
    ),
    (
        "CHIP Top { IN a;\n OUT o; PARTS: }",
        "Top.hdl:2:6: error: output pin 'o' of Top is not connected",
    ),
    (
        "CHIP Top { IN a; OUT o[4]; PARTS: Not(in=a, out=o[1]); }",
        "Top.hdl:1:22: error: bits 0, 2..3 of output pin 'o' of Top are not connected",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not(in=a, out=w[0]); Not(in=w, out=o); }",
        "Top.hdl:1:46: error: internal wire 'w' cannot be sliced where it is created; "
        "write 'out=w'",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: DFF(d=a, out=o); }",
        "Top.hdl:1:36: error: DFF has no pin 'd' (its pins are: in, out)",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: DFF(out=o); }",
        "Top.hdl:1:32: error: input pin 'in' of DFF is not connected",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: Not(in=a, out=clock); }",
        "Top.hdl:1:46: error: output pin 'out' of Not cannot be connected to the clock",
    ),
    (
        "CHIP Top { IN a; OUT o; PARTS: w = clock; Not(in=w, out=o); }",
        "Top.hdl:1:36: error: the width of new wire 'w' can't come from the clock; "
        "connect the clock to a pin instead",
    ),
]


def test_feedback_loops_build() -> None:
    """A signal may depend on itself: a latch is just two NANDs."""
    nl = build(
        "CHIP Top { IN s, r; OUT q; PARTS: Nand(a=s, b=nq, out=q); Nand(a=r, b=q, out=nq); }"
    )
    assert [lv.loops for lv in nl.levels] == [1]


def test_clock_fills_every_bit_like_a_constant() -> None:
    nl = build("CHIP Top { OUT o[2]; PARTS: o = clock; }")
    assert nl.outputs["o"] == [CLOCK_NET, CLOCK_NET]


@pytest.mark.parametrize(("src", "message"), ERRORS)
def test_wiring_errors(src: str, message: str) -> None:
    with pytest.raises(HdlError) as exc:
        build(src)
    assert str(exc.value) == message


def test_circular_dependency_between_chips() -> None:
    library = lib(
        A="CHIP A { IN a; OUT o; PARTS: B(a=a, o=o); }",
        B="CHIP B { IN a; OUT o; PARTS: A(a=a, o=o); }",
    )
    with pytest.raises(HdlError) as exc:
        build("CHIP Top { IN a; OUT o; PARTS: A(a=a, o=o); }", library)
    assert (
        str(exc.value) == "B.hdl:1:30: error: circular dependency between chips: Top -> A -> B -> A"
    )


def test_file_defining_wrong_chip() -> None:
    library = lib(Bad="CHIP Other { OUT o; PARTS: Nand(a=true, b=true, out=o); }")
    with pytest.raises(HdlError) as exc:
        build("CHIP Top { OUT o; PARTS: Bad(o=o); }", library)
    assert str(exc.value) == "Bad.hdl:1:1: error: file for chip 'Bad' defines chip 'Other' instead"


# ---- compiling each chip once ---------------------------------------------


def test_repeated_parts_get_their_own_nets() -> None:
    nl = build("CHIP Top { IN a, b; OUT x, y; PARTS: And(a=a, b=b, out=x); And(a=b, b=a, out=y); }")
    first, second = nl.wires["Top/And#1/n"], nl.wires["Top/And#2/n"]
    assert first != second
    assert nl.gate_count == 4 and len(set(nl.gates["Nand"].outputs[0].tolist())) == 4
    assert nl.wires["Top/And#2/a"] == nl.inputs["b"]
    assert nl.gate_paths["Nand"] == [
        "Top/And#1/Nand#1",
        "Top/And#1/Not#2/Nand#1",
        "Top/And#2/Nand#1",
        "Top/And#2/Not#2/Nand#1",
    ]


def test_a_chip_is_compiled_once_per_library(monkeypatch: pytest.MonkeyPatch) -> None:
    module = importlib.import_module("nandsim.netlist.elaborate")
    library = lib()
    top = parse(
        "CHIP Top { IN a, b; OUT x, y; PARTS: And(a=a, b=b, out=x); And(a=b, b=a, out=y); }",
        "Top.hdl",
    )
    calls: list[str] = []
    original = module._Builder.build

    def counting(self: object) -> object:
        calls.append(self.chip.name)  # type: ignore[attr-defined]
        return original(self)

    monkeypatch.setattr(module._Builder, "build", counting)
    elaborate(top, library)
    elaborate(top, library)
    assert sorted(calls) == ["And", "Not", "Top"]


def test_a_new_library_sees_edited_sources() -> None:
    top = "CHIP Top { IN a, b; OUT o; PARTS: And(a=a, b=b, out=o); }"
    assert build(top).gate_count == 2
    three = "CHIP And { IN a, b; OUT out; PARTS: Nand(a=a, b=b, out=n); Not(in=n, out=m);"
    three += " Not(in=m, out=k); Not(in=k, out=out); }"
    assert build(top, lib(And=three)).gate_count == 4


def test_wire_map_behaves_like_a_dict() -> None:
    nl = build("CHIP Top { IN a, b; OUT o; PARTS: And(a=a, b=b, out=o); }")
    paths = list(nl.wires)
    assert len(paths) == len(nl.wires) == len(set(paths))
    assert "Top/And#1/Not#2/Nand#1/out" in nl.wires
    assert "Top/And#1/Nope" not in nl.wires and "Top" not in nl.wires
    assert nl.wires.get("Other/a") is None
    with pytest.raises(KeyError):
        nl.wires["Top/And#3/a"]
    walked = dict(nl.wires.walk())  # type: ignore[attr-defined]
    assert {p: n.tolist() for p, n in walked.items()} == {p: nl.wires[p] for p in paths}
    # Parts come before the chip that holds them, as the GUI's names expect.
    assert paths.index("Top/And#1/a") < paths.index("Top/a")
