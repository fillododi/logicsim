"""The guided tour: steps from `chips/tutorial.toml`, progress in `tutorial.json`. No pygame.

The tour is a list of steps shown one at a time. Each step points at a part of
the UI (its *anchor*) and is completed by a player action (its *until* event),
so the tour advances when the player does the thing a bubble explains. The game
reports actions with `Tour.event()`. A step with a `level` only shows, and only
listens, while that level is open.

Progress lives next to the saves as

    tutorial.json    {"version": 1, "seen": ["welcome", ...], "skipped": false}

so `progress.json` keeps its version. *Seen* holds completed steps: after a
restart the tour resumes at the first step not seen. *Skip* hides the tour, and
*replay* (F1) clears both.
"""

from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path

from nandsim.gui.saves import atomic_write
from nandsim.paths import data_root

TUTORIAL_VERSION = 1

# Anchors a step may point at. "kind:arg" anchors take an argument.
ANCHORS = frozenset(
    {
        "levels",
        "brief",
        "editor",
        "canvas",
        "part",
        "wire",
        "header",
        "run_button",
        "results",
        "footer",
        "chips",
        "clock",
    }
)
ANCHOR_KINDS = frozenset({"level", "line", "pin"})
# Player actions the game reports. open_level may name the level: "open_level:Not".
EVENTS = frozenset(
    {
        "next",
        "save",
        "build_ok",
        "toggle",
        "set_value",
        "open_part",
        "up",
        "run_tests",
        "solved",
        "open_level",
        "export",
        "clock_step",
    }
)


@dataclass(frozen=True)
class Step:
    id: str
    text: str
    anchor: str
    until: str
    level: str | None = None

    def listens_to(self, event: str, detail: str | None) -> bool:
        if event == "set_value" and self.until == "toggle":
            return True  # typing an input's value changes it as much as a click does
        return self.until == event or (detail is not None and self.until == f"{event}:{detail}")


def load_steps(path: Path | None = None, levels: set[str] | None = None) -> list[Step]:
    """Read and check the tour. Errors name the step, so a typo in the data is easy to find.

    With `levels`, the level names in `level`, `level:<Name>` and `open_level:<Name>`
    are checked too: a step tied to a level that doesn't exist would never show.
    """
    path = path or data_root() / "chips" / "tutorial.toml"
    with open(path, "rb") as f:
        data = tomllib.load(f)
    steps: list[Step] = []
    for i, e in enumerate(data.get("step", []), 1):
        sid = str(e.get("id", ""))
        where = f"{path.name}: step {i} ({sid or 'no id'})"
        if not sid:
            raise ValueError(f"{where}: missing 'id'")
        if any(s.id == sid for s in steps):
            raise ValueError(f"{where}: duplicate id '{sid}'")
        anchor, until = str(e.get("anchor", "")), str(e.get("until", ""))
        kind, _, arg = anchor.partition(":")
        known = levels if levels is not None else None
        if not (anchor in ANCHORS or (kind in ANCHOR_KINDS and arg)) or (
            kind == "level" and known is not None and arg not in known
        ):
            raise ValueError(f"{where}: unknown anchor '{anchor}'")
        event, _, detail = until.partition(":")
        if (
            event not in EVENTS
            or (detail and event != "open_level")
            or (detail and known is not None and detail not in known)
        ):
            raise ValueError(f"{where}: unknown 'until' event '{until}'")
        text = str(e.get("text", "")).strip()
        if not text:
            raise ValueError(f"{where}: empty text")
        level = str(e["level"]) if e.get("level") else None
        if level is not None and known is not None and level not in known:
            raise ValueError(f"{where}: unknown level '{level}'")
        steps.append(Step(sid, text, anchor, until, level))
    return steps


class Tour:
    def __init__(self, steps: list[Step], path: Path) -> None:
        self.steps = steps
        self.path = path
        self.warning: str | None = None
        self.seen, self.skipped = self._read()
        # Actions no step was waiting for, as (level, event, detail), so a step whose
        # action already happened completes as soon as it comes up. Not saved: a
        # restart or a replay starts clean.
        self._done: set[tuple[str, str, str | None]] = set()

    # ---- state -----------------------------------------------------------

    @property
    def current(self) -> Step | None:
        """The first step not completed yet, or None when the tour is finished or skipped."""
        if self.skipped:
            return None
        return next((s for s in self.steps if s.id not in self.seen), None)

    def visible(self, level: str) -> Step | None:
        """The step to show while `level` is open: the first unseen one for it or for any level.

        Steps tied to other levels wait, but they don't hold up this level's steps, so a
        player who leaves the tutorial early still gets the bubbles of the level they are in.
        """
        if self.skipped:
            return None
        return next(
            (s for s in self.steps if s.id not in self.seen and s.level in (None, level)), None
        )

    def position(self, step: Step) -> tuple[int, int]:
        """(1-based index, total), for the "3 / 13" counter."""
        return self.steps.index(step) + 1, len(self.steps)

    # ---- actions ---------------------------------------------------------

    def event(self, level: str, name: str, detail: str | None = None) -> bool:
        """The player did `name` while `level` was open. True if that completed a step."""
        step = self.visible(level)
        if step is None or not step.listens_to(name, detail):
            self._done.add((level, name, detail))
            return False
        self.seen.add(step.id)
        self.catch_up(level)
        self._write()
        return True

    def catch_up(self, level: str) -> None:
        """Complete the steps now showing whose action the player already did on `level`."""
        while (step := self.visible(level)) is not None and any(
            lv == level and step.listens_to(name, detail) for lv, name, detail in self._done
        ):
            self.seen.add(step.id)

    def skip(self) -> None:
        self.skipped = True
        self._write()

    def replay(self) -> None:
        self.seen.clear()
        self._done.clear()
        self.skipped = False
        self._write()

    # ---- file ------------------------------------------------------------

    def _read(self) -> tuple[set[str], bool]:
        if not self.path.is_file():
            return set(), False
        try:
            text = self.path.read_text()
        except OSError as e:
            self.warning = f"tutorial file couldn't be read ({e}); the tour starts over"
            return set(), False
        try:
            data = json.loads(text)
            if data.get("version") != TUTORIAL_VERSION:
                raise ValueError(f"unknown version {data.get('version')!r}")
            return {str(s) for s in data["seen"]}, bool(data.get("skipped", False))
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            backup = self.path.with_suffix(".json.bad")
            self.path.replace(backup)
            self.warning = f"tutorial file was unreadable ({e}); kept a copy as {backup.name}"
            return set(), False

    def _write(self) -> None:
        order = {s.id: i for i, s in enumerate(self.steps)}
        seen = sorted(self.seen, key=lambda s: (order.get(s, len(order)), s))
        data = {"version": TUTORIAL_VERSION, "seen": seen, "skipped": self.skipped}
        atomic_write(self.path, json.dumps(data, indent=2) + "\n")


# ---- layout helpers (plain tuples, so they are testable without pygame) --------

Box = tuple[int, int, int, int]  # x, y, w, h


def paragraphs(text: str) -> list[tuple[str, bool]]:
    """Split step text into (paragraph, is_code) blocks.

    Blank lines separate paragraphs, lines inside a paragraph are joined with
    spaces, and lines indented by four spaces form a code block. Consecutive code
    lines stay one block, joined with newlines, so they are drawn without a gap.
    """
    blocks: list[tuple[str, bool]] = []
    para: list[str] = []
    code: list[str] = []

    def flush() -> None:
        if para:
            blocks.append((" ".join(para), False))
            para.clear()
        if code:
            blocks.append(("\n".join(code), True))
            code.clear()

    for line in text.splitlines():
        if line.startswith("    ") and line.strip():
            if para:
                flush()
            code.append(line.strip())
        elif not line.strip():
            flush()
        else:
            if code:
                flush()
            para.append(line.strip())
    flush()
    return blocks


def place_bubble(anchor: Box | None, size: tuple[int, int], bounds: Box, gap: int = 14) -> Box:
    """Where to draw a bubble of `size` so it sits next to `anchor` without covering it.

    Tries right, left, below and above the anchor, and takes the first spot that
    fits inside `bounds`, sliding along the anchor's side if needed. If none fits, it
    takes the one that covers the least of the anchor once clamped into `bounds`.
    With no anchor, the bubble is centred.
    """
    w, h = size
    bx, by, bw, bh = bounds

    def clamp(x: int, y: int) -> Box:
        return (max(bx, min(x, bx + bw - w)), max(by, min(y, by + bh - h)), w, h)

    if anchor is None:
        return clamp(bx + (bw - w) // 2, by + (bh - h) // 2)
    ax, ay, aw, ah = anchor
    mid_y = ay + ah // 2 - h // 2
    mid_x = ax + aw // 2 - w // 2
    candidates = [
        (ax + aw + gap, mid_y),
        (ax - gap - w, mid_y),
        (mid_x, ay + ah + gap),
        (mid_x, ay - gap - h),
    ]
    # A spot beside the anchor only has to fit across (it slides up or down to stay in
    # the window); a spot above or below only has to fit vertically.
    for i, (x, y) in enumerate(candidates):
        fits = bx <= x and x + w <= bx + bw if i < 2 else by <= y and y + h <= by + bh
        if fits and h <= bh and w <= bw:
            return clamp(x, y)
    return min((clamp(x, y) for x, y in candidates), key=lambda b: _overlap(b, anchor))


def _overlap(a: Box, b: Box) -> int:
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return max(0, w) * max(0, h)
