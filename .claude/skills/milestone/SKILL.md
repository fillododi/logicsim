---
name: milestone
description: Close a NAND Sim milestone — check every item from CLAUDE.md is done, run verify, write the journal entry, cut the changelog release, open the closing PR, then tag v0.N.0 and publish the GitHub release with the built wheel after merge. Use when asked to close, finish, or wrap up a milestone.
---

# Milestone

Argument: the milestone number N (1–6). If it is missing, infer it from `docs/journal.md`: N is the first milestone that has no entry yet.

## Steps

1. **Checklist:** list every item of milestone N from the Milestones section of `CLAUDE.md`. For each item, give its evidence (a file, a test, a level) or mark it ❌ missing. If anything is missing, stop and propose a `/make-change` for each gap.
2. **Gate:** run `/verify`. It must be green.
3. **Docs:** make sure `docs/hdl.md`, `docs/tst.md`, and `docs/decisions.md` reflect what was built.
4. **Journal:** append to `docs/journal.md`:

   ```
   ## Milestone N — <name> (YYYY-MM-DD)
   **Built:** …
   **Problems and how they were solved:** …
   **Learned:** …
   **Numbers:** tests, levels, LOC; engine speed where relevant (simulated clock Hz is required at M6)
   **Next:** what milestone N+1 starts with
   ```

   For the numbers, measure; don't estimate. Say how each was measured.
5. **Release notes:** in `CHANGELOG.md`, rename `## [Unreleased]` to `## [0.N.0] — YYYY-MM-DD` and add a fresh empty `## [Unreleased]` above it. Tidy the entries so they read as release notes for a player. Update the link references at the bottom (`[Unreleased]` compares `v0.N.0...HEAD`; `[0.N.0]` compares to the previous tag). Set `version = "0.N.0"` in `pyproject.toml` and run `uv lock`.
6. **PR:** commit the journal, changelog and version bump on the milestone branch (or a `docs/milestone-N` branch), then run `/pr`.
7. **Tag:** after the user merges the PR, run `git switch main && git pull`, then `git tag -a v0.N.0 -m "Milestone N: <name>"`.
8. **Publish:** ask the user once to confirm publishing; tag and release are public. On a yes:
   - `git push origin v0.N.0`
   - Extract the `## [0.N.0]` section of `CHANGELOG.md` (without its heading, up to the next `## [` or the link references) into a temp file.
   - `rm -rf dist && uv build` on the tagged commit.
   - `gh release create v0.N.0 --title "0.N.0 — Milestone N: <name>" --notes-file <tmpfile> dist/nandsim-0.N.0-py3-none-any.whl dist/nandsim-0.N.0.tar.gz`
   - **Check it:** from an empty temp dir, run `uvx --from https://github.com/fillododi/logicsim/releases/download/v0.N.0/nandsim-0.N.0-py3-none-any.whl nandsim test`. All levels must pass.
   - Give the user the release URL and the `uv tool install <wheel URL>` command.
