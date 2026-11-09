"""The game screen: level list and brief on the left, circuit in the middle, editor and
test results on the right.

It reuses `ViewerApp` for the canvas, the editor pane, navigation and error display,
and adds the level sidebar, the results panel, the "Run tests" action and the guided
tour's bubbles (F1 replays the tour), and plays the sound effects. Menus sit on
top: the title screen at start, and the pause menu on Esc, from which the game can
be reset, the sound muted or turned up, and the chip in the editor exported under
a name of its own, as a part every level may use. The sidebar lists those chips,
each with a × button that deletes it.
"""

from __future__ import annotations

from pathlib import Path

import pygame

from nandsim.gui import theme
from nandsim.gui.app import HEADER, ViewerApp
from nandsim.gui.brief import brief_lines
from nandsim.gui.canvas import Hover
from nandsim.gui.editor import EditorWidget
from nandsim.gui.game import GameState, group_label
from nandsim.gui.guide import Bubble, draw_bubble
from nandsim.gui.menu import BACK, Menu, MenuItem, dim
from nandsim.gui.model import child_path
from nandsim.gui.saves import SaveStore
from nandsim.gui.session import ChipSession
from nandsim.gui.settings import Settings
from nandsim.gui.sound import Sounds
from nandsim.gui.textbuffer import Pos, TextBuffer
from nandsim.gui.tutorial import Tour, load_steps
from nandsim.testing import Level, load_levels

SIDEBAR = 260
RESULTS_H = 190
ROW_H = 26
CHIP_ROW_H = 22  # a row of the "Your chips" list
BUTTON_W = 210

SILENT_ACTIONS = {"mute", "volume"}  # these play their own preview, if any

GLYPH = {"solved": "✓", "open": "○", "locked": "–"}
CHEVRON = {True: "▾", False: "▸"}  # a group header, open or closed
BRIEF_BOTTOM = 6  # gap between the brief and the footer
LIST_MIN_ROWS = 5  # the level list leaves the brief its room, but shows at least this many rows
CHIPS_MAX_ROWS = 4  # "Your chips" shows this many rows at most, and scrolls past that
BRIEF_WHEEL_LINES = 3  # lines of brief text one wheel notch scrolls
BRIEF_KEEP_LINES = 3  # in a short window, "Your chips" shrinks to leave the brief this many


def clamp_scroll(scroll: int, content: int, view: int) -> int:
    """A scroll offset that keeps the view inside the content."""
    return max(0, min(scroll, content - view))


def scroll_into_view(scroll: int, top: int, height: int, view: int) -> int:
    """The nearest scroll offset that shows the row from `top` to `top + height`."""
    if top < scroll:
        return top
    if top + height > scroll + view:
        return top + height - view
    return scroll


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
        self.brief_cut = False  # the window was too short for the whole brief: it scrolls
        self.brief_scroll = 0  # pixels of the brief scrolled past
        self.brief_view = pygame.Rect(0, 0, 0, 0)  # the visible part of the brief, as last drawn
        self._brief_for: str | None = None  # the level whose brief `brief_scroll` belongs to
        self._chips_rect: pygame.Rect | None = None  # the "Your chips" list, when shown
        self.chips_scroll = 0  # pixels of the chip list scrolled past, in whole rows
        self.chips_view = pygame.Rect(0, 0, 0, 0)  # its visible rows, as last drawn
        self._show_chip: str | None = None  # a chip just exported, to scroll into view
        session = ChipSession(self.game.loader(), program=self.game.program())
        session.reload()
        super().__init__(session, size=size)
        self.edit_path = Path(self.game.path)
        self.editor = EditorWidget(TextBuffer(self.game.text()), self.fonts, self.editor_rect)
        self.settings = Settings.load(store.settings_path)
        self.sounds = Sounds(self.settings)
        self.sounds.load()  # synthesized once, at startup; silent without an audio device
        warnings = [w for w in (store.warning, self.tour.warning, self.settings.warning) if w]
        self.notice: str | None = "; ".join(warnings) or None
        self._attempted = store.has_save(self.game.current)
        self._rows: list[tuple[pygame.Rect, Level]] = []  # level rows, as last drawn
        self._group_rows: list[tuple[pygame.Rect, str]] = []  # group headers, as last drawn
        self.expanded: set[str] = set()  # level groups open in the sidebar
        self._expanded_for: tuple[str, frozenset[str]] | None = None
        self.list_scroll = 0  # pixels of the level list scrolled past, in whole rows
        self.list_rect = pygame.Rect(0, 0, 0, 0)  # the visible part of the list, as last drawn
        self._scrolled_to: str | Level | None = None  # the row last scrolled into view
        self._exported = store.exported()  # the player's exported chips, for the sidebar
        self._chip_rows: list[tuple[pygame.Rect, str]] = []  # × buttons, as last drawn
        self._export_names: dict[str, str] = {}  # level -> name it was last exported as
        self._pending_export: tuple[str, str] | None = None  # waiting for "Replace it"
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

    def toggle_group(self, group: str) -> None:
        """Open or close a level group in the sidebar."""
        self._sync_expanded()
        if group in self.expanded:
            self.expanded.discard(group)
            self.sounds.play("back")
        else:
            self.expanded.add(group)
            self.sounds.play("select")

    def _sync_expanded(self) -> None:
        """Back to the default open groups when the current group or the solved levels change.

        Between those changes the player's own choices stay as they are.
        """
        key = (self.game.current.group, self.game.store.solved)
        if key != self._expanded_for:
            self._expanded_for = key
            self.expanded = self.game.default_expanded()

    def _load_current(self) -> None:
        """Show the current level: its text in the editor, its circuit on the canvas."""
        assert self.editor is not None
        self.editor.buffer.set_text(self.game.text())
        self.editor.focused = True
        self._attempted = self.game.store.has_save(self.game.current)
        self.edit_path = Path(self.game.path)
        builtins = self.session.builtins  # the player's choice holds from level to level
        self.session = ChipSession(self.game.loader(), program=self.game.program())
        self.session.builtins = builtins
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
        self._exported = self.game.store.exported()
        self._export_names = {}
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
                    MenuItem("Export this chip as…", "export"),
                    MenuItem("Main menu", "title"),
                    MenuItem("Reset game…", "reset"),
                    *self._sound_items(),
                    MenuItem("Quit", "quit"),
                ],
            )
        )

    def _title_menu(self) -> Menu:
        started = self.game.store.has_progress()
        items = [MenuItem("Continue" if started else "Play", "play")]
        if started:
            items.append(MenuItem("Reset game…", "reset"))
        items += [*self._sound_items(), MenuItem("Quit", "quit")]
        msg = "Build a computer, starting from a single kind of gate: the Nand."
        return Menu("NAND Sim", items, message=msg, big_title=True)

    def _sound_items(self) -> list[MenuItem]:
        return [MenuItem(*pair) for pair in self._sound_labels()]

    def _sound_labels(self) -> list[tuple[str, str]]:
        on = "Off" if self.settings.muted else "On"
        return [
            (f"Sound: {on}", "mute"),
            (f"Volume: {round(self.settings.volume * 100)}%", "volume"),
        ]

    def change_sound(self, action: str) -> None:
        """Mute or unmute, or step the volume; save it and let the player hear it.

        The labels of the open menu change in place, so the selection stays put.
        """
        if action == "mute":
            self.settings.muted = not self.settings.muted
        else:
            self.settings.volume = self.settings.next_volume()
        try:
            self.settings.save(self.game.store.settings_path)
        except OSError as e:
            self.notice = f"Couldn't save the sound settings: {e.strerror or e}"
        labels = dict((a, label) for label, a in self._sound_labels())
        for item in self.menus[-1].items if self.menus else []:
            item.label = labels.get(item.action, item.label)
        self.sounds.play("select")  # a preview at the new volume; silent once muted

    def _confirm_reset_menu(self) -> Menu:
        where = _home_short(self.game.store.backups)
        msg = (
            "Every chip you wrote, the chips you exported, the levels you solved and the "
            "tour start over from the first level.\n\n"
            f"Your files aren't deleted: they move to {where}."
        )
        # Cancel comes first, so Enter on a menu opened by mistake is harmless.
        items = [MenuItem("Cancel", BACK), MenuItem("Reset the game", "confirm_reset", True)]
        return Menu("Reset the game?", items, message=msg)

    def _export_menu(self) -> Menu:
        level = self.game.current.name
        where = _home_short(self.game.store.exports)
        msg = (
            "Name the chip in the editor. Every level can then use it as a part, "
            f"like a chip you solved: Name(...).\n\nIt is written to {where}."
        )
        items = [MenuItem("Export", "export_named"), MenuItem("Cancel", BACK)]
        name = self._export_names.get(level, f"My{level}")
        return Menu("Export this chip", items, message=msg, text=name, allowed=r"\w")

    def _confirm_delete_menu(self, name: str) -> Menu:
        users = self.game.store.users_of(name)
        msg = "No level will be able to use it any more."
        if users:
            them = (
                "they won't build until you change them"
                if len(users) > 1
                else ("it won't build until you change it")
            )
            msg += f"\n\nUsed by {', '.join(users)}: {them}."
        msg += f"\n\nThe file isn't destroyed: it moves to {_home_short(self.game.store.backups)}."
        # Cancel comes first, so Enter on a dialog opened by mistake is harmless.
        items = [MenuItem("Cancel", BACK), MenuItem("Delete it", f"confirm_delete:{name}", True)]
        return Menu(f"Delete {name}?", items, message=msg)

    def _confirm_export_menu(self, name: str) -> Menu:
        path = self.game.store.export_path(name)
        msg = (
            f"You already exported a different {name}, in {_home_short(path)}. "
            "Levels that use it will use the new one."
        )
        items = [MenuItem("Cancel", BACK), MenuItem("Replace it", "confirm_export", True)]
        return Menu(f"Replace {name}?", items, message=msg)

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
        elif action == "export":
            self.menus.append(self._export_menu())
        elif action == "export_named":
            self.export_chip(self.menus[-1])
        elif action == "confirm_export" and self._pending_export is not None:
            self._write_export(*self._pending_export)
        elif action in ("mute", "volume"):
            self.change_sound(action)
        elif action.startswith("confirm_delete:"):
            self.delete_chip(action.split(":", 1)[1])
        elif action == "quit":
            self.quit_requested = True

    def export_chip(self, dialog: Menu) -> None:
        """Export the editor's text under the name typed in `dialog`, once it builds.

        The editor's text, saved or not, is what the player sees, so that is what goes
        out, renamed to the typed name. A problem (a taken name, a build error) shows
        in the dialog; replacing a different chip of that name asks first.
        """
        assert self.editor is not None and dialog.text is not None
        store, name = self.game.store, dialog.text
        try:
            text = store.prepare_export(name, self.editor.buffer.text)
        except ValueError as e:
            dialog.error = str(e)
            return
        path = store.export_path(name)
        if path.is_file():
            try:
                same = path.read_text(encoding="utf-8") == text
            except (OSError, UnicodeDecodeError):
                same = False
            if not same:
                self._pending_export = (name, text)
                self.menus.append(self._confirm_export_menu(name))
                return
        self._write_export(name, text)

    def delete_chip(self, name: str) -> None:
        """Take an exported chip out of the library, then rebuild what is on screen."""
        try:
            gone = self.game.store.delete_export(name)
        except OSError as e:
            self.notice = f"Couldn't delete {name}: {e.strerror or e}"
        else:
            self.notice = f"Deleted {name}. Its file is in {_home_short(gone.parent.parent)}"
            self._export_names = {k: v for k, v in self._export_names.items() if v != name}
        self._exported = self.game.store.exported()
        self._close_menus()
        self._rebuild()  # the circuit on screen may have used it

    def _write_export(self, name: str, text: str) -> None:
        self._pending_export = None
        try:
            self.game.store.export(name, text)
        except OSError as e:
            self.notice = f"Couldn't export {name}: {e.strerror or e}"
        else:
            self._export_names[self.game.current.name] = name
            self._show_chip = name
            self.notice = f"Exported {name}. Every level can now use it as a part: {name}(...)"
            self.tour_event("export")
        self._exported = self.game.store.exported()
        self._close_menus()

    def save(self) -> None:
        assert self.editor is not None
        self.game.save(self.editor.buffer.text)
        self.editor.buffer.mark_saved()
        self._attempted = True
        self._rebuild()
        if self.session.error is not None and self.show_errors:
            self.sounds.play("error")
        self.tour_event("save")
        if self.session.error is None:
            self.tour_event("build_ok")

    def run_tests(self) -> None:
        assert self.editor is not None
        report = self.game.run_tests(self.editor.buffer.text)
        self.editor.buffer.mark_saved()
        self._attempted = True
        self._rebuild()
        self.sounds.play("solved" if report.newly_solved else "pass" if report.passed else "fail")
        self.tour_event("run_tests")
        if self.session.error is None:
            self.tour_event("build_ok")  # Ctrl+Enter builds too, so it counts as building
        if report.passed:
            self.tour_event("solved")

    def tour_event(self, name: str, detail: str | None = None) -> None:
        self.tour.event(self.game.current.name, name, detail)

    def on_action(self, name: str) -> None:
        if name in ("toggle", "set_value"):  # a typed value sounds like a click on the pin
            self.sounds.play("toggle")
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

    @property
    def clock_paused(self) -> bool:
        return bool(self.menus)  # the pause menu, and every other one, stops the clock

    def handle(self, ev: pygame.event.Event) -> None:
        if ev.type == pygame.KEYUP:
            self._held.discard(ev.key)  # menus take the event below; R must not stay "held"
        if self.menus:
            if hasattr(ev, "pos"):
                self.mouse = ev.pos
            self._menu_event(ev)
            return
        if self._field_event(ev):  # Esc closes a value field before it opens the menu
            return
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.open_pause()
            self.sounds.play("select")
            return
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F1:
            self.replay_tour()
            return
        if self._bubble_event(ev):
            return
        if ev.type == pygame.MOUSEWHEEL and self.list_rect.collidepoint(self.mouse):
            self.scroll_list(-ev.y)  # wheel up shows earlier levels
            return
        if ev.type == pygame.MOUSEWHEEL and self.chips_view.collidepoint(self.mouse):
            self.chips_scroll = max(0, self.chips_scroll - ev.y * CHIP_ROW_H)
            return
        if ev.type == pygame.MOUSEWHEEL and self.brief_view.collidepoint(self.mouse):
            step = BRIEF_WHEEL_LINES * self.fonts.get(13).get_linesize()
            self.brief_scroll = max(0, self.brief_scroll - ev.y * step)  # clamped when drawn
            return
        if ev.type == pygame.MOUSEWHEEL and self.mouse[0] < SIDEBAR:
            return  # over a sidebar heading or gap: nothing to scroll, and not the canvas
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.button_rect.collidepoint(ev.pos):
                self.run_tests()
                return
            for rect, name in self._chip_rows:
                if rect.collidepoint(ev.pos):
                    self._open_menu(self._confirm_delete_menu(name))
                    self.sounds.play("select")
                    return
            for rect, level in self._rows:
                if rect.collidepoint(ev.pos):
                    if level is not self.game.current:
                        self.open_level(level)
                    return
            for rect, group in self._group_rows:
                if rect.collidepoint(ev.pos):
                    self.toggle_group(group)
                    return
            if ev.pos[0] < SIDEBAR or self.results_rect.collidepoint(ev.pos):
                return
        super().handle(ev)

    def _menu_event(self, ev: pygame.event.Event) -> None:
        """Pass an event to the topmost menu, act on its answer, and sound it out.

        Moving the selection ticks, choosing blips up, going back blips down, and a
        choice the dialog refuses (an export name, say) sounds like an error.
        """
        menu = self.menus[-1]
        selected, error = menu.selected, menu.error
        action = menu.handle(ev)
        if action is None:
            if menu.selected != selected:
                self.sounds.play("move")
            return
        self.menu_action(action)
        if menu.error and menu.error != error:
            self.sounds.play("error")
        elif action == BACK:
            self.sounds.play("back")
        elif action not in SILENT_ACTIONS:
            self.sounds.play("select")

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
            rects = [r for r, _ in self._group_rows] + [r for r, _ in self._rows]
            return rects[0].unionall(rects[1:]) if rects else None
        if kind == "level":
            row = next((r for r, lv in self._rows if lv.name == arg), None)
            if row is not None:
                return row
            # In a closed group: point at its header, which the player clicks first.
            group = next((lv.group for lv in self.game.levels if lv.name == arg), None)
            return next((r for r, g in self._group_rows if g == group), None)
        if anchor == "brief":
            return self._brief_rect
        if anchor == "chips":
            return self._chips_rect
        if anchor == "clock":
            return self.clock_rect if self.session.has_clock else None
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
        if anchor == "wire":
            r = self._wire_rect()
            return r.clip(canvas) if r is not None and r.colliderect(canvas) else canvas
        return None

    def _wire_rect(self) -> pygame.Rect | None:
        """Around the first internal wire (from a part's output to another part) and both parts.

        The parts are included so the bubble never covers the chips the wire joins.
        """
        snap = self.session.snapshot
        if snap is None:
            return None
        route = next(
            (
                r
                for r in snap.layout.routes
                if r.edge.src.kind == "part" and r.edge.dst.kind == "part" and r.points
            ),
            None,
        )
        if route is None:
            return None
        boxes = [snap.layout.boxes[("part", e.part)] for e in (route.edge.src, route.edge.dst)]
        corners = [p for b in boxes for p in ((b.x, b.y), (b.right, b.bottom))] + route.points
        pts = [self.screen_of(p) for p in corners]
        xs, ys = [x for x, _ in pts], [y for _, y in pts]
        return pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

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

    def _draw_notice(self, surf: pygame.Surface) -> None:
        """The game shows its notice in the sidebar instead (see `_draw_sidebar`)."""

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
        if clear is not None and self.field_rect is not None:
            clear = clear.union(self.field_rect)  # the value being typed stays readable
        self.bubble = draw_bubble(
            surf, self.fonts, step, self.tour.position(step), anchor, bounds, self.mouse, clear
        )

    def _draw_sidebar(self, surf: pygame.Surface) -> None:
        h = self.size[1]
        pygame.draw.rect(surf, theme.PANEL, (0, 0, SIDEBAR, h - self.footer_height))
        title = self.fonts.get(16, bold=True).render("NAND Sim", True, theme.TEXT)
        surf.blit(title, (14, (HEADER - title.get_height()) // 2))
        font = self.fonts.get(14)
        y = self._draw_levels(surf, HEADER + 6)
        y += 8
        pygame.draw.line(surf, theme.PART_BORDER, (12, y), (SIDEBAR - 12, y))
        y += 10
        if self.notice:
            for line in _wrap(self.notice, (SIDEBAR - 28) // font.size("M")[0]):
                t = font.render(line, True, theme.WIRE_X)
                surf.blit(t, (14, y))
                y += font.get_linesize()
            y += 8
        self._chip_rows = []
        self._chips_rect = None
        self.chips_view = pygame.Rect(0, 0, 0, 0)  # no list, nothing for the wheel to catch
        if self._exported:
            top = y
            bold = self.fonts.get(13, bold=True)
            surf.blit(bold.render("Your chips", True, theme.TEXT), (14, y))
            hint = self.fonts.get(12).render("usable in every level", True, theme.TEXT_DIM)
            surf.blit(hint, (SIDEBAR - 14 - hint.get_width(), y + 1))
            y += font.get_linesize() + 2
            y = self._draw_chip_rows(surf, y, font)
            self._chips_rect = pygame.Rect(6, top - 4, SIDEBAR - 12, y - top + 6)
            y += 8
        self._draw_brief(surf, y)

    def _draw_chip_rows(self, surf: pygame.Surface, y: int, font: pygame.font.Font) -> int:
        """The exported chips, each with its × button, scrolling past `CHIPS_MAX_ROWS`.
        Returns the y below them.

        In a short window the list takes fewer rows (at least one) so that the brief keeps
        `BRIEF_KEEP_LINES`, and it never reaches below the footer's top.
        """
        content = len(self._exported) * CHIP_ROW_H
        bottom = self.size[1] - self.footer_height - BRIEF_BOTTOM
        keep = 8 + BRIEF_KEEP_LINES * self.fonts.get(13).get_linesize()  # gap, then the brief
        rows = max(1, min(CHIPS_MAX_ROWS, (bottom - y - keep) // CHIP_ROW_H))
        view = max(0, min(content, rows * CHIP_ROW_H, bottom - y))
        if self._show_chip in self._exported:
            at = self._exported.index(self._show_chip) * CHIP_ROW_H
            self.chips_scroll = scroll_into_view(self.chips_scroll, at, CHIP_ROW_H, view)
        self._show_chip = None
        self.chips_scroll = clamp_scroll(self.chips_scroll, content, view)
        self.chips_view = pygame.Rect(0, y, SIDEBAR, view)
        clip = surf.get_clip()
        surf.set_clip(self.chips_view.clip(clip) if clip else self.chips_view)
        for i, name in enumerate(self._exported):
            top = y + i * CHIP_ROW_H - self.chips_scroll
            if top + CHIP_ROW_H <= y or top >= y + view:
                continue  # scrolled out of sight: not drawn, not clickable
            row = pygame.Rect(6, top, SIDEBAR - 12, CHIP_ROW_H)
            surf.blit(font.render(name, True, theme.ACCENT), (14, top + 2))
            x_btn = pygame.Rect(row.right - CHIP_ROW_H - 2, top, CHIP_ROW_H, CHIP_ROW_H)
            hit = x_btn.clip(self.chips_view)  # only the visible part takes clicks
            hot = hit.collidepoint(self.mouse) and not self.menus
            if hot:
                pygame.draw.rect(surf, theme.ERROR_BG, x_btn, border_radius=4)
            cross = font.render("×", True, theme.ERROR_TEXT if hot else theme.TEXT_DIM)
            surf.blit(cross, cross.get_rect(center=x_btn.center))
            self._chip_rows.append((hit, name))
        surf.set_clip(clip)
        _draw_scrollbar(surf, y, view, content, self.chips_scroll, CHIP_ROW_H)
        return y + view

    def _draw_levels(self, surf: pygame.Surface, y: int) -> int:
        """The level list, group by group; a closed group is only its header. Returns the
        y below it.

        The list gets the room that the notice, "Your chips" and the brief below it don't
        need, in whole rows (at least `LIST_MIN_ROWS`), and scrolls past that, so the brief
        is shown whole whenever the window allows. When the row to show changes
        (the current level, or a level a tour bubble points at), the list scrolls to it;
        otherwise the player's own scrolling stays.
        """
        self._sync_expanded()
        font = self.fonts.get(14)
        small = self.fonts.get(12, bold=True)
        entries: list[tuple[str | Level, int]] = []  # a group name or a level, and its y
        content = 0
        for group, levels in self.game.groups():
            entries.append((group, content))
            content += ROW_H
            if group in self.expanded:
                for level in levels:
                    entries.append((level, content))
                    content += ROW_H
        room = self.size[1] - self.footer_height - y - self._below_list_height()
        view = min(content, max(LIST_MIN_ROWS, room // ROW_H) * ROW_H)
        target = self._scroll_target()
        if target != self._scrolled_to:
            self._scrolled_to = target
            at = next((cy for e, cy in entries if e == target or e is target), None)
            if at is not None:
                self.list_scroll = scroll_into_view(self.list_scroll, at, ROW_H, view)
        self.list_scroll = clamp_scroll(self.list_scroll, content, view)
        self.list_rect = pygame.Rect(0, y, SIDEBAR, view)
        self._rows, self._group_rows = [], []
        clip = surf.get_clip()
        surf.set_clip(self.list_rect.clip(clip) if clip else self.list_rect)
        for entry, cy in entries:
            top = y + cy - self.list_scroll
            if top + ROW_H <= y or top >= y + view:
                continue  # scrolled out of sight: not drawn, not clickable
            rect = pygame.Rect(6, top, SIDEBAR - 12, ROW_H - 2)
            if isinstance(entry, str):
                self._draw_group_row(surf, entry, rect, small)
                self._group_rows.append((rect, entry))
            else:
                self._draw_level_row(surf, entry, rect, font)
                self._rows.append((rect, entry))
        surf.set_clip(clip)
        _draw_scrollbar(surf, y, view, content, self.list_scroll, ROW_H)
        return y + view

    def _scroll_target(self) -> str | Level:
        """The row the list should show: a level a tour bubble points at, else the current one."""
        step = self.tour.visible(self.game.current.name)
        if step is not None and step.anchor.startswith("level:"):
            name = step.anchor.removeprefix("level:")
            level = next((lv for lv in self.game.levels if lv.name == name), None)
            if level is not None:
                return level if level.group in self.expanded else level.group
        return self.game.current

    def scroll_list(self, rows: int) -> None:
        """Scroll the level list by whole rows (positive: down); clamped when drawn."""
        self.list_scroll = max(0, self.list_scroll + rows * ROW_H)

    def _draw_group_row(
        self, surf: pygame.Surface, group: str, head: pygame.Rect, small: pygame.font.Font
    ) -> None:
        levels = next(lvs for g, lvs in self.game.groups() if g == group)
        if head.collidepoint(self.mouse) and self.list_rect.collidepoint(self.mouse):
            if not self.menus:
                pygame.draw.rect(surf, theme.BG, head, border_radius=5)
        chevron = small.render(CHEVRON[group in self.expanded], True, theme.TEXT_DIM)
        surf.blit(chevron, (head.x + 8, head.centery - chevron.get_height() // 2))
        label = small.render(group_label(group).upper(), True, theme.TEXT_DIM)
        surf.blit(label, (head.x + 24, head.centery - label.get_height() // 2))
        solved = sum(self.game.status(lv) == "solved" for lv in levels)
        done = solved == len(levels)
        count = small.render(
            f"✓ {solved}/{len(levels)}" if done else f"{solved}/{len(levels)}",
            True,
            theme.WIRE_1 if done else theme.TEXT_DIM,
        )
        surf.blit(
            count, (head.right - 8 - count.get_width(), head.centery - count.get_height() // 2)
        )

    def _draw_level_row(
        self, surf: pygame.Surface, level: Level, rect: pygame.Rect, font: pygame.font.Font
    ) -> None:
        status = self.game.status(level)
        if level is self.game.current:
            pygame.draw.rect(surf, theme.BG, rect, border_radius=5)
        color = {"solved": theme.WIRE_1, "open": theme.TEXT, "locked": theme.TEXT_DIM}[status]
        glyph = font.render(GLYPH[status], True, color)
        surf.blit(glyph, (rect.x + 8, rect.centery - glyph.get_height() // 2))
        name = font.render(level.name, True, theme.TEXT if status != "locked" else color)
        surf.blit(name, (rect.x + 30, rect.centery - name.get_height() // 2))

    def _below_list_height(self) -> int:
        """Height the sidebar wants under the level list: separator, notice, chips, brief.

        The whole brief when it fits; when it doesn't, the list keeps its `LIST_MIN_ROWS`
        anyway, and the brief scrolls in what is left.
        """
        font = self.fonts.get(14)
        h = 8 + 10  # the separator line and its gaps
        if self.notice:
            lines = _wrap(self.notice, (SIDEBAR - 28) // font.size("M")[0])
            h += len(lines) * font.get_linesize() + 8
        if self._exported:
            rows = min(len(self._exported), CHIPS_MAX_ROWS)
            h += font.get_linesize() + 2 + rows * CHIP_ROW_H + 8
        return h + sum(step for *_, step in self._brief_layout()) + BRIEF_BOTTOM

    @property
    def brief_cols(self) -> int:
        """How many characters of brief text fit across the sidebar."""
        return (SIDEBAR - 28) // self.fonts.get(13).size("M")[0]

    def _brief_layout(self) -> list[tuple[str, str, pygame.font.Font, int]]:
        """The brief's lines as (text, kind, font, height it takes)."""
        text_font = self.fonts.get(13)
        out = []
        for line, kind in brief_lines(self.game.current.brief.read_text(), self.brief_cols):
            font = {
                "title": self.fonts.get(16, bold=True),
                "bold": self.fonts.get(13, bold=True),
            }.get(kind, text_font)
            step = font.get_linesize() if kind != "blank" else font.get_linesize() // 2
            out.append((line, kind, font, step))
        return out

    def _draw_brief(self, surf: pygame.Surface, y: int) -> None:
        """The level's brief, below everything else; it scrolls when it doesn't fit.

        The scroll goes back to the top when another level opens.
        """
        if self._brief_for != self.game.current.name:
            self._brief_for = self.game.current.name
            self.brief_scroll = 0
        layout = self._brief_layout()
        content = sum(step for *_, step in layout)
        bottom = self.size[1] - self.footer_height - BRIEF_BOTTOM
        view = max(0, min(content, bottom - y))
        self.brief_cut = content > view
        self.brief_scroll = clamp_scroll(self.brief_scroll, content, view)
        self.brief_view = pygame.Rect(0, y, SIDEBAR, view)
        clip = surf.get_clip()
        surf.set_clip(self.brief_view.clip(clip) if clip else self.brief_view)
        line_y = y - self.brief_scroll
        for line, kind, font, step in layout:
            if line and line_y + step > y and line_y < y + view:
                color = theme.ACCENT if kind == "table" else theme.TEXT
                surf.blit(font.render(line, True, color), (14, line_y))
            line_y += step
        surf.set_clip(clip)
        line_h = self.fonts.get(13).get_linesize()
        _draw_scrollbar(surf, y, view, content, self.brief_scroll, line_h)
        self._brief_rect = pygame.Rect(6, y - 4, SIDEBAR - 12, view + 8)

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


def _draw_scrollbar(
    surf: pygame.Surface, y: int, view: int, content: int, scroll: int, min_h: int
) -> None:
    """A thin bar at the sidebar's right edge showing where a scrolled view sits in its
    content; nothing when the content fits."""
    if content <= view or view <= 0:
        return
    bar_h = min(view, max(min_h, view * view // content))
    bar_y = y + (view - bar_h) * scroll // (content - view)
    pygame.draw.rect(surf, theme.PART_BORDER, (SIDEBAR - 5, bar_y, 3, bar_h), border_radius=2)


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
