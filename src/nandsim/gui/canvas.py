"""Draws one level of a chip: wires coloured by value, parts, pins and bus values.

The net under the mouse (a wire or a chip pin) is highlighted everywhere it goes,
and dots mark where a wire branches.
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from nandsim.gui import theme
from nandsim.gui.camera import Camera
from nandsim.gui.layout import NodeKey, Route, hovered_net, source_key
from nandsim.gui.session import ChipSession


@dataclass
class Hover:
    node: NodeKey | None = None
    route: Route | None = None


def format_value(value: int | None, width: int, hex_mode: bool) -> str:
    if value is None:
        return "?"
    if width == 1:
        return str(value)
    if hex_mode:
        return f"0x{value:0{(width + 3) // 4}X}"
    return str(value)


def wire_style(session: ChipSession, nets: tuple[int, ...]) -> tuple[theme.Color, float]:
    """(colour, width in layout units) for a wire carrying `nets`."""
    if len(nets) == 1:
        return theme.bit_color(session.value(nets)), 2.0
    if session.known_fraction(nets) < 1.0:
        return theme.WIRE_X, 4.0
    return theme.BUS, 4.0


def draw_circuit(
    surf: pygame.Surface,
    session: ChipSession,
    cam: Camera,
    fonts: theme.Fonts,
    hover: Hover,
    hex_mode: bool,
) -> None:
    snap = session.snapshot
    if snap is None:
        return
    view, lay = snap.view, snap.layout
    s = cam.scale
    small = fonts.get(12 * s)
    label_font = fonts.get(13 * s, bold=True)

    # Wires first; the hovered net last, over a halo, so it reads across the canvas.
    net = hovered_net(lay, hover.node, hover.route)
    lit = [
        r
        for r in lay.routes
        if net is not None and source_key(r.edge) == net and len(r.points) >= 2
    ]
    lit_ids = {id(r) for r in lit}
    routes = [r for r in lay.routes if id(r) not in lit_ids] + lit
    for r in routes:
        if lit and r is lit[0]:
            for h in lit:  # halo under every wire of the net, drawn once before them
                _, hw = wire_style(session, h.edge.nets)
                hpts = [cam.to_screen(p) for p in h.points]
                halo = max(3, round((hw * 1.8 + 4) * s))
                pygame.draw.lines(surf, theme.ACCENT, False, hpts, halo)
        color, w = wire_style(session, r.edge.nets)
        width = max(1, round(w * s * (1.8 if id(r) in lit_ids else 1.0)))
        if r.label_at is not None:  # constant
            text = small.render(
                r.edge.label, True, theme.bit_color(1 if r.edge.label == "true" else 0)
            )
            surf.blit(text, cam.to_screen(r.label_at))
            continue
        pts = [cam.to_screen(p) for p in r.points]
        if len(pts) >= 2:
            pygame.draw.lines(surf, color, False, pts, width)
        if len(r.edge.nets) > 1 and len(pts) >= 2:  # bus value near its source
            val = format_value(session.value(r.edge.nets), len(r.edge.nets), hex_mode)
            tag = small.render(val, True, color)
            x, y = pts[0]
            surf.blit(tag, (x + 4 * s, y - tag.get_height() - 1))

    for p, r in lay.junctions:  # dots where a wire branches
        color, w = wire_style(session, r.edge.nets)
        grow = 1.8 if id(r) in lit_ids else 1.0
        pygame.draw.circle(surf, color, cam.to_screen(p), max(2, round((w * grow + 2) * s)))

    parts = {p.index: p for p in view.parts}
    radius = max(2, round(6 * s))
    for key, b in lay.boxes.items():
        kind, ident = key
        if kind == "dummy":
            continue
        x, y = cam.to_screen((b.x, b.y))
        rect = pygame.Rect(round(x), round(y), max(1, round(b.w * s)), max(1, round(b.h * s)))
        hovered = hover.node == key
        if kind == "part":
            p = parts[int(ident)]
            fill = theme.PRIMITIVE_FILL if p.primitive else theme.PART_FILL
            pygame.draw.rect(surf, fill, rect, border_radius=radius)
            border = theme.ACCENT if hovered and not p.primitive else theme.PART_BORDER
            pygame.draw.rect(surf, border, rect, width=max(1, round(1.5 * s)), border_radius=radius)
            title = label_font.render(p.label, True, theme.TEXT)
            surf.blit(title, (rect.centerx - title.get_width() / 2, rect.y + 2 * s))
            for q in p.inputs:
                ax, ay = cam.to_screen(b.anchors[("in", q.name)])
                t = small.render(q.name, True, theme.TEXT_DIM)
                surf.blit(t, (ax + 4 * s, ay - t.get_height() / 2))
            for q in p.outputs:
                ax, ay = cam.to_screen(b.anchors[("out", q.name)])
                t = small.render(q.name, True, theme.TEXT_DIM)
                surf.blit(t, (ax - 4 * s - t.get_width(), ay - t.get_height() / 2))
        else:
            pins = view.inputs if kind == "in" else view.outputs
            q = next(q for q in pins if q.name == ident)
            value = session.value(q.nets)
            color = (
                theme.bit_color(value)
                if q.width == 1
                else (theme.BUS if value is not None else theme.WIRE_X)
            )
            clickable = kind == "in" and session.at_top
            pygame.draw.rect(surf, theme.IO_FILL, rect, border_radius=radius)
            edge_w = max(1, round((2.5 if hovered and clickable else 1.5) * s))
            pygame.draw.rect(surf, color, rect, width=edge_w, border_radius=radius)
            name = q.name if q.width == 1 else f"{q.name}[{q.width}]"
            t = small.render(f"{name} {format_value(value, q.width, hex_mode)}", True, theme.TEXT)
            surf.blit(t, (rect.x + 5 * s, rect.centery - t.get_height() / 2))
