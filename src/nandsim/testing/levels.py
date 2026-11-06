"""The level list: `chips/levels.toml`, in unlock order, with the parts each level may use."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from nandsim.paths import data_root


@dataclass(frozen=True)
class Level:
    name: str
    group: str
    parts: tuple[str, ...]
    root: Path

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
        Level(e["name"], e["group"], tuple(e.get("parts", [])), root) for e in data.get("level", [])
    ]


def find_level(name: str, root: Path | None = None) -> Level | None:
    return next((lv for lv in load_levels(root) if lv.name == name), None)
