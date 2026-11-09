# Timing

The 4004 splits each instruction cycle into 8 clock periods: it sends the program address in **A1, A2, A3**, receives the instruction in **M1, M2**, and executes it in **X1, X2, X3**. Every other part of the CPU does its work in one of these periods.

`period` is the current period, 0 for A1 up to 7 for X3, and moves on by one each clock cycle, from X3 back to A1. When `reset` is 1 at a clock cycle, the next period is A1, so the first period after a reset is always A1.

`sync` is 1 during X3. The ROM and RAM chips on the bus watch it to know that a new instruction cycle starts.

**Parts you may use:** Nand, Not, And, Mux, Mux4, Inc4, Bit, Register4.

**Hint:** A register that loads its own value plus one every cycle counts by itself. Reset only changes what it loads.
