"""Drawing a guide bubble: the step's text, a highlight on its anchor, Next and Skip.

The tour's state lives in `tutorial.py`. This module only draws one step and
reports where its buttons ended up, so the game can route clicks to them.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass

import pygame

from nandsim.gui import theme
from nandsim.gui.tutorial import Step, paragraphs, place_bubble

WIDTH = 330
PAD = 14


@dataclass
class Bubble:
    """Where the bubble and its buttons are on screen, for click handling."""

    rect: pygame.Rect
    next: pygame.Rect | None
    skip: pygame.Rect


def draw_bubble(
    surf: pygame.Surface,
    fonts: theme.Fonts,
    step: Step,
    position: tuple[int, int],
    anchor: pygame.Rect | None,
    bounds: pygame.Rect,
    mouse: tuple[int, int],
    keep_clear: pygame.Rect | None = None,
) -> Bubble:
    """Draw `step` next to `anchor`. The bubble also avoids `keep_clear` (default: the anchor)."""
    font, code = fonts.get(14), fonts.get(14, bold=True)
    small = fonts.get(12)
    cols = (WIDTH - 2 * PAD) // font.size("M")[0]
    rows: list[tuple[str, bool]] = []
    for i, (para, is_code) in enumerate(paragraphs(step.text)):
        if i:
            rows.append(("", False))
        rows += [(para, True)] if is_code else [(t, False) for t in textwrap.wrap(para, cols)]
    line_h = font.get_linesize()
    head_h = small.get_linesize() + 8
    foot_h = 40 if step.until == "next" else small.get_linesize() + 14
    height = PAD + head_h + len(rows) * line_h + foot_h
    area = (bounds.x, bounds.y, bounds.width, bounds.height)
    box = pygame.Rect(place_bubble(_box(keep_clear or anchor), (WIDTH, height), area))

    if anchor is not None:
        pygame.draw.rect(surf, theme.ACCENT, anchor.inflate(8, 8), 2, border_radius=6)
        a = (
            _clamp(box.centerx, anchor.left, anchor.right),
            _clamp(box.centery, anchor.top, anchor.bottom),
        )
        b = (_clamp(a[0], box.left, box.right), _clamp(a[1], box.top, box.bottom))
        pygame.draw.line(surf, theme.ACCENT, a, b, 2)
        pygame.draw.circle(surf, theme.ACCENT, a, 4)

    pygame.draw.rect(surf, theme.BUBBLE, box, border_radius=10)
    pygame.draw.rect(surf, theme.ACCENT, box, 2, border_radius=10)
    index, total = position
    x, y = box.x + PAD, box.y + PAD
    surf.blit(small.render(f"Tour {index} / {total}", True, theme.TEXT_DIM), (x, y))
    skip_t = small.render("Skip tour", True, theme.TEXT_DIM)
    skip = skip_t.get_rect(topright=(box.right - PAD, y)).inflate(8, 6)
    if skip.collidepoint(mouse):
        skip_t = small.render("Skip tour", True, theme.ACCENT)
    surf.blit(skip_t, skip_t.get_rect(center=skip.center))
    y += head_h
    for text, is_code in rows:
        if text:
            f = code if is_code else font
            surf.blit(f.render(text, True, theme.WIRE_1 if is_code else theme.TEXT), (x, y))
        y += line_h

    next_rect = None
    if step.until == "next":
        label = code.render("Next ›", True, theme.BG)
        next_rect = pygame.Rect(0, 0, label.get_width() + 24, 28)
        next_rect.bottomright = (box.right - PAD, box.bottom - 10)
        color = theme.TEXT if next_rect.collidepoint(mouse) else theme.ACCENT
        pygame.draw.rect(surf, color, next_rect, border_radius=6)
        surf.blit(label, label.get_rect(center=next_rect.center))
    else:
        hint = small.render("Do it to continue  ·  F1: replay", True, theme.TEXT_DIM)
        surf.blit(hint, (x, box.bottom - 8 - hint.get_height()))
    return Bubble(box, next_rect, skip)


def _box(r: pygame.Rect | None) -> tuple[int, int, int, int] | None:
    return None if r is None else (r.x, r.y, r.width, r.height)


def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))
