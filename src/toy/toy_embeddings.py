from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from embeddings.interfaces import EmbeddingExtractor
from schemas.types import SpeechSegment


@dataclass
class ToyEmbeddingExtractor(EmbeddingExtractor):
    """
    Deterministic toy embeddings.

    You provide a `speaker_hint` per segment via `segment_to_speaker`.
    Embedding is a unit vector for that speaker plus small deterministic noise.
    """

    segment_to_speaker: dict[tuple[float, float], int]
    dim: int = 4
    noise: float = 0.01

    def embed_segments(self, samples: np.ndarray, sample_rate: int, segments: list[SpeechSegment]) -> np.ndarray:
        out = np.zeros((len(segments), self.dim), dtype=np.float32)
        for i, seg in enumerate(segments):
            key = (float(seg.start_s), float(seg.end_s))
            spk = int(self.segment_to_speaker.get(key, 0))
            v = np.zeros((self.dim,), dtype=np.float32)
            v[spk % self.dim] = 1.0
            # deterministic "noise"
            v = v + (self.noise * (i + 1)) * np.linspace(0.0, 1.0, self.dim, dtype=np.float32)
            v = v / (np.linalg.norm(v) + 1e-8)
            out[i] = v
        return out

