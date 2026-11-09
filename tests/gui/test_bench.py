"""The clock panel's MCS-4 memories: a CPU in the GUI runs the level's demo program."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from nandsim.gui.session import RESET_CLOCKS, ChipSession, file_loader
from nandsim.paths import data_root
from nandsim.testing import parse_rom

ROOT = data_root()
CPU = ROOT / "reference" / "05_cpu" / "CPU.hdl"
PROGRAM = parse_rom((ROOT / "chips" / "05_cpu" / "CPU.rom").read_text())
_spec = importlib.util.spec_from_file_location(
    "model4004", Path(__file__).resolve().parents[2] / "tools" / "model4004.py"
)
assert _spec is not None and _spec.loader is not None
m4 = importlib.util.module_from_spec(_spec)
sys.modules["model4004"] = m4
_spec.loader.exec_module(m4)


def cpu_session(program: list[int] | None = PROGRAM) -> ChipSession:
    s = ChipSession(file_loader(CPU), program=program)
    assert s.reload(), s.error
    return s


def counter(s: ChipSession) -> list[int | None]:
    assert s.memories is not None
    return [s.memories.cells.get((0, "main", k)) for k in range(4)]


def test_the_cpu_starts_reset_at_a1_of_address_0() -> None:
    s = cpu_session()
    assert s.memories is not None and s.memories.period() == "A1"
    assert s.cycle == 0 and s.inputs["reset"] == 0 and s.inputs["test"] == 0
    assert s.sim is not None and s.sim.get("dout") == 0 and s.sim.get("drive") == 1


def test_steps_run_the_demo_as_the_4004_model_does() -> None:
    s = cpu_session()
    model = m4.Mcs4(rom=PROGRAM + [0] * (4096 - len(PROGRAM)))
    model.reset()
    cycles = 0
    while cycles < 120:
        cycles += model.step()
    for _ in range(8 * cycles):
        s.step()
    assert s.bus_problem is None
    assert counter(s) == [model.main[(0, k)] for k in range(4)]
    assert s.memories is not None and s.memories.romport_out[0] == model.romport_out[0]


def test_din_belongs_to_the_memories() -> None:
    s = cpu_session()
    assert s.drives("din") and not s.drives("test")
    s.set_input("din", 9)
    assert "din" not in s.inputs or s.inputs["din"] != 9
    assert s.sim is not None and s.sim.get("din") == 0  # A1: nobody sends


def test_reset_restarts_the_program() -> None:
    s = cpu_session()
    for _ in range(8 * 60):
        s.step()
    assert counter(s) != [None] * 4
    s.reset_clock()
    assert s.cycle == 0 and s.memories is not None and s.memories.period() == "A1"
    assert counter(s) == [None] * 4  # fresh memories: the demo hasn't cleared them yet
    assert RESET_CLOCKS == 64


def test_memories_only_with_a_program_and_the_bus_pins(tmp_path: Path) -> None:
    assert cpu_session(program=None).memories is None
    bit = tmp_path / "B.hdl"
    bit.write_text("CHIP B { IN in, load; OUT out; PARTS: Bit(in=in, load=load, out=out); }")
    s = ChipSession(file_loader(bit, [ROOT / "reference"]), program=PROGRAM)
    assert s.reload(), s.error
    assert s.memories is None and not s.drives("din")
