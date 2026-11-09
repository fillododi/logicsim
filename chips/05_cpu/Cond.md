# Cond

`JCN` is the 4004's conditional jump. Its low digit is a condition code, written C1 C2 C3 C4 from the high bit down. It picks what to test, and the jump happens if any picked test is true:

- C2 (`cond[2]`): the accumulator is 0;
- C3 (`cond[1]`): the carry is 1;
- C4 (`cond[0]`): the TEST pin is 0.

C1 (`cond[3]`) inverts the answer: with C1 at 1, `JCN` jumps when none of the picked tests is true. With no test picked, the answer is "no", so `JCN 0` never jumps and `JCN 8` always does.

`jump` is 1 when `JCN` with this condition code would jump.

**Parts you may use:** Nand, Not, And, Or, Xor, Or4Way.

**Hint:** Each test counts only when its bit of `cond` picks it. Work out "any picked test is true" first, then let C1 flip it.
