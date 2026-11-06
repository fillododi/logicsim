"""The primitive table: chips implemented by the engine itself rather than in HDL.

Elaboration and the engine look primitives up here instead of hard-wiring Nand,
so DFF (milestone 6) and Python builtins can be added as new rows.
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
}
