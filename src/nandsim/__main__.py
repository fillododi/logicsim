"""Command-line entry point: the `gui` and `test` subcommands."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nandsim.testing import Impl, TstResult, load_levels, run_tst


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the `nandsim` command."""
    parser = argparse.ArgumentParser(prog="nandsim", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    gui = sub.add_parser("gui", help="play: level select and HDL editor")
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
    print("nandsim gui: the GUI arrives in milestone 2", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
