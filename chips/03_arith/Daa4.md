# Daa4

The 4004 counts in decimal by adding digits in binary and then fixing the result with `DAA`, decimal adjust. A decimal digit is 0 to 9; 10 to 15 aren't digits.

`DAA` adds 6 when `in` is greater than 9 or `cin` is 1 (the addition already carried past 15). Adding 6 skips the six values that aren't digits: `7 + 5 = 12`, plus 6 gives 18, so `out = 2` and `cout = 1`, a decimal carry.

`cout` is set to 1 if adding 6 carries out of bit 3. Otherwise it keeps the value of `cin`: `DAA` never clears the carry.

| in | cin | out | cout |
|---|---|---|---|
| 7 | 0 | 7 | 0 |
| 12 | 0 | 2 | 1 |
| 2 | 1 | 8 | 1 |

**Parts you may use:** Nand, Add4, And, Or.

**Hint:** Write 10 to 15 in binary: what do they share that 0 to 9 don't? 6 is `0b0110`.
