# ALU

The 4004's arithmetic and logic unit. `a` is the accumulator, `b` a register, `cin` the carry. `op` picks what goes to `out` (the new accumulator) and `cout` (the new carry). `zr` is 1 when `out` is 0.

Ops 0 to 12 are the low digit of the codes `F0` to `FC`.

| op | | out | cout |
|---|---|---|---|
| 0 | CLB | 0 | 0 |
| 1 | CLC | a | 0 |
| 2 | IAC | a+1 | carry |
| 3 | CMC | a | ~cin |
| 4 | CMA | ~a | cin |
| 5 | RAL | Rotate4 | Rotate4 |
| 6 | RAR | Rotate4 | Rotate4 |
| 7 | TCC | cin | 0 |
| 8 | DAC | a-1 | no borrow |
| 9 | TCS | 9+cin | 0 |
| 10 | STC | a | 1 |
| 11 | DAA | Daa4 | Daa4 |
| 12 | KBP | Kbp4 | cin |
| 13 | LD | b | cin |
| 14 | ADD | a+b+cin | carry |
| 15 | SUB | a+~b+~cin | no borrow |

**Parts you may use:** Nand, Not, Not4, Or4Way, Mux4, Mux8Way4, Add4, AddSub4, Rotate4, Daa4, Kbp4.

**Hint:** Build every result, then let `op` choose. `a - 1` is `a + 15`. A carry fits in bit 0 of a bus.
