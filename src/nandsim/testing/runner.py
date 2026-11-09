"""Runs a `.tst` script against an implementation: the hidden reference or a player save.

Before simulating, the runner enforces the level's rules: the implementation must
keep the stub's interface, and its parts must be among those the level allows or
the player's exported chips.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from nandsim.hdl import ChipDef, HdlError, SourcePos, parse
from nandsim.netlist import ChipLibrary, Primitive, elaborate, net_names
from nandsim.paths import data_root, default_save_dir, exports_dir
from nandsim.sim import Simulator
from nandsim.testing.levels import Level, exported_chips, find_level, load_levels
from nandsim.testing.memory import CellKey, Memories, cell_key, parse_rom
from nandsim.testing.tst import (
    AttachStep,
    EvalStep,
    ExpectRamStep,
    ExpectStep,
    RamStep,
    RomStep,
    SetStep,
    TickStep,
    TockStep,
    TstScript,
    Value,
    parse_tst,
)


@dataclass(frozen=True)
class Impl:
    """Which implementation of the chips to test."""

    kind: Literal["reference", "save"]
    save_dir: Path | None = None

    def directory(self, root: Path | None = None) -> Path:
        if self.kind == "reference":
            return (root or data_root()) / "reference"
        return self.save_dir or default_save_dir()

    def library(self, root: Path | None = None) -> ChipLibrary:
        """The reference chips, or the player's saves followed by their exported chips."""
        d = self.directory(root)
        return ChipLibrary([d] if self.kind == "reference" else [d, exports_dir(d)])

    def exported(self, root: Path | None = None) -> list[str]:
        """The player's exported chips, which every level may use; none for the reference."""
        if self.kind == "reference":
            return []
        return exported_chips(exports_dir(self.directory(root)), load_levels(root))


@dataclass(frozen=True)
class Failure:
    pos: SourcePos
    message: str

    def __str__(self) -> str:
        return f"{self.pos}: {self.message}"


@dataclass
class TstResult:
    path: str
    chip: str
    checks: int = 0
    failures: list[Failure] = field(default_factory=list)
    error: HdlError | None = None

    @property
    def passed(self) -> bool:
        return self.error is None and not self.failures


def run_tst(path: Path, impl: Impl, root: Path | None = None) -> TstResult:
    """Parse and run one `.tst` file. Never raises for HDL or test errors."""
    try:
        script = parse_tst(path.read_text(), str(path))
    except HdlError as e:
        return TstResult(str(path), "?", error=e)
    level = find_level(script.chip, root)
    where = str(impl.directory(root))
    return run_script(script, impl.library(root), level, where, impl.exported(root))


def run_script(
    script: TstScript,
    lib: ChipLibrary,
    level: Level | None,
    where: str = "the library",
    exported: list[str] | None = None,
    base: Path | None = None,
) -> TstResult:
    """Run a parsed script with chips from `lib`, enforcing `level`'s rules if given.

    `exported` names the player's exported chips, allowed in any level besides its parts.
    `base` is where `rom <file>` looks for program files: by default the script's folder.
    """
    result = TstResult(script.file, script.chip)
    try:
        top = _resolve_top(script, lib, where)
        if level is not None:
            _check_level(top, level, exported or [])
        sim = Simulator(elaborate(top, lib))
        _run_steps(script, sim, result, base or Path(script.file).parent)
    except HdlError as e:
        result.error = e
    return result


def _resolve_top(script: TstScript, lib: ChipLibrary, where: str) -> ChipDef:
    if lib.find_file(script.chip) is None and script.chip not in lib.sources:
        raise HdlError(f"no implementation of '{script.chip}' found in {where}", script.chip_pos)
    top = lib.resolve_top(script.chip, script.chip_pos)
    if isinstance(top, Primitive):
        raise HdlError(f"'{script.chip}' is a primitive and cannot be tested", script.chip_pos)
    return top


def _signature(chip: ChipDef) -> str:
    def pins(ps: tuple) -> str:
        return ", ".join(p.name if p.width == 1 else f"{p.name}[{p.width}]" for p in ps)

    return f"IN {pins(chip.inputs)}; OUT {pins(chip.outputs)}"


def _check_level(top: ChipDef, level: Level, exported: list[str]) -> None:
    stub = parse(level.stub.read_text(), str(level.stub))
    if _signature(top) != _signature(stub):
        raise HdlError(
            f"{top.name} must keep the level's pins ({_signature(stub)}) "
            f"but declares {_signature(top)}",
            top.pos,
        )
    allowed = [*level.parts, *(n for n in exported if n not in level.parts)]
    for part in top.parts:
        if part.chip not in allowed:
            raise HdlError(
                f"'{part.chip}' is not allowed in this level; {top.name} may use: "
                f"{', '.join(allowed)}",
                part.pos,
            )


def _format(value: int | None, bits: list[int | None], like: Value) -> str:
    width = len(bits)
    if like.base == 2:
        return "0b" + "".join("x" if b is None else str(b) for b in reversed(bits))
    if value is None:
        return "undefined"
    if like.base == 16:
        return f"0x{value:0{(width + 3) // 4}X}"
    return str(value)


def _when(sim: Simulator) -> str:
    """The clock time of a check, e.g. `cycle 3` or `cycle 3 after tick`."""
    return f"cycle {sim.cycle}" + (" after tick" if sim.mid_cycle else "")


def _unsettled(sim: Simulator, names: dict[int, str]) -> str:
    """`a loop didn't settle: x, y`, naming up to three of the nets it left undefined."""
    if not names:
        names.update(net_names(sim.netlist))  # walks every wire: only once, on a failure
    shown = sorted({names.get(int(n), f"net {n}") for n in sim.unsettled})
    more = f" and {len(shown) - 3} more" if len(shown) > 3 else ""
    return f"a loop didn't settle: {', '.join(shown[:3])}{more}"


def _cell(bank: Value, addr: Value, status: bool) -> CellKey:
    return cell_key(bank.encode(3, "bank"), addr.encode(8, "addr"), status)


def _rom_step(step: RomStep, mem: Memories, base: Path) -> None:
    assert mem.rom is not None  # the parser checks the attach comes first
    if step.file is not None:
        path = base / step.file
        try:
            text = path.read_text()
        except OSError as e:
            raise HdlError(
                f"can't read program file '{step.file}': {e.strerror}", step.pos
            ) from None
        mem.rom.write(0, parse_rom(text, str(path)), step.pos)
    else:
        assert step.addr is not None
        values = [v.encode(8, "rom") for v in step.data]
        mem.rom.write(step.addr.encode(12, "addr"), values, step.pos)


def _run_steps(script: TstScript, sim: Simulator, result: TstResult, base: Path) -> None:
    nl = sim.netlist
    names: dict[int, str] = {}  # filled on the first failure that needs them
    clocked = any(isinstance(s, TickStep | TockStep) for s in script.steps)
    mem = Memories(sim, script.chip)
    for step in script.steps:
        if isinstance(step, SetStep):
            if step.pin not in nl.inputs:
                hint = ": use 'expect' to check outputs" if step.pin in nl.outputs else ""
                raise HdlError(f"'{step.pin}' is not an input of {script.chip}{hint}", step.pos)
            driver = mem.driver(step.pin)
            if driver is not None:
                raise HdlError(f"'{step.pin}' is driven by the {driver}: it can't be set", step.pos)
            sim.set(step.pin, step.value.encode(len(nl.inputs[step.pin]), step.pin))
        elif isinstance(step, EvalStep):
            if mem:
                mem.settle(step.pos)
            else:
                sim.eval()
        elif isinstance(step, TickStep):
            problem = mem.before_tick(step.pos) if mem else None
            if problem is not None:
                result.failures.append(Failure(step.pos, f"{problem} ({_when(sim)})"))
            sim.tick()
            if mem:
                mem.after_tick(step.pos)
        elif isinstance(step, TockStep):
            sim.tock()
            if mem:
                mem.after_tock(step.pos)
        elif isinstance(step, AttachStep):
            links = {k.memory_pin: (k.chip_pin, k.pos) for k in step.links}
            mem.attach(step.kind, links)
        elif isinstance(step, RomStep):
            _rom_step(step, mem, base)
        elif isinstance(step, RamStep):
            assert mem.ram is not None  # the parser checks the attach comes first
            mem.ram.cells[_cell(step.bank, step.addr, step.status)] = step.value.encode(4, "ram")
        elif isinstance(step, ExpectRamStep):
            assert mem.ram is not None
            result.checks += 1
            if step.value.number is None:
                continue
            want = step.value.encode(4, "ram")
            got = mem.ram.cells.get(_cell(step.bank, step.addr, step.status))
            if got != want:
                bits = [None] * 4 if got is None else [(got >> i) & 1 for i in range(4)]
                shown = _format(got, bits, step.value)
                word = "ramstatus" if step.status else "ram"
                failure = (
                    f"{word} {step.bank.text} {step.addr.text}: expected {step.value.text}, "
                    f"got {shown} ({_when(sim)})"
                )
                result.failures.append(Failure(step.pos, failure))
        elif isinstance(step, ExpectStep):
            nets = nl.outputs.get(step.pin) or nl.inputs.get(step.pin)
            if nets is None:
                raise HdlError(f"'{step.pin}' is not a pin of {script.chip}", step.pos)
            result.checks += 1
            if step.value.number is None:
                continue
            want = step.value.encode(len(nets), step.pin)
            got = sim.get(step.pin)
            if got != want:
                shown = _format(got, sim.get_bits(step.pin), step.value)
                notes = [f"inputs {step.context}"] if step.context else []
                if clocked:
                    notes.append(_when(sim))
                if got is None and len(sim.unsettled):
                    notes.append(_unsettled(sim, names))
                where = f" ({', '.join(notes)})" if notes else ""
                result.failures.append(
                    Failure(step.pos, f"{step.pin}: expected {step.value.text}, got {shown}{where}")
                )
