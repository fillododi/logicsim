"""TextBuffer tests: typing, auto-indent, selection, movement, undo, comments."""

from __future__ import annotations

from nandsim.gui.textbuffer import Pos, TextBuffer


def typed(buf: TextBuffer, text: str) -> None:
    for ch in text:
        if ch == "\n":
            buf.newline()
        else:
            buf.type_char(ch)


def test_typing_and_undo_merges_a_word() -> None:
    b = TextBuffer()
    typed(b, "Nand")
    assert b.text == "Nand" and b.cursor == Pos(0, 4) and b.dirty
    b.insert(" ")
    typed(b, "x")
    b.undo()
    assert b.text == "Nand "
    b.undo()
    b.undo()
    assert b.text == ""
    b.redo()
    assert b.text == "Nand"


def test_auto_indent_and_closing_brace() -> None:
    b = TextBuffer()
    typed(b, "CHIP X {\nIN a;\n}")
    assert b.text == "CHIP X {\n    IN a;\n}"


def test_enter_between_braces_opens_block() -> None:
    b = TextBuffer("CHIP X {}")
    b.set_cursor(Pos(0, 8))
    b.newline()
    assert b.text == "CHIP X {\n    \n}"
    assert b.cursor == Pos(1, 4)


def test_backspace_removes_one_indent_level_and_joins_lines() -> None:
    b = TextBuffer("a\n        b")
    b.set_cursor(Pos(1, 8))
    b.backspace()
    assert b.lines[1] == "    b"
    b.set_cursor(Pos(1, 0))
    b.backspace()
    assert b.text == "a    b" and b.cursor == Pos(0, 1)


def test_selection_replace_cut_and_select_all() -> None:
    b = TextBuffer("Nand(a=a, b=b, out=out);")
    b.select_word_at(Pos(0, 2))
    assert b.selected_text() == "Nand"
    b.insert("Xor")
    assert b.text.startswith("Xor(")
    b.select_all()
    assert b.cut() == "Xor(a=a, b=b, out=out);" and b.text == ""
    b.undo()
    assert b.text == "Xor(a=a, b=b, out=out);"


def test_shift_movement_selects_across_lines() -> None:
    b = TextBuffer("abc\ndef")
    b.set_cursor(Pos(0, 1))
    b.move("down", select=True)
    b.move("right", select=True)
    assert b.selected_text() == "bc\nde"
    b.move("left")  # collapses to the start
    assert b.selection() is None and b.cursor == Pos(0, 1)


def test_vertical_movement_keeps_goal_column() -> None:
    b = TextBuffer("long line\nx\nanother line")
    b.set_cursor(Pos(0, 7))
    b.move("down")
    assert b.cursor == Pos(1, 1)
    b.move("down")
    assert b.cursor == Pos(2, 7)
    b.move("up")
    b.move("up")
    b.move("up")
    assert b.cursor == Pos(0, 0)


def test_word_moves_and_smart_home() -> None:
    b = TextBuffer("    Nand(a=in, b=in);")
    b.move("end")
    b.move("word_left")
    assert b.cursor == Pos(0, 20)  # before ";"
    b.move("word_left")
    assert b.cursor == Pos(0, 19)  # before ")": symbols are their own stop
    b.move("word_left")
    assert b.cursor == Pos(0, 17)  # before "in"
    b.move("home")
    assert b.cursor == Pos(0, 4)
    b.move("home")
    assert b.cursor == Pos(0, 0)
    b.move("word_right")
    assert b.cursor == Pos(0, 8)  # skips the indentation, stops after "Nand"
    b.move("word_right")
    assert b.cursor == Pos(0, 9)  # past "("


def test_tab_indents_selection_and_shift_tab_dedents() -> None:
    b = TextBuffer("a;\nb;\n\nc;")
    b.select_all()
    b.indent()
    assert b.text == "    a;\n    b;\n\n    c;"
    b.dedent()
    assert b.text == "a;\nb;\n\nc;"
    b.set_cursor(Pos(0, 1))
    b.indent()
    assert b.lines[0] == "a   ;"  # spaces up to the next tab stop


def test_toggle_comment() -> None:
    b = TextBuffer("    Nand(a=a);\n    Not(in=x);")
    b.select_all()
    b.toggle_comment()
    assert b.text == "    // Nand(a=a);\n    // Not(in=x);"
    b.toggle_comment()
    assert b.text == "    Nand(a=a);\n    Not(in=x);"


def test_dirty_tracking_and_set_text() -> None:
    b = TextBuffer("x")
    assert not b.dirty
    b.type_char("y")
    assert b.dirty
    b.mark_saved()
    assert not b.dirty
    b.set_text("fresh")
    assert b.text == "fresh" and not b.dirty
    b.undo()
    assert b.text == "fresh"  # history cleared on reload


def test_delete_and_paste_multiline() -> None:
    b = TextBuffer("ab\ncd")
    b.set_cursor(Pos(0, 2))
    b.delete()
    assert b.text == "abcd"
    b.insert("X\nY")
    assert b.text == "abX\nYcd" and b.cursor == Pos(1, 1)


def test_source_positions_are_one_based() -> None:
    assert Pos.from_source(3, 5) == Pos(2, 4)
