# `.tst` test format

Each level ships a `.tst` file that decides whether your chip is correct. The format is
line-based. `//` starts a comment.

## Example

```
// Mux: every input combination
chip Mux
table a b sel | out
    0 0 0 | 0
    0 1 1 | 1
    1 0 0 | 1
end
set a 1
set b 0
set sel 0
eval
expect out 1
```

## Commands

| Command | Meaning |
|---|---|
| `chip <Name>` | The chip under test. It must be the first command, and appears only once. |
| `table <inputs> \| <outputs>` | Starts a truth table. Each following row lists input values, `\|`, then expected outputs. For each row the runner sets the inputs, evaluates, and checks the outputs. `end` closes the table. |
| `set <pin> <value>` | Sets an input pin. |
| `eval` | Propagates the inputs through the chip. |
| `tick` | First half of a clock cycle: evaluates, then every DFF stores its input and `clock` rises to 1, and the chip settles again. Outputs of DFFs don't change yet. |
| `tock` | Second half: every DFF outputs what it stored at the last `tick`, `clock` falls to 0, then the chip evaluates. |
| `expect <pin> <value>` | Checks an output (or input) pin. Each `expect`, and each output in a table row, is one check. |

A full clock cycle is `tick` then `tock`. Inputs set before the `tick` are what the DFFs store:

```
// Bit: load a 1, then hold it with load off
chip Bit
set in 1
set load 1
tick
tock
expect out 1
set in 0
set load 0
tick
tock
expect out 1
```

A table row only sets, evaluates and checks: it never ticks. Every DFF starts undefined.

## Memories

A CPU reaches its program and its data through its pins. A script can attach a **program
memory** and a **data memory**, held by the test runner, to those pins. They aren't chips:
nothing about them is built in HDL, and they exist only while the test runs.

| Command | Meaning |
|---|---|
| `attach rom addr=<pin> out=<pin>` | A program memory of 4096 bytes, all 0. It reads its address from a chip output of up to 12 bits and sends the byte there to an 8-bit chip input. |
| `attach ram in=<pin> addr=<pin> bank=<pin> status=<pin> load=<pin> out=<pin>` | A data memory with DataRAM's pins and layout: 8 banks of 4002s, every character undefined. `in`, `addr` (8 bits), `bank` (3), `status` and `load` are chip outputs; `out` (4 bits) is a chip input. |
| `rom <addr> <byte> <byte>...` | Writes bytes into the program memory from `addr` on. |
| `rom <file>` | Loads a `.rom` file into the program memory from address 0. The path is relative to the `.tst` file. |
| `ram <bank> <addr> <value>` | Sets a main character of the data memory. |
| `ramstatus <bank> <addr> <value>` | Sets a status character: `addr[4..7]` pick the chip and register and `addr[0..1]` the character, as in DataRAM with `status` at 1. |
| `expect ram <bank> <addr> <value>` | Checks a main character. `*` is allowed, and an unwritten character is undefined. |
| `expect ramstatus <bank> <addr> <value>` | Checks a status character. |

Each memory can be attached once, and before any command that uses it. The memory pins
can be connected to any chip pins of the right direction and width. A pin a memory
drives can't be `set`.

**How they run.** A memory answers like combinational logic: on every `eval`, and before and
after every `tick` and `tock`, the runner evaluates the chip, sends each memory's `out` the
value at its current address, and evaluates again, until nothing changes. So the byte at
the address a CPU puts out is on its input before the tick stores it. If the address keeps
changing with the byte it gets back, the run stops after 8 passes with an error. An
undefined address reads as undefined.

The data memory writes like a DFF: if `load` is 1 at a `tick`, it remembers `in` and the
character picked, and stores it at the `tock`. Between the two, `out` still shows the old
value. An undefined `load` writes nothing, since a CPU's control lines are undefined until
its reset cycle has run. A `load` of 1 with an undefined `addr`, `bank` or `status` is a
failure, and nothing is written.

An example, with pin names for illustration (the CPU's own come with its level):

```
// LDM 5, then XCH R0: two instructions from the program memory
chip CPU
attach rom addr=romaddr out=instr
rom 0 0xD5 0xB0
set reset 1
tick
tock
set reset 0
tick
tock
```

### `.rom` files

One byte per line, written as 8 binary digits. Spaces and `_` may group the digits, and
`//` starts a comment. Lines with no byte don't count: the first byte is at address 0,
the next at 1, and so on. A file holds at most 4096 bytes.

```
// LDM 5, XCH R0
1101 0101
1011 0000
```

A line that isn't 8 binary digits is an error at its line and column.

## Values

| Written | Meaning |
|---|---|
| `13` | decimal |
| `-1` | negative decimal, stored as two's complement at the pin's width (`-1` on 8 bits is `0xFF`) |
| `0b1101` | binary |
| `0x0D` | hexadecimal (`0x0d` also works) |
| `*` | don't care: counts as a check but always passes. Only allowed in expected values. |

A value that doesn't fit the pin's width is an error.

The game takes the same syntax when you type an input's value on the circuit (**Enter** or a digit over the input), with the same error messages; `*` isn't allowed there.

## Results

A failing check names its position, the pin, the expected value, and the actual value printed in the same base. For a table row it also lists the inputs:

```
chips/01_gates/Xor.tst:6:13: out: expected 1, got 0 (inputs a=1 b=0)
```

In a script that uses `tick` or `tock`, a failure also says when it happened: the number of
finished cycles, and `after tick` when it falls between a `tick` and its `tock`.

```
Bit.tst:7:1: out: expected 0, got 1 (cycle 1)
Bit.tst:5:1: out: expected 1, got undefined (cycle 0 after tick)
Bit.tst:9:11: out: expected 0, got 1 (inputs in=0 load=1, cycle 1)
```

An output that has undefined bits prints as `undefined`, or as `0b1x0x` when the expected value was written in binary.

Run tests from the command line:

```bash
uv run nandsim test                          # every level against its reference
uv run nandsim test --impl save              # your saved chips, with your exported chips
uv run nandsim test chips/01_gates/Xor.tst   # one file
```
