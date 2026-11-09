# Sequencer

Six instructions take two instruction cycles: `JCN FIM JUN JMS ISZ` read a second word, and `FIN` fetches a byte. In OPR and OPA they are:

- `JCN` OPR 1, `JUN` 4, `JMS` 5, `ISZ` 7;
- `FIM` OPR 2 and `FIN` OPR 3, with OPA even (odd OPA there is `SRC` and `JIN`, one cycle).

`second` is 1 during the second cycle of one of these. It changes only at the clock cycle of X3 (`period` 7), the end of an instruction cycle: it becomes 1 if this was the first cycle of a two-cycle instruction, and 0 otherwise. `reset` makes it 0.

`finfetch` is 1 while `second` is 1 and the instruction is `FIN`: the cycle in which `FIN` fetches its byte instead of the next instruction.

`opr` and `opa` come from your InstrReg, which keeps the first word during the second cycle.

**Parts you may use:** Nand, Not, And, Or, Mux, DMux8Way, Bit.

**Hint:** One Bit is enough. Work out what it should hold after X3 from what it holds now.
