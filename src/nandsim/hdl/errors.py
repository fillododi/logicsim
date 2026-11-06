"""Source positions and the error type shared by every stage that reads player HDL."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourcePos:
    """A 1-based line and column in a named source file."""

    file: str
    line: int
    col: int

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.col}"


class HdlError(Exception):
    """An error in HDL or .tst source, positioned so an editor can underline it."""

    def __init__(self, message: str, pos: SourcePos | None) -> None:
        super().__init__(message)
        self.message = message
        self.pos = pos

    def __str__(self) -> str:
        if self.pos is None:
            return f"error: {self.message}"
        return f"{self.pos}: error: {self.message}"
