# FullAdder

Adds three bits: `a`, `b`, and a carry `c` coming from the column to the right. The
result is 0 to 3, so again `sum` is the low bit and `carry` the high one.

| a | b | c | carry | sum |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |

**Parts you may use:** Nand, HalfAdder, Or.

**Hint:** Add `a` and `b`, then add `c` to that sum. Can both additions carry at once?
