# Changelog

All notable changes to NAND Sim are listed here, newest first.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each milestone is
released as version `0.N.0` (milestone 1 = `0.1.0`, …, milestone 6 = `0.6.0`).

## [Unreleased]

### Added
- **Direct connections in HDL:**
  - `out = a;` connects a signal straight to an output or a new wire, with no gate in between. It
    also works for slices (`low[0..3] = in[4..7];`) and constants (`flag = true;`).
  - `g1: Nand(a=a, b=b);` labels a part, so its output can be used directly as `g1.out`
    without naming a wire.
  - Both are drawn in the circuit view, and labelled parts show their label.
- **The game:** `uv run nandsim gui` opens the level select.
  - The levels on the left show which are solved (✓), open (○) or locked (–). A locked level
    tells you which chips to solve first.
  - Under the list is the level's brief: what the chip does, its truth table and a hint.
  - Write the chip in the editor. Ctrl+S saves it and draws the circuit.
  - **Run tests** (or Ctrl+Enter) checks your chip against the level's tests. A failure shows
    the row and inputs that broke it.
  - Passing a level marks it solved and unlocks the levels that use it. Later levels are built
    from your own chips, not ready-made ones.
  - Your work and progress are saved in `~/.local/share/nandsim/save/` (choose another folder
    with `--save-dir`). Switching level never loses unsaved text.
- **Circuit viewer:** `nandsim gui path/to/Chip.hdl` draws a chip from its HDL, with no
  positions to write.
  - Wires are coloured by value: 0, 1 or undefined. Buses show their value; `H` switches between
    hex and decimal, and hovering any wire shows its value.
  - Click an input to toggle it. On a bus, click counts up and right-click counts down. `X` makes
    an input undefined, so you can see how undefined values spread (or don't).
  - Click a part to open its inside, and use the breadcrumbs or Backspace to go back up.
  - Zoom with the mouse wheel, drag to pan, and press `F` to fit.
  - Saving the file, or any chip next to it, reloads the view. Mistakes show as a banner with
    their line and column while the last working circuit stays on screen.
- **HDL editor:** `nandsim gui Chip.hdl` opens the chip's source next to its circuit.
  - Ctrl+S saves and rebuilds. A mistake is underlined at its exact spot, its line number turns
    red, and the full message appears below the circuit.
  - Syntax colours, line numbers, mouse selection (double-click selects a word), copy, cut and
    paste.
  - Undo and redo. Auto-indent after `{`, and a closing brace dedents itself. Tab and Shift+Tab
    indent and dedent, and Ctrl+/ comments lines out or back in.
  - Press Esc to go back to the circuit's shortcuts. `--no-edit` shows the circuit alone.

## [0.1.0] — 2026-11-06

Milestone 1: the core. There is no GUI yet; chips are tested from the command line.

### Added
- **Six levels:** Not, And, Or, Xor, Mux, DMux. Each starts from a stub with the chip's pins and
  comes with a brief (what the chip does, its truth table, a hint) and a test.
- **The HDL:** chips are built from parts, with buses (`a[8]`), slices (`a[0..3]`) and the
  constants `true` and `false`. Every mistake is reported at its exact line and column with a
  clear message: unknown pin, wrong width, unconnected output, combinational loop, and more
  (see `docs/hdl.md`).
- **The simulator:** every wire is 0, 1 or undefined. A chip is flattened to NAND gates and
  evaluated level by level.
- **Tests:** the `.tst` format has truth tables and scripts, with values in decimal, binary and
  hex. A failure shows the row and the inputs that caused it (see `docs/tst.md`).
- **`nandsim test`:** runs every level, or chosen `.tst` files, against the reference or against
  your own chips (`--impl save --save-dir <dir>`). It works from a source checkout and from an
  installed package.

### Project
- MIT license, CI on every pull request, and a protected `main` branch.
- Design decisions in `docs/decisions.md`, a development journal in `docs/journal.md`, and this
  changelog.
- Workflow skills for Claude Code: `/analyze`, `/make-change`, `/verify`, `/pr`, `/review` and
  `/milestone`.

[Unreleased]: https://github.com/fillododi/logicsim/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fillododi/logicsim/releases/tag/v0.1.0
