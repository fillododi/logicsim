"""Sound effects synthesized with numpy: no asset files, no pygame.

Each recipe in `RECIPES` turns a sample rate into a short mono signal of float32
samples in [-1, 1]. `to_mixer` converts a signal to whatever format the mixer
opened with (sample size, signedness, channels), which differs between devices,
so `gui.sound` can hand it to `pygame.sndarray.make_sound`.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

RATE = 44100
FADE = 0.004  # seconds of fade-out at the end of every sound, so it never clicks

Signal = np.ndarray


def _t(dur: float, rate: int) -> np.ndarray:
    return np.arange(int(dur * rate), dtype=np.float64) / rate


def _wave(phase: np.ndarray, wave: str) -> np.ndarray:
    """One of three shapes, from a phase measured in cycles."""
    frac = phase % 1.0
    if wave == "square":
        return np.where(frac < 0.5, 1.0, -1.0)
    if wave == "tri":
        return 4.0 * np.abs(frac - 0.5) - 1.0
    return np.sin(2 * np.pi * phase)


def _envelope(n: int, rate: int, attack: float, decay: float) -> np.ndarray:
    """A quick rise, then an exponential decay with time constant `decay` seconds."""
    t = np.arange(n) / rate
    rise = np.clip(t / attack, 0.0, 1.0) if attack > 0 else np.ones(n)
    return rise * np.exp(-t / decay)


def tone(
    freq: float,
    dur: float,
    rate: int = RATE,
    wave: str = "sine",
    attack: float = 0.003,
    decay: float = 0.08,
    gain: float = 0.6,
) -> Signal:
    t = _t(dur, rate)
    return gain * _wave(freq * t, wave) * _envelope(len(t), rate, attack, decay)


def glide(
    f0: float,
    f1: float,
    dur: float,
    rate: int = RATE,
    wave: str = "sine",
    decay: float = 0.08,
    gain: float = 0.6,
) -> Signal:
    """A tone whose pitch slides from `f0` to `f1`."""
    t = _t(dur, rate)
    freq = f0 + (f1 - f0) * t / max(dur, 1e-9)
    phase = np.cumsum(freq) / rate
    return gain * _wave(phase, wave) * _envelope(len(t), rate, 0.002, decay)


def noise(dur: float, rate: int = RATE, decay: float = 0.01, gain: float = 0.3) -> Signal:
    rng = np.random.default_rng(4004)  # fixed seed: the same click every time
    n = int(dur * rate)
    return gain * rng.uniform(-1.0, 1.0, n) * _envelope(n, rate, 0.0, decay)


def seq(*parts: Signal, gap: float = 0.0, rate: int = RATE) -> Signal:
    """Notes one after the other, each starting `gap` seconds after the previous one ends."""
    silence = np.zeros(int(gap * rate))
    out: list[Signal] = []
    for i, p in enumerate(parts):
        if i:
            out.append(silence)
        out.append(p)
    return np.concatenate(out) if out else np.zeros(0)


def mix(*parts: Signal) -> Signal:
    """Signals played together, from the same start."""
    n = max(len(p) for p in parts)
    out = np.zeros(n)
    for p in parts:
        out[: len(p)] += p
    return out


def finish(signal: Signal, rate: int = RATE) -> Signal:
    """Fade out the last few milliseconds and keep the peak within [-1, 1], as float32."""
    s = np.asarray(signal, dtype=np.float64).copy()
    n = min(len(s), int(FADE * rate))
    if n:
        s[-n:] *= np.linspace(1.0, 0.0, n)
    peak = float(np.max(np.abs(s))) if len(s) else 0.0
    if peak > 1.0:
        s /= peak
    return s.astype(np.float32)


# Notes, in Hz.
C5, E5, G5, C6 = 523.25, 659.25, 783.99, 1046.50
A3, E3 = 220.0, 164.81


def _toggle(rate: int) -> Signal:
    return mix(tone(1200, 0.03, rate, "tri", 0.0, 0.008, 0.5), noise(0.012, rate, 0.003, 0.15))


def _error(rate: int) -> Signal:
    note = {"wave": "square", "decay": 0.06, "gain": 0.22}
    return seq(tone(A3, 0.09, rate, **note), tone(E3, 0.14, rate, **note), gap=0.02, rate=rate)


def _pass(rate: int) -> Signal:
    return seq(tone(E5, 0.08, rate, decay=0.06), tone(C6, 0.25, rate, decay=0.12), rate=rate)


def _fail(rate: int) -> Signal:
    return glide(330, 150, 0.3, rate, "square", decay=0.12, gain=0.22)


def _solved(rate: int) -> Signal:
    notes = [tone(f, 0.09, rate, "tri", decay=0.08) for f in (C5, E5, G5)]
    chord = mix(
        tone(C6, 0.45, rate, "tri", decay=0.2),
        tone(G5, 0.45, rate, decay=0.2, gain=0.3),
        tone(E5, 0.45, rate, decay=0.2, gain=0.2),
    )
    return seq(*notes, chord, rate=rate)


def _move(rate: int) -> Signal:
    return tone(1800, 0.018, rate, "tri", 0.0, 0.006, 0.25)


def _select(rate: int) -> Signal:
    return glide(700, 1100, 0.07, rate, "tri", decay=0.05, gain=0.4)


def _back(rate: int) -> Signal:
    return glide(900, 550, 0.07, rate, "tri", decay=0.05, gain=0.35)


RECIPES: dict[str, Callable[[int], Signal]] = {
    "toggle": _toggle,
    "error": _error,
    "pass": _pass,
    "fail": _fail,
    "solved": _solved,
    "move": _move,
    "select": _select,
    "back": _back,
}


def render(name: str, rate: int = RATE) -> Signal:
    """The finished sound `name` at `rate`: mono float32 in [-1, 1]."""
    return finish(RECIPES[name](rate), rate)


def to_mixer(samples: Signal, size: int, channels: int) -> np.ndarray:
    """`samples` in the mixer's format, from `pygame.mixer.get_init()`'s `size` and `channels`.

    `size` is the bit depth, negative for signed integers; 32 means float32 (SDL's
    AUDIO_F32). More than one channel gives shape (n, channels), the same signal on each.
    """
    s = np.clip(np.asarray(samples, dtype=np.float64), -1.0, 1.0)
    bits = abs(size)
    if size == 32:
        out: np.ndarray = s.astype(np.float32)
    elif size < 0:
        top = 2 ** (bits - 1) - 1
        out = np.round(s * top).astype(f"int{bits}")
    else:
        half = 2 ** (bits - 1)
        out = np.round(s * (half - 1) + half).astype(f"uint{bits}")
    if channels > 1:
        out = np.repeat(out[:, None], channels, axis=1)
    return np.ascontiguousarray(out)
