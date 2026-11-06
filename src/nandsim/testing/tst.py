"""Parser for the `.tst` test format (see docs/tst.md).

A script names its chip, then lists steps. A `table` block is shorthand: each row
sets the inputs, evaluates, and checks the outputs.
"""

from __future__ import annotations

from dataclasses import dataclass

from nandsim.hdl import HdlError, SourcePos


@dataclass(frozen=True)
class Value:
    """A literal as written: decimal (possibly negative), 0b..., 0x..., or * (don't care)."""

    number: int | None
    base: int  # 2, 10 or 16; how to print actual values next to it
    text: str
    pos: SourcePos

    def encode(self, width: int, pin: str) -> int:
        """The unsigned bit pattern for a pin of `width` bits; negative uses two's complement."""
        assert self.number is not None
        v = self.number
        if v < 0:
            if v < -(1 << (width - 1)) or width == 1:
                raise HdlError(f"{self.text} does not fit in {width}-bit pin '{pin}'", self.pos)
            v += 1 << width
        elif v >= 1 << width:
            raise HdlError(f"{self.text} does not fit in {width}-bit pin '{pin}'", self.pos)
        return v


@dataclass(frozen=True)
class SetStep:
    pin: str
    value: Value
    pos: SourcePos


@dataclass(frozen=True)
class EvalStep:
    pos: SourcePos


@dataclass(frozen=True)
class ExpectStep:
    pin: str
    value: Value
    pos: SourcePos
    context: str = ""  # e.g. "a=1 b=0" for a table row


Step = SetStep | EvalStep | ExpectStep


@dataclass(frozen=True)
class TstScript:
    chip: str
    chip_pos: SourcePos
    steps: tuple[Step, ...]
    file: str


@dataclass(frozen=True)
class _Word:
    text: str
    pos: SourcePos


def _words(line: str, filename: str, lineno: int) -> list[_Word]:
    code = line.split("//", 1)[0]
    out: list[_Word] = []
    i = 0
    while i < len(code):
        if code[i].isspace():
            i += 1
            continue
        j = i
        while j < len(code) and not code[j].isspace():
            j += 1
        out.append(_Word(code[i:j], SourcePos(filename, lineno, i + 1)))
        i = j
    return out


def parse_value(w: _Word, allow_dont_care: bool) -> Value:
    t = w.text
    if t == "*":
        if not allow_dont_care:
            raise HdlError("'*' (don't care) is only allowed in expected values", w.pos)
        return Value(None, 10, t, w.pos)
    try:
        if t.lower().startswith(("0b", "-0b")):
            return Value(int(t, 2), 2, t, w.pos)
        if t.lower().startswith(("0x", "-0x")):
            return Value(int(t, 16), 16, t, w.pos)
        return Value(int(t, 10), 10, t, w.pos)
    except ValueError:
        raise HdlError(
            f"'{t}' is not a value: use decimal (5, -1), binary (0b101) or hex (0x1F)", w.pos
        ) from None


def parse_tst(text: str, filename: str = "<input>") -> TstScript:
    """Parse a `.tst` script. Raises `HdlError` at the first problem."""
    lines = text.splitlines()
    chip: _Word | None = None
    steps: list[Step] = []
    header: tuple[list[_Word], list[_Word]] | None = None
    table_pos: SourcePos | None = None

    for lineno, line in enumerate(lines, start=1):
        words = _words(line, filename, lineno)
        if not words:
            continue
        head = words[0]

        if header is not None:  # inside a table
            if head.text == "end":
                header = None
                continue
            ins, outs = header
            if "|" not in [w.text for w in words]:
                raise HdlError("table row needs '|' between inputs and outputs", head.pos)
            bar = [w.text for w in words].index("|")
            left, right = words[:bar], words[bar + 1 :]
            if len(left) != len(ins) or len(right) != len(outs):
                raise HdlError(
                    f"table row has {len(left)} input and {len(right)} output values; "
                    f"the header has {len(ins)} and {len(outs)}",
                    head.pos,
                )
            values = [parse_value(w, allow_dont_care=False) for w in left]
            context = " ".join(f"{p.text}={v.text}" for p, v in zip(ins, values, strict=True))
            for p, v in zip(ins, values, strict=True):
                steps.append(SetStep(p.text, v, v.pos))
            steps.append(EvalStep(head.pos))
            for p, w in zip(outs, right, strict=True):
                v = parse_value(w, allow_dont_care=True)
                steps.append(ExpectStep(p.text, v, v.pos, context))
            continue

        if chip is None and head.text != "chip":
            raise HdlError("a test must start with 'chip <Name>'", head.pos)
        cmd, args = head.text, words[1:]
        if cmd == "chip":
            if chip is not None:
                raise HdlError("'chip' can appear only once", head.pos)
            _arity(head, args, 1, "chip <Name>")
            chip = args[0]
        elif cmd == "table":
            texts = [w.text for w in args]
            if texts.count("|") != 1:
                raise HdlError("table header must be 'table <inputs> | <outputs>'", head.pos)
            bar = texts.index("|")
            header = (args[:bar], args[bar + 1 :])
            table_pos = head.pos
        elif cmd == "set":
            _arity(head, args, 2, "set <pin> <value>")
            steps.append(SetStep(args[0].text, parse_value(args[1], False), head.pos))
        elif cmd == "eval":
            _arity(head, args, 0, "eval")
            steps.append(EvalStep(head.pos))
        elif cmd == "expect":
            _arity(head, args, 2, "expect <pin> <value>")
            steps.append(ExpectStep(args[0].text, parse_value(args[1], True), head.pos))
        elif cmd in ("tick", "tock"):
            raise HdlError(
                f"'{cmd}' is for sequential chips, which arrive in milestone 6", head.pos
            )
        else:
            raise HdlError(
                f"unknown command '{cmd}' (expected chip, table, set, eval, expect)", head.pos
            )

    if header is not None:
        raise HdlError("table is never closed: missing 'end'", table_pos)
    if chip is None:
        raise HdlError("empty test: it must start with 'chip <Name>'", SourcePos(filename, 1, 1))
    return TstScript(chip.text, chip.pos, tuple(steps), filename)


def _arity(head: _Word, args: list[_Word], n: int, usage: str) -> None:
    if len(args) != n:
        raise HdlError(f"usage: {usage}", head.pos)
