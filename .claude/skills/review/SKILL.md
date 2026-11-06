---
name: review
description: Review a NAND Sim branch or PR against the project's own checklist, then run the built-in code review for bugs. Use when asked to review a branch, a PR, or a set of changes.
---

# Review

Target: a PR number (`gh pr diff <n>`), a branch (`git diff main...<branch>`), or the current branch by default.

## 1. Project checklist

For each item, mark ✅, ❌ (with `path:line`), or n/a.

- **Boundary:** no pygame import in `hdl`, `netlist`, `sim`, or `testing`. The GUI uses only the core's public API.
- **Engine:** evaluation is levelized and uses vectorized numpy over flat arrays, with no Python object per gate. Inner wire values stay inspectable.
- **Primitives:** only `Nand` and `DFF`. Every builtin has an HDL version that passes and an equivalence test.
- **Errors:** messages are precise (`line:col`, the pins involved) and a player can understand them. Each one has a test. Errors never crash the GUI.
- **Levels:** each new level has a stub, a brief, a `.tst`, a reference, and a `levels.toml` entry. The brief does not give away the solution. The reference is never reachable from the player's view.
- **Conventions:** type hints, module docstrings, dataclasses for AST and netlist structures, no new runtime dependencies.
- **Docs:** ambiguous points are recorded in `docs/decisions.md`. `docs/hdl.md` and `docs/tst.md` match any change in behavior. Every user-visible change has a `CHANGELOG.md` entry under `[Unreleased]`.
- **Commits:** small, each one green, each message says why.

## 2. Bugs

Run the built-in `/code-review` on the same target to find correctness bugs. Don't duplicate its findings in the checklist.

## 3. Report

Rank the findings most severe first. Each finding says what is wrong, where, and the fix. End with a verdict: approve, approve with nits, or changes requested.

Post the findings as PR comments only if the user asks for it.
