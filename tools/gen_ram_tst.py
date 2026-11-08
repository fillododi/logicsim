"""Generate the RAM levels' .tst files (RAM8 up to DataRAM) from a Python model.

A development script, not part of the game. Run it after changing the RAM levels' rules:

    uv run python tools/gen_ram_tst.py chips/04_seq

The output is deterministic (seed 4004), and `tests/test_tools.py` checks that the committed
files match it. Every test up to RAMBank has the same shape:

1. fill: write every cell once (its old value is undefined, so after the tick that check is `*`);
2. rewrite: write every cell again with a different value, so the check after the tick
   compares against a real old value and catches a RAM that shows `in` before the clock edge;
3. read every cell back with `load` off;
4. random cycles, which now always read cells that hold a known value.

DataRAM has 2,560 cells, too many to fill in a test the player waits for, so it does the same
on a sample of each bank that reaches every address bit (see `dataram`).
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

SEED = 4004

# ("main", address, 0) or ("status", register bits, character). With banks, the address
# carries the bank above its 8 bits, so the keys of different banks never meet.
Key = tuple[str, int, int]


@dataclass
class Gen:
    """Writes a .tst script while tracking what a correct RAM holds."""

    name: str
    header: list[str]
    status: bool  # whether the chip has a `status` pin
    banks: bool = False  # whether the chip has a `bank` pin, taken from addr >> 8
    mem: dict[Key, int] = field(default_factory=dict)
    lines: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.lines = [f"// {h}" for h in self.header] + [f"chip {self.name}"]

    @staticmethod
    def key(addr: int, st: int) -> Key:
        if not st:
            return ("main", addr, 0)
        # A status character: the chip and register bits, and addr[0..1]; addr[2..3] ignored.
        return ("status", addr >> 4, addr & 3)

    @staticmethod
    def fmt(v: int | None) -> str:
        return "*" if v is None else f"0x{v:X}"

    def _set(self, v: int, addr: int, st: int, load: int) -> None:
        if self.banks:
            self.lines += [f"set in 0x{v:X}", f"set addr {addr & 255}", f"set bank {addr >> 8}"]
        else:
            self.lines += [f"set in 0x{v:X}", f"set addr {addr}"]
        self.lines.append(f"set load {load}")
        if self.status:
            self.lines.append(f"set status {st}")

    def write(self, addr: int, v: int, st: int = 0, load: int = 1) -> None:
        """One clock cycle: `out` keeps the old value after the tick, shows the new one after."""
        k = self.key(addr, st)
        self._set(v, addr, st, load)
        self.lines += ["tick", f"expect out {self.fmt(self.mem.get(k))}", "tock"]
        if load:
            self.mem[k] = v
        self.lines.append(f"expect out {self.fmt(self.mem.get(k))}")

    def read(self, addr: int, st: int = 0) -> None:
        """Reading is combinational: `out` shows the cell at once, with no clock."""
        self._set(0, addr, st, 0)
        self.lines += ["eval", f"expect out {self.fmt(self.mem.get(self.key(addr, st)))}"]

    def note(self, text: str) -> None:
        self.lines.append(f"// {text}")

    def fill_rewrite_read(self, cells: list[tuple[int, int]], rng: random.Random) -> None:
        """Steps 1-3 for `cells`, a list of (addr, status)."""
        self.note("Fill: every cell once")
        for addr, st in cells:
            self.write(addr, rng.randrange(16), st)
        self.note("Rewrite: every cell again, each with a different value")
        for addr, st in cells:
            old = self.mem[self.key(addr, st)]
            self.write(addr, (old + 1 + rng.randrange(15)) & 15, st)
        self.note("Read everything back")
        for addr, st in cells:
            self.read(addr, st)

    def random_cycles(self, n: int, abits: int, rng: random.Random) -> None:
        self.note(f"{n} random cycles, load on about 60% of them")
        for _ in range(n):
            st = int(self.status and rng.random() < 0.3)
            self.write(rng.randrange(1 << abits), rng.randrange(16), st, int(rng.random() < 0.6))

    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


SHAPE = "fill every cell, rewrite each with a different value, read them all back"


def ram8(rng: random.Random) -> Gen:
    g = Gen(
        "RAM8",
        [
            f"RAM8: {SHAPE}, then 48 random cycles (seed {SEED}).",
            "Each write checks out after its tick (the old value) and after its tock.",
        ],
        status=False,
    )
    g.fill_rewrite_read([(a, 0) for a in range(8)], rng)
    g.random_cycles(48, 3, rng)
    return g


def ram64(rng: random.Random) -> Gen:
    g = Gen(
        "RAM64",
        [
            f"RAM64: {SHAPE}, then 64 random cycles (seed {SEED}).",
            "Each write checks out after its tick (the old value) and after its tock.",
        ],
        status=False,
    )
    g.fill_rewrite_read([(a, 0) for a in range(64)], rng)
    g.random_cycles(64, 6, rng)
    return g


def status_cells(chip_bits: int, rng: random.Random) -> list[tuple[int, int]]:
    """Every status character of the registers under `chip_bits` (0 for one 4002), named
    with random addr[2..3], which must not matter."""
    cells = []
    for r in range(4):
        for i in range(4):
            cells.append((chip_bits | r << 4 | rng.randrange(4) << 2 | i, 1))
    return cells


def ram4002(rng: random.Random) -> Gen:
    g = Gen(
        "RAM4002",
        [
            f"RAM4002: all 64 main and 16 status characters: {SHAPE};",
            "status characters named with addr[2..3] set to anything. Then 96 random",
            f"cycles (seed {SEED}). Each write checks out after its tick (the old value)",
            "and after its tock.",
        ],
        status=True,
    )
    g.fill_rewrite_read([(a, 0) for a in range(64)] + status_cells(0, rng), rng)
    g.random_cycles(96, 6, rng)
    return g


def rambank(rng: random.Random) -> Gen:
    g = Gen(
        "RAMBank",
        [
            f"RAMBank: all 256 main and 64 status characters of the four chips: {SHAPE};",
            "status characters named with addr[2..3] set to anything. Then 160 random",
            f"cycles (seed {SEED}). Each write checks out after its tick (the old value)",
            "and after its tock.",
        ],
        status=True,
    )
    cells = [(a, 0) for a in range(256)]
    for c in range(4):
        cells += status_cells(c << 6, rng)
    g.fill_rewrite_read(cells, rng)
    g.random_cycles(160, 8, rng)
    return g


# The main characters DataRAM writes in every bank: 0, each address bit alone, and 255. A bank
# whose address bit k is stuck or crossed puts the write to 1 << k somewhere else, which the
# read-back sees, because no two of them hold the same value.
DATARAM_MAIN = [0] + [1 << k for k in range(8)] + [255]
# Its status characters, one per chip, at addresses that are also main characters above, so a
# bank whose status pin is stuck at 0 overwrites a main character the read-back checks.
DATARAM_STATUS = [0, 64, 128, 255]


def dataram(rng: random.Random) -> Gen:
    g = Gen(
        "DataRAM",
        [
            "DataRAM: in each of the 8 banks, main characters 0, 1, 2, 4, ..., 128 and 255,",
            "and status characters at addresses 0, 64, 128 and 255, one in each chip. Fill",
            "them, rewrite each with a different value, read them all back. No two cells of",
            "a bank hold the same value, and no cell shares its value with the same cell in",
            f"another bank. Then 200 random cycles (seed {SEED}), most on those cells.",
            "Each write checks out after its tick (the old value) and after its tock.",
        ],
        status=True,
        banks=True,
    )
    cells = [(a, 0) for a in DATARAM_MAIN] + [(a, 1) for a in DATARAM_STATUS]
    # Value of cell i in bank b: perm[i] + b, distinct along a bank and across banks.
    perm = rng.sample(range(16), len(cells))
    shift = 1 + rng.randrange(15)
    g.note("Fill: the same cells in every bank")
    for b in range(8):
        for i, (addr, st) in enumerate(cells):
            g.write(b << 8 | addr, (perm[i] + b) & 15, st)
    g.note("Rewrite: every cell again, each with a different value")
    for b in range(8):
        for i, (addr, st) in enumerate(cells):
            g.write(b << 8 | addr, (perm[i] + b + shift) & 15, st)
    g.note("Read everything back")
    for b in range(8):
        for addr, st in cells:
            g.read(b << 8 | addr, st)
    g.note("200 random cycles, load on about 60% of them, 3 in 4 on the cells above")
    for _ in range(200):
        if rng.random() < 0.75:
            addr, st = rng.choice(cells)
        else:
            st = int(rng.random() < 0.3)
            addr = rng.randrange(256)
        g.write(rng.randrange(8) << 8 | addr, rng.randrange(16), st, int(rng.random() < 0.6))
    return g


def generate() -> dict[str, str]:
    """Every RAM level's .tst text, by chip name. One generator, so the order is fixed."""
    rng = random.Random(SEED)
    gens = (ram8(rng), ram64(rng), ram4002(rng), rambank(rng), dataram(rng))
    return {g.name: g.text() for g in gens}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: gen_ram_tst.py <output directory>", file=sys.stderr)
        return 2
    out = Path(argv[0])
    for name, text in generate().items():
        (out / f"{name}.tst").write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
