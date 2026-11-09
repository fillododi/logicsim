"""The MCS-4 memories a `.tst` script puts on a 4004's bus, and the `.rom` format.

A pass-through chip, `Bus`, stands in for the CPU: the script sets on its inputs what a
4004 would put on its pins in each clock period, and reads back on `seen` what the
memories send on `din`. `Cycle` writes those 8 periods for one instruction cycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from nandsim.hdl import HdlError
from nandsim.netlist import ChipLibrary
from nandsim.testing import TstResult, parse_rom, parse_tst, run_script
from nandsim.testing.memory import BUS_PINS, decode_bank
from nandsim.testing.tst import MCS4_PINS

BUS = """CHIP Bus {
    IN din[4], d[4], dr, sy, cr, cm[4], reset;
    OUT dout[4], drive, sync, cmrom, cmram[4], seen[4];
    PARTS:
    dout = d;
    drive = dr;
    sync = sy;
    cmrom = cr;
    cmram = cm;
    seen = din;
}"""

ATTACH = "attach mcs4 din=din dout=dout drive=drive sync=sync cmrom=cmrom cmram=cmram reset=reset"


@dataclass
class Script:
    """A `.tst` for `Bus`, written one clock period at a time."""

    lines: list[str] = field(default_factory=lambda: ["chip Bus", ATTACH])

    def add(self, *lines: str) -> Script:
        self.lines += lines
        return self

    def period(self, d: int = 0, dr: int = 0, sy: int = 0, cr: int = 0, cm: int = 0,
               seen: int | str | None = None) -> None:  # fmt: skip
        self.lines += [f"set d {d}", f"set dr {dr}", f"set sy {sy}", f"set cr {cr}"]
        self.lines.append(f"set cm {cm}")
        if seen is not None:
            self.lines += ["eval", f"expect seen {seen}"]
        self.lines += ["tick", "tock"]

    def reset(self) -> Script:
        self.lines.append("set reset 1")
        self.period()
        self.lines.append("set reset 0")
        return self

    def cycle(
        self,
        addr: int,
        op: tuple[int, int] | None = None,
        io: int = 0,
        x2: tuple[int, int, int, int] = (0, 0, 0, 0),
        x3: tuple[int, int] = (0, 0),
        seen_x2: int | str | None = None,
    ) -> Script:
        """One instruction cycle fetching from `addr`, as a correct 4004 would drive it.

        `op` is the (OPR, OPA) the memories should send at M1 and M2. `io` is the CM-RAM
        lines at M2 (CM-ROM goes with any of them). `x2` is (d, dr, cr, cm) at X2 and `x3`
        is (d, dr) at X3.
        """
        self.period(addr & 15, 1)
        self.period(addr >> 4 & 15, 1)
        self.period(addr >> 8, 1, cr=1)
        self.period(seen=None if op is None else op[0])
        self.period(cr=1 if io else 0, cm=io, seen=None if op is None else op[1])
        self.period()
        d, dr, cr, cm = x2
        self.period(d, dr, cr=cr, cm=cm, seen=seen_x2)
        self.period(x3[0], x3[1], sy=1)
        return self

    def src(self, addr: int, pair: int, bank_lines: int = 1) -> Script:
        """SRC: the instruction at `addr`, then the pair's high nibble at X2, low at X3."""
        return self.cycle(addr, x2=(pair >> 4, 1, 1, bank_lines), x3=(pair & 15, 1))

    def io(self, addr: int, bank_lines: int = 1, write: int | None = None,
           seen_x2: int | str | None = None) -> Script:  # fmt: skip
        """An I/O or RAM instruction at `addr`: CM lines at M2, data at X2."""
        x2 = (0, 0, 0, 0) if write is None else (write, 1, 0, 0)
        return self.cycle(addr, io=bank_lines, x2=x2, seen_x2=seen_x2)

    @property
    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


def run(tmp_path: Path, tst: str, hdl: str = BUS) -> TstResult:
    name = hdl.split()[1]
    (tmp_path / f"{name}.hdl").write_text(hdl)
    (tmp_path / f"{name}.tst").write_text(tst)
    script = parse_tst(tst, str(tmp_path / f"{name}.tst"))
    return run_script(script, ChipLibrary([tmp_path]), None)


def messages(result: TstResult) -> list[str]:
    return [str(f).split(": ", 1)[1] for f in result.failures]


def passes(result: TstResult) -> bool:
    return result.passed or pytest.fail(f"{result.error} {messages(result)}")


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


NEED = "needs the MCS-4 memories: add 'attach mcs4 ...' before it"


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("rom 0 1", f"2:1: error: 'rom' {NEED}"),
        ("ram 0 0 1", f"2:1: error: 'ram' {NEED}"),
        ("expect ramstatus 0 0 1", f"2:1: error: 'expect' {NEED}"),
        ("set romport 0 1", f"2:1: error: 'set' {NEED}"),
        ("expect ramport 0 0 1", f"2:1: error: 'expect' {NEED}"),
        ("attach rom addr=a out=o", "2:1: error: usage: attach mcs4 din=<pin> dout=<pin> "
         "drive=<pin> sync=<pin> cmrom=<pin> cmram=<pin> reset=<pin>"),
        ("attach mcs4 din=din", "2:1: error: attach mcs4 must connect dout, drive, sync, "
         "cmrom, cmram, reset"),
        ("attach mcs4 data=d", "2:13: error: mcs4 has no signal 'data' (its signals: din, "
         "dout, drive, sync, cmrom, cmram, reset)"),
        ("attach mcs4 din=a din=b", "2:19: error: mcs4 din is connected twice"),
        ("attach mcs4 din", "2:13: error: expected <signal>=<chip pin>, found 'din'"),
        (f"{ATTACH}\n{ATTACH}", "3:1: error: the MCS-4 memories are already attached"),
        (f"{ATTACH}\nrom 5", "3:1: error: usage: rom <addr> <byte>... or rom <file>.rom"),
        (f"{ATTACH}\nram 0 1", "3:1: error: usage: ram <bank> <addr> <value>"),
        (f"{ATTACH}\nexpect ram 0 1", "3:1: error: usage: expect ram <bank> <addr> <value>"),
        (f"{ATTACH}\nexpect ramport 0 1", "3:1: error: usage: expect ramport <bank> <chip> "
         "<value>"),
        (f"{ATTACH}\nset romport 1 2 3", "3:1: error: usage: set romport <chip> <value>"),
    ],
)  # fmt: skip
def test_memory_command_errors(text: str, message: str) -> None:
    with pytest.raises(HdlError) as e:
        parse_tst(f"chip X\n{text}\n", "t.tst")
    assert str(e.value) == f"t.tst:{message}"


def test_pins_named_like_commands_still_work_with_two_arguments() -> None:
    script = parse_tst("chip X\nexpect ram 1\nset romport 2\nexpect ramport 3\n", "t.tst")
    assert [s.pin for s in script.steps] == ["ram", "romport", "ramport"]  # type: ignore[union-attr]


def test_parser_and_memories_agree_on_the_signals() -> None:
    assert tuple(BUS_PINS) == MCS4_PINS


@pytest.mark.parametrize(
    ("swap", "message"),
    [
        (("din=din", "din=seen"), "2:13: error: mcs4 din needs Bus's input, but 'seen' is an "
         "output of Bus"),
        (("dout=dout", "dout=d"), "2:21: error: mcs4 dout needs Bus's output, but 'd' is an "
         "input of Bus"),
        (("sync=sync", "sync=nope"), "2:43: error: mcs4 sync needs Bus's output, but 'nope' is "
         "not a pin of Bus"),
        (("drive=drive", "drive=seen"), "2:31: error: mcs4 drive has 1 bit, 'seen' has 4"),
    ],
)  # fmt: skip
def test_attach_checks_the_chip_pins(tmp_path: Path, swap: tuple[str, str], message: str) -> None:
    result = run(tmp_path, f"chip Bus\n{ATTACH.replace(*swap)}\n")
    assert str(result.error) == f"{tmp_path / 'Bus.tst'}:{message}"


def test_din_cannot_be_set(tmp_path: Path) -> None:
    result = run(tmp_path, f"chip Bus\n{ATTACH}\nset din 3\n")
    assert str(result.error).endswith(
        ":3:1: error: 'din' is driven by the MCS-4 memories: it can't be set"
    )


def test_bytes_past_the_end_are_an_error(tmp_path: Path) -> None:
    result = run(tmp_path, f"chip Bus\n{ATTACH}\nrom 0xFFF 1 2\n")
    assert str(result.error).endswith(
        ":3:1: error: 2 bytes from 0xFFF run past the end of program memory (0xFFF)"
    )


def test_program_files_load_relative_to_the_script(tmp_path: Path) -> None:
    (tmp_path / "progs").mkdir()
    (tmp_path / "progs" / "p.rom").write_text("0000 0001\n1101 0101 // LDM 5\n")
    s = Script().add("rom progs/p.rom").reset().cycle(1, op=(0xD, 5))
    assert passes(run(tmp_path, s.text))
    (tmp_path / "bad.rom").write_text("1111\n")
    result = run(tmp_path, f"chip Bus\n{ATTACH}\nrom bad.rom\n")
    assert str(result.error) == (
        f"{tmp_path / 'bad.rom'}:1:1: error: a byte has 8 binary digits, this line has 4"
    )
    result = run(tmp_path, f"chip Bus\n{ATTACH}\nrom none.rom\n")
    assert str(result.error).startswith(
        f"{tmp_path / 'Bus.tst'}:3:1: error: can't read program file 'none.rom'"
    )


# ---- the bus --------------------------------------------------------------


def test_cm_ram_lines_select_banks_as_dcl_does() -> None:
    assert [decode_bank(x) for x in (0, 1, 2, 4, 8, 6, 10, 12, 14)] == [
        None, 0, 1, 2, 4, 3, 5, 6, 7,
    ]  # fmt: skip
    with pytest.raises(ValueError, match="bank 0 and another"):
        decode_bank(3)


def test_the_4001_at_a3_sends_the_instruction_at_m1_and_m2(tmp_path: Path) -> None:
    s = Script().add("rom 0x123 0xD5", "rom 0xFFF 0x2E").reset()
    s.cycle(0x123, op=(0xD, 5)).cycle(0xFFF, op=(2, 0xE)).cycle(0x124, op=(0, 0))
    assert passes(run(tmp_path, s.text))


def test_nothing_is_sent_before_the_first_reset(tmp_path: Path) -> None:
    s = Script().add("rom 0 0xFF").cycle(0, op=(0, 0))
    assert passes(run(tmp_path, s.text))


def test_src_then_wrm_rdm_and_status_characters(tmp_path: Path) -> None:
    # SRC P0 = 0x35 picks 4002 #0, register 3, character 5 in bank 0.
    s = Script().add("rom 0 0x21 0xE0 0xE9 0xE6 0xEE", "ram 0 0x35 1").reset()
    s.src(0, 0x35)
    s.io(1, write=7)  # WRM
    s.io(2, seen_x2=7)  # RDM
    s.io(3, write=9)  # WR2
    s.io(4, seen_x2=9)  # RD2
    s.add("expect ram 0 0x35 7", "expect ramstatus 0 0x32 9", "expect ramstatus 0 0x36 9")
    s.add("expect ram 0 0x36 *", "expect ramstatus 0 0x31 *")
    result = run(tmp_path, s.text)
    assert passes(result)


def test_each_bank_keeps_its_own_src_selection(tmp_path: Path) -> None:
    # DCL 5 raises CM-RAM1 and CM-RAM3: bank 5. Bank 0 keeps the address it took earlier.
    s = Script().add("rom 0 0x21 0x21 0xE0 0xE0").reset()
    s.src(0, 0x12, bank_lines=1).src(1, 0x47, bank_lines=0b1010)
    s.io(2, bank_lines=0b1010, write=3).io(3, bank_lines=1, write=4)
    s.add("expect ram 5 0x47 3", "expect ram 0 0x12 4", "expect ram 0 0x47 *")
    assert passes(run(tmp_path, s.text))


def test_ports_wrr_rdr_and_wmp(tmp_path: Path) -> None:
    # SRC 0xC9: 4001 #12, and 4002 #3 (register 0) in bank 2. WRR, RDR, WMP.
    s = Script().add("rom 0 0x21 0xE2 0xEA 0xE1", "set romport 12 6").reset()
    s.src(0, 0xC9, bank_lines=0b100)
    s.io(1, bank_lines=0b100, write=0xA)
    s.io(2, bank_lines=0b100, seen_x2=6)
    s.io(3, bank_lines=0b100, write=0xB)
    s.add("expect romport 12 0xA", "expect romport 11 0", "expect ramport 2 3 0xB")
    s.add("expect ramport 2 2 0")
    assert passes(run(tmp_path, s.text))


def test_reset_clears_ports_and_selection_but_keeps_memory(tmp_path: Path) -> None:
    s = Script().add("rom 0 0x21 0xE1 0xE9").reset()
    s.src(0, 0x00).io(1, write=5).add("expect ramport 0 0 5")
    s.add("ram 0 0x00 8").reset().add("expect ramport 0 0 0", "expect ram 0 0 8")
    s.io(2, seen_x2=0)  # RDM: SRC's selection went with the reset
    assert messages(run(tmp_path, s.text)) == [
        "bus at X2: RDM at X2, but no 4002 was selected by SRC (cycle 24)"
    ]


def test_port_values_print_in_the_expected_base(tmp_path: Path) -> None:
    s = Script().add("rom 0 0x21 0xE2").reset().src(0, 0x00).io(1, write=5)
    s.add("expect romport 0 0b0110", "expect ram 0 0 0x3")
    assert messages(run(tmp_path, s.text)) == [
        "romport 0: expected 0b0110, got 0b0101 (cycle 17)",
        "ram 0 0: expected 0x3, got undefined (cycle 17)",
    ]


# ---- protocol problems ----------------------------------------------------


def broken(tmp_path: Path, script: Script) -> list[str]:
    return messages(run(tmp_path, script.text))


def test_sync_must_be_1_only_at_x3(tmp_path: Path) -> None:
    s = Script().reset()
    s.period(0, 1)
    s.period(0, 1, sy=1)
    assert broken(tmp_path, s) == [
        "bus at A2: sync is 1 at A2: it must be 1 only during X3 (cycle 2)"
    ]
    s = Script().reset().cycle(0)
    s.lines[-5] = "set sy 0"  # the cycle's last period, X3, without sync
    assert broken(tmp_path, s) == [
        "bus at X3: sync is 0 at X3: it must be 1 during X3, before each A1 (cycle 8)"
    ]


def test_only_the_first_bus_problem_is_reported(tmp_path: Path) -> None:
    s = Script().reset()
    for _ in range(3):
        s.period(0, 0)  # A1, A2, A3 without driving
    assert broken(tmp_path, s) == [
        "bus at A1: the CPU must send the address at A1, but drive is 0 (cycle 1)"
    ]


def test_driving_while_a_memory_sends_is_a_conflict(tmp_path: Path) -> None:
    s = Script().reset()
    s.period(0, 1)
    s.period(0, 1)
    s.period(0, 1, cr=1)
    s.period(0, 1)  # M1, where 4001 #0 sends
    assert broken(tmp_path, s) == ["bus at M1: drive is 1 while 4001 #0 sends on the bus (cycle 4)"]


def test_dout_must_be_0_when_not_driving(tmp_path: Path) -> None:
    s = Script().reset()
    s.period(1, 1)
    s.period(0, 1)
    s.period(0, 1)
    s.period(0, 0)
    s.period(0, 0)
    s.period(4, 0)  # X1
    assert broken(tmp_path, s) == [
        "bus at X1: dout is 4 while drive is 0: it must be 0 when the CPU isn't driving (cycle 6)"
    ]


def test_ram_writes_need_an_src_and_one_bank(tmp_path: Path) -> None:
    s = Script().add("rom 0 0xE0").reset().io(0, write=1)
    assert broken(tmp_path, s) == [
        "bus at X2: WRM at X2, but no 4002 was selected by SRC in bank 0 (cycle 7)"
    ]
    s = Script().add("rom 0 0xE0").reset().io(0, bank_lines=0b11, write=1)
    assert broken(tmp_path, s) == [
        "bus at M2: cmram selects bank 0 and another bank at once at M2 (cycle 5)"
    ]
