"""Command-line entry point: the `gui` and `test` subcommands."""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the `nandsim` command."""
    parser = argparse.ArgumentParser(prog="nandsim", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    gui = sub.add_parser("gui", help="play: level select and HDL editor")
    gui.add_argument("--save-dir", help="where the player's chips are stored")

    test = sub.add_parser("test", help="run .tst files")
    test.add_argument("paths", nargs="+", help=".tst files or directories")
    test.add_argument(
        "--impl",
        choices=["reference", "save"],
        default="reference",
        help="which implementation to test: hidden reference or the player's save",
    )
    test.add_argument("--save-dir", help="player save directory (with --impl save)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to a subcommand. Returns the exit code."""
    args = build_parser().parse_args(argv)
    print(f"nandsim {args.command}: not implemented yet", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
