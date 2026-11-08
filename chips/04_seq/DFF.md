# DFF

A latch follows its input for as long as `load` is 1. A computer needs memory that changes only once per step, all at the same moment. That is the data flip-flop: its `out` is what `in` was one clock cycle earlier, and it doesn't change between cycles.

This chip reads the **clock**. `clock` works like `true` and `false`, wherever a part takes a signal, but it changes: a cycle starts with a **tick**, which raises it to 1, and ends with a **tock**, which lowers it to 0. A chip that reads `clock` gets the clock panel over its circuit: **Step** runs one cycle (so does Space, after a click on the circuit).

After a tick, `out` must still show the old value. After the tock it shows what `in` was at the tick. While the clock is 0, `out` must ignore `in`.

**Parts you may use:** Nand, Not, DLatch, and the signal `clock`.

**Hint:** One latch is never enough: whenever it is open, its output follows `in`. Use two latches in a row that are never open at the same time.

Every DFF you use as a part from here on runs as a built-in flip-flop that behaves exactly like the one you build here, only faster.
