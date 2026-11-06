"""Short tips for the most common build errors. Pure Python, no pygame.

The error message already says *what* is wrong, precisely. A tip adds *what to do
about it*, in the words of a player who is still learning the HDL. Tips match
on the message text, so a reworded error must update its pattern here (the
tests pin each pattern to a real error). `{group}` in a tip is filled from the
pattern's named group; any other brace is literal.
"""

from __future__ import annotations

import re

_TIPS: list[tuple[re.Pattern[str], str]] = [
    # Buses: widths, slices and partly connected pins.
    (
        re.compile(
            r"^width mismatch: pin '(?P<pin>[^']+)' of (?P<chip>\w+) has (?P<n>\d+ bits?) "
            r"but '(?P<base>[\w.]+)[^']*' has (?P<m>\d+)(?: bits?)?$"
        ),
        "{chip}'s pin {pin} takes {n} but its signal has {m}. A slice picks bits out of a bus, "
        "like {base}[0] or {base}[0..3]; a 1-bit part handles a bus one bit at a time.",
    ),
    (
        re.compile(
            r"^width mismatch: '(?P<target>[^']+)' has (?P<n>\d+ bits?) "
            r"but '(?P<source>[^']+)' has (?P<m>\d+)(?: bits?)?$"
        ),
        "In {target} = {source}, the left side has {n} and the right side {m}. "
        "Slice them so the widths match, like out[0..3] = in[4..7];",
    ),
    (
        re.compile(r"^\S+ is out of range: '(?P<name>[^']+)' has \d+ bits? \((?P<range>[^)]+)\)$"),
        "Bits are counted from 0, so {name} has bits {range}: the last one is the width minus 1.",
    ),
    (
        re.compile(
            r"^(?P<what>bits? .+?) of output pin '(?P<pin>[^']+)' of \w+ (?:is|are) not connected$"
        ),
        "Every bit of an OUT bus needs a driver, and nothing drives {what} of {pin} yet. "
        "Drive each bit with a part (out={pin}[i]) or a connection ({pin}[i] = ...).",
    ),
    (
        re.compile(
            r"^(?P<what>bits? .+?) of input pin '(?P<pin>[^']+)' of (?P<chip>\w+) "
            r"(?:is|are) not connected$"
        ),
        "Every bit of {chip}'s {pin} needs a value, and nothing connects {what} yet. "
        "Connect {pin} whole ({pin}=signal) or cover every bit with slices.",
    ),
    (
        re.compile(r"^output pin '(?P<pin>[^']+)' of \w+ is not connected$"),
        "Every OUT pin needs a driver: end a part with out={pin}, or write {pin} = <signal>;",
    ),
    (
        re.compile(r"^input pin '(?P<pin>[^']+)' of (?P<chip>\w+) is not connected$"),
        "Every input of a part needs a value: add {pin}=<signal> inside {chip}(...). "
        "A signal can be a pin, a wire, true or false.",
    ),
    (
        re.compile(r"^(?P<chip>\w+) has no pin '[^']+' \(its pins are: (?P<pins>[^)]*)\)$"),
        "In {chip}(pin=signal), the left side is one of {chip}'s own pins ({pins}); "
        "the right side is a signal of your chip.",
    ),
    (
        re.compile(r"^'(?P<name>\w+)' is not allowed in this level; (?P=name) may use: .*$"),
        "A chip can't be built from itself: use the smaller parts listed in the brief.",
    ),
    (
        re.compile(r"^'\w+' is not allowed in this level; \w+ may use: .*$"),
        "Only the parts in the brief and your exported chips can be used here. "
        "Names are case-sensitive.",
    ),
    (
        re.compile(r"^'(?P<name>[^']+)' is not a pin of \w+ and nothing drives a wire"),
        "To read the wire '{name}', some part must write it first (out={name}). "
        "Check the spelling too.",
    ),
    (
        re.compile(r"^'(?P<name>[^']+)' is already driven by "),
        "A signal has exactly one source. Send the second output to a new wire name.",
    ),
    (
        re.compile(r"^combinational loop "),
        "A signal can't depend on itself without a DFF in between. "
        "Follow the wires in the message to find the cycle.",
    ),
    (
        re.compile(r"^\w+ must keep the level's pins "),
        "Keep the IN and OUT lines as the level gave them: the tests rely on them.",
    ),
    (
        re.compile(r"^'[^']+' is an input pin of \w+: "),
        "Inputs are set from outside the chip. Drive an OUT pin or a new wire instead.",
    ),
    (
        re.compile(r"^file for chip '(?P<want>\w+)' defines chip '\w+' instead$"),
        "The name after CHIP must be the level's chip: CHIP {want} {",
    ),
    (re.compile(r"^expected ';'"), "Every part and connection ends with ';'."),
    (re.compile(r"^expected ':'"), "Write PARTS: with a colon before the first part."),
    (
        re.compile(r"^expected 'CHIP', found 'chip'"),
        "HDL keywords are uppercase: CHIP, IN, OUT, PARTS.",
    ),
    (
        re.compile(r"^expected '\}' to close the chip"),
        "Each '{' needs a matching '}': close the chip after the last part.",
    ),
]


def tip_for(message: str) -> str | None:
    """A one-line hint for a build error message, or None if there is no tip for it."""
    for pattern, tip in _TIPS:
        m = pattern.search(message)
        if m:
            return _fill(tip, m.groupdict())
    return None


def _fill(tip: str, groups: dict[str, str]) -> str:
    return re.sub(r"\{(\w+)\}", lambda g: groups.get(g[1], g[0]), tip)
