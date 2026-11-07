# HDL reference

The language you build chips in. A chip has input pins, output pins, and a list of
**parts**: other chips wired together. The only chips you don't build yourself are the two
primitives, `Nand` and `DFF`.

## A complete chip

```
// Xor from four NANDs
CHIP Xor {
    IN a, b;
    OUT out;
    PARTS:
    Nand(a=a, b=b, out=n);
    Nand(a=a, b=n, out=x);
    Nand(a=n, b=b, out=y);
    Nand(a=x, b=y, out=out);
}
```

- `CHIP Name { ... }` declares the chip. Its name must match the level.
- `IN` and `OUT` list the pins, separated by commas and ending with `;`. A chip may have no `IN` line.
- `PARTS:` is followed by zero or more parts, each ending with `;`.
- Comments: `// to the end of the line` and `/* across lines */`.
- Names are letters, digits and `_`, starting with a letter or `_`. `CHIP`, `IN`, `OUT`, `PARTS`, `true` and `false` are reserved.

## Parts and connections

A part is `ChipName(pin=signal, pin=signal, ...)`:

- On the **left** of `=` is a pin of the part (`a`, `b`, `out` for `Nand`).
- On the **right** is a signal of the chip you are building: one of its `IN` or `OUT` pins, an internal wire, or a constant.

**Internal wires** don't need to be declared. Connecting a part's output to a new name, such as `out=n` above, creates the wire `n`. Its width is the width of that output. Any other part can then read it.

Parts can appear in any order: hardware has no "before" and "after". You may read your chip's own `OUT` pins as inputs to other parts. You don't have to connect a part's outputs if you don't need them.

## Direct connections

Two shortcuts save you from inventing wire names or adding gates that do nothing.

**Connect a signal straight to another** with `target = source;` inside PARTS:

```
out = a;                 // an input straight to an output
low[0..3] = in[4..7];    // move bits around
flag = true;             // a constant
copy = out;              // the same signal on two outputs
```

- These are plain wires, not gates: they cost nothing.
- The target is one of your `OUT` pins (or a slice of one), or a new internal wire. A new wire takes the width of its source, so it can't be created from a constant.
- The source is anything a part input could read: a pin, a wire, a constant, or a labelled part's output.

**Label a part** to use its outputs without naming a wire:

```
g1: Nand(a=a, b=b);
Not(in=g1.out, out=out);
```

- `g1.out` reads the output `out` of the part labelled `g1`, and can be sliced (`alu.out[0..7]`).
- Labels must be unique and different from your pin names. A labelled part may still connect its outputs the usual way (`out=n`) as well.
- In the circuit, the part is titled `g1: Nand`.

## Buses, slices and constants

- `IN a[8]` declares an 8-bit bus. Bit 0 is the least significant bit.
- `a[3]` is one bit, and `a[0..3]` is bits 0 through 3. Both sides of a connection can be sliced: `Foo(in[0..3]=a[4..7], out[7]=sign)`.
- `true` and `false` are constants. They fill every bit of the pin they connect to: `Foo(in=false)` makes all bits of `in` zero.
- Both sides of a connection must have the same width. Constants are the exception.
- A new internal wire cannot be sliced where it is created. Write `out=w`, then read `w[0..3]` elsewhere.

## DFF: memory

`DFF(in=d, out=q)` is a data flip-flop, the one primitive with memory. Its output is its input
one clock cycle earlier: `out(t) = in(t-1)`. Each cycle has two halves:

- **tick:** the chip settles, then every DFF stores its `in`. Outputs don't change yet.
- **tock:** every DFF puts the stored value on `out`, all at once, and the chip settles again.

A DFF starts undefined, and stays undefined until it stores a known value. Anything else
uses it like a part: `DFF(in=d, out=q, out=out)` sends its output to two places.

A signal may depend on itself through a DFF, which is how a register keeps its value:

```
Mux(a=prev, b=in, sel=load, out=d);
DFF(in=d, out=prev, out=out);
```

Without the DFF that loop would be a combinational loop, an error.

## Rules and errors

Every error shows `file:line:col` and stops at the first problem.

| Mistake | Example message |
|---|---|
| syntax | `expected ';', found '}'` |
| pin declared twice | `pin 'a' is already declared at line 1` |
| bus of width 0 | `bus 'a' must be at least 1 bit wide` |
| reversed slice | `slice a[7..2] is reversed: write [2..7]` |
| unknown chip | `unknown chip 'Foo'` |
| unknown pin on a part | `Nand has no pin 'c' (its pins are: a, b, out)` |
| width mismatch | `width mismatch: pin 'in' of Not has 1 bit but 'a' has 2` |
| slice out of range | `a[2] is out of range: 'a' has 2 bits (0..1)` |
| reading a signal nothing drives | `'w' is not a pin of Top and nothing drives a wire with that name` |
| driving an input pin | `'a' is an input pin of Top: a part output cannot drive it` |
| driving a constant | `output pin 'out' of Not cannot be connected to a constant` |
| two drivers | `'o' is already driven by Not at line 2` |
| pin connected twice | `pin 'a' of Nand is connected more than once` |
| part input left open | `input pin 'b' of Nand is not connected` |
| chip output left open | `output pin 'out' of Xor is not connected` |
| chips using each other | `circular dependency between chips: Top -> A -> B -> A` |
| combinational loop | `combinational loop (a signal depends on itself without a DFF): y -> x -> y` |
| connecting to an input | `'a' is an input pin of T: it cannot be assigned` |
| new wire from a constant | `the width of new wire 'w' can't come from a constant; connect the constant to a pin instead` |
| connections in a loop | `'p' would be driven only by itself: assignments form a loop with nothing driving it` |
| unknown label | `no part is labelled 'g' in T` |
| reading a part's input | `'g.in' is an input pin of Not: only a part's outputs can be read this way` |
| driving a labelled output | `'g.out' is driven by part 'g' and cannot be assigned` |
| label used twice | `label 'g' is already used at line 1` |
| label that is a pin name | `label 'a' is also a pin of T; use another name` |

A level adds two more rules:
- Your chip must keep the pins of the level's starting text.
- It may use only the parts the level lists, plus the chips you exported under a name of your own (*Export this chip as…* in the Esc menu), such as `'Mux' is not allowed in this level; Xor may use: Nand, Not, And, Or, MyAnd`.

An exported chip's name must be an identifier that isn't an HDL word (`CHIP IN OUT PARTS true false`), a primitive (`Nand`, `DFF`) or a level's chip.

## Values

Every wire is 0, 1 or **undefined**. Inputs start undefined until you set them. `Nand` outputs 1 whenever one of its inputs is a known 0, even if the other input is undefined. Otherwise, an undefined input makes its output undefined.
