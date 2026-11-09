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

## Milestone 5 — Buses (2026-11-06)

**Built:** the chips that move the 4004's values around, and the UI to work with them.
- **13 bus levels** in a new *Buses* group, at the 4004's widths: Not4, And4, Or4, Xor4 (4-bit bitwise); Mux4, Mux8, Mux12 (2-way, 4/8/12 bits); Or4Way; Mux4Way4, Mux8Way4, Mux4Way12; DMux4Way, DMux8Way. Each has a stub, a brief, a `.tst` and a hidden reference. Pins follow nand2tetris (`sel = 0` picks `a`). Each level lists only the gate it widens or combines, so Not4 opens as soon as Not is solved.
- **Typing an input's value** on the circuit: **Enter** or a digit over an input opens a small field that takes `.tst` syntax (`13`, `-1`, `0b1101`, `0x0D`) through a new `testing.parse_pin_value`, with the same error messages. A 12-bit input no longer takes thousands of clicks.
- **A sidebar for many levels:** groups fold (the current one and the next with a level to play are open by default), and the list scrolls past the room the brief needs, keeping the current level in sight.
- **The tour** teaches typing a value (Hello) and exporting a chip and the *Your chips* list (And), and mentions folding groups.
- **Tips for bus errors:** a wrong width on a pin or in a connection, a slice past the last bit, and a partly connected bus.

**Problems and how they were solved:**
- *A list that outgrew its sidebar.* The milestone's analysis predicted that 21 levels would push the brief off the 860 px window. Folding groups (#27) helped until the bus levels arrived: solving Not opens Not4, so Gates and Buses are open together, 22 rows, and And's brief lost its table and hint. A fixed half of the sidebar for the list still cut And's hint. The list now gets what the brief leaves, in whole rows and never fewer than 5, and scrolls past it (#31).
- *Keys that mean two things.* With the value field open, `x`, `b` and `h` must be typed, not fire X (undefined) or H (hex). The field takes every key while open, and in the game it sees Esc before the pause menu does. Writing the tour playtest showed that after the new step, Ctrl+Enter over an input opened the field instead of doing nothing; modified keys no longer open it.
- *A bubble over what you type.* The Hello bubble covered the value field's hint. It showed only in a screenshot, since the tests passed. The bubble now keeps clear of the field as well as of its anchor.
- *Tests that prove something.* The muxes are too wide to test every input. Their `.tst` files check every `sel` with distinct inputs, then one bit set or cleared on the chosen input, then seeded random rows. Seven plausible wrong solutions (swapped `sel` bits, crossed bits, a stuck bit, outputs in the wrong order, a missing input) each failed 1 to 57 checks before the levels were committed.
- *A message that didn't match.* The first width-mismatch tips never fired: the error says `has 1 bit but 'in' has 4`, with a unit only after the first number. Pinning each tip to a real error from a bus level caught it at once.
- *Parallel branches.* Two branches each appended an entry to `docs/decisions.md`. The second was brought up to date by merging `main` rather than rebasing, which would have needed a force-push.

**Learned:**
- Look at the screen. Two of this milestone's problems (the cut brief, the covered field) passed every test and showed only in a screenshot.
- Size UI by its content, not by ratios: the brief's real height decided the list's, which a share of the window couldn't.
- A test file is only as good as the wrong answers it rejects. Running a few plausible mistakes against generated tests costs minutes and shows what they actually check.
- Tips and messages drift apart unless a test ties them together.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 438 (+107 since 0.4.0) | `uv run pytest --co -q` |
| Levels | 21/21 pass against their references (13 new, 1,366 checks in the bus `.tst` files) | `uv run nandsim test --impl reference chips/` |
| NAND count (depth) per bus reference | Not4 4 (1), And4 8 (2), Or4 12 (2), Xor4 16 (3), Mux4 32 (5), Mux8 64 (5), Mux12 96 (5), Or4Way 9 (4), Mux4Way4 96 (9), Mux8Way4 224 (13), Mux4Way12 288 (9), DMux4Way 15 (5), DMux8Way 35 (7) | `elaborate()` on each reference: `gate_count` and `len(levels)` |
| Engine on the widest bus chip | Mux4Way12, 288 NAND, depth 9: 28.5k evals/s (8.2 M gate-evals/s); elaboration 9 ms; top-level layout 0.6 ms | `Simulator.eval()` in a loop for 2 s with `sel` changing, `layout(build_view(...))` averaged over 20 runs; Python 3.12.3, this laptop |
| Source LOC | 6068 (gui 4440, netlist 696, testing 385, hdl 362, sim 81); +367 since 0.4.0, of which gui +353 | non-blank lines of `src/**/*.py` at HEAD and at v0.4.0, same script |
| Test LOC | 3284 (+437) | non-blank lines of `tests/**/*.py`, same script (it counts 2847 at v0.4.0) |
| Work since 0.4.0 | 6 merged PRs (#27–#32), 13 commits | `gh pr list`, `git log --no-merges v0.4.0..HEAD` |

**Next:** milestone 6, Arithmetic: HalfAdder, FullAdder, Add4 with carry in and out, Inc4, Inc12 for the program counter, and the 4004's ALU (add and subtract with carry/borrow, increment and decrement, complement, rotate through carry, DAA, KBP, TCS, and the zero and carry flags JCN tests). It starts with an analysis of the ALU's operations and flags against Intel's MCS-4 manual, then the adders, which are ordinary levels.

## Milestone 6 — Arithmetic (2026-11-07)

**Built:** the arithmetic of the Intel 4004, in a new *Arithmetic* group of 10 levels.
- **Adders:** HalfAdder, FullAdder, Add4 (`a[4], b[4], cin` → `out[4], cout`, the datapath of `ADD`), Inc4 (`INC` and `ISZ` on a register, no carry) and Inc12 (the program counter, from three chained Add4s).
- **The 4004's quirks, one level each:** AddSub4 subtracts as `SUB` does, `a + ~b + ~cin`, where a carry of 1 means *no borrow*. Rotate4 is `RAL` and `RAR` through the carry. Daa4 adds 6 when the digit is over 9 or the carry is set, and never clears the carry. Kbp4 maps a one-hot key row to 1–4, with 15 for errors.
- **The ALU:** `a[4], b[4], cin, op[4]` → `out[4], cout, zr`. Ops 0–12 are the low digit of the accumulator group `F0`–`FC`, so the CPU can pass it straight in. 13 is LD (`out = b`), so every accumulator write can go through the ALU. 14 and 15 are ADD and SUB. Its decision entry records the interface, since the CPU, the emulator project and saves will depend on it.
- **The sidebar** names the group "Arithmetic", and a test now checks that every brief's tables fit the sidebar.

**Problems and how they were solved:**
- *A manual that wasn't there.* The analysis meant to check the ALU against Intel's MCS-4 manual, but its URL returned 404. Sources disagreed on DAA (does a set carry alone trigger +6?). The pyntel4004 docs, which quote the manual, settled it: +6 if A > 9 **or** CY, and the carry is never cleared. They also confirmed SUB, DAC, TCS and KBP. The decision entries name the source for each rule, and say the semantics should be checked against the manual if a copy turns up.
- *Briefs that looked fine in Markdown.* Three ways a brief went wrong, each seen only in a screenshot:
  - Hard-wrapped paragraphs broke early, because the renderer treats each source line as a paragraph.
  - Two tables were wider than the sidebar and silently lost their last column.
  - The ALU's brief pushed its own hint off the bottom.

  The first two now have rules (one line per paragraph, narrow tables), and the second has a test against the sidebar's real width in characters. The third was fixed by shortening the brief.
- *Tests of the tests.* As in milestone 5, plausible wrong solutions were run against each new `.tst`: 9 for the adders, 12 for the part levels, 15 for the ALU. All fail. One "wrong" Rotate4 passed at first. It was a broken mutant (it muxed a result with itself), not a weak test, and a real direction swap fails. A smoke-test "error" that didn't show was likewise valid HDL (`carry[0]` on a 1-bit wire).
- *One model for two generators.* The ALU's `.tst` generator imports the part levels' model rather than re-deriving DAA and SUB, so the ALU and its parts can't disagree on the 4004's semantics.
- *An ALU four times the size of anything before it.* The estimate was 400–600 NANDs; the reference is 1,319. Nearly 450 of them choose a single carry bit through two Mux8Way4s, the trick the hint teaches. It stays, since CLAUDE.md says not to optimize early, and a builtin ALU with its equivalence test is the plan if the CPU needs the speed.

**Learned:**
- Get the semantics from a source before writing a reference. Two of the 4004's rules (SUB's inverted borrow, DAA's sticky carry) are the opposite of what most CPUs do, and a reference written from habit would have made the tests reject correct chips.
- Small levels before a big one: AddSub4, Rotate4, Daa4 and Kbp4 each carry one quirk, so the ALU level is only about choosing by `op`.
- A rule that only lives in someone's head gets broken. The brief layout rules are now in a test and a decision entry.
- Check a test-of-the-test before trusting it: a mutant that passes may be a no-op.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 489 (+51 since 0.5.0) | `uv run pytest --co -q` |
| Levels | 31/31 pass against their references (10 new, 9,221 checks in the arithmetic `.tst` files, 5,856 of them the ALU's) | `uv run nandsim test --impl reference chips/` |
| NAND count (depth) per arithmetic reference | HalfAdder 6 (3), FullAdder 15 (7), Add4 60 (19), Inc4 24 (9), Inc12 180 (51), AddSub4 80 (22), Rotate4 40 (5), Daa4 71 (23), Kbp4 33 (8), ALU 1,319 (42) | `elaborate()` on each reference: `gate_count` and `len(levels)` |
| Engine on the ALU | 6.4k evals/s (8.5 M gate-evals/s, the same per-gate rate as Mux4Way12 in 0.5.0); elaboration 36 ms; the 1,952-row ALU `.tst` runs in 0.55 s | `Simulator.eval()` in a loop for 2 s with `op`, `a` and `cin` changing; `elaborate()` averaged over 10 runs; `time nandsim test` on `ALU.tst`; Python 3.12.3, this laptop |
| Source LOC | 6075 (gui 4447, netlist 696, testing 385, hdl 362, sim 81); +7 since 0.5.0, all in gui | non-blank lines of `src/**/*.py` at HEAD and at v0.5.0, same script |
| Test LOC | 3294 (+10) | non-blank lines of `tests/**/*.py`, same script |
| Work since 0.5.0 | 3 merged PRs (#34–#36), 8 commits | `git log --merges` and `git log --no-merges v0.5.0..HEAD` |

Almost all of this milestone is level data rather than code: 10 stubs, briefs, references and `.tst` files, plus three decision entries.

**Next:** milestone 7, Sequential logic. It starts with the DFF in the GUI and the `tick`/`tock` commands in `.tst`, which `docs/tst.md` already promises. Then come Bit and Register4/8/12, the index register file (16 × 4, also as 8 pairs), the PC with its 3-level stack (Inc12 is ready for it), RAM up to the 4002 layout, a 4096 × 8 ROM, and clock controls. The `.tst` format will need a way to load ROM contents before milestone 8.

## Milestone 7 — Sequential logic (2026-11-08)

**Built:** memory, in a new *Memory* group of 14 levels, and the clock to drive it.
- **The clock:** `tick` and `tock` in `.tst`, with failures that name their cycle. A clock panel in the GUI (step, run at 1–1000 cycles/s, reset, speed) that keeps the stored bits across a rebuild when every DFF is still where it was.
- **Flip-flops from NAND.** The engine now simulates feedback loops, and HDL can read the clock as `clock`. The player builds SRLatch, DLatch and the DFF itself. Every DFF part after that runs as the engine's DFF, a built-in shown as `DFF (built-in)`, and B swaps the player's own DFF back in, down to its latches.
- **The 4004's storage:** Bit, Register4/8/12, IndexRegs (16 × 4, also as 8 pairs), PC (12-bit counter with the 3-level address stack, wrapping as on the chip), and RAM8, RAM64, RAM4002, RAMBank and DataRAM. The last is all 2,560 characters a 4004 can address, picked by `SRC` and `DCL`.
- **Plan changes, recorded as decisions:** the program ROM and its editor moved after the CPU (#49), and a milestone 9, the Busicom 141-PF calculator, became the end of the game (#48).

**Problems and how they were solved:**
- *A DFF the player never built.* Midway, the user decided the player should build flip-flops too. That broke two rules in CLAUDE.md: loops without a DFF were errors, and DFF was a primitive. The work came in three PRs.
  - #50, the engine. Loops are found as strongly connected components, but only among the gates that plain levelization can't order, so chips without loops are untouched. Each loop runs in vectorized unit-delay rounds until it settles. Unit delay matters: with one delay per gate, a master–slave flip-flop locks its closing latch before new data can race through, as real gates do. A loop that won't settle is set undefined and settled again from there, which three-valued logic guarantees to finish.
  - #51, the levels.
  - #52, the switch back to the player's DFF.
- *The latch DFF is about 7× slower than the primitive* (measured below). So a part named `DFF` stays the primitive once the DFF level passes. An equivalence test runs both on random sets, ticks, tocks and evals. They differ in one documented case, an `eval` between tick and tock with a new input, which no test and no GUI action produces.
- *DataRAM took 7.4 s to build.* Elaboration re-checked every instance of a chip. Since #46, each chip is compiled once into a template and stamped out, and levelization runs as numpy frontiers instead of a loop per gate. DataRAM now builds in about 0.1 s and shipped in HDL, without waiting for a builtin.
- *A DFF leaked into early exports.* Review of #38 found a one-DFF chip exportable from Not, usable in every level. Exports may now use a primitive only once an unlocked level lists it, checked on the flattened netlist (#39).
- *A clock that kept values on the wrong DFF.* Review of #40 found that carrying state across a rebuild one path at a time put a register's high bit into its low bit. State is now carried only when every DFF path is unchanged.
- *Tests that passed wrong chips.* As in earlier milestones, wrong versions were run against every new `.tst`. Several reached the fix only that way:
  - DataRAM's first sampled test let a stuck `status` bit and a bank-7-for-0 swap pass (shift 7, from the review of #47).
  - DFF's test needed checks after the tick, while the clock is low and between tick and tock: each one fails a different single-latch design.
- *Messages that blamed the wrong thing.* Review of #52 reproduced two:
  - B claimed "your DFF" when no DFF HDL existed.
  - B blamed the player's DFF for the chip's own error.

  Both are now refused with an accurate message, each with a regression test.

**Learned:**
- A rule in CLAUDE.md is the user's to change. The analysis named both rules this would break and asked first. Then the change went in small, merged steps, each green.
- Simulation semantics decide correctness, not just speed. Zero-delay settling in level order would have let data race through a flip-flop; unit-delay rounds get it right for the same reason hardware does.
- A stand-in needs an equivalence test with its exceptions spelled out, or "the same, only faster" is a promise nobody checked.
- For each new check, write the wrong chip it is meant to catch. Several tests in this milestone looked thorough and weren't, until a specific mutant passed them.
- Messages are behaviour too. Both bugs found in the review of #52 were wrong *messages*, not wrong circuits, and only a reproduction showed them.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 664 (+175 since 0.6.0) | `uv run pytest --co -q` |
| Levels | 45/45 pass against their references (14 new, 5,574 checks in the Memory `.tst` files, 1,920 of them RAMBank's) | `uv run nandsim test --impl reference chips/` |
| Reference size (NANDs, DFFs) | SRLatch 4, DLatch 9, DFF 19 (latches only, 2 loops); Bit 9 + 1 DFF; Register12 108 + 12; IndexRegs 1,169 + 64; PC 1,620 + 50; RAM4002 5,803 + 320; RAMBank 23,323 + 1,280; DataRAM 186,843 + 10,240 | `elaborate()` on each reference: `gate_count`, `dff_count`, loop count from `Netlist.levels` |
| Clock speed, built-in DFF | Register12 24.4k cycles/s, IndexRegs 7.1k, PC 1.8k, RAM4002 3.8k, RAMBank 2.1k, DataRAM 557 cycles/s; DataRAM builds in 97 ms | `Simulator.tick()` + `tock()` in a loop for 1.5 s with every input changing each cycle; `elaborate()` timed once; Python 3.12.3, this laptop |
| Clock speed, the player's DFF (B) | Register12 6.4k, IndexRegs 1.5k, PC 417, RAMBank 390, DataRAM 63 cycles/s (371,163 NANDs), 4–9× slower | same loop, `ChipLibrary(builtins=False)` |
| Source LOC | 6,974 (gui 4,824, netlist 1,027, testing 424, hdl 372, sim 223), +899 since 0.6.0 | non-blank lines of `src/**/*.py` at HEAD and at v0.6.0, same script |
| Test LOC | 4,486 (+1,192) | non-blank lines of `tests/**/*.py`, same script |
| Work since 0.6.0 | 15 merged PRs (#38–#52), 41 commits | `git log --merges` and `git log --no-merges v0.6.0..HEAD` |

The real 4004 runs about 92.5k instruction cycles per second. The CPU will be several times DataRAM's size in its datapath alone, so DataRAM's 557 cycles/s is the number to watch. The builtins planned for RAMBank and the ALU, each with its equivalence test, are the likely next step for speed.

**Next:** milestone 8, the Intel 4004. It starts with the `.tst` command that attaches a program memory, held by the runner, to the CPU's ROM pins, since the ROM levels now come in milestone 9. Then the instruction decoder and the two-cycle instructions (`JCN FIM JUN JMS ISZ`, and `FIN`), from the parts already built: ALU, IndexRegs, PC and DataRAM. The goal is a hand-assembled BCD addition checked in RAM. The journal must report the CPU's simulated clock against 92.5k cycles/s.

## Milestone 8 — CPU: the Intel 4004 (2026-11-09)

**Built:** the Intel 4004, on its own 16 pins, in a new *CPU (4004)* group of 10 levels, and the memories around it in `.tst` files.
- **The CPU on the 4004's pins:** `IN din[4], test, reset; OUT dout[4], drive, sync, cmrom, cmram[4]`. It is the multiplexed bus split by direction, with 8 clock periods per instruction cycle (A1 A2 A3 M1 M2 X1 X2 X3), and 16 for `JCN FIM JUN JMS ISZ` and `FIN`. All 46 instructions run with the 4004's encodings (#56, #62).
- **Ten levels up to it:**
  - **First, Timing, Cond, CmLines and InstrReg:** the 8 periods, JCN's condition, DCL's CM-RAM lines, and the instruction from the bus (#58–#60).
  - **Then five units:** Sequencer, Accumulator, Registers, Jumps, BusOut. Each decodes OPR and OPA itself.
  - **Last, the CPU:** 16 parts that give each unit its moment (#62).
- **Memories in tests:** `attach mcs4` puts sixteen 4001 ROMs and eight banks of 4002 RAMs, with their I/O ports, on a chip's bus pins, played by the runner (#55, #57). `.tst` gained `rom`, `set romport`, `expect ram`, `expect ramstatus`, `expect romport`, `expect ramport` and `cycles <n>`. A CPU that breaks the bus protocol fails at the period where it happens.
- **An instruction-level 4004 model and assembler** in `tools/`, checked against Intel's *MCS-4* manual. It generates the CPU's tests, and those of the five units (#61).
- **The CPU test:** one program that runs all 46 instructions, then Intel's own 16-digit decimal addition from the manual (section IV B), checked in RAM and on the ports. A test now fails if the program stops using any of the 46 (#66).
- **Playing it:** the CPU level's clock panel runs the player's CPU on the MCS-4 memories with a demo, a decimal counter in RAM, and shows the period, the counter and the ports (#63).
- **The computer's chips get their own groups,** starting with *RAM (4002)*. It holds the five RAM levels, which moved after the CPU and open once it is solved (#54, #65).
- **Around the game:**
  - The tour now tells the 4004's story, with one bubble opening each group, and the briefs say where each chip goes in the CPU (#65).
  - The sidebar sizes itself to the window, exported chips open in the editor, and the editor scrolls sideways (#64).
  - A background soundtrack plays from four supplied tracks (#67).

**Problems and how they were solved:**
- *What "compatible at the pins" means in a logic simulator.* The real 4004 has a two-way bus and two-phase clocks. The CPU splits the bus into `din`, `dout` and `drive` in positive logic, with one simulated clock cycle per 4004 clock period (#56). Intel's figures, read from the scanned manual's page images, settled what the text didn't: SYNC during X3, and the CM-RAM line active at A3 with CM-ROM. The latter corrected an earlier decision (#58).
- *Tests that need a 4004 to write.* Hand-written expected values wouldn't scale to 46 instructions. A Python model, kept outside the game, computes them, and refuses to guess where the hardware wouldn't define a value: RAM never written, missing SRC, undefined opcodes.
  - Intel's decimal routine is assembled from its source. The manual's octal column disagrees with its own source (`JUN NEXT` printed as 0310).
  - The model also confirmed, from the manual itself, the ALU semantics that milestone 6 had taken from pyntel4004.
- *Reset and the index registers.* The 4004 clears its registers over 8 instruction cycles of RESET, sweeping them with its refresh counter. In a simulator where every DFF powers up undefined, no logic can derive a defined sweep from all-undefined state and a constant input. The CPU first shipped with undefined registers after reset. The user then chose to change the milestone 7 level: IndexRegs got a `reset` pin. Players with 0.7.0 saves were told how to update theirs.
- *One CPU level was too big.* The first reference was about 110 parts. The user chose a split into functional units over a single Decoder level or a Datapath/Control pair. Each unit decodes the instruction itself, so its brief is about the 4004's instructions, not about control lines invented for one design. The CPU itself is now 16 parts, mostly timing.
- *A test that claimed more than it checked.* The CPU test said "all 46 instructions", but never ran `RD1` or `RD2`, and cleared what `RD3` read before checking it. This was found while checking this milestone. The program now reads all three status characters back into RAM, and a guard test fails if it ever drops a mnemonic again. Run against the old generator, the guard reports exactly `RD1` and `RD2` (#66).
- *Wrong CPUs that pass.* As in earlier milestones, each test was run against wrong chips. For the CPU there were ten, including:
  - the PC stepping at A2;
  - SRC's halves swapped;
  - FIN fetching from the PC;
  - no CM lines at M2;
  - `sync` at X2;
  - ISZ jumping on zero.

  Each unit's test has its own list in `docs/decisions.md`.

**Learned:**
- The manual is the spec, and its figures carry facts that its prose leaves out. Read the page images, not a summary.
- A model that refuses to guess is worth more than one that always answers. Every refusal marks a value a test must not depend on.
- Check a "covers everything" claim mechanically. A count of mnemonics would have caught `RD1`/`RD2` on day one.
- Split a big level where the domain splits it. Units named after what the 4004 does gave briefs a player can follow, at the cost of a few repeated DMux8Ways.
- Some hardware behaviour can't be modelled as the chip does it: a power-on sweep from unknown state is one. Say so, and let the user choose the trade-off.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 823 (+159 since 0.7.0) | `uv run pytest --co -q` |
| Levels | 55/55 pass against their references (10 new in CPU (4004); the CPU group's `.tst` files hold 13,013 checks, 131 of them the CPU's own over 7,776 clocks) | `uv run nandsim test --impl reference chips/` |
| Reference size (primitives + DFFs, levels deep) | Timing 92 + 4 (15); Cond 27 (14); CmLines 15 (7); InstrReg 172 + 16 (14); Sequencer 110 + 1 (27); Accumulator 1,672 + 9 (61); Registers 1,431 + 64 (51); Jumps 1,900 + 50 (75); BusOut 482 (28); **CPU 5,908 + 144 DFFs, 84 levels** | `elaborate()` on each reference: `gate_count` less DFFs, DFF count, `len(Netlist.levels)` |
| CPU build | 69 ms | `elaborate()` of the reference CPU in a fresh process, timed once |
| **CPU clock speed, in the game** | **2,236 clocks/s = 279 instruction cycles/s, 1/331 of the real 4004's 92.5k** (740 kHz, 8 clocks per instruction cycle) | `ChipSession.step()` with the MCS-4 memories attached, running the demo program, as the clock panel does: 3 s loop after 64 reset clocks |
| CPU clock speed, raw | 1,473 cycles/s with every input random each cycle; units: Timing 9,330, InstrReg 9,408, Registers 2,506, Accumulator 2,196, Jumps 1,678 | `Simulator.tick()` + `tock()` for 1.5 s, inputs set each cycle, seed 4004, as in milestone 7 |
| CPU test run | 7,776 clocks in 3.8 s, including Python startup and elaboration (about 2,070 clocks/s) | `nandsim test --impl reference chips/05_cpu/CPU.tst`, wall time |
| Source LOC | 7,929 (gui 5,250, netlist 1,027, testing 949, hdl 372, sim 227, top level 104), +955 since 0.7.0 (testing +525 for the memories, gui +426) | non-blank lines of `src/**/*.py` at HEAD and at v0.7.0, same script |
| Test LOC | 5,503 (+1,017) | non-blank lines of `tests/**/*.py`, same script |
| Tools LOC | 1,361: model4004 348, gen_cpu_tst 418, gen_cpu_units 375, gen_ram_tst 220 (only the last existed at 0.7.0) | non-blank lines of `tools/*.py` |
| Work since 0.7.0 | 14 merged PRs (#54–#67), 41 commits | `gh pr list --state merged` and `git log --no-merges v0.7.0..HEAD` |

At 279 instruction cycles per second, the simulated 4004 runs about 331 times slower than the real one. Intel's 16-digit addition, 167 instruction cycles, takes 0.6 s here and 1.8 ms on the chip. The slowest unit is Jumps, which holds the PC, 75 levels deep. The milestone 7 plan still stands: a builtin PC and ALU, each with its equivalence test, are the first candidates if milestone 9's programs need more speed.

**Next:** milestone 9, the Busicom 141-PF. It starts with the decision CLAUDE.md asks for: keyboard, printer, which program, and how many 4003s. The ROM levels follow in their own *ROM (4001)* group (a 4096 × 8 program ROM in the 4001 layout, with a write port), then the 4001's and 4002's bus logic, so the player's own memories plug into the CPU's pins, then the in-game ROM editor.
