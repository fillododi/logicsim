# InstrReg

The ROM sends each instruction to the 4004 over the 4-bit bus `din`, one digit at a time: its high digit, **OPR**, during M1 (`period` 3), and its low digit, **OPA**, during M2 (`period` 4). The CPU keeps them for the rest of the instruction cycle.

Five instructions (`JCN FIM JUN JMS ISZ`) take two words, and `FIN` fetches a byte of data, so they run for two instruction cycles. In the second one, `second` is 1, and the byte fetched then goes to `data` (high digit at M1, low digit at M2), while `opr` and `opa` keep the first word.

A digit is stored at the clock cycle of its period, and shows on the outputs from the next one. At every other period, and in the half that `second` doesn't pick, nothing changes.

**Parts you may use:** Nand, Not, And, Mux4, DMux8Way, Register4, Register8.

**Hint:** There are four digits to keep. Each one has its own period and its own value of `second`, and loads only then.
