"""The soundtrack: the playlist, the settings it follows, and staying quiet when it must."""

from __future__ import annotations

import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from pathlib import Path  # noqa: E402

import pygame  # noqa: E402

from nandsim.gui.music import TRACKS_DIR, Music, find_tracks  # noqa: E402
from nandsim.gui.settings import MUSIC_VOLUMES, Settings  # noqa: E402

TRACKS = [Path("a.mp3"), Path("b.mp3"), Path("c.mp3")]


class FakePlayer:
    """Stands in for `pygame.mixer.music`: records what it was asked to do."""

    def __init__(self, broken: set[str] | None = None) -> None:
        self.loaded: list[str] = []
        self.busy = False
        self.volume = 1.0
        self.stops = 0
        self.broken = broken or set()
        self.device_lost = False

    def load(self, filename: str) -> None:
        if filename in self.broken:
            raise pygame.error(f"can't decode {filename}")
        self.loaded.append(filename)

    def play(self) -> None:
        self.busy = True

    def stop(self) -> None:
        self.busy = False
        self.stops += 1

    def set_volume(self, volume: float) -> None:
        self.volume = volume

    def get_busy(self) -> bool:
        if self.device_lost:
            raise pygame.error("audio device lost")
        return self.busy


def music(settings: Settings | None = None, **kw: object) -> tuple[Music, FakePlayer]:
    player = kw.pop("player", None) or FakePlayer()
    m = Music(settings or Settings(), tracks=kw.pop("tracks", TRACKS), player=player, start=1)
    return m, player  # type: ignore[return-value]


def test_the_shipped_tracks_are_found() -> None:
    tracks = find_tracks()
    assert len(tracks) == 4 and all(t.suffix == ".mp3" and t.parent == TRACKS_DIR for t in tracks)


def test_it_plays_from_its_start_track_at_the_music_volume() -> None:
    m, p = music()
    m.start(True)
    assert p.loaded == ["b.mp3"] and p.busy and p.volume == 0.3
    m.update()
    assert p.loaded == ["b.mp3"]  # still playing: nothing new


def test_the_next_track_follows_and_the_playlist_goes_round() -> None:
    m, p = music()
    m.start(True)
    for _ in range(3):
        p.busy = False  # the track ended
        m.update()
    assert p.loaded == ["b.mp3", "c.mp3", "a.mp3", "b.mp3"]


def test_mute_and_music_off_stop_it_and_turning_back_on_resumes() -> None:
    s = Settings()
    m, p = music(s)
    m.start(True)
    s.muted = True
    m.update()
    assert not p.busy and m.playing is None
    s.muted, s.music = False, False
    m.update()
    assert not p.busy and p.loaded == ["b.mp3"]
    s.music = True
    s.music_volume = 0.7
    m.update()
    assert p.busy and p.volume == 0.7 and p.loaded == ["b.mp3", "b.mp3"]


def test_silent_without_a_mixer_or_without_tracks() -> None:
    m, p = music()
    m.start(False)  # no audio device: the sound effects' mixer didn't open
    assert p.loaded == [] and m.playing is None
    m2, p2 = music(tracks=[])
    m2.start(True)
    assert p2.loaded == [] and m2.playing is None


def test_a_track_that_wont_load_is_skipped_and_none_loading_gives_up() -> None:
    m, p = music(player=FakePlayer(broken={"b.mp3"}))
    m.start(True)
    assert p.loaded == ["c.mp3"] and m.playing == Path("c.mp3")
    m2, p2 = music(player=FakePlayer(broken={"a.mp3", "b.mp3", "c.mp3"}))
    m2.start(True)  # never raises
    assert not m2.enabled and m2.playing is None


def test_a_lost_device_goes_quiet_without_raising() -> None:
    m, p = music()
    m.start(True)
    p.device_lost = True
    m.update()
    assert not m.enabled and m.playing is None
    m.update()  # and stays quiet
    assert p.loaded == ["b.mp3"]


# ---- settings ------------------------------------------------------------------


def test_a_settings_file_from_before_the_soundtrack_gets_its_defaults(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text('{"version": 1, "muted": false, "volume": 0.4}')
    s = Settings.load(path)
    assert (s.volume, s.music, s.music_volume, s.warning) == (0.4, True, 0.3, None)


def test_music_settings_round_trip_and_bad_values_warn(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    Settings(music=False, music_volume=0.5).save(path)
    assert json.loads(path.read_text())["music"] is False
    s = Settings.load(path)
    assert (s.music, s.music_volume) == (False, 0.5)
    path.write_text('{"version": 1, "muted": false, "volume": 0.4, "music": "yes"}')
    assert Settings.load(path).warning is not None


def test_the_music_volume_steps_round() -> None:
    s = Settings(music_volume=MUSIC_VOLUMES[-1])
    assert s.next_music_volume() == MUSIC_VOLUMES[0]
    s.music_volume = 0.3
    assert s.next_music_volume() == 0.5
