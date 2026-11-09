"""An instruction-level model of the Intel 4004 in an MCS-4 system, and a small assembler.

A development script, not part of the game: it computes what the CPU level's tests expect
(RAM contents, ports, registers) for 4004 programs. Every instruction follows Intel's
*MCS-4 Micro Computer Set* manual, section VII. The memories follow the runner's
`attach mcs4` (docs/tst.md): sixteen 4001s holding 4 KB of program, eight banks of four
4002s, SRC selections kept per bank, and a reset that keeps memory contents.

    uv run python tools/model4004.py program.asm      # assemble, run to the halt, print state

A program halts on a jump to itself (`here: JUN here`). The assembler takes one
instruction per line, `label:` prefixes, `;` or `//` comments, registers as `R0`-`R15`,
pairs as `P0`-`P7`, numbers in decimal, `0x` or `0b`, and the directives `org <addr>` and
`byte <value>...`.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field

ROM_SIZE = 4096


class ModelError(Exception):
    """A program did something the model refuses to guess about (reading unwritten RAM...)."""


# ---- the assembler ----------------------------------------------------------

# Instructions without operands: mnemonic -> byte.
SIMPLE = {
    "NOP": 0x00,
    **{m: 0xE0 | i for i, m in enumerate(
        "WRM WMP WRR WPM WR0 WR1 WR2 WR3 SBM RDM RDR ADM RD0 RD1 RD2 RD3".split())},
    **{m: 0xF0 | i for i, m in enumerate(
        "CLB CLC IAC CMC CMA RAL RAR TCC DAC TCS STC DAA KBP DCL".split())},
}  # fmt: skip
REGISTER_OPS = {"INC": 0x6, "ADD": 0x8, "SUB": 0x9, "LD": 0xA, "XCH": 0xB}  # OPR, OPA = Rn
DATA_OPS = {"BBL": 0xC, "LDM": 0xD}  # OPR, OPA = 4-bit data
PAIR_OPS = {"SRC": 0x21, "FIN": 0x30, "JIN": 0x31}  # byte | pair << 1


class AsmError(Exception):
    pass


def _number(text: str, labels: dict[str, int] | None = None) -> int:
    t = text.strip()
    try:
        return int(t, 0)
    except ValueError:
        if labels is not None and t in labels:
            return labels[t]
        raise AsmError(
            f"'{t}' is not a number" + ("" if labels is None else " or a label")
        ) from None


def _reg(text: str, prefix: str, top: int) -> int:
    t = text.strip().upper()
    n = int(t[1:], 0) if t.startswith(prefix) else _number(t)
    if not 0 <= n <= top:
        raise AsmError(f"'{text}' is not a {'register' if prefix == 'R' else 'pair'} 0-{top}")
    return n


def _size(mnemonic: str, args: list[str]) -> int:
    if mnemonic == "BYTE":
        return len(args)
    return 2 if mnemonic in ("JCN", "FIM", "JUN", "JMS", "ISZ") else 1


def assemble(text: str) -> list[int]:
    """Assemble 4004 source into a 4 KB ROM image (unused bytes are 0, NOP)."""
    return assemble_labels(text)[0]


def assemble_labels(text: str) -> tuple[list[int], dict[str, int]]:
    """Assemble 4004 source: the ROM image and the address of each label."""
    lines: list[tuple[int, int, str, list[str]]] = []  # (line number, address, mnemonic, args)
    labels: dict[str, int] = {}
    addr = 0
    for lineno, raw in enumerate(text.splitlines(), start=1):
        code = raw.split(";", 1)[0].split("//", 1)[0].strip()
        while ":" in code:
            name, code = (s.strip() for s in code.split(":", 1))
            if name in labels:
                raise AsmError(f"line {lineno}: label '{name}' defined twice")
            labels[name] = addr
        if not code:
            continue
        mnemonic, _, rest = code.partition(" ")
        mnemonic = mnemonic.upper()
        args = [a for a in rest.replace(",", " ").split() if a]
        if mnemonic == "ORG":
            addr = _number(args[0])
            continue
        lines.append((lineno, addr, mnemonic, args))
        addr += _size(mnemonic, args)
    rom = [0] * ROM_SIZE
    written: dict[int, int] = {}  # address -> the line that put a byte there
    for lineno, at, mnemonic, args in lines:
        try:
            code = _encode(at, mnemonic, args, labels)
        except AsmError as e:
            raise AsmError(f"line {lineno}: {e}") from None
        if at + len(code) > ROM_SIZE:
            raise AsmError(f"line {lineno}: past the end of program memory")
        for a in range(at, at + len(code)):
            if a in written:
                raise AsmError(f"line {lineno}: 0x{a:03X} already holds line {written[a]}'s code")
            written[a] = lineno
        rom[at : at + len(code)] = code
    return rom, labels


def _page_target(at: int, size: int, target: int) -> int:
    """The low byte of a jump within the page of the next instruction, as JCN and ISZ do."""
    page = ((at + size) & 0xFFF) >> 8
    if target >> 8 != page:
        raise AsmError(f"target 0x{target:03X} is not on page {page} (the page after the jump)")
    return target & 0xFF


def _encode(at: int, m: str, args: list[str], labels: dict[str, int]) -> list[int]:
    def want(n: int) -> None:
        if len(args) != n:
            raise AsmError(f"{m} takes {n} operand{'s' if n != 1 else ''}")

    if m == "BYTE":
        return [_number(a, labels) & 0xFF for a in args]
    if m in SIMPLE:
        want(0)
        return [SIMPLE[m]]
    if m in REGISTER_OPS:
        want(1)
        return [REGISTER_OPS[m] << 4 | _reg(args[0], "R", 15)]
    if m in DATA_OPS:
        want(1)
        return [DATA_OPS[m] << 4 | (_number(args[0], labels) & 15)]
    if m in PAIR_OPS:
        want(1)
        return [PAIR_OPS[m] | _reg(args[0], "P", 7) << 1]
    if m == "FIM":
        want(2)
        return [0x20 | _reg(args[0], "P", 7) << 1, _number(args[1], labels) & 0xFF]
    if m in ("JUN", "JMS"):
        want(1)
        target = _number(args[0], labels) & 0xFFF
        return [(0x40 if m == "JUN" else 0x50) | target >> 8, target & 0xFF]
    if m == "JCN":
        want(2)
        cond = _number(args[0], labels) & 15
        return [0x10 | cond, _page_target(at, 2, _number(args[1], labels))]
    if m == "ISZ":
        want(2)
        return [0x70 | _reg(args[0], "R", 15), _page_target(at, 2, _number(args[1], labels))]
    raise AsmError(f"unknown instruction '{m}'")


# ---- the machine ------------------------------------------------------------

KBP = {0: 0, 1: 1, 2: 2, 4: 3, 8: 4}  # the manual's table; anything else gives 15


@dataclass
class Mcs4:
    """A 4004 with its 4001 ROMs and 4002 RAMs. RAM keys are the runner's: main characters
    by (bank, SRC address), status characters by (bank, SRC address >> 4, index)."""

    rom: list[int] = field(default_factory=lambda: [0] * ROM_SIZE)
    main: dict[tuple[int, int], int] = field(default_factory=dict)
    status: dict[tuple[int, int, int], int] = field(default_factory=dict)
    romport_in: dict[int, int] = field(default_factory=dict)  # what RDR reads, per 4001
    romport_out: dict[int, int] = field(default_factory=dict)  # what WRR wrote
    ramport: dict[tuple[int, int], int] = field(default_factory=dict)  # (bank, 4002) WMP
    test: int = 0  # the TEST pin
    # The CPU.
    acc: int | None = 0  # None: undefined, as after XCH with an unwritten register
    cy: int = 0
    regs: list[int | None] = field(default_factory=lambda: [None] * 16)
    stack: list[int] = field(default_factory=lambda: [0] * 4)  # the PC is stack[sp]
    sp: int = 0
    bank: int = 0  # DCL's command register
    src_rom: int | None = None
    src_ram: dict[int, int] = field(default_factory=dict)  # bank -> SRC address
    cycles: int = 0  # instruction cycles since reset

    @property
    def pc(self) -> int:
        return self.stack[self.sp]

    @pc.setter
    def pc(self, value: int) -> None:
        self.stack[self.sp] = value & 0xFFF

    def reset(self) -> None:
        """RESET: A, CY, the index registers, the stack, DCL and SRC selections cleared;
        ports to 0; memory kept. Before the first reset the registers are undefined, as at
        power-on in the simulator, and the model refuses to read them.
        """
        self.acc, self.cy, self.sp, self.bank, self.cycles = 0, 0, 0, 0, 0
        self.regs, self.stack = [0] * 16, [0] * 4
        self.src_rom, self.src_ram = None, {}
        self.romport_out = dict.fromkeys(range(16), 0)
        self.ramport = {(b, c): 0 for b in range(8) for c in range(4)}

    def _r(self, n: int) -> int:
        value = self.regs[n]
        if value is None:
            raise ModelError(f"R{n} is read at 0x{self.pc:03X} before anything was written to it")
        return value

    def _acc(self) -> int:
        if self.acc is None:
            raise ModelError(
                f"A is used at 0x{self.pc:03X} while undefined (XCH of an unwritten register)"
            )
        return self.acc

    def pair(self, p: int) -> int:
        return self._r(2 * p) << 4 | self._r(2 * p + 1)

    def set_pair(self, p: int, value: int) -> None:
        self.regs[2 * p], self.regs[2 * p + 1] = value >> 4 & 15, value & 15

    def _fetch(self) -> int:
        byte = self.rom[self.pc]
        self.pc = self.pc + 1
        return byte

    def _add(self, a: int, b: int, cin: int) -> None:
        total = a + b + cin
        self.acc, self.cy = total & 15, total >> 4

    def halted(self) -> bool:
        """At a jump to itself: `JUN` with its own address."""
        pc = self.pc
        return self.rom[pc] == 0x40 | pc >> 8 and self.rom[(pc + 1) & 0xFFF] == pc & 0xFF

    def step(self) -> int:
        """Run one instruction. Returns the instruction cycles it took (1 or 2)."""
        at = self.pc
        byte = self._fetch()
        opr, opa = byte >> 4, byte & 15
        took = 1
        if opr == 0x0:
            if opa:
                raise ModelError(f"0x{byte:02X} at 0x{at:03X} is not a 4004 instruction")
        elif opr in (0x1, 0x4, 0x5, 0x7) or (opr == 0x2 and not opa & 1):
            took = 2
            second = self._fetch()
            if opr == 0x1:  # JCN
                zero, carry, notest = self._acc() == 0, self.cy == 1, self.test == 0
                hit = (opa & 4 and zero) or (opa & 2 and carry) or (opa & 1 and notest)
                if bool(hit) != bool(opa & 8):
                    self.pc = (self.pc & 0xF00) | second
            elif opr == 0x2:  # FIM
                self.set_pair(opa >> 1, second)
            elif opr == 0x4:  # JUN
                self.pc = opa << 8 | second
            elif opr == 0x5:  # JMS
                self.sp = (self.sp + 1) % 4
                self.pc = opa << 8 | second
            else:  # ISZ
                self.regs[opa] = (self._r(opa) + 1) & 15
                if self.regs[opa]:
                    self.pc = (self.pc & 0xF00) | second
        elif opr == 0x2:  # SRC
            address = self.pair(opa >> 1)
            self.src_rom = address >> 4
            self.src_ram[self.bank] = address
        elif opr == 0x3:
            if opa & 1:  # JIN
                self.pc = (self.pc & 0xF00) | self.pair(opa >> 1)
            else:  # FIN: a second cycle fetches from the page of the next instruction
                took = 2
                self.set_pair(opa >> 1, self.rom[(self.pc & 0xF00) | self.pair(0)])
        elif opr == 0x6:  # INC
            self.regs[opa] = (self._r(opa) + 1) & 15
        elif opr == 0x8:  # ADD
            self._add(self._acc(), self._r(opa), self.cy)
        elif opr == 0x9:  # SUB
            self._add(self._acc(), ~self._r(opa) & 15, 1 - self.cy)
        elif opr == 0xA:  # LD
            self.acc = self._r(opa)
        elif opr == 0xB:  # XCH: undefined values may move, as the hardware moves them
            self.acc, self.regs[opa] = self.regs[opa], self.acc
        elif opr == 0xC:  # BBL
            self.sp = (self.sp - 1) % 4
            self.acc = opa
        elif opr == 0xD:  # LDM
            self.acc = opa
        elif opr == 0xE:
            self._io(opa, at)
        else:
            self._accumulator(opa, at)
        self.cycles += took
        return took

    def _ram_address(self, at: int) -> int:
        if self.bank not in self.src_ram:
            raise ModelError(f"RAM instruction at 0x{at:03X}: no SRC in bank {self.bank}")
        return self.src_ram[self.bank]

    def _io(self, opa: int, at: int) -> None:
        if opa in (2, 10):  # WRR, RDR
            if self.src_rom is None:
                raise ModelError(f"ROM port instruction at 0x{at:03X} before any SRC")
            if opa == 2:
                self.romport_out[self.src_rom] = self._acc()
            elif self.src_rom not in self.romport_in:
                raise ModelError(f"RDR at 0x{at:03X}: 4001 #{self.src_rom}'s input isn't set")
            else:
                self.acc = self.romport_in[self.src_rom]
            return
        if opa == 3:  # WPM: needs a 4008/4009, which isn't modelled
            return
        address = self._ram_address(at)
        if opa == 1:  # WMP
            self.ramport[(self.bank, address >> 6)] = self._acc()
            return
        if 4 <= opa < 8 or opa >= 12:
            store, key = self.status, (self.bank, address >> 4, opa & 3)
        else:
            store, key = self.main, (self.bank, address)  # type: ignore[assignment]
        if opa < 8:  # WRM, WR0-3
            store[key] = self._acc()  # type: ignore[index]
            return
        if key not in store:
            raise ModelError(f"read at 0x{at:03X} of RAM bank {self.bank} {key[1:]}, never written")
        value = store[key]  # type: ignore[index]
        if opa == 8:  # SBM
            self._add(self._acc(), ~value & 15, 1 - self.cy)
        elif opa == 11:  # ADM
            self._add(self._acc(), value, self.cy)
        else:  # RDM, RD0-3
            self.acc = value

    def _accumulator(self, opa: int, at: int) -> None:
        cy = self.cy
        # CLB, CLC, CMC, TCC, TCS and STC don't read A, so they may follow an undefined one.
        a = self._acc() if opa in (2, 4, 5, 6, 8, 11, 12, 13) else 0
        if opa == 0:  # CLB
            self.acc, self.cy = 0, 0
        elif opa == 1:  # CLC
            self.cy = 0
        elif opa == 2:  # IAC
            self._add(a, 1, 0)
        elif opa == 3:  # CMC
            self.cy = 1 - cy
        elif opa == 4:  # CMA
            self.acc = ~a & 15
        elif opa == 5:  # RAL
            self.acc, self.cy = (a << 1 | cy) & 15, a >> 3
        elif opa == 6:  # RAR
            self.acc, self.cy = a >> 1 | cy << 3, a & 1
        elif opa == 7:  # TCC
            self.acc, self.cy = cy, 0
        elif opa == 8:  # DAC: a + 15, so the carry is 1 unless there was a borrow
            self._add(a, 15, 0)
        elif opa == 9:  # TCS
            self.acc, self.cy = 9 + cy, 0
        elif opa == 10:  # STC
            self.cy = 1
        elif opa == 11:  # DAA: the carry is set on overflow, otherwise left alone
            if a > 9 or cy:
                total = a + 6
                self.acc = total & 15
                if total > 15:
                    self.cy = 1
        elif opa == 12:  # KBP
            self.acc = KBP.get(a, 15)
        elif opa == 13:  # DCL
            self.bank = a & 7
        else:
            raise ModelError(f"0xF{opa:X} at 0x{at:03X} is not a 4004 instruction")

    def run(self, max_cycles: int = 100_000) -> int:
        """Step until the program halts. Returns the instruction cycles it took."""
        start = self.cycles
        while not self.halted():
            if self.cycles - start > max_cycles:
                raise ModelError(f"no halt after {max_cycles} instruction cycles")
            self.step()
        return self.cycles - start


def main() -> None:
    m = Mcs4(rom=assemble(open(sys.argv[1]).read()))
    m.reset()
    took = m.run()
    print(f"halted at 0x{m.pc:03X} after {took} instruction cycles ({8 * took} clocks)")
    print(f"acc={m.acc} cy={m.cy} bank={m.bank} regs={' '.join(f'{r:X}' for r in m.regs)}")
    for (bank, addr), v in sorted(m.main.items()):
        print(f"ram {bank} 0x{addr:02X} = {v}")


if __name__ == "__main__":
    main()
