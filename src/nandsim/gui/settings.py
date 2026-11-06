"""The player's settings: mute and volume. Pure Python, no pygame.

They live in `<save dir>-settings.json`, beside the save directory and not inside
it, so a game reset (which moves every file in the save directory to a backup)
keeps them. An unreadable file means the defaults, with a warning for the GUI:
settings are cheap to lose, so the bad file is simply overwritten on the next save.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from nandsim.gui.saves import atomic_write

SETTINGS_VERSION = 1
VOLUMES = (0.2, 0.4, 0.6, 0.8, 1.0)  # the steps of the menu's Volume item


@dataclass
class Settings:
    muted: bool = False
    volume: float = 0.6
    warning: str | None = None  # shown by the GUI if the file was unreadable

    @classmethod
    def load(cls, path: Path) -> Settings:
        if not path.is_file():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("version") != SETTINGS_VERSION:
                raise ValueError(f"unknown version {data.get('version')!r}")
            muted, volume = data["muted"], data["volume"]
            if not isinstance(muted, bool) or not isinstance(volume, int | float):
                raise ValueError("muted must be true or false, volume a number")
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as e:
            return cls(warning=f"settings were unreadable ({e}); using the defaults")
        return cls(muted, min(1.0, max(0.0, float(volume))))

    def save(self, path: Path) -> None:
        data = {"version": SETTINGS_VERSION, "muted": self.muted, "volume": self.volume}
        atomic_write(path, json.dumps(data, indent=2) + "\n")

    def next_volume(self) -> float:
        """The volume step after the current one, wrapping from the loudest to the quietest."""
        return next((v for v in VOLUMES if v > self.volume + 1e-6), VOLUMES[0])
