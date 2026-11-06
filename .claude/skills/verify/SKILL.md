---
name: verify
description: Run NAND Sim's definition-of-done gate (pytest, every level's .tst against its reference, ruff, core/GUI boundary, headless GUI smoke test) and report each gate. Use before declaring any step done, before a PR, and whenever asked to check, test, or verify.
---

# Verify

Run every gate, even after one fails, so the report is complete. Do not fix anything here. Report only.

## Gates

```bash
uv run pytest -q
uv run python -m nandsim test --impl reference chips/
uv run ruff check .
uv run ruff format --check .
grep -rnE '^\s*(import|from)\s+pygame' src/nandsim/{hdl,netlist,sim,testing} && echo "BOUNDARY VIOLATION" || echo "boundary ok"
```

- **Levels:** each level in `chips/levels.toml` must have a stub `.hdl`, a brief `.md`, a `.tst`, and a reference in `reference/`. Every part a level allows must be unlocked earlier.
- **GUI**, only if `src/nandsim/gui/` changed on this branch (`git diff --name-only main...`): run the headless smoke test with `SDL_VIDEODRIVER=dummy`. Save a screenshot to `screenshots/` and look at it with Read. Check that the circuit is drawn, errors show inline, and nothing from `reference/` appears.

Before milestone 1 there is no package yet. Say so plainly instead of reporting the gates as failures.

## Report

One line per gate, ✅ or ❌. Under each ❌, put the relevant part of the failing output.

The verdict is **green** only if every gate passes. Never call a red gate done, flaky, or "unrelated" without evidence.
