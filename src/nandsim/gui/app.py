"""The viewer window: event handling, header (breadcrumbs), footer (help), error banner.

`ViewerApp` takes pygame events through `handle()` and draws through `render()`,
so tests and the playtest hook can drive it headless (`SDL_VIDEODRIVER=dummy`)
exactly as a player would. `run()` is the real event loop around those two.
"""

from __future__ import annotations

import time
from pathlib import Path

import pygame

from nandsim.gui import theme
from nandsim.gui.camera import Camera, box_at, route_at
from nandsim.gui.canvas import Hover, draw_circuit, format_value
from nandsim.gui.model import breadcrumbs
from nandsim.gui.session import ChipSession, FileWatcher

HEADER = 36
FOOTER = 26
CLICK_SLOP = 4  # pixels a press may move and still count as a click
POLL_SECONDS = 0.5
HELP = (
    "click input: toggle (right-click: count down, X: undefined)  ·  click part: open  ·  "
    "Backspace: up  ·  wheel: zoom  ·  drag: pan  ·  F: fit  ·  H: hex/dec"
)


class ViewerApp:
    def __init__(
        self,
        session: ChipSession,
        size: tuple[int, int] = (1280, 800),
        watcher: FileWatcher | None = None,
    ) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        self.session = session
        self.size = size
        self.watcher = watcher
        self.fonts = theme.Fonts()
        self.cam = Camera()
        self.hover = Hover()
        self.hex_mode = True
        self.mouse = (0, 0)
        self._press: tuple[int, int] | None = None
        self._dragged = False
        self._crumbs: list[tuple[pygame.Rect, str]] = []
        self._last_poll = 0.0
        self._fitted_path: str | None = None
        self.fit()

    # ---- geometry --------------------------------------------------------

    @property
    def canvas_area(self) -> tuple[float, float, float, float]:
        w, h = self.size
        return (0.0, float(HEADER), float(w), float(h - HEADER - FOOTER))

    def fit(self) -> None:
        if self.session.snapshot is not None:
            self.cam.fit(self.session.snapshot.layout, self.canvas_area)
            self._fitted_path = self.session.path

    def screen_of(self, layout_point: tuple[float, float]) -> tuple[int, int]:
        """Screen pixel of a layout point (used by tests to click on things)."""
        x, y = self.cam.to_screen(layout_point)
        return round(x), round(y)

    # ---- events ----------------------------------------------------------

    def handle(self, ev: pygame.event.Event) -> None:
        if ev.type == pygame.MOUSEMOTION:
            if self._press is not None and pygame.BUTTON_LEFT in self._buttons(ev):
                dx, dy = ev.rel
                if (
                    self._dragged
                    or abs(ev.pos[0] - self._press[0]) + abs(ev.pos[1] - self._press[1])
                    > CLICK_SLOP
                ):
                    self._dragged = True
                    self.cam.pan(dx, dy)
            self.mouse = ev.pos
            self._update_hover()
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (1, 3):
            self._press, self._dragged = ev.pos, False
            self.mouse = ev.pos
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button in (1, 3):
            if self._press is not None and not self._dragged:
                self._click(ev.pos, right=ev.button == 3)
            self._press = None
        elif ev.type == pygame.MOUSEWHEEL:
            self.cam.zoom_at(self.mouse, 1.15**ev.y)
            self._update_hover()
        elif ev.type == pygame.KEYDOWN:
            self._key(ev.key)

    @staticmethod
    def _buttons(ev: pygame.event.Event) -> set[int]:
        pressed = getattr(ev, "buttons", (0, 0, 0))
        return {i + 1 for i, b in enumerate(pressed) if b}

    def _click(self, pos: tuple[int, int], right: bool) -> None:
        for rect, path in self._crumbs:
            if rect.collidepoint(pos):
                self._navigate(path)
                return
        snap = self.session.snapshot
        if snap is None or pos[1] < HEADER:
            return
        key = box_at(snap.layout, self.cam.to_layout(pos))
        if key is None:
            return
        kind, ident = key
        if kind == "in" and self.session.at_top:
            self.session.toggle(str(ident), -1 if right else 1)
        elif kind == "part" and not right:
            if self.session.open(snap.view.part(int(ident))):
                self.fit()
        self._update_hover()

    def _key(self, key: int) -> None:
        if key in (pygame.K_BACKSPACE, pygame.K_ESCAPE):
            if self.session.up():
                self.fit()
        elif key == pygame.K_f:
            self.fit()
        elif key == pygame.K_h:
            self.hex_mode = not self.hex_mode
        elif key == pygame.K_x and self.hover.node and self.hover.node[0] == "in":
            if self.session.at_top:
                self.session.set_input(str(self.hover.node[1]), None)

    def _navigate(self, path: str) -> None:
        if path != self.session.path:
            self.session.goto(path)
            self.fit()

    def _update_hover(self) -> None:
        snap = self.session.snapshot
        if snap is None or self.mouse[1] < HEADER:
            self.hover = Hover()
            return
        p = self.cam.to_layout(self.mouse)
        node = box_at(snap.layout, p)
        route = None if node else route_at(snap.layout, p, 5 / self.cam.scale)
        self.hover = Hover(node, route)

    # ---- time ------------------------------------------------------------

    def tick(self, now: float | None = None) -> None:
        """Poll for changed files and reload; refit if the view jumped elsewhere."""
        now = time.monotonic() if now is None else now
        if self.watcher is None or now - self._last_poll < POLL_SECONDS:
            return
        self._last_poll = now
        if self.watcher.changed():
            self.session.reload()
            if self.session.path != self._fitted_path:
                self.fit()
            self._update_hover()

    # ---- drawing ---------------------------------------------------------

    def render(self, surf: pygame.Surface) -> None:
        surf.fill(theme.BG)
        draw_circuit(surf, self.session, self.cam, self.fonts, self.hover, self.hex_mode)
        self._draw_header(surf)
        self._draw_footer(surf)
        self._draw_tooltip(surf)

    def _draw_header(self, surf: pygame.Surface) -> None:
        w = self.size[0]
        pygame.draw.rect(surf, theme.PANEL, (0, 0, w, HEADER))
        font = self.fonts.get(15, bold=True)
        x = 12
        self._crumbs = []
        crumbs = breadcrumbs(self.session.path) if self.session.path else []
        for i, (label, path) in enumerate(crumbs):
            current = i == len(crumbs) - 1
            t = font.render(label, True, theme.TEXT if current else theme.ACCENT)
            rect = t.get_rect(topleft=(x, (HEADER - t.get_height()) // 2))
            surf.blit(t, rect)
            if not current:
                self._crumbs.append((rect.inflate(6, 6), path))
                sep = font.render("  ›  ", True, theme.TEXT_DIM)
                surf.blit(sep, (rect.right, rect.y))
                x = rect.right + sep.get_width()
        if not self.session.at_top:
            note = self.fonts.get(12).render(
                "inputs are set at the top level", True, theme.TEXT_DIM
            )
            surf.blit(note, (w - note.get_width() - 12, (HEADER - note.get_height()) // 2))

    def _draw_footer(self, surf: pygame.Surface) -> None:
        w, h = self.size
        err = self.session.error
        if err is not None:
            font = self.fonts.get(13)
            lines = str(err).splitlines() + ["(showing the last version that compiled)"]
            height = 10 + len(lines) * (font.get_linesize())
            top = h - FOOTER - height
            pygame.draw.rect(surf, theme.ERROR_BG, (0, top, w, height))
            for i, line in enumerate(lines):
                t = font.render(line, True, theme.ERROR_TEXT)
                surf.blit(t, (12, top + 5 + i * font.get_linesize()))
        pygame.draw.rect(surf, theme.PANEL, (0, h - FOOTER, w, FOOTER))
        t = self.fonts.get(12).render(HELP, True, theme.TEXT_DIM)
        surf.blit(t, (12, h - FOOTER + (FOOTER - t.get_height()) // 2))

    def _draw_tooltip(self, surf: pygame.Surface) -> None:
        r = self.hover.route
        if r is None:
            return
        val = format_value(self.session.value(r.edge.nets), len(r.edge.nets), self.hex_mode)
        t = self.fonts.get(13).render(f" {r.edge.label} = {val} ", True, theme.TEXT, theme.PANEL)
        x = min(self.mouse[0] + 14, self.size[0] - t.get_width() - 4)
        surf.blit(t, (x, self.mouse[1] + 14))

    def screenshot(self, path: Path) -> None:
        surf = pygame.Surface(self.size)
        self.render(surf)
        pygame.image.save(surf, str(path))

    # ---- real loop -------------------------------------------------------

    def run(self, title: str = "NAND Sim") -> None:
        pygame.init()
        screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption(title)
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return
                if ev.type == pygame.VIDEORESIZE:
                    self.size = (ev.w, ev.h)
                    self.fit()
                    continue
                self.handle(ev)
            self.tick()
            self.render(screen)
            pygame.display.flip()
            clock.tick(60)


def open_viewer(path: Path, search_dirs: list[Path] | None = None) -> int:
    """`nandsim gui FILE`: view one chip file and reload it when any .hdl around it changes."""
    from nandsim.gui.session import file_loader

    dirs = search_dirs or [path.parent, path.parent.parent]
    session = ChipSession(file_loader(path, dirs))
    session.reload()  # on error the window opens with the message and waits for a fix
    app = ViewerApp(session, watcher=FileWatcher(dirs))
    app.run(title=f"NAND Sim — {path.name}")
    return 0
