from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class AudioChunk:
    start_s: float
    end_s: float
    samples: np.ndarray  # view/copy of mono float32


def iter_chunks(
    samples: np.ndarray,
    sample_rate: int,
    chunk_s: float,
    hop_s: float | None = None,
):
    """
    Yield overlapping chunks.

    - `chunk_s`: chunk duration in seconds (e.g., 1.0)
    - `hop_s`: hop in seconds. If None, hop == chunk (no overlap).
    """
    if hop_s is None:
        hop_s = chunk_s
    if chunk_s <= 0 or hop_s <= 0:
        raise ValueError("chunk_s and hop_s must be > 0")

    n = int(samples.shape[0])
    chunk_n = max(1, int(round(chunk_s * sample_rate)))
    hop_n = max(1, int(round(hop_s * sample_rate)))

    i = 0
    while i < n:
        j = min(n, i + chunk_n)
        start_s = i / float(sample_rate)
        end_s = j / float(sample_rate)
        yield AudioChunk(start_s=start_s, end_s=end_s, samples=samples[i:j].astype(np.float32, copy=False))
        if j >= n:
            break
        i += hop_n

