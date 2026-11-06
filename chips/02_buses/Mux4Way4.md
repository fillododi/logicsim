# Mux4Way4

Four inputs, and a 2-bit `sel` that picks one of them.

| sel | out |
|---|---|
| 0 (0b00) | a |
| 1 (0b01) | b |
| 2 (0b10) | c |
| 3 (0b11) | d |

**Parts you may use:** Nand, Mux4.

**Hint:** Let sel[0] choose within each pair, then sel[1] choose between the pairs.
