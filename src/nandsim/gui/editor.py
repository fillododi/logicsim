"""The HDL editor widget: draws a TextBuffer and turns key and mouse events into edits.

`handle(event)` returns an action string for the host ("save") or None. The host
owns what saving means (write a file, compile, run tests).
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import pygame

from nandsim.gui import theme
from nandsim.gui.syntax import highlight, token_end
from nandsim.gui.textbuffer import Pos, TextBuffer

FONT_SIZE = 14
GUTTER_PAD = 10
DOUBLE_CLICK_S = 0.4
WHEEL_LINES = 3  # lines one wheel notch scrolls
WHEEL_COLS = 6  # columns one sideways notch (or Shift + wheel) scrolls
HBAR_H = 8  # the horizontal scrollbar, along the bottom when a line is wider than the view
HBAR_MIN_W = 24  # its thumb never gets narrower than this

SYNTAX_COLORS: dict[str, theme.Color] = {
    "plain": (216, 219, 226),
    "comment": (110, 120, 135),
    "keyword": (198, 146, 234),
    "constant": (240, 160, 110),
    "number": (240, 160, 110),
    "chip": (110, 190, 255),
    "punct": (150, 156, 170),
}
SELECTION: theme.Color = (55, 75, 110)
CURRENT_LINE: theme.Color = (36, 38, 45)
CURSOR: theme.Color = (230, 230, 230)
ERROR: theme.Color = (255, 95, 95)


@dataclass
class EditorError:
    """An error to mark: 0-based position and the message."""

    pos: Pos
    message: str


class _Clipboard:
    """System clipboard (pygame-ce's scrap text API), falling back to an in-process one.

    The fallback matters headless and on systems without a clipboard service.
    """

    def __init__(self) -> None:
        self._local = ""

    def put(self, text: str) -> None:
        self._local = text
        try:
            pygame.scrap.put_text(text)
        except pygame.error:
            pass

    def get(self) -> str:
        try:
            text = pygame.scrap.get_text()
        except pygame.error:
            text = ""
        return text or self._local


class EditorWidget:
    def __init__(self, buffer: TextBuffer, fonts: theme.Fonts, rect: pygame.Rect) -> None:
        self.buffer = buffer
        self.fonts = fonts
        self.rect = rect
        self.focused = True
        self.error: EditorError | None = None
        self.scroll_line = 0
        self.scroll_x = 0
        self.clipboard = _Clipboard()
        self._dragging = False
        self._bar_grab: int | None = None  # dragging the scrollbar: mouse x minus thumb x
        self._last_click: tuple[float, Pos] | None = None
        self._blink_start = time.monotonic()

    # ---- geometry ----------------------------------------------------------

    @property
    def font(self) -> pygame.font.Font:
        return self.fonts.get(FONT_SIZE)

    @property
    def line_h(self) -> int:
        return self.font.get_linesize()

    @property
    def char_w(self) -> int:
        return self.font.size("M")[0]

    @property
    def gutter_w(self) -> int:
        return self.char_w * max(3, len(str(len(self.buffer.lines)))) + 2 * GUTTER_PAD

    @property
    def visible_lines(self) -> int:
        return max(1, (self.rect.height - self._hbar_h) // self.line_h)

    @property
    def text_w(self) -> int:
        """Width of the text area, right of the gutter."""
        return max(1, self.rect.width - self.gutter_w)

    @property
    def content_w(self) -> int:
        """Width of the longest line, plus room for the cursor after it."""
        return (max(len(line) for line in self.buffer.lines) + 2) * self.char_w

    @property
    def max_scroll_x(self) -> int:
        return max(0, self.content_w - self.text_w)

    @property
    def _hbar_h(self) -> int:
        return HBAR_H if self.max_scroll_x > 0 else 0

    def hbar(self) -> tuple[pygame.Rect, pygame.Rect] | None:
        """The horizontal scrollbar's track and thumb, or None when every line fits."""
        if self.max_scroll_x <= 0:
            return None
        r = self.rect
        track = pygame.Rect(r.x + self.gutter_w, r.bottom - HBAR_H, self.text_w, HBAR_H)
        w = max(HBAR_MIN_W, track.width * self.text_w // self.content_w)
        x = track.x + (track.width - w) * self.scroll_x // self.max_scroll_x
        return track, pygame.Rect(x, track.y + 1, w, HBAR_H - 2)

    @property
    def dragging(self) -> bool:
        """A drag started in the editor (selecting text, or the scrollbar) is under way."""
        return self._dragging or self._bar_grab is not None

    def pos_at(self, screen: tuple[int, int]) -> Pos:
        x, y = screen
        line = self.scroll_line + (y - self.rect.y) // self.line_h
        col = round((x - self.rect.x - self.gutter_w + self.scroll_x) / self.char_w)
        line = max(0, min(len(self.buffer.lines) - 1, line))
        return Pos(line, max(0, min(len(self.buffer.lines[line]), col)))

    def screen_of(self, p: Pos) -> tuple[int, int]:
        x = self.rect.x + self.gutter_w + p.col * self.char_w - self.scroll_x
        y = self.rect.y + (p.line - self.scroll_line) * self.line_h
        return x, y

    def ensure_cursor_visible(self) -> None:
        c = self.buffer.cursor
        if c.line < self.scroll_line:
            self.scroll_line = c.line
        elif c.line >= self.scroll_line + self.visible_lines:
            self.scroll_line = c.line - self.visible_lines + 1
        text_w = self.rect.width - self.gutter_w - self.char_w
        x = c.col * self.char_w
        if x < self.scroll_x:
            self.scroll_x = max(0, x - 4 * self.char_w)
        elif x > self.scroll_x + text_w:
            self.scroll_x = x - text_w + 4 * self.char_w

    def set_error(self, error: EditorError | None) -> None:
        self.error = error

    # ---- events ------------------------------------------------------------

    def handle(self, ev: pygame.event.Event) -> str | None:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            self.focused = self.rect.collidepoint(ev.pos)
            if not self.focused:
                return None
            bar = self.hbar()
            if bar is not None and bar[0].collidepoint(ev.pos):
                track, thumb = bar
                if not thumb.collidepoint(ev.pos):  # on the track: the thumb jumps there
                    self._drag_bar_to(ev.pos[0] - thumb.width // 2)
                    moved = self.hbar()
                    assert moved is not None  # the lines didn't change
                    thumb = moved[1]
                self._bar_grab = ev.pos[0] - thumb.x
                return None
            p = self.pos_at(ev.pos)
            now = time.monotonic()
            if (
                self._last_click
                and now - self._last_click[0] < DOUBLE_CLICK_S
                and (self._last_click[1] == p)
            ):
                self.buffer.select_word_at(p)
                self._last_click = None
            else:
                shift = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)
                self.buffer.set_cursor(p, select=shift)
                if not shift:
                    self.buffer.anchor = p
                self._dragging = True
                self._last_click = (now, p)
            self._touch()
        elif ev.type == pygame.MOUSEMOTION and self._bar_grab is not None:
            self._drag_bar_to(ev.pos[0] - self._bar_grab)
        elif ev.type == pygame.MOUSEMOTION and self._dragging:
            self.buffer.cursor = self.pos_at(ev.pos)
            self.ensure_cursor_visible()
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self._dragging = False
            self._bar_grab = None
        elif ev.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.wheel(ev.x, ev.y)
        elif not self.focused:
            return None
        elif ev.type == pygame.TEXTINPUT:
            for ch in ev.text:
                self.buffer.type_char(ch)
            self._touch()
        elif ev.type == pygame.KEYDOWN:
            return self._key(ev)
        return None

    def scroll(self, lines: int) -> None:
        last = max(0, len(self.buffer.lines) - self.visible_lines // 2)
        self.scroll_line = max(0, min(last, self.scroll_line + lines))

    def scroll_cols(self, cols: int) -> None:
        """Scroll sideways by `cols` characters (positive: right), within the longest line."""
        self.scroll_x = max(0, min(self.max_scroll_x, self.scroll_x + cols * self.char_w))

    def wheel(self, x: int, y: int) -> None:
        """A wheel or trackpad move: sideways moves scroll sideways, and so does the wheel
        with Shift held, as in most editors."""
        if pygame.key.get_mods() & pygame.KMOD_SHIFT and y and not x:
            x, y = -y, 0  # wheel down (y < 0) goes right
        if x:
            self.scroll_cols(x * WHEEL_COLS)
        if y:
            self.scroll(-y * WHEEL_LINES)

    def _drag_bar_to(self, thumb_x: int) -> None:
        """Move the scrollbar's thumb so its left edge is at `thumb_x`."""
        bar = self.hbar()
        if bar is None:
            return
        track, thumb = bar
        room = track.width - thumb.width
        if room <= 0:
            return
        at = max(0, min(room, thumb_x - track.x))
        self.scroll_x = at * self.max_scroll_x // room

    def _key(self, ev: pygame.event.Event) -> str | None:
        ctrl = bool(ev.mod & (pygame.KMOD_CTRL | pygame.KMOD_META))
        shift = bool(ev.mod & pygame.KMOD_SHIFT)
        b = self.buffer
        b.page_lines = max(1, self.visible_lines - 2)
        k = ev.key
        if ctrl:
            if k == pygame.K_s:
                return "save"
            if k in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return "run"
            if k == pygame.K_z:
                b.redo() if shift else b.undo()
            elif k == pygame.K_y:
                b.redo()
            elif k == pygame.K_a:
                b.select_all()
            elif k == pygame.K_c:
                if b.selected_text():
                    self.clipboard.put(b.selected_text())
            elif k == pygame.K_x:
                text = b.cut()
                if text:
                    self.clipboard.put(text)
            elif k == pygame.K_v:
                text = self.clipboard.get().replace("\r\n", "\n").replace("\t", "    ")
                if text:
                    b.insert(text)
            elif k == pygame.K_SLASH:
                b.toggle_comment()
            elif k == pygame.K_LEFT:
                b.move("word_left", shift)
            elif k == pygame.K_RIGHT:
                b.move("word_right", shift)
            elif k == pygame.K_HOME:
                b.move("doc_start", shift)
            elif k == pygame.K_END:
                b.move("doc_end", shift)
            else:
                return None
        else:
            moves = {
                pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right",
                pygame.K_UP: "up",
                pygame.K_DOWN: "down",
                pygame.K_HOME: "home",
                pygame.K_END: "end",
                pygame.K_PAGEUP: "page_up",
                pygame.K_PAGEDOWN: "page_down",
            }
            if k in moves:
                b.move(moves[k], shift)  # type: ignore[arg-type]
            elif k == pygame.K_BACKSPACE:
                b.backspace()
            elif k == pygame.K_DELETE:
                b.delete()
            elif k in (pygame.K_RETURN, pygame.K_KP_ENTER):
                b.newline()
            elif k == pygame.K_TAB:
                b.dedent() if shift else b.indent()
            else:
                return None
        self._touch()
        return None

    def _touch(self) -> None:
        self._blink_start = time.monotonic()
        self.ensure_cursor_visible()

    # ---- drawing -----------------------------------------------------------

    def render(self, surf: pygame.Surface) -> None:
        r = self.rect
        font, lh, cw, gw = self.font, self.line_h, self.char_w, self.gutter_w
        pygame.draw.rect(surf, theme.BG, r)
        pygame.draw.rect(surf, theme.PANEL, (r.x, r.y, gw - 4, r.height))
        old_clip = surf.get_clip()
        surf.set_clip(r)
        b = self.buffer
        first, last = self.scroll_line, min(len(b.lines), self.scroll_line + self.visible_lines + 1)
        spans = highlight(b.lines)  # needs lines above the view for block comments
        self.scroll_x = min(self.scroll_x, self.max_scroll_x)  # the long line may be gone
        sel = b.selection()
        text_x = r.x + gw - self.scroll_x
        for i in range(first, last):
            y = r.y + (i - first) * lh
            if i == b.cursor.line and self.focused and sel is None:
                pygame.draw.rect(surf, CURRENT_LINE, (r.x + gw - 4, y, r.width, lh))
            if sel is not None and sel[0].line <= i <= sel[1].line:
                a = sel[0].col if i == sel[0].line else 0
                z = sel[1].col if i == sel[1].line else len(b.lines[i]) + 1
                pygame.draw.rect(surf, SELECTION, (text_x + a * cw, y, max(1, z - a) * cw, lh))
            num_color = ERROR if self.error and self.error.pos.line == i else theme.TEXT_DIM
            num = font.render(str(i + 1), True, num_color)
            surf.set_clip(r)
            surf.blit(num, (r.x + gw - GUTTER_PAD - 4 - num.get_width(), y))
            surf.set_clip(pygame.Rect(r.x + gw - 2, r.y, r.width - gw + 2, r.height))
            line = b.lines[i]
            for a, z, kind in spans[i]:
                t = font.render(line[a:z], True, SYNTAX_COLORS[kind])
                surf.blit(t, (text_x + a * cw, y))
            if self.error and self.error.pos.line == i:
                col = min(self.error.pos.col, len(line))
                end = max(col + 1, token_end(line, col))
                self._squiggle(surf, text_x + col * cw, text_x + end * cw, y + lh - 3)
        if self.focused and (time.monotonic() - self._blink_start) % 1.0 < 0.6:
            cx, cy = self.screen_of(b.cursor)
            pygame.draw.line(surf, CURSOR, (cx, cy + 1), (cx, cy + lh - 2), 2)
        surf.set_clip(r)
        bar = self.hbar()
        if bar is not None:
            track, thumb = bar
            pygame.draw.rect(surf, theme.PANEL, track)
            hot = self._bar_grab is not None or track.collidepoint(pygame.mouse.get_pos())
            color = theme.ACCENT if hot else theme.PART_BORDER
            pygame.draw.rect(surf, color, thumb, border_radius=3)
        surf.set_clip(old_clip)

    @staticmethod
    def _squiggle(surf: pygame.Surface, x1: int, x2: int, y: int) -> None:
        pts = [(x, y + (2 if (x // 3) % 2 else 0)) for x in range(x1, x2 + 1, 3)]
        if len(pts) >= 2:
            pygame.draw.lines(surf, ERROR, False, pts, 1)
