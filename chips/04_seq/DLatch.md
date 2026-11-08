# DLatch

An SRLatch that takes the bit itself instead of two commands. While `load` is 1, `out` follows `in`, as a wire would. While `load` is 0, `out` keeps the last value it had, however `in` changes. Before the first load its output is undefined.

**Parts you may use:** Nand, Not, And, SRLatch.

**Hint:** When `load` is 1, `in` decides between set and reset. When `load` is 0, the SRLatch should get neither.
