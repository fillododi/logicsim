# SRLatch

Your first chip with memory, and the first whose wires feed back into themselves. While `set` is 1, `out` is 1. While `reset` is 1, `out` is 0. When both are 0, `out` keeps whichever value it had last. Before the first set or reset it holds nothing, so its output is undefined. Never raise both at once.

A wire may now be read by the very parts that drive it. The circuit settles step by step, one gate delay at a time, until nothing changes. A loop that never comes to rest, like a Not wired to its own input, shows as undefined.

**Parts you may use:** Nand, Not.

**Hint:** A NAND with a 0 on either input outputs 1, whatever the other input is. Two NANDs that each read the other's output can hold either of two states. Which input of each should pull it out of the other state?
