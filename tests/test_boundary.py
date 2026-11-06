"""The core packages must work without pygame: the emulator project will reuse them."""

from __future__ import annotations

import importlib
import subprocess
import sys

CORE_PACKAGES = ["nandsim.hdl", "nandsim.netlist", "nandsim.sim", "nandsim.testing"]


def test_core_imports_without_pygame() -> None:
    # Fresh interpreter, pygame made unimportable: any core import of it fails loudly.
    code = (
        "import sys; sys.modules['pygame'] = None\n"
        + "\n".join(f"import {pkg}" for pkg in CORE_PACKAGES)
        + "\nassert 'pygame' not in {m for m, v in sys.modules.items() if v is not None}"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_core_packages_exist() -> None:
    for pkg in CORE_PACKAGES:
        assert importlib.import_module(pkg).__doc__
