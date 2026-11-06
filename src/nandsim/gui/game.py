"""Game rules for the GUI: which level is open, its status, building and testing it. No pygame.

The player's own chips (in the save dir) are the only implementations the game
ever uses; the hidden reference solutions are never loaded here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from nandsim.gui.saves import SaveStore
from nandsim.gui.session import Loader
from nandsim.netlist import PRIMITIVES, ChipLibrary
from nandsim.testing import Level, TstResult, parse_tst, run_script

Status = Literal["solved", "open", "locked"]


@dataclass
class TestReport:
    """What the results panel shows after "Run tests"."""

    passed: bool
    summary: str
    lines: list[str]


class GameState:
    def __init__(self, store: SaveStore) -> None:
        self.store = store
        self.levels = store.levels
        self.current: Level = self._first_level()
        self.report: TestReport | None = None

    def _first_level(self) -> Level:
        """The first unlocked level not solved yet; otherwise the first level."""
        for lv in self.levels:
            if self.status(lv) == "open":
                return lv
        return self.levels[0]

    # ---- levels -----------------------------------------------------------

    def status(self, level: Level) -> Status:
        if level.name in self.store.solved:
            return "solved"
        return "open" if self.store.is_unlocked(level) else "locked"

    def missing(self, level: Level) -> list[str]:
        """Chips the player must solve before this level unlocks."""
        return [p for p in level.parts if p not in PRIMITIVES and p not in self.store.solved]

    def select(self, level: Level) -> bool:
        """Open a level; locked levels can't be opened."""
        if self.status(level) == "locked":
            return False
        self.current = level
        self.report = None
        return True

    def text(self) -> str:
        return self.store.load(self.current)

    def save(self, text: str) -> None:
        self.store.save(self.current, text)

    @property
    def path(self) -> str:
        return str(self.store.path(self.current))

    # ---- building and testing ----------------------------------------------

    def library(self, text: str | None = None) -> ChipLibrary:
        level = self.current
        return self.store.library(level, text if text is not None else self.store.load(level))

    def loader(self) -> Loader:
        """Loader for the circuit view: the current level as last saved (or its stub)."""

        def load() -> tuple[str, ChipLibrary]:
            return self.current.name, self.library()

        return load

    def run_tests(self, text: str) -> TestReport:
        """Save `text`, then run the level's tests on it with the player's other chips.

        Saving first matters: later levels are built from the saved files, so a
        level must never count as solved with a version that isn't on disk.
        """
        level = self.current
        self.save(text)
        script = parse_tst(level.tst.read_text(), level.tst.name)
        result = run_script(script, self.library(text), level)
        report = _report(result)
        if result.passed:
            newly = level.name not in self.store.solved
            self.store.mark_solved(level)
            unlocked = [
                lv.name for lv in self.levels if newly and self.missing(lv) == [] and
                level.name in lv.parts and lv.name not in self.store.solved
            ]  # fmt: skip
            if unlocked:
                report.lines.append(f"Unlocked: {', '.join(unlocked)}")
        self.report = report
        return report


def _report(result: TstResult) -> TestReport:
    if result.error is not None:
        e = result.error
        where = f"line {e.pos.line}:{e.pos.col}: " if e.pos else ""
        return TestReport(False, "Doesn't build", [f"{where}{e.message}"])
    if result.passed:
        return TestReport(True, f"All {result.checks} checks passed", [])
    bad = len(result.failures)
    lines = [f"test line {f.pos.line}: {f.message}" for f in result.failures[:12]]
    if bad > 12:
        lines.append(f"... and {bad - 12} more")
    return TestReport(False, f"{bad} of {result.checks} checks failed", lines)
