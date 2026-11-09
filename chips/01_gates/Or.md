# Or

Outputs 1 when at least one input is 1.

| a | b | out |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

Or merges conditions: the index registers are written by `XCH` or `INC` or `ISZ` or `FIM` or `FIN`. One Or per extra reason.

**Parts you may use:** Nand, Not, And.

**Hint:** Look at Nand's truth table with both inputs inverted.
