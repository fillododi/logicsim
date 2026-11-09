# CPU

The Intel 4004, on its own pins. It reaches its program and its data only through the 4-bit bus: `din` is what the ROM and RAM chips send, and `dout` is what it sends while `drive` is 1. When `drive` is 0, `dout` must be 0.

Every instruction cycle is 8 clock periods, counted by your Timing:

- **A1, A2, A3:** send the address of the next instruction, low digit first. `cmrom` is 1 at A3, so the ROM chip with that number answers.
- **M1, M2:** receive the instruction, OPR then OPA, into your InstrReg.
- **X1, X2, X3:** execute. Results reach A, CY and the registers by X2. Reads from RAM and ROM ports arrive on `din` at X2, and writes send A on `dout` at X2. `sync` is 1 during X3.

`JCN FIM JUN JMS ISZ` read a second word, and `FIN` fetches a byte from the page it is on, so they take two instruction cycles. In `FIN`'s second one, the address sent is register pair 0 with the page of the next instruction.

`SRC` sends its register pair at X2 (even register) and X3 (odd register). Raise `cmrom` and the CM-RAM lines of the bank `DCL` picked (your CmLines) at A3, at X2 of `SRC`, and at M2 of every I/O or RAM instruction (OPR 1110).

`reset` held for 64 clock periods restarts the CPU at address 0 with A, CY and the DCL bank at 0, and the next period is A1. The index registers keep whatever they held: a program sets them before using them.

The test runs one program through every instruction, checking what it stores in RAM, then Intel's own 16-digit decimal addition.

**Parts you may use:** Nand, Not, And, Or, Xor, Mux, Mux4, Mux8, Mux12, Mux4Way4, Mux8Way4, Mux4Way12, DMux, DMux8Way, And4, Or4, Or4Way, Inc4, Bit, Register4, Register8, Register12, Timing, InstrReg, Cond, CmLines, PC, IndexRegs, ALU.

**Hint:** Decide when each part changes: the PC steps once per cycle, after A3. Almost everything else loads at X2, and jumps, calls and returns at X3.
