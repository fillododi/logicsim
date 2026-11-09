"""The level list: `chips/levels.toml`, in unlock order, with the parts each level may use.

Besides the parts a level lists, every level may use the chips the player exported
(see `exported_chips`): they are the player's own building blocks, made of parts
they have already unlocked.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from nandsim.netlist import PRIMITIVES
from nandsim.paths import data_root

CHIP_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
KEYWORDS = frozenset({"CHIP", "IN", "OUT", "PARTS", "true", "false", "clock"})


@dataclass(frozen=True)
class Level:
    name: str
    group: str
    parts: tuple[str, ...]
    root: Path
    # Levels that must be solved first besides the parts, to open a group in story order.
    requires: tuple[str, ...] = ()

    def _file(self, folder: str, ext: str) -> Path:
        return self.root / folder / self.group / f"{self.name}{ext}"

    @property
    def stub(self) -> Path:
        return self._file("chips", ".hdl")

    @property
    def brief(self) -> Path:
        return self._file("chips", ".md")

    @property
    def tst(self) -> Path:
        return self._file("chips", ".tst")

    @property
    def reference(self) -> Path:
        return self._file("reference", ".hdl")


def load_levels(root: Path | None = None) -> list[Level]:
    """Read `levels.toml` under `root` (default: `data_root()`)."""
    root = root or data_root()
    with open(root / "chips" / "levels.toml", "rb") as f:
        data = tomllib.load(f)
    return [
        Level(e["name"], e["group"], tuple(e.get("parts", [])), root, tuple(e.get("requires", [])))
        for e in data.get("level", [])
    ]


def find_level(name: str, root: Path | None = None) -> Level | None:
    return next((lv for lv in load_levels(root) if lv.name == name), None)


def exported_chips(directory: Path, levels: list[Level]) -> list[str]:
    """Names of the player's exported chips: `<Name>.hdl` files directly in `directory`.

    A file whose name couldn't be a chip of its own (not an identifier, a keyword, a
    primitive or a level's chip) is left out, so it can never stand in for a level.
    """
    if not directory.is_dir():
        return []
    taken = {lv.name for lv in levels} | set(PRIMITIVES) | KEYWORDS
    names = [
        p.stem
        for p in directory.iterdir()
        if p.suffix == ".hdl" and p.is_file() and CHIP_NAME.fullmatch(p.stem)
    ]
    return sorted((n for n in names if n not in taken), key=str.lower)
