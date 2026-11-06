# Mux8Way4

Eight inputs, and a 3-bit `sel`: `a` when sel is 0, `b` when 1, up to `h` when 7.

| sel | out |
|---|---|
| 0 | a |
| 1 | b |
| ... | ... |
| 7 | h |

**Parts you may use:** Nand, Mux4, Mux4Way4.

**Hint:** Two Mux4Way4s each pick a candidate with sel[0..1]; sel[2] picks between them.
