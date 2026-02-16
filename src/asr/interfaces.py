from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from schemas.types import SpeechSegment, Word


class AsrBackend(ABC):
    @abstractmethod
    def transcribe(self, samples: np.ndarray, sample_rate: int, segments: list[SpeechSegment]) -> list[Word]:
        """
        Transcribe speech segments and return word timestamps.
        """
        raise NotImplementedError

