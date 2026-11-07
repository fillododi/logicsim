# Inc12

Adds 1 to a 12-bit number, and `0xFFF` wraps around to 0. The 4004's program counter
is 12 bits wide, and after each instruction it steps to the next address.

**Parts you may use:** Nand, Add4.

**Hint:** Three Add4s side by side make a 12-bit adder, if each carry out feeds the
next one's carry in. What do you add, and where does the 1 come in?
