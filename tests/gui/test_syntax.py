"""Syntax colouring tests."""

from __future__ import annotations

from nandsim.gui.syntax import highlight, token_end


def kinds(line: str) -> list[tuple[str, str]]:
    return [(line[a:b], k) for a, b, k in highlight([line])[0] if k != "punct"]


def test_keywords_chips_constants_numbers_comments() -> None:
    assert kinds("CHIP Mux {") == [("CHIP", "keyword"), ("Mux", "plain")]
    assert kinds("    Nand (a=a[0..7], b=true); // hi") == [
        ("Nand", "chip"),
        ("a", "plain"),
        ("a", "plain"),
        ("0", "number"),
        ("7", "number"),
        ("b", "plain"),
        ("true", "constant"),
        ("// hi", "comment"),
    ]


def test_block_comment_across_lines() -> None:
    spans = highlight(["a /* one", "two", "three */ b"])
    assert spans[0][-1] == (2, 8, "comment")
    assert spans[1] == [(0, 3, "comment")]
    assert spans[2][0] == (0, 8, "comment") and spans[2][1] == (9, 10, "plain")


def test_half_typed_code_does_not_crash() -> None:
    highlight(["CHIP {", "Nand(a=", "/*", "$$$ ]]]"])


def test_token_end() -> None:
    assert token_end("    Nand(a=x)", 4) == 8
    assert token_end("a;", 1) == 2
    assert token_end("", 0) == 1
