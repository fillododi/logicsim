# Rotate4

The 4004's `RAL` and `RAR` rotate the accumulator through the carry: five bits in a ring.

With `right = 0` (`RAL`), every bit moves up one place: `cin` enters at bit 0, and bit 3 leaves into `cout`.

| in | cin | out | cout |
|---|---|---|---|
| 0b1001 | 0 | 0b0010 | 1 |
| 0b1001 | 1 | 0b0011 | 1 |

With `right = 1` (`RAR`), every bit moves down: `cin` enters at bit 3, and bit 0 leaves into `cout`.

| in | cin | out | cout |
|---|---|---|---|
| 0b1001 | 0 | 0b0100 | 1 |
| 0b0110 | 1 | 0b1011 | 0 |

**Parts you may use:** Nand, Mux, Mux4.

**Hint:** Moving bits takes no gates, only wires: `x[1..3]=in[0..2]` on a part's pin. Build both results, then choose.
