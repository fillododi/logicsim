"""The primitive table: chips implemented by the engine itself rather than in HDL.

Elaboration and the engine look primitives up here instead of hard-wiring them,
so Python builtins can be added as new rows. `Nand` is combinational; `DFF` is
sequential: levelization leaves it out, and the engine updates it on the clock.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Primitive:
    """A primitive chip's interface. Every pin of a primitive is one bit wide."""

    name: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    sequential: bool = False

    def pin_width(self, pin: str) -> int | None:
        return 1 if pin in self.inputs or pin in self.outputs else None


PRIMITIVES: dict[str, Primitive] = {
    "Nand": Primitive("Nand", inputs=("a", "b"), outputs=("out",)),
    "DFF": Primitive("DFF", inputs=("in",), outputs=("out",), sequential=True),
}
