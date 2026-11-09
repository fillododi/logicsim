"""The committed .tst files that a script in tools/ generates match what it generates now."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_tool(name: str):  # noqa: ANN201 - a module loaded from a path
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses look their module up while it loads
    spec.loader.exec_module(module)
    return module


def test_ram_tests_match_their_generator() -> None:
    generated = load_tool("gen_ram_tst").generate()
    assert sorted(generated) == ["DataRAM", "RAM4002", "RAM64", "RAM8", "RAMBank"]
    for name, text in generated.items():
        committed = (ROOT / "chips" / "06_ram" / f"{name}.tst").read_text()
        assert committed == text, f"{name}.tst is stale: run tools/gen_ram_tst.py chips/06_ram"


def test_cpu_test_matches_its_generator() -> None:
    committed = (ROOT / "chips" / "05_cpu" / "CPU.tst").read_text()
    assert committed == load_tool("gen_cpu_tst").generate(), (
        "CPU.tst is stale: run tools/gen_cpu_tst.py chips/05_cpu"
    )


def test_cpu_unit_tests_match_their_generator() -> None:
    generated = load_tool("gen_cpu_units").generate()
    assert sorted(generated) == ["Accumulator", "BusOut", "Jumps", "Registers", "Sequencer"]
    for name, text in generated.items():
        committed = (ROOT / "chips" / "05_cpu" / f"{name}.tst").read_text()
        assert committed == text, f"{name}.tst is stale: run tools/gen_cpu_units.py chips/05_cpu"
