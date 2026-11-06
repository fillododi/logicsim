# Mux4

A Mux for buses: `out` is all of `a` when `sel` is 0, and all of `b` when `sel` is 1. The 4004 moves 4-bit values around, and a Mux4 picks which one goes where.

| sel | out |
|---|---|
| 0 | a |
| 1 | b |

**Parts you may use:** Nand, Mux.

**Hint:** One Mux per bit, all sharing the same sel.
