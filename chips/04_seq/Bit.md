# Bit

Your first chip with memory. Each clock cycle, if `load` is 1, `out` becomes `in` from the cycle before; if `load` is 0, `out` keeps its value however `in` changes. Before the first load it holds nothing: its output is undefined.

The new part is the `DFF`: `DFF(in=d, out=q)` outputs, this cycle, what its `in` was the cycle before. Once your chip has a DFF, the clock panel appears over the circuit: **Step** (Space) runs one cycle.

**Parts you may use:** Nand, Mux, DFF.

**Hint:** A DFF alone forgets after one cycle. What should it receive when `load` is 0, so that next cycle it outputs the same thing again?
