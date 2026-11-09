# BusOut

Everything the 4004 puts on its pins, for the current `period`:

- **A1, A2, A3** (0 to 2): `dout` is the address, low digit first, and `drive` is 1. The address is `pc`, or while `finfetch` is 1, `pair` with the page of `pc`.
- **X2** (6): `SRC` (OPR 2, OPA odd) sends `pair`'s even register, and the I/O writes (OPR E, OPA 0 to 7) send `acc`.
- **X3** (7): `SRC` sends `pair`'s odd register.

`SRC` and the I/O writes count only in a first cycle (`second` 0). At every other period `drive` is 0, and then `dout` must be 0.

`cmrom` is 1 at A3, at M2 (`period` 4) of an I/O instruction (OPR E, first cycle) and at X2 of `SRC`. `cmram` raises the lines of `bank` at those same times, as your CmLines does.

**Parts you may use:** Nand, Not, And, Or, Mux4, Mux12, Mux4Way4, DMux8Way, CmLines.

**Hint:** Choose the value first, then let `drive` decide whether it reaches `dout`.
