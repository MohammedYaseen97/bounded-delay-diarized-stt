from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from common.errors import NotImplementedAssignmentError
from diarization.interfaces import DiarizationHypothesis, OnlineSpeakerTracker
from schemas.types import SpeechSegment


@dataclass
class PrototypeOnlineSpeakerTracker(OnlineSpeakerTracker):
    """
    TODO (Week 2):
    Implement online speaker tracking using prototypes (centroids) with:
    - cosine distance gating
    - EMA or count-weighted updates
    - new-speaker creation and inactivity decay
    """

    cosine_threshold: float = 0.35
    max_speakers: int = 20
    ema_alpha: float = 0.2
    inactivity_s: float = 30.0

    def assign(self, segments: list[SpeechSegment], embeddings: np.ndarray) -> DiarizationHypothesis:
        raise NotImplementedAssignmentError(
            "Week 2 task: implement online speaker tracking (prototype updates + gating + speaker lifecycle). "
            "Goal: a deterministic baseline you can later improve with stabilization (Week 3). "
            "Acceptance criteria are enforced by the Week 2 check and described in ASSIGNMENT.md."
        )

