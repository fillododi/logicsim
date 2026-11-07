# RAMBank

A bank of four RAM4002 chips. `addr` is the 8-bit address that the 4004's `SRC` instruction sends out:

- `addr[6..7]` picks the chip,
- `addr[4..5]` the register in it,
- `addr[0..3]` the main character, or `addr[0..1]` the status character when `status` is 1.

`out` is the character picked, and `load` stores `in` there at the next clock cycle.

**Parts you may use:** Nand, DMux4Way, Mux4Way4, RAM4002.

**Hint:** Each chip takes the same low 6 bits of the address.
