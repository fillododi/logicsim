# Or4Way

`out` is 1 when at least one bit of `in` is 1, and 0 only when `in` is 0b0000. Turned around, it tells whether a value is zero, which the 4004 needs for its jumps.

| in | out |
|---|---|
| 0b0000 | 0 |
| 0b0100 | 1 |
| 0b1111 | 1 |

**Parts you may use:** Nand, Or.

**Hint:** An Or takes two bits; chain them, or pair them up and combine the pairs.
