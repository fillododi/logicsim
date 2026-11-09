"""The 4004 model in tools/ against the levels' own tests and Intel's manual.

The ALU and Cond tests were generated from separate models, so running every row of them
through the 4004 model checks both sides. Intel's 16-digit decimal addition routine
(MCS-4 manual, section IV B) runs from its source lines.
"""

from __future__ import annotations

import random
from pathlib import Path
from types import ModuleType

import pytest
from test_tools import load_tool

ROOT = Path(__file__).resolve().parent.parent
m4: ModuleType = load_tool("model4004")


def machine(source: str, **regs: int) -> object:
    m = m4.Mcs4(rom=m4.assemble(source))
    m.reset()
    for name, value in regs.items():
        setattr(m, name, value)
    return m


def table_rows(path: Path) -> list[list[int]]:
    rows = []
    for line in path.read_text().splitlines():
        line = line.split("//", 1)[0]
        if "|" in line and not line.strip().startswith("table"):
            rows.append([int(v, 0) for v in line.replace("|", " ").split()])
    return rows


# ---- against the levels -----------------------------------------------------


def test_every_alu_row_matches_the_instruction() -> None:
    rows = table_rows(ROOT / "chips" / "03_arith" / "ALU.tst")
    assert len(rows) == 1952  # 5,856 checks, three per row
    for a, b, cin, op, out, cout, _ in rows:
        if op <= 12:
            byte = 0xF0 | op
        else:
            byte = {13: 0xA0, 14: 0x80, 15: 0x90}[op]  # LD, ADD, SUB with R0
        m = m4.Mcs4()
        m.rom[0] = byte
        m.reset()
        m.acc, m.cy, m.regs[0] = a, cin, b
        m.step()
        assert (m.acc, m.cy) == (out, cout), f"op {op} a={a} b={b} cin={cin}"


def test_every_cond_row_matches_jcn() -> None:
    rows = table_rows(ROOT / "chips" / "05_cpu" / "Cond.tst")
    assert len(rows) == 1024
    for cond, acc, carry, test, jump in rows:
        m = machine(f"JCN {cond} target\nNOP\nNOP\ntarget: NOP")
        m.acc, m.cy, m.test = acc, carry, test
        m.step()
        assert m.pc == (4 if jump else 2), f"cond={cond:04b} acc={acc} cy={carry} test={test}"


# ---- Intel's 16-digit decimal addition --------------------------------------

DECIMAL_ADDITION = """
; Intel MCS-4 manual, section IV B: 16-digit decimal addition. Adds RAM register 3 of
; chip 0 to register 0, digit by digit from character 0 (the lowest), with DAA.
ADDIN:  FIM P0 0        ; IR(0-1) = 0: RAM chip 0, register 0, character 0
        FIM P2 48       ; IR(4) = 3, IR(5) = 0: register 3
        LDM 0
        XCH R6          ; IR(6) = 0, the digit counter
        CLC
ADI:    SRC P2
        RDM             ; a digit of the addend
        SRC P0
        ADM             ; plus the augend's digit and the carry
        DAA
        WRM             ; back into register 0
        INC R1
        INC R5
        ISZ R6 ADI      ; 16 digits
done:   JUN done
"""


def digits(n: int) -> list[int]:
    return [n // 10**k % 10 for k in range(16)]


@pytest.mark.parametrize("seed", range(5))
def test_intels_decimal_addition_routine(seed: int) -> None:
    rng = random.Random(seed)
    x, y = rng.randrange(10**16), rng.randrange(10**16)
    if seed == 0:
        x, y = 10**16 - 1, 1  # every digit carries, and the sum overflows
    m = machine(DECIMAL_ADDITION)
    for k, (dx, dy) in enumerate(zip(digits(x), digits(y), strict=True)):
        m.main[(0, k)] = dx  # register 0, the augend and the result
        m.main[(0, 0x30 | k)] = dy  # register 3, the addend
    took = m.run()
    total = x + y
    assert [m.main[(0, k)] for k in range(16)] == digits(total % 10**16)
    assert m.cy == int(total >= 10**16)
    assert took == 2 + 2 + 1 + 1 + 1 + 16 * (8 + 2)  # FIM FIM LDM XCH CLC, 16 loops


# ---- control flow -----------------------------------------------------------


def test_jms_bbl_and_a_fourth_call_loses_the_deepest_return() -> None:
    src = """
        JMS one
        LDM 0
        JUN end
    one: JMS two
        BBL 1
    two: JMS three
        BBL 2
    three: JMS four
        BBL 3
    four: BBL 4
    end: JUN end
    """
    m = machine(src)
    for _ in range(5):  # four calls, then BBL 4 back into three's return
        m.step()
    assert m.acc == 4 and m.sp == 3
    m.step()  # BBL 3 returns into two
    m.step()  # BBL 2 returns into one
    assert m.acc == 2
    m.step()  # BBL 1 would return after the first call, but the fourth call reused its level
    # The level holds the PC as `four` left it: the address after `BBL 4`, not 0x002.
    assert m.acc == 1 and m.pc == 0x00F


def test_jcn_isz_jin_and_fin_use_the_page_of_the_next_instruction() -> None:
    m = machine("org 0x0FE\nJCN 8 0x105")  # at 254-255: the target is on page 1
    m.pc = 0x0FE
    m.step()
    assert m.pc == 0x105
    m = machine("org 0x0FF\nJIN P1")  # at 255: the next page
    m.pc, m.regs[2], m.regs[3] = 0x0FF, 0x3, 0x4
    m.step()
    assert m.pc == 0x134
    m = machine("org 0x0FF\nFIN P1\norg 0x112\nbyte 0xAB")
    m.pc, m.regs[0], m.regs[1] = 0x0FF, 1, 2
    assert m.step() == 2  # one word, two instruction cycles
    assert m.pair(1) == 0xAB and m.pc == 0x100


def test_isz_counts_and_skips_at_zero() -> None:
    m = machine("LDM 13\nXCH R2\nloop: ISZ R2 loop\nend: JUN end")
    m.run()
    assert m.regs[2] == 0 and m.cycles == 2 + 2 * 3


# ---- RAM, banks and ports ---------------------------------------------------


def test_dcl_src_and_each_bank_keep_their_own_address() -> None:
    src = """
        FIM P0 0x12
        SRC P0          ; bank 0
        LDM 5
        DCL
        FIM P0 0x47
        SRC P0          ; bank 5
        LDM 3
        WRM
        WR2
        CLB
        DCL
        LDM 4
        WRM             ; bank 0 still at 0x12
        WMP
    end: JUN end
    """
    m = machine(src)
    m.run()
    assert m.main == {(5, 0x47): 3, (0, 0x12): 4}
    assert m.status == {(5, 0x4, 2): 3}
    assert m.ramport[(0, 0)] == 4


def test_rom_ports_and_kbp() -> None:
    m = machine("FIM P0 0xC0\nSRC P0\nRDR\nKBP\nWRR\nend: JUN end")
    m.romport_in[12] = 0b0100
    m.run()
    assert m.romport_out[12] == 3 and m.acc == 3


def test_reading_unwritten_ram_is_an_error() -> None:
    m = machine("FIM P0 0\nSRC P0\nRDM\nend: JUN end")
    with pytest.raises(m4.ModelError, match="never written"):
        m.run()


# ---- the assembler ----------------------------------------------------------


def test_assembler_encodings() -> None:
    rom = m4.assemble("FIM P3 0x9A\nJUN 0x123\nISZ R5 0x00\nSRC P7\nJCN 0b1010 0\nBBL 7")
    assert rom[:12] == [0x26, 0x9A, 0x41, 0x23, 0x75, 0x00, 0x2F, 0x1A, 0x00, 0xC7, 0, 0]


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("org 0xFE\nJCN 4 0x020", "line 2: target 0x020 is not on page 1"),
        ("ADD R16", "line 1: 'R16' is not a register 0-15"),
        ("FIM P0", "line 1: FIM takes 2 operands"),
        ("JUN nowhere", "line 1: 'nowhere' is not a number or a label"),
        ("MOV R1", "line 1: unknown instruction 'MOV'"),
    ],
)
def test_assembler_errors(src: str, message: str) -> None:
    with pytest.raises(m4.AsmError, match=message):
        m4.assemble(src)


def test_reset_clears_the_index_registers_as_the_chip_does() -> None:
    m = machine("INC R3\nLD R9\nend: JUN end")
    m.run()
    assert m.regs[3] == 1 and m.acc == 0 and m.regs.count(0) == 15


def test_registers_are_undefined_before_the_first_reset() -> None:
    m = m4.Mcs4(rom=m4.assemble("INC R3\nend: JUN end"))  # no reset: power-on state
    with pytest.raises(m4.ModelError, match="R3 is read at 0x001 before anything was written"):
        m.run()
    m = m4.Mcs4(rom=m4.assemble("XCH R3\nXCH R3\nCLC\nend: JUN end"))
    m.run()  # moving an undefined value is fine
    m = m4.Mcs4(rom=m4.assemble("XCH R3\nIAC\nend: JUN end"))
    with pytest.raises(m4.ModelError, match="A is used"):
        m.run()  # using it isn't


def test_assembler_refuses_overlapping_code() -> None:
    with pytest.raises(m4.AsmError, match="line 3: 0x001 already holds line 1's code"):
        m4.assemble("JUN 0x123\norg 1\nNOP")
