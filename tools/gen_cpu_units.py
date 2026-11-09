"""Generate the tests of the CPU's five unit levels from small models of each unit.

A development script, not part of the game:

    uv run python tools/gen_cpu_units.py chips/05_cpu

Sequencer, Accumulator, Registers and Jumps are sequential: each test starts with a cycle
before any reset (outputs `*`), then runs random cycles with fixed seeds, checking after
each tick (the old value) and each tock. BusOut is combinational: a table of random rows
plus every period against each kind of instruction. The Accumulator's arithmetic comes from
tools/model4004.py, so the units agree with the 4004 model the CPU test is built from.
`tests/test_tools.py` checks the committed files match this script.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model4004 as m4  # noqa: E402

SEED = 4004
Bit = int | None


def fmt(v: int | None, digits: int = 1) -> str:
    return "*" if v is None else f"0x{v:0{digits}X}"


def is_fim(opr: int, opa: int) -> bool:
    return opr == 2 and not opa & 1


def is_fin(opr: int, opa: int) -> bool:
    return opr == 3 and not opa & 1


def two_cycle(opr: int, opa: int) -> bool:
    return opr in (1, 4, 5, 7) or is_fim(opr, opa) or is_fin(opr, opa)


class Script:
    def __init__(self, chip: str, header: list[str]) -> None:
        self.lines = [f"// {h}" for h in header] + [f"chip {chip}"]

    def sets(self, **pins: int) -> None:
        self.lines += [f"set {p} {v}" for p, v in pins.items()]

    def expect(self, **pins: str) -> None:
        self.lines += [f"expect {p} {v}" for p, v in pins.items()]

    def comment(self, text: str) -> None:
        self.lines.append(f"// {text}")

    @property
    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


def clocked(s: Script, inputs: dict[str, int], show: Callable[[], dict[str, str]],
            advance: Callable[[], None]) -> None:  # fmt: skip
    """One clock cycle: set inputs, tick (old outputs), tock (new outputs)."""
    s.sets(**inputs)
    s.lines.append("tick")
    s.expect(**show())
    s.lines.append("tock")
    advance()
    s.expect(**show())


# ---- Sequencer ----------------------------------------------------------------


def sequencer() -> str:
    rng = random.Random(SEED)
    s = Script("Sequencer", [
        "Sequencer: `second` is 1 in the second instruction cycle of JCN FIM FIN JUN JMS ISZ;",
        "it changes at X3 (period 7) and clears on reset. `finfetch` is `second` and FIN.",
        "Instruction cycles in period order, with the instruction kept over both cycles as",
        "InstrReg keeps it, then random periods. Generated from a model, seed 4004.",
    ])  # fmt: skip
    state: list[Bit] = [None]

    def show(opr: int, opa: int) -> Callable[[], dict[str, str]]:
        def f() -> dict[str, str]:
            sec = state[0]
            fin = None if sec is None else int(sec == 1 and is_fin(opr, opa))
            if sec == 0:
                fin = 0
            return {"second": fmt(sec), "finfetch": fmt(fin)}

        return f

    def cycle(opr: int, opa: int, period: int, reset: int) -> None:
        def advance() -> None:
            sec = state[0]
            if reset:
                state[0] = 0
            elif period == 7:
                if not two_cycle(opr, opa) or sec == 1:
                    state[0] = 0
                else:
                    state[0] = None if sec is None else 1

        clocked(s, {"opr": opr, "opa": opa, "period": period, "reset": reset},
                show(opr, opa), advance)  # fmt: skip

    s.comment("Before any reset, `second` is unknown.")
    cycle(4, 0, 7, 0)
    s.comment("Reset, then instruction cycles as Timing and InstrReg run them.")
    cycle(0, 0, 0, 1)
    kinds = [(1, 6), (2, 4), (2, 5), (3, 2), (3, 3), (4, 1), (5, 2), (7, 9), (0, 0), (0xD, 3),
             (0xE, 9), (0xF, 2), (6, 1), (0xB, 4)]  # fmt: skip
    for _ in range(40):
        opr, opa = rng.choice(kinds)
        for period in range(8):
            cycle(opr, opa, period, 0)
        if state[0] == 1:  # its second cycle, with the first word still in InstrReg
            for period in range(8):
                cycle(opr, opa, period, 0)
    s.comment("Random periods and instructions, reset now and then.")
    for _ in range(120):
        opr, opa = rng.choice(kinds)
        cycle(opr, opa, rng.randrange(8), int(rng.random() < 0.06))
    return s.text


# ---- Accumulator --------------------------------------------------------------


def alu(op: str | int, a: int, b: int, cin: int) -> tuple[int, int]:
    """A and CY after an ALU operation, from the 4004 model."""
    m = m4.Mcs4()
    m.acc, m.cy = a, cin
    if op == "LD":
        return b, cin
    if op == "ADD":
        m._add(a, b, cin)
    elif op == "SUB":
        m._add(a, ~b & 15, 1 - cin)
    else:
        m._accumulator(int(op), 0)
    return m.acc, m.cy  # type: ignore[return-value]


def acc_effect(opr: int, opa: int, a: int, cy: int, reg: int, din: int) -> tuple[int, int] | None:
    """What an instruction does to A and CY, or None if it leaves them alone."""
    if 8 <= opr <= 0xD:
        b = reg if opr <= 0xB else opa
        op = {8: "ADD", 9: "SUB"}.get(opr, "LD")
        return alu(op, a, b, cy)
    if opr == 0xE and opa >= 8:
        op = {8: "SUB", 11: "ADD"}.get(opa, "LD")
        return alu(op, a, din, cy)
    if opr == 0xF and opa <= 12:
        return alu(opa, a, 0, cy)
    return None


def accumulator() -> str:
    rng = random.Random(SEED + 1)
    s = Script("Accumulator", [
        "Accumulator: with write at 1, the instruction's effect on A, CY and DCL's bank, from",
        "a set A, CY, register and bus value; with reset at 1, all three clear. Random",
        "instructions (every OPR and OPA appears) with seed 4005, from tools/model4004.py.",
    ])  # fmt: skip
    st: dict[str, int | None] = {"acc": None, "carry": None, "bank": None}

    def show() -> dict[str, str]:
        return {"acc": fmt(st["acc"]), "carry": fmt(st["carry"]), "bank": fmt(st["bank"])}

    def cycle(opr: int, opa: int, reg: int, din: int, write: int, reset: int) -> None:
        def advance() -> None:
            if reset:
                st.update(acc=0, carry=0, bank=0)
                return
            if not write:
                return
            if opr == 0xF and opa == 13:
                st["bank"] = None if st["acc"] is None else st["acc"] & 7
                return
            if st["acc"] is None or st["carry"] is None:
                if acc_effect(opr, opa, 0, 0, reg, din) is not None:
                    st.update(acc=None, carry=None)
                return
            new = acc_effect(opr, opa, st["acc"], st["carry"], reg, din)
            if new is not None:
                st["acc"], st["carry"] = new

        inputs = {"opr": opr, "opa": opa, "reg": reg, "din": din, "write": write, "reset": reset}
        clocked(s, inputs, show, advance)

    s.comment("Before any reset everything is unknown; without write nothing changes.")
    cycle(0xD, 5, 0, 0, 0, 0)
    s.comment("Reset, then every OPR and OPA once with write at 1, from changing A and CY.")
    cycle(0, 0, 0, 0, 0, 1)
    for opr in range(16):
        for opa in range(16):
            if opr == 0xD:  # LDM sets a known A for what follows
                pass
            cycle(opr, opa, rng.randrange(16), rng.randrange(16), 1, 0)
            if opr == 0xF and opa == 0:
                cycle(0xD, 9, 0, 0, 1, 0)  # after CLB, a nonzero A again
    s.comment("Random instructions; write at 0 now and then, reset rarely.")
    for _ in range(300):
        opr = rng.choice([8, 9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xE, 0xF, 0xF, 0xF, rng.randrange(8)])
        cycle(opr, rng.randrange(16), rng.randrange(16), rng.randrange(16),
              int(rng.random() < 0.85), int(rng.random() < 0.02))  # fmt: skip
    return s.text


# ---- Registers ----------------------------------------------------------------


def registers() -> str:
    rng = random.Random(SEED + 2)
    s = Script("Registers", [
        "Registers: reg and pair are register opa and its pair (pair 0 while readp0 is 1).",
        "With write at 1: XCH writes acc, INC and ISZ add one, in a first cycle; FIM and FIN",
        "write data to the pair in a second cycle. Reset clears all 16. readp0 and write are",
        "never 1 together. Random cycles with seed 4006, from a model.",
    ])  # fmt: skip
    regs: list[int | None] = [None] * 16

    def show(opa: int, readp0: int) -> Callable[[], dict[str, str]]:
        def f() -> dict[str, str]:
            addr = 0 if readp0 else opa
            r = regs[addr]
            even, odd = regs[addr & 14], regs[addr | 1]
            pair = None if even is None or odd is None else even << 4 | odd
            return {"reg": fmt(r), "pair": fmt(pair, 2)}

        return f

    def cycle(opr: int, opa: int, acc: int, data: int, second: int, write: int, readp0: int,
              reset: int) -> None:  # fmt: skip
        def advance() -> None:
            if reset:
                regs[:] = [0] * 16
                return
            if not write:
                return
            if not second and opr in (0xB, 6, 7):
                if opr == 0xB:
                    regs[opa] = acc
                else:
                    r = regs[opa]
                    regs[opa] = None if r is None else (r + 1) & 15
            elif second and (is_fim(opr, opa) or is_fin(opr, opa)):
                regs[opa & 14], regs[opa | 1] = data >> 4, data & 15

        inputs = {"opr": opr, "opa": opa, "acc": acc, "data": data, "second": second,
                  "write": write, "readp0": readp0, "reset": reset}  # fmt: skip
        s.sets(**inputs)
        s.lines.append("eval")
        s.expect(**show(opa, readp0)())
        clocked(s, {}, show(opa, readp0), advance)

    s.comment("Before any reset the registers are unknown.")
    cycle(0xB, 3, 5, 0, 0, 0, 0, 0)
    s.comment("Reset, then each register read, and written by XCH.")
    cycle(0, 0, 0, 0, 0, 0, 0, 1)
    for r in range(16):
        cycle(0xA, r, 0, 0, 0, 0, 0, 0)
        cycle(0xB, r, (r * 7 + 3) & 15, 0, 0, 1, 0, 0)
    s.comment("Random instructions, first and second cycles, readp0 and reset now and then.")
    kinds = [0xB, 6, 7, 2, 3, 2, 3, 0xA, 8, 0xE, 1, 4]
    for _ in range(300):
        opr, opa = rng.choice(kinds), rng.randrange(16)
        readp0 = int(rng.random() < 0.15)
        write = 0 if readp0 else int(rng.random() < 0.8)
        cycle(opr, opa, rng.randrange(16), rng.randrange(256), rng.randrange(2), write, readp0,
              int(rng.random() < 0.02))  # fmt: skip
    return s.text


# ---- Jumps ----------------------------------------------------------------------


def cond(c: int, acc: int, carry: int, test: int) -> bool:
    hit = (c & 4 and acc == 0) or (c & 2 and carry == 1) or (c & 1 and test == 0)
    return bool(hit) != bool(c & 8)


def jumps() -> str:
    rng = random.Random(SEED + 3)
    s = Script("Jumps", [
        "Jumps: step adds one to the PC; exec at 1 runs the instruction's jump: in a second",
        "cycle JUN, JMS, and JCN and ISZ when they jump; in a first cycle JIN and BBL. Reset",
        "clears the PC and the stack. step and exec are never 1 together. Random cycles with",
        "seed 4007, from a model of the 4004's 4-level stack.",
    ])  # fmt: skip
    st: dict[str, object] = {"stack": [None] * 4, "sp": None}

    def pc() -> int | None:
        if st["sp"] is None:
            return None
        return st["stack"][st["sp"]]  # type: ignore[index]

    def show() -> dict[str, str]:
        return {"pc": fmt(pc(), 3)}

    def cycle(opr: int, opa: int, data: int, pair: int, reg: int, acc: int, carry: int,
              test: int, second: int, step: int, exec_: int, reset: int) -> None:  # fmt: skip
        def advance() -> None:
            stack: list[int | None] = st["stack"]  # type: ignore[assignment]
            if reset:
                st["stack"], st["sp"] = [0, 0, 0, 0], 0
                return
            sp = st["sp"]
            cur = pc()
            if step:
                if sp is not None:
                    stack[sp] = None if cur is None else (cur + 1) & 0xFFF  # type: ignore[index]
                return
            if not exec_ or sp is None:
                return
            page = None if cur is None else cur & 0xF00
            far = opa << 8 | data
            if second:
                if opr == 4:
                    stack[sp] = far  # type: ignore[index]
                elif opr == 5:
                    st["sp"] = (sp + 1) % 4  # type: ignore[operator]
                    stack[st["sp"]] = far  # type: ignore[index]
                elif (opr == 1 and cond(opa, acc, carry, test)) or (opr == 7 and reg != 0):
                    stack[sp] = None if page is None else page | data  # type: ignore[index]
            elif opr == 3 and opa & 1:
                stack[sp] = None if page is None else page | pair  # type: ignore[index]
            elif opr == 0xC:
                st["sp"] = (sp - 1) % 4  # type: ignore[operator]

        inputs = {"opr": opr, "opa": opa, "data": data, "pair": pair, "reg": reg, "acc": acc,
                  "carry": carry, "test": test, "second": second, "step": step, "exec": exec_,
                  "reset": reset}  # fmt: skip
        clocked(s, inputs, show, advance)

    def rand(**fixed: int) -> None:
        v = {"opr": rng.choice([1, 1, 3, 4, 5, 5, 7, 7, 0xC, 0xC, 2, 0xD]),
             "opa": rng.randrange(16), "data": rng.randrange(256), "pair": rng.randrange(256),
             "reg": rng.randrange(16),
             "acc": rng.choice([0, rng.randrange(16)]), "carry": rng.randrange(2),
             "test": rng.randrange(2), "second": rng.randrange(2), "step": 0, "exec_": 0,
             "reset": 0}  # fmt: skip
        v.update(fixed)
        cycle(*v.values())  # type: ignore[arg-type]

    s.comment("Before any reset the PC is unknown.")
    rand(step=1)
    s.comment("Reset, then steps, calls four deep, returns, and every kind of jump.")
    rand(reset=1)
    for _ in range(3):
        rand(step=1)
    for _ in range(4):  # four deep: the fourth call overwrites the oldest return
        rand(opr=5, second=1, exec_=1)
        rand(step=1)
    for _ in range(5):
        rand(opr=0xC, second=0, exec_=1)
    s.comment("Random cycles: a step, an exec or nothing; reset now and then.")
    for _ in range(400):
        kind = rng.random()
        if kind < 0.3:
            rand(step=1)
        elif kind < 0.85:
            rand(exec_=1)
        elif kind < 0.97:
            rand()
        else:
            rand(reset=1)
    return s.text


# ---- BusOut ---------------------------------------------------------------------


def lines_for(bank: int, on: bool) -> int:
    if not on:
        return 0
    return 1 if bank == 0 else bank << 1


def busout_row(period: int, pc: int, pair: int, acc: int, opr: int, opa: int, second: int,
               finfetch: int, bank: int) -> tuple[int, int, int, int]:  # fmt: skip
    first = not second
    issrc = opr == 2 and bool(opa & 1) and first
    iowrite = opr == 0xE and opa < 8 and first
    early, x2, x3 = period < 3, period == 6, period == 7
    fetch = (pc & 0xF00) | pair if finfetch else pc
    if early:
        value = fetch >> (4 * period) & 15
    elif x2:
        value = pair >> 4 if issrc else acc
    else:
        value = pair & 15
    drive = early or (x2 and (issrc or iowrite)) or (x3 and issrc)
    cmon = period == 2 or (period == 4 and opr == 0xE and first) or (x2 and issrc)
    return (value if drive else 0), int(drive), int(cmon), lines_for(bank, cmon)


def busout() -> str:
    rng = random.Random(SEED + 4)
    s = Script("BusOut", [
        "BusOut: A1-A3 send the address nibbles (P0 and the page while finfetch is 1), SRC",
        "sends its pair at X2 and X3, the I/O writes send acc at X2; dout is 0 when drive is 0.",
        "CM lines at A3, at M2 of OPR 1110 and at X2 of SRC. Every period against each kind",
        "of instruction, then random rows with seed 4008, from a model.",
    ])  # fmt: skip
    cols = ["period", "pc", "pair", "acc", "opr", "opa", "second", "finfetch", "bank"]
    s.lines.append(f"table {' '.join(cols)} | dout drive cmrom cmram")

    def row(*v: int) -> None:
        dout, drive, cmrom, cmram = busout_row(*v)
        period, pc, pair, acc, opr, opa, second, finfetch, bank = v
        s.lines.append(
            f"    {period} 0x{pc:03X} 0x{pair:02X} 0x{acc:X} 0x{opr:X} 0x{opa:X} {second} "
            f"{finfetch} {bank} | 0x{dout:X} {drive} {cmrom} 0b{cmram:04b}"
        )

    # (opr, opa, second, finfetch): SRC, FIM, WRM, WRR, RDM, WRM in a second cycle, LDM,
    # FIN's fetch, FIN's first cycle, DCL.
    kinds = [(2, 5, 0, 0), (2, 4, 0, 0), (0xE, 0, 0, 0), (0xE, 2, 0, 0), (0xE, 9, 0, 0),
             (0xE, 0, 1, 0), (0xD, 7, 0, 0), (3, 2, 1, 1), (3, 2, 0, 0),
             (0xF, 13, 0, 0)]  # fmt: skip
    for opr, opa, second, finfetch in kinds:
        for period in range(8):
            row(period, 0x5A3, 0xC9, 0x6, opr, opa, second, finfetch, period % 8)
    for _ in range(400):
        second = rng.randrange(2)
        row(rng.randrange(8), rng.randrange(4096), rng.randrange(256), rng.randrange(16),
            rng.choice([2, 2, 0xE, 0xE, 3, rng.randrange(16)]), rng.randrange(16), second,
            second & rng.randrange(2), rng.randrange(8))  # fmt: skip
    s.lines.append("end")
    return s.text


def generate() -> dict[str, str]:
    return {
        "Sequencer": sequencer(),
        "Accumulator": accumulator(),
        "Registers": registers(),
        "Jumps": jumps(),
        "BusOut": busout(),
    }


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("chips/05_cpu")
    for name, text in generate().items():
        (out / f"{name}.tst").write_text(text)


if __name__ == "__main__":
    main()
