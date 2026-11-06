# Wire

The simplest chip there is: its output is always equal to its input.

| in | out |
|---|---|
| 0 | 0 |
| 1 | 1 |

A chip lists its pins (`IN`, `OUT`) and then, after `PARTS:`, what it is made of. A connection `target = source;` joins two signals directly, like a piece of wire: the target always has the same value as the source.

**Parts you may use:** none. A connection is enough.

**Hint:** The output is the target and the input is the source.
