# AddSub4

With `sub = 0`, Add4: `out = a + b + cin`, and `cout` is the carry out.

With `sub = 1`, it subtracts the way the 4004's `SUB` does. There the carry means **no borrow**: `cin = 0` is a plain `a - b`, `cin = 1` takes one more away (a borrow from the digit before), and `cout = 1` when the result didn't need to borrow.

| a | b | cin | sub | out | cout |
|---|---|---|---|---|---|
| 6 | 2 | 0 | 0 | 8 | 0 |
| 6 | 2 | 0 | 1 | 4 | 1 |
| 6 | 2 | 1 | 1 | 3 | 1 |
| 2 | 6 | 0 | 1 | 12 | 0 |

**Parts you may use:** Nand, Add4, Xor4, Xor.

**Hint:** `a - b` is `a + (not b) + 1`. A Xor with `sub` is a Not that works only when `sub` is 1. The carry needs flipping too.
