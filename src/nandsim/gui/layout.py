"""Automatic layered layout of a `ChipView`. Pure Python, no pygame.

A simplified Sugiyama layout:

1. Break part-level cycles (feedback) so the rest is acyclic.
2. Assign layers: inputs in column 0, each part one column right of everything
   that feeds it, outputs in the last column.
3. Insert dummy nodes on wires that skip columns, so they get their own lanes.
4. Order each column with barycenter sweeps to reduce crossings.
5. Place nodes (y aligned towards their sources, x by column widths).
6. Route wires orthogonally; vertical runs get their own track in the channel
   between two columns, shared only by wires of the same source (fan-out).

Coordinates are in "view units" (pixels at zoom 1). Text width is estimated
with `Style.char_w`, which the renderer's monospace font should match.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from nandsim.gui.model import ChipView, Edge, Endpoint

NodeKey = tuple[str, str | int]  # ("in", name) | ("out", name) | ("part", index) | ("dummy", n)
Point = tuple[float, float]


@dataclass(frozen=True)
class Style:
    pitch: float = 24  # vertical distance between pins
    pad: float = 10  # padding above and below a part's pins
    char_w: float = 8  # estimated width of one monospace character
    min_part_w: float = 72
    min_io_w: float = 56
    row_gap: float = 28  # vertical gap between nodes in a column
    track: float = 10  # distance between vertical wire tracks
    min_channel: float = 48  # minimum gap between columns
    margin: float = 24


@dataclass
class Box:
    key: NodeKey
    x: float
    y: float
    w: float
    h: float
    layer: int
    anchors: dict[tuple[str, str], Point] = field(default_factory=dict)  # (side, pin)

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h


@dataclass
class Route:
    edge: Edge
    points: list[Point]  # empty for constants
    feedback: bool = False
    label_at: Point | None = None  # where a constant's value is written


@dataclass
class Layout:
    boxes: dict[NodeKey, Box]
    routes: list[Route]
    width: float
    height: float
    layers: list[list[NodeKey]]


def _node(e: Endpoint) -> NodeKey:
    if e.kind == "input":
        return ("in", e.pin)
    if e.kind == "output":
        return ("out", e.pin)
    assert e.part is not None
    return ("part", e.part)


def layout(view: ChipView, style: Style | None = None) -> Layout:
    st = style or Style()
    wired = [e for e in view.edges if e.src.kind != "const"]

    # 1-2. Layers, with part-level cycles broken by DFS back edges.
    succ: dict[int, list[int]] = {p.index: [] for p in view.parts}
    for e in wired:
        if e.src.kind == "part" and e.dst.kind == "part":
            assert e.src.part is not None and e.dst.part is not None
            succ[e.src.part].append(e.dst.part)
    back: set[tuple[int, int]] = set()
    state: dict[int, int] = {}  # 1 = on stack, 2 = done

    def dfs(u: int) -> None:
        state[u] = 1
        for v in succ[u]:
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2

    for p in view.parts:
        if p.index not in state:
            dfs(p.index)

    def is_feedback(e: Edge) -> bool:
        return e.src.kind == "part" and e.dst.kind == "part" and (e.src.part, e.dst.part) in back

    layer: dict[NodeKey, int] = {("in", p.name): 0 for p in view.inputs}
    preds: dict[int, list[int]] = {p.index: [] for p in view.parts}
    for e in wired:
        if e.dst.kind == "part" and e.src.kind == "part" and not is_feedback(e):
            assert e.src.part is not None and e.dst.part is not None
            preds[e.dst.part].append(e.src.part)

    memo: dict[int, int] = {}

    def part_layer(i: int) -> int:
        if i not in memo:
            memo[i] = 1 + max((part_layer(j) for j in preds[i]), default=0)
        return memo[i]

    for p in view.parts:
        layer[("part", p.index)] = part_layer(p.index)
    last = max((layer[("part", p.index)] for p in view.parts), default=0) + 1
    for p in view.outputs:
        layer[("out", p.name)] = last

    # 3. Chains: each forward wire becomes src -> dummy... -> dst, one hop per column.
    columns: list[list[NodeKey]] = [[] for _ in range(last + 1)]
    for p in view.inputs:
        columns[0].append(("in", p.name))
    for p in view.parts:
        columns[layer[("part", p.index)]].append(("part", p.index))
    for p in view.outputs:
        columns[last].append(("out", p.name))

    chains: list[tuple[Edge, list[NodeKey]]] = []
    hops: list[tuple[NodeKey, NodeKey, float, float]] = []  # (u, v, u_pin_frac, v_pin_frac)
    dummy = 0
    for e in wired:
        if is_feedback(e):
            continue
        u, v = _node(e.src), _node(e.dst)
        chain = [u]
        for col in range(layer[u] + 1, layer[v]):
            d: NodeKey = ("dummy", dummy)
            dummy += 1
            layer[d] = col
            columns[col].append(d)
            chain.append(d)
        chain.append(v)
        chains.append((e, chain))
        uf = _pin_frac(view, e.src, "out")
        vf = _pin_frac(view, e.dst, "in")
        for k in range(len(chain) - 1):
            hops.append(
                (chain[k], chain[k + 1], uf if k == 0 else 0.5, vf if k == len(chain) - 2 else 0.5)
            )

    # 4. Ordering by barycenter sweeps; inputs and outputs keep their declared order.
    pos: dict[NodeKey, float] = {}

    def index_positions() -> None:
        for col in columns:
            for i, n in enumerate(col):
                pos[n] = float(i)

    index_positions()
    by_dst: dict[NodeKey, list[tuple[NodeKey, float]]] = {}
    by_src: dict[NodeKey, list[tuple[NodeKey, float]]] = {}
    for u, v, uf, vf in hops:
        by_dst.setdefault(v, []).append((u, uf))
        by_src.setdefault(u, []).append((v, vf))

    def sweep(col: list[NodeKey], nbrs: dict[NodeKey, list[tuple[NodeKey, float]]]) -> None:
        def key(n: NodeKey) -> tuple[float, float]:
            ns = nbrs.get(n)
            if not ns:
                return (pos[n], pos[n])
            return (sum(pos[m] + f for m, f in ns) / len(ns), pos[n])

        col.sort(key=key)
        for i, n in enumerate(col):
            pos[n] = float(i)

    best = [list(c) for c in columns]
    best_x = _crossings_by_order(hops, pos, layer)
    for _ in range(12):
        for col in columns[1:last]:
            sweep(col, by_dst)
        for col in reversed(columns[1:last]):
            sweep(col, by_src)
        x = _crossings_by_order(hops, pos, layer)
        if x < best_x:
            best, best_x = [list(c) for c in columns], x
        if best_x == 0:
            break
    columns = best
    index_positions()

    # 5. Node sizes and placement.
    boxes: dict[NodeKey, Box] = {}
    parts = {p.index: p for p in view.parts}
    for n, lay in layer.items():
        kind, ident = n
        if kind == "part":
            p = parts[int(ident)]
            rows = max(len(p.inputs), len(p.outputs), 1)
            names_w = max((len(_pin_label(q.name, q.width)) for q in p.inputs), default=0) + max(
                (len(_pin_label(q.name, q.width)) for q in p.outputs), default=0
            )
            w = max(st.min_part_w, st.char_w * (len(p.label) + 4), st.char_w * (names_w + 4))
            boxes[n] = Box(n, 0, 0, w, rows * st.pitch + 2 * st.pad, lay)
        elif kind in ("in", "out"):
            pins = view.inputs if kind == "in" else view.outputs
            q = next(q for q in pins if q.name == ident)
            w = max(st.min_io_w, st.char_w * (len(_pin_label(q.name, q.width)) + 3))
            boxes[n] = Box(n, 0, 0, w, st.pitch, lay)
        else:
            boxes[n] = Box(n, 0, 0, 0, st.pitch, lay)

    def anchor_y(n: NodeKey, frac: float) -> float:
        b = boxes[n]
        if n[0] == "part":
            rows = (b.h - 2 * st.pad) / st.pitch
            return b.y + st.pad + frac * rows * st.pitch
        return b.y + b.h / 2

    def stack(col: list[NodeKey], want: dict[NodeKey, float]) -> None:
        """Place nodes in order, as close to their wanted y as overlap allows."""
        y = 0.0
        for n in col:
            b = boxes[n]
            b.y = max(y, want.get(n, y))
            y = b.bottom + st.row_gap
        y = col and boxes[col[-1]].bottom or 0.0
        for n in reversed(col):  # pull back up where the pass above pushed too far
            b = boxes[n]
            target = want.get(n, b.y)
            limit = y - b.h
            if b.y > target:
                b.y = max(target, min(b.y, limit))
            y = b.y - st.row_gap

    for col in columns:
        stack(col, {})
    for _ in range(3):
        for c in range(1, len(columns)):
            want: dict[NodeKey, float] = {}
            for n in columns[c]:
                ins = by_dst.get(n, [])
                if ins:
                    ys = [anchor_y(m, f) for m, f in ins]
                    own = _first_in_frac(view, n)
                    want[n] = sum(ys) / len(ys) - (anchor_y(n, own) - boxes[n].y)
            stack(columns[c], want)
    top = min((b.y for b in boxes.values()), default=0.0)
    for b in boxes.values():
        b.y += st.margin - top

    # 6a. Channel tracks: one per (source group) that needs a vertical run.
    fb_edges = [e for e in wired if is_feedback(e)]
    channel_groups: list[dict[tuple, list[float]]] = [{} for _ in range(len(columns))]

    def group_of(e: Edge, k: int) -> tuple:
        # One trunk per source pin: slices of the same bus branch off a shared track.
        return (e.src.kind, e.src.part, e.src.pin, k if k else 0, k > 0 and id(e))

    for e, chain in chains:
        for k in range(len(chain) - 1):
            u, v = chain[k], chain[k + 1]
            y1 = anchor_y(u, _pin_frac(view, e.src, "out") if k == 0 else 0.5)
            y2 = anchor_y(v, _pin_frac(view, e.dst, "in") if k == len(chain) - 2 else 0.5)
            if abs(y1 - y2) > 1e-6:
                channel_groups[layer[u]].setdefault(group_of(e, k), []).extend([y1, y2])
    for i, e in enumerate(fb_edges):
        u, v = _node(e.src), _node(e.dst)
        channel_groups[layer[u]][("fb-out", i)] = [0.0]
        channel_groups[layer[v] - 1][("fb-in", i)] = [0.0]

    tracks: list[dict[tuple, int]] = []
    for groups in channel_groups:
        order = sorted(groups, key=lambda g: (min(groups[g]), max(groups[g]), str(g)))
        tracks.append({g: i for i, g in enumerate(order)})

    # 5b. x positions: column widths plus channels sized for their tracks.
    x = st.margin
    col_x: list[float] = []
    chan_x: list[float] = []
    for c, col in enumerate(columns):
        width = max((boxes[n].w for n in col), default=0.0)
        col_x.append(x)
        for n in col:
            b = boxes[n]
            b.x = x + (width - b.w) / 2 if n[0] in ("part", "dummy") else x
            if n[0] == "out":
                b.x = x
        x += width
        chan_x.append(x)
        x += max(st.min_channel, (len(tracks[c]) + 1) * st.track + 2 * st.track)

    for b in boxes.values():
        kind, ident = b.key
        if kind == "in":
            b.anchors[("out", str(ident))] = (b.right, b.y + b.h / 2)
        elif kind == "out":
            b.anchors[("in", str(ident))] = (b.x, b.y + b.h / 2)
        elif kind == "part":
            p = parts[int(ident)]
            for i, q in enumerate(p.inputs):
                b.anchors[("in", q.name)] = (b.x, b.y + st.pad + (i + 0.5) * st.pitch)
            for i, q in enumerate(p.outputs):
                b.anchors[("out", q.name)] = (b.right, b.y + st.pad + (i + 0.5) * st.pitch)
        else:
            b.anchors[("in", "")] = (b.x, b.y + b.h / 2)
            b.anchors[("out", "")] = (b.right, b.y + b.h / 2)

    def anchor(n: NodeKey, side: str, e: Endpoint | None) -> Point:
        b = boxes[n]
        pin = "" if n[0] == "dummy" else (e.pin if e is not None else "")
        return b.anchors[(side, pin)]

    def track_x(c: int, g: tuple) -> float:
        return chan_x[c] + st.track * (1.5 + tracks[c][g])

    # 6b. Routes.
    routes: list[Route] = []
    for e, chain in chains:
        pts: list[Point] = []
        for k in range(len(chain) - 1):
            u, v = chain[k], chain[k + 1]
            p1 = anchor(u, "out", e.src if k == 0 else None)
            p2 = anchor(v, "in", e.dst if k == len(chain) - 2 else None)
            if not pts:
                pts.append(p1)
            elif pts[-1] != p1:
                pts.append(p1)  # straight through a dummy column
            if abs(p1[1] - p2[1]) > 1e-6:
                tx = track_x(layer[u], group_of(e, k))
                pts += [(tx, p1[1]), (tx, p2[1])]
            pts.append(p2)
        routes.append(Route(e, _simplify(pts)))

    lane_top = min((b.y for b in boxes.values()), default=st.margin)
    for i, e in enumerate(fb_edges):
        u, v = _node(e.src), _node(e.dst)
        p1 = anchor(u, "out", e.src)
        p2 = anchor(v, "in", e.dst)
        lane = lane_top - st.track * (2 + i)
        x1 = track_x(layer[u], ("fb-out", i))
        x2 = track_x(layer[v] - 1, ("fb-in", i))
        pts = [p1, (x1, p1[1]), (x1, lane), (x2, lane), (x2, p2[1]), p2]
        routes.append(Route(e, _simplify(pts), feedback=True))

    for e in view.edges:
        if e.src.kind == "const":
            p = anchor(_node(e.dst), "in", e.dst)
            routes.append(Route(e, [], label_at=(p[0] - st.char_w * (len(e.label) + 1), p[1])))

    # Shift everything down if feedback lanes went above the top margin.
    min_y = min([b.y for b in boxes.values()] + [y for r in routes for _, y in r.points] + [0.0])
    if min_y < st.margin:
        dy = st.margin - min_y
        for b in boxes.values():
            b.y += dy
            b.anchors = {k: (ax, ay + dy) for k, (ax, ay) in b.anchors.items()}
        for r in routes:
            r.points = [(px, py + dy) for px, py in r.points]
            if r.label_at:
                r.label_at = (r.label_at[0], r.label_at[1] + dy)

    width = max((b.right for b in boxes.values()), default=0.0) + st.margin
    height = max([b.bottom for b in boxes.values()] + [0.0]) + st.margin
    return Layout(boxes, routes, width, height, columns)


# ---- helpers -------------------------------------------------------------


def _pin_label(name: str, width: int) -> str:
    return name if width == 1 else f"{name}[{width}]"


def _pin_frac(view: ChipView, e: Endpoint, side: str) -> float:
    """Where on its node the pin sits, as a fraction of the node's pin rows."""
    if e.kind != "part" or e.part is None:
        return 0.5
    p = view.part(e.part)
    pins = p.outputs if side == "out" else p.inputs
    rows = max(len(p.inputs), len(p.outputs), 1)
    i = next((k for k, q in enumerate(pins) if q.name == e.pin), 0)
    return (i + 0.5) / rows


def _first_in_frac(view: ChipView, n: NodeKey) -> float:
    if n[0] != "part":
        return 0.5
    p = view.part(int(n[1]))
    rows = max(len(p.inputs), len(p.outputs), 1)
    return (len(p.inputs) / 2) / rows


def _crossings_by_order(
    hops: list[tuple[NodeKey, NodeKey, float, float]],
    pos: dict[NodeKey, float],
    layer: dict[NodeKey, int],
) -> int:
    """Crossings implied by the current column orders (between adjacent columns)."""
    by_layer: dict[int, list[tuple[float, float]]] = {}
    for u, v, uf, vf in hops:
        by_layer.setdefault(layer[u], []).append((pos[u] + uf, pos[v] + vf))
    total = 0
    for segs in by_layer.values():
        segs.sort()
        for i in range(len(segs)):
            for j in range(i + 1, len(segs)):
                if (segs[i][0] - segs[j][0]) * (segs[i][1] - segs[j][1]) < 0:
                    total += 1
    return total


def _simplify(pts: list[Point]) -> list[Point]:
    """Drop repeated and collinear middle points."""
    out: list[Point] = []
    for p in pts:
        if out and out[-1] == p:
            continue
        if len(out) >= 2:
            a, b = out[-2], out[-1]
            if (a[0] == b[0] == p[0]) or (a[1] == b[1] == p[1]):
                out[-1] = p
                continue
        out.append(p)
    return out


def crossings(lay: Layout) -> int:
    """Count where wires of different sources cross (horizontal over vertical)."""
    segs: list[tuple[float, float, float, float, str]] = []
    for r in lay.routes:
        g = f"{r.edge.src.kind}:{r.edge.src.part}:{r.edge.src.pin}"
        for (x1, y1), (x2, y2) in zip(r.points, r.points[1:], strict=False):
            segs.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2), g))
    hs = [s for s in segs if s[1] == s[3] and s[0] != s[2]]
    vs = [s for s in segs if s[0] == s[2] and s[1] != s[3]]
    n = 0
    for hx1, hy, hx2, _, hg in hs:
        for vx, vy1, _, vy2, vg in vs:
            if hg != vg and hx1 < vx < hx2 and vy1 < hy < vy2:
                n += 1
    return n
