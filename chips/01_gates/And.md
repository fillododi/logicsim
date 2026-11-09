# And

Outputs 1 only when both inputs are 1.

| a | b | out |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

This is the first chip with two parts in a row. To use one part's output as another part's input, connect them through a **wire**: a name of your own, written as the first part's output and as an input of the second. For example, `Not(in=a, out=na); Not(in=na, out=out);` passes `a` through two Nots, carried between them by the wire `na`.

**Parts you may use:** Nand, Not.

**Hint:** Nand is "not And". What undoes a "not"?
