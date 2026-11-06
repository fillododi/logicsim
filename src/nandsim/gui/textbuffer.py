"""The editor's text model: lines, cursor, selection, undo. Pure Python, no pygame.

Positions are 0-based (line, col). HDL errors use 1-based line:col; convert at
the boundary with `Pos.from_source`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

INDENT = "    "
COMMENT = "// "

Move = Literal[
    "left",
    "right",
    "up",
    "down",
    "home",
    "end",
    "word_left",
    "word_right",
    "doc_start",
    "doc_end",
    "page_up",
    "page_down",
]


@dataclass(frozen=True, order=True)
class Pos:
    line: int
    col: int

    @staticmethod
    def from_source(line: int, col: int) -> Pos:
        return Pos(line - 1, col - 1)


@dataclass(frozen=True)
class _State:
    lines: tuple[str, ...]
    cursor: Pos
    anchor: Pos | None


def _is_word(c: str) -> bool:
    return c.isalnum() or c == "_"


class TextBuffer:
    def __init__(self, text: str = "") -> None:
        self.lines: list[str] = text.split("\n")
        self.cursor = Pos(0, 0)
        self.anchor: Pos | None = None  # selection is anchor..cursor when set
        self.goal_col: int | None = None  # column kept while moving up/down
        self.page_lines = 20
        self._undo: list[_State] = []
        self._redo: list[_State] = []
        self._coalesce: str | None = None  # kind of the last edit, to merge typing
        self._saved = self.text

    # ---- text --------------------------------------------------------------

    @property
    def text(self) -> str:
        return "\n".join(self.lines)

    def set_text(self, text: str) -> None:
        """Replace everything (e.g. reloaded from disk). Clears history; marks saved."""
        self.lines = text.split("\n")
        self.cursor = self._clamp(self.cursor)
        self.anchor = None
        self._undo.clear()
        self._redo.clear()
        self._coalesce = None
        self._saved = text

    @property
    def dirty(self) -> bool:
        return self.text != self._saved

    def mark_saved(self) -> None:
        self._saved = self.text

    # ---- selection ----------------------------------------------------------

    def selection(self) -> tuple[Pos, Pos] | None:
        if self.anchor is None or self.anchor == self.cursor:
            return None
        return (min(self.anchor, self.cursor), max(self.anchor, self.cursor))

    def selected_text(self) -> str:
        sel = self.selection()
        return "" if sel is None else self._slice(*sel)

    def select_all(self) -> None:
        self.anchor = Pos(0, 0)
        self.cursor = Pos(len(self.lines) - 1, len(self.lines[-1]))

    def select_word_at(self, pos: Pos) -> None:
        pos = self._clamp(pos)
        line = self.lines[pos.line]
        start = end = pos.col
        while start > 0 and _is_word(line[start - 1]):
            start -= 1
        while end < len(line) and _is_word(line[end]):
            end += 1
        self.anchor = Pos(pos.line, start)
        self.cursor = Pos(pos.line, end)

    def set_cursor(self, pos: Pos, select: bool = False) -> None:
        self._begin_move(select)
        self.cursor = self._clamp(pos)
        self.goal_col = None

    # ---- editing ------------------------------------------------------------

    def insert(self, text: str) -> None:
        """Type or paste `text`, replacing the selection. Single characters merge into one undo."""
        kind = "type" if len(text) == 1 and text not in "\n " and self.selection() is None else None
        self._edit(kind)
        self._delete_selection()
        self.cursor = self._replace(self.cursor, self.cursor, text)

    def newline(self) -> None:
        """Enter: keep the current indentation, one level more after an opening brace."""
        self._edit(None)
        self._delete_selection()
        line = self.lines[self.cursor.line]
        indent = line[: len(line) - len(line.lstrip(" \t"))]
        before = line[: self.cursor.col].rstrip()
        after = line[self.cursor.col :].lstrip()
        if before.endswith(("{", "(")):
            inner = indent + INDENT
            if after.startswith(("}", ")")):  # Enter between braces: open a block
                self.cursor = self._replace(
                    self.cursor, Pos(self.cursor.line, len(line) - len(after)),
                    "\n" + inner + "\n" + indent,
                )  # fmt: skip
                self.cursor = Pos(self.cursor.line - 1, len(inner))
                return
            indent = inner
        self.cursor = self._replace(
            self.cursor, Pos(self.cursor.line, len(line) - len(after)), "\n" + indent
        )

    def type_char(self, ch: str) -> None:
        """Insert one typed character; a closing brace on a blank line dedents itself."""
        line = self.lines[self.cursor.line]
        if ch in "})" and self.selection() is None and line.strip() == "" and line.endswith(INDENT):
            self._edit(None)
            self.lines[self.cursor.line] = line[: -len(INDENT)]
            self.cursor = Pos(self.cursor.line, self.cursor.col - len(INDENT))
        self.insert(ch)

    def backspace(self) -> None:
        if self.selection() is not None:
            self._edit(None)
            self._delete_selection()
            return
        c = self.cursor
        if c == Pos(0, 0):
            return
        self._edit("backspace")
        line = self.lines[c.line]
        if c.col > 0 and line[: c.col].strip() == "" and c.col % len(INDENT) == 0:
            start = Pos(c.line, c.col - len(INDENT))  # in leading indentation: one level
        elif c.col > 0:
            start = Pos(c.line, c.col - 1)
        else:
            start = Pos(c.line - 1, len(self.lines[c.line - 1]))
        self.cursor = self._replace(start, c, "")

    def delete(self) -> None:
        if self.selection() is not None:
            self._edit(None)
            self._delete_selection()
            return
        c = self.cursor
        if c.col < len(self.lines[c.line]):
            end = Pos(c.line, c.col + 1)
        elif c.line + 1 < len(self.lines):
            end = Pos(c.line + 1, 0)
        else:
            return
        self._edit("delete")
        self._replace(c, end, "")

    def cut(self) -> str:
        text = self.selected_text()
        if text:
            self._edit(None)
            self._delete_selection()
        return text

    def indent(self) -> None:
        """Tab: indent selected lines, or insert spaces up to the next tab stop."""
        sel = self.selection()
        if sel is None:
            self.insert(" " * (len(INDENT) - self.cursor.col % len(INDENT)))
            return
        self._edit(None)
        first, last = self._selected_lines(sel)
        for i in range(first, last + 1):
            if self.lines[i].strip():
                self.lines[i] = INDENT + self.lines[i]
        self._shift_selection(first, last, len(INDENT))

    def dedent(self) -> None:
        sel = self.selection() or (self.cursor, self.cursor)
        self._edit(None)
        first, last = self._selected_lines(sel)
        removed: dict[int, int] = {}
        for i in range(first, last + 1):
            line = self.lines[i]
            n = len(line) - len(line.lstrip(" "))
            k = min(n, len(INDENT))
            self.lines[i] = line[k:]
            removed[i] = k
        self.cursor = Pos(self.cursor.line, max(0, self.cursor.col - removed[self.cursor.line]))
        if self.anchor is not None:
            self.anchor = Pos(
                self.anchor.line, max(0, self.anchor.col - removed.get(self.anchor.line, 0))
            )

    def toggle_comment(self) -> None:
        """Ctrl+/: comment the selected lines out with `//`, or back in if all are commented."""
        sel = self.selection() or (self.cursor, self.cursor)
        self._edit(None)
        first, last = self._selected_lines(sel)
        rows = [i for i in range(first, last + 1) if self.lines[i].strip()]
        if not rows:
            return
        commented = all(self.lines[i].lstrip().startswith("//") for i in rows)
        col = min(len(self.lines[i]) - len(self.lines[i].lstrip()) for i in rows)
        for i in rows:
            line = self.lines[i]
            if commented:
                j = line.index("//")
                k = 3 if line[j : j + 3] == COMMENT else 2
                self.lines[i] = line[:j] + line[j + k :]
            else:
                self.lines[i] = line[:col] + COMMENT + line[col:]
        self.cursor = self._clamp(self.cursor)
        if self.anchor is not None:
            self.anchor = self._clamp(self.anchor)

    # ---- movement ------------------------------------------------------------

    def move(self, how: Move, select: bool = False) -> None:
        sel = self.selection()
        self._begin_move(select)
        self._coalesce = None
        c = self.cursor
        if how in ("left", "right") and sel is not None and not select:
            self.cursor = sel[0] if how == "left" else sel[1]  # collapse the selection
            self.goal_col = None
            return
        if how in ("up", "down", "page_up", "page_down"):
            goal = self.goal_col if self.goal_col is not None else c.col
            step = {"up": -1, "down": 1, "page_up": -self.page_lines, "page_down": self.page_lines}
            line = max(0, min(len(self.lines) - 1, c.line + step[how]))
            if line == c.line and how in ("up", "page_up"):
                self.cursor = Pos(line, 0)
            elif line == c.line:
                self.cursor = Pos(line, len(self.lines[line]))
            else:
                self.cursor = Pos(line, min(goal, len(self.lines[line])))
            self.goal_col = goal
            return
        self.goal_col = None
        line = self.lines[c.line]
        if how == "left":
            self.cursor = (
                Pos(c.line, c.col - 1)
                if c.col > 0
                else (Pos(c.line - 1, len(self.lines[c.line - 1])) if c.line > 0 else c)
            )
        elif how == "right":
            self.cursor = (
                Pos(c.line, c.col + 1)
                if c.col < len(line)
                else (Pos(c.line + 1, 0) if c.line + 1 < len(self.lines) else c)
            )
        elif how == "home":  # smart home: first non-blank, then column 0
            first = len(line) - len(line.lstrip())
            self.cursor = Pos(c.line, 0 if c.col == first else first)
        elif how == "end":
            self.cursor = Pos(c.line, len(line))
        elif how == "doc_start":
            self.cursor = Pos(0, 0)
        elif how == "doc_end":
            self.cursor = Pos(len(self.lines) - 1, len(self.lines[-1]))
        elif how == "word_left":
            self.cursor = self._word_left(c)
        elif how == "word_right":
            self.cursor = self._word_right(c)

    # ---- undo ------------------------------------------------------------------

    def undo(self) -> None:
        if self._undo:
            self._redo.append(self._state())
            self._restore(self._undo.pop())

    def redo(self) -> None:
        if self._redo:
            self._undo.append(self._state())
            self._restore(self._redo.pop())

    # ---- internals ------------------------------------------------------------

    def _state(self) -> _State:
        return _State(tuple(self.lines), self.cursor, self.anchor)

    def _restore(self, s: _State) -> None:
        self.lines = list(s.lines)
        self.cursor, self.anchor = s.cursor, s.anchor
        self._coalesce = None

    def _edit(self, kind: str | None) -> None:
        """Record an undo point unless this edit continues the previous one of the same kind."""
        if kind is None or kind != self._coalesce:
            self._undo.append(self._state())
            if len(self._undo) > 500:
                del self._undo[0]
        self._redo.clear()
        self._coalesce = kind
        self.goal_col = None

    def _begin_move(self, select: bool) -> None:
        if select:
            if self.anchor is None:
                self.anchor = self.cursor
        else:
            self.anchor = None

    def _delete_selection(self) -> None:
        sel = self.selection()
        if sel is not None:
            self.cursor = self._replace(sel[0], sel[1], "")
        self.anchor = None

    def _replace(self, start: Pos, end: Pos, text: str) -> Pos:
        """Replace start..end with text; return the position right after the new text."""
        head = self.lines[start.line][: start.col]
        tail = self.lines[end.line][end.col :]
        new = (head + text + tail).split("\n")
        self.lines[start.line : end.line + 1] = new
        last = start.line + len(new) - 1
        return Pos(last, len(new[-1]) - len(tail))

    def _slice(self, start: Pos, end: Pos) -> str:
        if start.line == end.line:
            return self.lines[start.line][start.col : end.col]
        parts = [self.lines[start.line][start.col :]]
        parts += self.lines[start.line + 1 : end.line]
        parts.append(self.lines[end.line][: end.col])
        return "\n".join(parts)

    def _clamp(self, p: Pos) -> Pos:
        line = max(0, min(len(self.lines) - 1, p.line))
        return Pos(line, max(0, min(len(self.lines[line]), p.col)))

    def _selected_lines(self, sel: tuple[Pos, Pos]) -> tuple[int, int]:
        start, end = sel
        last = end.line - 1 if end.col == 0 and end.line > start.line else end.line
        return start.line, last

    def _shift_selection(self, first: int, last: int, delta: int) -> None:
        def shift(p: Pos) -> Pos:
            if first <= p.line <= last and self.lines[p.line].strip() and p.col > 0:
                return Pos(p.line, p.col + delta)
            return p

        self.cursor = shift(self.cursor)
        if self.anchor is not None:
            self.anchor = shift(self.anchor)

    def _word_left(self, c: Pos) -> Pos:
        if c.col == 0:
            return Pos(c.line - 1, len(self.lines[c.line - 1])) if c.line > 0 else c
        line, i = self.lines[c.line], c.col
        while i > 0 and line[i - 1].isspace():
            i -= 1
        if i > 0 and _is_word(line[i - 1]):
            while i > 0 and _is_word(line[i - 1]):
                i -= 1
        elif i > 0:
            i -= 1
        return Pos(c.line, i)

    def _word_right(self, c: Pos) -> Pos:
        """Skip whitespace, then to the end of the next word (or past one symbol)."""
        line, i = self.lines[c.line], c.col
        if i == len(line):
            return Pos(c.line + 1, 0) if c.line + 1 < len(self.lines) else c
        while i < len(line) and line[i].isspace():
            i += 1
        if i < len(line) and _is_word(line[i]):
            while i < len(line) and _is_word(line[i]):
                i += 1
        elif i < len(line):
            i += 1
        return Pos(c.line, i)
