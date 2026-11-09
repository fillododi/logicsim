# Accumulator

The 4004's accumulator A, its carry CY, and the RAM bank `DCL` picks. When `write` is 1, the next clock cycle applies what the instruction in `opr` and `opa` does to them:

- OPR 8 `ADD`, 9 `SUB`, A `LD`, B `XCH`: with register value `reg`. `XCH` only loads A here; Registers stores the old A.
- OPR C `BBL`, D `LDM`: A becomes OPA.
- OPR E with OPA 8 to F (`SBM RDM RDR ADM RD0-RD3`): with `din`, the value read from the bus.
- OPR F with OPA 0 to C: the accumulator group, `CLB` to `KBP`, as in your ALU.
- `DCL` (1111 1101): `bank` becomes A's low three bits.

Every other instruction leaves them alone, and so does `write` at 0. `reset` sets A, CY and `bank` to 0.

**Parts you may use:** Nand, Not, And, Or, Mux, Mux4, DMux8Way, Bit, Register4, ALU.

**Hint:** Your ALU already does every operation. ADD, SUB and LD are its op codes 14, 15 and 13. The work is choosing `b` and `op`, and when to load.
