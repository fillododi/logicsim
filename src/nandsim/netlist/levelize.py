"""Levelization: orders combinational gates so each level depends only on earlier ones.

Runs once per elaboration, vectorized too: a DataRAM has 180k gates, and a Python
loop per gate cost most of its compile time. The result is a list of levels of
index arrays that the engine evaluates with vectorized numpy.

Feedback loops (a latch made of two NANDs, say) can't be ordered. When some gates
are left over, their strongly connected components are found, and the graph of
components, which has no cycles, is levelized the same way. Each level then splits
into a plain level, evaluated once, and a loop level holding the gates of its
loops, which the engine evaluates in rounds until it settles.
"""

from __future__ import annotations

import numpy as np

from nandsim.netlist.netlist import Level, LevelOp, Netlist
from nandsim.netlist.primitives import Primitive


def levelize(netlist: Netlist, primitives: dict[str, Primitive]) -> list[Level]:
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

    level = _longest_paths(n, src, dst)
    loop = np.full(n, -1, dtype=np.int64)  # component id of each gate inside a loop
    if (level < 0).any():
        comp, in_loop = _components(n, src, dst, level < 0)
        cs, cd = comp[src], comp[dst]
        cross = cs != cd
        clevel = _longest_paths(int(comp.max()) + 1, cs[cross], cd[cross])
        assert (clevel >= 0).all(), "the graph of components has no cycles"
        level = clevel[comp]
        loop[in_loop] = comp[in_loop]

    # Level r becomes step 2r (its plain gates) and step 2r+1 (its loops), if present.
    step = 2 * level + (loop >= 0)
    used = np.unique(step)
    pos = np.searchsorted(used, step)
    local, loops = _local_loop_ids(pos, loop, len(used))

    result = [Level([], int(loops[s])) for s in range(len(used))]
    for k, off, count in zip(kinds, offsets, counts, strict=False):
        lv = pos[off : off + count]
        by_level = np.argsort(lv, kind="stable")  # gates of one level stay in creation order
        bounds = np.searchsorted(lv[by_level], np.arange(len(result) + 1))
        arrays = netlist.gates[k]
        for L, out in enumerate(result):
            idx = by_level[bounds[L] : bounds[L + 1]]
            if len(idx):
                out.ops.append(
                    LevelOp(
                        k,
                        [c[idx] for c in arrays.inputs],
                        [c[idx] for c in arrays.outputs],
                        local[off + idx] if out.is_loop else None,
                    )
                )
    return result


def _longest_paths(n: int, src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """Each node's longest path from a node with no inputs; -1 if a cycle blocks it.

    Kahn's algorithm one frontier at a time: round r finds every node whose longest
    path is r, so each round is exactly one level.
    """
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
    return level


def _components(
    n: int, src: np.ndarray, dst: np.ndarray, stuck: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Component id of every gate, and which gates sit in a feedback loop.

    Only the gates Kahn's algorithm left over can be in a loop, so Tarjan's algorithm
    (a Python loop, unlike the rest) runs on those alone. Every other gate is a
    component of its own. A loop is a component of two or more gates, or one gate
    that reads its own output.
    """
    nodes = np.flatnonzero(stuck)
    m = len(nodes)
    local = np.full(n, -1, dtype=np.int64)
    local[nodes] = np.arange(m)
    both = stuck[src] & stuck[dst]
    ls, ld = local[src[both]], local[dst[both]]
    order = np.argsort(ls, kind="stable")
    adj = ld[order].tolist()
    starts = np.searchsorted(ls[order], np.arange(m + 1)).tolist()

    index = [-1] * m
    low = [0] * m
    on_stack = [False] * m
    stack: list[int] = []
    scc = [-1] * m
    count = 0
    seen = 0
    for root in range(m):
        if index[root] >= 0:
            continue
        index[root] = low[root] = seen
        seen += 1
        stack.append(root)
        on_stack[root] = True
        work = [(root, starts[root])]
        while work:
            v, e = work[-1]
            if e < starts[v + 1]:
                work[-1] = (v, e + 1)
                w = adj[e]
                if index[w] < 0:
                    index[w] = low[w] = seen
                    seen += 1
                    stack.append(w)
                    on_stack[w] = True
                    work.append((w, starts[w]))
                elif on_stack[w] and index[w] < low[v]:
                    low[v] = index[w]
                continue
            work.pop()
            if work:
                u = work[-1][0]
                if low[v] < low[u]:
                    low[u] = low[v]
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc[w] = count
                    if w == v:
                        break
                count += 1

    free = np.flatnonzero(~stuck)
    comp = np.empty(n, dtype=np.int64)
    comp[free] = np.arange(len(free))
    sub = np.asarray(scc, dtype=np.int64)
    comp[nodes] = len(free) + sub
    sizes = np.bincount(sub, minlength=count)
    loopy = sizes > 1
    loopy[sub[ls[ls == ld]]] = True  # a gate that reads its own output
    in_loop = np.zeros(n, dtype=bool)
    in_loop[nodes] = loopy[sub]
    return comp, in_loop


def _local_loop_ids(pos: np.ndarray, loop: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Loop ids renumbered from 0 within each step, and each step's loop count."""
    local = np.full(len(pos), -1, dtype=np.int64)
    gates = np.flatnonzero(loop >= 0)
    if not len(gates):
        return local, np.zeros(steps, dtype=np.int64)
    width = int(loop.max()) + 1
    keys, inv = np.unique(pos[gates] * width + loop[gates], return_inverse=True)
    step_of = keys // width  # sorted, so each step's loops are contiguous
    first = np.searchsorted(step_of, step_of)
    local[gates] = inv - first[inv]
    return local, np.bincount(step_of, minlength=steps)


def net_names(netlist: Netlist) -> dict[int, str]:
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
