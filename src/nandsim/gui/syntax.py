"""Syntax colouring for HDL in the editor. Pure Python, no pygame.

Lenient on purpose: half-typed code must still colour sensibly, so this is a
small per-line scanner, not the real lexer (which stops at the first error).
"""

from __future__ import annotations

from typing import Literal

Kind = Literal["plain", "comment", "keyword", "constant", "number", "chip", "punct"]
Span = tuple[int, int, Kind]  # [start, end) columns

KEYWORDS = {"CHIP", "IN", "OUT", "PARTS"}
CONSTANTS = {"true", "false"}


def highlight(lines: list[str]) -> list[list[Span]]:
    """Spans for each line. Block comments may span lines."""
    result: list[list[Span]] = []
    in_block = False
    for line in lines:
        spans: list[Span] = []
        i, n = 0, len(line)
        while i < n:
            if in_block:
                end = line.find("*/", i)
                stop = n if end < 0 else end + 2
                spans.append((i, stop, "comment"))
                in_block = end < 0
                i = stop
                continue
            c = line[i]
            if line.startswith("//", i):
                spans.append((i, n, "comment"))
                break
            if line.startswith("/*", i):
                in_block = True
                spans.append((i, i + 2, "comment"))
                i += 2
                continue
            if c.isalpha() or c == "_":
                j = i
                while j < n and (line[j].isalnum() or line[j] == "_"):
                    j += 1
                word = line[i:j]
                k = j
                while k < n and line[k] == " ":
                    k += 1
                if word in KEYWORDS:
                    kind: Kind = "keyword"
                elif word in CONSTANTS:
                    kind = "constant"
                elif k < n and line[k] == "(":
                    kind = "chip"
                else:
                    kind = "plain"
                spans.append((i, j, kind))
                i = j
                continue
            if c.isdigit():
                j = i
                while j < n and line[j].isdigit():
                    j += 1
                spans.append((i, j, "number"))
                i = j
                continue
            if not c.isspace():
                spans.append((i, i + 1, "punct"))
            i += 1
        result.append(_merge(spans))
    return result


def _merge(spans: list[Span]) -> list[Span]:
    """Merge a block comment's pieces on one line into a single span."""
    out: list[Span] = []
    for s in spans:
        if out and out[-1][2] == s[2] == "comment" and out[-1][1] == s[0]:
            out[-1] = (out[-1][0], s[1], "comment")
        else:
            out.append(s)
    return out


def token_end(line: str, col: int) -> int:
    """End column of the token starting at `col`, for underlining an error."""
    n = len(line)
    if col >= n:
        return col + 1
    if line[col].isalnum() or line[col] == "_":
        j = col
        while j < n and (line[j].isalnum() or line[j] == "_"):
            j += 1
        return j
    return col + 1
