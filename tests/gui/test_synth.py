"""Synthesized sounds: every recipe is short, audible, in range and click-free."""

from __future__ import annotations

import numpy as np
import pytest

from nandsim.gui.synth import RATE, RECIPES, render, to_mixer


@pytest.mark.parametrize("name", sorted(RECIPES))
def test_recipe_is_short_audible_and_click_free(name: str) -> None:
    s = render(name)
    assert s.dtype == np.float32 and s.ndim == 1
    assert 0 < len(s) <= 0.8 * RATE
    assert float(np.max(np.abs(s))) <= 1.0
    assert float(np.max(np.abs(s))) > 0.05  # not silent
    assert abs(float(s[-1])) < 1e-3  # faded out: no click at the end


def test_recipes_follow_the_rate() -> None:
    assert len(render("solved", 22050)) == pytest.approx(len(render("solved")) / 2, abs=4)


def test_to_mixer_formats() -> None:
    s = np.array([-1.0, 0.0, 0.5, 1.0, 2.0], dtype=np.float32)  # 2.0 is clipped

    mono = to_mixer(s, -16, 1)
    assert mono.dtype == np.int16 and mono.shape == (5,)
    assert mono.tolist() == [-32767, 0, 16384, 32767, 32767]

    stereo = to_mixer(s, -16, 2)
    assert stereo.shape == (5, 2) and stereo.flags["C_CONTIGUOUS"]
    assert (stereo[:, 0] == stereo[:, 1]).all() and (stereo[:, 0] == mono).all()

    u8 = to_mixer(s, 8, 1)
    assert u8.dtype == np.uint8 and u8.tolist() == [1, 128, 192, 255, 255]

    f32 = to_mixer(s, 32, 2)
    assert f32.dtype == np.float32 and f32.shape == (5, 2) and float(f32.max()) == 1.0

    s32 = to_mixer(s, -32, 1)
    assert s32.dtype == np.int32 and int(s32[-1]) == 2**31 - 1
