"""Where level data and player saves live, for both a repo checkout and an installed wheel."""

from __future__ import annotations

import os
from pathlib import Path

_PACKAGE = Path(__file__).resolve().parent


def data_root() -> Path:
    """Directory holding `chips/` and `reference/`.

    An installed wheel ships them as `nandsim/_data/`; a source checkout uses the repo root.
    """
    packaged = _PACKAGE / "_data"
    if (packaged / "chips").is_dir():
        return packaged
    return _PACKAGE.parents[1]


def default_save_dir() -> Path:
    """The player's saved chips: `$XDG_DATA_HOME/nandsim/save`, else `~/.local/share/...`."""
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "nandsim" / "save"


def exports_dir(save_dir: Path) -> Path:
    """The chips a player exported: `<save dir>-exports`, beside the save directory.

    Never inside it: the chip library searches directories recursively, and a game
    reset empties the save directory but must keep the exported chips.
    """
    return save_dir.with_name(save_dir.name + "-exports")
