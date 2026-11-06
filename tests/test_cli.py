"""Tests for the command-line interface."""

from __future__ import annotations

from pathlib import Path

import pytest

from nandsim.__main__ import build_parser, main

NOT_TST = "chip Not\ntable in | out\n 0 | 1\n 1 | 0\nend\n"


def test_subcommands_parse() -> None:
    args = build_parser().parse_args(["test", "--impl", "save", "chips/"])
    assert args.command == "test"
    assert args.impl == "save"
    assert args.paths == [Path("chips/")]


def test_command_required() -> None:
    with pytest.raises(SystemExit):
        main([])


def test_pass_and_fail_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tst = tmp_path / "Not.tst"
    tst.write_text(NOT_TST)
    save = tmp_path / "save"
    save.mkdir()
    (save / "Not.hdl").write_text("CHIP Not { IN in; OUT out; PARTS: Nand(a=in, b=in, out=out); }")

    assert main(["test", "--impl", "save", "--save-dir", str(save), str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert f"PASS {tst} (2 checks)" in out and "1/1 passed" in out

    (save / "Not.hdl").write_text("CHIP Not { IN in; OUT out; PARTS: }")
    assert main(["test", "--impl", "save", "--save-dir", str(save), str(tst)]) == 1
    out = capsys.readouterr().out
    assert f"FAIL {tst}" in out
    assert "error: output pin 'out' of Not is not connected" in out
    assert "0/1 passed" in out


def test_gui_not_yet(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["gui"]) == 2
    assert "milestone 2" in capsys.readouterr().err
