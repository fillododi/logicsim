"""Sound playback: works on the dummy audio driver, and stays silent without a device."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from collections.abc import Iterator  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from nandsim.gui.settings import Settings  # noqa: E402
from nandsim.gui.sound import Sounds  # noqa: E402
from nandsim.gui.synth import RECIPES  # noqa: E402


@pytest.fixture
def no_mixer() -> Iterator[None]:
    pygame.mixer.quit()
    yield
    pygame.mixer.quit()


def test_load_and_play_on_the_dummy_driver(no_mixer: None) -> None:
    sounds = Sounds(Settings(volume=0.4))
    assert sounds.load() and sounds.enabled
    assert set(sounds._sounds) == set(RECIPES)
    for name in RECIPES:
        sounds.play(name)
    assert sounds.played == list(RECIPES)
    assert sounds._sounds["toggle"].get_volume() == pytest.approx(0.4, abs=0.01)


def test_mixer_already_open_in_another_format_is_used_as_is(no_mixer: None) -> None:
    pygame.mixer.init(22050, 8, 1)  # unsigned 8-bit mono
    sounds = Sounds(Settings())
    assert sounds.load()
    assert pygame.mixer.get_init() == (22050, 8, 1)
    sounds.play("solved")


def test_no_audio_device_means_silence_not_a_crash(
    no_mixer: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(*args: object) -> None:
        raise pygame.error("Audio target 'nonexistent' not available")

    monkeypatch.setattr(pygame.mixer, "init", broken)
    sounds = Sounds(Settings())
    assert not sounds.load() and not sounds.enabled
    sounds.play("solved")  # does nothing, raises nothing
    assert sounds.played == ["solved"]


def test_muted_plays_nothing(no_mixer: None) -> None:
    settings = Settings(muted=True)
    sounds = Sounds(settings)
    sounds.load()
    sounds.play("toggle")
    assert sounds.played == []
    settings.muted = False
    sounds.play("toggle")
    assert sounds.played == ["toggle"]
