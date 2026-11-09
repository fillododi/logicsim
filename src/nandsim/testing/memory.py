"""Memories held by the test runner and wired to a chip's pins: program ROM and data RAM.

The CPU levels reach memory through their pins, and the memory chips come later in the
game, so a `.tst` script attaches these instead (see docs/tst.md and docs/decisions.md).
They are test-harness code, not chips: they act like a combinational read port plus, for
the data memory, a write that is sampled at `tick` and stored at `tock`, as a DFF does.

Also here: the `.rom` file format, one byte per line in binary, shared with the ROM editor.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from nandsim.hdl import HdlError, SourcePos
from nandsim.sim import Simulator

ROM_SIZE = 4096  # the 4004's whole program address space
DATA_PINS = {"in": 4, "addr": 8, "bank": 3, "status": 1, "load": 1, "out": 4}  # as DataRAM

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
    """The character `addr` picks in `bank`, as DataRAM decodes it.

    A main character is `addr` itself. A status character is picked by the chip and
    register bits `addr[4..7]` and the character `addr[0..1]`; `addr[2..3]` are ignored.
    """
    if status:
        return (bank, "status", addr >> 4, addr & 3)
    return (bank, "main", addr)


def _check_pins(
    sim: Simulator,
    chip: str,
    links: dict[str, tuple[str, SourcePos]],
    widths: dict[str, int],
    kind: str,
) -> None:
    """Every memory pin reads a chip output of its width, and `out` drives a chip input."""
    nl = sim.netlist
    for mem_pin, (chip_pin, pos) in links.items():
        if mem_pin == "out":
            nets = nl.inputs.get(chip_pin)
            if nets is None:
                what = "an output" if chip_pin in nl.outputs else "not a pin"
                raise HdlError(
                    f"the {kind}'s out drives '{chip_pin}', which is {what} of {chip}: "
                    "it must be an input",
                    pos,
                )
        else:
            nets = nl.outputs.get(chip_pin)
            if nets is None:
                what = "an input" if chip_pin in nl.inputs else "not a pin"
                raise HdlError(
                    f"the {kind}'s {mem_pin} reads '{chip_pin}', which is {what} of {chip}: "
                    "it must be an output",
                    pos,
                )
        want = widths[mem_pin]
        if mem_pin == "addr" and kind == "program memory":
            if not 1 <= len(nets) <= want:
                raise HdlError(
                    f"the {kind}'s addr has at most {want} bits, '{chip_pin}' has {len(nets)}",
                    pos,
                )
        elif len(nets) != want:
            raise HdlError(
                f"the {kind}'s {mem_pin} has {want} bit{'s' if want > 1 else ''}, "
                f"'{chip_pin}' has {len(nets)}",
                pos,
            )


@dataclass
class ProgramMemory:
    """4096 bytes, all 0 until written; `out` is the byte at `addr`, with no clock."""

    addr: str
    out: str
    data: list[int] = field(default_factory=lambda: [0] * ROM_SIZE)

    def write(self, start: int, values: list[int], pos: SourcePos) -> None:
        if start + len(values) > ROM_SIZE:
            raise HdlError(
                f"{len(values)} bytes from 0x{start:03X} run past the end of program memory "
                f"(0x{ROM_SIZE - 1:03X})",
                pos,
            )
        self.data[start : start + len(values)] = values

    def read(self, sim: Simulator) -> int | None:
        addr = sim.get(self.addr)
        return None if addr is None else self.data[addr]


@dataclass
class DataMemory:
    """The data memory DataRAM models: 8 banks of 4002s, every character undefined at first."""

    pins: dict[str, str]  # DataRAM pin -> chip pin
    cells: dict[CellKey, int | None] = field(default_factory=dict)
    pending: tuple[CellKey, int | None] | None = None  # sampled at tick, stored at tock

    def _key(self, sim: Simulator) -> CellKey | None:
        bank, addr, status = (sim.get(self.pins[p]) for p in ("bank", "addr", "status"))
        if bank is None or addr is None or status is None:
            return None
        return cell_key(bank, addr, bool(status))

    def read(self, sim: Simulator) -> int | None:
        key = self._key(sim)
        return None if key is None else self.cells.get(key)

    def sample(self, sim: Simulator) -> str | None:
        """At tick: remember the write `load` asks for. Returns a problem to report, if any.

        An undefined `load` writes nothing (a CPU's control lines are undefined until its
        reset cycle has run); `load` at 1 with an undefined address is a failure.
        """
        self.pending = None
        if sim.get(self.pins["load"]) != 1:
            return None
        key = self._key(sim)
        if key is None:
            pins = [self.pins[p] for p in ("bank", "addr", "status")]
            undefined = [p for p in pins if sim.get(p) is None]
            return (
                f"data memory: {self.pins['load']} is 1 but {', '.join(undefined)} "
                f"{'is' if len(undefined) == 1 else 'are'} undefined, so nothing was written"
            )
        self.pending = (key, sim.get(self.pins["in"]))
        return None

    def commit(self) -> None:
        """At tock: store the write sampled at the tick."""
        if self.pending is not None:
            key, value = self.pending
            self.cells[key] = value
            self.pending = None


MAX_PASSES = 8


class Memories:
    """The memories a script attached, kept in step with the simulator."""

    def __init__(self, sim: Simulator, chip: str) -> None:
        self.sim = sim
        self.chip = chip
        self.rom: ProgramMemory | None = None
        self.ram: DataMemory | None = None

    def __bool__(self) -> bool:
        return self.rom is not None or self.ram is not None

    def attach(self, kind: str, links: dict[str, tuple[str, SourcePos]]) -> None:
        if kind == "rom":
            _check_pins(self.sim, self.chip, links, {"addr": 12, "out": 8}, "program memory")
            self.rom = ProgramMemory(links["addr"][0], links["out"][0])
        else:
            _check_pins(self.sim, self.chip, links, DATA_PINS, "data memory")
            self.ram = DataMemory({p: pin for p, (pin, _) in links.items()})

    def driver(self, pin: str) -> str | None:
        """Which memory drives this chip input, if one does."""
        if self.rom is not None and self.rom.out == pin:
            return "program memory"
        if self.ram is not None and self.ram.pins["out"] == pin:
            return "data memory"
        return None

    def settle(self, pos: SourcePos) -> None:
        """Evaluate, then drive each memory's `out` from its address until nothing changes."""
        sim = self.sim
        sim.eval()
        mems = [m for m in (self.rom, self.ram) if m is not None]
        for _ in range(MAX_PASSES):
            changed = False
            for mem in mems:
                out = mem.out if isinstance(mem, ProgramMemory) else mem.pins["out"]
                want = mem.read(sim)
                have = sim.get_bits(out)
                if want is None:
                    stale = any(b is not None for b in have)
                else:
                    stale = sim.get(out) != want
                if stale:
                    sim.set(out, want)
                    changed = True
            if not changed:
                return
            sim.eval()
        addrs = [p for p in (self.rom and self.rom.addr, self.ram and self.ram.pins["addr"]) if p]
        raise HdlError(
            f"the memories and {self.chip} never settled: after {MAX_PASSES} passes, "
            f"{' and '.join(addrs)} still changed with what the memory sent back",
            pos,
        )

    def before_tick(self, pos: SourcePos) -> str | None:
        self.settle(pos)
        return self.ram.sample(self.sim) if self.ram is not None else None

    def after_tick(self, pos: SourcePos) -> None:
        if self.sim.reads_clock:  # the rising clock may have moved an address
            self.settle(pos)

    def after_tock(self, pos: SourcePos) -> None:
        if self.ram is not None:
            self.ram.commit()
        self.settle(pos)
