# Not

Outputs the opposite of its input: 0 becomes 1, 1 becomes 0.

| in | out |
|---|---|
| 0 | 1 |
| 1 | 0 |

The 4004's `CMA` instruction complements the accumulator: four Nots side by side. Inverted signals are everywhere in control logic too, wherever something should happen when a bit is not set.

**Parts you may use:** Nand.

**Hint:** A Nand whose two inputs are the same signal behaves like a Not.
