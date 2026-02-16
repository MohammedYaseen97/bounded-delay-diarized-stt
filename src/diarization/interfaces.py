from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from schemas.types import SpeakerTurn, SpeechSegment


@dataclass(frozen=True)
class DiarizationHypothesis:
    """
    Minimal output of online diarization for a set of speech segments.
    """

    turns: list[SpeakerTurn]
    # Optional debug info can be added in meta if needed.
    meta: dict[str, object] | None = None


class OnlineSpeakerTracker(ABC):
    """
    TODO (Week 2):
    Online assignment/clustering over speaker embeddings.
    """

    @abstractmethod
    def assign(self, segments: list[SpeechSegment], embeddings: np.ndarray) -> DiarizationHypothesis:
        raise NotImplementedError

