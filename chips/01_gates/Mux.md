# Mux

A selector: outputs `a` when `sel` is 0 and `b` when `sel` is 1.

| a | b | sel | out |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

**Parts you may use:** Nand, Not, And, Or, Xor.

**Hint:** Let `a` through only when sel is 0, let `b` through only when sel is 1, then combine.
