---
name: analyze
description: Read-only investigation of a question, bug, or area of the NAND Sim codebase before changing anything. Use when asked to analyze, investigate, explain, or figure out how something works or why something fails, or before a non-trivial change whose approach is unclear.
---

# Analyze

Investigate. **Do not edit, create, or delete project files, and do not commit.** Scratch scripts go in the scratchpad directory.

## Steps

1. Restate the question in one sentence. If it is too vague to investigate, ask one clarifying question.
2. Read the relevant code, docs (`docs/hdl.md`, `docs/tst.md`, `docs/decisions.md`), and tests. Check `docs/decisions.md` for decisions already taken on this topic, so you don't reopen them.
3. For a bug, reproduce it: give the exact command, the observed output, and the expected output. If it does not reproduce, say so.
4. Check the question against the hard rules in `CLAUDE.md`: no pygame in the core, the levelized numpy engine, only `Nand` as the player's primitive (the DFF is built from latches), builtins only with an equivalence test, the reference never visible to the player.

## Report

Keep it short and scannable:

- **Answer / root cause**: the direct answer first.
- **Where**: the relevant files as `path:line`.
- **How it works today**: only what is needed to follow the answer.
- **Options**: if there is a choice to make, give a recommendation first and the alternatives in one line each.
- **Risks**: what could break, and what is hard to undo.
- **Next step**: usually `/make-change <scope>`, with the scope stated precisely.
