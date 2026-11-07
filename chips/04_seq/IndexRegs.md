# IndexRegs

The 4004's scratchpad: 16 registers of 4 bits, R0 to R15. The same registers also work as 8 pairs of 8 bits: pair P0 is R0 and R1, P1 is R2 and R3, up to P7, R14 and R15. The even register is the pair's high half.

- `out` is always the register numbered `addr`, and `pairout` is always the pair that holds it, `pairout[4..7]` = the even register, `pairout[0..3]` = the odd one.
- When `load` is 1, the next cycle stores `in[0..3]` in that register.
- When `loadpair` is 1, the next cycle stores all of `in` in the pair: `in[4..7]` in the even register, `in[0..3]` in the odd one. If both are 1, `loadpair` wins.

In the 4004 an instruction's low digit is `addr`. Pair instructions such as `FIM` and `SRC` name the pair in its top three bits, and use bit 0 for something else.

**Parts you may use:** Nand, Or, DMux, DMux8Way, Mux4, Mux8Way4, Register4.

**Hint:** Think of the 16 registers as an even column and an odd column of 8. `addr[1..3]` picks the row in both; `addr[0]` only chooses between the columns.
