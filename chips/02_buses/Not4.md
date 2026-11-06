# Not4

Your first **bus**: `in[4]` is four wires under one name, `in[0]` the least significant. Each `out[i]` is the opposite of `in[i]`.

| in | out |
|---|---|
| 0b0000 | 0b1111 |
| 0b0101 | 0b1010 |

Buses show their value in hex (H: decimal). Point at an input and type 0b0101 to set it.

**Parts you may use:** Nand, Not.

**Hint:** A part can read one bit of a bus and drive one bit of another, as in `Not(in=in[0], out=out[0])`.
