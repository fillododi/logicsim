# Journal

One entry per milestone: what was built, problems, what was learned, numbers.

## Milestone 1 — Core (2026-11-06)

**Built:** the whole non-GUI pipeline.
- HDL lexer, parser and dataclass AST, with `file:line:col` errors.
- Elaboration that flattens any chip into a bit-level NAND netlist through a primitive table, then levelizes it.
- A three-valued engine (`value`/`known` bit-planes, Kleene NAND) that evaluates each level with one vectorized numpy operation.
- Our own `.tst` format and runner. The runner enforces each level's pins and allowed parts.
- `nandsim test`.
- The first six levels: Not, And, Or, Xor, Mux, DMux, each with a stub, brief, test and hidden reference.
- Level data ships inside the wheel. CI installs the wheel and runs every level from it.

**Problems and how they were solved:**
- *Parts in any order.* A part may read a wire that a later part drives. Every chip output and internal wire first gets a placeholder net, and when a part's output is bound, the placeholder is aliased to the real net. All aliases are resolved at the end in one vectorized pass (`mapping = mapping[mapping]` until stable).
- *Readable loop errors.* A loop shows up as gates left over after Kahn's algorithm. To name the wires, the levelizer walks back from a stuck gate through stuck drivers until a gate repeats. Each net is labelled with its shallowest wire path in the hierarchy, giving messages like `y -> x -> y`.
- *Levels in an installed game.* `chips/` and `reference/` live at the repo root for easy review. Hatch copies them into `nandsim/_data`, and `data_root()` prefers that directory when it exists.
- *Golden error tests.* My hand-counted columns were wrong three times, and the parser was right each time. Error tests are now written by running the parser once and checking the output by eye.

**Learned:**
- **Engine cost scales with depth, not gate count.** Each level costs about 3.4 µs of fixed numpy overhead, so a 4096-gate netlist 3 levels deep runs at about 148 M gate-evals/s, while a 257-gate chain 257 levels deep manages only about 0.3 M. The single-cycle CPU (now milestone 7) will be a few hundred levels deep, which points to roughly 1 kHz before builtins. The levers, in order: builtins for wide, deep blocks (adder, ALU, RAM, register file), then merging small levels or compiling level schedules.
- Kleene NAND matters already: `Mux` with `sel` defined and the unselected input undefined gives a defined output, as real hardware does.
- Stopping at the first error keeps every message precise; recovery can come later without changing the format.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 103 | `uv run pytest`: hdl 15, netlist 22, sim 15, testing 26, levels 19, cli 4, boundary 2 |
| Levels | 6/6 pass against their references | `uv run nandsim test` |
| Source LOC | 1358 | non-blank lines of `src/**/*.py`: hdl 302, netlist 564, sim 81, testing 333 |
| Test LOC | 513 | non-blank lines of `tests/**/*.py` |
| NAND count (depth) per reference | Not 1 (1), And 2 (2), Or 3 (2), Xor 4 (3), Mux 8 (5), DMux 5 (3) | `elaborate()` on each reference |
| Engine, wide | 4096 NAND, depth 3: 36k evals/s (148 M gate-evals/s); elaboration 0.12 s | 1024 parallel `Xor`s, `Simulator.eval()` in a loop for 2 s, Python 3.12.3, numpy 2.x, this laptop |
| Engine, deep | 257 NAND, depth 257: 1175 evals/s (0.3 M gate-evals/s) | chain of 257 `Not`s, same method |

**Next:** milestone 2, the base GUI. It starts with a pygame window that draws a chip from its netlist with a layered layout (inputs left, outputs right, parts in levels) and colours wires by 0, 1 or undefined. Then: clickable inputs, hierarchical navigation, the in-app editor with inline errors, saves, and the level select.

## Milestone 2 — Base GUI (2026-11-06)

**Built:** `nandsim gui` is now a game.
- **Levels:**
  - a level list showing solved, open and locked, with the reason a level is locked;
  - each level's brief: description, truth table and hint;
  - unlocking by parts: a level opens when every chip it may use is solved, and later levels are built from the player's own saved chips.
- **Circuit:**
  - an automatically laid-out circuit (Sugiyama-style layers, barycenter ordering, orthogonal wires on separate tracks, buses as one trunk, feedback drawn as loops over the top);
  - wires coloured 0, 1 or undefined; bus values in hex or decimal;
  - clickable inputs; clicking into parts, with breadcrumbs; zoom and pan.
- **Editor:**
  - written from scratch: syntax colours, undo, auto-indent, selection, clipboard;
  - Ctrl+S builds and underlines errors at their `line:col`;
  - Run tests (button or Ctrl+Enter) reports failing rows with their inputs.
- **Saves:** progress lives in the user data dir and survives restarts.
- **Developer mode:** `nandsim gui FILE` edits and views a single file, reloading on save.
- **HDL:** gained direct connections (`out = a;`, `low[0..3] = in[4..7];`) and labelled parts (`g1: Nand(...)`, read as `g1.out`), at the user's request.

**Problems and how they were solved:**
- *Testing a GUI without a screen.* Every pygame class takes events through `handle()` and draws through `render()`. Tests feed it real `KEYDOWN`, `TEXTINPUT` and mouse events under `SDL_VIDEODRIVER=dummy`. Everything that isn't drawing lives in pure modules (model, layout, camera, session, text buffer, syntax, brief, game rules), and a boundary test keeps pygame out of them. The playtest solves Not and And with real events only.
- *The playtest found real bugs.* Switching level saved the unsaved text into the *new* level's file. A chip that grew after a rebuild no longer fit the canvas. Both were fixed with the test as the regression check.
- *Readable wiring.* At first, each bit of a bus got its own vertical track, which made wide chips unreadable. Grouping tracks by source pin turned a bus into one trunk with taps. A bit swap was drawn as `b[1..0]` until bits merged only when their source bits run in order.
- *Fonts.* `SysFont("monospace")` returned a proportional font on the dev machine, so DejaVu Sans Mono is bundled, with its licence.
- *Errors that greet you.* A fresh level's starting text "isn't connected" by design. Errors now appear only after the player first saves or runs that level.
- *Hidden solutions.* A test forbids any GUI code from touching `reference/`. The game builds and tests only with the player's own chips.

**Learned:**
- Separating "what to show" from "how to draw it" paid off immediately. The editor, game rules and layout were tested headless in milliseconds, and most bugs were found there rather than on screen.
- Scripted playtests with screenshots are the closest thing to a user test without a user. The two bugs they caught would have been the first things a player hit.
- **Layout quality degrades on large, deeply connected chips.** The 64-part ripple chip has about 2500 wire crossings. Correct and fast, but hard to read. The 32-bit buses, adders and ALU (milestones 4–5) would make this the main GUI issue, so it moves into milestone 3. The levers: better track ordering in channels, dummy-node straightening, and highlighting the hovered net across the whole canvas.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 200 | `uv run pytest`: hdl 15, netlist 42, sim 15, testing 26, gui 75, levels 19, cli 4, boundary 4 |
| GUI tests | 75 | model 8, layout 13, saves 5, session 7, app 5, text buffer 13, syntax 4, editor 8, brief 3, game 6, playtest 3 |
| Levels | 6/6 pass against their references | `uv run nandsim test` |
| Source LOC | 4035 (gui 2480, netlist 696, hdl 352, testing 333, sim 81) | non-blank lines of `src/**/*.py` |
| Test LOC | 1591 | non-blank lines of `tests/**/*.py` |
| Work since 0.1.0 | 6 merged PRs, 25 commits | `git log v0.1.0..HEAD` |
| Layout time | Mux (4 parts) 0.5 ms; 16-bit ripple chip (64 parts) 33 ms | best of 5 `layout()` calls |
| Crossings | Mux 3; 64-part chip 2537 | `layout.crossings()` |
| Rebuild time | 64-part chip: 44 ms for parse, elaborate and layout | best of 3 `ChipSession.reload()` |
| Frame time | game screen 0.9 ms; viewer with the 64-part chip 1.5 ms | best of 30 / 10 `render()` calls at 1440×860, headless software surface |

**Next:** release 0.2.0, then the tutorial agreed for after it:
- a first level that wires a single Nand;
- guide bubbles anchored to the editor, canvas, Run tests button and sidebar, driven by `chips/tutorial.toml`;
- progress in `tutorial.json`.

This became milestone 3, Tutorial and UI, which also takes on layout readability for large chips. Buses move to milestone 4.

## Milestone 3 — Tutorial and UI (2026-11-06)

**Built:** the game teaches itself, and large chips are easier to read.
- **Tutorial levels:** `Wire` is solved with one connection, `out = in;`. `Hello` is solved with a single `Nand(a=a, b=b, out=out);`. Both sit before Not, and both are optional, since Not doesn't depend on them.
- **Guided tour:** 19 steps written as data in `chips/tutorial.toml`.
  - Bubbles are anchored to the level list, brief, editor lines, pins, parts, a wire, the breadcrumbs, the footer and the Run tests button.
  - Each step moves on when the player does what it explains: build, toggle, open a part, go up, run the tests, solve the level, open the next one.
  - Skip it from any bubble, replay it with F1 (also from the pause menu). Progress is kept in `tutorial.json`.
  - In And, the tour now teaches internal wires: a double-Not example that doesn't give away the answer, then a bubble pointing at the player's own wire on the circuit.
- **Tips for build errors:** 15 common mistakes get a one-line "what to do" under the error and in the test results.
- **Readability:**
  - channel tracks are ordered by crossing cost (2537 → 944 crossings on the 64-part chip);
  - the hovered net is highlighted across the whole canvas, from a wire or a chip pin;
  - dots mark where wires branch;
  - the help line wraps in narrow windows.
- **Menus**, at the user's request:
  - a title screen;
  - an Esc pause menu that works from the editor too;
  - "Reset game…", which moves the player's files to `<save dir>-backups/<time>/` after a confirmation whose default is Cancel.
  - Quitting no longer loses unsaved editor text.

**Problems and how they were solved:**
- *Where the crossings came from.* The plan in milestone 2 was to work on the column order. Measuring first showed the column order accounted for only about 500 of the 2537 crossings. The rest came from the order of vertical tracks inside each channel, sorted by y. Ordering tracks by pairwise crossing cost removed 63%. A transpose pass on the column order was then tried and dropped, because it changed the drawn total by under 1%.
- *What a junction is.* The first test assumed a fork is a corner on every branch. The layout showed otherwise: one branch turns while the other carries straight on down the shared track. A junction is now defined as three or more directions of one net meeting at some route's corner, and the test checks exactly that.
- *Backups the library could still see.* The first version of reset put backups in `save/backups/`. A test showed `ChipLibrary` (which searches recursively) still resolving the backed-up `Not`, so a "reset" player would have kept their old chips. Backups moved beside the save directory instead of teaching the core about GUI folders.
- *Help that doesn't fit even wrapped.* At 420 px, one shortcut item alone is wider than the window. Items wrap between `·` first, and inside an item only when they must.
- *Two branches touching the footer.* The menus and the polish branch both edited the footer code. The second was merged with `main` rather than rebased, to avoid a force-push. The code merged cleanly. Only the changelog and decisions needed both sides kept, and the gates were rerun on the merge.
- *Tour steps whose action already happened.* A player who solves Hello before the "run the tests" bubble shouldn't have to do it again. Actions are remembered per level, and a step whose action is already done completes as soon as it comes up.

**Learned:**
- Measure before optimising, even in the GUI. The obvious lever, column order, was the minor one.
- Pin a fact in a test as soon as one is discovered. The recursive library search was found by the reset test, not on a player's machine.
- A tutorial has to teach without solving. Hello may show its answer because it is the syntax lesson, but And's example must be a different circuit with the same shape.
- Screenshots review the tour better than assertions do. The bubble that covered the Not part and the code lines split by blank rows were both visible only in the playtest's screenshots.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 284 (+84 since 0.2.0) | `uv run pytest --co`: netlist 42, testing 26, levels 25, sim 15, hdl 15, cli 4, boundary 4, gui 153 |
| GUI tests | 153 | layout 28, tutorial 21, tips 15, text buffer 13, menus 10, app 10, tour playtest 9, model 8, game 8, editor 8, session 7, saves 6, syntax 4, playtest 3, brief 3 |
| Levels | 8/8 pass against their references (Wire and Hello added) | `uv run nandsim test --impl reference chips/` |
| Source LOC | 5076 (gui 3521, netlist 696, hdl 352, testing 333, sim 81); +1041, all in the GUI | non-blank lines of `src/**/*.py`, same script for v0.2.0 (4035) |
| Test LOC | 2392 (+801) | non-blank lines of `tests/**/*.py` |
| Work since 0.2.0 | 6 merged PRs (#13–#18), 21 commits | `git log v0.2.0..main` |
| Crossings | all levels 2 (was 10); Xor 0 (was 4); 64-part chip 944 (was 2537) | `layout.crossings()` |
| Layout time | Mux 0.5 ms; 64-part chip 58 ms (was 33 ms: track ordering and junctions) | best of 5 `layout()` calls |
| Rebuild time | 64-part chip: 68 ms for parse, elaborate and layout | best of 3 `ChipSession.reload()` |
| Frame time | game screen 1.3 ms; viewer with the 64-part chip 1.75 ms | best of 30 / 10 `render()` calls at 1440×860, headless software surface |
| Tour | 19 steps in 4 levels; 15 error tips | `chips/tutorial.toml`, `gui/tips.py` |

**Next:** milestone 4, Buses: Not32, And32, Or32, Mux32, Or8Way, Mux4Way32, Mux8Way32, DMux4Way, DMux8Way. It starts with Not32, the first 32-bit level. That is where the readability work meets real buses, and where the brief and tour should introduce `a[i]` slices and bus values in hex.

## Milestone 4 — Chip files and sound (2026-11-06)

**Built:** the player can keep their own chips and hears the game.
- **Your own chips:**
  - *Export this chip as…* in the Esc menu asks for a name in a text field (new in `Menu`), renames the `CHIP` line to it, checks that the chip builds, and writes it to `<save dir>-exports/<Name>.hdl`.
  - Every level may then use it as a part, besides the parts it lists, in the game and in `nandsim test --impl save`.
  - The sidebar lists the player's chips, each with a × that deletes it after a confirmation naming the chips that use it.
  - Deleting and resetting move the files to `<save dir>-backups/<time>/exports/`; nothing is destroyed.
- **Sound:**
  - eight effects synthesized with numpy at startup (toggle, build error, tests passed, tests failed, level solved, and three menu sounds), played through `pygame.mixer` in whatever format the device opened with;
  - *Sound: On/Off* and *Volume* on the pause menu and title screen, saved in `<save dir>-settings.json` so a reset keeps them;
  - no audio device means silence, not a crash.
- **Roadmap:** at the start of the milestone, the Intel 4004 replaced RV32I as the game's CPU, and the bus, arithmetic and memory milestones were resized to 4, 8 and 12 bits.

**Problems and how they were solved:**
- *Import, then no import.* The first version (#22) followed the milestone text: export a file, import it back into the editor. Reviewing it, the user wanted something else: type a name on export, and have exported chips always available as parts. The request ("the user should be able to type the chip's name") had three readings, so I asked rather than guessed. #23 replaced import with named parts, and `CLAUDE.md`'s milestone text was updated to match.
- *Renaming a chip safely.* Replacing `CHIP Not` with a regex could hit a comment. `ChipDef` now records where its name is written (`name_pos`), and export replaces exactly those characters. Build error positions still match the editor.
- *Names that must never be chips.* An exported `Not.hdl` could stand in for the Not level, and a `DFF.hdl` would clash with the primitive due in milestone 7. `exported_chips` ignores any file named like a level, a primitive (`DFF` included ahead of time) or an HDL word. This also neutralizes the level-named files that #22's export wrote.
- *Settings and reset.* A reset moves every file in the save directory, so settings stored there would unmute the game on every reset. They live beside it, like the exports and backups.
- *The mixer's real format.* A device may open in stereo or another sample size even when mono is asked for. `to_mixer` converts to whatever `mixer.get_init()` reports, and a test opens an unsigned 8-bit mono mixer to prove it.
- *A test click that didn't toggle.* The first click on the circuit only leaves the editor, by design (milestone 3). The sound test clicks twice, as a player would, rather than changing the behaviour.

**Learned:**
- Ask when a request has several readings that lead to different code. The round trip cost one message, and guessing would have cost a branch.
- A milestone's text is a starting point. When the user changes its intent mid-milestone, the change belongs in `decisions.md` and in `CLAUDE.md`, so the checklist at closing matches what was asked for.
- Keep anything a device decides (sample format, channels) out of the code that makes the sound. The synthesis is pure numpy and fully tested without audio. Only `sound.py` knows about the mixer.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 331 (+47 since 0.3.0) | `uv run pytest --co`; new or grown: menus 19, saves 18, synth 10, settings 9, sound 4, tst 29 |
| Levels | 8/8 pass against their references | `uv run nandsim test --impl reference chips/` |
| Source LOC | 5701 (gui 4087, netlist 696, testing 371, hdl 362, sim 81); +625, of which gui +566 | non-blank lines of `src/**/*.py`, same script for v0.3.0 (5076) |
| Test LOC | 2736 (+344) | non-blank lines of `tests/**/*.py` |
| Work since 0.3.0 | 5 merged PRs (#21–#25), 17 commits | `gh api …/pulls`, `git log --no-merges v0.3.0..main` |
| Sounds | 8 effects, 1.79 s of audio in all (78,850 samples at 44.1 kHz) | `synth.render` on every recipe |
| Sound startup | 10 ms to synthesize all; 17 ms to open the mixer and build the `Sound`s | `time.perf_counter()` around `synth.render` and `Sounds.load()`, dummy audio driver |

**Next:** milestone 5, Buses (4, 8 and 12 bits): Not4, And4, Or4, Xor4, Mux4, Mux8, Mux12, Or4Way, Mux4Way4, Mux8Way4, Mux4Way12, DMux4Way, DMux8Way. It starts with Not4, the first level with a bus. Its brief and the tour should introduce `a[i]` and `a[0..3]` slices and show bus values in hex.
