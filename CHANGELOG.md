# Changelog

All notable changes to NAND Sim are listed here, newest first.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each milestone is
released as version `0.N.0` (milestone 1 = `0.1.0`, …, milestone 6 = `0.6.0`).

## [Unreleased]

## [0.1.0] — 2026-11-06

Milestone 1: the core. There is no GUI yet; chips are tested from the command line.

### Added
- **Six levels:** Not, And, Or, Xor, Mux, DMux. Each starts from a stub with the chip's pins and
  comes with a brief (what the chip does, its truth table, a hint) and a test.
- **The HDL:** chips are built from parts, with buses (`a[8]`), slices (`a[0..3]`) and the
  constants `true` and `false`. Every mistake is reported at its exact line and column with a
  clear message: unknown pin, wrong width, unconnected output, combinational loop, and more
  (see `docs/hdl.md`).
- **The simulator:** every wire is 0, 1 or undefined. A chip is flattened to NAND gates and
  evaluated level by level.
- **Tests:** the `.tst` format has truth tables and scripts, with values in decimal, binary and
  hex. A failure shows the row and the inputs that caused it (see `docs/tst.md`).
- **`nandsim test`:** runs every level, or chosen `.tst` files, against the reference or against
  your own chips (`--impl save --save-dir <dir>`). It works from a source checkout and from an
  installed package.

### Project
- MIT license, CI on every pull request, and a protected `main` branch.
- Design decisions in `docs/decisions.md`, a development journal in `docs/journal.md`, and this
  changelog.
- Workflow skills for Claude Code: `/analyze`, `/make-change`, `/verify`, `/pr`, `/review` and
  `/milestone`.

[Unreleased]: https://github.com/fillododi/logicsim/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fillododi/logicsim/releases/tag/v0.1.0
