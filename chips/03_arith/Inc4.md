# Inc4

Adds 1: `out = in + 1`, and 15 wraps around to 0. The 4004 counts this way with `INC`
on a register, and with `ISZ` to run a loop.

**Parts you may use:** Nand, HalfAdder.

**Hint:** Adding 1 is adding to bit 0 only; after that only the carries move. A pin
can be wired to the constant `true`.
