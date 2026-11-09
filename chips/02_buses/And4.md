# And4

And, bit by bit: `out[i]` is 1 when `a[i]` and `b[i]` are both 1.

| a | b | out |
|---|---|---|
| 0b1100 | 0b1010 | 0b1000 |
| 0b1111 | 0b0110 | 0b0110 |

The 4004 has no AND instruction: programs test bits with rotates and the carry. Its own circuits need 4-bit gates all the same, to mask and combine values on their way between units.

**Parts you may use:** Nand, And.

**Hint:** Same shape as Not4, with two buses in.
