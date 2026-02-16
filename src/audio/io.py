from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf


@dataclass(frozen=True)
class Audio:
    samples: np.ndarray  # shape: (n,) float32
    sample_rate: int

    @property
    def duration_s(self) -> float:
        return float(self.samples.shape[0]) / float(self.sample_rate)


def load_audio_mono(path: str | Path, target_sr: int | None = None) -> Audio:
    """
    Load audio as mono float32.

    Notes:
    - Resampling is intentionally NOT implemented here to keep Week 0/1 simple.
      If you need it later, add an optional resampler behind a feature flag.
    """
    samples, sr = sf.read(str(path), always_2d=False)
    if samples.ndim == 2:
        samples = samples.mean(axis=1)
    samples = samples.astype(np.float32)

    if target_sr is not None and target_sr != sr:
        raise ValueError(
            f"Resampling not implemented yet (got sr={sr}, target_sr={target_sr}). "
            "Keep sr consistent for now, or add resampling later."
        )

    return Audio(samples=samples, sample_rate=int(sr))


def generate_sine(duration_s: float = 2.0, sr: int = 16000, freq_hz: float = 220.0) -> Audio:
    t = np.arange(int(duration_s * sr), dtype=np.float32) / float(sr)
    x = 0.1 * np.sin(2.0 * np.pi * freq_hz * t)
    return Audio(samples=x.astype(np.float32), sample_rate=sr)

