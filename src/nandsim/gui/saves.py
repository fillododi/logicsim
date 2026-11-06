"""The player's saved chips and progress. Pure Python, no pygame.

Layout of the save directory (default `~/.local/share/nandsim/save/`):

    <Name>.hdl       the player's HDL for each chip they have opened
    progress.json    {"version": 1, "solved": ["Not", "And", ...]}

A game reset moves all of these into `<save dir>-backups/<time>/`, next to the
save directory and never inside it: the chip library searches the save directory
recursively, so a backup inside it would still be used as the player's chips.

Chip files the player exports, or wants to import, live in `<save dir>-exports/`,
beside the save directory for the same reason, and a reset leaves them alone.

A level is *unlocked* when every level it may use as a part is solved; primitives
are always available. *Solved* is sticky: it records that the chip passed its
tests once, so later experiments never lock the player out of a level.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
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
        atomic_write(self.path(level), text)

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

    # ---- chip files ---------------------------------------------------

    @property
    def exports(self) -> Path:
        return self.root.with_name(self.root.name + "-exports")

    def export_path(self, level: Level) -> Path:
        return self.exports / f"{level.name}.hdl"

    def export(self, level: Level, text: str) -> Path:
        """Write `text` as the level's chip file in the exports folder, replacing any old one."""
        path = self.export_path(level)
        atomic_write(path, text)
        return path

    def chip_files(self, first: str | None = None) -> list[Path]:
        """The `.hdl` files in the exports folder: `<first>.hdl` leads, the rest by name."""
        if not self.exports.is_dir():
            return []
        files = [p for p in self.exports.iterdir() if p.suffix == ".hdl" and p.is_file()]
        return sorted(files, key=lambda p: (p.stem != first, p.name.lower()))

    def read_chip_file(self, path: Path) -> str:
        """The text of a chip file; ValueError, with a message for the player, if unreadable."""
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ValueError(f"{path.name} isn't a text file") from None
        except OSError as e:
            raise ValueError(f"couldn't read {path.name}: {e.strerror or e}") from None

    # ---- reset --------------------------------------------------------

    @property
    def backups(self) -> Path:
        return self.root.with_name(self.root.name + "-backups")

    def has_progress(self) -> bool:
        """Whether the player has anything to lose: a saved chip, progress or tour state."""
        return bool(self._player_files())

    def reset(self, now: datetime | None = None) -> Path | None:
        """Start over: move every player file into `backups/<time>/` and return that folder.

        `backups` is `<save dir>-backups`, beside the save directory (see the module doc).

        Nothing is deleted, so a reset by mistake can be undone by moving the files
        back. Returns None, and creates nothing, when there was nothing to move.
        """
        files = self._player_files()
        self._solved = set()
        self.warning = None
        if not files:
            return None
        stamp = (now or datetime.now()).strftime("%Y-%m-%d_%H%M%S")
        dest = self.backups / stamp
        n = 1
        while dest.exists():  # two resets within the same second
            n += 1
            dest = self.backups / f"{stamp}-{n}"
        dest.mkdir(parents=True)
        for f in files:
            f.replace(dest / f.name)
        return dest

    def _player_files(self) -> list[Path]:
        if not self.root.is_dir():
            return []
        return sorted(p for p in self.root.iterdir() if p.is_file())

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
        atomic_write(self.root / "progress.json", json.dumps(data, indent=2) + "\n")


def atomic_write(path: Path, text: str) -> None:
    """Write via a temp file and rename, so a crash never leaves half a save."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)
