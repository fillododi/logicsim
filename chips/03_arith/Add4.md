# Add4

Adds two 4-bit numbers and a carry in: `out = a + b + cin`. A result above 15 doesn't
fit in 4 bits, so `cout` is 1 and `out` keeps the low 4 bits: `9 + 8 = 17` gives
`out = 1`, `cout = 1`.

This is the heart of the 4004's `ADD` instruction: the accumulator, a register, and
the carry flag in, a new accumulator and carry flag out.

**Parts you may use:** Nand, FullAdder.

**Hint:** Add column by column, as on paper, starting from bit 0. Each column's carry
goes into the next.
