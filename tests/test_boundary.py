"""Architecture rules enforced as tests.

- The core packages must work without pygame: the emulator project will reuse them.
- The GUI's model, layout and save modules are pure too, so they can be tested headless.
- The GUI must never load the hidden reference solutions.
"""

from __future__ import annotations

import importlib
import re
import subprocess
import sys
from pathlib import Path

CORE_PACKAGES = ["nandsim.hdl", "nandsim.netlist", "nandsim.sim", "nandsim.testing"]
PURE_GUI_MODULES = [
    "nandsim.gui.model",
    "nandsim.gui.layout",
    "nandsim.gui.saves",
    "nandsim.gui.session",
    "nandsim.gui.camera",
    "nandsim.gui.textbuffer",
    "nandsim.gui.syntax",
    "nandsim.gui.brief",
    "nandsim.gui.game",
]
GUI_DIR = Path(__file__).parents[1] / "src" / "nandsim" / "gui"


def _imports_without_pygame(modules: list[str]) -> subprocess.CompletedProcess[str]:
    # Fresh interpreter, pygame made unimportable: any import of it fails loudly.
    code = (
        "import sys; sys.modules['pygame'] = None\n"
        + "\n".join(f"import {m}" for m in modules)
        + "\nassert 'pygame' not in {m for m, v in sys.modules.items() if v is not None}"
    )
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)


def test_core_imports_without_pygame() -> None:
    result = _imports_without_pygame(CORE_PACKAGES)
    assert result.returncode == 0, result.stderr


def test_pure_gui_modules_import_without_pygame() -> None:
    result = _imports_without_pygame(PURE_GUI_MODULES)
    assert result.returncode == 0, result.stderr


def test_core_packages_exist() -> None:
    for pkg in CORE_PACKAGES:
        assert importlib.import_module(pkg).__doc__


def test_gui_never_touches_reference_solutions() -> None:
    # The reference is reachable only via Impl("reference") or a Level's .reference path.
    forbidden = re.compile(r"""Impl\(\s*["']reference|\.reference\b|["']reference["']""")
    offenders = [
        f"{path.relative_to(GUI_DIR)}:{n}"
        for path in sorted(GUI_DIR.rglob("*.py"))
        for n, line in enumerate(path.read_text().splitlines(), start=1)
        if forbidden.search(line)
    ]
    assert not offenders, f"GUI code references the hidden solutions: {offenders}"
