"""Turns a level's brief (a small subset of Markdown) into wrapped display lines. No pygame.

Supported: `# title`, paragraphs, `**bold**` and `` `code` `` markers (dropped,
with the whole line shown bold if it starts bold), and pipe tables (shown as
aligned monospace rows, separator row omitted).
"""

from __future__ import annotations

import textwrap
from typing import Literal

LineKind = Literal["title", "text", "bold", "table", "blank"]
Line = tuple[str, LineKind]


def _plain(s: str) -> str:
    return s.replace("**", "").replace("`", "")


def brief_lines(md: str, cols: int) -> list[Line]:
    """Display lines for a brief, wrapped to `cols` characters."""
    out: list[Line] = []
    rows: list[list[str]] = []

    def flush_table() -> None:
        if not rows:
            return
        widths = [max(len(r[i]) for r in rows if i < len(r)) for i in range(len(rows[0]))]
        for r in rows:
            cells = [c.center(widths[i]) for i, c in enumerate(r)]
            out.append(("  ".join(cells)[:cols], "table"))
        rows.clear()

    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue  # separator row
            rows.append([_plain(c) for c in cells])
            continue
        flush_table()
        if not line:
            if out and out[-1][1] != "blank":
                out.append(("", "blank"))
        elif line.startswith("#"):
            out.append((_plain(line.lstrip("#").strip()), "title"))
        else:
            kind: LineKind = "bold" if line.startswith("**") else "text"
            for piece in textwrap.wrap(_plain(line), max(10, cols)) or [""]:
                out.append((piece, kind))
    flush_table()
    while out and out[-1][1] == "blank":
        out.pop()
    return out
