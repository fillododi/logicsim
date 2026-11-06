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
