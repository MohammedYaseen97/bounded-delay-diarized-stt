from __future__ import annotations

from dataclasses import dataclass

from common.errors import NotImplementedAssignmentError
from schemas.types import SpeakerTurn
from stabilization.interfaces import BoundedDelayStabilizer, StabilizedDiarization


@dataclass
class SwitchCostBoundedDelayStabilizer(BoundedDelayStabilizer):
    """
    TODO (Week 3):
    Implement bounded-delay stabilization:
    - freeze output for time < now - D
    - allow revisions only within [now - D, now]
    - apply switch penalty to discourage A<->B flips
    """

    D_s: float = 1.0
    switch_cost: float = 1.0

    def update(self, now_s: float, provisional_turns: list[SpeakerTurn]) -> StabilizedDiarization:
        raise NotImplementedAssignmentError(
            "Week 3 task: implement bounded-delay stabilization with a revision window D and switch penalty. "
            "Hard constraint: output for time < (now - D) must be frozen; only the last D seconds may change. "
            "Acceptance criteria are enforced by the Week 3 check and described in ASSIGNMENT.md."
        )

