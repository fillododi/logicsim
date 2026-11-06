# NAND Sim

**Build a computer from a single NAND gate.** NAND Sim is a game: each level asks you to build a
chip out of chips you have already built. It starts with `Not` from a `Nand` and ends with a
working Intel 4004, the first commercial microprocessor, running real 4004 programs.

![Solving the And level: level list and brief on the left, the circuit in the middle, the
editor and test results on the right](docs/images/game-solved.png)

## Play

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). Then either install the game:

```bash
uv tool install git+https://github.com/fillododi/logicsim
nandsim gui
```

or run it from a clone:

```bash
git clone https://github.com/fillododi/logicsim && cd logicsim
uv run nandsim gui
```

A new game opens the two tutorial levels: **Wire**, which connects an input straight to an
output (`out = in;`), then **Hello**, your first part, a Nand. Guide bubbles walk you through
them: each one
points at a part of the screen and moves on when you do what it says. Skip the tour from any
bubble, and press **F1** to replay it.

Each level gives you:
- **a brief:** what the chip does, its truth table and a hint;
- **a starting text:** the chip's pins.

You add the parts in the editor:
- **Ctrl+S** builds the circuit so you can see it and poke at it.
- **Run tests** (or **Ctrl+Enter**) checks your chip. A pass unlocks the levels that use it.

Later levels are built from *your* chips, so a mistake in `And` will show up in `Mux`, just
like in real hardware.

Your work is saved in `~/.local/share/nandsim/save/`. Pass `--save-dir` to use another folder.
To start over, choose **Reset game…** on the main menu or in the Esc menu. Your old files
aren't deleted: they move to `~/.local/share/nandsim/save-backups/<date and time>/`.

To turn a chip into a building block of your own, choose **Export this chip as…** in the Esc
menu and type a name. Every level can then use it as a part, besides the parts in its brief.
Your chips are written to `~/.local/share/nandsim/save-exports/<Name>.hdl`; a `.hdl` file
copied there, whose `CHIP` name matches the file name, becomes one of your chips too, and
`nandsim test --impl save` uses them as well. The sidebar lists your chips; click the **×** next
to one to delete it. A deleted chip, and all of them on a reset, move to
`~/.local/share/nandsim/save-backups/<date and time>/exports/`.

The game has sound effects. Turn them off with **Sound: On/Off**, or step the volume with
**Volume**, on the title screen or in the Esc menu. The choice is kept in
`~/.local/share/nandsim/save-settings.json`, so a reset doesn't change it. Without an audio
device the game runs silently.

### Controls

| | |
|---|---|
| Click an input | toggle it. On a bus, click counts up and right-click counts down. |
| `Enter` or a digit over an input | type its value: `13`, `-1`, `0b1101` or `0x0D`, as in `.tst` files. Enter sets it, Esc cancels. |
| `X` over an input | make it undefined (amber), to see how unknown values spread |
| Click a part | open it and see its inside. The breadcrumbs or Backspace go back up. |
| `F1` | replay the guided tour |
| Mouse wheel, drag, `F` | zoom, pan, fit to the window |
| `H` | show buses in hex or decimal |
| Hover a wire | show its name and value |
| Ctrl+S, Ctrl+Enter | build, run the tests |
| Ctrl+Z / Ctrl+Y, Ctrl+/, Tab / Shift+Tab | undo / redo, comment, indent |
| Click the circuit | leave the editor so the keys above control the circuit |
| Esc | pause: resume, replay the tour, go to the main menu, reset the game or quit |

## The language

Chips are written in a small HDL ([full reference](docs/hdl.md)). Here is a chip that is
*not* one of the levels: "a implies b", false only when `a` is 1 and `b` is 0.

```
// a implies b
CHIP Imply {
    IN a, b;
    OUT out;
    PARTS:
    Not(in=b, out=nb);
    Nand(a=a, b=nb, out=out);
}
```

- **Buses and constants:** buses (`IN a[12]`), slices (`a[0..3]`) and the constants `true` and `false`.
- **Parts:** they can be listed in any order, and wires don't need declaring.
- **Errors:** mistakes are reported at their exact line and column (`Nand has no pin 'c' (its pins are: a, b, out)`), and the game keeps showing the last circuit that worked.
- **Values:** every wire is 0, 1 or undefined.

Levels are checked by `.tst` files ([format](docs/tst.md)). They are truth tables or short scripts, with values in decimal, binary or hex.

## Command line

```bash
nandsim gui                       # play
nandsim gui path/to/Chip.hdl      # edit one chip file next to its circuit; reloads on save
nandsim test                      # run every level against the reference solutions
nandsim test --impl save          # run every level against your saved chips
nandsim test chips/01_gates/Xor.tst
```

## Roadmap

| Milestone | | Status |
|---|---|---|
| 1. Core | HDL, simulator, tests, the gates Not to DMux | ✅ [0.1.0](https://github.com/fillododi/logicsim/releases/tag/v0.1.0) |
| 2. GUI | the game screen, circuit view, editor, saves | ✅ [0.2.0](https://github.com/fillododi/logicsim/releases/tag/v0.2.0) |
| 3. Tutorial and UI | a first level and guide bubbles that teach the game; readable large chips | ✅ [0.3.0](https://github.com/fillododi/logicsim/releases/tag/v0.3.0) |
| 4. Chip files and sound | export and import single chips; sound effects | next |
| 5. Buses | 4-, 8- and 12-bit Not, And, Or, Mux, multi-way Mux and DMux | |
| 6. Arithmetic | adders, incrementers, the 4004 ALU with decimal adjust | |
| 7. Sequential logic | DFF, registers, index registers, PC and stack, RAM, ROM, clock controls | |
| 8. CPU | the Intel 4004: all 46 instructions, running a hand-assembled program | |

NAND Sim is the first project in a series that retraces computing from the hardware up. Next come an emulator for the same CPU, an assembler, a ROM monitor, a compiler, an operating system, networking, and finally real machines (boot sector, BIOS, UEFI on QEMU). Each step targets the same 4004, checked against Intel's MCS-4 documentation and existing 4004 programs.

## Development

```bash
uv sync
uv run pytest                                   # unit, GUI (headless) and playtest tests
uv run nandsim test                             # every level against its reference
uv run ruff check . && uv run ruff format .
```

| Path | What's there |
|---|---|
| `src/nandsim/hdl` | the HDL lexer and parser |
| `src/nandsim/netlist` | elaboration into a flat netlist of NAND gates |
| `src/nandsim/sim` | the simulation engine: levelized, three-valued, numpy |
| `src/nandsim/testing` | `.tst` files and the test runner |
| `src/nandsim/gui` | the game. Only this package uses pygame; layout, saves and game rules inside it are plain Python. |
| `chips/` | the levels: starting text, brief, tests, and `levels.toml` for the unlock order |
| `reference/` | hidden reference solutions, used only to check that the levels can be solved |

Design choices are logged in [`docs/decisions.md`](docs/decisions.md), progress per milestone in [`docs/journal.md`](docs/journal.md), and releases in [`CHANGELOG.md`](CHANGELOG.md). The code is written by Claude (Claude Code) under the direction of the repository owner; [`CLAUDE.md`](CLAUDE.md) is the project brief it works from.

## License

MIT. The bundled DejaVu Sans Mono font is under its own free licence: [`src/nandsim/gui/fonts/LICENSE`](src/nandsim/gui/fonts/LICENSE).
