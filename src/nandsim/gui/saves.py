"""The player's saved chips and progress. Pure Python, no pygame.

Layout of the save directory (default `~/.local/share/nandsim/save/`):

    <Name>.hdl       the player's HDL for each chip they have opened
    progress.json    {"version": 1, "solved": ["Not", "And", ...]}

A level is *unlocked* when every level it may use as a part is solved; primitives
are always available. *Solved* is sticky: it records that the chip passed its
tests once, so later experiments never lock the player out of a level.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from nandsim.netlist import PRIMITIVES, ChipLibrary
from nandsim.paths import default_save_dir
from nandsim.testing import Level

PROGRESS_VERSION = 1


class SaveStore:
    def __init__(self, levels: list[Level], root: Path | None = None) -> None:
        self.levels = levels
        self.root = root or default_save_dir()
        self.warning: str | None = None  # shown by the GUI if progress was unreadable
        self._solved = self._read_progress()

    # ---- chip sources -------------------------------------------------

    def path(self, level: Level) -> Path:
        return self.root / f"{level.name}.hdl"

    def load(self, level: Level) -> str:
        """The player's text for a level, or the level's stub if they never saved it."""
        p = self.path(level)
        return p.read_text() if p.is_file() else level.stub.read_text()

    def has_save(self, level: Level) -> bool:
        return self.path(level).is_file()

    def save(self, level: Level, text: str) -> None:
        _atomic_write(self.path(level), text)

    def library(self, editing: Level | None = None, text: str | None = None) -> ChipLibrary:
        """Chips as the player built them; `text` overrides `editing`'s file (unsaved editor)."""
        sources = {}
        if editing is not None and text is not None:
            sources[editing.name] = (text, str(self.path(editing)))
        return ChipLibrary([self.root], sources)

    # ---- progress -----------------------------------------------------

    @property
    def solved(self) -> frozenset[str]:
        return frozenset(self._solved)

    def mark_solved(self, level: Level) -> None:
        if level.name not in self._solved:
            self._solved.add(level.name)
            self._write_progress()

    def is_unlocked(self, level: Level) -> bool:
        needed = {p for p in level.parts if p not in PRIMITIVES}
        return needed <= self._solved

    def _read_progress(self) -> set[str]:
        p = self.root / "progress.json"
        if not p.is_file():
            return set()
        try:
            data = json.loads(p.read_text())
            if data.get("version") != PROGRESS_VERSION:
                raise ValueError(f"unknown version {data.get('version')!r}")
            return {str(n) for n in data["solved"]}
        except (ValueError, KeyError, TypeError) as e:
            backup = p.with_suffix(".json.bad")
            p.replace(backup)
            self.warning = f"progress file was unreadable ({e}); kept a copy as {backup.name}"
            return set()

    def _write_progress(self) -> None:
        data = {"version": PROGRESS_VERSION, "solved": sorted(self._solved)}
        _atomic_write(self.root / "progress.json", json.dumps(data, indent=2) + "\n")


def _atomic_write(path: Path, text: str) -> None:
    """Write via a temp file and rename, so a crash never leaves half a save."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)
