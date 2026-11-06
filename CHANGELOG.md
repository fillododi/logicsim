# Changelog

All notable changes to NAND Sim are listed here, newest first.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each milestone is
released as version `0.N.0` (milestone 1 = `0.1.0`, …, milestone 6 = `0.6.0`).

## [Unreleased]

### Added
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
