---
name: pr
description: Open a GitHub pull request for the current NAND Sim branch after a green verify, with a body covering why, what, decisions, and how it was verified. Use when asked to open, create, or send a PR, or to ship a finished branch.
---

# PR

## Preconditions

- The current branch is not `main` and the working tree is clean. If there are uncommitted changes, ask the user before committing them.
- `/verify` ran green on the current HEAD. If it did not, run it, and stop if any gate is red.

## Steps

1. Read the changes since `main`: `git log --oneline main..HEAD` and `git diff --stat main...HEAD`.
2. Push the branch: `git push -u origin <branch>`.
3. Run `gh pr create --base main --title "<imperative summary>" --body-file <tmpfile>` with this body:

   ```markdown
   ## Why
   <problem or goal, 1–3 sentences>

   ## What changed
   - <bullet per meaningful change>

   ## Decisions
   - <link to each new docs/decisions.md entry, or "none">

   ## How verified
   - <verify gate summary: pytest N passed, levels N/N, ruff clean>
   - <screenshot for GUI changes>
   ```

   Never write a bare `@name` unless you mean to notify that person.
4. Give the user the PR URL.

**Never merge, close, or force-push** unless the user asks to.
