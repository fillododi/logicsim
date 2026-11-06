"""Tokenizer for the HDL: identifiers, numbers, punctuation and comments."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from nandsim.hdl.errors import HdlError, SourcePos


class Kind(Enum):
    IDENT = "identifier"
    NUMBER = "number"
    PUNCT = "symbol"
    EOF = "end of file"


@dataclass(frozen=True)
class Token:
    kind: Kind
    text: str
    pos: SourcePos

    def describe(self) -> str:
        """How the token is named in error messages."""
        if self.kind is Kind.EOF:
            return "end of file"
        return f"'{self.text}'"


_PUNCT = ("..", "{", "}", "(", ")", "[", "]", ";", ",", "=", ":")


def tokenize(text: str, filename: str) -> list[Token]:
    """Split HDL source into tokens, skipping whitespace and comments."""
    tokens: list[Token] = []
    i, line, col = 0, 1, 1
    n = len(text)

    def advance(k: int) -> None:
        nonlocal i, line, col
        for _ in range(k):
            if text[i] == "\n":
                line, col = line + 1, 1
            else:
                col += 1
            i += 1

    while i < n:
        c = text[i]
        if c in " \t\r\n":
            advance(1)
        elif text.startswith("//", i):
            while i < n and text[i] != "\n":
                advance(1)
        elif text.startswith("/*", i):
            start = SourcePos(filename, line, col)
            end = text.find("*/", i + 2)
            if end < 0:
                raise HdlError("comment is never closed: missing '*/'", start)
            advance(end + 2 - i)
        elif c.isalpha() or c == "_":
            pos = SourcePos(filename, line, col)
            j = i
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            tokens.append(Token(Kind.IDENT, text[i:j], pos))
            advance(j - i)
        elif c.isdigit():
            pos = SourcePos(filename, line, col)
            j = i
            while j < n and text[j].isdigit():
                j += 1
            tokens.append(Token(Kind.NUMBER, text[i:j], pos))
            advance(j - i)
        else:
            pos = SourcePos(filename, line, col)
            for p in _PUNCT:
                if text.startswith(p, i):
                    tokens.append(Token(Kind.PUNCT, p, pos))
                    advance(len(p))
                    break
            else:
                raise HdlError(f"unexpected character '{c}'", pos)
    tokens.append(Token(Kind.EOF, "", SourcePos(filename, line, col)))
    return tokens
