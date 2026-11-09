# Xor

Outputs 1 when the inputs differ.

| a | b | out |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Xor is the heart of addition: the low bit of a + b is a xor b. It also inverts on demand, since x xor 1 = not x: that is how the 4004's `SUB` reuses the adder.

**Parts you may use:** Nand, Not, And, Or.

**Hint:** "a or b, but not both" can be written with the gates you already have. With only Nand it takes four.
