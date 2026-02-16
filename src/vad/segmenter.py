from __future__ import annotations

from dataclasses import dataclass

from common.errors import NotImplementedAssignmentError
from schemas.types import SpeechSegment
from vad.interfaces import Segmenter, VadFrameProbs


@dataclass
class HysteresisHangoverSegmenter(Segmenter):
    """
    TODO (Week 2):
    Implement a segmentation policy with:
    - hysteresis: start threshold > end threshold
    - hangover: keep speech \"on\" for a short time after falling below end threshold
    - min/max segment duration
    """

    start_threshold: float = 0.6
    end_threshold: float = 0.4
    hangover_s: float = 0.2
    min_segment_s: float = 0.3
    max_segment_s: float = 15.0

    def probs_to_segments(self, probs: VadFrameProbs, audio_id: str = "audio") -> list[SpeechSegment]:
        raise NotImplementedAssignmentError(
            "Week 2 task: implement VAD→segments with hysteresis + hangover + min/max duration. "
            "Target: stable, product-usable segments (not perfect VAD). "
            "Acceptance criteria are enforced by the Week 2 check and described in ASSIGNMENT.md."
        )

