"""Command-line entry point: the `gui` and `test` subcommands."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from nandsim.testing import Impl, TstResult, load_levels, run_tst


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the `nandsim` command."""
    parser = argparse.ArgumentParser(prog="nandsim", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    gui = sub.add_parser("gui", help="play the game (or, with a file, edit and view one chip)")
    gui.add_argument("file", nargs="?", type=Path, help=".hdl file to view (developer mode)")
    gui.add_argument(
        "--search",
        type=Path,
        action="append",
        help="directory to look for parts in (repeatable; default: next to the file and one up)",
    )
    gui.add_argument("--no-edit", action="store_true", help="view only, without the editor pane")
    gui.add_argument("--save-dir", type=Path, help="where the player's chips are stored")

    test = sub.add_parser("test", help="run .tst files (default: every level)")
    test.add_argument("paths", nargs="*", type=Path, help=".tst files or directories")
    test.add_argument(
        "--impl",
        choices=["reference", "save"],
        default="reference",
        help="which implementation to test: hidden reference or the player's save",
    )
    test.add_argument("--save-dir", type=Path, help="player save directory (with --impl save)")
    return parser


def collect(paths: list[Path]) -> list[Path]:
    """Expand directories to the `.tst` files inside; no paths means every level in order."""
    if not paths:
        return [lv.tst for lv in load_levels()]
    files: list[Path] = []
    for p in paths:
        files += sorted(p.rglob("*.tst")) if p.is_dir() else [p]
    return files


def report(result: TstResult) -> str:
    if result.passed:
        return f"PASS {result.path} ({result.checks} checks)"
    lines = [f"FAIL {result.path}"]
    if result.error is not None:
        lines.append(f"  {result.error}")
    lines += [f"  {f}" for f in result.failures]
    return "\n".join(lines)


def cmd_test(args: argparse.Namespace) -> int:
    impl = Impl(args.impl, args.save_dir)
    files = collect(args.paths)
    if not files:
        print("no .tst files found", file=sys.stderr)
        return 1
    results = [run_tst(f, impl) for f in files]
    for r in results:
        print(report(r))
    failed = sum(not r.passed for r in results)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to a subcommand. Returns the exit code."""
    args = build_parser().parse_args(argv)
    if args.command == "test":
        return cmd_test(args)
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")  # no banner in the terminal
    if args.file is None:
        from nandsim.gui.game_app import open_game  # pygame is imported only for the GUI

        return open_game(args.save_dir)
    if not args.file.is_file():
        print(f"nandsim gui: no such file: {args.file}", file=sys.stderr)
        return 1
    from nandsim.gui.app import open_viewer  # pygame is imported only for the GUI

    return open_viewer(args.file, args.search, edit=not args.no_edit)


if __name__ == "__main__":
    sys.exit(main())
