# Register8

Remembers a 8-bit number. Each clock cycle, if `load` is 1, `out` becomes `in`; otherwise it keeps its value. An 8-bit register holds a whole instruction word, or a pair of index registers read together.

**Parts you may use:** Nand, Register4.

**Hint:** Two Register4s, each holding half of the bits.
