"""The viewer window: circuit canvas, optional HDL editor pane, header, footer, error banner.

`ViewerApp` takes pygame events through `handle()` and draws through `render()`,
so tests and the playtest hook can drive it headless (`SDL_VIDEODRIVER=dummy`)
exactly as a player would. `run()` is the real event loop around those two.
"""

from __future__ import annotations

import os
import textwrap
import time
from collections.abc import Callable
from pathlib import Path

import pygame

from nandsim.gui import theme
from nandsim.gui.camera import Camera, box_at, route_at
from nandsim.gui.canvas import Hover, draw_circuit, format_value
from nandsim.gui.editor import EditorError, EditorWidget
from nandsim.gui.model import breadcrumbs
from nandsim.gui.session import ChipSession, FileWatcher
from nandsim.gui.textbuffer import Pos, TextBuffer
from nandsim.gui.tips import tip_for
from nandsim.gui.valuefield import ValueField
from nandsim.hdl import HdlError

HEADER = 36
FOOTER = 26  # minimum footer height; it grows when the help wraps
HELP_SIZE = 12
HELP_PAD = 12
SEP = "  ·  "  # between help items: the only places the help line may wrap
CLICK_SLOP = 4  # pixels a press may move and still count as a click
POLL_SECONDS = 0.5
HELP = (
    "click input: toggle (right-click: count down, Enter: type a value, X: undefined)  ·  "
    "click part: open  ·  "
    "Backspace: up  ·  wheel: zoom  ·  drag: pan  ·  F: fit  ·  H: hex/dec"
)
CLOCK_HELP = "Space: step a cycle  ·  R: run / pause  ·  Shift+R: reset clock  ·  [ ]: speed"
BUILTIN_HELP = "B: built-in DFF / your DFF"
CLOCK_PAD = 8  # inside the clock panel and between its items
MAX_FRAME_DT = 0.25  # seconds; a longer stall (a drag, a slow rebuild) doesn't pile up cycles
EDITOR_HELP = (
    "Ctrl+S: save & build  ·  Ctrl+Z / Ctrl+Y: undo / redo  ·  Ctrl+/: comment  ·  "
    "Tab / Shift+Tab: indent  ·  Esc: back to the circuit"
)

# The speed goes by the character typed, not the key: on many layouts (Italian,
# German, French) brackets need AltGr and have no bracket keycode.
CLOCK_CHARS = {"[": "slower", "]": "faster"}


class ViewerApp:
    def __init__(
        self,
        session: ChipSession,
        size: tuple[int, int] = (1280, 800),
        watcher: FileWatcher | None = None,
        edit_path: Path | None = None,
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
        self._clock_buttons: list[tuple[pygame.Rect, str]] = []
        self.clock_rect: pygame.Rect | None = None  # the clock panel, once drawn
        self._last_frame: float | None = None
        self._held: set[int] = set()  # keys down now, so a held R doesn't repeat its toggle
        self._press_on_clock = False  # a press that began on the clock panel never pans
        self._last_poll = 0.0
        self._fitted_path: str | None = None
        self.quit_requested = False  # set to leave `run()` after the current frame
        self.edit_path = edit_path
        self.editor: EditorWidget | None = None
        self.value_field: ValueField | None = None  # a value being typed for an input pin
        self.field_rect: pygame.Rect | None = None  # where the value field was last drawn
        self.notice: str | None = None  # a one-off message; the game shows it in its sidebar
        if edit_path is not None:
            buffer = TextBuffer(edit_path.read_text())
            self.editor = EditorWidget(buffer, self.fonts, self.editor_rect)
            self._sync_error()
        self.fit()

    # ---- geometry --------------------------------------------------------

    @property
    def editor_width(self) -> int:
        if self.editor is None and self.edit_path is None:
            return 0
        return max(380, int((self.size[0] - self.left_width) * 0.45))

    @property
    def left_width(self) -> int:
        """Width of a panel left of the canvas (the game's sidebar); 0 in the viewer."""
        return 0

    @property
    def editor_rect(self) -> pygame.Rect:
        w, h = self.size
        ew = self.editor_width
        return pygame.Rect(w - ew, HEADER, ew, h - HEADER - self.footer_height)

    @property
    def canvas_area(self) -> tuple[float, float, float, float]:
        w, h = self.size
        x = float(self.left_width)
        return (
            x,
            float(HEADER),
            float(w - self.editor_width) - x,
            float(h - HEADER - self.footer_height),
        )

    @property
    def show_errors(self) -> bool:
        """Whether to display the current build error (the game hides it on untouched stubs)."""
        return True

    def in_canvas(self, pos: tuple[int, int]) -> bool:
        x, y, w, h = self.canvas_area
        return x <= pos[0] < x + w and y <= pos[1] < y + h

    @property
    def help_text(self) -> str:
        if self.editing:
            return EDITOR_HELP
        items = [HELP]
        if self.session.has_clock:
            items.append(CLOCK_HELP)
        if self.session.can_switch:
            items.append(BUILTIN_HELP)
        return SEP.join(items)

    def help_lines(self) -> list[str]:
        """The help line, wrapped between items to fit the window."""
        font = self.fonts.get(HELP_SIZE)
        room = self.size[0] - 2 * HELP_PAD
        return wrap_items(self.help_text.split(SEP), lambda s: font.size(s)[0] <= room)

    @property
    def footer_height(self) -> int:
        """At least FOOTER; taller when a narrow window wraps the help onto more lines."""
        lines = len(self.help_lines())
        return max(FOOTER, lines * self.fonts.get(HELP_SIZE).get_linesize() + 10)

    @property
    def editing(self) -> bool:
        return self.editor is not None and self.editor.focused

    @property
    def clock_height(self) -> int:
        """Height of the clock panel with its margin; 0 when the chip has no clock."""
        if not self.session.has_clock:
            return 0
        extra = len(self._memory_lines()) * (self.fonts.get(13).get_linesize() + CLOCK_PAD)
        return self.fonts.get(13, bold=True).get_linesize() + 6 + 3 * CLOCK_PAD + extra

    def _memory_lines(self) -> list[tuple[str, theme.Color]]:
        """What the clock panel shows of a CPU's memories: RAM, ports and any bus problem."""
        m = self.session.memories
        if m is None:
            return []
        chars = [m.cells.get((0, "main", k)) for k in range(16)]
        ram = "".join("·" if c is None else f"{c:X}" for c in reversed(chars))

        def port(v: int | None) -> str:
            return "·" if v is None else f"{v:X}"

        lines = [(
            f"{m.period()}   RAM 0 reg 0: {ram}   ROM port 0: {port(m.romport_out.get(0))}"
            f"   RAM port 0: {port(m.ramport.get((0, 0)))}",
            theme.TEXT_DIM,
        )]  # fmt: skip
        if self.session.bus_problem is not None:
            lines.append((f"bus {self.session.bus_problem}", theme.ERROR_TEXT))
        return lines

    def fit(self) -> None:
        if self.session.snapshot is not None:
            x, y, w, h = self.canvas_area
            room = self.clock_height  # so a fitted circuit starts below the clock panel
            self.cam.fit(self.session.snapshot.layout, (x, y + room, w, h - room))
            self._fitted_path = self.session.path

    def screen_of(self, layout_point: tuple[float, float]) -> tuple[int, int]:
        """Screen pixel of a layout point (used by tests to click on things)."""
        x, y = self.cam.to_screen(layout_point)
        return round(x), round(y)

    # ---- events ----------------------------------------------------------

    def handle(self, ev: pygame.event.Event) -> None:
        if ev.type == pygame.KEYUP:
            self._held.discard(ev.key)
        if self._field_event(ev):
            return
        if self.editor is not None and self._editor_event(ev):
            return
        if ev.type == pygame.MOUSEMOTION:
            if self._press is not None and pygame.BUTTON_LEFT in self._buttons(ev):
                dx, dy = ev.rel
                if (
                    self._dragged
                    or abs(ev.pos[0] - self._press[0]) + abs(ev.pos[1] - self._press[1])
                    > CLICK_SLOP
                ):
                    self._dragged = True  # too far to be a click
                    if not self._press_on_clock:
                        self.cam.pan(dx, dy)
            self.mouse = ev.pos
            self._update_hover()
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (1, 3):
            self._press, self._dragged = ev.pos, False
            self._press_on_clock = self._on_clock(ev.pos)
            self.mouse = ev.pos
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button in (1, 3):
            if self._press is not None and not self._dragged:
                self._click(ev.pos, right=ev.button == 3)
            self._press = None
        elif ev.type == pygame.MOUSEWHEEL:
            self.cam.zoom_at(self.mouse, 1.15**ev.y)
            self._update_hover()
        elif ev.type == pygame.KEYDOWN:
            self._key(ev.key, getattr(ev, "unicode", ""), getattr(ev, "mod", 0))
        elif ev.type == pygame.TEXTINPUT and ev.text in CLOCK_CHARS and self.session.has_clock:
            self.clock(CLOCK_CHARS[ev.text])

    def _field_event(self, ev: pygame.event.Event) -> bool:
        """Typing into the value field, if one is open. True if the event was used for it.

        Every key goes to the field while it is open, so typing `b` or `x` in a value
        never toggles hex mode or sets a pin undefined. A click anywhere closes it
        without setting anything, and still does what it would have done.
        """
        field = self.value_field
        if field is None:
            return False
        if ev.type == pygame.MOUSEBUTTONDOWN:
            self.value_field = None
            return False
        if ev.type == pygame.TEXTINPUT:
            field.type(ev.text)
            return True
        if ev.type != pygame.KEYDOWN:
            return False
        if ev.key == pygame.K_ESCAPE:
            self.value_field = None
        elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._apply_field(field)
        elif ev.key == pygame.K_BACKSPACE:
            field.backspace(everything=bool(getattr(ev, "mod", 0) & pygame.KMOD_CTRL))
        return True

    def _apply_field(self, field: ValueField) -> None:
        """Enter: set the pin to the typed value; an empty field just closes."""
        if field.empty:
            self.value_field = None
            return
        value = field.value()
        if value is None:
            return  # the field stays open and shows why
        self.value_field = None
        if self.session.at_top and self.session.netlist is not None:
            if field.pin in self.session.netlist.inputs:
                self.session.set_input(field.pin, value)
                self.on_action("set_value")

    def open_value_field(self, pin: str) -> None:
        """Start typing a value for one of the top chip's input pins."""
        assert self.session.netlist is not None
        self.value_field = ValueField(pin, len(self.session.netlist.inputs[pin]))

    def _editor_event(self, ev: pygame.event.Event) -> bool:
        """Route an event to the editor if it belongs there. True if consumed."""
        ed = self.editor
        assert ed is not None
        pos = getattr(ev, "pos", None)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            inside = pos is not None and ed.rect.collidepoint(pos)
            ed.focused = inside
            if inside:
                ed.handle(ev)
                return True
            return False
        if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP) and ed._dragging:
            ed.handle(ev)
            return True
        if ev.type == pygame.MOUSEWHEEL and ed.rect.collidepoint(self.mouse):
            ed.scroll(-ev.y * 3)
            return True
        if ev.type == pygame.MOUSEMOTION and pos is not None and ed.rect.collidepoint(pos):
            self.mouse = pos
            self.hover = Hover()
            return True
        if not ed.focused or ev.type not in (pygame.KEYDOWN, pygame.TEXTINPUT):
            return False
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            ed.focused = False
            return True
        action = ed.handle(ev)
        if action is not None:
            self.on_editor_action(action)
        return True

    def on_action(self, name: str) -> None:
        """Hook for circuit actions ("toggle", "set_value", "open_part", "up"); the tour listens."""

    def on_editor_action(self, action: str) -> None:
        """Editor shortcuts the host handles: "save" (Ctrl+S), "run" (Ctrl+Enter)."""
        if action == "save":
            self.save()

    def save(self) -> None:
        """Write the editor's text, rebuild the circuit and mark any error in the editor."""
        assert self.editor is not None and self.edit_path is not None
        tmp = self.edit_path.with_suffix(self.edit_path.suffix + ".tmp")
        tmp.write_text(self.editor.buffer.text)
        os.replace(tmp, self.edit_path)
        self.editor.buffer.mark_saved()
        if self.watcher is not None:
            self.watcher.changed()  # absorb our own write
        self._rebuild()

    def _rebuild(self) -> None:
        built = self.session.reload()
        self._sync_error()
        if built or self.session.path != self._fitted_path:
            self.fit()  # a new circuit may have a different size
        self._update_hover()

    def _sync_error(self) -> None:
        """Show the session's error in the editor when it points into the edited file."""
        if self.editor is None or self.edit_path is None:
            return
        err = self.session.error if self.show_errors else None
        if err is not None and err.pos is not None and _same_file(err.pos.file, self.edit_path):
            self.editor.set_error(
                EditorError(Pos.from_source(err.pos.line, err.pos.col), err.message)
            )
        else:
            self.editor.set_error(None)

    @staticmethod
    def _buttons(ev: pygame.event.Event) -> set[int]:
        pressed = getattr(ev, "buttons", (0, 0, 0))
        return {i + 1 for i, b in enumerate(pressed) if b}

    def _click(self, pos: tuple[int, int], right: bool) -> None:
        for rect, path in self._crumbs:
            if rect.collidepoint(pos):
                self._navigate(path)
                return
        if self._on_clock(pos):
            for rect, action in self._clock_buttons:
                if rect.collidepoint(pos) and not right:
                    self.clock(action)
            return  # the panel covers the circuit: a click on it never reaches a part
        snap = self.session.snapshot
        if snap is None or not self.in_canvas(pos):
            return
        key = box_at(snap.layout, self.cam.to_layout(pos))
        if key is None:
            return
        kind, ident = key
        if kind == "in" and self.session.at_top:
            self.session.toggle(str(ident), -1 if right else 1)
            self.on_action("toggle")
        elif kind == "part" and not right:
            if self.session.open(snap.view.part(int(ident))):
                self.fit()
                self.on_action("open_part")
        self._update_hover()

    def _key(self, key: int, char: str = "", mod: int = 0) -> None:
        on_input = self.hover.node is not None and self.hover.node[0] == "in"
        plain = not mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT | pygame.KMOD_META)
        if on_input and plain and self.session.at_top and self.session.netlist is not None:
            # Enter, or the first character of a value, opens the field; that character
            # then arrives as the TEXTINPUT event that follows its KEYDOWN.
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER) or (char and char in "0123456789-"):
                assert self.hover.node is not None
                self.open_value_field(str(self.hover.node[1]))
                return
        if self.session.has_clock and plain:
            if key == pygame.K_r:
                if key not in self._held:  # a held key repeats: toggle once per press
                    self._held.add(key)
                    self.clock("reset" if mod & pygame.KMOD_SHIFT else "run")
                return
            if key == pygame.K_SPACE:  # held, it keeps stepping: that one is useful
                self.clock("step")
                return
        if key in (pygame.K_BACKSPACE, pygame.K_ESCAPE):
            if self.session.up():
                self.fit()
                self.on_action("up")
        elif key == pygame.K_f:
            self.fit()
        elif key == pygame.K_h:
            self.hex_mode = not self.hex_mode
        elif key == pygame.K_b and plain and self.session.can_switch:
            self.toggle_builtins()
        elif key == pygame.K_x and self.hover.node and self.hover.node[0] == "in":
            if self.session.at_top:
                self.session.set_input(str(self.hover.node[1]), None)

    def toggle_builtins(self) -> None:
        """Run DFF parts as the built-in flip-flop or as the player's own DFF."""
        why = self.session.toggle_builtins()
        if why is not None:
            self.notice = why  # nothing changed: the view stays where it was
        else:
            if self.session.builtins:
                self.notice = "DFF parts run as the built-in flip-flop again: faster, same results."
            else:
                self.notice = "DFF parts now run as your own DFF: click one to see its latches."
            self.fit()  # a new circuit: the DFF boxes changed size
            self.on_action("builtins")
        self._update_hover()

    def _on_clock(self, pos: tuple[int, int]) -> bool:
        """Whether `pos` is on the clock panel as last drawn, and the chip still has a clock."""
        rect = self.clock_rect
        return rect is not None and self.session.has_clock and bool(rect.collidepoint(pos))

    @property
    def clock_paused(self) -> bool:
        """Whether something on top (the game's menus) holds the clock; never in the viewer."""
        return False

    def clock(self, action: str) -> None:
        """A clock control: "step", "run" (also pauses), "reset", "slower" or "faster"."""
        s = self.session
        if not s.has_clock:
            return
        if action == "step":
            s.running = False  # stepping by hand pauses a running clock
            s.step()
        elif action == "run":
            s.toggle_run()
        elif action == "reset":
            s.reset_clock()
        elif action in ("slower", "faster"):
            s.change_speed(-1 if action == "slower" else 1)
        self.on_action(f"clock_{action}")

    def _navigate(self, path: str) -> None:
        if path != self.session.path:
            self.session.goto(path)
            self.fit()
            self.on_action("up")  # breadcrumbs only lead to ancestors

    def _update_hover(self) -> None:
        snap = self.session.snapshot
        if snap is None or not self.in_canvas(self.mouse) or self._on_clock(self.mouse):
            self.hover = Hover()
            return
        p = self.cam.to_layout(self.mouse)
        node = box_at(snap.layout, p)
        route = None if node else route_at(snap.layout, p, 5 / self.cam.scale)
        self.hover = Hover(node, route)

    # ---- time ------------------------------------------------------------

    def tick(self, now: float | None = None) -> None:
        """Run the clock if it is running, then poll for changed files and reload."""
        now = time.monotonic() if now is None else now
        if self._last_frame is not None and not self.clock_paused:
            self.session.advance(min(now - self._last_frame, MAX_FRAME_DT))
        self._last_frame = now
        if self.watcher is None or now - self._last_poll < POLL_SECONDS:
            return
        self._last_poll = now
        if self.watcher.changed():
            if self.editor is not None and self.edit_path is not None:
                on_disk = self.edit_path.read_text()
                if not self.editor.buffer.dirty and on_disk != self.editor.buffer.text:
                    self.editor.buffer.set_text(on_disk)  # edited elsewhere, nothing to lose
            self._rebuild()

    # ---- drawing ---------------------------------------------------------

    def render(self, surf: pygame.Surface) -> None:
        surf.fill(theme.BG)
        draw_circuit(surf, self.session, self.cam, self.fonts, self.hover, self.hex_mode)
        if self.session.snapshot is None:
            x, y, w, h = self.canvas_area
            t = self.fonts.get(16).render("nothing to draw yet", True, theme.TEXT_DIM)
            surf.blit(t, (x + (w - t.get_width()) / 2, y + h / 2 - t.get_height()))
        if self.editor is not None:
            self.editor.rect = self.editor_rect
            self.editor.render(surf)
            r = self.editor.rect
            border = theme.ACCENT if self.editor.focused else theme.PART_BORDER
            pygame.draw.line(surf, border, (r.x - 1, r.y), (r.x - 1, r.bottom), 2)
        self._draw_clock(surf)
        self._draw_value_field(surf)
        self._draw_header(surf)
        self._draw_notice(surf)
        self._draw_footer(surf)
        self._draw_tooltip(surf)

    def _draw_notice(self, surf: pygame.Surface) -> None:
        """The last notice, under the header at the canvas's left; the game uses its sidebar."""
        if not self.notice:
            return
        x, y, w, _ = self.canvas_area
        font = self.fonts.get(13)
        cols = max(20, int(w - 24) // font.size("M")[0])
        for i, line in enumerate(textwrap.wrap(self.notice, cols)):
            t = font.render(line, True, theme.WIRE_X)
            surf.blit(t, (x + 12, y + 8 + i * font.get_linesize()))

    def _draw_value_field(self, surf: pygame.Surface) -> None:
        """The value field, just under its input pin, kept inside the canvas."""
        field = self.value_field
        snap = self.session.snapshot
        box = None if snap is None else snap.layout.boxes.get(("in", field.pin)) if field else None
        self.field_rect = None
        if field is None or box is None or not self.session.at_top:
            self.value_field = None  # its pin is gone: rebuilt, or navigated away
            return
        font = self.fonts.get(15)
        small = self.fonts.get(12)
        label = f"{field.pin}[{field.width}] = " if field.width > 1 else f"{field.pin} = "
        typed = font.render(label + field.text + "▏", True, theme.TEXT)
        hint = small.render(field.hint, True, theme.WIRE_X if field.error else theme.TEXT_DIM)
        w = max(typed.get_width(), hint.get_width()) + 20
        h = typed.get_height() + hint.get_height() + 16
        cx, cy, cw, ch = (round(v) for v in self.canvas_area)
        x, y = self.cam.to_screen((box.x, box.bottom))
        x = max(cx + 4, min(round(x), cx + cw - w - 4))
        y = max(cy + 4, min(round(y) + 6, cy + ch - h - 4))
        rect = self.field_rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surf, theme.PANEL, rect, border_radius=6)
        border = theme.WIRE_X if field.error else theme.ACCENT
        pygame.draw.rect(surf, border, rect, 2, border_radius=6)
        surf.blit(typed, (x + 10, y + 6))
        surf.blit(hint, (x + 10, y + 10 + typed.get_height()))

    def _draw_clock(self, surf: pygame.Surface) -> None:
        """The clock panel, top right of the canvas, for chips with DFFs.

        Left to right: the cycle count, Reset, Run (Pause while running), Step, and
        the speed between − and +.
        """
        self._clock_buttons = []
        self.clock_rect = None
        s = self.session
        if not s.has_clock:
            return
        bold, plain = self.fonts.get(13, bold=True), self.fonts.get(13)
        running = s.running
        items: list[tuple[str | None, pygame.Surface]] = [
            (None, plain.render(f"cycle {s.cycle}", True, theme.TEXT)),
            ("reset", bold.render("Reset", True, theme.TEXT)),
            (
                "run",
                bold.render(
                    "Pause" if running else "Run", True, theme.BG if running else theme.TEXT
                ),
            ),
            ("step", bold.render("Step", True, theme.TEXT)),
            ("slower", bold.render("−", True, theme.TEXT)),
            (None, plain.render(f"{s.speed}/s", True, theme.TEXT_DIM)),
            ("faster", bold.render("+", True, theme.TEXT)),
        ]
        bh = bold.get_linesize() + 6
        widths = [t.get_width() + (2 * CLOCK_PAD if a else 0) for a, t in items]
        x0, y0, cw, _ = self.canvas_area
        notes = [plain.render(text, True, color) for text, color in self._memory_lines()]
        width = sum(widths) + CLOCK_PAD * (len(items) + 1)
        width = max([width] + [n.get_width() + 2 * CLOCK_PAD for n in notes])
        height = bh + 2 * CLOCK_PAD + sum(n.get_height() + CLOCK_PAD for n in notes)
        panel = pygame.Rect(0, 0, width, height)
        panel.topright = (round(x0 + cw) - CLOCK_PAD, round(y0) + CLOCK_PAD)
        panel.left = max(panel.left, round(x0) + CLOCK_PAD)  # a narrow canvas: stay off the sidebar
        pygame.draw.rect(surf, theme.PANEL, panel, border_radius=6)
        pygame.draw.rect(surf, theme.PART_BORDER, panel, 1, border_radius=6)
        x, y = panel.x + CLOCK_PAD, panel.y + CLOCK_PAD
        for (action, text), w in zip(items, widths, strict=True):
            rect = pygame.Rect(x, y, w, bh)
            if action is not None:
                active = action == "run" and running
                hot = rect.collidepoint(self.mouse)
                pygame.draw.rect(surf, theme.ACCENT if active else theme.BG, rect, border_radius=4)
                edge = theme.ACCENT if active or hot else theme.PART_BORDER
                pygame.draw.rect(surf, edge, rect, 1, border_radius=4)
                self._clock_buttons.append((rect, action))
            surf.blit(text, text.get_rect(center=rect.center))
            x += w + CLOCK_PAD
        y += bh + CLOCK_PAD
        for note in notes:
            surf.blit(note, (panel.x + CLOCK_PAD, y))
            y += note.get_height() + CLOCK_PAD
        self.clock_rect = panel

    def _draw_header(self, surf: pygame.Surface) -> None:
        w = self.size[0]
        pygame.draw.rect(surf, theme.PANEL, (0, 0, w, HEADER))
        font = self.fonts.get(15, bold=True)
        x = self.left_width + 12
        end = x  # where the breadcrumbs end
        self._crumbs = []
        crumbs = breadcrumbs(self.session.path) if self.session.path else []
        for i, (label, path) in enumerate(crumbs):
            current = i == len(crumbs) - 1
            t = font.render(label, True, theme.TEXT if current else theme.ACCENT)
            rect = t.get_rect(topleft=(x, (HEADER - t.get_height()) // 2))
            surf.blit(t, rect)
            end = rect.right
            if not current:
                self._crumbs.append((rect.inflate(6, 6), path))
                sep = font.render("  ›  ", True, theme.TEXT_DIM)
                surf.blit(sep, (rect.right, rect.y))
                x = rect.right + sep.get_width()
        right = w - self.editor_width
        notes: list[str] = []
        if self.session.can_switch and not self.session.builtins:
            notes.append("DFFs: yours (B: built-in)")
        if not self.session.at_top:
            notes.append("inputs are set at the top level")
        small = self.fonts.get(12)
        while notes:  # never over the breadcrumbs: drop the last note until the rest fits
            note = small.render("  ·  ".join(notes), True, theme.TEXT_DIM)
            left = right - note.get_width() - 12
            if left >= end + 24:
                surf.blit(note, (left, (HEADER - note.get_height()) // 2))
                break
            notes.pop()
        if self.editor is not None and self.edit_path is not None:
            dirty = self.editor.buffer.dirty
            label = f"{self.edit_path.name}{'  ● unsaved' if dirty else ''}"
            t = self.fonts.get(13, bold=True).render(
                label, True, theme.WIRE_X if dirty else theme.TEXT_DIM
            )
            surf.blit(t, (right + 12, (HEADER - t.get_height()) // 2))

    def _draw_footer(self, surf: pygame.Surface) -> None:
        w, h = self.size
        err = self.session.error if self.show_errors else None
        if err is not None:
            font = self.fonts.get(13)
            note = (
                "(showing the last version that compiled)"
                if self.session.snapshot is not None
                else "(the circuit appears once the chip compiles)"
            )
            tip = tip_for(err.message)
            left = self.left_width
            cols = max(20, (w - self.editor_width - left - 24) // font.size("M")[0])
            raw = _short_error(err).splitlines() + ([f"Tip: {tip}"] if tip else []) + [note]
            lines = [part for line in raw for part in textwrap.wrap(line, cols) or [""]]
            height = 10 + len(lines) * (font.get_linesize())
            top = h - self.footer_height - height
            pygame.draw.rect(
                surf, theme.ERROR_BG, (left, top, w - self.editor_width - left, height)
            )
            for i, line in enumerate(lines):
                t = font.render(line, True, theme.ERROR_TEXT)
                surf.blit(t, (left + 12, top + 5 + i * font.get_linesize()))
        fh = self.footer_height
        pygame.draw.rect(surf, theme.PANEL, (0, h - fh, w, fh))
        font = self.fonts.get(HELP_SIZE)
        lines = self.help_lines()
        y = h - fh + (fh - len(lines) * font.get_linesize()) // 2
        for i, line in enumerate(lines):
            t = font.render(line, True, theme.TEXT_DIM)
            surf.blit(t, (HELP_PAD, y + i * font.get_linesize()))

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

    def before_quit(self) -> None:
        """Hook run once before the window closes; the game keeps unsaved text here."""

    def run(self, title: str = "NAND Sim") -> None:
        pygame.init()
        screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption(title)
        pygame.key.start_text_input()
        pygame.key.set_repeat(400, 35)
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.quit_requested = True
                    break
                if ev.type == pygame.VIDEORESIZE:
                    self.size = (ev.w, ev.h)
                    self.fit()
                    continue
                self.handle(ev)
            if self.quit_requested:  # the window closed, or a menu chose Quit
                self.before_quit()
                pygame.quit()
                return
            self.tick()
            self.render(screen)
            pygame.display.flip()
            clock.tick(60)


def wrap_items(items: list[str], fits: Callable[[str], bool]) -> list[str]:
    """Pack items into lines joined by SEP, starting a new line when one would not fit.

    An item too long for a line on its own is wrapped between its words; a single
    word wider than the line is left whole.
    """
    lines: list[str] = []
    for item in items:
        if lines and fits(lines[-1] + SEP + item):
            lines[-1] += SEP + item
        elif fits(item):
            lines.append(item)
        else:
            words = item.split(" ")
            lines.append(words[0])
            for word in words[1:]:
                if fits(lines[-1] + " " + word):
                    lines[-1] += " " + word
                else:
                    lines.append(word)
    return lines


def _short_error(err: HdlError) -> str:
    """The error with just the file name: players don't need the save directory's path."""
    if err.pos is None:
        return str(err)
    return f"{Path(err.pos.file).name}:{err.pos.line}:{err.pos.col}: error: {err.message}"


def _same_file(a: str, b: Path) -> bool:
    try:
        return Path(a).resolve() == b.resolve()
    except OSError:
        return False


def open_viewer(path: Path, search_dirs: list[Path] | None = None, edit: bool = True) -> int:
    """`nandsim gui FILE`: edit and view one chip file; reloads when any .hdl around it changes."""
    from nandsim.gui.game import level_program
    from nandsim.gui.session import file_loader
    from nandsim.testing import find_level

    dirs = search_dirs or [path.parent, path.parent.parent]
    # A level's chip runs its demo program on the clock panel, as in the game.
    session = ChipSession(file_loader(path, dirs), program=level_program(find_level(path.stem)))
    session.reload()  # on error the window opens with the message and waits for a fix
    app = ViewerApp(session, watcher=FileWatcher(dirs), edit_path=path if edit else None)
    app.run(title=f"NAND Sim — {path.name}")
    return 0
