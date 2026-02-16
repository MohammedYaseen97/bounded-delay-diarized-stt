from __future__ import annotations

from dataclasses import dataclass

from common.errors import NotImplementedAssignmentError
from schemas.types import SpeakerTurn, Word


@dataclass
class WordToSpeakerAttributor:
    """
    TODO (Week 4):
    Attribute each word to a speaker turn according to an overlap policy.
    Keep it simple and document the policy in code/docstrings.
    """

    def attribute(self, words: list[Word], turns: list[SpeakerTurn]) -> list[tuple[Word, str]]:
        raise NotImplementedAssignmentError(
            "Week 4 task: implement word→speaker attribution with a clearly documented overlap policy. "
            "Goal: produce speaker-attributed words that match your stabilized turns. "
            "Acceptance criteria are enforced by the Week 4 check and described in ASSIGNMENT.md."
        )

