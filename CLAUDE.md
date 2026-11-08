# NAND Sim — guide for Claude

## Context

This is the first project in a series that retraces the history of computing from the systems side. Each project builds the next one:

1. **Logic simulator (this project)**: from the NAND gate up to a working CPU
2. Instruction-level emulator for the same CPU
3. Assembler
4. ROM monitor (ancestor of the BIOS)
5. Compiler
6. Operating system
7. Networking between emulator instances
8. Real machines: boot sector, BIOS and UEFI on QEMU

The target CPU is the **Intel 4004** (1971, the first commercial microprocessor), compatible at the instruction level: same registers, stack, instruction encodings and results, but not the real chip's multiplexed bus or clock phases. Later projects follow the same CPU and are checked against Intel's MCS-4 documentation and existing 4004 programs.

## Roles

- NAND Sim is a game. The **player** builds chips from NAND upward by writing HDL in an **editor inside the GUI**, never by editing repo files.
- The user directs, reviews and reads. **Claude implements everything**: core, GUI and editor, tests, and the levels. Each level is an interface stub, a brief shown in game, a `.tst` file, and a hidden reference solution in `reference/` that the GUI never shows.
- When a spec point is ambiguous, pick the simplest reasonable option, record it in `docs/decisions.md`, and keep going. Ask only about decisions that are hard to undo.

## Tech stack

- Python 3.12+, environment and dependencies managed with `uv`
- `pygame-ce` for the GUI
- `numpy` for the simulation engine
- `pytest` for tests, `ruff` for linting and formatting
- Do not add other runtime dependencies without asking first.

## Commands

```bash
uv sync                                         # install dependencies
uv run python -m nandsim gui                                   # play: level select + editor
uv run python -m nandsim gui reference/01_gates/Mux.hdl        # developer editor + viewer, reloads on save
uv run python -m nandsim test --impl reference chips/01_gates/Xor.tst  # one level vs its reference
uv run python -m nandsim test --impl reference chips/           # every level vs its reference
uv run python -m nandsim test --impl save chips/                # the player's saves
uv run pytest                                   # Python unit tests
uv run ruff check . && uv run ruff format .     # lint and format
```

Before declaring a step done: `pytest` green, every level's `.tst` green against its reference, `ruff` clean (the `/verify` skill runs all of it).

## Workflow

Work on branches, never directly on `main`. The project skills in `.claude/skills/` define the loop: `/analyze` → `/make-change` → `/verify` → `/pr` → `/review`, and `/milestone` to close a milestone.

## Architecture

```
src/nandsim/
  hdl/        lexer, parser, AST, error messages with file:line:col
  netlist/    elaboration: resolves the chip hierarchy into a netlist
  sim/        simulation engine
  testing/    .tst format and test runner
  gui/        pygame viewer and HDL editor (the only package that imports pygame)
  __main__.py CLI: `gui` and `test` subcommands
chips/        level definitions: interface stub .hdl, brief .md, .tst
  01_gates/  02_buses/  03_arith/  04_seq/  05_memory/  06_cpu/
  levels.toml unlock order and the parts each level may use
reference/    hidden reference solutions, same layout as chips/
docs/
  hdl.md  tst.md  decisions.md  journal.md
CHANGELOG.md  release notes; one version 0.N.0 per milestone
tests/
```

**Hard rule:** the core (`hdl`, `netlist`, `sim`, `testing`) never imports pygame. The GUI uses only the core's public API. The next project, the emulator, will reuse parts of the core.

## HDL

The full syntax lives in `docs/hdl.md`, written in milestone 1. The starting point is a nand2tetris-like syntax:

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

- Supports buses (`IN a[32]`), slices (`a[0..7]`, `out[31]=sign`) and the constants `true` and `false`.
- **The only primitives are `Nand` and `DFF`.** Every other chip is built in HDL from these.
- **Builtin chips:** for speed, a large chip (RAM, register file, ALU) may get a Python implementation, but only after its HDL version exists and passes its tests. An automated test must check that the builtin and HDL versions are equivalent. The GUI marks builtins visibly, and you can always switch back to the HDL version.
- Errors must be clear and precise: unknown pin, wrong width, unconnected output, circular dependency between chips, and so on.

## Simulation semantics

- **Combinational logic:** the netlist is flattened down to primitives and levelized (topological order). A combinational loop that does not pass through a DFF is an error, and the message names the involved pins.
- **Sequential logic:** one global clock. `DFF`: `out(t) = in(t-1)`. Each cycle has two phases, tick and tock, as in nand2tetris.
- **Performance:** evaluate level by level with vectorized numpy operations over flat arrays, rather than a Python object per gate. Profile before optimizing. Report in the journal the simulated clock speed reached by the final CPU, next to the real 4004's rate of about 92.5 k instruction cycles per second (a 740 kHz clock, 8 clocks per instruction cycle). One simulated cycle is one instruction cycle, so compare against that rate, not the raw clock.
- Inner wire values must stay inspectable, because the GUI shows them.

## Tests (.tst)

The format is specified in `docs/tst.md`. At minimum it must support:

- truth tables (inputs, then expected outputs) for combinational chips;
- sequential scripts (set inputs, tick/tock, check outputs) for registers, memory and the CPU;
- values in binary, decimal and hex.

Each chip in `chips/` has a `.tst` file next to it.

## GUI

- The circuit is drawn **automatically from the HDL**, with a layered layout: inputs on the left, outputs on the right, parts arranged in levels, and wires routed to keep crossings few. Positions are never written into the HDL. An optional `.layout.json` sidecar file for manual adjustments may come later.
- **Hierarchical navigation:** click a part to open its inner circuit, with breadcrumbs to go back up. This is the main way to handle circuit size, so do not try to draw a whole CPU flattened.
- Click an input to change its value. Wire colors show their state (0, 1, undefined), and buses show their value in hex or decimal (toggle).
- Controls: step (one tick/tock), run with adjustable speed, pause, reset.
- **Editor:** the player writes HDL in an in-app editor. Ctrl+S compiles, errors are underlined at `line:col` and listed in a panel, and they never crash the GUI. The circuit view keeps the last version that compiled and keeps the current navigation where possible. A "Run tests" button runs the level's `.tst`.
- **Levels and saves:** a level select follows `chips/levels.toml`. The player's HDL is saved in a user data dir (default `~/.local/share/nandsim/save/`, overridable for tests). A solved chip becomes usable as a part in later levels.
- **Hot reload** of `.hdl` files from disk remains only as a developer convenience.
- Zoom and pan with the mouse.

## Milestones

Complete them in order. Each one ends with green tests, updated docs, a journal entry and a `CHANGELOG.md` release `0.N.0` tagged `v0.N.0`. Every user-visible change adds a line under `[Unreleased]` as it lands.

1. **Core:** HDL parser, elaboration, combinational simulation, `.tst` runner, CLI. Chips: Not, And, Or, Xor, Mux, DMux. No GUI yet.
2. **Base GUI:** automatic layout, inputs and outputs that can be toggled, wire colors, hierarchical navigation, in-app HDL editor with inline errors, saves, level select.
3. **Tutorial and UI:** teach the game inside the game, and make large chips readable.
   - A tutorial level before Not whose answer is a single `Nand` line.
   - Guide bubbles anchored to UI elements (editor lines, canvas pins and parts, the Run tests button, the level list). They are written as data in `chips/tutorial.toml`, advance when the player does the thing they explain, can be skipped and replayed (F1), and remember what was seen in `tutorial.json`.
   - Short tips for the most common build errors.
   - UI polish: fewer wire crossings on large chips, the hovered net highlighted across the canvas, junction dots where wires branch, and a help line that fits narrow windows.
4. **Chip files and sound:**
   - Export the editor's chip under a name the player types, to a `.hdl` file in an exports folder beside the save dir (never inside it), with no file dialog. Exported chips are in the library: every level may use them as parts, and there is no import. The sidebar lists them with a delete button; deleting and resetting move them to the backups folder.
   - Sound effects synthesized with numpy at startup (no asset files) through `pygame.mixer`: toggles, build errors, tests passed and failed, level solved, menus. Mute and volume in the menu, stored in a settings file next to the saves. Without an audio device the game runs silently.
5. **Buses (4, 8 and 12 bits):** Not4, And4, Or4, Xor4, Mux4, Mux8, Mux12, Or4Way, Mux4Way4, Mux8Way4, Mux4Way12, DMux4Way, DMux8Way.
6. **Arithmetic:** HalfAdder, FullAdder, Add4 (carry in and out), Inc4, Inc12 (for the PC), and the 4004 ALU: add and subtract with carry/borrow, increment and decrement, complement, rotate through carry, decimal adjust (DAA), KBP, TCS, with the zero and carry flags that JCN tests.
7. **Sequential logic:** DFF in the GUI, Bit, Register4, Register8, Register12, the index register file (16 × 4 bits, also read and written as 8 pairs), the PC with its 3-level address stack, RAM at increasing sizes up to the 4002 layout (registers of 16 main and 4 status characters, selected by bank, chip and register), a 4096 × 8 program ROM in the 4001 layout (sixteen 256 × 8 chips, picked by `addr[8..11]`), with a write port. Clock controls in the GUI.
   - **ROM editor:** the player types a program in binary in a dedicated in-game editor, saved as a `.rom` file with the saves. The game loads it into the player's ROM through the write port, one byte per cycle, on reset. A `.tst` loads a program file the same way.
8. **CPU: the Intel 4004.** All 46 instructions, with the 4004's encodings: `NOP JCN FIM SRC FIN JIN JUN JMS INC ISZ ADD SUB LD XCH BBL LDM`, `WRM WMP WRR WPM WR0 WR1 WR2 WR3 SBM RDM RDR ADM RD0 RD1 RD2 RD3`, `CLB CLC IAC CMC CMA RAL RAR TCC DAC TCS STC DAA KBP DCL`. Separate program ROM and data RAM, as in the real MCS-4 system, with the ROM and RAM I/O ports as chip pins. One clock cycle per 4004 instruction cycle, so two-word instructions (`JCN FIM JUN JMS ISZ`) and `FIN` take two. Goal: run a hand-assembled 4004 program, such as multi-digit BCD addition, and check RAM and the output ports with a `.tst` file.
9. **The Busicom 141-PF, the end of the game.** The calculator the 4004 was designed for, built from the player's chips: the 4004, 4001 ROMs, 4002 RAMs and a 4003 shift register. Its scope (keyboard, printer, which program and how many 4003s) gets its own decision before work starts.

## Code conventions

- Type hints everywhere. Use `dataclass` for AST and netlist structures.
- Each module gets a short docstring explaining its role.
- Make small commits, one green step at a time, with messages that explain why the change was made, not only what changed.
- Do not optimize prematurely, except in the simulation engine, where the levelized vectorized design is a requirement from the start.