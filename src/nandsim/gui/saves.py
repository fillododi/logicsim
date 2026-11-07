"""The player's saved chips and progress. Pure Python, no pygame.

Layout of the save directory (default `~/.local/share/nandsim/save/`):

    <Name>.hdl       the player's HDL for each chip they have opened
    progress.json    {"version": 1, "solved": ["Not", "And", ...]}

A game reset moves all of these into `<save dir>-backups/<time>/`, next to the
save directory and never inside it: the chip library searches the save directory
recursively, so a backup inside it would still be used as the player's chips.

Chips the player exports under a name of their own live in `<save dir>-exports/`,
beside the save directory for the same reason. Every level may use them as parts,
so they are part of the library. Deleting one moves its file to
`<save dir>-backups/<time>/exports/`, and so does a reset for all of them.

A level is *unlocked* when every level it may use as a part is solved; primitives
are always available. An exported chip may use a primitive only once an unlocked
level lists it, so exports never carry a DFF into the levels before it.

*Solved* is sticky: it records that the chip passed its tests once, so later
experiments never lock the player out of a level.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from nandsim.hdl import ChipDef, HdlError, parse
from nandsim.netlist import PRIMITIVES, ChipLibrary, Primitive, elaborate
from nandsim.paths import default_save_dir, exports_dir, settings_file
from nandsim.testing import Level, exported_chips
from nandsim.testing.levels import CHIP_NAME, KEYWORDS

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
        return ChipLibrary([self.root, self.exports], sources)

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

    def unlocked_primitives(self) -> frozenset[str]:
        """The primitives some unlocked level lists: the ones exported chips may use."""
        return frozenset(
            p for lv in self.levels if self.is_unlocked(lv) for p in lv.parts if p in PRIMITIVES
        )

    # ---- exported chips -----------------------------------------------

    @property
    def exports(self) -> Path:
        return exports_dir(self.root)

    @property
    def settings_path(self) -> Path:
        """Mute and volume (see `gui.settings`), beside the save dir so a reset keeps them."""
        return settings_file(self.root)

    def exported(self) -> list[str]:
        """The player's exported chips, by name: parts that every level may use."""
        return exported_chips(self.exports, self.levels)

    def export_path(self, name: str) -> Path:
        return self.exports / f"{name}.hdl"

    def name_problem(self, name: str) -> str | None:
        """Why `name` can't be an exported chip's name, or None if it can."""
        if not name:
            return "Type a name for the chip."
        if not CHIP_NAME.fullmatch(name):
            return "A chip name starts with a letter and has only letters, digits and _."
        if name in KEYWORDS:
            return f"{name} is a word of the HDL. Pick another name."
        if name in PRIMITIVES:
            return f"{name} is a built-in chip. Pick another name."
        if any(lv.name == name for lv in self.levels):
            return f"{name} is a level's chip. Pick another name, like My{name}."
        return None

    def prepare_export(self, name: str, text: str) -> str:
        """`text` renamed to `CHIP <name>`, once it is known to build.

        Raises ValueError with a message for the player: a bad name, or the build
        error (positions match the editor, since renaming keeps lines and columns
        apart from the name itself).
        """
        problem = self.name_problem(name)
        if problem:
            raise ValueError(problem)
        try:
            chip = parse(text, f"{name}.hdl")
            renamed = _rename(text, chip, name)
            lib = ChipLibrary(
                [self.root, self.exports], {name: (renamed, str(self.export_path(name)))}
            )
            top = lib.resolve(name)
            assert not isinstance(top, Primitive)
            netlist = elaborate(top, lib)
        except HdlError as e:
            where = f"line {e.pos.line}:{e.pos.col}: " if e.pos else ""
            raise ValueError(f"It doesn't build yet: {where}{e.message}") from None
        # Checked on the flattened chip, so a DFF inside a saved or exported part counts.
        allowed = self.unlocked_primitives()
        for kind, gates in netlist.gates.items():
            if gates.count and kind not in allowed:
                raise ValueError(f"It uses {kind}, which no level you have unlocked allows yet.")
        return renamed

    def export(self, name: str, text: str) -> Path:
        """Write `text`, as returned by `prepare_export`, to `<exports>/<name>.hdl`."""
        path = self.export_path(name)
        atomic_write(path, text)
        return path

    def delete_export(self, name: str, now: datetime | None = None) -> Path:
        """Take an exported chip out of the library; return where its file went.

        Like a reset, nothing is destroyed: the file moves to `backups/<time>/exports/`.
        """
        path = self.export_path(name)
        dest = self._new_backup(now) / "exports"
        dest.mkdir()
        return path.replace(dest / path.name)

    def users_of(self, name: str) -> list[str]:
        """The player's chips, saved or exported, that use `name` directly as a part.

        Files that don't parse are skipped: they can't be using anything yet.
        """
        files = [self.path(lv) for lv in self.levels]
        files += [self.export_path(n) for n in self.exported() if n != name]
        users = []
        for f in files:
            if not f.is_file():
                continue
            try:
                chip = parse(f.read_text(encoding="utf-8"), str(f))
            except (HdlError, OSError, UnicodeDecodeError):
                continue
            if any(part.chip == name for part in chip.parts):
                users.append(f.stem)
        return users

    # ---- reset --------------------------------------------------------

    @property
    def backups(self) -> Path:
        return self.root.with_name(self.root.name + "-backups")

    def has_progress(self) -> bool:
        """Whether the player has anything to lose: a chip, saved or exported, progress
        or tour state."""
        return bool(self._player_files() or self._export_files())

    def reset(self, now: datetime | None = None) -> Path | None:
        """Start over: move every player file into `backups/<time>/` and return that folder.

        `backups` is `<save dir>-backups`, beside the save directory (see the module doc).
        Exported chips go too, into `backups/<time>/exports/`.

        Nothing is deleted, so a reset by mistake can be undone by moving the files
        back. Returns None, and creates nothing, when there was nothing to move.
        """
        files, exports = self._player_files(), self._export_files()
        self._solved = set()
        self.warning = None
        if not files and not exports:
            return None
        dest = self._new_backup(now)
        for f in files:
            f.replace(dest / f.name)
        if exports:
            (dest / "exports").mkdir()
            for f in exports:
                f.replace(dest / "exports" / f.name)
        return dest

    def _new_backup(self, now: datetime | None) -> Path:
        """A new, empty `backups/<time>/` folder, made unique within the same second."""
        stamp = (now or datetime.now()).strftime("%Y-%m-%d_%H%M%S")
        dest = self.backups / stamp
        n = 1
        while dest.exists():
            n += 1
            dest = self.backups / f"{stamp}-{n}"
        dest.mkdir(parents=True)
        return dest

    def _player_files(self) -> list[Path]:
        if not self.root.is_dir():
            return []
        return sorted(p for p in self.root.iterdir() if p.is_file())

    def _export_files(self) -> list[Path]:
        """Every file in the exports folder, chip or not: a reset leaves it empty."""
        if not self.exports.is_dir():
            return []
        return sorted(p for p in self.exports.iterdir() if p.is_file())

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


def _rename(text: str, chip: ChipDef, name: str) -> str:
    """`text` with the name after CHIP replaced by `name`; everything else is kept."""
    pos = chip.name_pos
    assert pos is not None
    lines = text.split("\n")
    line = lines[pos.line - 1]
    start = pos.col - 1
    lines[pos.line - 1] = line[:start] + name + line[start + len(chip.name) :]
    return "\n".join(lines)
