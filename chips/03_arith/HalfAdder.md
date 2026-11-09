# HalfAdder

Adds two bits. The result can be 0, 1 or 2, so it needs two bits: `sum` is the low bit and `carry` the high one.

| a | b | carry | sum |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

Every addition the 4004 makes, `ADD`, `IAC`, `ISZ`, `DAA` and even its program counter moving on, ends up as a chain of adders built from this one.

**Parts you may use:** Nand, Xor, And.

**Hint:** Look at each output column on its own. Each one is a gate you already have.
