# Bit

A register of one bit. Each clock cycle, if `load` is 1, `out` becomes `in` from the cycle before; if `load` is 0, `out` keeps its value however `in` changes. Before the first load it holds nothing: its output is undefined.

Your `DFF` does half of this: it remembers for exactly one cycle. From here on every DFF part runs as a built-in flip-flop that behaves like yours, only faster. To watch your own latches at work instead, press **B** on the circuit.

The 4004's carry flag CY is exactly this: one bit that an instruction may load and every other instruction leaves alone.

**Parts you may use:** Nand, Mux, DFF.

**Hint:** A DFF alone forgets after one cycle. What should it receive when `load` is 0, so that next cycle it outputs the same thing again?
