# CmLines

The 4004 has four CM-RAM lines to tell the RAM chips which bank of 4002s an instruction is for. `DCL` stores a bank number, 0 to 7, and the CPU raises the lines for that bank whenever it talks to RAM:

- bank 0 has a line of its own, `cmram[0]`;
- banks 1 to 7 are their number in binary on `cmram[1..3]`, so bank 5 (`101`) raises `cmram[1]` and `cmram[3]`.

When `on` is 0, every line is 0.

**Parts you may use:** Nand, Not, And, Or.

**Hint:** Three of the lines just copy a bit of `bank` while `on` is 1. Only `cmram[0]` has to look at all three bits.
