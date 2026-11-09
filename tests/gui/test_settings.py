"""Settings: mute and volume, stored beside the save directory."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from nandsim.gui.saves import SaveStore
from nandsim.gui.settings import VOLUMES, Settings
from nandsim.testing import load_levels


def test_defaults_without_a_file(tmp_path: Path) -> None:
    s = Settings.load(tmp_path / "missing.json")
    assert (s.muted, s.volume, s.warning) == (False, 0.6, None)


def test_round_trip_and_clamping(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    Settings(muted=True, volume=0.8).save(path)
    assert json.loads(path.read_text()) == {
        "version": 1,
        "muted": True,
        "volume": 0.8,
        "music": True,
        "music_volume": 0.3,
    }
    s = Settings.load(path)
    assert (s.muted, s.volume, s.warning) == (True, 0.8, None)
    path.write_text('{"version": 1, "muted": false, "volume": 7}')
    assert Settings.load(path).volume == 1.0


@pytest.mark.parametrize(
    "text",
    ["{nope", '{"version": 2, "muted": false, "volume": 1}', '{"version": 1}', "[]",
     '{"version": 1, "muted": "yes", "volume": 1}'],
)  # fmt: skip
def test_unreadable_file_gives_defaults_and_a_warning(tmp_path: Path, text: str) -> None:
    path = tmp_path / "settings.json"
    path.write_text(text)
    s = Settings.load(path)
    assert (s.muted, s.volume) == (False, 0.6)
    assert s.warning is not None and s.warning.startswith("settings were unreadable (")


def test_volume_steps_wrap() -> None:
    assert [Settings(volume=v).next_volume() for v in VOLUMES] == [0.4, 0.6, 0.8, 1.0, 0.2]
    assert Settings(volume=0.5).next_volume() == 0.6  # an odd value joins the steps
    assert Settings(volume=0.0).next_volume() == 0.2


def test_settings_live_beside_the_saves_and_survive_a_reset(tmp_path: Path) -> None:
    store = SaveStore(load_levels(), tmp_path / "save")
    assert store.settings_path == tmp_path / "save-settings.json"
    Settings(muted=True).save(store.settings_path)
    levels = {lv.name: lv for lv in store.levels}
    store.mark_solved(levels["Wire"])  # something to reset
    assert store.reset() is not None
    assert Settings.load(store.settings_path).muted
