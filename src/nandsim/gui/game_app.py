"""The game screen: level list and brief on the left, circuit in the middle, editor and
test results on the right.

It reuses `ViewerApp` for the canvas, the editor pane, navigation and error display,
and adds the level sidebar, the results panel, the "Run tests" action and the guided
tour's bubbles (F1 replays the tour). Menus sit on top: the title screen at start,
and the pause menu on Esc, from which the game can be reset.
"""

from __future__ import annotations

from pathlib import Path

import pygame

from nandsim.gui import theme
from nandsim.gui.app import HEADER, ViewerApp
from nandsim.gui.brief import brief_lines
from nandsim.gui.canvas import Hover
from nandsim.gui.editor import EditorWidget
from nandsim.gui.game import GameState
from nandsim.gui.guide import Bubble, draw_bubble
from nandsim.gui.menu import BACK, Menu, MenuItem, dim
from nandsim.gui.model import child_path
from nandsim.gui.saves import SaveStore
from nandsim.gui.session import ChipSession
from nandsim.gui.textbuffer import Pos, TextBuffer
from nandsim.gui.tutorial import Tour, load_steps
from nandsim.testing import Level, load_levels

SIDEBAR = 260
RESULTS_H = 190
ROW_H = 26
BUTTON_W = 210

GLYPH = {"solved": "✓", "open": "○", "locked": "–"}


class GameApp(ViewerApp):
    def __init__(
        self, store: SaveStore, size: tuple[int, int] = (1440, 860), title_screen: bool = False
    ) -> None:
        self.game = GameState(store)
        self._level_names = {lv.name for lv in store.levels}
        self.tour = self._new_tour()
        self.menus: list[Menu] = []  # open menus, topmost last; while any is open it takes input
        self.on_title = False  # the title screen replaces the game, the pause menu overlays it
        self._focus_before_menu = True
        self.bubble: Bubble | None = None
        self._bubble_press = False  # a press started on the bubble; its release is ours too
        self._brief_rect = pygame.Rect(0, 0, 0, 0)
        session = ChipSession(self.game.loader())
        session.reload()
        super().__init__(session, size=size)
        self.edit_path = Path(self.game.path)
        self.editor = EditorWidget(TextBuffer(self.game.text()), self.fonts, self.editor_rect)
        warnings = [w for w in (store.warning, self.tour.warning) if w]
        self.notice: str | None = "; ".join(warnings) or None
        self._attempted = store.has_save(self.game.current)
        self._rows: list[tuple[pygame.Rect, Level]] = []
        self._sync_error()
        self.fit()
        if title_screen:
            self.open_title()

    def _new_tour(self) -> Tour:
        return Tour(load_steps(levels=self._level_names), self.game.store.root / "tutorial.json")

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
    def help_text(self) -> str:
        # Esc opens the menu in the game, even from the editor (a click on the circuit
        # leaves the editor instead), so the viewer's "Esc: ..." item doesn't apply.
        items = [i for i in super().help_text.split("  ·  ") if not i.startswith("Esc")]
        return "  ·  ".join(["Esc: menu", "F1: tour", *items])

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
        self.tour_event("open_level", level.name)  # reported from the level being left
        if self.editor.buffer.dirty:  # never lose work: save it to the level it belongs to
            self.game.save(self.editor.buffer.text)
        self.game.select(level)
        self.tour.catch_up(level.name)  # its next step may be something already done here
        self._load_current()

    def _load_current(self) -> None:
        """Show the current level: its text in the editor, its circuit on the canvas."""
        assert self.editor is not None
        self.editor.buffer.set_text(self.game.text())
        self.editor.focused = True
        self._attempted = self.game.store.has_save(self.game.current)
        self.edit_path = Path(self.game.path)
        self.session = ChipSession(self.game.loader())
        self.session.reload()
        self._sync_error()
        self.fit()

    def reset_game(self) -> None:
        """Start over from the first level; the old files are kept in a backup folder.

        The editor's unsaved text is dropped on purpose: saving it would put a chip
        back into the save directory that was just emptied.
        """
        backup = self.game.store.reset()
        self.game = GameState(self.game.store)
        self.tour = self._new_tour()
        self._load_current()
        self.notice = f"New game. Your old chips are in {_home_short(backup)}" if backup else None

    def before_quit(self) -> None:
        """Never lose typing: unsaved editor text goes to the level's save file."""
        if self.editor is not None and self.editor.buffer.dirty:
            self.game.save(self.editor.buffer.text)

    # ---- menus ---------------------------------------------------------------

    def open_title(self) -> None:
        self.on_title = True
        self._open_menu(self._title_menu())

    def open_pause(self) -> None:
        self._open_menu(
            Menu(
                "Paused",
                [
                    MenuItem("Resume", "resume"),
                    MenuItem("Replay the tour", "tour"),
                    MenuItem("Main menu", "title"),
                    MenuItem("Reset game…", "reset"),
                    MenuItem("Quit", "quit"),
                ],
            )
        )

    def _title_menu(self) -> Menu:
        started = self.game.store.has_progress()
        items = [MenuItem("Continue" if started else "Play", "play")]
        if started:
            items.append(MenuItem("Reset game…", "reset"))
        items.append(MenuItem("Quit", "quit"))
        msg = "Build a computer, starting from a single kind of gate: the Nand."
        return Menu("NAND Sim", items, message=msg, big_title=True)

    def _confirm_reset_menu(self) -> Menu:
        where = _home_short(self.game.store.backups)
        msg = (
            "Every chip you wrote, the levels you solved and the tour start over from the "
            f"first level.\n\nYour files aren't deleted: they move to {where}."
        )
        # Cancel comes first, so Enter on a menu opened by mistake is harmless.
        items = [MenuItem("Cancel", BACK), MenuItem("Reset the game", "confirm_reset", True)]
        return Menu("Reset the game?", items, message=msg)

    def _open_menu(self, menu: Menu) -> None:
        if not self.menus:
            assert self.editor is not None
            self._focus_before_menu = self.editor.focused
            self.editor.focused = False
        self.menus = [menu]
        self.hover = Hover()

    def _close_menus(self) -> None:
        assert self.editor is not None
        self.menus = []
        self.on_title = False
        self.editor.focused = self._focus_before_menu

    def menu_action(self, action: str) -> None:
        """Carry out what the player chose in the topmost menu."""
        if action == BACK:
            if len(self.menus) > 1:
                self.menus.pop()
            elif not self.on_title:  # the title screen has nothing to go back to
                self._close_menus()
        elif action in ("play", "resume"):
            self._close_menus()
        elif action == "tour":
            self._close_menus()
            self.replay_tour()
        elif action == "title":
            self.on_title = True
            self.menus = [self._title_menu()]
        elif action == "reset":
            self.menus.append(self._confirm_reset_menu())
        elif action == "confirm_reset":
            self.reset_game()
            self._focus_before_menu = True  # a new game starts in the editor
            self._close_menus()
        elif action == "quit":
            self.quit_requested = True

    def save(self) -> None:
        assert self.editor is not None
        self.game.save(self.editor.buffer.text)
        self.editor.buffer.mark_saved()
        self._attempted = True
        self._rebuild()
        self.tour_event("save")
        if self.session.error is None:
            self.tour_event("build_ok")

    def run_tests(self) -> None:
        assert self.editor is not None
        report = self.game.run_tests(self.editor.buffer.text)
        self.editor.buffer.mark_saved()
        self._attempted = True
        self._rebuild()
        self.tour_event("run_tests")
        if self.session.error is None:
            self.tour_event("build_ok")  # Ctrl+Enter builds too, so it counts as building
        if report.passed:
            self.tour_event("solved")

    def tour_event(self, name: str, detail: str | None = None) -> None:
        self.tour.event(self.game.current.name, name, detail)

    def on_action(self, name: str) -> None:
        self.tour_event(name)

    def replay_tour(self) -> None:
        """F1: start the tour again, from the level its first step belongs to."""
        self.tour.replay()
        step = self.tour.current
        if step is not None and step.level and step.level != self.game.current.name:
            level = next((lv for lv in self.game.levels if lv.name == step.level), None)
            if level is not None and self.game.status(level) != "locked":
                self.open_level(level)

    def on_editor_action(self, action: str) -> None:
        if action == "save":
            self.save()
        elif action == "run":
            self.run_tests()

    # ---- events --------------------------------------------------------------

    def handle(self, ev: pygame.event.Event) -> None:
        if self.menus:
            if hasattr(ev, "pos"):
                self.mouse = ev.pos
            action = self.menus[-1].handle(ev)
            if action is not None:
                self.menu_action(action)
            return
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.open_pause()
            return
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F1:
            self.replay_tour()
            return
        if self._bubble_event(ev):
            return
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

    def _bubble_event(self, ev: pygame.event.Event) -> bool:
        """Presses, wheel turns and plain moves over the bubble never reach what lies under it.

        Only gestures that start on the bubble are swallowed: a text selection or a pan
        that merely ends over the bubble still gets its moves and its release.
        """
        if ev.type == pygame.MOUSEBUTTONUP and self._bubble_press:
            self._bubble_press = False
            return True
        b = self.bubble
        pos = self.mouse if ev.type == pygame.MOUSEWHEEL else getattr(ev, "pos", None)
        if b is None or pos is None or not b.rect.collidepoint(pos):
            return False
        if ev.type == pygame.MOUSEMOTION:
            if any(getattr(ev, "buttons", ())):
                return False  # a drag passing over the bubble
            self.mouse = pos
            self.hover = Hover()  # nothing under the bubble is hovered
            return True
        if ev.type == pygame.MOUSEBUTTONDOWN:
            self._bubble_press = True
            if ev.button == 1 and b.next is not None and b.next.collidepoint(pos):
                self.tour_event("next")
            elif ev.button == 1 and b.skip.collidepoint(pos):
                self.tour.skip()
            return True
        return ev.type == pygame.MOUSEWHEEL

    # ---- tour anchors --------------------------------------------------------

    def anchor_rect(self, anchor: str) -> pygame.Rect | None:
        """Screen rectangle of a tour anchor (see `tutorial.ANCHORS`); None if not on screen."""
        kind, _, arg = anchor.partition(":")
        w, h = self.size
        x, y, cw, ch = (round(v) for v in self.canvas_area)
        canvas = pygame.Rect(x, y, cw, ch)
        if anchor == "levels":
            rects = [r for r, _ in self._rows]
            return rects[0].unionall(rects[1:]) if rects else None
        if kind == "level":
            return next((r for r, lv in self._rows if lv.name == arg), None)
        if anchor == "brief":
            return self._brief_rect
        if anchor == "editor":
            return self.editor_rect
        if anchor == "canvas":
            return canvas
        if anchor == "header":
            return pygame.Rect(self.left_width, 0, cw, HEADER)
        if anchor == "run_button":
            return self.button_rect
        if anchor == "results":
            return self.results_rect
        if anchor == "footer":
            return pygame.Rect(0, h - self.footer_height, w, self.footer_height)
        if kind == "line":
            return self._line_rect(arg)
        if kind == "pin" or anchor == "part":
            box = self._box_rect(arg if kind == "pin" else None)
            return box.clip(canvas) if box is not None and box.colliderect(canvas) else canvas
        return None

    def _line_rect(self, text: str) -> pygame.Rect:
        ed = self.editor
        assert ed is not None
        lines = ed.buffer.lines
        i = next((n for n, t in enumerate(lines) if text in t), None)
        if i is None or not ed.scroll_line <= i < ed.scroll_line + ed.visible_lines:
            return ed.rect
        col = lines[i].index(text)
        x, y = ed.screen_of(Pos(i, col))
        r = pygame.Rect(x, y, len(text) * ed.char_w, ed.line_h)
        return r.clip(ed.rect)

    def _box_rect(self, pin: str | None) -> pygame.Rect | None:
        """The box of input/output `pin`, or of the first part that opens (any part if none)."""
        snap = self.session.snapshot
        if snap is None:
            return None
        if pin is not None:
            keys = [("in", pin), ("out", pin)]
        else:
            parts = sorted(k for k in snap.layout.boxes if k[0] == "part")
            view = snap.view
            opens = [k for k in parts if child_path(self.session.path, view.part(int(k[1])))]
            keys = opens + parts
        box = next((snap.layout.boxes[k] for k in keys if k in snap.layout.boxes), None)
        if box is None:
            return None
        x0, y0 = self.screen_of((box.x, box.y))
        x1, y1 = self.screen_of((box.right, box.bottom))
        return pygame.Rect(x0, y0, max(1, x1 - x0), max(1, y1 - y0))

    # ---- drawing -------------------------------------------------------------

    def render(self, surf: pygame.Surface) -> None:
        if self.on_title:
            surf.fill(theme.BG)
        else:
            super().render(surf)
            self._draw_sidebar(surf)
            self._draw_results(surf)
            self._draw_tour(surf)
            if self.menus:
                dim(surf)
        if self.menus:
            self.menus[-1].draw(surf, self.fonts, pygame.Rect(0, 0, *self.size))

    def _draw_tour(self, surf: pygame.Surface) -> None:
        step = self.tour.visible(self.game.current.name)
        if step is None:
            self.bubble = None
            return
        bounds = pygame.Rect(0, 0, self.size[0], self.size[1] - self.footer_height)
        anchor = self.anchor_rect(step.anchor)
        clear = anchor
        if anchor is not None and step.anchor.startswith("line:"):
            # Keep the whole editor row free: the player is about to type on that line.
            e = self.editor_rect
            clear = pygame.Rect(e.x, anchor.y, e.width, anchor.height)
        self.bubble = draw_bubble(
            surf, self.fonts, step, self.tour.position(step), anchor, bounds, self.mouse, clear
        )

    def _draw_sidebar(self, surf: pygame.Surface) -> None:
        h = self.size[1]
        pygame.draw.rect(surf, theme.PANEL, (0, 0, SIDEBAR, h - self.footer_height))
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
        bottom = self.size[1] - self.footer_height - 6
        top = y
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
        self._brief_rect = pygame.Rect(6, top - 4, SIDEBAR - 12, min(y, bottom) - top + 8)

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


def _home_short(path: Path) -> str:
    """`path` with the home directory written as ~, so it fits a sidebar or a dialog."""
    try:
        return "~/" + str(path.relative_to(Path.home()))
    except ValueError:
        return str(path)


def _wrap(text: str, cols: int) -> list[str]:
    import textwrap

    return textwrap.wrap(text, max(10, cols)) or [""]


def open_game(save_dir: Path | None = None) -> int:
    """`nandsim gui`: the game."""
    store = SaveStore(load_levels(), save_dir)
    GameApp(store, title_screen=True).run(title="NAND Sim")
    return 0
