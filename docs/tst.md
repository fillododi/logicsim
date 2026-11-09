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
| `cycles <n>` | `n` full clock cycles, each a `tick` then a `tock`, with no checks in between. A CPU test runs thousands of them. |
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

The CPU has the 4004's pins and reaches its memories only through its bus. A script can put
the memories of an MCS-4 system, held by the test runner, on that bus: sixteen 4001 ROMs
with the 4 KB of program memory (chip n holds addresses `n·256` to `n·256+255`, and each
has an I/O port) and eight banks of four 4002 RAMs (each with an output port). They aren't
chips: nothing about them is built in HDL, and they exist only while the test runs.

| Command | Meaning |
|---|---|
| `attach mcs4 din=<pin> dout=<pin> drive=<pin> sync=<pin> cmrom=<pin> cmram=<pin> reset=<pin>` | Puts the memories on the chip's bus. `din` (4 bits) and `reset` are chip inputs; `dout` (4), `drive`, `sync`, `cmrom` and `cmram` (4) are chip outputs. Once only, before the commands below. |
| `rom <addr> <byte> <byte>...` | Writes bytes into program memory from `addr` on. Program memory starts as all 0 (NOP). |
| `rom <file>` | Loads a `.rom` file into program memory from address 0. The path is relative to the `.tst` file. |
| `ram <bank> <addr> <value>` | Sets a main character. `addr` is what SRC sends: `addr[6..7]` pick the 4002, `addr[4..5]` its register, `addr[0..3]` the character. Characters start undefined. |
| `ramstatus <bank> <addr> <value>` | Sets a status character: `addr[4..7]` as above, `addr[0..1]` the character. |
| `set romport <chip> <value>` | What the I/O lines of 4001 `chip` show: what RDR reads. |
| `expect ram <bank> <addr> <value>` | Checks a main character. `*` is allowed. |
| `expect ramstatus <bank> <addr> <value>` | Checks a status character. |
| `expect romport <chip> <value>` | Checks what WRR last wrote to 4001 `chip`'s port. |
| `expect ramport <bank> <chip> <value>` | Checks what WMP last wrote to the port of 4002 `chip` in `bank`. |

With only two words after it, `set` or `expect` takes the first as a pin, so a chip may
still have a pin named `ram` or `romport`. `din` can't be `set`: the memories drive it.

**How they run.** Like a real 4001 or 4002, the memories count the 8 clock periods of each
instruction cycle, A1 A2 A3 M1 M2 X1 X2 X3, one per `tick` and `tock`. While `reset` is 1 at
a tick, the next period is A1. Until the first reset they do nothing. At each tick they
read what the CPU puts on the bus in the current period, and after each tock they put on
`din` what they send in the new one, or 0 when they send nothing:

- **A1, A2, A3:** they take the address, low nibble first. At A3, if `cmrom` is 1, the 4001
  whose number is that nibble is selected.
- **M1, M2:** that 4001 sends the byte at the address, its high nibble (OPR) at M1 and its
  low one (OPA) at M2. If `cmrom` or a CM-RAM line is 1 at M2, the instruction is an I/O or
  RAM instruction for the chips SRC selected. Which ones depends on the line:
  - `cmrom`: the 4001 SRC selected;
  - CM-RAM0 alone: bank 0;
  - CM-RAM1–3: banks 1–7, as a binary number, as `DCL` selects them.
- **X2:** if `cmrom` or a CM-RAM line is 1, this is SRC. The 4001s take their chip number
  from `dout`, and the bank whose line is up takes the 4002 and register. For an I/O or RAM
  instruction, this is where the data moves. Writes (WRM, WMP, WRR, WR0–3) take `dout`. Reads
  (RDM, RDR, RD0–3, SBM, ADM) are sent on `din`. WPM goes nowhere: it needs a 4008/4009.
- **X3:** the bank that took X2 of an SRC takes the character from `dout`.

A reset clears the SRC selections and sets every output port to 0. It keeps the contents
of program and data memory, so a test can fill them first.

**Bus problems** are failures, reported at the tick where they happen, with the period:

- `sync` must be 1 at X3 and only at X3.
- `dout` must be 0 when `drive` is 0.
- The CPU must drive the bus at A1–A3, at X2 and X3 of an SRC, and at X2 of a write.
- It must not drive the bus while a memory sends.
- A RAM instruction needs a 4002 selected by SRC in its bank, and an RDR a 4001 selected
  by SRC.
- The CM-RAM lines may not select bank 0 and another bank at once.

Only the first bus problem in a test is reported: a CPU that gets the protocol wrong once
usually gets it wrong every cycle.

```
Bus.tst:52:1: bus at M1: drive is 1 while 4001 #0 sends on the bus (cycle 4)
```

The start of a CPU test, with the program LDM 5, XCH R0:

```
chip CPU
attach mcs4 din=din dout=dout drive=drive sync=sync cmrom=cmrom cmram=cmram reset=reset
rom 0 0xD5 0xB0
set test 0
set reset 1
// 8 instruction cycles of reset, as on the chip: 64 clock periods
tick
tock
// ...
set reset 0
// then 8 clock periods for each instruction
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
