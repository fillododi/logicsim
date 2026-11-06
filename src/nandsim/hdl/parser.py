"""Recursive-descent parser: HDL source text to a `ChipDef`."""

from __future__ import annotations

from nandsim.hdl.ast import Assign, ChipDef, Connection, Const, Part, PinDecl, PinRef
from nandsim.hdl.errors import HdlError, SourcePos
from nandsim.hdl.lexer import Kind, Token, tokenize

KEYWORDS = {"CHIP", "IN", "OUT", "PARTS", "true", "false"}


class _Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    @property
    def tok(self) -> Token:
        return self.tokens[self.i]

    def next(self) -> Token:
        t = self.tokens[self.i]
        if t.kind is not Kind.EOF:
            self.i += 1
        return t

    def at(self, text: str) -> bool:
        return self.tok.kind in (Kind.PUNCT, Kind.IDENT) and self.tok.text == text

    def expect(self, text: str, what: str | None = None) -> Token:
        if not self.at(text):
            raise HdlError(
                f"expected {what or repr(text)}, found {self.tok.describe()}", self.tok.pos
            )
        return self.next()

    def ident(self, what: str) -> Token:
        t = self.tok
        if t.kind is not Kind.IDENT or t.text in KEYWORDS:
            raise HdlError(f"expected {what}, found {t.describe()}", t.pos)
        return self.next()

    def number(self, what: str) -> int:
        t = self.tok
        if t.kind is not Kind.NUMBER:
            raise HdlError(f"expected {what}, found {t.describe()}", t.pos)
        self.next()
        return int(t.text)

    # CHIP Name { IN ...; OUT ...; PARTS: ... }
    def chip(self) -> ChipDef:
        start = self.expect("CHIP", "'CHIP'")
        name = self.ident("a chip name").text
        self.expect("{")
        inputs: list[PinDecl] = []
        outputs: list[PinDecl] = []
        seen: dict[str, PinDecl] = {}
        if self.at("IN"):
            self.next()
            inputs = self.pin_decls(seen)
        if self.at("OUT"):
            self.next()
            outputs = self.pin_decls(seen)
        self.expect("PARTS", "'PARTS:'")
        self.expect(":")
        parts: list[Part] = []
        assigns: list[Assign] = []
        while not self.at("}"):
            if self.tok.kind is Kind.EOF:
                raise HdlError("expected '}' to close the chip, found end of file", self.tok.pos)
            stmt = self.statement()
            if isinstance(stmt, Part):
                parts.append(stmt)
            else:
                assigns.append(stmt)
        self.next()
        if self.tok.kind is not Kind.EOF:
            raise HdlError(
                f"unexpected {self.tok.describe()} after the end of the chip", self.tok.pos
            )
        return ChipDef(name, tuple(inputs), tuple(outputs), tuple(parts), start.pos, tuple(assigns))

    def pin_decls(self, seen: dict[str, PinDecl]) -> list[PinDecl]:
        decls: list[PinDecl] = []
        while True:
            t = self.ident("a pin name")
            width = 1
            if self.at("["):
                self.next()
                wpos = self.tok.pos
                width = self.number("a bus width")
                if width < 1:
                    raise HdlError(f"bus '{t.text}' must be at least 1 bit wide", wpos)
                self.expect("]")
            if t.text in seen:
                first = seen[t.text].pos
                raise HdlError(f"pin '{t.text}' is already declared at line {first.line}", t.pos)
            d = PinDecl(t.text, width, t.pos)
            seen[t.text] = d
            decls.append(d)
            if self.at(","):
                self.next()
                continue
            self.expect(";", "',' or ';'")
            return decls

    def statement(self) -> Part | Assign:
        """A part (`Nand(...)`), a labelled part (`g1: Nand(...)`) or an assignment (`out = a`)."""
        t = self.ident("a part name")
        if self.at(":"):
            self.next()
            return self.part(self.ident("a part name after the label"), t)
        if self.at("("):
            return self.part(t, None)
        if self.at("=") or self.at("[") or self.at("."):
            self.i -= 1  # re-read the name as the assignment's target
            target = self.pin_ref(allow_const=False)
            assert isinstance(target, PinRef)
            self.expect("=")
            source = self.pin_ref(allow_const=True)
            self.expect(";")
            return Assign(target, source, t.pos)
        raise HdlError(
            f"expected '(' for a part, ':' after a label, or '=' to connect, "
            f"found {self.tok.describe()}",
            self.tok.pos,
        )

    def part(self, t: Token, label: Token | None) -> Part:
        self.expect("(")
        conns: list[Connection] = []
        if not self.at(")"):
            while True:
                conns.append(self.connection())
                if self.at(","):
                    self.next()
                    continue
                break
        self.expect(")", "',' or ')'")
        self.expect(";")
        if label is None:
            return Part(t.text, tuple(conns), t.pos)
        return Part(t.text, tuple(conns), t.pos, label.text, label.pos)

    def connection(self) -> Connection:
        inner = self.pin_ref(allow_const=False, allow_part=False)
        assert isinstance(inner, PinRef)
        self.expect("=")
        outer = self.pin_ref(allow_const=True)
        return Connection(inner, outer, inner.pos)

    def pin_ref(self, allow_const: bool, allow_part: bool = True) -> PinRef | Const:
        t = self.tok
        if allow_const and t.kind is Kind.IDENT and t.text in ("true", "false"):
            self.next()
            return Const(t.text == "true", t.pos)
        name = self.ident("a pin name")
        part: str | None = None
        if allow_part and self.at("."):
            self.next()
            part, name = name.text, self.ident(f"an output pin of '{name.text}'")
            name = Token(name.kind, name.text, t.pos)
        if not self.at("["):
            return PinRef(name.text, None, None, name.pos, part)
        self.next()
        lo = self.number("a bit index")
        hi = lo
        if self.at(".."):
            self.next()
            hpos = self.tok.pos
            hi = self.number("a bit index")
            if hi < lo:
                raise HdlError(
                    f"slice {name.text}[{lo}..{hi}] is reversed: write [{hi}..{lo}]", hpos
                )
        self.expect("]")
        return PinRef(name.text, lo, hi, name.pos, part)


def parse(text: str, filename: str = "<input>") -> ChipDef:
    """Parse one chip definition. Raises `HdlError` at the first problem."""
    return _Parser(tokenize(text, filename)).chip()


__all__ = ["parse", "SourcePos"]
