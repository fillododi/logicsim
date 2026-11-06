"""Overlay menus: the title screen, the Esc pause menu and confirmation dialogs.

A `Menu` is a title, an optional message, an optional one-line text field and a
column of buttons. It takes pygame events and answers with the chosen item's
action, or "back" on Esc; the host decides what the actions mean. Up/Down (or
Tab) move the selection, Enter or Space choose, and the mouse hovers and clicks.
With a text field, typing edits the field (Backspace deletes, Ctrl+Backspace
clears) and Space no longer chooses.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field

import pygame

from nandsim.gui import theme

BUTTON_H = 40
FIELD_H = 36
FIELD_MAX = 40  # characters
PANEL_W = 380
PAD = 24

BACK = "back"
HINT = "↑ ↓  choose  ·  Enter  select  ·  Esc  back"


@dataclass
class MenuItem:
    label: str
    action: str
    danger: bool = False  # drawn in the error colour: it throws something away


@dataclass
class Menu:
    title: str
    items: list[MenuItem]
    message: str = ""
    selected: int = 0
    big_title: bool = False  # the title screen's name, larger than a dialog's title
    text: str | None = None  # the text field's contents; None: no field
    allowed: str = r"\S"  # regex for one character the field accepts
    error: str = ""  # shown under the field, in the error colour
    rects: list[pygame.Rect] = field(default_factory=list)  # buttons, as last drawn
    panel: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))

    def handle(self, ev: pygame.event.Event) -> str | None:
        """The action chosen by this event, BACK for Esc, or None."""
        if self.text is not None and self._edit(ev):
            return None
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                return BACK
            if ev.key in (pygame.K_DOWN, pygame.K_TAB):
                self.selected = (self.selected + 1) % len(self.items)
            elif ev.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.items)
            elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self.items[self.selected].action
        elif ev.type == pygame.MOUSEMOTION:
            i = self._at(ev.pos)
            if i is not None:
                self.selected = i
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            i = self._at(ev.pos)
            if i is not None:
                return self.items[i].action
        return None

    def _edit(self, ev: pygame.event.Event) -> bool:
        """Typing into the text field; True if the event was used for it."""
        assert self.text is not None
        if ev.type == pygame.TEXTINPUT:
            keep = "".join(c for c in ev.text if re.fullmatch(self.allowed, c))
            self.text = (self.text + keep)[:FIELD_MAX]
            self.error = ""
            return True
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_BACKSPACE:
            ctrl = getattr(ev, "mod", 0) & pygame.KMOD_CTRL
            self.text = "" if ctrl else self.text[:-1]
            self.error = ""
            return True
        # Space would type nothing (names have no spaces) and must not press a button.
        return ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE

    def _at(self, pos: tuple[int, int]) -> int | None:
        return next((i for i, r in enumerate(self.rects) if r.collidepoint(pos)), None)

    def draw(self, surf: pygame.Surface, fonts: theme.Fonts, area: pygame.Rect) -> None:
        """Draw the panel centred in `area` and remember where the buttons are."""
        title_font = fonts.get(34 if self.big_title else 20, bold=True)
        text_font = fonts.get(14)
        button_font = fonts.get(15, bold=True)
        width = min(PANEL_W, area.width - 32)
        cols = max(16, (width - 2 * PAD) // text_font.size("M")[0])
        paras = self.message.split("\n") if self.message else []
        message = [ln for para in paras for ln in textwrap.wrap(para, cols) or [""]]
        errors = textwrap.wrap(self.error, cols) if self.error else []
        field_h = 0
        if self.text is not None:
            field_h = 8 + FIELD_H + 6 + len(errors) * text_font.get_linesize()
        height = (
            PAD
            + title_font.get_linesize()
            + (len(message) * text_font.get_linesize() + 12 if message else 0)
            + field_h
            + 12
            + len(self.items) * (BUTTON_H + 10)
            + PAD
            - 10
        )
        self.panel = pygame.Rect(0, 0, width, height)
        self.panel.center = area.center
        pygame.draw.rect(surf, theme.PANEL, self.panel, border_radius=10)
        pygame.draw.rect(surf, theme.PART_BORDER, self.panel, width=1, border_radius=10)
        y = self.panel.y + PAD
        t = title_font.render(self.title, True, theme.TEXT)
        surf.blit(t, (self.panel.centerx - t.get_width() // 2, y))
        y += title_font.get_linesize()
        if message:
            y += 4
            for line in message:
                surf.blit(text_font.render(line, True, theme.TEXT_DIM), (self.panel.x + PAD, y))
                y += text_font.get_linesize()
            y += 8
        if self.text is not None:
            y += 8
            box = pygame.Rect(self.panel.x + PAD, y, width - 2 * PAD, FIELD_H)
            pygame.draw.rect(surf, theme.BG, box, border_radius=6)
            edge = theme.ERROR_TEXT if self.error else theme.ACCENT
            pygame.draw.rect(surf, edge, box, width=2, border_radius=6)
            font = fonts.get(16)
            t = font.render(self.text, True, theme.TEXT)
            tx, ty = box.x + 10, box.centery - t.get_height() // 2
            surf.blit(t, (tx, ty))
            caret_x = tx + t.get_width() + 1
            pygame.draw.line(
                surf, theme.TEXT, (caret_x, ty + 2), (caret_x, ty + t.get_height() - 2)
            )
            y = box.bottom + 6
            for line in errors:
                surf.blit(text_font.render(line, True, theme.ERROR_TEXT), (self.panel.x + PAD, y))
                y += text_font.get_linesize()
        y += 12
        self.rects = []
        for i, item in enumerate(self.items):
            r = pygame.Rect(self.panel.x + PAD, y, width - 2 * PAD, BUTTON_H)
            on = i == self.selected
            if item.danger:
                fill, text = (
                    (theme.ERROR_BG, theme.ERROR_TEXT) if on else (theme.BG, theme.ERROR_TEXT)
                )
            else:
                fill, text = (theme.ACCENT, theme.BG) if on else (theme.BG, theme.TEXT)
            pygame.draw.rect(surf, fill, r, border_radius=6)
            if not on:
                pygame.draw.rect(surf, theme.PART_BORDER, r, width=1, border_radius=6)
            t = button_font.render(item.label, True, text)
            surf.blit(t, (r.centerx - t.get_width() // 2, r.centery - t.get_height() // 2))
            self.rects.append(r)
            y += BUTTON_H + 10
        hint = fonts.get(12).render(HINT, True, theme.TEXT_DIM)
        surf.blit(hint, (self.panel.centerx - hint.get_width() // 2, self.panel.bottom + 10))


def dim(surf: pygame.Surface) -> None:
    """Darken what is behind a menu so the menu reads as on top."""
    shade = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    shade.fill((*theme.BG, 190))
    surf.blit(shade, (0, 0))
