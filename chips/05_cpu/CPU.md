# CPU

The Intel 4004, on its own pins, from the parts you built in this group. It reaches its program and its data only through the 4-bit bus: `din` is what the ROM and RAM chips send, and `dout` is what it sends while `drive` is 1.

Every instruction cycle is 8 clock periods, counted by your Timing. The units each do their work at a certain time, and wiring them is about giving each one its moment:

- **InstrReg** takes the instruction at M1 and M2; **Sequencer** says whether this is a second cycle, and whether it is `FIN`'s fetch.
- **Registers** reads pair 0 at A1 to A3 of `FIN`'s fetch (`readp0`), and writes at X2.
- **Accumulator** writes at X2 of a first cycle.
- **Jumps** steps the PC after A3 (but not in `FIN`'s fetch, which isn't an instruction fetch), and runs jumps at X3.
- **BusOut** drives `dout`, `drive` and the command lines from all of them. `sync` is your Timing's.

`reset` held for 64 clock periods restarts the CPU at address 0, with A, CY, the 16 index registers and the DCL bank at 0, and the next period is A1.

The test runs one program through all 46 instructions, checking what it stores in RAM, then Intel's own 16-digit decimal addition.

The clock panel runs your CPU on a small program from `CPU.rom`, a decimal counter in RAM, and shows the period, the counter's RAM register and the ports under its buttons. Reset restarts it from address 0.

**Parts you may use:** Nand, Not, And, Or, Mux, Mux4, DMux8Way, Timing, InstrReg, Sequencer, Accumulator, Registers, Jumps, BusOut.

**Hint:** Timing's period through a DMux8Way gives you one line per period. Most of the CPU is a few Ands of those lines.
