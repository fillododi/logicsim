"""The MCS-4 memories a test runner puts on a 4004's bus: 4001 ROMs and 4002 RAMs.

The CPU level has the 4004's pins (see docs/decisions.md, 2026-11-09), and the memory chips
come later in the game, so a `.tst` script attaches these with `attach mcs4`. They are
test-harness code, not chips. Like the real 4001s and 4002s they count the 8 clock periods
of each instruction cycle (A1 A2 A3 M1 M2 X1 X2 X3) from reset, read the bus at every tick,
and drive `din` for the periods in which they send. Sixteen 4001s hold the 4 KB of program
memory, each with an I/O port; eight banks of four 4002s hold the data memory, each 4002
with an output port.

Also here: the `.rom` file format, one byte per line in binary, shared with the ROM editor.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from nandsim.hdl import HdlError, SourcePos
from nandsim.sim import Simulator

ROM_SIZE = 4096  # the 4004's whole program address space
PERIODS = ("A1", "A2", "A3", "M1", "M2", "X1", "X2", "X3")
A1, A2, A3, M1, M2, X1, X2, X3 = range(8)

# The CPU pins `attach mcs4` connects: name -> (width, direction seen from the CPU).
BUS_PINS: dict[str, tuple[int, str]] = {
    "din": (4, "in"),
    "dout": (4, "out"),
    "drive": (1, "out"),
    "sync": (1, "out"),
    "cmrom": (1, "out"),
    "cmram": (4, "out"),
    "reset": (1, "in"),
}

# The I/O and RAM instructions (OPR 1110), by OPA. Writes take the accumulator from the
# bus at X2; reads put a value on it.
IO_NAMES = (
    "WRM", "WMP", "WRR", "WPM", "WR0", "WR1", "WR2", "WR3",
    "SBM", "RDM", "RDR", "ADM", "RD0", "RD1", "RD2", "RD3",
)  # fmt: skip
WRM, WMP, WRR, WPM = 0, 1, 2, 3
SBM, RDM, RDR, ADM = 8, 9, 10, 11

# A data memory character: (bank, "main", addr) or (bank, "status", chip and register, char).
CellKey = tuple[int, str, int] | tuple[int, str, int, int]


def parse_rom(text: str, filename: str = "<rom>") -> list[int]:
    """Parse a `.rom` file: one byte per line, 8 binary digits, `//` comments.

    Spaces and `_` may group the digits (`1101 0101`). Blank and comment-only lines hold
    no byte, so line numbers don't have to match addresses. Raises `HdlError` at the first
    problem, with its line and column.
    """
    data: list[int] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        code = line.split("//", 1)[0]
        stripped = code.strip()
        if not stripped:
            continue
        col = code.index(stripped[0]) + 1
        bad = next((i for i, c in enumerate(code) if c not in "01 _\t"), None)
        if bad is not None:
            raise HdlError(
                f"'{code[bad]}' in a byte: write each byte as 8 binary digits, like 1101 0101",
                SourcePos(filename, lineno, bad + 1),
            )
        digits = "".join(c for c in stripped if c in "01")
        if len(digits) != 8:
            raise HdlError(
                f"a byte has 8 binary digits, this line has {len(digits)}",
                SourcePos(filename, lineno, col),
            )
        if len(data) == ROM_SIZE:
            raise HdlError(
                f"too many bytes: program memory holds {ROM_SIZE}",
                SourcePos(filename, lineno, col),
            )
        data.append(int(digits, 2))
    return data


def cell_key(bank: int, addr: int, status: bool) -> CellKey:
    """The character `addr` picks in `bank`, as DataRAM and SRC address it.

    `addr[6..7]` pick the 4002 and `addr[4..5]` its register, which is what SRC sends at
    X2. A main character is then `addr[0..3]`, sent at X3. A status character is
    `addr[0..1]`; `addr[2..3]` are ignored.
    """
    if status:
        return (bank, "status", addr >> 4, addr & 3)
    return (bank, "main", addr)


def decode_bank(lines: int) -> int | None:
    """The bank the CM-RAM lines select, or None for none.

    CM-RAM0 alone is bank 0; CM-RAM1..3 carry banks 1-7 as a binary number, as a 3-to-8
    decoder on them does in Intel's 8-bank layout. So bank n is what `DCL` n selects.
    Raises ValueError when CM-RAM0 and another line are both active.
    """
    if lines & 1:
        if lines >> 1:
            raise ValueError("cmram selects bank 0 and another bank at once")
        return 0
    return (lines >> 1) or None


def check_pins(sim: Simulator, chip: str, links: dict[str, tuple[str, SourcePos]]) -> None:
    """Each link reaches a chip pin of the width and direction `BUS_PINS` gives."""
    nl = sim.netlist
    for name, (pin, pos) in links.items():
        width, direction = BUS_PINS[name]
        table, other = (nl.inputs, nl.outputs) if direction == "in" else (nl.outputs, nl.inputs)
        nets = table.get(pin)
        if nets is None:
            what = (
                f"an {'output' if direction == 'in' else 'input'}" if pin in other else "not a pin"
            )
            raise HdlError(
                f"mcs4 {name} needs {chip}'s {direction}put, but '{pin}' is {what} of {chip}",
                pos,
            )
        if len(nets) != width:
            raise HdlError(
                f"mcs4 {name} has {width} bit{'s' if width > 1 else ''}, '{pin}' has {len(nets)}",
                pos,
            )


@dataclass
class Mcs4:
    """Sixteen 4001s and eight banks of 4002s on a CPU's bus, as the runner simulates them."""

    sim: Simulator
    pins: dict[str, str]  # BUS_PINS name -> chip pin
    rom: list[int] = field(default_factory=lambda: [0] * ROM_SIZE)
    cells: dict[CellKey, int | None] = field(default_factory=dict)
    romport_in: dict[int, int] = field(default_factory=dict)  # what RDR reads, per 4001
    romport_out: dict[int, int | None] = field(default_factory=dict)  # what WRR wrote
    ramport: dict[tuple[int, int], int | None] = field(default_factory=dict)  # (bank, 4002)
    phase: int | None = None  # the current period; None until the first reset
    next_phase: int | None = None  # decided at the tick, taken at the tock
    complained: bool = False  # only the first bus problem is reported

    # One instruction cycle's state.
    addr: list[int | None] = field(default_factory=lambda: [None, None, None])
    fetch_chip: int | None = None  # the 4001 that matched at A3
    opa: int | None = None
    io_rom: bool = False  # CM-ROM at M2: the 4001 picked by SRC takes this instruction
    io_bank: int | None = None  # CM-RAM at M2: that bank's 4002 picked by SRC takes it
    # What SRC selected: the 4001 chip number, and per bank the X2 and X3 nibbles.
    src_rom: int | None = None
    src_ram: dict[int, tuple[int, int | None]] = field(default_factory=dict)
    src_bank: int | None = None  # the bank that took X2 of this cycle's SRC

    def period(self) -> str:
        return "?" if self.phase is None else PERIODS[self.phase]

    def _get(self, name: str) -> int | None:
        return self.sim.get(self.pins[name])

    # ---- what the memories send -----------------------------------------

    def sender(self) -> tuple[str, int | None] | None:
        """Who drives the bus in the current period, and the value, or None if no memory does."""
        p = self.phase
        if p in (M1, M2) and self.fetch_chip is not None:
            if None in self.addr:
                return (f"4001 #{self.fetch_chip}", None)
            a = self.addr[0] | self.addr[1] << 4 | self.addr[2] << 8  # type: ignore[operator]
            byte = self.rom[a]
            return (f"4001 #{self.fetch_chip}", byte >> 4 if p == M1 else byte & 15)
        if p != X2 or self.opa is None or self.opa < SBM:
            return None
        if self.opa == RDR:
            if self.io_rom and self.src_rom is not None:
                return (f"4001 #{self.src_rom}", self.romport_in.get(self.src_rom))
            return None
        key = self._ram_key()
        if key is None:
            return None
        return (f"4002 in bank {self.io_bank}", self.cells.get(key))

    def _ram_key(self) -> CellKey | None:
        """The character this cycle's RAM instruction reaches, if SRC picked a 4002 there."""
        if self.io_bank is None or self.opa is None or self.io_bank not in self.src_ram:
            return None
        high, char = self.src_ram[self.io_bank]
        if self.opa >= 12 or 4 <= self.opa < 8:  # RD0-3, WR0-3: a status character
            return cell_key(self.io_bank, high << 4 | (self.opa & 3), True)
        if char is None:
            return None
        return cell_key(self.io_bank, high << 4 | char, False)

    def drive_bus(self) -> None:
        """Put the sender's value on `din`, or 0 when no memory sends, and evaluate.

        Most periods leave `din` as it was, and then nothing needs evaluating again.
        """
        s = self.sender()
        value = 0 if s is None else s[1]
        din = self.pins["din"]
        bits = self.sim.get_bits(din)
        same = all(b is None for b in bits) if value is None else self.sim.get(din) == value
        if not same:
            self.sim.set(din, value)
        self.sim.refresh()

    # ---- the clock ------------------------------------------------------

    def tick(self) -> str | None:
        """Read the bus for the current period. Returns the first protocol problem, if any."""
        reset = self._get("reset")
        if reset == 1:
            self._reset()
            return None
        self.next_phase = None if self.phase is None else (self.phase + 1) % 8
        if self.phase is None or reset is None:
            return None
        problem = self._period()
        if problem is None or self.complained:
            return None
        self.complained = True
        return problem

    def tock(self) -> None:
        """The next period starts: the memories that send in it drive the bus."""
        self.phase = self.next_phase
        if self.phase == A1:
            self.addr = [None, None, None]
            self.fetch_chip = None
            self.opa = None
            self.io_rom, self.io_bank = False, None
        self.drive_bus()

    def _reset(self) -> None:
        """RESET: the next period is A1, SRC selections and output ports are cleared.

        The memory contents stay, so a test can fill them before it resets the CPU.
        """
        self.next_phase = A1
        self.src_rom, self.src_ram, self.src_bank = None, {}, None
        self.romport_out = dict.fromkeys(range(16), 0)
        self.ramport = {(b, c): 0 for b in range(8) for c in range(4)}

    def _period(self) -> str | None:
        p = self.phase
        drive, dout, sync = self._get("drive"), self._get("dout"), self._get("sync")
        if sync != (p == X3):
            want = "1 only during X3" if p != X3 else "1 during X3, before each A1"
            return f"sync is {_show(sync)} at {PERIODS[p]}: it must be {want}"  # type: ignore[index]
        if drive == 0 and dout != 0:
            return (
                f"dout is {_show(dout)} while drive is 0: it must be 0 when the CPU isn't driving"
            )
        s = self.sender()
        if s is not None and drive != 0:
            return f"drive is {_show(drive)} while {s[0]} sends on the bus"
        if p in (A1, A2, A3):
            if drive != 1:
                return f"the CPU must send the address at {PERIODS[p]}, but drive is {_show(drive)}"
            self.addr[p] = dout  # type: ignore[index]
            if p == A3 and self._get("cmrom") == 1:
                self.fetch_chip = dout
        elif p == M2:
            self.opa = s[1] if s is not None else None
            self.io_rom = self._get("cmrom") == 1
            try:
                self.io_bank = self._bank()
            except ValueError as e:
                return f"{e} at M2"
            if not (self.io_rom or self.io_bank is not None):
                self.opa = None  # not an I/O or RAM instruction: no memory acts on it
        elif p == X2:
            return self._x2(drive, dout)
        elif p == X3 and self.src_bank is not None:
            if drive != 1:
                return f"SRC must send its second register at X3, but drive is {_show(drive)}"
            high, _ = self.src_ram[self.src_bank]
            self.src_ram[self.src_bank] = (high, dout)
            self.src_bank = None
        return None

    def _bank(self) -> int | None:
        lines = self._get("cmram")
        if lines is None:
            raise ValueError("cmram is undefined")
        return decode_bank(lines)

    def _x2(self, drive: int | None, dout: int | None) -> str | None:
        """SRC (CM lines active now), or the data of an I/O or RAM instruction."""
        cmrom = self._get("cmrom") == 1
        try:
            bank = self._bank()
        except ValueError as e:
            return f"{e} at X2"
        if cmrom or bank is not None:
            if drive != 1:
                return f"SRC must send its first register at X2, but drive is {_show(drive)}"
            if cmrom:
                self.src_rom = dout
            if bank is not None:
                self.src_ram[bank] = (dout, None)  # type: ignore[assignment]
                self.src_bank = bank
        op = self.opa
        if op is not None and op >= SBM:  # a read: `sender` put the value on the bus
            if self.sender() is None:
                chip = "4001" if op == RDR else "4002"
                return f"{IO_NAMES[op]} at X2, but no {chip} was selected by SRC"
            return None
        if op is None or op == WPM:
            return None  # WPM needs a 4008/4009, which isn't modelled
        if drive != 1:
            return f"{IO_NAMES[op]} must send the accumulator at X2, but drive is {_show(drive)}"
        if op == WRR:
            if self.io_rom and self.src_rom is not None:
                self.romport_out[self.src_rom] = dout
            return None
        if self.io_bank is None:
            return f"{IO_NAMES[op]} at X2, but no CM-RAM line was 1 at M2"
        if self.io_bank not in self.src_ram:
            return f"{IO_NAMES[op]} at X2, but no 4002 was selected by SRC in bank {self.io_bank}"
        if op == WMP:
            self.ramport[(self.io_bank, self.src_ram[self.io_bank][0] >> 2)] = dout
            return None
        key = self._ram_key()
        if key is not None:
            self.cells[key] = dout
        return None


def _show(v: int | None) -> str:
    return "undefined" if v is None else str(v)
