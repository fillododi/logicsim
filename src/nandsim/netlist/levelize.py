"""Levelization: orders combinational gates so each level depends only on earlier ones.

Runs once per elaboration (Python loops are fine here); the result is a list of
per-level index arrays that the engine evaluates with vectorized numpy.
A gate set that cannot be ordered is a combinational loop, reported by wire name.
"""

from __future__ import annotations

from collections import deque

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
    owners: list[tuple[str, int]] = []
    for k in kinds:
        owners += [(k, i) for i in range(netlist.gates[k].count)]
    n = len(owners)

    driver = np.full(netlist.num_nets, -1, dtype=np.int64)
    offset = 0
    for k in kinds:
        g = netlist.gates[k]
        for col in g.outputs:
            driver[col] = np.arange(offset, offset + g.count)
        offset += g.count

    deps: list[list[int]] = [[] for _ in range(n)]
    gid = 0
    for k in kinds:
        g = netlist.gates[k]
        ins = np.stack(g.inputs, axis=1) if g.inputs else np.zeros((g.count, 0), np.int64)
        drv = driver[ins]
        for row in drv:
            deps[gid] = [int(d) for d in row if d >= 0]
            gid += 1

    users: list[list[int]] = [[] for _ in range(n)]
    pending = [0] * n
    for g, ds in enumerate(deps):
        pending[g] = len(ds)
        for d in ds:
            users[d].append(g)

    level = [0] * n
    queue = deque(g for g in range(n) if pending[g] == 0)
    done = 0
    while queue:
        g = queue.popleft()
        done += 1
        for u in users[g]:
            level[u] = max(level[u], level[g] + 1)
            pending[u] -= 1
            if pending[u] == 0:
                queue.append(u)

    if done < n:
        _report_loop(netlist, owners, deps, pending, driver, gate_pos, top_pos)

    if n == 0:
        return []
    by_level: list[dict[str, list[int]]] = [{} for _ in range(max(level) + 1)]
    for g, (k, i) in enumerate(owners):
        by_level[level[g]].setdefault(k, []).append(i)
    result: list[list[LevelOp]] = []
    for groups in by_level:
        ops = []
        for k, idx_list in groups.items():
            idx = np.asarray(idx_list, dtype=np.int64)
            arrays = netlist.gates[k]
            ops.append(
                LevelOp(k, [c[idx] for c in arrays.inputs], [c[idx] for c in arrays.outputs])
            )
        result.append(ops)
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
