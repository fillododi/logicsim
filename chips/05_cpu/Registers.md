# Registers

Your IndexRegs, used the way the instructions use them. `reg` is register OPA and `pair` the pair that holds it, except while `readp0` is 1, when both read register pair 0 (`FIN` fetches from the address in P0).

When `write` is 1, the next clock cycle writes:

- in a first cycle (`second` 0): `XCH` (OPR B) stores `acc` in register OPA; `INC` (6) and `ISZ` (7) add one to it;
- in a second cycle (`second` 1): `FIM` and `FIN` (OPR 2 and 3, OPA even) store `data` in pair OPA, the high digit in the even register.

Any other instruction writes nothing. `reset` clears all 16 registers. `readp0` and `write` are never 1 together.

**Parts you may use:** Nand, Not, And, Or, Mux4, DMux8Way, Inc4, IndexRegs.

**Hint:** IndexRegs already writes one register or one pair. Work out its `in`, `load` and `loadpair` from the instruction.
