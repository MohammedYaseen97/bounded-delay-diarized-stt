from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from schemas.types import SpeakerTurn


@dataclass(frozen=True)
class StabilizedDiarization:
    turns: list[SpeakerTurn]
    revision_start_s: float


class BoundedDelayStabilizer(ABC):
    """
    TODO (Week 3):
    Stabilize speaker labels with bounded revision window D and switch penalty.
    """

    @abstractmethod
    def update(self, now_s: float, provisional_turns: list[SpeakerTurn]) -> StabilizedDiarization:
        raise NotImplementedError

