from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Sequence


@dataclass(frozen=True)
class SpeechSegment:
    """A contiguous span of detected speech."""

    start_s: float
    end_s: float
    audio_id: str = "audio"


@dataclass(frozen=True)
class Word:
    start_s: float
    end_s: float
    text: str
    confidence: float | None = None


@dataclass(frozen=True)
class SpeakerTurn:
    start_s: float
    end_s: float
    speaker_id: str


TranscriptEventType = Literal["partial", "revision", "final"]


@dataclass(frozen=True)
class TranscriptEvent:
    """
    Streaming output event.

    - `now_s`: timestamp of emission.
    - `revision_start_s`: earliest time that may be revised in this event.
      For bounded-delay stabilization, this is typically `max(0, now_s - D)`.
    - `items`: implementation-defined payload (segments/words/turns).
    """

    type: TranscriptEventType
    now_s: float
    revision_start_s: float
    items: Sequence[Any] = field(default_factory=list)


@dataclass(frozen=True)
class DiarizedTranscript:
    """
    Offline output artifact (final).
    Keep this minimal; add fields only when necessary for evaluation/demo.
    """

    audio_id: str
    words: list[Word]
    turns: list[SpeakerTurn]
    meta: dict[str, Any] = field(default_factory=dict)

