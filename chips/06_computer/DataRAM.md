# DataRAM

All the data memory a 4004 can reach: eight RAMBanks, 2,560 characters. The 4004's `DCL` instruction picks a bank, and `SRC` sends the 8-bit address inside it.

- `bank` picks the RAMBank,
- `addr` and `status` pick a character in it, as in RAMBank.

`out` is the character picked, and `load` stores `in` there at the next clock cycle.

**Parts you may use:** Nand, DMux8Way, Mux8Way4, RAMBank.

**Hint:** Only the bank picked may load.
