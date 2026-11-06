# DMux8Way

`in` goes to the output that `sel` names, from `a` (sel 0) to `h` (sel 7). The others are 0. A memory uses this to send a write to the one register being addressed.

| sel | a | b | ... | h |
|---|---|---|---|---|
| 0 | in | 0 | ... | 0 |
| 1 | 0 | in | ... | 0 |
| 7 | 0 | 0 | ... | in |

**Parts you may use:** Nand, DMux, DMux4Way.

**Hint:** sel[2] says which half; each half is a DMux4Way.
