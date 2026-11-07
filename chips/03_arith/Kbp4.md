# Kbp4

The 4004's `KBP`, keyboard process, reads a row of four keys with at most one held down, and gives its number: 1 to 4, or 0 when no key is held. Two or more keys are an error, 15.

| in | out |
|---|---|
| 0b0000 | 0 |
| 0b0001 | 1 |
| 0b0010 | 2 |
| 0b0100 | 3 |
| 0b1000 | 4 |
| other | 15 |

**Parts you may use:** Nand, Not, And, Or.

**Hint:** Solve it in two halves. First the number for a single key, bit by bit. Then "two or more keys", which can force every bit to 1.
