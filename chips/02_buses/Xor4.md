# Xor4

Xor, bit by bit: `out[i]` is 1 when `a[i]` and `b[i]` differ.

| a | b | out |
|---|---|---|
| 0b1100 | 0b1010 | 0b0110 |
| 0b1111 | 0b0101 | 0b1010 |

Your 4-bit subtractor will use one of these: Xoring the second operand with 1111 inverts it, and adding the inverse is how the 4004 subtracts.

**Parts you may use:** Nand, Xor.

**Hint:** One Xor per bit.
