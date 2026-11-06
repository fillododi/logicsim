---
name: make-change
description: Implement one scoped change to NAND Sim end to end — branch, small green commits, decisions and docs, then the verify gate. Use for any feature, fix, refactor, level, or docs change once the scope is clear.
---

# Make change

## 1. Scope and branch

- State the scope in one or two sentences. If it is unclear, run `/analyze` first.
- Start from an up-to-date `main` and create a branch named `feat/<slug>`, `fix/<slug>`, `refactor/<slug>`, `level/<slug>` or `docs/<slug>`. Never commit on `main`.

## 2. Implement in small green steps

- **Bug:** first write a test that fails because of the bug, then fix it.
- **Feature:** write tests together with the code. Each new HDL or `.tst` error gets a test that asserts the exact message, including `line:col` and the names of the involved pins.
- **Level:** write the interface stub, the brief `.md` (what the chip does and one hint, never the solution), and the `.tst`: exhaustive up to about 8 input bits, otherwise edge cases plus random vectors with a fixed seed. Write the reference in `reference/` using only parts the level allows, and add the `chips/levels.toml` entry. Check that the reference passes and that the empty stub fails with a clear message, not a crash.
- After each step that is green, commit it on its own. Stage files by name, not with `git add -A`. The message says **why**, not only what changed.

## 3. Hard rules (from CLAUDE.md)

- Type hints everywhere, a docstring for each module, and dataclasses for AST and netlist structures.
- The core (`hdl`, `netlist`, `sim`, `testing`) never imports pygame.
- The engine evaluates level by level with vectorized numpy, with no Python object per gate.
- No new runtime dependency without asking the user.
- Builtins only after the HDL version passes, and always with an equivalence test.

## 4. Decisions and docs

- When a spec point is ambiguous, pick the simplest reasonable option and keep going. Append this to `docs/decisions.md`:

  ```
  ## YYYY-MM-DD — <title>
  **Context:** … **Decision:** … **Alternatives:** … **Consequences:** …
  ```

  Ask the user only about decisions that are hard to undo.
- When behavior changes, update `docs/hdl.md`, `docs/tst.md`, or the in-game help in the same branch.

## 5. Finish

Run `/verify`. If any gate is red, fix it and run it again. When it is green, report what changed, which decisions were taken, and suggest `/pr`.
