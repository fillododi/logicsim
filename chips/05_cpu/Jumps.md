# Jumps

Your PC, with its stack, moved by the instructions. `step` adds one to the PC, as each instruction fetch does. When `exec` is 1, the next clock cycle runs the instruction's jump:

- in a second cycle (`second` 1): `JUN` (OPR 4) goes to OPA and `data` (12 bits); `JMS` (5) calls there, saving the PC on the stack; `JCN` (1) and `ISZ` (7) go to `data` in the PC's current page if they jump. `JCN` jumps when Cond says so for `acc`, `carry` and `test`, and `ISZ` when `reg`, already incremented, isn't 0.
- in a first cycle (`second` 0): `JIN` (OPR 3, OPA odd) goes to `pair` in the current page, and `BBL` (C) returns.

Anything else, or `exec` at 0, leaves the PC alone. `reset` clears the PC and the stack. `step` and `exec` are never 1 together.

**Parts you may use:** Nand, Not, And, Or, Mux12, DMux8Way, Or4Way, Cond, PC.

**Hint:** The PC level already pushes, pops, loads and steps. Build the target address from the instruction, then decide which of those to ask for.
