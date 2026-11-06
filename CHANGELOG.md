# Changelog

All notable changes to NAND Sim are listed here, newest first.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each milestone is
released as version `0.N.0` (milestone 1 = `0.1.0`, …, milestone 7 = `0.7.0`).

## [Unreleased]

### Added
- **Tutorial levels, Wire and Hello:** two new first levels. Wire is solved with one connection,
  `out = in;`, and introduces pins, connections and the editor. Hello is solved with a single
  Nand line and introduces parts. Not is still open from the start, so you can skip them.
- **Guided tour:** bubbles point at the level list, the brief, the editor, the circuit and the
  Run tests button, and move on when you do what they explain. Skip it from any bubble, or press
  **F1** to replay it. The tour remembers where you got to.
- **Tips for build errors:** the most common mistakes (an unconnected pin, a wrong pin name, a
  missing `;`, a part the level doesn't allow, …) now come with a one-line tip on how to fix
  them, under the error and in the test results.
- **Follow a signal:** hover a wire or a chip pin and every wire of that signal lights up, all
  the way to each part it feeds.
- **Junction dots** mark where a wire branches, so a fork no longer looks like two wires
  crossing.
- **Main menu:** the game opens on a title screen with Play (or Continue), Reset game and Quit.
- **Pause menu:** press **Esc**, even while typing, to resume, replay the tour, go back to the
  main menu, reset the game or quit.
- **Reset game:** start over from the first level, after a confirmation. Your old chips and
  progress aren't deleted: they move to a `save-backups/` folder next to your saves.

- **Wires in the tour:** in the And level, the tour and the brief explain how to pass one
  part's output into another through a wire of your own, then point at your wire on the
  circuit.

### Changed
- **Fewer wire crossings:** wires between two columns of parts are spread out so they cross
  each other much less; a 64-part test chip went from about 2500 crossings to under 1000.
- **Help line in narrow windows:** the shortcuts at the bottom wrap onto more lines instead of
  running off the edge of the window.
- **Esc opens the pause menu** in the game instead of leaving the editor. Click the circuit to
  leave the editor. The developer viewer (`nandsim gui FILE`) keeps Esc as before.
- On start, the game opens the first open level after the furthest one you solved, so skipping
  the tutorial doesn't send you back to it every time.

### Fixed
- Closing the window no longer loses text you typed but hadn't saved; it is saved to the level,
  as switching level already did.

## [0.2.0] — 2026-11-06

Milestone 2: the game. Play with `nandsim gui`: pick a level, write the chip, see its circuit,
run the tests and unlock what comes next.

### Added
- **The game:** `nandsim gui` opens the level select.
  - The levels on the left show which are solved (✓), open (○) or locked (–). A locked level
    tells you which chips to solve first.
  - Under the list is the level's brief: what the chip does, its truth table and a hint.
  - Write the chip in the editor. Ctrl+S saves it and draws its circuit.
  - **Run tests** (or Ctrl+Enter) checks your chip. A failure lists the rows and inputs that broke
    it.
  - Passing a level unlocks the levels that use it. Later levels are built from your own chips,
    not ready-made ones.
  - Work and progress are saved in `~/.local/share/nandsim/save/` (or `--save-dir`). Switching
    level never loses unsaved text.
- **The circuit:** drawn automatically from your HDL.
  - Wires are coloured by value: 0, 1 or undefined.
  - Buses show their value; `H` switches between hex and decimal, and hovering a wire shows its
    name and value.
  - Click an input to toggle it. On a bus, click counts up and right-click counts down. `X` makes
    it undefined, so you can watch unknown values spread (or not).
  - Click a part to see inside it, and use the breadcrumbs or Backspace to come back.
  - Zoom with the wheel, drag to pan, and press `F` to fit.
  - If a change doesn't build, the error shows with its line and column while the last working
    circuit stays on screen.
- **The editor:**
  - syntax colours and line numbers;
  - the mistake underlined where it is;
  - mouse selection, with double-click for a word; copy, cut and paste;
  - undo and redo;
  - auto-indent: Tab / Shift+Tab, and a closing brace that dedents itself;
  - Ctrl+/ to comment lines out or back in;
  - Esc to hand the keys back to the circuit.
- **Direct connections in the HDL:**
  - `out = a;` wires a signal straight to an output or a new wire, with no gate in between. It
    also works for slices (`low[0..3] = in[4..7];`) and constants (`flag = true;`).
  - `g1: Nand(a=a, b=b);` labels a part, so its output can be used as `g1.out` without naming a
    wire.
- **For chip authors:** `nandsim gui path/to/Chip.hdl` opens one file in the editor next to its
  circuit and reloads when any chip next to it changes. `--no-edit` shows only the circuit.

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

[Unreleased]: https://github.com/fillododi/logicsim/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/fillododi/logicsim/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fillododi/logicsim/releases/tag/v0.1.0
