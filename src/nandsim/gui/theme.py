"""Colours and the bundled monospace font."""

from __future__ import annotations

from pathlib import Path

import pygame

FONT_DIR = Path(__file__).parent / "fonts"
FONT_REGULAR = FONT_DIR / "DejaVuSansMono.ttf"
FONT_BOLD = FONT_DIR / "DejaVuSansMono-Bold.ttf"

Color = tuple[int, int, int]

BG: Color = (30, 31, 36)
PANEL: Color = (40, 42, 50)
TEXT: Color = (216, 219, 226)
TEXT_DIM: Color = (138, 144, 160)
ACCENT: Color = (159, 180, 255)

WIRE_0: Color = (78, 88, 108)
WIRE_1: Color = (72, 209, 122)
WIRE_X: Color = (224, 160, 48)  # undefined
BUS: Color = (106, 168, 255)

PART_FILL: Color = (43, 45, 53)
PRIMITIVE_FILL: Color = (54, 46, 62)
PART_BORDER: Color = (90, 95, 110)
IO_FILL: Color = (36, 52, 60)

BUBBLE: Color = (50, 55, 76)  # guide bubbles

ERROR_BG: Color = (90, 31, 36)
ERROR_TEXT: Color = (255, 215, 215)


def bit_color(value: int | None) -> Color:
    if value is None:
        return WIRE_X
    return WIRE_1 if value else WIRE_0


class Fonts:
    """Font cache by (size, bold). Sizes are clamped so zooming never makes text unusable."""

    def __init__(self) -> None:
        self._cache: dict[tuple[int, bool], pygame.font.Font] = {}

    def get(self, size: float, bold: bool = False) -> pygame.font.Font:
        px = int(max(7, min(40, round(size))))
        key = (px, bold)
        if key not in self._cache:
            self._cache[key] = pygame.font.Font(str(FONT_BOLD if bold else FONT_REGULAR), px)
        return self._cache[key]
