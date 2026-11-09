"""Runner-held program and data memories in `.tst` scripts, and the `.rom` format."""

from __future__ import annotations

from pathlib import Path

import pytest

from nandsim.hdl import HdlError
from nandsim.netlist import ChipLibrary
from nandsim.testing import TstResult, parse_rom, parse_tst, run_script

# Reads the program memory at `a`, and shows the byte it gets back on `data`.
ECHO = """CHIP Echo {
    IN instr[8], a[12];
    OUT addr[12], data[8];
    PARTS:
    addr = a;
    data = instr;
}"""

# The byte at `a` is latched at the tick, as a CPU latches the instruction it fetched.
FETCH = """CHIP Fetch {
    IN instr[8], a[12];
    OUT addr[12], q;
    PARTS:
    addr = a;
    DFF(in=instr[0], out=q);
}"""

# Its address bit 0 is NOT the byte's bit 0 once `go` is 1: with rom bytes 0 and 1 at
# addresses 0 and 1 it chases its own tail.
LOOP = """CHIP Loop {
    IN instr[8], go;
    OUT addr[12];
    PARTS:
    Nand(a=instr[0], b=go, out=addr[0]);
    addr[1..11] = false;
}"""

# Every DataRAM pin brought out to an input, and the character read back on `r`.
PORT = """CHIP Port {
    IN ramout[4], i[4], a[8], b[3], s, l;
    OUT ramin[4], ramaddr[8], bank[3], status, ramload, r[4];
    PARTS:
    ramin = i;
    ramaddr = a;
    bank = b;
    status = s;
    ramload = l;
    r = ramout;
}"""

ATTACH_RAM = "attach ram in=ramin addr=ramaddr bank=bank status=status load=ramload out=ramout"


def run(tmp_path: Path, hdl: str, tst: str) -> TstResult:
    name = hdl.split()[1]
    (tmp_path / f"{name}.hdl").write_text(hdl)
    (tmp_path / f"{name}.tst").write_text(tst)
    script = parse_tst(tst, str(tmp_path / f"{name}.tst"))
    return run_script(script, ChipLibrary([tmp_path]), None)


def messages(result: TstResult) -> list[str]:
    return [str(f) for f in result.failures]


# ---- the .rom format ------------------------------------------------------


def test_rom_file_one_byte_per_line_with_comments_and_groups() -> None:
    text = "// header\n1101 0101   // LDM 5\n\n0000_0000\n11110010\n"
    assert parse_rom(text, "p.rom") == [0xD5, 0x00, 0xF2]


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("1101 010\n", "p.rom:1:1: error: a byte has 8 binary digits, this line has 7"),
        (
            "00000000\n  1101 01011\n",
            "p.rom:2:3: error: a byte has 8 binary digits, this line has 9",
        ),
        (
            "1101 0x01\n",
            "p.rom:1:7: error: 'x' in a byte: write each byte as 8 binary digits, like 1101 0101",
        ),
        ("00000000\n" * 4097, "p.rom:4097:1: error: too many bytes: program memory holds 4096"),
    ],
)
def test_rom_file_errors(text: str, message: str) -> None:
    with pytest.raises(HdlError) as e:
        parse_rom(text, "p.rom")
    assert str(e.value) == message


# ---- parsing the commands -------------------------------------------------


@pytest.mark.parametrize(
    ("text", "message"),
    [
        (
            "chip X\nrom 0 1\n",
            "t.tst:2:1: error: 'rom' needs a program memory: add 'attach rom ...' before it",
        ),
        (
            "chip X\nram 0 0 1\n",
            "t.tst:2:1: error: 'ram' needs a data memory: add 'attach ram ...' before it",
        ),
        (
            "chip X\nexpect ramstatus 0 0 1\n",
            "t.tst:2:1: error: 'expect' needs a data memory: add 'attach ram ...' before it",
        ),
        ("chip X\nattach rom addr=a\n", "t.tst:2:1: error: attach rom must connect out"),
        (
            "chip X\nattach rom addr=a data=d\n",
            "t.tst:2:19: error: the rom has no pin 'data' (its pins: addr, out)",
        ),
        (
            "chip X\nattach rom addr=a addr=b\n",
            "t.tst:2:19: error: the rom's pin 'addr' is connected twice",
        ),
        (
            "chip X\nattach rom addr out=o\n",
            "t.tst:2:12: error: expected <memory pin>=<chip pin>, found 'addr'",
        ),
        (
            "chip X\nattach disk\n",
            "t.tst:2:1: error: usage: attach rom addr=<pin> out=<pin>, or attach ram in=<pin> "
            "addr=<pin> bank=<pin> status=<pin> load=<pin> out=<pin>",
        ),
        (
            "chip X\nattach rom addr=a out=o\nattach rom addr=a out=o\n",
            "t.tst:3:1: error: a rom is already attached",
        ),
        (
            "chip X\nattach rom addr=a out=o\nrom 5\n",
            "t.tst:3:1: error: usage: rom <addr> <byte>... or rom <file>.rom",
        ),
        (
            "chip X\n" + ATTACH_RAM + "\nram 0 1\n",
            "t.tst:3:1: error: usage: ram <bank> <addr> <value>",
        ),
        (
            "chip X\n" + ATTACH_RAM + "\nexpect ram 0 1\n",
            "t.tst:3:1: error: usage: expect ram <bank> <addr> <value>",
        ),
    ],
)
def test_memory_command_errors(text: str, message: str) -> None:
    with pytest.raises(HdlError) as e:
        parse_tst(text, "t.tst")
    assert str(e.value) == message


def test_expect_on_a_pin_named_ram_still_works() -> None:
    script = parse_tst("chip X\nexpect ram 1\n", "t.tst")
    assert script.steps[0].pin == "ram"  # type: ignore[union-attr]


# ---- the program memory ---------------------------------------------------


def test_program_memory_answers_the_address(tmp_path: Path) -> None:
    tst = """chip Echo
attach rom addr=addr out=instr
rom 0x000 0xD5 0b11110010
rom 0xFFF 7
set a 1
eval
expect data 0xF2
set a 0xFFF
eval
expect data 7
set a 2
eval
expect data 0
"""
    result = run(tmp_path, ECHO, tst)
    assert result.passed, (result.error, messages(result))
    assert result.checks == 3


def test_byte_fetched_this_cycle_is_what_the_tick_latches(tmp_path: Path) -> None:
    # Without settling before the tick, the DFF would latch the byte of the old address.
    tst = """chip Fetch
attach rom addr=addr out=instr
rom 0 0 1
set a 0
eval
set a 1
tick
tock
expect q 1
set a 0
tick
tock
expect q 0
"""
    result = run(tmp_path, FETCH, tst)
    assert result.passed, (result.error, messages(result))


def test_program_file_is_loaded_relative_to_the_script(tmp_path: Path) -> None:
    (tmp_path / "progs").mkdir()
    (tmp_path / "progs" / "p.rom").write_text("0000 0001\n0000 0010 // two\n")
    tst = (
        "chip Echo\nattach rom addr=addr out=instr\nrom progs/p.rom\nset a 1\neval\nexpect data 2\n"
    )
    result = run(tmp_path, ECHO, tst)
    assert result.passed, (result.error, messages(result))


def test_program_file_errors_point_into_the_file(tmp_path: Path) -> None:
    (tmp_path / "p.rom").write_text("1111\n")
    result = run(tmp_path, ECHO, "chip Echo\nattach rom addr=addr out=instr\nrom p.rom\n")
    assert (
        str(result.error)
        == f"{tmp_path / 'p.rom'}:1:1: error: a byte has 8 binary digits, this line has 4"
    )
    result = run(tmp_path, ECHO, "chip Echo\nattach rom addr=addr out=instr\nrom q.rom\n")
    assert str(result.error).startswith(
        f"{tmp_path / 'Echo.tst'}:3:1: error: can't read program file 'q.rom'"
    )


def test_bytes_past_the_end_are_an_error(tmp_path: Path) -> None:
    result = run(tmp_path, ECHO, "chip Echo\nattach rom addr=addr out=instr\nrom 0xFFF 1 2\n")
    assert str(result.error).endswith(
        ":3:1: error: 2 bytes from 0xFFF run past the end of program memory (0xFFF)"
    )


def test_a_driven_pin_cannot_be_set(tmp_path: Path) -> None:
    result = run(tmp_path, ECHO, "chip Echo\nattach rom addr=addr out=instr\nset instr 3\n")
    assert str(result.error).endswith(
        ":3:1: error: 'instr' is driven by the program memory: it can't be set"
    )


@pytest.mark.parametrize(
    ("links", "at", "message"),
    [
        ("addr=a out=instr", "2:12", "addr reads 'a', which is an input of Echo: it must be"
         " an output"),
        ("addr=addr out=data", "2:22", "out drives 'data', which is an output of Echo: it must"
         " be an input"),
        ("addr=nope out=instr", "2:12", "addr reads 'nope', which is not a pin of Echo: it must"
         " be an output"),
        ("addr=addr out=a", "2:22", "out has 8 bits, 'a' has 12"),
    ],
)  # fmt: skip
def test_attach_checks_the_chip_pins(tmp_path: Path, links: str, at: str, message: str) -> None:
    result = run(tmp_path, ECHO, f"chip Echo\nattach rom {links}\n")
    want = f"{tmp_path / 'Echo.tst'}:{at}: error: the program memory's {message}"
    assert str(result.error) == want


def test_data_memory_width_is_checked(tmp_path: Path) -> None:
    hdl = PORT.replace("ramin[4]", "ramin[8]").replace(
        "ramin = i;", "ramin[0..3] = i;\n ramin[4..7] = i;"
    )
    result = run(tmp_path, hdl, f"chip Port\n{ATTACH_RAM}\n")
    assert str(result.error).endswith(
        ":2:12: error: the data memory's in has 4 bits, 'ramin' has 8"
    )


def test_an_address_that_never_settles_is_an_error(tmp_path: Path) -> None:
    tst = "chip Loop\nattach rom addr=addr out=instr\nrom 0 0 1\nset go 0\neval\nset go 1\neval\n"
    result = run(tmp_path, LOOP, tst)
    assert str(result.error).endswith(
        ":7:1: error: the memories and Loop never settled: after 8 passes, "
        "addr still changed with what the memory sent back"
    )


# ---- the data memory ------------------------------------------------------


def test_data_memory_writes_at_the_clock_like_a_dff(tmp_path: Path) -> None:
    tst = f"""chip Port
{ATTACH_RAM}
ram 2 0x35 9
set b 2
set a 0x35
set s 0
set l 0
set i 4
eval
expect r 9
set l 1
tick
expect r 9
expect ram 2 0x35 9
tock
expect r 4
expect ram 2 0x35 4
expect ram 1 0x35 *
"""
    result = run(tmp_path, PORT, tst)
    assert result.passed, (result.error, messages(result))
    assert result.checks == 6


def test_status_characters_are_separate_and_ignore_addr_2_3(tmp_path: Path) -> None:
    tst = f"""chip Port
{ATTACH_RAM}
ram 0 0x21 5
set b 0
set a 0x2D
set s 1
set l 1
set i 6
tick
tock
expect ramstatus 0 0x21 6
expect ram 0 0x21 5
expect ram 0 0x2D 5
"""
    result = run(tmp_path, PORT, tst)
    assert messages(result) == [
        f"{tmp_path / 'Port.tst'}:13:1: ram 0 0x2D: expected 5, got undefined (cycle 1)"
    ]


def test_undefined_load_writes_nothing_and_undefined_address_fails(tmp_path: Path) -> None:
    tst = f"""chip Port
{ATTACH_RAM}
ram 0 0 1
set i 2
set b 0
set s 0
set a 0
tick
tock
expect ram 0 0 1
set l 1
set a 0
tick
tock
expect ram 0 0 2
"""
    result = run(tmp_path, PORT, tst)
    assert result.passed, (result.error, messages(result))
    bad = tst.replace("set b 0\n", "")
    result = run(tmp_path, PORT, bad)
    assert messages(result) == [
        f"{tmp_path / 'Port.tst'}:12:1: data memory: ramload is 1 but bank is undefined, "
        "so nothing was written (cycle 1)",
        f"{tmp_path / 'Port.tst'}:14:1: ram 0 0: expected 2, got 1 (cycle 2)",
    ]
