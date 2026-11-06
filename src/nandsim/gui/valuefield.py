"""The value field: a value the player types for an input pin on the canvas. No pygame.

Clicking a bus input only counts up or down by one, which is far too slow for a 12-bit
pin. The field takes a value written as in a `.tst` file (`13`, `-1`, `0b1101`, `0x0D`)
and checks it with the same rules and messages.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from nandsim.hdl import HdlError
from nandsim.testing import parse_pin_value

ALLOWED = re.compile(r"[0-9a-fA-FxXbB-]")  # every character a value can contain
MAX_LEN = 24  # enough for a 16-bit binary value with its 0b


@dataclass
class ValueField:
    pin: str
    width: int
    text: str = ""
    error: str = ""

    def type(self, chars: str) -> None:
        """Add typed characters, dropping any a value can't contain."""
        keep = "".join(c for c in chars if ALLOWED.fullmatch(c))
        self.text = (self.text + keep)[:MAX_LEN]
        self.error = ""

    def backspace(self, everything: bool = False) -> None:
        self.text = "" if everything else self.text[:-1]
        self.error = ""

    @property
    def empty(self) -> bool:
        return not self.text.strip()

    def value(self) -> int | None:
        """The typed value as the pin's bit pattern, or None with `error` saying why."""
        try:
            return parse_pin_value(self.text, self.width, self.pin)
        except HdlError as e:
            self.error = e.message
            return None

    @property
    def hint(self) -> str:
        """The line under the field: the error, or how to write a value."""
        return self.error or "e.g. 13, 0xD, 0b1101 · Enter: set · Esc: cancel"
