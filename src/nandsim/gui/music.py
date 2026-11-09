"""The soundtrack: the MP3s in `gui/music/`, streamed one after another by `pygame.mixer.music`.

Streaming keeps the tracks off the startup path and out of memory: only the one
playing is decoded, a little at a time. The playlist starts at a random track and
goes round in order. `update()`, called every frame, starts the next track when one
ends, and follows the settings: the soundtrack plays only while `music` is on and the
game isn't muted, at `music_volume`.

Like the sound effects, it never takes the game down: without an audio device, with
no tracks, or if a file won't play, the soundtrack goes quiet and the game goes on.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Protocol

import pygame

from nandsim.gui.settings import Settings

TRACKS_DIR = Path(__file__).resolve().parent / "music"


class Player(Protocol):
    """What the soundtrack needs from `pygame.mixer.music`; tests pass a fake."""

    def load(self, filename: str) -> None: ...
    def play(self) -> None: ...
    def stop(self) -> None: ...
    def set_volume(self, volume: float) -> None: ...
    def get_busy(self) -> bool: ...


def find_tracks(folder: Path = TRACKS_DIR) -> list[Path]:
    """The soundtrack's files, by name."""
    return sorted(folder.glob("*.mp3")) if folder.is_dir() else []


class Music:
    def __init__(
        self,
        settings: Settings,
        tracks: list[Path] | None = None,
        player: Player | None = None,
        start: int | None = None,
    ) -> None:
        self.settings = settings
        self.tracks = find_tracks() if tracks is None else tracks
        self.player: Player = player if player is not None else pygame.mixer.music
        self.enabled = False  # set by `start()` once the mixer is known to work
        self.index = random.randrange(len(self.tracks)) if start is None and self.tracks else 0
        if start is not None:
            self.index = start
        self.playing: Path | None = None  # the track started last, while one is playing

    @property
    def wanted(self) -> bool:
        s = self.settings
        return self.enabled and bool(self.tracks) and s.music and not s.muted

    def start(self, mixer_ready: bool) -> None:
        """Begin, if the mixer opened (the sound effects open it first)."""
        self.enabled = mixer_ready
        self.update()

    def update(self) -> None:
        """Every frame: follow the settings, and move on when a track ends."""
        try:
            if not self.wanted:
                if self.playing is not None:
                    self.player.stop()
                    self.playing = None
                return
            self.player.set_volume(self.settings.music_volume)
            if self.playing is None or not self.player.get_busy():
                self._play_next()
        except pygame.error:
            self.enabled = False  # the device went away: stay quiet from now on
            self.playing = None

    def _play_next(self) -> None:
        """Start the next track; one that won't load is skipped, and if none will, give up."""
        if self.playing is not None:
            self.index = (self.index + 1) % len(self.tracks)
        for _ in range(len(self.tracks)):
            track = self.tracks[self.index]
            try:
                self.player.load(str(track))
                self.player.play()
            except pygame.error:
                self.index = (self.index + 1) % len(self.tracks)
                continue
            self.playing = track
            return
        self.enabled = False  # not one of them plays
        self.playing = None
