# PC

The 4004 keeps four 12-bit addresses and a 2-bit pointer. The address the pointer selects is the program counter, `out`; the other three are the stack, holding where each call returns to. A call moves the pointer up, a return moves it down, and both wrap around: a fourth call in a row overwrites the oldest return address.

Each clock cycle does the first of these that is asked for:

- `reset`: the pointer and all four addresses go to 0.
- `push` (a call, `JMS`): the pointer moves up and the address there becomes `in`. If `inc` is also 1, the address left behind steps by 1 first, so the return skips the call.
- `pop` (a return, `BBL`): the pointer moves down; its address is where the program goes on.
- `load` (a jump): the current address becomes `in`.
- `inc`: the current address steps by 1, from `0xFFF` around to 0.

Otherwise nothing changes. Every address and the pointer start undefined until `reset`.

**Parts you may use:** Nand, Not, And, Or, Xor, Mux, Mux12, DMux4Way, Mux4Way12, Inc12, Register12, Bit.

**Hint:** It is IndexRegs again, with four registers and the address picked by the pointer. A push writes the register after the pointer, which is the pointer's next value; on a push with `inc`, the register at the old pointer is written in the same cycle.
