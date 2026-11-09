# RAM64

64 characters of 4 bits, numbered 0 to 63, with the same rules as RAM8: `out` is the character at `addr`, and `load` stores `in` there at the next clock cycle.

**Parts you may use:** Nand, DMux8Way, Mux8Way4, RAM8.

**Hint:** Eight RAM8s. Which bits of `addr` pick the RAM8, and which pick the character inside it?
