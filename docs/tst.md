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
| `expect <pin> <value>` | Checks an output (or input) pin. Each `expect`, and each output in a table row, is one check. |

`tick` and `tock`, for sequential chips, arrive in milestone 7.

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

An output that has undefined bits prints as `undefined`, or as `0b1x0x` when the expected value was written in binary.

Run tests from the command line:

```bash
uv run nandsim test                          # every level against its reference
uv run nandsim test --impl save              # your saved chips, with your exported chips
uv run nandsim test chips/01_gates/Xor.tst   # one file
```
