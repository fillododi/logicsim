# Changelog

All notable changes to NAND Sim are listed here, newest first.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each milestone is
released as version `0.N.0` (milestone 1 = `0.1.0`, …, milestone 6 = `0.6.0`).

## [Unreleased]

### Added
- The first six levels: Not, And, Or, Xor, Mux, DMux. Each has a starting stub, a brief with
  its truth table and a hint, and a test.
- The HDL: chips built from parts, with buses (`a[8]`), slices (`a[0..3]`) and the constants
  `true` and `false`. Mistakes are reported with their exact line and column and a clear
  message (unknown pin, wrong width, unconnected output, combinational loop, …).
- The simulator: every wire is 0, 1 or undefined, and whole chips are flattened to NAND gates and
  evaluated level by level.
- The `.tst` test format: truth tables and scripts, with values in decimal, binary and hex.
  A failure shows the row and the inputs that caused it.
- `nandsim test` runs every level (or chosen `.tst` files) against the reference or against your
  saved chips (`--impl save`). It also works from an installed wheel.
- Project guide (`CLAUDE.md`) describing NAND Sim as a game: the player writes chips in an in-game
  HDL editor; levels ship with an interface stub, a brief, a `.tst` and a hidden reference solution.
- Workflow skills for Claude: `/analyze`, `/make-change`, `/verify`, `/pr`, `/review`, `/milestone`.
- Python package skeleton managed with `uv`: `nandsim` CLI with `gui` and `test` subcommands
  (not implemented yet), core packages `hdl`, `netlist`, `sim`, `testing` and the `gui` package.
- Test that the core packages import without pygame.
- CI on GitHub Actions running ruff, pytest and (from milestone 1) the level tests; `main` is
  protected and requires it.
- Design decisions in `docs/decisions.md`: level layout, save location, three-valued wires,
  bit-level levelized engine.
- This changelog.
- MIT license.

[Unreleased]: https://github.com/fillododi/logicsim/commits/main
