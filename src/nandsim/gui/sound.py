"""Plays the synthesized sound effects through `pygame.mixer`.

`Sounds.load()` opens the mixer if nothing has yet, then turns every recipe in
`gui.synth` into a `pygame.mixer.Sound` in the format the mixer actually opened
with. Without an audio device, or if anything goes wrong while loading, the
game stays silent: `play` then does nothing, and never raises.
"""

from __future__ import annotations

import pygame

from nandsim.gui import synth
from nandsim.gui.settings import Settings

MIXER = (synth.RATE, -16, 2, 512)  # frequency, size, channels, buffer


class Sounds:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.enabled = False
        self.played: list[str] = []  # what was played, newest last (tests read it)
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    def load(self) -> bool:
        """Open the mixer and build every sound; False (and silence) if that fails."""
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(*MIXER)
            init = pygame.mixer.get_init()
            if init is None:
                return False
            rate, size, channels = init
            self._sounds = {
                name: pygame.sndarray.make_sound(
                    synth.to_mixer(synth.render(name, rate), size, channels)
                )
                for name in synth.RECIPES
            }
        except (pygame.error, ValueError, TypeError):
            self._sounds = {}
            self.enabled = False
            return False
        self.enabled = True
        return True

    def play(self, name: str) -> None:
        """Play a sound at the current volume, unless muted or there is no audio."""
        if self.settings.muted:
            return
        self.played = [*self.played[-49:], name]
        sound = self._sounds.get(name) if self.enabled else None
        if sound is None:
            return
        try:
            sound.set_volume(self.settings.volume)
            sound.play()
        except pygame.error:
            self.enabled = False
