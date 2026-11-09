"""The player's settings: mute, volume and the soundtrack. Pure Python, no pygame.

They live in `<save dir>-settings.json`, beside the save directory and not inside
it, so a game reset (which moves every file in the save directory to a backup)
keeps them. An unreadable file means the defaults, with a warning for the GUI:
settings are cheap to lose, so the bad file is simply overwritten on the next save.

`music` and `music_volume` came after version 1 was written, so a file without them
is still version 1 and gets their defaults.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from nandsim.gui.saves import atomic_write

SETTINGS_VERSION = 1
VOLUMES = (0.2, 0.4, 0.6, 0.8, 1.0)  # the steps of the menu's Volume item
MUSIC_VOLUMES = (0.1, 0.2, 0.3, 0.5, 0.7)  # the soundtrack's steps: it stays in the background


@dataclass
class Settings:
    muted: bool = False  # silences everything, the soundtrack included
    volume: float = 0.6
    music: bool = True
    music_volume: float = 0.3
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
            music = data.get("music", cls.music)
            music_volume = data.get("music_volume", cls.music_volume)
            if not isinstance(muted, bool) or not isinstance(music, bool):
                raise ValueError("muted and music must be true or false")
            if not isinstance(volume, int | float) or not isinstance(music_volume, int | float):
                raise ValueError("volume and music_volume must be numbers")
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as e:
            return cls(warning=f"settings were unreadable ({e}); using the defaults")
        return cls(muted, _unit(volume), music, _unit(music_volume))

    def save(self, path: Path) -> None:
        data = {
            "version": SETTINGS_VERSION,
            "muted": self.muted,
            "volume": self.volume,
            "music": self.music,
            "music_volume": self.music_volume,
        }
        atomic_write(path, json.dumps(data, indent=2) + "\n")

    def next_volume(self) -> float:
        """The volume step after the current one, wrapping from the loudest to the quietest."""
        return _next_step(VOLUMES, self.volume)

    def next_music_volume(self) -> float:
        return _next_step(MUSIC_VOLUMES, self.music_volume)


def _unit(v: float) -> float:
    return min(1.0, max(0.0, float(v)))


def _next_step(steps: tuple[float, ...], now: float) -> float:
    return next((v for v in steps if v > now + 1e-6), steps[0])
