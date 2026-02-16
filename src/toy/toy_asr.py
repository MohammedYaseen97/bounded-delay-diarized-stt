from __future__ import annotations

import numpy as np

from asr.interfaces import AsrBackend
from schemas.types import SpeechSegment, Word


class ToyAsrBackend(AsrBackend):
    """
    Deterministic toy ASR.
    For each segment, emits two words whose timestamps lie within the segment.
    """

    def transcribe(self, samples: np.ndarray, sample_rate: int, segments: list[SpeechSegment]) -> list[Word]:
        words: list[Word] = []
        for i, seg in enumerate(segments):
            mid = (seg.start_s + seg.end_s) / 2.0
            words.append(Word(start_s=seg.start_s, end_s=mid, text=f"w{i}_a", confidence=1.0))
            words.append(Word(start_s=mid, end_s=seg.end_s, text=f"w{i}_b", confidence=1.0))
        return words

