"""Levelization: orders combinational gates so each level depends only on earlier ones.

Runs once per elaboration, vectorized too: a DataRAM has 180k gates, and a Python
loop per gate cost most of its compile time. The result is a list of per-level
index arrays that the engine evaluates with vectorized numpy.
A gate set that cannot be ordered is a combinational loop, reported by wire name.
"""

from __future__ import annotations

import numpy as np

from nandsim.hdl import HdlError, SourcePos
from nandsim.netlist.netlist import LevelOp, Netlist
from nandsim.netlist.primitives import Primitive


def levelize(
    netlist: Netlist,
    primitives: dict[str, Primitive],
    gate_pos: dict[str, list[SourcePos]],
    top_pos: SourcePos,
) -> list[list[LevelOp]]:
    # Global gate ids: kinds in table order, gates in creation order.
    kinds = [k for k in netlist.gates if not primitives[k].sequential]
    counts = [netlist.gates[k].count for k in kinds]
    offsets = np.cumsum([0, *counts])
    n = int(offsets[-1])
    if n == 0:
        return []

    driver = np.full(netlist.num_nets, -1, dtype=np.int64)
    for k, off in zip(kinds, offsets, strict=False):
        g = netlist.gates[k]
        for col in g.outputs:
            driver[col] = np.arange(off, off + g.count)

    # Dependency edges src -> dst: gate dst reads a net that gate src drives.
    srcs: list[np.ndarray] = []
    dsts: list[np.ndarray] = []
    for k, off in zip(kinds, offsets, strict=False):
        g = netlist.gates[k]
        ids = np.arange(off, off + g.count, dtype=np.int64)
        for col in g.inputs:
            d = driver[col]
            used = d >= 0
            srcs.append(d[used])
            dsts.append(ids[used])
    src = np.concatenate(srcs) if srcs else np.zeros(0, np.int64)
    dst = np.concatenate(dsts) if dsts else np.zeros(0, np.int64)

    # Kahn's algorithm one frontier at a time: round r finds every gate whose
    # longest path from an input is r, so each round is exactly one level.
    order = np.argsort(src, kind="stable")
    users = dst[order]
    starts = np.searchsorted(src[order], np.arange(n + 1))
    pending = np.bincount(dst, minlength=n)
    level = np.full(n, -1, dtype=np.int64)
    frontier = np.flatnonzero(pending == 0)
    r = 0
    while len(frontier):
        level[frontier] = r
        first, deg = starts[frontier], starts[frontier + 1] - starts[frontier]
        total = int(deg.sum())
        if total == 0:
            break
        # Positions of every user edge of the frontier, without a Python loop.
        base = np.repeat(first - np.cumsum(deg) + deg, deg)
        hit = users[base + np.arange(total)]
        pending -= np.bincount(hit, minlength=n)
        hit = np.unique(hit)
        frontier = hit[pending[hit] == 0]
        r += 1

    if (level < 0).any():
        deps: list[list[int]] = [[] for _ in range(n)]
        for a, b in zip(src.tolist(), dst.tolist(), strict=True):
            deps[b].append(a)
        owners = [(k, i) for k, c in zip(kinds, counts, strict=True) for i in range(c)]
        # A gate never reached still waits on a driver: pending > 0 marks the loop.
        _report_loop(netlist, owners, deps, pending.tolist(), driver, gate_pos, top_pos)

    result: list[list[LevelOp]] = [[] for _ in range(int(level.max()) + 1)]
    for k, off, count in zip(kinds, offsets, counts, strict=False):
        lv = level[off : off + count]
        by_level = np.argsort(lv, kind="stable")  # gates of one level stay in creation order
        bounds = np.searchsorted(lv[by_level], np.arange(len(result) + 1))
        arrays = netlist.gates[k]
        for L in range(len(result)):
            idx = by_level[bounds[L] : bounds[L + 1]]
            if len(idx):
                result[L].append(
                    LevelOp(k, [c[idx] for c in arrays.inputs], [c[idx] for c in arrays.outputs])
                )
    return result


def _net_names(netlist: Netlist) -> dict[int, str]:
    """Best human name for each net: the shallowest wire path, relative to the top chip."""
    names: dict[int, tuple[int, str]] = {}
    prefix = netlist.top + "/"
    wires = netlist.wires
    walk = getattr(wires, "walk", None)  # elaboration's lazy map walks its tree faster
    items = walk() if walk is not None else wires.items()
    for path, nets in items:
        nets = [int(n) for n in nets]
        short = path[len(prefix) :] if path.startswith(prefix) else path
        depth = short.count("/")
        for bit, net in enumerate(nets):
            label = f"{short}[{bit}]" if len(nets) > 1 else short
            if net not in names or (depth, len(label)) < (names[net][0], len(names[net][1])):
                names[net] = (depth, label)
    return {net: label for net, (_, label) in names.items()}


def _report_loop(
    netlist: Netlist,
    owners: list[tuple[str, int]],
    deps: list[list[int]],
    pending: list[int],
    driver: np.ndarray,
    gate_pos: dict[str, list[SourcePos]],
    top_pos: SourcePos,
) -> None:
    stuck = {g for g in range(len(owners)) if pending[g] > 0}
    # Walk backwards from a stuck gate through stuck drivers until a gate repeats.
    start = min(stuck)
    order: list[int] = []
    seen: dict[int, int] = {}
    g = start
    while g not in seen:
        seen[g] = len(order)
        order.append(g)
        g = next(d for d in deps[g] if d in stuck)
    cycle = order[seen[g] :]
    cycle.reverse()  # signal-flow order: driver before user
    names = _net_names(netlist)
    labels = []
    for gate in cycle:
        k, i = owners[gate]
        net = int(netlist.gates[k].outputs[0][i])
        labels.append(names.get(net, f"net {net}"))
    labels.append(labels[0])
    k, i = owners[cycle[0]]
    pos = gate_pos.get(k, [top_pos])[i] if k in gate_pos else top_pos
    raise HdlError(
        "combinational loop (a signal depends on itself without a DFF): " + " -> ".join(labels),
        pos,
    )
