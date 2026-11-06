# DMux4Way

The opposite of a 4-way Mux: `in` goes to the output that `sel` names, and the other three are 0.

| sel | a | b | c | d |
|---|---|---|---|---|
| 0 | in | 0 | 0 | 0 |
| 1 | 0 | in | 0 | 0 |
| 2 | 0 | 0 | in | 0 |
| 3 | 0 | 0 | 0 | in |

**Parts you may use:** Nand, DMux.

**Hint:** Split in two with one bit of sel, then split each half with the other bit.
