# Changelog

All notable changes to NAND Sim are listed here, newest first.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each milestone is
released as version `0.N.0` (milestone 1 = `0.1.0`, …, milestone 8 = `0.8.0`).

## [Unreleased]

### Added

- **Memory: the DFF.** A second primitive beside `Nand`, a flip-flop whose output is its input
  one clock cycle earlier. Tests can now run the clock with `tick` and `tock`, and a failing
  check in a clocked test says which cycle it happened in. The levels that use it come next.
  A chip you export can contain a DFF only once a level that uses one is open.
- **Clock controls.** A chip with DFFs gets a clock panel over its circuit: step one cycle,
  run and pause at 1 to 1000 cycles a second, and reset, with the cycle count beside them.
  The keys are Space (step), R (run / pause), Shift+R (reset) and [ ] (speed). Saving your
  chip keeps what its DFFs hold, unless you added or removed parts. The clock stops while a
  menu is open.
- **Memory levels: Bit, Register4, Register8 and Register12.** A new Memory group after
  Arithmetic. Bit stores one bit with a DFF and keeps it while `load` is 0; the registers put
  Bits side by side, up to the 12 bits of the 4004's program counter. On Bit, two new tour
  bubbles show the clock panel and ask for one step.

### Changed

- **The level brief and *Your chips* scroll.** In a short window, scroll the brief with the
  mouse wheel to read it to its end. *Your chips* shows four chips at a time and scrolls
  past that, so a long library no longer pushes the brief off the sidebar.

## [0.6.0] — 2026-11-07

Milestone 6: arithmetic. Ten new levels teach your chips to count, from adding two bits up
to the Intel 4004's whole arithmetic and logic unit, with its decimal adjust, its inverted
borrow and its keyboard code.

### Added

- **Adders.** Five levels in a new *Arithmetic* group add bits and numbers: HalfAdder and
  FullAdder add single bits, Add4 adds two 4-bit numbers with a carry in and out (the 4004's
  `ADD`), and Inc4 and Inc12 count up by one, for a register and the program counter.
- **The 4004's odd instructions.** Four levels build the parts of its ALU that aren't plain
  adders: AddSub4 subtracts with the 4004's inverted borrow, Rotate4 rotates through the carry
  (`RAL`, `RAR`), Daa4 keeps a sum a decimal digit (`DAA`), and Kbp4 turns a key row into a
  number (`KBP`).
- **The ALU.** The last Arithmetic level puts the 4004's accumulator instructions together:
  16 operations, chosen by a 4-bit `op`, with the new carry and a zero flag. It's the
  biggest chip yet, built from the levels before it.

## [0.5.0] — 2026-11-06

Milestone 5: buses. Thirteen new levels widen your gates to the 4, 8 and 12 bits of the
Intel 4004, so values, instructions and addresses can move around as one. Typing a value
into an input, tips for bus mistakes and a sidebar that folds and scrolls make the wider
chips easier to build.

### Added
- **Buses: 13 new levels.** Not4, And4, Or4 and Xor4 widen the gates to 4 bits; Mux4, Mux8
  and Mux12 select between buses of the 4004's widths; Or4Way tells whether any bit is set;
  Mux4Way4, Mux8Way4 and Mux4Way12 pick one of four or eight buses; DMux4Way and DMux8Way send
  a bit to one of four or eight outputs. Each opens as soon as the gate it builds on is solved,
  and Not4's brief introduces bus notation.
- **Tips for bus mistakes.** A pin given the wrong number of bits, a bit past the end of a
  bus, or a bus left partly unconnected now comes with a tip on how to fix it, like using
  `in[0]` to give a one-bit part one bit of a bus.
- **Type a value into an input.** Point at an input on the circuit and press **Enter**, or
  just start typing a number: `13`, `-1`, `0b1101` or `0x0D`, as in test files. **Enter**
  sets it and **Esc** cancels. Much quicker than clicking a 12-bit bus up to the value you
  want.
- **The tour teaches the newer features.** In Hello it shows how to type an input's value;
  in And it walks you through exporting your first chip and the *Your chips* list, including
  how to use a chip someone shares with you. The welcome bubble mentions folding level groups.
  If you already finished the tour, the new bubbles appear the next time you open Hello or
  And.

### Changed
- **Level groups fold up.** The level list shows your current group and the next one with a
  level to play; the others fold into one line with a count of solved levels, like
  `▸ TUTORIAL ✓ 2/2`. Click a group's name to open or close it. When the list is still
  longer than the room the brief leaves, it scrolls with the mouse wheel and keeps the level
  you're on in sight, so the brief is always shown whole.

## [0.4.0] — 2026-11-06

Milestone 4: your chips become building blocks, and the game makes sound. Name a chip you
built and use it in every level after, hear your toggles, errors and solved levels, and get
ready for the new goal: the Intel 4004.

### Added
- **Your own chips:** press **Esc**, choose *Export this chip as…* and type a name, like
  `MyAnd`. The chip in the editor becomes a part that every level can use, `MyAnd(a=…, b=…)`,
  on top of the parts in the brief. The sidebar lists your chips; the **×** next to one deletes
  it, after telling you which of your chips use it. They are saved in
  `~/.local/share/nandsim/save-exports/`, where you can keep or share them. A game reset clears
  them too. Deleted chips aren't lost: like a reset, they move to the backups folder.
- **Sound:** clicks when you toggle an input, a buzz for a build error, a chime when the tests
  pass, a low tone when they fail, a little fanfare when you solve a level, and ticks and blips
  in the menus. *Sound: On/Off* and *Volume* are in the Esc menu and on the title screen, and
  the game remembers them, even after a reset. No audio device? The game simply plays silently.

### Changed
- **New goal: the Intel 4004.** The game now ends with the first commercial microprocessor
  (4-bit data, 12-bit addresses, 46 instructions) instead of a RISC-V CPU. The bus, arithmetic
  and memory levels ahead are resized to match.
- **The "not allowed in this level" tip** now mentions your exported chips, and the error lists
  them among the parts you may use.

## [0.3.0] — 2026-11-06

Milestone 3: the game teaches itself. A guided tour walks you from your first wire to your
first gate made of gates, build errors come with tips, and big circuits are easier to read.

### Added
- **Learning to play:**
  - **Two tutorial levels, Wire and Hello,** come before Not. Wire is solved with one
    connection, `out = in;`, and introduces pins, connections and the editor. Hello is solved
    with a single Nand line and introduces parts. Both are optional: Not is open from the
    start.
  - **Guided tour:** bubbles point at the level list, the brief, the editor, the circuit and
    the Run tests button, and move on when you do what they explain. Skip it from any bubble,
    or press **F1** to replay it. The tour remembers where you got to.
  - **Wires:** in the And level, the tour and the brief show how to pass one part's output into
    another through a wire you name, then point at your wire on the circuit.
  - **Tips for build errors:** the most common mistakes (an unconnected pin, a wrong pin name, a
    missing `;`, a part the level doesn't allow, …) come with a one-line tip on how to fix
    them, under the error and in the test results.
- **Reading circuits:**
  - **Follow a signal:** hover a wire or a chip pin and every wire of that signal lights up,
    all the way to each part it feeds.
  - **Junction dots** mark where a wire branches, so a fork no longer looks like two wires
    crossing.
- **Menus:**
  - **Main menu:** the game opens on a title screen with Play (or Continue), Reset game and
    Quit.
  - **Pause menu:** press **Esc**, even while typing, to resume, replay the tour, go back to
    the main menu, reset the game or quit.
  - **Reset game:** start over from the first level, after a confirmation. Your old chips and
    progress aren't deleted: they move to a `save-backups/` folder next to your saves.

### Changed
- **Fewer wire crossings:** wires between two columns of parts are spread out so they cross
  much less. A 64-part test chip went from about 2500 crossings to under 1000.
- **The help line fits narrow windows:** the shortcuts at the bottom wrap onto more lines
  instead of running off the edge.
- **Esc opens the pause menu** in the game instead of leaving the editor. Click the circuit to
  leave the editor. The developer viewer (`nandsim gui FILE`) keeps Esc as before.
- On start, the game opens the first open level after the furthest one you solved, so skipping
  the tutorial doesn't send you back to it every time.

### Fixed
- Closing the window no longer loses text you typed but hadn't saved. It is saved to the level,
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

[Unreleased]: https://github.com/fillododi/logicsim/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/fillododi/logicsim/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/fillododi/logicsim/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/fillododi/logicsim/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/fillododi/logicsim/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/fillododi/logicsim/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fillododi/logicsim/releases/tag/v0.1.0
