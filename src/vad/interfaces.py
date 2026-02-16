from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from schemas.types import SpeechSegment


@dataclass(frozen=True)
class VadFrameProbs:
    """
    Speech probability per frame.
    - `frame_hop_s`: time between frames (e.g., 0.02s)
    - `p_speech`: shape (T,)
    """

    frame_hop_s: float
    p_speech: np.ndarray


class VadModel(ABC):
    @abstractmethod
    def infer_frame_probs(self, samples: np.ndarray, sample_rate: int) -> VadFrameProbs:
        raise NotImplementedError


class Segmenter(ABC):
    """
    Converts frame-level speech probabilities into speech segments.
    This is an assignment component (hysteresis + hangover + min/max durations).
    """

    @abstractmethod
    def probs_to_segments(self, probs: VadFrameProbs, audio_id: str = "audio") -> list[SpeechSegment]:
        raise NotImplementedError

