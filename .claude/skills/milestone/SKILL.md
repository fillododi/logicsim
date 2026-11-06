---
name: milestone
description: Close a NAND Sim milestone — check every item from CLAUDE.md is done, run verify, write the journal entry, cut the changelog release, open the closing PR, and tag v0.N.0 after merge. Use when asked to close, finish, or wrap up a milestone.
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
7. **Tag:** after the user merges the PR, run `git switch main && git pull`, then `git tag -a v0.N.0 -m "Milestone N: <name>"`. Push the tag only after the user confirms.
