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
- **Engine cost scales with depth, not gate count.** Each level costs about 3.4 µs of fixed numpy overhead, so a 4096-gate netlist 3 levels deep runs at about 148 M gate-evals/s, while a 257-gate chain 257 levels deep manages only about 0.3 M. Milestone 6's single-cycle CPU will be a few hundred levels deep, which points to roughly 1 kHz before builtins. The levers, in order: builtins for wide, deep blocks (adder, ALU, RAM, register file), then merging small levels or compiling level schedules.
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
- **Layout quality degrades on large, deeply connected chips.** The 64-part ripple chip has about 2500 wire crossings. Correct and fast, but hard to read. Milestones 3–4 (32-bit buses, adders, ALU) will make this the main GUI issue. The levers: better track ordering in channels, dummy-node straightening, and highlighting the hovered net across the whole canvas.

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

Then milestone 3, buses: Not32, And32, Or32, Mux32, Or8Way, Mux4Way32, Mux8Way32, DMux4Way, DMux8Way. Improving layout readability for 32-bit chips comes with it.
