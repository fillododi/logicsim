# DMux

The opposite of Mux: sends `in` to output `a` when `sel` is 0, to `b` when `sel` is 1. The other output is 0.

| in | sel | a | b |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

**Parts you may use:** Nand, Not, And, Or, Xor, Mux.

**Hint:** Each output is `in` gated by a condition on sel.
