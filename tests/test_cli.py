"""Smoke tests for the command-line interface."""

from __future__ import annotations

import pytest

from nandsim.__main__ import build_parser, main


def test_subcommands_parse() -> None:
    args = build_parser().parse_args(["test", "--impl", "save", "chips/"])
    assert args.command == "test"
    assert args.impl == "save"
    assert args.paths == ["chips/"]


def test_command_required() -> None:
    with pytest.raises(SystemExit):
        main([])
