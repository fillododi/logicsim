"""Zoom and pan between layout coordinates and screen pixels, plus hit testing. No pygame."""

from __future__ import annotations

from dataclasses import dataclass

from nandsim.gui.layout import Box, Layout, NodeKey, Point, Route

MIN_SCALE = 0.2
MAX_SCALE = 4.0


@dataclass
class Camera:
    scale: float = 1.0
    ox: float = 0.0  # screen x of layout x=0
    oy: float = 0.0

    def to_screen(self, p: Point) -> Point:
        return (p[0] * self.scale + self.ox, p[1] * self.scale + self.oy)

    def to_layout(self, p: Point) -> Point:
        return ((p[0] - self.ox) / self.scale, (p[1] - self.oy) / self.scale)

    def zoom_at(self, screen: Point, factor: float) -> None:
        """Zoom keeping the layout point under `screen` fixed."""
        lx, ly = self.to_layout(screen)
        self.scale = min(MAX_SCALE, max(MIN_SCALE, self.scale * factor))
        self.ox = screen[0] - lx * self.scale
        self.oy = screen[1] - ly * self.scale

    def pan(self, dx: float, dy: float) -> None:
        self.ox += dx
        self.oy += dy

    def fit(
        self, lay: Layout, area: tuple[float, float, float, float], max_scale: float = 1.5
    ) -> None:
        """Scale and center the whole layout inside `area` = (x, y, w, h) in screen pixels."""
        x, y, w, h = area
        if lay.width <= 0 or lay.height <= 0:
            return
        self.scale = max(MIN_SCALE, min(max_scale, w / lay.width, h / lay.height))
        self.ox = x + (w - lay.width * self.scale) / 2
        self.oy = y + (h - lay.height * self.scale) / 2


def box_at(lay: Layout, p: Point) -> NodeKey | None:
    """The node under a layout point (dummies excluded)."""
    for key, b in lay.boxes.items():
        if key[0] != "dummy" and _inside(b, p):
            return key
    return None


def route_at(lay: Layout, p: Point, tolerance: float) -> Route | None:
    """The wire closest to a layout point, if within `tolerance` layout units."""
    best: tuple[float, Route] | None = None
    for r in lay.routes:
        for a, b in zip(r.points, r.points[1:], strict=False):
            d = _segment_distance(p, a, b)
            if d <= tolerance and (best is None or d < best[0]):
                best = (d, r)
    return best[1] if best else None


def _inside(b: Box, p: Point) -> bool:
    return b.x <= p[0] <= b.right and b.y <= p[1] <= b.bottom


def _segment_distance(p: Point, a: Point, b: Point) -> float:
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    cx, cy = ax + t * dx, ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
