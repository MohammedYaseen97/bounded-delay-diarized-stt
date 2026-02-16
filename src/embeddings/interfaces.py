from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from schemas.types import SpeechSegment


class EmbeddingExtractor(ABC):
    @abstractmethod
    def embed_segments(self, samples: np.ndarray, sample_rate: int, segments: list[SpeechSegment]) -> np.ndarray:
        """
        Returns embeddings of shape (N, D).
        """
        raise NotImplementedError

