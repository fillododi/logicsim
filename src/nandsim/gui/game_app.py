"""The game screen: level list and brief on the left, circuit in the middle, editor and
test results on the right.

It reuses `ViewerApp` for the canvas, the editor pane, navigation and error display,
and adds the level sidebar, the results panel and the "Run tests" action.
"""

from __future__ import annotations

from pathlib import Path

import pygame

from nandsim.gui import theme
from nandsim.gui.app import FOOTER, HEADER, ViewerApp
from nandsim.gui.brief import brief_lines
from nandsim.gui.editor import EditorWidget
from nandsim.gui.game import GameState
from nandsim.gui.saves import SaveStore
from nandsim.gui.session import ChipSession
from nandsim.gui.textbuffer import TextBuffer
from nandsim.testing import Level, load_levels

SIDEBAR = 260
RESULTS_H = 190
ROW_H = 26
BUTTON_W = 210

GLYPH = {"solved": "✓", "open": "○", "locked": "–"}


class GameApp(ViewerApp):
    def __init__(self, store: SaveStore, size: tuple[int, int] = (1440, 860)) -> None:
        self.game = GameState(store)
        session = ChipSession(self.game.loader())
        session.reload()
        super().__init__(session, size=size)
        self.edit_path = Path(self.game.path)
        self.editor = EditorWidget(TextBuffer(self.game.text()), self.fonts, self.editor_rect)
        self.notice: str | None = store.warning
        self._attempted = store.has_save(self.game.current)
        self._rows: list[tuple[pygame.Rect, Level]] = []
        self._sync_error()
        self.fit()

    # ---- geometry ------------------------------------------------------------

    @property
    def left_width(self) -> int:
        return SIDEBAR

    @property
    def editor_rect(self) -> pygame.Rect:
        r = super().editor_rect
        return pygame.Rect(r.x, r.y, r.width, r.height - RESULTS_H)

    @property
    def results_rect(self) -> pygame.Rect:
        e = self.editor_rect
        return pygame.Rect(e.x, e.bottom, e.width, RESULTS_H)

    @property
    def button_rect(self) -> pygame.Rect:
        r = self.results_rect
        return pygame.Rect(r.x + 12, r.y + 10, BUTTON_W, 30)

    @property
    def show_errors(self) -> bool:
        # A level's starting text "isn't connected" by design: don't greet the player with
        # an error before they have saved or run this level at least once.
        return getattr(self, "_attempted", False)

    # ---- actions -------------------------------------------------------------

    def open_level(self, level: Level) -> None:
        if self.game.status(level) == "locked":
            missing = ", ".join(self.game.missing(level))
            self.notice = f"{level.name} is locked: solve {missing} first."
            return
        self.notice = None
        assert self.editor is not None
        if self.editor.buffer.dirty:  # never lose work: save it to the level it belongs to
            self.game.save(self.editor.buffer.text)
        self.game.select(level)
        self.editor.buffer.set_text(self.game.text())
        self.editor.focused = True
        self._attempted = self.game.store.has_save(level)
        self.edit_path = Path(self.game.path)
        self.session = ChipSession(self.game.loader())
        self.session.reload()
        self._sync_error()
        self.fit()

    def save(self) -> None:
        assert self.editor is not None
        self.game.save(self.editor.buffer.text)
        self.editor.buffer.mark_saved()
        self._attempted = True
        self._rebuild()

    def run_tests(self) -> None:
        assert self.editor is not None
        self.game.run_tests(self.editor.buffer.text)
        self.editor.buffer.mark_saved()
        self._attempted = True
        self._rebuild()

    def on_editor_action(self, action: str) -> None:
        if action == "save":
            self.save()
        elif action == "run":
            self.run_tests()

    # ---- events --------------------------------------------------------------

    def handle(self, ev: pygame.event.Event) -> None:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.button_rect.collidepoint(ev.pos):
                self.run_tests()
                return
            for rect, level in self._rows:
                if rect.collidepoint(ev.pos):
                    if level is not self.game.current:
                        self.open_level(level)
                    return
            if ev.pos[0] < SIDEBAR or self.results_rect.collidepoint(ev.pos):
                return
        super().handle(ev)

    # ---- drawing -------------------------------------------------------------

    def render(self, surf: pygame.Surface) -> None:
        super().render(surf)
        self._draw_sidebar(surf)
        self._draw_results(surf)

    def _draw_sidebar(self, surf: pygame.Surface) -> None:
        h = self.size[1]
        pygame.draw.rect(surf, theme.PANEL, (0, 0, SIDEBAR, h - FOOTER))
        title = self.fonts.get(16, bold=True).render("NAND Sim", True, theme.TEXT)
        surf.blit(title, (14, (HEADER - title.get_height()) // 2))
        font = self.fonts.get(14)
        y = HEADER + 6
        self._rows = []
        group = None
        for level in self.game.levels:
            if level.group != group:
                group = level.group
                label = group.split("_", 1)[-1].replace("_", " ").title()
                t = self.fonts.get(12, bold=True).render(label.upper(), True, theme.TEXT_DIM)
                surf.blit(t, (14, y + 6))
                y += ROW_H
            status = self.game.status(level)
            rect = pygame.Rect(6, y, SIDEBAR - 12, ROW_H - 2)
            if level is self.game.current:
                pygame.draw.rect(surf, theme.BG, rect, border_radius=5)
            color = {"solved": theme.WIRE_1, "open": theme.TEXT, "locked": theme.TEXT_DIM}[status]
            glyph = font.render(GLYPH[status], True, color)
            surf.blit(glyph, (rect.x + 8, rect.centery - glyph.get_height() // 2))
            name = font.render(level.name, True, theme.TEXT if status != "locked" else color)
            surf.blit(name, (rect.x + 30, rect.centery - name.get_height() // 2))
            self._rows.append((rect, level))
            y += ROW_H
        y += 8
        pygame.draw.line(surf, theme.PART_BORDER, (12, y), (SIDEBAR - 12, y))
        y += 10
        if self.notice:
            for line in _wrap(self.notice, (SIDEBAR - 28) // font.size("M")[0]):
                t = font.render(line, True, theme.WIRE_X)
                surf.blit(t, (14, y))
                y += font.get_linesize()
            y += 8
        self._draw_brief(surf, y)

    def _draw_brief(self, surf: pygame.Surface, y: int) -> None:
        text_font = self.fonts.get(13)
        cols = (SIDEBAR - 28) // text_font.size("M")[0]
        bottom = self.size[1] - FOOTER - 6
        md = self.game.current.brief.read_text()
        for line, kind in brief_lines(md, cols):
            font = {
                "title": self.fonts.get(16, bold=True),
                "bold": self.fonts.get(13, bold=True),
            }.get(kind, text_font)
            if y + font.get_linesize() > bottom:
                break
            color = theme.ACCENT if kind == "table" else theme.TEXT
            if line:
                surf.blit(font.render(line, True, color), (14, y))
            y += font.get_linesize() if kind != "blank" else font.get_linesize() // 2

    def _draw_results(self, surf: pygame.Surface) -> None:
        r = self.results_rect
        pygame.draw.rect(surf, theme.PANEL, r)
        pygame.draw.line(surf, theme.PART_BORDER, (r.x, r.y), (r.right, r.y))
        b = self.button_rect
        hovered = b.collidepoint(self.mouse)
        pygame.draw.rect(surf, theme.ACCENT if hovered else theme.PART_BORDER, b, border_radius=6)
        t = self.fonts.get(14, bold=True).render("▶ Run tests", True, theme.BG)
        surf.blit(t, (b.x + 12, b.centery - t.get_height() // 2))
        hint = self.fonts.get(12).render("Ctrl+Enter", True, theme.TEXT_DIM)
        surf.blit(hint, (b.right + 10, b.centery - hint.get_height() // 2))
        font = self.fonts.get(13)
        cols = max(20, (r.width - 24) // font.size("M")[0])
        y = b.bottom + 10
        report = self.game.report
        if report is None:
            msg = "Write the chip, then run the tests. Ctrl+S saves and shows the circuit."
            for line in _wrap(msg, cols):
                surf.blit(font.render(line, True, theme.TEXT_DIM), (r.x + 12, y))
                y += font.get_linesize()
            return
        color = theme.WIRE_1 if report.passed else theme.ERROR_TEXT
        summary = report.summary + (" — level solved!" if report.passed else "")
        surf.blit(self.fonts.get(14, bold=True).render(summary, True, color), (r.x + 12, y))
        y += font.get_linesize() + 4
        for item in report.lines:
            for line in _wrap(item, cols):
                if y + font.get_linesize() > r.bottom - 4:
                    return
                accent = item.startswith(("Unlocked", "Tip:"))
                surf.blit(
                    font.render(line, True, theme.ACCENT if accent else theme.TEXT),
                    (r.x + 12, y),
                )
                y += font.get_linesize()


def _wrap(text: str, cols: int) -> list[str]:
    import textwrap

    return textwrap.wrap(text, max(10, cols)) or [""]


def open_game(save_dir: Path | None = None) -> int:
    """`nandsim gui`: the game."""
    store = SaveStore(load_levels(), save_dir)
    GameApp(store).run(title="NAND Sim")
    return 0
