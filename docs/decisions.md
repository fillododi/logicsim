# Decisions

Ambiguous spec points and the option chosen. Newest last.

## 2026-11-06 — The player writes chips in the in-game editor
**Context:** CLAUDE.md originally had Claude writing the whole chip library.
**Decision:** NAND Sim is a game. The player writes each chip's HDL in an editor inside the GUI and never edits repo files. Claude ships the levels.
**Alternatives:** the player edits `.hdl` files on disk (rejected: not a game); Claude writes the full library (rejected: nothing left to play).
**Consequences:** milestone 2 includes an editor with inline errors, saves and a level select. File hot reload is only a developer convenience.

## 2026-11-06 — Level layout: chips/ for definitions, reference/ for hidden solutions
**Context:** each level needs a solution to validate its tests, but the player must not see it.
**Decision:** `chips/<NN_group>/<Name>.{hdl,md,tst}` hold the interface stub, the brief and the tests; `chips/levels.toml` holds the unlock order and allowed parts; `reference/<NN_group>/<Name>.hdl` holds the solution. The done gate runs every `.tst` against `reference/`.
**Alternatives:** solution next to the stub (rejected: too easy to leak into the GUI).
**Consequences:** the GUI loads only from `chips/` and the save dir; `nandsim test --impl reference|save` picks the implementation.

## 2026-11-06 — Player saves live in a user data dir
**Context:** player progress must not dirty the repo.
**Decision:** default `~/.local/share/nandsim/save/`, overridable with `--save-dir` (tests use a temp dir).
**Alternatives:** a `saves/` folder in the repo (rejected: mixes player data with source).
**Consequences:** solved chips are looked up in the save dir when used as parts in later levels.

## 2026-11-06 — Three-valued wires: value and known bit-planes
**Context:** the GUI must colour wires as 0, 1 or undefined, so the engine needs an undefined state.
**Decision:** each net has two numpy boolean planes, `value` and `known`. NAND follows Kleene logic: a known 0 on any input gives a known 1; all inputs known gives the normal result; otherwise undefined. DFFs and unset inputs start undefined.
**Alternatives:** two-valued wires that start at 0 (rejected: the undefined colour would need an engine rewrite later).
**Consequences:** roughly twice the work per gate; `.tst` output checks fail on undefined outputs with a dedicated message.

## 2026-11-06 — Bit-level levelized engine with a primitive table
**Context:** CLAUDE.md requires levelized, vectorized numpy evaluation.
**Decision:** elaboration flattens every chip to single-bit primitives. Gates are grouped by topological level; each level is evaluated with one vectorized operation over index arrays. Buses exist only in the HDL and netlist layers, as lists of bit indices. Primitives are looked up in a table rather than hard-wired, so Python builtins (RAM, register file) can plug in later.
**Alternatives:** word-level evaluation of buses (rejected for now: more complex, premature).
**Consequences:** large memories made of DFFs are slow; builtins handle them once their HDL version passes.

## 2026-11-06 — Workflow through project skills
**Context:** every change should follow the same steps.
**Decision:** work on branches and use `/analyze → /make-change → /verify → /pr → /review`, and `/milestone` to close a milestone. `main` is protected and requires green CI.
**Alternatives:** ad-hoc commits on `main` (rejected: no review point).
**Consequences:** every change lands through a PR.

## 2026-11-06 — Changelog and versioning
**Context:** the user asked for a changelog; releases needed a numbering scheme.
**Decision:** `CHANGELOG.md` in Keep a Changelog format. Every user-visible change adds a line under `[Unreleased]` in the same PR. Each milestone is a release `0.N.0`, tagged `v0.N.0` (replacing the earlier `mN` tags, which were never created).
**Alternatives:** generating the changelog from commit messages (rejected: commits explain *why* for developers, release notes speak to players); separate milestone and version tags (rejected: redundant).
**Consequences:** `/make-change` writes the entry, `/review` checks it, `/milestone` cuts the release and bumps `pyproject.toml`.

## 2026-11-06 — The `.tst` format
**Context:** CLAUDE.md requires truth tables, sequential scripts and values in three bases, but leaves the syntax open.
**Decision:** a line-based format of our own: `chip`, `table … | … end`, `set`, `eval`, `expect`. Values may be decimal (negatives in two's complement), `0b`, `0x`, or `*` for don't care. A table row expands to set, eval and expect. `tick` and `tock` are parsed and rejected until milestone 5.
**Alternatives:** the nand2tetris `.tst` + `.cmp` pair (rejected: two files per test and fixed-width output columns are awkward to write and to read in error messages).
**Consequences:** failures point at the exact row and print actual values in the base the expected value was written in.

## 2026-11-06 — HDL errors stop at the first problem
**Context:** the parser and elaborator could try to recover and report many errors.
**Decision:** raise one `HdlError` with `file:line:col` at the first problem.
**Alternatives:** error recovery that collects several errors (rejected for now: complex, and cascades confuse beginners).
**Consequences:** the editor underlines one spot at a time. Collecting several errors can be added later without changing the message format.

## 2026-11-06 — Unconnected part inputs are errors
**Context:** nand2tetris silently ties unconnected part inputs to false.
**Decision:** an unconnected part input, or any unconnected bit of one, is an error. Write `false` to mean false.
**Alternatives:** default to false (rejected: hides a common beginner mistake).
**Consequences:** HDL is slightly more verbose; mistakes surface at the line that makes them.

## 2026-11-06 — Chips may read their own OUT pins
**Context:** nand2tetris forbids feeding an output pin back into a part, which forces an extra internal wire.
**Decision:** allowed. In a flattened netlist an output pin is just a net.
**Alternatives:** forbid it as nand2tetris does (rejected: an arbitrary rule with no hardware reason).
**Consequences:** none for the engine; one less error for players to meet.

## 2026-11-06 — Levels list their allowed parts explicitly, and keep the stub's pins
**Context:** a level must be solved with earlier chips, not with the chip itself or a later one.
**Decision:** each `[[level]]` in `chips/levels.toml` has a `parts` list. The runner rejects any other part used directly by the top chip, and rejects an implementation whose `IN`/`OUT` differ from the stub. A pytest guard checks that every allowed part is a primitive or an earlier level.
**Alternatives:** derive the allowed parts from the unlock order (rejected: some levels will want to restrict parts on purpose).
**Consequences:** sub-chips are not re-checked: they passed their own level.

## 2026-11-06 — Level data packaged as `nandsim/_data`
**Context:** an installed wheel has no repo, but `chips/` and `reference/` live at the repo root.
**Decision:** hatch `force-include` copies them to `nandsim/_data/`. `nandsim.paths.data_root()` uses that directory when present, and the repo root otherwise. CI runs every level from an installed wheel.
**Alternatives:** move the data into `src/nandsim/` (rejected: buries the levels deep in the package tree, where they are awkward to edit and review).
**Consequences:** the reference solutions ship inside the wheel. They are hidden from the GUI, not secret.

## 2026-11-06 — Unlocking follows the parts a level may use; solved is sticky
**Context:** the GUI needs a progression rule. The user chose part-based unlocking.
**Decision:** a level is unlocked when every non-primitive chip in its `parts` list is solved. A level counts as solved once its tests pass, and stays solved. Progress is stored in `progress.json` (`{"version": 1, "solved": [...]}`) next to the `<Name>.hdl` saves. An unreadable progress file is moved aside to `progress.json.bad`, and the player starts fresh.
**Alternatives:** strictly linear unlocking (rejected by the user: less freedom); solved status that is recomputed on every run (rejected: breaking And while experimenting would re-lock Xor).
**Consequences:** later levels use the player's own chips, so a broken saved And makes Xor's tests fail, as it would in real hardware. The save format is versioned so it can evolve.

## 2026-11-06 — Bundle DejaVu Sans Mono for the GUI
**Context:** the editor and circuit labels need a monospace font. On the dev machine, `pygame.font.SysFont("monospace")` returned a proportional font (`i` 8 px, `W` 9 px).
**Decision:** ship DejaVu Sans Mono (Bitstream Vera licence, redistributable) as package data, with its licence file. It is added together with the viewer in milestone 2.
**Alternatives:** system font lookup (rejected: not monospace on every machine); pygame's default font (rejected: proportional).
**Consequences:** about 340 KB more in the wheel; identical text metrics everywhere, which the layout's `Style.char_w` relies on.

## 2026-11-06 — GUI model, layout and saves are pure Python
**Context:** most GUI logic needs no display, and testing it through pygame would be slow and fragile.
**Decision:** `nandsim.gui.model` (what one hierarchy level shows), `nandsim.gui.layout` (Sugiyama-style layout with orthogonal routing) and `nandsim.gui.saves` live in the gui package but never import pygame. A boundary test enforces this, and another test forbids any GUI reference to the hidden solutions.
**Alternatives:** a separate top-level package (rejected: they serve only the GUI); putting everything in pygame widgets (rejected: untestable without a display).
**Consequences:** the pygame layer only draws and handles events. Layout quality can be improved and measured (`layout.crossings`) without opening a window.

## 2026-11-06 — Viewer interactions and reload behaviour
**Context:** CLAUDE.md asks for clickable inputs, hierarchical navigation, zoom/pan and hot reload, without fixing the details.
**Decision:**
- Inputs: left click toggles a bit, or counts a bus up. Right click counts down. `X` makes the hovered input undefined, so players can explore three-valued logic. Inputs are only set at the top level; inner levels show what the parent drives.
- Navigation: a single click opens a part, and breadcrumbs or Backspace go back up. The view refits on every navigation.
- Zoom: the wheel zooms at the cursor. Dragging with the left button pans, and a press that moves less than 4 px counts as a click.
- Hot reload: every `.hdl` under the search dirs is polled twice a second. A failed reload keeps the last circuit that compiled and shows the error as a banner. Inputs are kept by pin name, and the view returns to the nearest hierarchy level that still exists.
- Developer mode: `nandsim gui FILE` searches for parts next to the file and one directory up (`--search` overrides this). Without a file, the command explains that the level select comes later.
**Alternatives:** double-click to open parts (rejected: slower to explore); inputs settable at any level (rejected: they would contradict the parent's wiring); file-system events instead of polling (rejected: platform-specific, and polling a few files is cheap).
**Consequences:** the session layer (`gui/session.py`) owns all of this and is pure Python, so the editor PR reuses it by swapping the file loader for one that reads the editor's text.

## 2026-11-06 — Editor behaviour
**Context:** players write every chip in the in-game editor, which is built from scratch on pygame (no new dependency).
**Decision:**
- **Model and highlighting:** a pure `TextBuffer` (lines, cursor, anchor-based selection, snapshot undo) and a lenient per-line syntax highlighter that never fails on half-typed code.
- **Typing:**
  - consecutive typed characters merge into one undo step until a space, newline or other command;
  - Enter keeps the current indentation and adds a level after `{` or `(`;
  - a closing brace typed on a blank line removes one level;
  - Backspace inside the indentation removes a whole level (4 spaces);
  - Tab inserts spaces up to the next tab stop, or indents the selected lines;
  - Ctrl+/ toggles `// ` comments.
- **Movement:** Home goes to the first non-blank character, then to column 0. Word moves treat each symbol as its own stop.
- **Save and errors:** Ctrl+S writes the file atomically and rebuilds. An error whose position is in the edited file is underlined there; errors in other files show only in the banner.
- **Focus:** the editor takes keys while focused, and Esc or a click on the canvas gives them back to the circuit.
- **External edits:** a change on disk replaces the buffer only when it has no unsaved edits.
- **Clipboard:** pygame-ce's `scrap.put_text`/`get_text`, with an in-process fallback for headless runs.

**Alternatives:** compiling on every keystroke (rejected: noisy while code is half-written); tabs for indentation (rejected: spaces keep columns predictable for error positions); an external editor (rejected: contradicts the game model).

**Consequences:** the game PR reuses `EditorWidget` unchanged, with the save handler writing to the player's save dir instead of the opened file.

## 2026-11-06 — Game screen rules
**Context:** the game screen ties the level list, the editor, the circuit and the tests together. A few behaviours needed choosing.
**Decision:**
- **Layout:**
  - left sidebar (260 px): levels grouped by folder, then the brief;
  - centre: the circuit;
  - right: the editor, with a results panel holding a Run tests button.
- **Keys:** Ctrl+S saves and builds the circuit. Run tests (button or Ctrl+Enter) saves, then runs the level's `.tst` against the player's own chips.
- **Switching level:** unsaved text is saved to the level it belongs to before the switch.
- **Locked levels:** they can't be opened. Clicking one explains which chips to solve first.
- **Build errors:** hidden until the player has saved or run that level once (or already has a save for it), so a fresh level doesn't open with an error.
- **Results wording:** "Doesn't build" with the error; "N of M checks failed" with up to 12 failing rows (test line, pin, expected, got, inputs); or "All N checks passed — level solved!" with the levels it unlocked.

**Alternatives:**
- run tests on every save (rejected: noisy while experimenting);
- ask before switching with unsaved text (rejected: a dialog for something saving solves silently);
- open locked levels read-only (rejected: confusing about what can be done).

**Consequences:** the playtest test drives this whole loop with real events, and stays the regression check for future GUI changes.

## 2026-11-06 — Direct connections: `target = source;` and labelled parts
**Context:** the user asked to connect an input straight to an output, and one chip straight to another. Before this, an `OUT` pin could only be driven by a part output, and two parts could only meet through a named wire. Passing a signal through, setting an output to a constant, or reordering bits needed a dummy gate.

**Decision:**
- **Connection statements:** `target = source;` statements inside PARTS. The target is an `OUT` pin, a slice of one, or a new internal wire whose width comes from the source; it can't be an input pin, a constant, or a labelled part's output. The source is any readable signal or constant. They are elaborated as pure aliases (no gates). A chain that loops back to its own target is an error.
- **Labelled parts:** `label: Chip(...)`, whose outputs are readable as `label.pin`, sliced if needed. Labels are unique per chip and can't shadow a pin. Reading a part's input this way, or driving a labelled output, is an error.
- **Level rules:** unchanged. Connections are not parts, so they never count against a level's allowed parts.

**Alternatives:**
- Nested part expressions (`Not(in=Nand(a=a, b=b))`): rejected. They are harder to read, and multi-output parts need names anyway.
- Implicit labels such as `Nand#1.out`: rejected. They are fragile when parts are reordered.
- Keep nand2tetris's rule that only parts drive outputs: rejected. It forces meaningless gates.

**Consequences:** the circuit view tracks drivers per bit, for inputs, labelled outputs and constants too. Wire paths gain `label.pin` entries such as `Top/g1.out`.

## 2026-11-06 — New milestone 3: Tutorial and UI
**Context:** after 0.2.0 the user asked to make the tutorial (agreed in the GUI analysis) and UI work the next milestone. The milestone 2 journal also found that large chips, though correct, are hard to read: about 2500 crossings for 64 parts. The 32-bit chips coming next would make that worse.

**Decision:** insert milestone 3, "Tutorial and UI", and renumber the rest: Buses 4, Arithmetic 5, Sequential logic 6, CPU 7. Releases stay one per milestone (`0.3.0` … `0.7.0`).
- **Scope:**
  - a tutorial level before Not;
  - guide bubbles defined in `chips/tutorial.toml`, completed by player actions, with skip and F1 replay, and progress in `tutorial.json` (so `progress.json` keeps version 1);
  - tips for common build errors;
  - layout readability, hovered-net highlighting, junction dots, and a help line that fits.
- **Renumbering:** text that pointed at future milestones (the `tick`/`tock` message, the DFF note, docs, the milestone skill) now uses the new numbers. Earlier decision entries keep their wording.

**Alternatives:**
- Fold the tutorial into milestone 4: rejected, because it mixes teaching with new content and delays the fix for unreadable large chips.
- A 0.2.x patch series outside the milestones: rejected, because this is enough work to deserve its own checklist and journal entry.

**Consequences:** the CPU is now milestone 7, and the simulated clock speed is reported in its journal entry. The tutorial level shifts which level opens first in a new game. Saves are keyed by chip name, so existing saves keep working.

## 2026-11-06 — Tutorial level: `Hello` in `00_tutorial`
**Context:** milestone 3 asks for a tutorial level before Not whose answer is a single `Nand` line.

**Decision:**
- **The level:** chip `Hello` (`IN a, b; OUT out;`), solved by `Nand(a=a, b=b, out=out);`, in a new group `chips/00_tutorial/` (shown as "Tutorial"). Its brief explains pins and the `Chip(pin=signal)` syntax, and its hint is close to the answer on purpose, since teaching the syntax is the level's job.
- **Optional:** `Hello` allows only `Nand`, and Not doesn't list `Hello` as a part, so Not stays open from the start and solving `Hello` unlocks nothing new.
- **Where a game opens:** it opens the first open level after the furthest solved level (wrapping around), instead of the first open unsolved level. Otherwise a player who skipped `Hello` would land on it every time they start.

**Alternatives:**
- Make Not require `Hello`: rejected, because experienced players would be forced through it.
- Name the chip after what it does (it is a Nand): rejected, because `Nand` is the primitive's name and a second name for the same gate adds nothing. "Hello" says what the level is for.

**Consequences:** `levels.toml` starts with `Hello`. `test_levels_exist` now checks seven names.

## 2026-11-06 — Guided tour: data, anchors, events and progress
**Context:** milestone 3 asks for guide bubbles anchored to UI elements, written as data in `chips/tutorial.toml`. They should advance when the player does what they explain, can be skipped and replayed with F1, and remember what was seen in `tutorial.json`.

**Decision:**
- **One linear tour.** It is a list of `[[step]]` entries with `id`, `text`, `anchor`, `until` and an optional `level`. One bubble shows at a time: the first unseen step tied to the open level or to no level. A step tied to a level only shows, and only listens, while that level is open, so the tour continues in Not and And. Steps waiting on another level don't hold up the open level's steps, so a player who leaves the tutorial early still gets the Not and And bubbles.
- **Anchors** are named UI regions resolved to screen rectangles each frame: `levels`, `level:<Name>`, `brief`, `editor`, `line:<text>` (the first editor line containing the text), `canvas`, `pin:<name>`, `part` (the first part that opens, else any part), `header`, `run_button`, `results` and `footer`. A pin or part that isn't drawn falls back to the canvas. For `line:` anchors the bubble keeps the whole editor row clear, since the player is about to type there.
- **Events** are player actions the game reports: `next` (the bubble's button), `save`, `build_ok`, `toggle`, `open_part`, `up`, `run_tests`, `solved` and `open_level[:<Name>]`. Ctrl+Enter counts as a build too, so a player who skips Ctrl+S isn't stuck. An action no step was waiting for is remembered for the session, per level. When a step whose action already happened comes up, it completes at once: solving Hello before the "run" bubble doesn't make the player run the tests again. A replay forgets these actions.
- **Progress:** `tutorial.json` (`version`, `seen`, `skipped`) sits next to the saves. The tour resumes at the first unseen step. Skip hides it. F1 clears it and opens the first step's level. A corrupt file is set aside as `.json.bad`, as `progress.json` is. A file that can't be read at all (permissions, I/O) only restarts the tour. Either way the sidebar says so, next to any `progress.json` warning.
- **Validation:** loading checks the ids, anchors and events and names the offending step. The game also passes the level names, so a typo in `level`, `level:<Name>` or `open_level:<Name>` is an error at start-up instead of a step that never shows.
- **Gestures:** the bubble swallows a press that starts on it, its release, the wheel, and plain moves over it. Moves also clear the canvas hover. A drag that only passes over the bubble, or ends on it, still reaches the editor or the canvas.
- **Bubbles swallow clicks** that land on them, so a click on a bubble never reaches what lies under it.

**Alternatives:**
- Per-level tours that are independent of each other: rejected for now. A single sequence is simpler to write and to resume, and the `level` field covers what is needed.
- Timed or "click anywhere" advancing: rejected, because the spec wants the player to do the thing.
- Anchors as fixed coordinates: rejected, because they would break on resize and with the automatic layout.

**Consequences:** new UI regions need a named anchor in `GameApp.anchor_rect` and `tutorial.ANCHORS`. `ViewerApp` gained an `on_action` hook (a no-op in the developer viewer).

## 2026-11-06 — A second tutorial level, Wire, before Hello
**Context:** the user asked the tutorial to explain how to connect signals directly (`out = in;`) before introducing the Nand gate.

**Decision:** add a level `Wire` (`IN in; OUT out;`, no parts allowed), solved by the connection `out = in;`, before `Hello` in `00_tutorial`. The tour's first bubbles (welcome, brief, writing HDL, the circuit, toggling an input, running the tests) move to Wire. Hello's bubbles now introduce parts and the Nand, and present `pin=signal` as a connection to a part's pin. The brief of Hello says the same.

**Alternatives:**
- A bubble in Hello that only describes connections: rejected. The tour teaches by doing, and Hello can't be solved with a connection alone.
- Teaching `pin=signal` first and connections later: rejected, because a connection is the simpler idea and part pins build on it.

**Consequences:** a new game opens Wire. Both tutorial levels stay optional, since Not depends on neither. `place_bubble` now lets a bubble beside its anchor slide up or down to stay in the window, because Wire's taller "connect" bubble otherwise dropped below the `PARTS:` line and covered the editor.

## 2026-11-06 — UI polish: track order, net highlight, junctions, wrapped help
**Context:** milestone 3 asks for fewer wire crossings on large chips, the hovered net highlighted across the canvas, junction dots where wires branch, and a help line that fits narrow windows.

**Decision:**
- **Crossings:** measured first. On a 64-part chip the column order accounted for about 500 crossings, but the drawn total was 2537: most came from the order of vertical tracks inside each channel, which was sorted by y. Tracks are now ordered by pairwise crossing cost (a trunk's stubs that run across another trunk's span), ranked by pairwise wins and then improved by neighbour swaps. Result: 944 on that chip, and 2 instead of 10 over all shipped levels. A transpose pass on the column order was also tried; it changed the drawn total by under 1%, so it was left out.
- **Net:** what lights up is every wire from the same source pin, including slices of the same bus. Hovering a wire, an input pin, or an output fed by one source selects it. A part selects nothing, because it has several outputs.
- **Junction:** a route corner where wires of one source leave in three or more directions. Junctions are computed once with the layout, not per frame.
- **Help line:** it wraps between `·` items. Only an item wider than the window on its own wraps between words. The footer grows to fit, and every panel sizes against the real footer height.

**Alternatives:**
- Truncating the help with "…": rejected, because the hidden shortcuts were the reason for the item.
- A global crossing minimisation (an ILP, or many random restarts): rejected for now, since the heuristic is linear in practice and the remaining crossings are mostly forced by the placement.
- Highlighting only the exact nets (bits) of the hovered wire: rejected, because a slice would then light up only part of its bus trunk, which reads as a broken wire.

**Consequences:** `layout.py` exposes `source_key`, `junctions`, `hovered_net` and `Layout.junctions`. `ViewerApp.footer_height` replaces the `FOOTER` constant wherever a panel is sized.

## 2026-11-06 — Main menu, Esc pause menu and game reset
**Context:** the user asked for an escape screen, a main menu and a way to reset the game.

**Decision:**
- **Title screen** at start (`nandsim gui` only). It offers Play, or Continue once there is progress, then Reset game… (only when there is something to reset) and Quit. `GameApp(title_screen=False)` stays the default, so tests and hooks open straight into a level.
- **Esc pauses from anywhere in the game, the editor included.** The editor has focus nearly all the time, so Esc that first left the editor would need two presses to reach the menu. Leaving the editor is a click on the circuit. Resume gives focus back to where it was. Esc on the pause menu resumes. On the title screen it does nothing. The developer viewer keeps Esc for leaving the editor.
- **The pause menu** offers Resume, Replay the tour, Main menu, Reset game… and Quit.
- **A reset is a move, not a delete.** Every file in the save directory goes to `<save dir>-backups/<YYYY-MM-DD_HHMMSS>/`, so a mistaken reset can be undone by moving the files back. Backups live beside the save directory, not inside it, because `ChipLibrary` searches its directories recursively and would keep using the backed-up chips. A regression test pins this.
- **Confirmation** first, with Cancel as the default selection, so Enter on a menu opened by mistake does nothing. The dialog says where the files go. After a reset, the game opens the first level with the tour started over, and the sidebar names the backup folder.
- **Unsaved editor text:** quitting (from the menu or by closing the window) saves it to the level, as switching level already did. A reset drops it, because saving it would put a chip back into the directory that was just emptied.

**Alternatives:**
- Deleting the save files on reset: rejected. Losing a player's work for good is the kind of thing that is hard to undo.
- Teaching `ChipLibrary` to skip a `backups/` folder: rejected. The core shouldn't know about the GUI's save layout.
- Esc leaves the editor first, then opens the menu: rejected, as explained above.

**Consequences:** `ViewerApp` gained `quit_requested` and a `before_quit()` hook, and `SaveStore` gained `has_progress()`, `reset()` and `backups`. Old backups are never cleaned up automatically.

## 2026-11-06 — Teaching internal wires in the And level
**Context:** the user asked the And tutorial to teach how to connect a gate's output to another gate's input. And is the first level that needs two parts in a row, and until now neither the tour nor the brief explained internal wires.

**Decision:**
- **Two tour steps before `open_part`, both tied to And.** `wires` points at the `PARTS:` line, explains that a name of your own on a part's output is a wire that another part can read, and waits for `build_ok`, so the player builds their own And. `see_wire` then points at that wire on the circuit and invites the player to hover it (the net lights up) and to toggle `a` and `b`.
- **The example isn't the answer.** The bubble and the brief show `Not(in=a, out=na); Not(in=na, out=out);`, a double Not, so the And puzzle and its hint ("what undoes a not?") stay the player's to solve. Hello's tour gives its answer because Hello is the syntax lesson; And is a real gate.
- **A new `wire` anchor:** the first part-to-part wire on the canvas, framed together with the two parts it joins, so the bubble sits beside them rather than over them. Like `pin:` and `part`, it falls back to the whole canvas when there is no such wire.
- **Code lines in a bubble:** consecutive indented lines now form one code block, drawn without blank rows between them. A blank line still separates two blocks.

**Alternatives:**
- Showing the And solution in the bubble: rejected, because it would solve the level for the player.
- A separate tutorial level just for wires: rejected. And already needs exactly this, so it teaches by doing.

**Consequences:** the tour has 19 steps. `wire` joins the anchor list in `chips/tutorial.toml` and `tutorial.ANCHORS`.

## 2026-11-06 — The player's goal: a CPU, then a whole computer
**Context:** the user set the game's overall aim. The milestones so far end with a single-cycle CPU (milestone 7) running a hand-assembled program, but nothing said where the game itself goes after that.

**Decision:** the player's aim is to build first a working CPU, and then a whole computer around it. What "a whole computer" includes (memory map, I/O, display, keyboard, storage, and so on) will be defined later, as its own milestones.

**Alternatives:**
- Stop the game at the CPU and leave the rest to the later projects (emulator, OS…): not chosen. The user wants the game to carry on to a complete machine.

**Consequences:** level and milestone design should keep the CPU reusable as a part of a larger machine (clean interfaces to instruction ROM, data RAM and future I/O), so the computer levels can be added without reworking it. The scope of the computer stage is still open and needs its own decision before work starts.

## 2026-11-06 — The Intel 4004 replaces RV32I; new milestone 4, chip files and sound
**Context:** the user asked for three changes to the milestones: saving and loading single chips, audio, and making the last goal a chip with the same requirements as an Intel 4004. Asked to choose, they picked the 4004 as *the* game CPU (replacing RV32I, not added after it) and export/import of chip files (not several save slots per level).

**Decision:**
- **CPU:** the Intel 4004, compatible at the instruction level: 4-bit accumulator and carry, 16 four-bit index registers (8 pairs), a 12-bit PC with a 3-level stack, all 46 instructions with their real encodings, and the 4001 ROM and 4002 RAM organization and I/O ports. Not modelled: the multiplexed 4-bit bus and the 8-phase clock. Our single clock fits the simulator's tick/tock semantics, and an instruction-level match is what a `.tst` can check.
- **Timing:** one clock cycle per 4004 instruction cycle, so the two-word instructions (`JCN FIM JUN JMS ISZ`) and `FIN` take two cycles, as on the real chip. Test programs can then count cycles the way 4004 documentation does.
- **The end of the game** is the 4004 (milestone 8). *(Superseded by 2026-11-08, the Busicom 141-PF as milestone 9.)* This replaces the "CPU, then a whole computer" aim of the entry above: the program ROM, data RAM and I/O ports of the CPU milestone already form a small MCS-4 computer. A stage after it would need a new decision.
- **New milestone 4, "Chip files and sound",** before Buses, because it polishes what exists and is small. Renumbered: Buses 5, Arithmetic 6, Sequential logic 7, CPU 8. Releases stay one per milestone, up to `0.8.0`.
- **Widths:** Buses, Arithmetic and Sequential logic are rescoped from 32 bits to the 4004's 4-bit data, 8-bit instructions and register pairs, and 12-bit addresses. The barrel shifter and RV32I comparisons are dropped; decimal adjust, rotate through carry and the 3-level stack are added.
- **Chip files:** an exports folder beside the save dir, never inside it (`ChipLibrary` searches the save dir recursively, as found with backups), browsed from an in-game menu instead of a file dialog. An imported chip is unsaved editor text until Ctrl+S or Run tests, so importing alone never solves a level.
- **Sound:** synthesized with numpy at startup and played with `pygame.mixer`, which is part of pygame-ce, so there is no new dependency and no asset licence. Mute and volume live in a settings file next to the saves; no audio device means silence, never a crash.

**Alternatives:**
- Keep RV32I and add the 4004 as a final open-ended challenge: recommended in the analysis, not chosen.
- The 4004 as a step between sequential logic and RV32I: not chosen, the user wants the 4004 to be the goal.
- Several named save slots per level instead of export/import: not chosen.
- A tkinter file dialog or a typed path for chip files: rejected, tkinter and pygame mix badly on Linux, and typing paths is fiddly.
- Cycle-accurate 4004 (multiplexed bus, clock phases): rejected, it would bend the single-clock simulation semantics for no gain in what the player learns about the ISA.

**Consequences:**
- The later projects in the series (emulator, assembler, ROM monitor, compiler, OS, networking) now target the 4004 and lose the RISC-V toolchain and QEMU as references; Intel's MCS-4 manuals, existing 4004 programs and open 4004 emulators replace them. A compiler and an OS for a 4-bit CPU with a 3-level stack and 4 KB of ROM are a stretch, and their scope should be revisited when those projects start. Project 8 (real machines, on QEMU) is unaffected.
- `.tst` needs a way to load program ROM contents before milestone 8.
- Future milestone numbers changed in the `tick`/`tock` error message, `docs/tst.md`, the primitives docstring and `CHANGELOG.md`. Earlier decision and journal entries keep their wording.


## 2026-11-06 — Chip files: exporting and importing from the pause menu
**Context:** milestone 4 asks for exporting the current level's chip to a `.hdl` file and importing one into a level's editor, from an in-game menu, in an exports folder beside the save dir. The entry above fixed the folder's place and that an import is unsaved text; the details were open.

**Decision:**
- **Folder:** `<save dir>-exports/` (default `~/.local/share/nandsim/save-exports/`), the same naming as `-backups`. A reset doesn't touch it, and `ChipLibrary` never searches it.
- **Where in the game:** two items in the Esc pause menu, *Export this chip* and *Import a chip…*. None on the title screen, which has no current level.
- **Export writes the editor's text**, saved or not, because that is what the player is looking at and expects to get. It does not save the level or mark the buffer saved. The file is `<Level>.hdl`. If that file exists with different contents, a *Replace?* dialog asks first, with Cancel selected; identical contents are rewritten silently.
- **Import lists every `.hdl` file** in the folder (not subfolders, not other extensions), with the current level's file first and marked *(this level)*, the rest by name, case-insensitively. Files for other chips are listed too, so a renamed or shared file can still be loaded; a wrong `CHIP` name is then an ordinary build error, which already has a tip.
- **Six files per page**, with Next and Previous page items, because `Menu` doesn't scroll and the window has no minimum size. Back from any page returns to the pause menu.
- **An import replaces the editor's text as one undoable edit** (select all, then insert), leaving it unsaved. It counts only after Ctrl+S or Run tests, as the milestone requires, and Ctrl+Z restores the previous text. The cursor goes to the top.
- **Errors are notices, never crashes:** an unreadable or non-UTF-8 file, or a failed write, shows a line in the sidebar and leaves the editor as it was.

**Alternatives:**
- Exporting the saved file instead of the editor's text: rejected, it would surprise a player who just typed something and exports it.
- A text field for a file name on export: rejected for now, it needs a text-input widget in menus; renaming in the file manager covers it.
- Listing only files named after the current level: rejected, it hides renamed or shared chips.
- A scrolling menu: more work than paging for the same result.

**Consequences:** `SaveStore` gained `exports`, `export_path`, `export`, `chip_files` and `read_chip_file`; `GameApp` gained `export_chip` and `import_chip`. Exported files are never cleaned up.

## 2026-11-06 — Exported chips are named parts of the library; no import
**Context:** after the first version of chip files (entry above), the user asked that exporting not replace the editor's text on import, and that the player type the chip's name instead. Asked to clarify, they said: on export the player types the file's name, and there is no import, because exported files are always in the library.

**Decision:**
- **Export asks for a name** in a one-line text field (*Export this chip as…* in the Esc menu). The field suggests `My<Level>`, or the name this level was last exported under. The editor's text, saved or not, is written to `<save dir>-exports/<Name>.hdl` with the name after `CHIP` replaced by the typed one; nothing else in the text changes, so build error positions still match the editor. The editor itself is untouched.
- **A name must be able to stand for a chip of its own:** an ASCII identifier, not an HDL word (`CHIP IN OUT PARTS true false`), not a primitive (`Nand`, and `DFF` ahead of milestone 7), not any level's chip. The dialog shows why a name is refused, under the field.
- **The chip must build** (parse and elaborate, with the player's saves and other exports) before it is written, so an export can never break a level that uses it. A circular use, a chip that contains its own exported name, is a build error like any other.
- **Replacing** an exported chip of the same name with different contents asks first, with Cancel selected.
- **Exported chips are in the library and allowed in every level**, besides the level's parts, both in the game and in `nandsim test --impl save`: the runner searches the exports folder after the saves and lists exported chips in the *not allowed* message. A file whose name couldn't be a chip of its own (the rules above) is never treated as an exported chip.
- **No import.** A shared `.hdl` file is used by copying it into the exports folder. The sidebar lists the player's chips under *Your chips*.

**Alternatives:**
- Exported chips allowed only in levels already solved: not chosen; the user wants them always in the library.
- Keeping import beside named export: not chosen, the user dropped it.
- Exporting without a build check: rejected, a broken export would surface as a confusing error in another level.

**Consequences:**
- A player can export a level's answer under another name and use it in that same level. Since they wrote the answer themselves, this is accepted. A file copied in from someone else can solve a level, which is what sharing chips means.
- `ChipDef` gained `name_pos`. `testing` gained `exported_chips`, and `run_script` an `exported` argument. `SaveStore` replaced `chip_files`, `read_chip_file` and `export(level, …)` with `exported`, `name_problem`, `prepare_export` and `export(name, …)`. `Menu` gained a text field. The import menu and its paging are gone.
- The level briefs' *Parts you may use* line doesn't list exported chips; the sidebar does.

## 2026-11-06 — Deleting exported chips, and resetting them with the game
**Context:** the user asked that exported chips can be deleted from a button in the sidebar list, and that a game reset deletes them too. Until now a reset left the exports folder alone (entry above).

**Decision:**
- **One row per exported chip** under *Your chips*, with a **×** button on the right that turns red on hover.
- **A confirmation first**, with Cancel selected. It names the player's chips, saved levels and other exports, that use the chip directly as a part, because those stop building. Solved levels stay solved (solved is sticky), so a delete never locks a level.
- **"Deleted" means moved, never destroyed**, as for a reset: the file goes to `<save dir>-backups/<time>/exports/`, which the library never searches. Undoing it is moving the file back.
- **A reset moves every file in the exports folder** (not only chips) to `backups/<time>/exports/`, beside the save files it already moved, and the reset dialog says exported chips start over too. Exported chips alone count as progress, so the title screen offers *Reset game…* when they are all there is.
- **After a delete the circuit on screen is rebuilt**, because it may have used the chip: it then shows the build error instead of a circuit that can no longer be built.

**Alternatives:**
- Deleting the files for good: rejected, for the same reason as for reset.
- Refusing to delete a chip that others use: rejected, it would force the player to edit those first; the warning is enough.
- Keeping exports on reset: the user asked otherwise.

**Consequences:** `SaveStore` gained `delete_export` and `users_of`; `reset` and `has_progress` include the exports folder; the backup-folder naming moved into `_new_backup`, shared by both.

## 2026-11-06 — Sound effects, mute and volume
**Context:** milestone 4 asks for sound effects synthesized with numpy at startup, with no asset files, played through `pygame.mixer`: toggles, build errors, tests passed and failed, level solved, menus. Mute and volume go in the menu and in a settings file next to the saves, and without an audio device the game runs silently.

**Decision:**
- **Three modules.** `gui/synth.py` (numpy only) holds the recipes and `to_mixer`, `gui/settings.py` (pure) holds mute and volume, and `gui/sound.py` is the only one that touches `pygame.mixer`. Synthesis is tested without a device.
- **Eight sounds**, each 0.8 s at most and faded out at the end:

  | sound | when |
  |---|---|
  | `toggle` | an input is clicked on the canvas |
  | `error` | Ctrl+S with a build error, or a refused export name |
  | `pass` | tests pass on a level already solved |
  | `fail` | tests fail or don't build |
  | `solved` | a level is solved for the first time (`TestReport.newly_solved`) |
  | `move` | the menu selection changes |
  | `select` | a menu item is chosen, the pause menu opens, a delete dialog opens |
  | `back` | Esc or Cancel in a menu |

  Typing in a menu's text field is silent.
- **The mixer's real format.** If the mixer isn't open yet, `Sounds.load()` asks for 44.1 kHz, 16-bit, stereo. Then it builds every sound in whatever format the mixer actually reports, since a device may force another one. `to_mixer` handles signed and unsigned integers, float32, mono and stereo.
- **Silence, never a crash.** A `pygame.error` while opening the mixer or building sounds disables them; `play` then does nothing and never raises.
- **Settings** go in `<save dir>-settings.json`, beside the save directory like `-exports` and `-backups`, so a reset keeps them. An unreadable file means the defaults (on, 60%) and a sidebar warning; it's overwritten at the next change, since settings are cheap to lose.
- **Menu items.** *Sound: On/Off* and *Volume: N%* sit above Quit on both the pause menu and the title screen. Volume steps through 20–100% by 20 and wraps around. Volume is applied when a sound plays, so changing it doesn't re-synthesize anything. Both items relabel in place and play a preview, and they are saved at once.
- **The developer viewer** (`nandsim gui FILE`) is silent: it is a tool, not the game.

**Alternatives:**
- Sound files: ruled out by the milestone, and they would bring asset licences.
- A volume slider widget: more UI for little gain over five steps.
- Settings inside the save directory: rejected, a reset would undo the player's mute.

**Consequences:** `GameApp` has `settings` and `sounds`; `sounds.played` logs recent sounds for tests. `SaveStore.settings_path` and `paths.settings_file` name the file.

## 2026-11-06 — Level groups fold in the sidebar
**Context:** milestone 5 adds 13 bus levels. The sidebar draws the whole level list, then the brief, with no scrolling: 21 levels and 3 group headers take about 666 of the 860 default pixels, which pushes the brief off-screen. Later milestones add more.

**Decision:**
- **Each group header is a button** (`▾`/`▸`, the group name, solved/total, green with a ✓ when all are solved). Clicking it opens or closes the group; a closed group is only its header.
- **Default open groups:** the current level's group, and the next group after it that has an open (unlocked, unsolved) level. At most two groups, and what to do next is always in sight: Not from the tutorial, the first bus level once Gates is under way. Earlier groups with unsolved levels, such as a skipped tutorial, stay closed with their count showing.
- **The player's choice lasts until the defaults change**, which is when the current level moves to another group or a level gets solved. It isn't saved: the game starts with the defaults.
- **Tour bubbles** that point at a level in a closed group point at the group's header instead; the `levels` anchor covers headers and rows.
- `GameState.groups()`, `default_expanded()` and `group_label()` hold the rules, without pygame.

**Alternatives:**
- Scrolling the list in a fixed height: the brief still loses space, and a wheel over the sidebar is easy to miss.
- An accordion with only the current group open: hides Not from a player in the tutorial, which the tour and the "Not is open from the start" rule rely on.
- Opening every group with an open level: with part-based unlocking, several groups open at once later in the game, and the list overflows again.
- Smaller rows: only delays the problem.

**Consequences:** two open groups of many levels can still fill the sidebar (Buses alone has 13); if a later milestone makes that happen, the list may need a maximum height too. Tests that click levels must open a closed group first, as `test_tour_playtest.click_level` does.

## 2026-11-06 — Typing a value for an input pin
**Context:** clicking a bus input counts up (right-click down) by one. Milestone 5 brings 12-bit buses, where reaching a value can take up to 4095 clicks.

**Decision:**
- **Opening:** with the circuit focused (not the editor) and the mouse over an input of the top chip, **Enter** opens an empty field, and so does typing a digit or `-`, which also becomes the field's first character (it arrives as the TEXTINPUT that follows the KEYDOWN). It works on 1-bit pins too.
- **Syntax and errors** are those of `.tst` values (`13`, `-1`, `0b1101`, `0x0D`), through `testing.parse_pin_value`, so the messages match: `16 does not fit in 4-bit pin 'a'`. `*` is not a value here. Characters that can't be in a value are dropped as they are typed.
- **Enter** sets the pin and closes the field; on an error the field stays open and shows the message until the player types again. Enter on an empty field just closes it. **Esc** cancels, before the game's pause menu; **a click anywhere** cancels and still does what it would. Ctrl+Backspace clears.
- **While the field is open, every key goes to it**, so `x`, `b` and `h` are typed rather than firing X (undefined) or H (hex/dec).
- **A typed value counts as a toggle**: same sound, and tour steps waiting for a toggle accept it.
- The field sits just under its pin, at a fixed size whatever the zoom, kept inside the canvas. It closes if its pin disappears (a rebuild, or navigating into a part).
- The state is the pygame-free `gui/valuefield.ValueField`; `ViewerApp` draws and routes it, so the developer viewer has it too.

**Alternatives:**
- Clicking single bits of a bus: needs per-bit drawing on the pin, and is still slow for 12 bits.
- The pause menu's text-field dialog: hides the circuit while typing, and the developer viewer has no menus.
- Mouse wheel with a step: still slow, and the wheel already zooms.
- Prefilling the field with the current value: a value is usually replaced, not edited; an empty field is simpler.

**Consequences:** `testing` exports `parse_pin_value`. The help line and README list the new control.

## 2026-11-06 — The tour teaches typed values and exported chips
**Context:** the tour was written before players could export chips, type input values or fold level groups, so it said nothing about them. The user asked for the tutorial to cover them. There is no chip import: exported chips are in every level's library, and a shared chip is used by copying its `.hdl` file into the exports folder.

**Decision:**
- **Hello, `type_value`** (after `output`): click an empty spot of the circuit so the keys go to it, point at `b`, type `1`, press Enter. It waits for a new event, `set_value`, reported when a typed value is applied. A `set_value` also completes a step waiting for `toggle` (a typed value changes the pin as a click does); a click doesn't complete a `set_value` step.
- **And, `export`** (after `back_up`): export the chip from the Esc menu, keeping the suggested `MyAnd` or another name. It waits for a new event, `export`, reported when an export is written. Then **`your_chips`**, anchored on the *Your chips* list (new anchor `chips`), explains using the chip as a part, the × button, and sharing by copying files into the exports folder. Both are tied to And, so they never jump ahead of Not's steps for a new player.
- **Folding groups** gets a sentence in `welcome` rather than a step of its own: it needs no practice.
- **The bubble avoids the value field** while one is open, as well as its anchor, so the player sees what they type.
- **Ctrl+Enter, Ctrl+S and other modified keys never open the value field.** After `type_value` the circuit has the keys, and the player's habit of Ctrl+Enter to run tests opened the field instead.

**Alternatives:**
- Teaching typed values in the first bus level (Not4), where they matter: that level doesn't exist yet, and Hello's one-bit pins are enough to learn the gesture. A short reminder can go in the bus briefs.
- Ending the export step with Next instead of an actual export: the tour teaches by doing everywhere else, and the × removes the chip afterwards.
- A level-less export step that would also reach players who are past And: for a new player it would show in Not, before the And steps it builds on.

**Consequences:** players who finished the tour see the new bubbles when they next open Hello or And (the tour shows unseen steps of the open level). `Tour` events gained `set_value` and `export`, anchors gained `chips`; `ViewerApp.on_action` reports `set_value` instead of `toggle` for typed values, and the game still plays the toggle sound for it. `ViewerApp.field_rect` is where the field was last drawn.

## 2026-11-06 — The bus levels: pins, parts and tests
**Context:** milestone 5 lists 13 bus levels at the 4004's widths but not their pins, allowed parts or test strategy. Pin names are hard to change once players have saves, because the runner rejects a chip whose pins differ from the stub.

**Decision:**
- **Pins follow nand2tetris:** `in`→`out` for Not4 and Or4Way, `a, b`→`out` for the bitwise gates, `a, b, …, sel`→`out` for the muxes, and `in, sel`→`a, b, …` for the demuxes. `sel` is a bus whose value names the input: `sel = 0` is `a`, `sel = 3` is `d`, with `sel[0]` the least significant bit. Or4Way's `in` is 4 bits.
- **Order** is the milestone's: Not4, And4, Or4, Xor4, Mux4, Mux8, Mux12, Or4Way, Mux4Way4, Mux8Way4, Mux4Way12, DMux4Way, DMux8Way, in group `02_buses` ("Buses").
- **Parts are minimal:** `Nand` plus the chips a level naturally widens or combines (Not4: Not; Mux12: Mux, Mux4, Mux8; DMux8Way: DMux, DMux4Way). With part-based unlocking, Not4 opens as soon as Not is solved, so bus levels open alongside the gates instead of after all of them.
- **Tests:** every input combination up to 8 input bits (Not4, And4, Or4, Xor4, Or4Way, both DMuxes). Wider muxes check every `sel` with each input holding its own value, then, for each `sel` and bit, the chosen input with only that bit set (the others 0) and with only that bit clear (the others all ones), then 16 random rows with seed 4004. Values are binary up to 4 bits and hex above. Wrong solutions tried while writing them (swapped `sel` bits, crossed bits, a stuck top bit, outputs in the wrong order, an input left out of Or4Way) all fail.
- **Not4's brief teaches buses:** bus notation, bit 0 as the least significant, hex display and typing a value. Mux8's hint introduces slices.
- **Briefs stay short enough** to show in full under the sidebar's open Buses group at the default window size; Not4's, the longest, is 23 lines at the sidebar's width.

**Alternatives:**
- Cumulative parts lists, as in the gates: every bus level would wait for all six gates, and the lists would grow long.
- Exhaustive tests for Mux4 (9 bits, 512 rows): the structured rows find the same mistakes with far fewer lines.
- A tour step in Not4: the brief carries the bus notation, and the tour already ends in And.

**Consequences:** solving Not now also unlocks Not4 (the tests that check the unlock line say so). The `.tst` files were generated by a script kept out of the repo; the seed is in each file's first comment.

## 2026-11-06 — Tips for bus errors
**Context:** the bus levels bring new build errors. Their messages say precisely what is wrong; milestone 3's tips add what to do, but none covered buses.

**Decision:**
- **Five new tips**, matched before the general ones: a width mismatch on a part's pin, a width mismatch in a direct connection, a slice out of range, and some bits of an output bus, or of a part's input bus, left unconnected. They name the pin and widths from the message and show the slice notation (`in[0]`, `in[0..3]`).
- **No tip** where the message already says what to write: a reversed slice (`write [0..3]`), a new wire sliced where it is created (`write 'out=w'`), and a new wire from a constant.
- Each tip is tested against the real error from a bus level (Not4, or Mux8 for a part's bus input).

**Alternatives:** rewording the errors themselves to include the advice: the messages are shared with the CLI and stay short and exact, as `docs/hdl.md` lists them.

**Consequences:** the width-mismatch patterns depend on the message giving a unit only after the first width (`has 1 bit but 'in' has 4`); a change there needs the pattern updated, which the tests catch.

## 2026-11-06 — The level list scrolls; the brief keeps its room
**Context:** with Buses open under Gates (which happens as soon as Not is solved), the level list is 22 rows and pushed most of And's brief off the sidebar at the default window size. The folding entry above had flagged this. The user asked to cap the list's height and scroll past it.

**Decision:**
- **The cap follows the brief:** the list gets the sidebar's height minus what the separator, the notice, *Your chips* and the whole brief need, rounded down to whole rows, and never fewer than 5 rows. A short brief leaves more room for levels; only a window too short for both cuts the brief (`GameApp.brief_cut`).
- **Scrolling** is by whole rows with the mouse wheel over the list; elsewhere the wheel still zooms the canvas. A thin bar at the sidebar's right edge shows the position when the list scrolls.
- **The list scrolls to show a row** when the row it should show changes: the current level, or the level a tour bubble points at (its group header if the group is folded). Between those changes the player's scrolling stays.
- **Rows scrolled out are not drawn and not clickable**, and tour anchors only see visible rows.

**Alternatives:**
- A fixed share of the sidebar (tried first at a half): And's brief still lost its hint, and short briefs would waste room.
- Scrolling the brief instead of the list: the brief is what the player reads while building; the list is glanced at.
- Never opening a second group by default: hides the next level to play, which the folding rule exists to show.

**Consequences:** `GameApp` has `list_scroll`, `list_rect`, `scroll_list()` and `brief_cut`; `clamp_scroll` and `scroll_into_view` are module functions. The brief is laid out twice per frame (measured, then drawn), which is cheap at its size.

## 2026-11-07 — The adder levels: pins, parts and tests
**Context:** milestone 6 opens with five adders (HalfAdder, FullAdder, Add4, Inc4, Inc12) but doesn't give their pins, allowed parts or tests. As with the bus levels, pin names are hard to change once players have saves. The 4004's ALU comes afterwards: its interface is still undecided and is left to its own entry.

**Decision:**
- **Pins:** HalfAdder `a, b`→`sum, carry` and FullAdder `a, b, c`→`sum, carry`, as in nand2tetris. Add4 `a[4], b[4], cin`→`out[4], cout`, so the 4004's `ADD` maps straight onto it: accumulator, register and carry flag in, accumulator and carry flag out. Inc4 `in[4]`→`out[4]` and Inc12 `in[12]`→`out[12]`, with no carry out: `INC` and `ISZ` leave the carry flag alone, and the program counter just wraps.
- **Parts are minimal**, as for the buses: HalfAdder may use Xor and And; FullAdder HalfAdder and Or; Add4 FullAdder; Inc4 HalfAdder, with the constant `true` as the added 1; Inc12 Add4, chained through the carries. Inc4 has no carry out, so it can't be chained into Inc12; Add4 can. Inc12 opens with Add4, before Inc4 is solved.
- **Group** `03_arith`, shown as "Arithmetic" by a small label table in `group_label`, since the folder name would read "Arith". The folder keeps the name `CLAUDE.md` gives it.
- **Tests:** exhaustive for HalfAdder, FullAdder, Inc4 and Add4 (Add4 is 9 input bits, 512 rows; it's the chip `ADD` relies on, so every case is checked). Inc12 checks edges (0, nibble and byte boundaries, `0xFFF` wrapping to 0), a single 0 at each bit that stops the carry, a carry running up to each bit, then 16 random rows with seed 4004. Nine plausible wrong solutions (carry from Or, carry from And in FullAdder, an ignored carry in, cout taken from bit 2, crossed bits, 1 added to every bit, unchained or always-set carries in Inc12) each fail.

**Alternatives:**
- Inc4 with a carry out, so Inc12 could chain three of them: it would give Inc4 a pin that the 4004's `INC` doesn't use. Add4 already chains.
- Renaming the folder to `03_arithmetic`: it would differ from the layout in `CLAUDE.md` for a display string.

**Consequences:** the `.tst` files were generated by a script kept out of the repo, as for the buses. A new game now shows four groups, with Arithmetic folded until Xor is solved.

## 2026-11-07 — Four smaller levels before the 4004 ALU
**Context:** the milestone lists the 4004's ALU as one level, with 16 operations. Going straight from Add4 to all of them is a big jump, and a failing `.tst` row would say "op 11" without saying what DAA is. The analysis proposed four smaller levels, one per operation that isn't a plain adder, and the user agreed. The ALU's own pins and `op` codes get their own entry when that level is built.

**Decision:**
- **AddSub4** `a[4], b[4], cin, sub`→`out[4], cout`. With `sub = 1` it is the 4004's `SUB`: `a + ~b + ~cin`, so `cin = 1` is a borrow in and `cout = 1` means no borrow. This is the opposite of most CPUs, and pyntel4004's `sub.html` confirms it. Parts: Add4, Xor4, Xor.
- **Rotate4** `in[4], cin, right`→`out[4], cout`. It covers `RAL` (`right = 0`) and `RAR`, both through the carry. Parts: Mux, Mux4. It is all wiring and slices.
- **Daa4** `in[4], cin`→`out[4], cout`. It adds 6 when `in > 9` **or** `cin = 1`. `cout` is set when adding 6 carries out, and otherwise keeps `cin`: the carry is never cleared, as pyntel's `daa.html` says. Parts: Add4, And, Or.
- **Kbp4** `in[4]`→`out[4]`, with 0, 1, 2, 4, 8 mapped to 0, 1, 2, 3, 4 and anything else to 15, as in pyntel's `kbp.html` table. Parts: Not, And, Or.
- **Order** after Inc12: AddSub4, Rotate4, Daa4, Kbp4, all in `03_arith`. Names take the 4004 mnemonic where there is one, with the width as for the bus chips.
- **Tests:** every input combination for each (AddSub4 1,024 rows, Rotate4 64, Daa4 32, Kbp4 16). They are generated from a Python model of the instructions written apart from the references, and the model is checked against every example row in the briefs. The tests catch these wrong solutions: SUB without the complemented carry, with the borrow read the usual way, or without the +1; a shift instead of a rotate, the rotate directions swapped, or `cout` from the wrong end; DAA that ignores `cin`, clears the carry, or adjusts at 9; KBP that misses two keys in different pairs, or maps 4 to 4.
- **Brief tables must fit the sidebar.** Two first drafts had tables too wide for the sidebar, and the renderer silently cuts the last columns. Kbp4 now keeps explanations out of its cells, and Rotate4 shows RAL and RAR as two tables. A test checks every level's table rows against `GameApp.brief_cols`, the sidebar's width in characters.

**Alternatives:**
- One ALU level only, as listed in the milestone: rejected for the size of the jump.
- An IncDec4 level for `IAC` and `DAC`: both are AddSub4 with constant inputs (`b = 0, cin = 1` and `sub = 1, b = 1, cin = 0`), which the ALU level can teach.
- Wrapping wide table rows in the renderer: a wrapped row breaks the table's alignment. Keeping tables narrow is a rule for briefs, and the test enforces it.

**Consequences:**
- The ALU level can use these four chips as parts, so it's mostly about choosing results by `op`.
- The Intel manual's URL was unreachable, so these semantics rest on the pyntel4004 docs, which quote it. They should be checked against the manual if it turns up.

## 2026-11-07 — The 4004 ALU: pins and op codes
**Context:** the ALU is the last Arithmetic level, and its interface is the hardest one to change later. The milestone 8 CPU decoder, the instruction-level emulator in project 2, and players' saves will all depend on it. The analysis proposed the interface below and the user went ahead with it.

**Decision:**
- **Pins:** `IN a[4], b[4], cin, op[4]; OUT out[4], cout, zr;`. `a` is the accumulator, `b` a register or RAM, and `cin` the carry flag. `out` and `cout` are the new accumulator and carry, and `zr` is `out == 0`.
- **op codes:** 0–12 are the low digit of the accumulator group `F0`–`FC`: CLB, CLC, IAC, CMC, CMA, RAL, RAR, TCC, DAC, TCS, STC, DAA, KBP. The CPU can pass that digit straight in. 13 is LD (`out = b`, carry kept), in the slot of DCL, which changes neither A nor CY. 14 is ADD and 15 SUB, in the two codes after `FD` that the 4004 doesn't use. ADM and SBM are ADD and SUB with `b` from RAM.
- **Semantics** are those of the four part levels before it, plus: IAC `a+1` with carry out; DAC `a+15`, whose carry is 1 unless `a` was 0 (no borrow); CMC `~cin`; CMA `~a`, carry kept; TCC `out = cin`, carry 0; TCS `9 + cin`, carry 0; KBP keeps the carry.
- **LD in the ALU** puts every accumulator write through `out`. LD, LDM, XCH, RDM, RDR and RD0–RD3 put their value on `b` and use op 13. Instructions that don't write A (DCL, WRM, …) just don't load the accumulator.
- **`zr` is a convenience, not the 4004's zero test.** The 4004 has no zero flag: JCN tests the accumulator as it is. The CPU should test its accumulator register (Or4Way and Not), not this pin, because the ALU's output at JCN time comes from whatever `op` is applied then. The pin is there so the milestone's "zero and carry flags" can be tested at the ALU.
- **Parts:** Nand, Not, Not4, Or4Way, Mux4, Mux8Way4, Add4 and the four part levels. Mux is left out on purpose: the hint points at carrying a carry in bit 0 of a 4-bit bus, so two Mux8Way4s choose it.
- **Tests (5,856 checks):** every `a` and `cin` for each op, with `b` random (seed 4004), and every `a`, `b` and `cin` for LD, ADD and SUB, with `out`, `cout` and `zr` checked on each row. They are generated from a model that reuses the part levels' model, with spot checks from the 4004 docs (DAC 0 → 15 with carry 0, TCS, SUB, IAC overflow). These wrong ALUs each fail: RAL and RAR swapped, ADD as SUB, DAC's carry as a borrow, TCS backwards, `zr` from `a` or inverted, KBP, CLC or DAA clearing or keeping the carry wrongly, CMC keeping it, LD passing `a`, TCC giving 1, IAC without a carry, STC as CLC, and `op[3]` ignored.

**Alternatives:**
- nand2tetris-style control bits instead of `op`: DAA, KBP and TCS don't fit them, and the CPU decoder would have to map every instruction.
- op 13 as DCL passing `a` through: no use to the ALU, and LD and the reads would need their own mux into the accumulator.
- No `zr` pin: closer to the real chip, but the milestone asks for the flags at the ALU.

**Consequences:**
- The reference is 1,319 NANDs at depth 42, four times the largest chip so far. Nearly 450 of them are the two Mux8Way4s that choose the 1-bit carry. It simulates at about 6.5k evaluations/s (8.5 M gate-evaluations/s, the same rate per gate as the bus chips). A builtin ALU, with its equivalence test, is the option if the CPU in milestone 8 needs the speed.
- Its circuit is dense but readable at the top level: 14 parts, inputs on the left, `out`, `cout` and `zr` on the right.

## 2026-11-07 — DFF and the clock: tick latches, tock commits
**Context:** milestone 7 needs state. CLAUDE.md fixes `out(t) = in(t-1)` with a tick and a tock per cycle, as in nand2tetris, and the three-valued engine entry says DFFs start undefined. Still open: what each half does exactly, what a lone `tock` does, how a `.tst` failure says when it happened, and whether tables tick.

**Decision:**
- **`tick`** evaluates the chip, then every DFF latches its input. **`tock`** puts every latched value on its DFF's output, evaluates again, and counts one cycle. Both are a single vectorized copy over all DFFs. Inputs changed between a tick and its tock don't reach that cycle.
- **A `tock` with no `tick` before it** commits whatever is latched: undefined at power-on, so it changes nothing. It isn't an error, and it still counts a cycle.
- **`Simulator.reset()`** returns to power-on: every input, wire and latch undefined, cycle 0. It lands now, for the GUI's reset button.
- **In a `.tst`,** `tick` and `tock` are plain commands with no arguments. A failing check in a script that uses either one ends with `cycle N`, or `cycle N after tick` between the halves, after the table inputs if any. Combinational scripts print as before.
- **Table rows don't tick.** They stay set, eval, expect. Sequential tests write their cycles out until a shorthand earns its place.
- **`DFF` is allowed only where a level lists it,** like any other part.

**Alternatives:**
- A `cycle` command for tick plus tock: left out to keep the format small; it can be added without changing anything else.
- Times printed nand2tetris style (`3+`): shorter but cryptic to a new player.
- A lone `tock` as an error: it is harmless, and an error would only get in the way of a GUI that lets the player press either half.

**Consequences:** the GUI's clock controls (next) need only `tick`, `tock`, `reset`, `cycle` and `mid_cycle`. `levels.RESERVED` now derives from the primitive table.

## 2026-11-07 — Exported chips may use a primitive only once a level lists it
**Context:** reviewing #38 showed that once `DFF` resolves as a primitive, the export dialog let a player on Not export a one-DFF chip. Exported chips are allowed in every level, and the level check only looks at a chip's direct parts, so the DFF would reach levels that don't list it.

**Decision:** an export may use a primitive only if some unlocked level lists it among its parts. The check runs on the flattened netlist, so a DFF inside a saved or exported part counts too. The message is `It uses DFF, which no level you have unlocked allows yet.` `Nand` is unaffected, since the first levels list it and they are always open. `RESERVED` is gone: the primitive table is the one list of names a player's chip can't take.

**Alternatives:**
- Check DFF use transitively in the test runner for every level: sequential levels (Register4 uses Bit, which holds a DFF) would need a rule for which hidden DFFs are fine, which the export check avoids.
- Refuse DFF in exports for good: it would stop players from exporting their own registers in milestone 7.

**Consequences:** export is the only way a chip gets into the exports folder (there is no import), so checking there is enough. A file put there by hand isn't checked; players never edit files. `SaveStore.unlocked_primitives()` is available for the GUI if it ever wants to show which primitives are open.

## 2026-11-07 — Clock controls in the circuit view
**Context:** milestone 7 asks for clock controls in the GUI, and CLAUDE.md lists step (one tick/tock), run with adjustable speed, pause and reset. Open: where they live, which keys, what reset and a rebuild do to state, and whether the view can stop between a tick and its tock.

**Decision:**
- **A clock panel** at the top right of the canvas: the cycle count, Reset, Run (Pause while running), Step, and the speed between − and +. It and its help items appear only for chips with DFFs, so the combinational levels are unchanged. Fit leaves room for it, and clicks and drags on it never reach the circuit.
- **Keys** on the circuit (not in the editor), without Ctrl, Alt or Cmd: Space steps one cycle and repeats while held, R runs or pauses and Shift+R resets, once per press, and the typed characters `[` and `]` change the speed. They go by character, not key, because on Italian, German or French layouts brackets need AltGr. Stepping by hand pauses a running clock.
- **Speeds** 1, 2, 5, 10, 20, 50, 100, 200, 500 and 1000 cycles/s, 5 by default. Each frame runs the cycles the elapsed time is worth, but spends at most 30 ms doing so and counts a stall as 0.25 s at most. A chip too slow for its speed falls behind, and the window stays responsive. Any open menu in the game, the pause menu first, holds the clock, and the time spent there isn't owed afterwards.
- **Reset** puts every DFF back to undefined and the cycle to 0, and pauses. The input values stay: the player set them on purpose.
- **A rebuild keeps the DFFs' values and the cycle count only if every DFF sits where it did**: the list of DFF part paths (`Reg2/Bit#1/DFF#5`, recorded by elaboration) is exactly the same. A comment, a renamed wire or new wiring keeps everything, and a running clock keeps running. Adding or removing a part renumbers the parts after it, so the old paths would name other DFFs: then every DFF starts undefined, the count restarts and the clock pauses, as after a reset. A value is never shown on the wrong DFF. (The first version matched DFFs one path at a time, which the review of #40 showed put a register's high bit into its low bit.)
- **Whole cycles only.** The view never rests between a tick and its tock, so what the DFFs latched never needs showing. That settles the review note on #38 about exposing latched values.

**Alternatives:**
- Tick and tock as separate controls, as in nand2tetris: shows the two-phase clock but doubles the presses for no gain in what the levels ask; it can be added later with the latched values drawn on DFFs.
- Controls in the header: too little room beside long breadcrumbs.
- Matching DFFs across rebuilds one path at a time, or by wire names: a renumbered part can't be told from a moved one, so values land on the wrong DFFs. Labelled parts (`g1: Bit(...)`) could give stable names later, if losing state on structural edits turns out to annoy players.
- Reset clearing the inputs too: makes the player re-enter values they meant to keep.

**Consequences:** `ChipSession` owns the clock (`step`, `advance`, `reset_clock`, `toggle_run`, `change_speed`) and is tested without a window. The engine gained `dff_paths`, `dff_outputs`, `dff_state` and `load_dff_state`, and the netlist `gate_paths`. `tick` skips its evaluation when nothing changed since the last one, so a step costs one evaluation, not two. Opening a level builds a new session, so its clock starts at cycle 0. The register levels' briefs and the tour will introduce the controls.


## 2026-11-07 — The brief and *Your chips* scroll too
**Context:** the level list scrolls since 2026-11-06, but a window too short for the list's 5 rows plus the brief cut the brief with no way to read its end, and every exported chip added a row to *Your chips*, pushing the brief further down.
**Decision:**
- ***Your chips* shows at most 4 rows** (`CHIPS_MAX_ROWS`) and scrolls by whole rows past that. Its header stays put. A chip just exported scrolls into view. In a short window it takes fewer rows, down to one, so the brief keeps 3 lines (`BRIEF_KEEP_LINES`), and it never runs past the footer.
- **The brief scrolls** in whatever height is left under the chips, by 3 text lines per wheel notch. It goes back to its top when another level opens. The list's height rule doesn't change: it still leaves the whole brief its room when the window allows, so the brief only scrolls in short windows.
- **The wheel scrolls what is under the mouse**: the level list, the chips or the brief. Over the rest of the sidebar (headings, the notice, gaps) it does nothing; over the canvas it still zooms. All three views show the same thin bar at the sidebar's right edge, and rows scrolled out are neither drawn nor clickable.
**Alternatives:**
- One scroll view for everything under the level list: a long chip list would push the brief out of sight again.
- Shrinking the level list below 5 rows to fit the brief: the list is how the player moves around, and it already scrolls.
**Consequences:** `GameApp` gained `brief_scroll`/`brief_view` and `chips_scroll`/`chips_view`, next to `list_scroll`/`list_rect`. `brief_cut` now means "the brief scrolls". The `brief` tour anchor is the visible part of the brief.

## 2026-11-07 — The register levels
**Context:** milestone 7 lists Bit, Register4, Register8 and Register12 after the DFF and the clock controls. Still open: the group, the pins, what each level may use, how a `.tst` tells a real register from a wrong one, and how the game introduces the clock.
**Decision:**
- **A new group `04_seq`, shown as "Memory"**, after Arithmetic. It will also hold the register file, the PC and the RAM levels.
- **Pins as in nand2tetris:** `IN in[N], load; OUT out[N]`, with `load` 1 storing `in` at the next clock cycle.
- **Parts:** Bit may use Nand, Mux and DFF (it is the only level that lists DFF so far). Register4 uses Bit, Register8 uses Register4, and Register12 may use Register4 and Register8. Each level builds on the one before, as the bus levels do.
- **Tests are scripts that check twice per cycle:** after the `tick` (the output must still be the old value) and after the `tock` (the new one). The after-tick check fails a Bit whose output is taken in front of the DFF, which would otherwise pass every after-tock check. Bit covers every (stored, in, load) transition. Register4 loads all 16 values and holds each against a random `in`. Register8 and Register12 test each bit on its own, the edges, and 24 random cycles. Randomness uses seed 4004. The vectors were generated once and committed, as for the earlier levels.
- **The tour introduces the clock on Bit** with two steps after the And steps: one on the brief until the chip builds, and one on a new `clock` anchor (the clock panel, only while the chip has a DFF) until a new `clock_step` event (one Step). The tour's "done" bubble now says that more bubbles wait in Memory.
**Alternatives:**
- A level for the bare DFF before Bit: a chip that is just one DFF teaches nothing the Bit brief doesn't.
- Letting every register use Bit directly: Register12 from 12 Bits is a chore, not a puzzle.
- Tour steps that explain Run and Reset one at a time: the panel is small, and one bubble covers it.
**Consequences:** `tutorial.ANCHORS` gains `clock` and `EVENTS` gains `clock_step`. A player who finished the tour before this change still sees the two Bit bubbles when they reach Bit. Exports may now use DFF once Bit is open.

## 2026-11-07 — The index register file: one address, two widths
**Context:** milestone 7 asks for the 4004's index registers: 16 × 4 bits, also read and written as 8 pairs. The CPU uses them in several ways. `ADD`, `SUB`, `LD`, `XCH`, `INC` and `ISZ` read one register, and `XCH`, `INC` and `ISZ` also write it back in the same instruction. `FIM` and `FIN` write a pair, and `SRC`, `JIN` and `FIN` read one. Open: the pins, how a pair is addressed, which half of a pair is high, and what happens when both kinds of write are asked for.
**Decision:**
- **`CHIP IndexRegs { IN in[8], addr[4], load, loadpair; OUT out[4], pairout[8]; }`.** One address port. `out` is always register `addr`, and `pairout` is always the pair that holds it, so the CPU never has to switch the chip between modes to read.
- **`addr` is the instruction's low digit as encoded.** A pair is `addr[1..3]`, and `addr[0]` is ignored for pairs, as in the 4004's `RRR0`/`RRR1` encodings (`FIM`/`SRC`, `FIN`/`JIN`).
- **The even register is the pair's high half**, as in the 4004: `FIM P0` puts the first data digit in R0, and `SRC` sends R0 out first.
- **`load` writes `in[0..3]` into register `addr`. `loadpair` writes `in[4..7]` into the even register and `in[0..3]` into the odd one.** If both are set, `loadpair` wins. That falls out of the obvious design, and the test pins it down.
- **One address is enough for the CPU.** `FIN` reads P0 and writes another pair, but in different cycles of a two-cycle instruction, so the CPU chooses `addr` per cycle.
- **Parts:** Nand, Or, DMux, DMux8Way, Mux4, Mux8Way4, Register4.
- **Test:** each register and each pair written and read back, a cycle with neither load, load against loadpair, then 64 random cycles with seed 4004, checked against a Python model. Every clock cycle checks both reads after its tick (still the old value) and after its tock (496 checks). A check before the tick would repeat the after-tick one, since a tick evaluates before it latches. When a single register is written, the ignored high digit of `in` differs from both registers of its pair, so writing that digit anywhere shows. Registers not written yet are `*`. Wrong versions fail it: pair halves swapped, a pair loading only when P0 loads, the pair picked from `addr[0..2]`, and an odd-register load that also writes the even one.
**Alternatives:**
- A `pair` mode bit that switches `out` between 4 and 8 bits: more muxing, and a mode to keep in step.
- Separate read and write addresses: no 4004 instruction needs them in the same cycle.
- Making both loads at once undefined: tests can't check "undefined" usefully, and the CPU never does it.
**Consequences:** the CPU level will drive `addr` from the instruction's low digit (from R0's pair for `FIN`'s fetch), `load` for `XCH`/`INC`/`ISZ`, and `loadpair` for `FIM`/`FIN`. A builtin for this chip can come later if the CPU needs the speed, with an equivalence test.

## 2026-11-07 — The PC and its stack: four addresses and a wrapping pointer
**Context:** milestone 7 asks for the PC with its 3-level address stack. The 4004 keeps four 12-bit address registers and a 2-bit pointer. The one selected is the program counter, `JMS` moves the pointer up and `BBL` moves it down, and the pointer wraps. A stack built as a shift register (PC, S1, S2, S3) behaves the same for programs that nest at most three calls, but not after a fourth call or a return past the bottom. Also open: the controls, what wins when several are set, how the return address skips the call, and how the counter starts.
**Decision:**
- **Four addresses and a wrapping pointer, as on the chip,** so even an overflowing program behaves as on a real 4004. The emulator in the next project will follow the same model.
- **`CHIP PC { IN in[12], inc, load, push, pop, reset; OUT out[12]; }`.** Priority is `reset` > `push` > `pop` > `load` > `inc`, and the test pins it down.
- **`push` with `inc` also steps the address it leaves behind.** On `JMS`'s second cycle the CPU both fetches (which steps the PC) and calls, so the saved address must point past the call. A push without `inc` saves the address unchanged.
- **`pop` writes nothing.** The address under the new pointer is already the return address, stepped when the call was made.
- **`reset`** sets the pointer and all four addresses to 0 in one cycle. The 4004 clears the program counter at once, but needs reset held for 8 instruction cycles to clear the whole stack. This project models instruction cycles, not the chip's clock phases, so one cycle gives the end state a program can rely on, and a return past a reset reads 0 as on the real chip. Everything starts undefined, so the CPU needs one reset cycle.
- **Parts:** Nand, Not, And, Or, Xor, Mux, Mux12, DMux4Way, Mux4Way12, Inc12, Register12, Bit. The pointer is two Bits.
- **Test:** reset, counting across `0xFFF`, a jump, calls three deep with and without `inc`, a fourth call, two returns past the bottom, returns past a reset finding 0, then each of the 10 pairs of controls, then 200 random cycles (seed 4004), all from a Python model, 654 checks. Each pair case starts from a known stack and ends with two pops, because some outcomes only show in the stack (push and load both put `in` on `out`). The generator asserts that the reversed priority would give a different result, so the priority order no longer depends on the random section. Every clock cycle checks `out` after its tick and after its tock. Wrong versions fail: a push that doesn't step the address it leaves, a reset that doesn't clear the address or the stack, a push that writes at the old pointer, and each of load over pop, inc over load and pop over push.
**Alternatives:**
- A shift-register stack: just as easy to build, but it differs from the 4004 after an overflow.
- Making the CPU save the return address itself: two writes in one cycle would move into the CPU, which is already the largest chip.
- Showing the stack on extra outputs: the CPU doesn't need it, and the circuit view already shows every register's value.
**Consequences:** the CPU will raise `inc` on every fetch cycle, `push` with `inc` on `JMS`'s second cycle, `pop` on `BBL`, `load` on jumps that are taken, and `reset` from its own reset pin.

## 2026-11-07 — The RAM levels, up to one bank of 4002s
**Context:** milestone 7 asks for RAM at increasing sizes up to the 4002 layout: registers of 16 main and 4 status characters, picked by bank, chip and register. Open: the sizes on the way, the pins, how status characters are addressed, how many banks, whether the 4002's output port belongs here, and whether every size can run as HDL.
**Decision:**
- **The ladder is RAM8 → RAM64 → RAM4002 → RAMBank**, each built from the one before (RAM8 from Register4), with 4-bit characters throughout. The status characters are what the levels add after RAM64.
- **Addresses as `SRC` sends them:** RAMBank's `addr[8]` is chip `addr[6..7]`, register `addr[4..5]` and main character `addr[0..3]`. RAM4002 takes the low 6 bits. The CPU can wire its `SRC` register straight in.
- **One `status` pin chooses status characters,** picked by `addr[0..1]` within the register, with `addr[2..3]` ignored. For `WRn`/`RDn` the CPU puts `n` on `addr[0..1]`. The alternative, a separate 2-bit pin for the status index, would add a pin to every level for a two-bit Mux in the CPU.
- **Banks: 8, picked by a 3-bit number** (the low 3 bits of `DCL`), as in MCS-4 systems with a bank decoder and in most emulators. A system without the decoder drives the CM-RAM lines directly, and some `DCL` values select two banks at once. That is wiring, not memory, and few programs rely on it.
- **The 4002's 4-bit output port is not in these levels.** It is written by `WMP`, not by memory writes, and the CPU milestone turns ports into chip pins, so it is decided there.
- **The eight-bank memory (DataRAM) waits for a builtin.** In HDL it comes to 187k gates. It simulates at about 490 cycles/s, but elaborating it takes 7.4 s, on every save and every Run tests. RAMBank is 23k gates, takes 0.8 s and runs about 2,100 cycles/s. CLAUDE.md allows a builtin once the HDL version passes, so a builtin RAMBank, with its equivalence test, comes first. DataRAM then is eight of those. Its HDL reference passes too; it is kept out of the repo until then. *(Superseded by 2026-11-08, DataRAM in HDL with a sampled test: since the compile cache it builds in 0.09 s and ships in HDL.)*
- **Tests** come from `tools/gen_ram_tst.py`, a Python model with seed 4004, and `tests/test_tools.py` fails if a committed `.tst` no longer matches it. Each test fills every cell, writes every cell again with a different value, reads everything back, then runs random cycles. RAM4002 and RAMBank cover all their main and status characters, the status ones named with random `addr[2..3]`. Each write checks `out` after its tick and after its tock. The fill's after-tick checks can only be `*`, because the cell is still undefined. The rewrite's are real, so a RAM whose `out` shows `in` before the clock edge fails at its first rewrite. Once everything is filled, every random read is a real check too. Wrong versions fail: a RAM8 that loads every register, a RAM8 of Bits that let `in` through early, status characters picked by `addr[2..3]` or by the wrong register bit, status writes leaking into main memory, a RAMBank picking chips by `addr[4..5]`, and each of the 20 RAMBanks with one of address bits 0–4 stuck at 0 inside one chip. Four of those 20 passed the first version of the test, which only wrote characters 0 and 15 outside chip 0.
**Alternatives:**
- A flat `RAM512`/`RAM4K` ladder as in nand2tetris: the 4002 layout would then be index arithmetic in the CPU.
- Generated tests without their generator, as for the earlier levels: the first version of these did that, and fixing its gap meant regenerating thousands of lines. The earlier levels' generators can move to `tools/` when they next change.
- Four banks (the CM-RAM lines without a decoder): the multi-bank `DCL` codes would need modelling for little gain.
**Consequences:** pytest takes about 9 s, up from 5 s, because every level's reference and stub run. The next step is builtins: RAMBank first, marked in the GUI, switchable back to HDL, with a test that the builtin and HDL versions agree, then the DataRAM level. *(Superseded: DataRAM came first, see 2026-11-08.)*

## 2026-11-07 — Compile each chip once, and keep wire paths lazy
**Context:** elaboration re-walked a chip's HDL, re-checked its wiring and rebuilt its wire paths for every instance. A RAMBank (4,000 copies of a few small chips) took 0.8 s on every save and Run tests, and an eight-bank DataRAM 7.3 s, which kept that level waiting for a builtin. Profiling showed the time spread over the per-instance checks and the 1.3M wire paths of a DataRAM. Once those were gone, levelization (a Python loop per gate) was 85% of what remained.
**Decision:**
- **Each distinct chip compiles once into a template:** its flattened gates and wires in a numbering of its own (constants, then input bits, then internal nets), already checked, with placeholder aliases resolved. A part is instantiated by giving its internal nets a fresh block in the parent and remapping the template's arrays with numpy.
- **Templates are cached per `ChipLibrary`, keyed by the parsed `ChipDef` object.** The library already hands out one `ChipDef` per name, so a template is valid exactly as long as the parse cache. Every compile in the GUI and the CLI makes a fresh library, so an edit is never served stale. A cache keyed on source text across libraries would also skip unchanged chips between saves, but it needs to track what each chip resolved to. It is not needed at these times.
- **`Netlist.wires` and `Netlist.gate_paths` become read-only `Mapping`s computed on demand** by walking the template tree. The GUI and the engine look up a few paths at a time; nothing needs all of them except a combinational-loop message, which walks the tree once.
- **Levelization processes one frontier per round with numpy.** It gives the same levels, and the same gate order within each level, as the old loop. This was checked on every reference chip and on DataRAM.
- **Results:** RAMBank 0.81 s → 0.016 s, DataRAM (187k gates) 7.34 s → 0.087 s. Simulation speed is unchanged.
**Alternatives:**
- Memoizing only the parse, or only the error checks: the per-instance wire paths alone took about a second for DataRAM.
- Keeping `wires` an eager dict: 1.3M lists for DataRAM, built on every save.
- A builtin RAMBank first, as planned: still useful for simulation speed (DataRAM runs about 490 cycles/s in HDL), but the build time no longer blocks the level.
**Consequences:** net numbers are now compact (placeholders no longer take a slot), so `num_nets` is smaller than before. Code that needs every wire should use `wires.walk()` rather than one lookup per path. The DataRAM level can now be added in HDL. Whether it still waits for a builtin depends only on simulation speed.

## 2026-11-08 — DataRAM in HDL, with a sampled test
**Context:** the RAM entry above held the eight-bank memory back for a builtin, because it took 7.4 s to build. Since the compile cache it builds in 0.09 s, and the entry after it says only simulation speed is left to decide. Open: the pins, and how to test 2,560 cells in a test the player waits for.
**Decision:**
- **Ship DataRAM now, in HDL.** It runs about 490 cycles/s, enough for its own test. A builtin is still the plan for the CPU's speed, and doesn't change these pins.
- **`CHIP DataRAM { IN in[4], addr[8], bank[3], status, load; OUT out[4]; }`.** RAMBank's pins plus `bank`, the low 3 bits of `DCL`, as decided above. Parts: Nand, DMux8Way, Mux8Way4, RAMBank.
- **The test samples each bank instead of filling it.** RAMBank's test already checks everything inside a bank, so DataRAM's checks how the banks are wired. In each bank it writes main characters 0, each power of two and 255, so every address bit of a main character matters, and status characters at 0, 64, 128 and 255, one per chip. Which status character inside a chip is picked is left to RAMBank's test: DataRAM gives every bank the same `addr` and `status`, so it can't wire them differently in one bank. Those addresses are also main characters the test writes, so a bank whose `status` is stuck at 0 overwrites a value that the read-back checks. The first version picked random status addresses, and that wrong version passed it. A cell's value differs from every other cell in its bank and from the same cell in every other bank, so a crossed or stuck address bit, or a wrong bank, always reads a wrong value. The rewrite adds the same shift to every cell, which keeps those values apart, and the shift is 8 or more, so it never equals the difference between two bank numbers. With a smaller one (7, as the review of #47 found), a DataRAM that shows bank 0 for bank 7 passed the rewrite's after-tick checks and was only caught by the read-back. Then 200 random cycles, all on those cells, so the only `*` checks are the fill's after-tick ones. That is 960 checks, about 1 s.
- **Wrong versions fail:** bank select bits swapped on `out`, `load` ignoring `bank[2]`, bank 0 loading every time, banks 1 and 2 crossed on `out`, a bank with address bit 0, 3, 6 or 7 stuck at 0, a bank with `status` stuck at 0 (banks 0, 5, 7), and bank 0 showing bank 7's data.
**Alternatives:**
- Filling all 2,560 cells: about 5,000 cycles, over 10 s for each Run tests.
- Waiting for the builtin: it would hold the level back for speed it doesn't need yet.
**Consequences:** the CPU level can use DataRAM directly, with `bank` from its `DCL` register. A builtin RAMBank/DataRAM comes next with the CPU's speed in mind.

## 2026-11-08 — Feedback loops and the clock signal: the player builds the DFF
**Context:** the user decided that the player should not get `DFF` as a primitive, and should build latches and flip-flops from NAND instead. The user approved changing the two `CLAUDE.md` rules this breaks: "the only primitives are `Nand` and `DFF`" and "a combinational loop that does not pass through a DFF is an error". The work comes in three PRs: the engine (this entry), the SRLatch, DLatch and DFF levels, and a fast DFF builtin that replaces the player's DFF once it passes. Until then the `DFF` primitive stays as it is.
**Decision:**
- **Loops are levelized as components.** When Kahn's algorithm leaves gates over, Tarjan's algorithm finds their strongly connected components. It is a Python loop, but it runs only on the leftover gates. The graph of components is levelized the same vectorized way. Each level becomes a plain level, evaluated once, then a loop level that holds that level's loops. A chip without loops levels exactly as before: same levels, same order, same speed (DataRAM's test takes 1.25 s before and after).
- **A loop level runs in unit-delay rounds.** Every gate of the level reads the values of the previous round, and the rounds stop when one changes nothing. Every loop of the level is evaluated together, vectorized, so a RAM's many latches settle in one level. Unit delay makes a master–slave flip-flop work as in hardware. The latch that closes on a clock edge locks one gate delay later, while new data needs at least two delays to reach it from the other latch. Everything a loop reads from outside it is already settled, because it comes from earlier levels.
- **A loop that doesn't settle goes undefined.** After `min(2 × gates in the level + 4, 1000)` rounds, the nets of the loops that changed in the last round become undefined. The rounds then continue from there. Kleene NAND is monotone, so from undefined each round can only learn values, never flip them, and the rounds always end. Other loops of the level keep their values. This covers oscillators (`Nand(a=en, b=x, out=x)` with `en = 1`) and races, such as releasing both inputs of an SR latch at once, where real gates would be metastable.
- **Failing checks name the unsettled wires.** `Simulator.unsettled` holds the nets the last evaluation left undefined that way. A `.tst` failure that reads undefined then ends with `a loop didn't settle: x, y`, naming up to three wires and how many more. Names come from the shallowest wire path, computed only on such a failure. The level report adds a tip for it. The old build-error tip for loops is gone with the error.
- **`clock` is net 2,** after `false` and `true`, in every chip's template. It is read like a constant (`Const` now holds a name, `true`, `false` or `clock`) and can't be driven or give a new wire its width. It is a reserved name: `IN clock;` fails with `expected a pin name, found 'clock', a name kept for the clock signal`. It is 0 at power-on and after a reset. `tick` evaluates, latches the DFF primitives, raises the clock and evaluates again. `tock` updates the DFF outputs, lowers the clock and evaluates. A flip-flop whose master latch is open while `clock` is 1 and whose slave latch is open while it is 0 therefore matches the primitive's `out(t) = in(t-1)`, with the old value after a tick and the new one after the tock. A test checks the two against each other on random inputs.
- **The clock panel appears for chips that read `clock`,** not only for chips with DFFs (`Simulator.clocked`). The canvas colours a `clock` label by its value, like `true` and `false`.
**Alternatives:**
- A clock pin threaded through every sequential chip (`IN clk`): it would change every register, RAM and CPU interface, and players' saves.
- Zero-delay (Gauss–Seidel) settling in level order: the result would depend on gate order, and a flip-flop could let data race through both latches in one evaluation.
- Unit delay over the whole netlist: correct, but every evaluation would take as many rounds as the deepest path.
- Keeping the loop build error for loops that can never settle: telling them apart takes solving the circuit. Undefined, with the wires named, is honest and cheap.
- Carrying latch state across a rebuild in the GUI: the DFF rule needs stable DFF paths. Loop nets have no such identity yet, so a rebuild starts latches undefined. That can wait for the builtin, which brings DFF paths back.
**Consequences:** a loop costs about seven times the primitive. 256 Bits built from latches run at 4,250 cycles/s with 3,329 gates, against 29,000 cycles/s and 1,281 gates with the DFF primitive. So the CPU will need the DFF builtin from the third PR, and the player's latch DFF stays for the levels that teach it. `Netlist.levels` is now a list of `Level` (ops plus a loop count). `levelize` no longer needs source positions. Net numbers inside chips moved up by one.
## 2026-11-08 — The Busicom 141-PF as milestone 9, and a ROM in the 4001 layout
**Context:** milestone 7 lists a 4096 × 8 program ROM, and its contents need a way in. The only primitives are `Nand` and `DFF`, so a player's ROM is memory built from DFFs, and the game can't tell which DFF holds which bit. Asked how programs get in, the user chose an in-game editor where the player types binary code, loaded through a write port, and said the ROM should follow the computer that comes after the 4004 as a new milestone: the Busicom 141-PF calculator.
**Decision:**
- **Milestone 9, the Busicom 141-PF, is the new end of the game,** replacing the 4004 (2026-11-06 entry). The 141-PF is a 4004, four 4001 ROMs (1 KB, a fifth for the square-root option), two 4002 RAMs and a 4003 shift register for the printer, running an interpreter whose registers live in RAM. Sources disagree on the number of 4003s, so its scope (keyboard, printer, program, 4003s) gets its own decision before work starts. Releases go up to `0.9.0`.
- **The ROM follows the 4001, as the RAM follows the 4002:** `ROM4001` (`IN in[8], addr[8], load; OUT out[8];`, 256 × 8) and `ROM4K` (`IN in[8], addr[12], load; OUT out[8];`, sixteen ROM4001s picked by `addr[8..11]`, the 4004's whole address space). The 141-PF fills four or five of the sixteen.
- **A write port, though the 4001 is mask-programmed.** Writing through the chip's own pins is the only way to load a ROM the player built, whatever its insides. The CPU keeps `load` at 0. MCS-4 systems did run from program RAM (4008/4009 with `WPM`), so it isn't foreign to the platform.
- **The 4001's I/O port** waits for the CPU milestone, like the 4002's output port.
- **A ROM editor:** the player types bytes in binary, with `//` comments, saved as a `.rom` file with the saves. On reset the game writes them in through `in`, `addr` and `load`, one per cycle, before handing over the clock. A `.tst` command loads a `.rom` file the same way. The file format and the command get their own entry when built.
**Alternatives:**
- A read-only ROM whose contents come from a file: it must be a Python builtin, so the player builds nothing, against "HDL version first".
- A 1 KB ROM sized for the 141-PF: the 4004 addresses 4 KB, and the milestone asks for 4096 × 8.
- Keeping the 4004 as the end: the user asked for the calculator.
**Consequences:** a ROM4K in HDL holds about three times DataRAM's bits and will run at about 150 cycles/s, so loading the 141-PF's 1 KB takes about 7 s. Builtin memories, with their equivalence tests, are needed by milestone 9 at the latest. The CPU milestone's pins should leave room for the 4003 and for the 141-PF's keyboard and printer.

## 2026-11-08 — The program ROM comes after the CPU
**Context:** the entry above put the ROM levels and the ROM editor in milestone 7. The user asked for them after the CPU instead. The CPU milestone's tests still have to give the CPU a program.
**Decision:**
- **The ROM levels (`ROM4001`, `ROM4K`) and the ROM editor move to the start of milestone 9,** with the Busicom 141-PF, which is the machine that uses the 4001s. Their pins and loading model stay as the entry above decided. Milestone 7 now closes without a ROM.
- **In milestone 8, the test runner holds the program.** A `.tst` command attaches a program memory to the CPU's ROM pins: each cycle the runner reads the CPU's address output and drives its instruction input. This is test-harness code, not a chip, so it bends neither "only Nand and DFF" nor "HDL version first". The command's syntax and the `.rom` file format get their own entry when built, and the ROM editor in milestone 9 reuses that format.
**Alternatives:**
- Straight-line programs set by hand in each `.tst`: no jumps or calls, so most of the 46 instructions couldn't be tested in a program.
- Moving the ROM levels to the end of milestone 8, after the CPU: the CPU doesn't need them, and the 141-PF is what fills them.
**Consequences:** the CPU level's pins are a ROM address out and an instruction in, which the runner's memory and, later, the player's ROM4K both plug into. The ROM's own I/O port still waits for the CPU milestone.

## 2026-11-08 — SRLatch, DLatch and DFF: the player builds the flip-flop, the primitive stands in for it
**Context:** this is the second step after feedback loops and the clock signal. The player should build the DFF from NAND. Bit, the registers, the RAMs and the CPU all use DFF parts, and latch flip-flops run about seven times slower than the primitive.
**Decision:**
- **Three levels open the Memory group, before Bit.** SRLatch (`IN set, reset; OUT out`; Nand, Not) has active-high inputs, two Nots in front of cross-coupled NANDs. DLatch (`IN in, load; OUT out`; Nand, Not, And, SRLatch) follows `in` while `load` is 1, with the same pin names as Bit. DFF (`IN in; OUT out`; Nand, Not, DLatch) reads `clock`.
- **No Mux for DLatch.** A latch made of a Mux feeding itself glitches when `sel` changes. In the unit-delay engine, as on real gates, it can catch its own glitch.
- **Tests are sequences, not truth tables of independent rows.** Each row of SRLatch's and DLatch's tables follows the one before, so a row with neither command checks the value the row before left. SRLatch never raises both inputs at once: that state isn't part of the chip's contract, and releasing both together is a race. DFF's script checks after every tick (the old value: this fails a latch open while `clock` is 1) and after every tock (the new value). Some cycles also change `in` while the clock is low and run `eval` (`out` must not follow: this fails a latch open while `clock` is 0). Others change `in` between the tick and the tock (the value at the tick wins, as for the primitive). Eight wrong versions fail, among them each single latch, swapped clock phases and latches that are always open.
- **A part named `DFF` stays the primitive.** `ChipLibrary.resolve` still returns the primitive for every part. The new `resolve_top` returns the player's HDL for the chip being tested, built or shown, so the DFF level tests the player's own latches. `STAND_INS = {"DFF"}` marks it. A level that lists DFF needs the DFF level solved, exactly as for any chip: `FREE_PRIMITIVES` (only `Nand`) is what `missing`, `is_unlocked` and the level-order test treat as always available. This is CLAUDE.md's builtin rule: the HDL version comes first and must pass.
- **Equivalence test:** the reference DFF and the primitive run side by side on 4 × 400 random sets, ticks, tocks and evals, and agree at every step. The exception, by design, is an `eval` between a tick and its tock with a new `in`. The latch master is still open then and takes it, while the primitive stored its input at the tick. No `.tst` does that, and the GUI only runs whole cycles.
- **SRLatch unlocks as soon as Not is solved,** since it needs only Nand and Not, just as the bus levels open early. The Memory group stays after Arithmetic in the list.
- **The tour:** the "memory" bubble moves to SRLatch, a new "flipflop" bubble on DFF asks for a build, and the "clock" bubble moves to DFF, the first chip with a clock.
**Alternatives:**
- No stand-in, every DFF built from the player's latches: RAM and CPU levels about seven times slower (DataRAM's test would take seconds), for no gain in what they teach.
- Naming the player's chip something else (`FlipFlop`) and keeping `DFF` a free primitive: Bit would still hand the player a flip-flop they never had to build.
- Marking the stand-in in the GUI and switching back to HDL now: that is the next PR, with the general builtin mechanism.
**Consequences:** a player who solved Bit before this change keeps it solved. Its DFF parts still build, and Register4 and later levels stay open. Bit itself now waits for DFF on a new save. Exports may contain a DFF once the DFF level is solved (Bit lists DFF, and Bit is unlocked only then).

## 2026-11-08 — The built-in DFF: marked on the canvas, switchable to the player's own
**Context:** CLAUDE.md asks that a builtin be marked visibly in the GUI and that the player can always switch back to the HDL version. Since the previous entry, every DFF part runs as the engine's primitive in place of the player's latch DFF. Open: how to mark it, how to switch, and how far the switch reaches.
**Decision:**
- **The mark is in the title:** a built-in part is titled `DFF (built-in)`. The layout already sizes boxes by their title, so nothing else changes. It still doesn't open, as before.
- **One switch for the whole circuit,** `B` on the canvas, without modifiers. It is shown in the help line, and works only when a DFF part sits anywhere under the chip and the player's DFF HDL exists (`ChipSession.can_switch`). The parts are found by walking the chip definitions, not the netlist. A save that solved Bit before the DFF level, or the developer viewer on a folder without `DFF.hdl`, has nothing to switch to, so B isn't offered there. The review of #52 found that it first claimed "your DFF" while the primitive still ran. B sets `ChipLibrary.builtins = False` on the next library, whose `resolve` then returns the player's DFF HDL for a `DFF` part, and the session rebuilds. `has_hdl` is remembered per library, so drawing many DFF parts doesn't search the disk again.
- **A chip that doesn't build is refused up front:** B leaves the error showing and asks the player to fix it first. Otherwise a failure from the chip's own error would be blamed on the DFF, as the review of #52 found.
- **The player's DFF is whatever they last saved** on the DFF level, even an edit that no longer passes its tests. It is labelled "yours", which is true. The built-in DFF is the one Run tests trusts.
- **While the player's DFF runs, every save starts the clock over.** The clock is carried across a reload by DFF paths, and latches have none. The feedback-loop entry left this for later. It costs a few clicks only in the mode for looking inside, so it stays.
- **Per-part switching:** rejected. A DFF from latches inside one Bit and a primitive in the next would make a chip whose timing and gate count depend on clicks nobody sees.
- **A DFF that no longer builds keeps the built-in one.** If the player edited their saved DFF after solving it, the switch rebuilds, fails, and restores the flag. A failed reload leaves the running circuit untouched, so nothing is rebuilt a second time. The reason goes in the notice: the game shows it in its sidebar, the developer viewer under its header. The circuit never shows the error, because it isn't about the chip being edited.
- **The header note never covers the breadcrumbs.** In a narrow window the notes are dropped, last first, until the rest fits.
- **The clock starts over on a switch.** The DFF paths change (the primitive is gone, or back), and the reload rule already resets the clock when they do.
- **Not saved:** the choice lasts for the session, and the game keeps it from level to level. It always starts built-in, the fast default. Run tests and the CLI always use the built-in DFF. The equivalence test from the previous entry is what makes that safe.
- **The header says `DFFs: yours (B: built-in)`** while the player's DFF runs, so a slow circuit explains itself.
**Alternatives:**
- A setting in the Esc menu, saved with the sound settings: one more menu item for something done to look inside, not a preference.
- A badge or a different fill colour for built-in parts: primitives already have their own fill, and a word says more than a colour.
**Consequences:** with this, the three steps toward a player-built DFF are done. Other builtins (RAM, ALU) can reuse `STAND_INS`, `builtins` and the label once their HDL versions pass.

## 2026-11-09 — Data RAM comes after the CPU, as the program ROM does
**Context:** milestone 7 shipped the RAM levels (RAM8 up to DataRAM) in the Memory group, and milestone 8 would have put a DataRAM inside the CPU. The user asked for the RAM levels after the CPU, because data memory is part of the computer around it, like the program ROM (2026-11-08, "The program ROM comes after the CPU").
**Decision:**
- **The CPU level has data-RAM pins instead of a RAM inside it.** They mirror DataRAM's pins, so a DataRAM plugs straight in later: the CPU drives `addr[8]` (its `SRC` register, which the CPU holds), `bank[3]` (from `DCL`), `status`, `load` and the 4-bit character to write, and reads the 4-bit character back. The exact pin names, and the 4002's output port for `WMP`, are settled with the CPU level.
- **In milestone 8, the test runner holds the data memory**, as it holds the program: a `.tst` command attaches a runner-held data memory to the CPU's RAM pins, and `.tst` checks can read its cells. Its model is the one in `tools/gen_ram_tst.py`. Like the program memory, it is test-harness code, not a chip. Its syntax gets its own entry when built.
- **The RAM levels move to a new group, `06_computer`, shown as "Computer".** The CPU will be `05_cpu`, between Memory and Computer. Milestone 9 starts with the RAM levels, then the ROM levels and the ROM editor, then the 141-PF. The levels, pins and tests are unchanged, and saves are named by level, so no player loses a solution.
- **The gate comes with the CPU level.** Unlocking goes by parts: RAM8 opens once Register4 is solved, wherever it sits in the list. To open the Computer group only after the CPU, the CPU branch adds `requires = ["CPU"]` to RAM8 in `levels.toml`, read by `is_unlocked` and checked by the level-order test. Adding it now would name a level that doesn't exist yet and lock RAM8 for every player until then. Until the CPU lands, the RAM levels are only listed last.
**Alternatives:**
- RAM at the end of milestone 8, with a closing CPU + DataRAM level: it splits the computer between two milestones.
- Only reordering the list, with no gate: RAM8 would still open right after Register4.
**Consequences:** CPU tests don't simulate a DataRAM, the largest chip so far (187k NANDs, about 557 cycles/s), so they run at the CPU's own speed. Milestone 8 checks data memory through the runner, and the player's DataRAM first runs a program in milestone 9. A player who already solved the RAM levels keeps them solved, but will see them locked until the CPU is solved once the gate lands.


## 2026-11-09 — Runner-held memories in `.tst`, and the `.rom` format
**Context:** two earlier entries ("The program ROM comes after the CPU", "Data RAM comes after the CPU") left the syntax of the commands that attach a program memory and a data memory to the CPU, and the `.rom` file format, for when they were built. The CPU's pin names aren't decided yet.
**Decision:**
- **`attach rom addr=<pin> out=<pin>` and `attach ram in= addr= bank= status= load= out=`.** The memory's pins are named on the left and the chip's on the right, as in an HDL part. So the commands don't fix the CPU's pin names, and the RAM's are DataRAM's own, which a DataRAM will later plug into. The runner checks direction and width: `out` drives a chip input, the rest read chip outputs. The ROM's `addr` may have up to 12 bits, so a small test chip can use fewer.
- **Contents:** `rom <addr> <bytes>` writes bytes inline, so CPU tests can keep small programs next to their checks, and `rom <file>` loads a `.rom` file relative to the `.tst`. `ram`/`ramstatus <bank> <addr> <value>` set a character, and `expect ram`/`expect ramstatus` check one. A status character uses DataRAM's addressing: `addr[4..7]` and `addr[0..1]`. The word after `expect` is a cell only with four arguments, so a pin named `ram` still works with two.
- **Reads are combinational, settled by the runner.** On every `eval`, before and after `tick` (after only if the chip reads `clock`) and after `tock`, the runner evaluates, drives each memory's `out` from its address, and evaluates again until nothing changes, with at most 8 passes, then an error. Settling before the tick is what lets a CPU latch the byte it fetched in the same cycle, as a 4004 does in one instruction cycle. A pin a memory drives can't be `set`.
- **Writes act like a DFF:** sampled at `tick`, stored at `tock`. An undefined `load` writes nothing, because a CPU's control lines are undefined until its first reset cycle has run. `load` at 1 with an undefined address is a test failure.
- **Program memory starts as all 0** (NOP on the 4004), so a CPU that runs past its program executes NOPs. Data memory starts undefined, as a DataRAM built from DFFs does.
- **`.rom`: one byte per line, 8 binary digits,** grouped by spaces or `_`, with `//` comments. One byte per line keeps a line for each address, which suits the ROM editor of milestone 9. The parser is `nandsim.testing.parse_rom`, with errors at line and column.
- **The 4001 and 4002 output ports are left out.** Which pins carry them depends on the CPU's interface, so they come with the CPU level.
**Alternatives:**
- Fixed pin names (`romaddr`, `instr`, ...): this would decide the CPU's interface in a test-format change.
- Writes stored at the tick: a DataRAM shows a new value only after the tock, and the CPU's tests should pass with either.
- Several bytes per line, or hex: the earlier entry chose binary, and one byte per line keeps addresses easy to follow.
**Consequences:** with a memory attached, each cycle costs about three evaluations instead of two. `run_script` takes a `base` folder for `.rom` files, and the game passes the level's folder. The GUI's clock panel doesn't attach memories yet: playing a CPU level by hand needs that, and it comes with the CPU level.

## 2026-11-09 — The CPU has the 4004's own pins, bus and clock periods
**Context:** CLAUDE.md had the CPU compatible at the instruction level, "but not the real chip's multiplexed bus or clock phases", and earlier entries gave it a ROM address out, an instruction in and DataRAM-shaped RAM pins. Asked to settle the pins, the user chose the literal 16-pin 4004 over the 4004's signals on separate pins. Sources: Intel's *MCS-4 Micro Computer Set* manual (sections on basic system timing, the 4004's peripheral circuitry, the command control lines, the 4001 and the 4002, and DCL).
**Decision:**
- **Pins:** `CHIP CPU { IN din[4], test, reset; OUT dout[4], drive, sync, cmrom, cmram[4]; }`. The power and clock-phase pins (VDD, VSS, Φ1, Φ2) have no logic role: the global clock (tick, tock) stands in for Φ1 and Φ2. Logic is positive (1 = active), where the chip's is negative.
- **D0–D3 are split by direction,** because HDL has no two-way pins. While the CPU drives the bus, `drive` is 1 and `dout` carries the value. Otherwise `drive` is 0 and `dout` is 0, so a Computer level can OR together the outputs of every chip on the bus. `din` is the bus as the memories drive it.
- **One clock cycle (tick, tock) is one 4004 clock period. An instruction cycle is 8 of them, A1 A2 A3 M1 M2 X1 X2 X3,** as in the manual:
  - **A1, A2, A3:** the CPU sends the program address, low nibble first: bits 0–3, then 4–7, then 8–11. At A3, `cmrom` is 1, and the 4001 whose chip number matches the nibble is selected.
  - **M1, M2:** the selected ROM sends the instruction, OPR (the high nibble) at M1 and OPA at M2. If the instruction is an I/O or RAM instruction (OPR = 1110), `cmrom` and the CM-RAM lines that DCL selected are 1 at M2, so the 4001 and 4002 picked by SRC read OPA too.
  - **X1, X2, X3:** the CPU executes. For SRC it sends the register pair, the even register at X2 and the odd one at X3, with `cmrom` and the selected CM-RAM lines at 1 during X2. A 4002 takes chip `D3 D2` and register `D1 D0` from X2 and the character from X3. A 4001 takes its chip number from X2. For I/O and RAM instructions, the data moves at X2: the CPU drives the accumulator for writes (WRM, WMP, WRR, WR0–3, and WPM, which goes nowhere without a 4008/4009), and the selected chip drives `din` for reads (RDM, RDR, RD0–3, SBM, ADM).
  - **Two-word instructions** (JCN, FIM, JUN, JMS, ISZ) and FIN take two instruction cycles: 16 clocks.
- **`sync` is 1 during X3,** the period before each A1, so the memory chips can count the 8 periods from it. The CM-RAM lines are 0 at A3: only the 4001s read A3. The manual's text marks SYNC as the start of the cycle but doesn't name the period, and puts CM-ROM at A3 for the 4001s. Both details get checked against the 4004 datasheet's timing diagram before the timing level ships.
- **DCL drives the CM-RAM lines as in the manual's table:** 0 selects CM-RAM0, and 1–7 select CM-RAM1–3 by bit (`acc[0]` → CM-RAM1, `acc[1]` → CM-RAM2, `acc[2]` → CM-RAM3). A 3-to-8 decoder on CM-RAM1–3 gives the 8 banks, as in the manual, so bank n is DCL n, which matches DataRAM's `bank`.
- **Reset as on the chip:** `reset` must be held for 8 instruction cycles (64 clocks). That clears the PC, the stack, the accumulator, the carry and all 16 index registers, selects CM-RAM0, and keeps `drive` at 0. The first clock after reset is A1. A shorter reset leaves anything not yet cleared undefined. The real chip clears its registers through its refresh counter over those 8 cycles, so the reference CPU writes one register pair per instruction cycle. IndexRegs has no reset, and needs none.
- **The runner's memories become the MCS-4 chips on the bus.** `attach mcs4 din=… dout=… drive=… sync=… cmrom=… cmram=…` puts sixteen 4001s (the whole 4 KB, chip n holding addresses `n·256` to `n·256+255`, each with a 4-bit I/O port) and eight banks of four 4002s (with their output ports) on the CPU's pins. They follow `sync`, read the bus at each tick and drive `din` in their periods. The `rom`, `ram`, `ramstatus` and `expect ram`/`ramstatus` commands and the `.rom` format stay as they are. New commands `set romport <chip> <value>` (what RDR reads), `expect romport <chip> <value>` (what WRR wrote) and `expect ramport <bank> <chip> <value>` (WMP) cover the ports. A clock period where `drive` is 1 while a memory also drives the bus is a failure. `attach rom` and `attach ram`, with their address pins, were built for the pins this entry replaces and no level uses them, so they go. The exact syntax gets its own entry when built.
- **Superseded:** the CPU pins in "The program ROM comes after the CPU" (2026-11-08) and "Data RAM comes after the CPU" (2026-11-09). The order of the levels in those entries stands.
**Alternatives:**
- The 4004's signals on separate pins (address out, instruction in, one instruction cycle per clock): simpler, and what CLAUDE.md said, but not the chip the user asked for.
- Two-way pins in HDL with tri-state wires: they would need a new wire state and bus resolution in the engine, while splitting by direction costs only a `drive` pin.
- One clock per instruction cycle with the bus fields sent all at once: it would no longer be the 4004's bus.
**Consequences:**
- The CPU needs an 8-period timing generator, which is a natural first CPU level. Its tests run 8 clocks per instruction cycle, so a builtin ALU, IndexRegs or PC (each with its equivalence test) becomes more likely. The journal compares clocks/s ÷ 8 with the 4004's 92.5k instruction cycles per second.
- Milestone 9 gains bus levels: the 4001's and 4002's bus logic around the player's ROM4001 and RAM4002, so that they plug into the CPU. The RAM levels' pins stay as they are, as the inside of those chips.
- The emulator in project 2 works at the instruction level and isn't affected. The GUI can step through single clock periods, which shows the bus at work.
- CLAUDE.md now describes the pin-level 4004 and the 8-clock instruction cycle.

## 2026-11-09 — The MCS-4 memories on the bus: how the runner plays the 4001s and 4002s
**Context:** the entry before this one settled that `.tst` scripts attach 4001s and 4002s to the CPU's bus with `attach mcs4`, and left the syntax and the details for when it was built.
**Decision:**
- **`attach mcs4 din= dout= drive= sync= cmrom= cmram= reset=`.** It connects all seven signals, once, before any command that uses the memories. `reset` is the CPU's own input: the real 4001s and 4002s share the RESET line, and the memories need it to know where A1 is.
- **The memories count periods from reset and check `sync` instead of following it.** A tick with `reset` at 1 makes the next period A1. After that they count, and a `sync` that isn't 1 at X3 and only at X3 is a failure. Following `sync` would let a CPU with a broken timing generator half-work. Until the first reset the memories do nothing, so a CPU still undefined before its reset can't trip them.
- **`din` is 0 when no memory sends,** which matches the OR-the-outputs convention for the bus. While a memory sends, `din` is its value, undefined if the cell is.
- **Protocol failures name the period and stop after the first one.** The list: `sync` wrong; `dout` not 0 while `drive` is 0; the CPU not driving where it must (A1–A3, X2 and X3 of SRC, X2 of writes); driving while a memory sends; a RAM instruction with no 4002 selected by SRC in its bank, or with no CM-RAM line at M2; RDR with no 4001 selected; CM-RAM0 together with another line. A broken CPU repeats its mistake every cycle, so later ones would only bury the first.
- **Not checked, on purpose:** the CM lines at periods where no chip reads them, and the CM-RAM lines at A3, which the previous entry left to be confirmed against the datasheet.
- **A reset clears the SRC selections and sets every output port to 0, but keeps both memories.** The real 4002 needs 32 instruction cycles of reset to clear its RAM. Keeping memory lets a test fill it before resetting the CPU, and a CPU test never relies on reset clearing RAM.
- **Ports:** `set romport <chip> <value>` is what RDR reads from a 4001. `expect romport <chip>` and `expect ramport <bank> <chip>` check what WRR and WMP last wrote. The 4001's per-line choice of input or output is a mask option that doesn't matter here: input and output are kept apart. WPM writes nowhere, since no 4008/4009 is modelled.
- **`set` and `expect` decide by argument count:** with two arguments they read a pin, so a chip may still have a pin named `ram` or `romport`.
- **`attach rom` and `attach ram` are gone,** with the combinational settling they needed. Nothing reads `din` combinationally now: the memories decide what they send from their own state at the start of each period.
**Alternatives:**
- Following `sync` to find A1: more lenient, but it hides timing bugs that a real 4001 would also stumble on.
- Reporting every bus problem: one off-by-one in the timing generator would produce thousands of lines.
- Leaving `din` undefined when nobody sends: a CPU that reads the bus at the wrong period would see `x` instead of a wrong value. That is more honest, but it doesn't match the OR convention a Computer level will use.
**Consequences:** with memories attached, a cycle costs one more evaluation (the runner evaluates before the memories read the bus). The CPU level's tests are written in clock periods, 8 per instruction, and need the 64-clock reset. The developer tests use a pass-through `Bus` chip to drive the protocol by hand.

## 2026-11-09 — The Timing level, and CM-RAM at A3 corrected
**Context:** this is the first CPU level. "The CPU has the 4004's own pins" left two timing details to be checked against Intel's diagrams: SYNC during X3, and the CM-RAM lines at A3. The text of the MCS-4 manual didn't settle them, but its figures do. Figure 2 (Basic Instruction Cycle) and Figure 4 (Operation of the Command Control Lines) are images in the scanned manual, read here from the page images.
**Decision:**
- **SYNC is active during X3, the period before A1** (Figure 2), as decided.
- **Correction: the CM-RAM line DCL selected is active at A3 too, together with CM-ROM** (Figure 4: CM-ROM and the selected CM-RAM line pulse at every A3, at X2 of SRC and at M2 of an I/O or RAM instruction). The earlier entry said the CM-RAM lines are 0 at A3. The CPU level follows the figure. The runner's 4002s don't read A3, so neither the test memories nor their tests change.
- **`CHIP Timing { IN reset; OUT period[3], sync; }`** in a new group `05_cpu`, shown as "CPU", between Memory and Computer. `period` is 0 (A1) to 7 (X3) and steps once per clock cycle. A `reset` of 1 at a tick makes the next period A1. `sync` is `period == 7`.
- **`period` is a 3-bit number, not 8 one-hot lines.** The CPU decodes it with DMux8Way where it needs single periods. Most of the CPU needs only a few periods, and a number is easier to read on the canvas.
- **Parts:** Nand, Not, And, Mux, Mux4, Inc4, Bit, Register4. The reference is a Register4 that loads itself plus one (Inc4), a Mux4 that picks 0 on reset, and two Ands for `sync`. Bits with half adders also work.
- **Test (352 checks):** one cycle before any reset (`*`), a reset and 20 cycles (two and a half wraps), a reset at X2, a reset held for three cycles, a reset at X3, then 48 random cycles with seed 4004, from a Python model. Each cycle is checked after its tick (still the old period) and after its tock. These wrong chips fail it: `sync` at A1, `sync` at X2, a reset that lands on A2, and a reset that is ignored. A 4-bit count that never drops bit 3 passes, rightly: its pins can't be told apart from the 3-bit one.
**Alternatives:**
- One-hot periods (`a1`, …, `x3`): eight more pins, and more wiring on a chip the player first meets alone.
- The memories following `sync` instead of reset: rejected in the bus memories entry.
**Consequences:** the CPU will use Timing as a part. RAM8 still opens with Register4. The `requires = ["CPU"]` gate comes with the CPU level, as the Data RAM entry says.

## 2026-11-09 — The CPU levels before the CPU, and the Cond and CmLines levels
**Context:** the analysis of how to split the 4004 into levels proposed three small levels before the CPU (Cond, CmLines, InstrReg). A Decoder level waits until a reference CPU shows which control lines a natural design uses, since a Decoder's pins would fix the player's datapath before any CPU exists. This entry records that plan and the first two of those levels.
**Decision:**
- **The CPU group, in order:** Timing, Cond, CmLines, InstrReg, then the CPU. Each level before the CPU follows one of the 4004's own fields or signals rather than control lines of my choosing. A Decoder level is added only if the reference CPU turns out too large for one step, with pins taken from its control lines.
- **`CHIP Cond { IN cond[4], acc[4], carry, test; OUT jump; }`:** JCN's condition code as encoded, C1 C2 C3 C4 from the high bit (`cond[3]` is C1). `jump = C1 XOR ((C2 and acc = 0) or (C3 and carry = 1) or (C4 and test = 0))`, the equation in Intel's MCS-4 manual. So `JCN 0` never jumps and `JCN 8` always does. `test` is the TEST pin in positive logic. Parts: Nand, Not, And, Or, Xor, Or4Way. The test is exhaustive (1,024 rows).
- **`CHIP CmLines { IN bank[3], on; OUT cmram[4]; }`:** DCL's bank on the CM-RAM lines, from the manual's DCL table. Bank 0 raises `cmram[0]` alone, and banks 1–7 put their number on `cmram[1..3]`. `on` gates every line, because the CPU raises them only at A3, at M2 of I/O instructions and at X2 of SRC. Parts: Nand, Not, And, Or. The test is exhaustive (16 rows).
- **Wrong chips that fail the tests:**
  - Cond: the condition bits reversed, TEST active high, a jump on a nonzero accumulator, the tests combined with And, C1 ignored.
  - CmLines: CM-RAM0 ignoring `on`, one-hot bank lines, lines shifted by one.
**Alternatives:**
- Decoder and datapath levels now: more guidance, but they freeze an interface before the CPU exists.
- The CPU right after Timing: too big a step, given 46 instructions and a multiplexed bus.
- A `cmrom` output on CmLines: it would just repeat `on`.
**Consequences:** InstrReg is the next level, then a Python 4004 model in `tools/` that generates the CPU's tests, then the CPU with the `requires` gate on RAM8. Measured just now on the reference parts, the CPU should run at roughly 500–1,000 clocks/s (60–125 instruction cycles/s). The PC is the slowest part (1.7k cycles/s, 75 levels deep) and the first candidate for a builtin if tests get too slow.

## 2026-11-09 — The InstrReg level
**Context:** the last level before the CPU in the planned order. The bus brings each instruction one digit per period, and two-word instructions (JCN, FIM, JUN, JMS, ISZ) and FIN's fetch bring a second byte in the next instruction cycle, while the first word must stay.
**Decision:**
- **`CHIP InstrReg { IN din[4], period[3], second; OUT opr[4], opa[4], data[8]; }`.** `din` is stored at the tick of M1 (period 3) into `opr`, or into `data[4..7]` when `second` is 1, and at the tick of M2 (period 4) into `opa`, or into `data[0..3]`. Each digit shows from the tock on, like every register. Nothing else loads.
- **`second` is read at each period on its own,** so a change between M1 and M2 sends each digit where `second` says at that moment. The CPU keeps `second` steady over an instruction cycle, but the rule is simpler to state and test per digit.
- **`opr` is visible from M2 on,** which is what the CPU needs to raise the CM lines at M2 for an I/O or RAM instruction (OPR = 1110).
- **Parts:** Nand, Not, And, Mux4, DMux8Way, Register4, Register8. The reference is four Register4s with loads from DMux8Way's M1 and M2 lines, gated by `second`. Register8 and Mux4 are allowed for players who keep the second word in one register.
- **Test (936 checks):**
  - seven instruction cycles in period order with `second` at 0 or 1, four cycles where `second` changes between M1 and M2, then 96 random cycles, with seed 4004, from a Python model;
  - every cycle puts a new digit on `din`, different from what any register holds, so a load at the wrong time always shows;
  - each cycle is checked after its tick and after its tock.
  
  These wrong chips fail it: M1 and M2 swapped, periods off by one, `second` ignored for OPR, the second word's halves swapped, and OPA reloaded during the second word.
**Alternatives:**
- Loading `opr` and `opa` together at M2: OPR would arrive a period too late for the CM lines at M2.
- Leaving the second word to the CPU: InstrReg is where the bus timing lives, and the second word follows the same timing.
**Consequences:** next comes the Python 4004 model in `tools/`, then the CPU, which feeds InstrReg from `din` and Timing's `period`, and keeps `second` itself.

## 2026-11-09 — An instruction-level 4004 model in tools/, checked against Intel's manual
**Context:** the CPU level's tests need expected RAM, port and register contents for real programs, computed apart from the HDL. Earlier ALU work relied on the pyntel4004 docs because Intel's manual was unreachable. A scan of the *MCS-4 Micro Computer Set* manual has since been found, and its section VII describes every instruction.
**Decision:**
- **`tools/model4004.py`** is a development script, outside the game and its core. `Mcs4` is a 4004 with its memories as `attach mcs4` plays them: sixteen 4001s, eight banks of 4002s, SRC kept per bank, port outputs, and the RAM keys the runner uses. `step()` runs one instruction and returns its instruction cycles (2 for JCN, FIM, JUN, JMS, ISZ and FIN). `run()` goes until a jump to itself, the halt convention for test programs.
- **Semantics, all from section VII of the manual,** read from the page images:
  - SUB and SBM are `ACC + ~R + ~CY` (CY = 1 means no borrow).
  - DAA adds 6 if CY = 1 or ACC > 9, sets CY on overflow and otherwise leaves it.
  - DAC is `ACC + 15` (CY = 1 means no borrow).
  - TCS gives 9 or 10 and clears CY. KBP follows the manual's table.
  - JCN and ISZ jump within the page of the instruction after their second word, and JIN and FIN within the page of the next address. So all four reach the next page when they sit at the end of one.
  - JMS pushes the address after its second word onto a 4-level stack with a wrapping pointer, so a fourth nested call overwrites the oldest return. This matches the manual's figure and the PC level.
  - **This confirms, from the manual itself, the ALU semantics that "Four smaller levels before the 4004 ALU" took from pyntel4004.**
- **The model refuses to guess.** Reading RAM that was never written, RDR with no input set, a RAM instruction with no SRC in the current bank, and the codes the 4004 doesn't define (`0x01`–`0x0F`, `0xFE`, `0xFF`) each raise `ModelError`. So a test program can't depend on a value the hardware wouldn't define.
- **A small assembler** with labels, `org`, `byte`, `Rn`/`Pn`, and errors for jumps outside their page. Test programs stay readable, and Intel's listings can be retyped from their source. Project 3 builds the real assembler. This one only serves tests.
- **Checks** (`tests/test_model4004.py`):
  - every row of the ALU level's test (1,952) run as its instruction;
  - every row of Cond's (1,024) run as a JCN;
  - Intel's 16-digit decimal addition routine (manual section IV B), assembled from its source, on five pairs of numbers including one that carries through every digit and overflows, with the cycle count;
  - the stack overflow, page edges, ISZ, DCL and SRC per bank, ports and KBP, and assembler errors.
- **Intel's routine is assembled from its source, not its object code.** The listing's octal column doesn't match its own source (the bytes for `JUN NEXT` with NEXT = 0200 are given as 0310). The source lines and comments agree with the instruction descriptions.
**Alternatives:**
- Expected values written by hand in each `.tst`: unchecked and slow to extend to 46 instructions.
- The model inside `src/nandsim`: it is test tooling, and the emulator of project 2 will be its own package, which can start from this file.
**Consequences:** the CPU level's `.tst` files will be generated from this model, like the RAM levels' from `gen_ram_tst.py`, with a test that the committed files match. The manual's scan is the reference for the CPU from now on.

## 2026-11-09 — The CPU level, and why reset can't clear the index registers
**Context:** the goal of milestone 8: the 4004 on its own pins (decided earlier), built from the CPU group's levels and the earlier register, PC and ALU levels. Open questions: when each part changes within the 8 periods, how reset behaves, how the CPU is tested, and when the Computer group opens.
**Decision:**
- **`CHIP CPU { IN din[4], test, reset; OUT dout[4], drive, sync, cmrom, cmram[4]; }`.** Parts: the gates, the Mux and DMux family, And4, Or4, Or4Way, Inc4, Bit, the registers, Timing, InstrReg, Cond, CmLines, PC, IndexRegs and the ALU.
- **The reference's timing:**
  - **A1–A3:** the PC's nibbles. In FIN's second cycle they are P0's and then the PC's page.
  - **M1/M2:** InstrReg takes OPR and OPA.
  - **After A3:** the PC steps, except in FIN's second cycle.
  - **X2:** the accumulator, carry, index registers (one register, or a pair in a second cycle) and DCL load. I/O reads arrive on `din` at X2, and I/O writes and the first half of SRC go out then.
  - **X3:** SRC's second half goes out. Jumps load the PC, JMS pushes, BBL pops, and `second` is set or cleared.
  - **CM-ROM and DCL's CM-RAM lines** are up at A3, at M2 of OPR 1110 and at X2 of SRC.

  This is one working schedule, not a requirement: the test checks the bus and memory, not internal timing.
- **Reset can't clear the index registers, unlike the chip.** The real 4004 clears them over 8 instruction cycles with its refresh counter, which sweeps the pairs from whatever state it powers up in. In this simulator every DFF powers up undefined, and `reset` is the only defined input. A defined signal that changes over time can't be derived from all-undefined state and a constant input: any value the logic can be sure of is one it would also produce with every unknown bit set, and that doesn't change from clock to clock. IndexRegs has no reset pin, and adding one would change a solved level. So after reset the PC, the stack, A, CY and the DCL bank are 0, and the index registers stay as they were (undefined at power-on). This replaces the reset clause of "The CPU has the 4004's own pins". The model refuses to read a register before it is written, so no test depends on it, and the brief says a program must set registers before using them. Reset is still held for 64 clocks in the test, as on the chip.
- **The test is generated** by `tools/gen_cpu_tst.py` from the 4004 model, and a test keeps the committed file in step with it. One program covers all 46 instructions in segments, each on its own ROM page:
  - the accumulator group from set values of A and CY, starting with A and CY straight after reset;
  - registers, ADD, SUB and an ISZ loop;
  - every JCN condition, with TEST at 0 and at 1;
  - JMS three deep with BBL values;
  - FIN, JIN, and a FIN at a page's last byte;
  - DCL with SRC in two banks, every RAM, status and port instruction (WPM included);
  - Intel's 16-digit decimal addition, on operands whose sum carries out of 16 digits.

  Results go to RAM chip 1 through inline stores (and through a `put` subroutine in the JMS segment). After each segment the test checks every RAM character and port it changed: 126 checks over 7,500 clocks. Any bus mistake fails it at the period where it happens. Ten wrong CPUs fail it:
  - the PC stepping at A2;
  - SRC's halves swapped;
  - FIN fetching from the PC;
  - JIN into page 0;
  - DCL ignored;
  - BBL not returning;
  - no CM lines at M2;
  - `sync` at X2;
  - CY not cleared on reset;
  - ISZ jumping on zero.
- **`.tst` gains `cycles <n>`,** shorthand for n ticks and tocks, so a CPU test stays readable.
- **The runner evaluates less:** before a tick only if an input changed, and after driving `din` only if it changed. This halves the CPU test's time.
- **The Computer group opens after the CPU:** a level may list `requires`, levels that must be solved besides its parts. RAM8 requires CPU. `is_unlocked`, `missing` and the level-order test read it.
**Alternatives:**
- A reset pin on IndexRegs: it changes a solved level's interface and players' saves.
- Clearing registers with an undefined address: writes with an undefined load leave undefined registers undefined.
- One `.tst` per instruction group: a level has one test file, and a reset per group would add 64 clocks each.
- A Decoder level now: still possible, see the consequences.
**Consequences:**
- **Size and speed:** the reference is 5,639 primitives, 84 levels deep, in 110 parts. The test runs in about 4 s: roughly 2,000 clocks/s, 250 instruction cycles/s, against the real 4004's 92.5k. 110 parts is a lot for one level. If playtesting shows it, a Decoder level can be cut from the reference's control lines.
- **The GUI's clock panel doesn't attach the bus memories yet,** so the CPU can't be stepped by hand on a program. That is the next change.
- **Players:** players who solved RAM levels see them locked until they solve the CPU, as the RAM-after-CPU entry said.

## 2026-11-09 — IndexRegs gets a reset pin, so the CPU clears its registers as the 4004 does
**Context:** the CPU level left the 16 index registers undefined after reset, because nothing in the simulator can sweep them clear from all-undefined state. The user asked for the CPU to behave like the real 4004. Of three ways to do that, they chose to change the milestone 7 level: a reset pin on IndexRegs. The other two were a new level wrapping IndexRegs with per-register "written since reset" flags, and the same flags inside the CPU.
**Decision:**
- **`CHIP IndexRegs { IN in[8], addr[4], load, loadpair, reset; OUT out[4], pairout[8]; }`.** With `reset` at 1, the next cycle sets all 16 registers to 0, ahead of `load` and `loadpair`. The priority is now reset > loadpair > load. The parts are unchanged: the reference ORs reset into every register's load and muxes their inputs to 0.
- **The test** keeps its 496 checks with `reset` held at 0, then adds 41:
  - a reset in the same cycle as a load, which must win;
  - all 16 registers read back as 0;
  - a write after the reset;
  - a reset against `loadpair`.

  Three wrong IndexRegs fail it: one ignoring reset, one clearing only the addressed register, and one that loads on reset without zeroing.
- **The CPU passes `reset` to IndexRegs.** After a reset the PC, stack, A, CY, all 16 index registers and the DCL bank are 0, as on the chip, which needs 8 instruction cycles of RESET for this. Ours clears in one clock, but the test holds reset for 64 clocks as the chip requires. This replaces "reset can't clear the index registers" in the CPU level entry.
- **The model clears the registers on reset again.** They stay undefined only before the first reset, as at power-on in the simulator. The CPU test now reads R4, then FINs from P0 into P4 and reads R9, right after reset. A CPU that doesn't wire reset to IndexRegs fails at that check.
**Alternatives:**
- A ResetRegs level wrapping IndexRegs: no solved level would change, but it adds a level whose only purpose is a workaround.
- The flags inside the CPU: about 25 more parts in an already large level.
**Consequences:**
- **Saves:** an IndexRegs solved in v0.7.0 no longer has the level's pins. Its tests fail with "must keep the level's pins", and the CPU can't use it until the player adds `reset`. The level stays marked solved, since solved is sticky, and the changelog says what to do.
- **Earlier entries:** the IndexRegs entry of 2026-11-07 still holds, apart from the pins and the priority.

## 2026-11-09 — The CPU is split into five unit levels
**Context:** the CPU level's reference was about 110 parts. The user found that too much for one level. Of three splits, they chose functional units over a single Decoder level (leaving the CPU around 75 parts) and over Datapath + Control (two levels of about 50 parts each).
**Decision:**
- **Five new levels between InstrReg and the CPU,** each one job of the chip, carved from the reference so nothing about the CPU's behaviour changes:
  - **`Sequencer { IN opr[4], opa[4], period[3], reset; OUT second, finfetch; }`:** `second` changes at X3 and marks the second cycle of JCN FIM FIN JUN JMS ISZ. `finfetch` is `second` and FIN.
  - **`Accumulator { IN opr[4], opa[4], reg[4], din[4], write, reset; OUT acc[4], carry, bank[3]; }`:** with `write`, the instruction's effect on A and CY (OPR 8–D, the I/O reads, the accumulator group through the ALU) and DCL's bank.
  - **`Registers { IN opr[4], opa[4], acc[4], data[8], second, write, readp0, reset; OUT reg[4], pair[8]; }`:**
    - **Reads:** register OPA and its pair, or pair 0 while `readp0` is 1.
    - **Writes, with `write`:** XCH, INC and ISZ in a first cycle, FIM and FIN to a pair in a second cycle.
    - **Contract:** `readp0` and `write` are never 1 together.
  - **`Jumps { IN opr[4], opa[4], data[8], pair[8], reg[4], acc[4], carry, test, second, step, exec, reset; OUT pc[12]; }`:**
    - **`step`:** steps the PC.
    - **`exec`, in a second cycle:** JUN, JMS, and JCN and ISZ when they jump.
    - **`exec`, in a first cycle:** JIN and BBL.
    - **Contract:** `step` and `exec` are never 1 together.
  - **`BusOut { IN period[3], pc[12], pair[8], acc[4], opr[4], opa[4], second, finfetch, bank[3]; OUT dout[4], drive, cmrom, cmram[4]; }`:** everything on the pins, combinational.
- **The units take OPR and OPA and decode what they need themselves,** rather than taking control lines from a shared decoder. Each brief is then about the instructions, which players know from the 4004, not about wires invented for this design. The cost is some repeated decoding: a few DMux8Ways.
- **The CPU is 16 parts:** Timing, a DMux8Way of the periods, InstrReg, the five units, and a few gates that give each unit its moment:
  - **Registers:** write at X2, and `readp0` at A1–A3 of FIN's fetch;
  - **Accumulator:** write at X2 of a first cycle;
  - **Jumps:** step after A3 outside FIN's fetch, and exec at X3.

  Its parts are Nand, Not, And, Or, Mux, Mux4, DMux8Way, Timing, InstrReg and the five units.
- **Each unit's test is generated** by `tools/gen_cpu_units.py` from a small model of the unit (`tests/test_tools.py` keeps the files in step):
  - Sequencer, Accumulator, Registers and Jumps are sequential: before any reset, then a reset, then targeted and random cycles, checked after each tick and tock.
  - BusOut is a table: every period against ten kinds of instruction, then 400 random rows.
  - The Accumulator's arithmetic comes from the 4004 model.

  The checks: Sequencer 2,440, Accumulator 3,354, Registers 2,004, Jumps 836, BusOut 1,924. Nineteen wrong units each fail their test, among them `second` changing at X2, DCL ignored, ADM as SUB, FIM writing in its first cycle, `readp0` ignored, JIN into page 0, JMS loading instead of pushing, SRC's halves swapped and `dout` not 0 when idle.
- **The CPU's test is unchanged** (128 checks), and the CPU built from the units passes it.
**Alternatives:**
- A shared Decoder level feeding control lines to the units: one place for decoding, but the units' pins would be invented control lines, and Decoder would have around 20 outputs.
- Splitting further, for example the ALU's operand choice out of Accumulator: the units are 20–30 parts, about the size of the larger earlier levels.
**Consequences:** the CPU group has 10 levels. A player's CPU is now mostly timing: which period each unit acts in. The size and speed figures in the CPU level entry still hold for the whole chip: the units add no gates, only boundaries.

## 2026-11-09 — One level group per chip of the computer, and a tour bubble per group
**Context:** The RAM levels sat in a catch-all *Computer* group, which would have grown to hold the ROM and the bus logic as well: separate chips of the MCS-4 family mixed in one list. The tour and the early briefs taught the editor but never said what the player was building toward.
**Decision:** Each chip of the computer gets its own group, labelled with Intel's part number: `06_ram` is *RAM (4002)*, the CPU's group is *CPU (4004)*, and the ROM and bus levels will get their own (`07_rom`, …). The folder rename doesn't touch saves, which are keyed by level name. The tour's welcome names the goal (the 4004, then its computer), and the first level of each group shows one `next` bubble anchored on the level list, on what that group adds. A test fails if a group has no bubble at its first level. Briefs that didn't link their chip to the 4004 get one plain paragraph that does, before the parts line; it isn't bold, so the parts and hint lines stay the ones that stand out.
**Alternatives:** Group descriptions in `levels.toml` shown under each sidebar header (takes space in a list that is already long, and isn't seen at the right moment); a label such as "In the 4004:" on each new brief paragraph (the sentences already name the 4004, so it read twice).
**Consequences:** The tour grows from 25 to 31 steps. New groups need a bubble at their first level, and a brief needs a word on where its chip goes.
