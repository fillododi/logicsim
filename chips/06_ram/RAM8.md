# RAM8

Memory: eight characters of 4 bits, numbered 0 to 7. `out` is always the character at `addr`. When `load` is 1, the next clock cycle stores `in` there. The other seven keep their values.

The 4004 calls a 4-bit memory cell a "character": one decimal digit, or one hex digit.

**Parts you may use:** Nand, DMux8Way, Mux8Way4, Register4.

**Hint:** Eight registers. Only the one at `addr` may see `load`; all eight can see `in`.
