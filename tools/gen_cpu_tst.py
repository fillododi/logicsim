"""Generate the CPU level's .tst (chips/05_cpu/CPU.tst) from the 4004 model.

A development script, not part of the game. Run it after changing the test program:

    uv run python tools/gen_cpu_tst.py chips/05_cpu

One program covers all 46 instructions in segments, each starting on its own ROM page so
that JCN and ISZ targets stay in their page. Each result goes into RAM through `put`,
and after each segment the test checks every RAM character and port the segment changed,
with the instruction cycles counted by tools/model4004.py. The last segment is Intel's
16-digit decimal addition routine (MCS-4 manual, section IV B). `tests/test_tools.py`
checks that the committed file matches this script.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model4004 as m4  # noqa: E402

ATTACH = "attach mcs4 din=din dout=dout drive=drive sync=sync cmrom=cmrom cmram=cmram reset=reset"
RESET_CLOCKS = 64  # 8 instruction cycles, as the 4004 asks
X = 10**16 - 1 - 4004  # the decimal routine's operands: their sum carries out of 16 digits
Y = 4004 + 1957


@dataclass
class Segment:
    name: str
    source: str
    test: int = 0  # the TEST pin while the segment runs


ACC_CASES = [
    ("CLB", 5, 1), ("CLC", 5, 1), ("IAC", 14, 0), ("IAC", 15, 0), ("CMC", 6, 0),
    ("CMC", 6, 1), ("CMA", 5, 1), ("RAL", 9, 1), ("RAL", 9, 0), ("RAR", 9, 1),
    ("RAR", 6, 0), ("TCC", 3, 1), ("DAC", 0, 0), ("DAC", 5, 1), ("TCS", 4, 0),
    ("TCS", 4, 1), ("STC", 2, 0), ("DAA", 7, 1), ("DAA", 12, 0), ("DAA", 3, 0),
    ("DAA", 9, 0), ("KBP", 4, 0), ("KBP", 6, 0), ("KBP", 0, 1), ("KBP", 8, 0),
    ("NOP", 11, 1),
]  # fmt: skip


def acc_tests(cases: list[tuple[str, int, int]]) -> str:
    """Each accumulator instruction from a set A and CY; A then CY are stored."""
    lines = []
    for op, a, cy in cases:
        lines += [f"LDM {a}", "STC" if cy else "CLC", op, "JMS put", "TCC", "JMS put"]
    return "\n".join(lines)


def jcn_tests(conditions: list[tuple[int, str, int, int]]) -> str:
    """JCN with each condition from a set A and CY: stores 2 if it jumped, 1 if not."""
    lines = []
    for i, (cond, _, a, cy) in enumerate(conditions):
        lines += [
            f"LDM {a}", "STC" if cy else "CLC", f"JCN {cond} j{i}",
            "LDM 1", f"JUN k{i}", f"j{i}: LDM 2", f"k{i}: JMS put",
        ]  # fmt: skip
    return "\n".join(lines)


JCN_FLAGS = [
    (0, "never", 0, 0), (8, "always", 5, 1), (4, "A = 0", 0, 0), (4, "A = 0", 3, 0),
    (12, "A != 0", 0, 0), (12, "A != 0", 3, 0), (2, "CY = 1", 1, 1), (2, "CY = 1", 1, 0),
    (10, "CY = 0", 1, 1), (10, "CY = 0", 1, 0), (6, "A = 0 or CY", 7, 1),
    (6, "A = 0 or CY", 7, 0), (14, "A != 0 and CY = 0", 7, 0),
]  # fmt: skip
JCN_TEST = [(1, "TEST = 0", 4, 0), (9, "TEST = 1", 4, 0), (5, "A = 0 or TEST = 0", 4, 0)]

SEGMENTS = [
    Segment(
        "accumulator group",
        f"""
        org 0x000
        FIM P7 0x40     ; results go to RAM chip 1, register 0, character 0 on
        JMS put         ; A after reset
        TCC
        JMS put         ; CY after reset
        LD R4
        JMS put         ; an index register after reset
        FIN P4          ; P0 after reset: fetches the byte at 0x000 into P4
        LD R9
        JMS put         ; the odd register of the pair FIN wrote
        {acc_tests(ACC_CASES[:13])}
        JUN acc2
put:    SRC P7          ; store A at the next result character
        WRM
        ISZ R15 putend
        INC R14         ; past character 15: the next register
putend: BBL 0
""",
    ),
    Segment(
        "accumulator group, part 2",
        f"""
        org 0x100
acc2:   {acc_tests(ACC_CASES[13:])}
        JUN regs
""",
    ),
    Segment(
        "registers, ADD, SUB, ISZ",
        """
        org 0x200
regs:   FIM P0 0x3C     ; R0 = 3, R1 = 12
        LD R0
        JMS put
        LD R1
        JMS put
        FIM P1 0x00
        LDM 9
        XCH R2          ; R2 = 9, A = 0
        JMS put
        LD R2
        JMS put
        INC R2
        LD R2
        JMS put
        LDM 7
        CLC
        ADD R0
        JMS put
        TCC
        JMS put
        LDM 15
        STC
        ADD R1
        JMS put
        TCC
        JMS put
        LDM 7
        CLC
        SUB R0          ; no borrow in
        JMS put
        TCC
        JMS put
        LDM 7
        STC
        SUB R0          ; a borrow in
        JMS put
        TCC
        JMS put
        LDM 2
        CLC
        SUB R1          ; 2 - 12 borrows
        JMS put
        TCC
        JMS put
        FIM P1 0x0D     ; R2 = 0, R3 = 13
loop:   INC R2
        ISZ R3 loop     ; three rounds
        LD R2
        JMS put
        LD R3
        JMS put
        JUN flags
""",
    ),
    Segment(
        "JCN on A and CY",
        f"""
        org 0x300
flags:  {jcn_tests(JCN_FLAGS)}
        JUN tests
""",
    ),
    Segment(
        "JCN on TEST at 0",
        f"""
        org 0x400
tests:  {jcn_tests(JCN_TEST).replace("j", "t").replace("k", "u")}
        JUN testhi
""",
    ),
    Segment(
        "JCN on TEST at 1",
        f"""
        org 0x480
testhi: {jcn_tests(JCN_TEST).replace("j", "v").replace("k", "w")}
        JUN calls
""",
        test=1,
    ),
    Segment(
        "JMS and BBL, three deep",
        """
        org 0x500
calls:  JMS one
        JMS put         ; 6, from one's BBL
        JUN tables
one:    JMS two
        JMS put         ; 5, from two's BBL
        BBL 6
two:    LDM 4
        JMS put         ; the third level
        BBL 5
""",
    ),
    Segment(
        "FIN and JIN, and a FIN at the end of a page",
        """
        org 0x600
tables: FIM P0 0xF2
        FIN P1          ; the byte at 0x6F2
        LD R2
        JMS put
        LD R3
        JMS put
        FIM P1 jin1
        JIN P1          ; to jin1, in this page
        LDM 1
        JMS put
jin1:   LDM 2
        JMS put
        FIM P0 0x07
        JUN edge
        org 0x6F2
        byte 0xA5
        org 0x6FF
edge:   FIN P1          ; at 0x6FF: the byte comes from page 7, at 0x707
        LD R2
        JMS put
        LD R3
        JMS put
        JUN io
        byte 0x3C       ; 0x707
""",
    ),
    Segment(
        "DCL, SRC in two banks, RAM and port instructions",
        """
        org 0x800
io:     FIM P0 0x25     ; bank 0: chip 0, register 2, character 5
        SRC P0
        LDM 6
        DCL             ; bank 6
        FIM P1 0xC3     ; bank 6: chip 3, register 0, character 3
        SRC P1
        LDM 9
        WRM
        WR0
        LDM 4
        WR3
        LDM 11
        WMP             ; bank 6, chip 3's port
        LDM 7
        WPM             ; nothing to write to: the bus still sends A
        LDM 2
        CLC
        ADM             ; 2 + 9
        WR1
        RD0
        STC
        SBM             ; 9 - 9 with a borrow in
        WR2
        RDM
        RD3
        CLB
        DCL             ; back to bank 0, still at 0x25
        LDM 13
        WRM
        SRC P0          ; 0x25 again: 4001 #2 for the ROM port
        LDM 5
        WRR
        RDR             ; 4001 #2's input lines
        WMP             ; bank 0, chip 0's port
        RDM
        JMS put
        SRC P1          ; bank 0, chip 3 now
        LDM 1
        WMP
        JUN decimal
""",
    ),
    Segment(
        "Intel's 16-digit decimal addition",
        """
        org 0x900
decimal: FIM P0 0       ; Intel MCS-4 manual, section IV B
        FIM P2 48
        LDM 0
        XCH R6
        CLC
ADI:    SRC P2
        RDM
        SRC P0
        ADM
        DAA
        WRM
        INC R1
        INC R5
        ISZ R6 ADI
        TCC             ; the carry out of the 16 digits
        JMS put
halt:   JUN halt
""",
    ),
]


def digits(n: int) -> list[int]:
    return [n // 10**k % 10 for k in range(16)]


def program() -> str:
    """The segments, with `JMS put` inlined except where the calls themselves are tested.

    Inline, a store takes 4 instruction cycles (SRC, WRM, ISZ) instead of 7, which keeps the
    test quick; the JMS and BBL segment still stores through `put`, three calls deep.
    """
    parts, n = [], 0
    for seg in SEGMENTS:
        if seg.name.startswith("JMS"):
            parts.append(seg.source)
            continue
        pieces = seg.source.split("JMS put")
        text = pieces[0]
        for piece in pieces[1:]:
            text += f"SRC P7\nWRM\nISZ R15 st{n}\nINC R14\nst{n}:" + piece
            n += 1
        parts.append(text)
    return "\n".join(parts)


def generate() -> str:
    rom, labels = m4.assemble_labels(program())
    # Each segment ends where the next one starts; the last at the halt.
    names = ["acc2", "regs", "flags", "tests", "testhi", "calls", "tables", "io", "decimal", "halt"]
    starts = [labels[n] for n in names]
    m = m4.Mcs4(rom=rom)
    m.romport_in[2] = 0b1010
    for k, (dx, dy) in enumerate(zip(digits(X), digits(Y), strict=True)):
        m.main[(0, k)] = dx
        m.main[(0, 0x30 | k)] = dy
    preset = dict(m.main)
    m.reset()

    out = [
        "// CPU: the 4004 runs one program that uses all 46 instructions, then Intel's 16-digit",
        "// decimal addition. Each segment stores its results in RAM (chip 1 of bank 0) and the",
        "// test checks them after the segment's last instruction cycle (8 clocks each).",
        "// Generated by tools/gen_cpu_tst.py from tools/model4004.py: don't edit by hand.",
        "chip CPU",
        ATTACH,
    ]
    for start in range(0, m4.ROM_SIZE, 16):
        chunk = rom[start : start + 16]
        if any(chunk):
            out.append(f"rom 0x{start:03X} " + " ".join(f"0x{b:02X}" for b in chunk))
    out.append("set romport 2 0b1010")
    out.append("// The decimal routine's operands: register 0 + register 3 of chip 0.")
    for (bank, addr), v in sorted(preset.items()):
        out.append(f"ram {bank} 0x{addr:02X} {v}")
    out += ["set test 0", "set reset 1", f"cycles {RESET_CLOCKS}", "set reset 0"]

    before_main, before_status = dict(m.main), dict(m.status)
    before_ports = (dict(m.romport_out), dict(m.ramport))
    for seg, end in zip(SEGMENTS, starts, strict=True):
        m.test = seg.test
        out.append(f"// ---- {seg.name}")
        out.append(f"set test {seg.test}")
        took = 0
        while m.pc != end:
            took += m.step()
            if took > 1000:
                raise SystemExit(f"segment '{seg.name}' never reaches 0x{end:03X}")
        out.append(f"cycles {8 * took}")
        for (bank, addr), v in sorted(m.main.items()):
            if before_main.get((bank, addr)) != v:
                out.append(f"expect ram {bank} 0x{addr:02X} {v}")
        for (bank, reg, idx), v in sorted(m.status.items()):
            if before_status.get((bank, reg, idx)) != v:
                out.append(f"expect ramstatus {bank} 0x{reg << 4 | idx:02X} {v}")
        for chip, v in sorted(m.romport_out.items()):
            if before_ports[0].get(chip) != v:
                out.append(f"expect romport {chip} {v}")
        for (bank, chip), v in sorted(m.ramport.items()):
            if before_ports[1].get((bank, chip)) != v:
                out.append(f"expect ramport {bank} {chip} {v}")
        before_main, before_status = dict(m.main), dict(m.status)
        before_ports = (dict(m.romport_out), dict(m.ramport))
    assert [m.main[(0, k)] for k in range(16)] == digits((X + Y) % 10**16)
    out.append("// ---- halted: a few more cycles change nothing")
    out.append("cycles 16")
    out.append(f"expect ram 0 0x0F {digits((X + Y) % 10**16)[15]}")
    return "\n".join(out) + "\n"


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("chips/05_cpu")
    (out / "CPU.tst").write_text(generate())


if __name__ == "__main__":
    main()
