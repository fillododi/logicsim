# Hello

Your first chip that computes something behaves exactly like a Nand: its output is 0 only when both inputs are 1.

| a | b | out |
|---|---|---|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

A connection only passes a signal along. To compute, a chip needs parts: other chips used inside it. A part is written as `Chip(pin=signal, ...)`. Each `pin=signal` works like a connection: the name on the left of `=` is the part's own pin, and the one on the right is a signal in your chip.

**Parts you may use:** Nand.

**Hint:** One Nand is enough. Connect its `a`, `b` and `out` to the chip's pins with the same names.
