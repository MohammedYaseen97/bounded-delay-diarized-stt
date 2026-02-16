from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from vad.interfaces import VadFrameProbs, VadModel


@dataclass
class ToyVadModel(VadModel):
    """
    Toy VAD that returns a provided probability series.
    This is only used by check scripts.
    """

    frame_hop_s: float
    p_speech: np.ndarray

    def infer_frame_probs(self, samples: np.ndarray, sample_rate: int) -> VadFrameProbs:
        return VadFrameProbs(frame_hop_s=float(self.frame_hop_s), p_speech=self.p_speech.astype(np.float32))

