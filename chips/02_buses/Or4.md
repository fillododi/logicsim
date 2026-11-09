# Or4

Or, bit by bit: `out[i]` is 1 when `a[i]` or `b[i]` is 1.

| a | b | out |
|---|---|---|
| 0b1100 | 0b1010 | 0b1110 |
| 0b0000 | 0b0110 | 0b0110 |

The 4004 has no OR instruction either, but its circuits merge 4-bit values with Ors: when only one source can be active at a time, Oring them all together picks the active one.

**Parts you may use:** Nand, Or.

**Hint:** One Or per bit.
