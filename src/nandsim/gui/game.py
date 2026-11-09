"""Game rules for the GUI: which level is open, its status, building and testing it. No pygame.

The player's own chips (in the save dir) are the only implementations the game
ever uses; the hidden reference solutions are never loaded here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from nandsim.gui.saves import SaveStore
from nandsim.gui.session import Loader
from nandsim.gui.tips import tip_for
from nandsim.netlist import FREE_PRIMITIVES, ChipLibrary
from nandsim.testing import Level, TstResult, parse_tst, run_script

Status = Literal["solved", "open", "locked"]


@dataclass
class TestReport:
    """What the results panel shows after "Run tests"."""

    passed: bool
    summary: str
    lines: list[str]
    newly_solved: bool = False  # passed for the first time: the level just got solved


class GameState:
    def __init__(self, store: SaveStore) -> None:
        self.store = store
        self.levels = store.levels
        self.current: Level = self._first_level()
        self.report: TestReport | None = None

    def _first_level(self) -> Level:
        """The first open level past the furthest solved one; else any open level; else the first.

        Looking past the furthest solved level means a player who skipped the
        tutorial isn't sent back to it every time they start the game.
        """
        solved = [i for i, lv in enumerate(self.levels) if self.status(lv) == "solved"]
        start = solved[-1] + 1 if solved else 0
        for lv in self.levels[start:] + self.levels[:start]:
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
        needed = [p for p in level.parts if p not in FREE_PRIMITIVES]
        needed += [r for r in level.requires if r not in needed]
        return [p for p in needed if p not in self.store.solved]

    # ---- level groups -------------------------------------------------------

    def groups(self) -> list[tuple[str, list[Level]]]:
        """The levels by group (`01_gates`, ...), in the order of `levels.toml`."""
        out: list[tuple[str, list[Level]]] = []
        for lv in self.levels:
            if not out or out[-1][0] != lv.group:
                out.append((lv.group, []))
            out[-1][1].append(lv)
        return out

    def default_expanded(self) -> set[str]:
        """Groups the sidebar opens: the current level's, and the next one with an open level.

        At most two groups are open, so the list stays short, and the next thing to
        do is always in sight: Not while the player is in the tutorial, the first
        bus level once Gates is under way.
        """
        groups = self.groups()
        names = [g for g, _ in groups]
        mine = self.current.group
        later = groups[names.index(mine) + 1 :]
        nxt = next((g for g, lvs in later if any(self.status(lv) == "open" for lv in lvs)), None)
        return {mine} | ({nxt} if nxt else set())

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
        result = run_script(
            script,
            self.library(text),
            level,
            exported=self.store.exported(),
            base=level.tst.parent,
        )
        report = _report(result)
        if result.passed:
            newly = level.name not in self.store.solved
            report.newly_solved = newly
            self.store.mark_solved(level)
            unlocked = [
                lv.name for lv in self.levels if newly and self.missing(lv) == [] and
                level.name in lv.parts and lv.name not in self.store.solved
            ]  # fmt: skip
            if unlocked:
                report.lines.append(f"Unlocked: {', '.join(unlocked)}")
        self.report = report
        return report


# Groups whose folder name is shortened: `03_arith` reads better as "Arithmetic".
_GROUP_LABELS = {
    "03_arith": "Arithmetic",
    "04_seq": "Memory",
    "05_cpu": "CPU",
    "06_computer": "Computer",
}


def group_label(group: str) -> str:
    """What the sidebar calls a group: `01_gates` is "Gates", `00_tutorial` "Tutorial"."""
    if group in _GROUP_LABELS:
        return _GROUP_LABELS[group]
    return group.split("_", 1)[-1].replace("_", " ").title()


def _report(result: TstResult) -> TestReport:
    if result.error is not None:
        e = result.error
        where = f"line {e.pos.line}:{e.pos.col}: " if e.pos else ""
        tip = tip_for(e.message)
        return TestReport(
            False, "Doesn't build", [f"{where}{e.message}"] + ([f"Tip: {tip}"] if tip else [])
        )
    if result.passed:
        return TestReport(True, f"All {result.checks} checks passed", [])
    bad = len(result.failures)
    lines = [f"test line {f.pos.line}: {f.message}" for f in result.failures[:12]]
    if bad > 12:
        lines.append(f"... and {bad - 12} more")
    tip = next((t for f in result.failures if (t := tip_for(f.message))), None)
    if tip:
        lines.append(f"Tip: {tip}")
    return TestReport(False, f"{bad} of {result.checks} checks failed", lines)
