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
