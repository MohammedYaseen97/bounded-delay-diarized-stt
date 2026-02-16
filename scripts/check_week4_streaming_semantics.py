from __future__ import annotations

"""
Week 4 check: streaming event semantics + word-to-speaker attribution.

Expected to FAIL until you implement:
- `fusion/attribution.py` (WordToSpeakerAttributor)
Optionally depends on stabilizer semantics for revision window correctness.
"""

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from common.errors import NotImplementedAssignmentError  # noqa: E402
from fusion.attribution import WordToSpeakerAttributor  # noqa: E402
from schemas.types import SpeakerTurn, TranscriptEvent, Word  # noqa: E402


def check_attribution_overlap_policy() -> None:
    words = [
        Word(0.0, 0.5, "hello", 1.0),
        Word(0.5, 1.0, "world", 1.0),
        Word(1.0, 1.5, "foo", 1.0),
    ]
    turns = [
        SpeakerTurn(0.0, 1.0, "S0"),
        SpeakerTurn(1.0, 2.0, "S1"),
    ]
    attrib = WordToSpeakerAttributor().attribute(words, turns)
    assert len(attrib) == len(words)
    assert attrib[0][1] == "S0"
    assert attrib[1][1] == "S0"
    assert attrib[2][1] == "S1"


def check_revision_window_semantics() -> None:
    # For bounded-delay, events should only claim revisions within last D seconds.
    D = 1.0
    now = 4.0
    rev_start = now - D
    ev = TranscriptEvent(type="revision", now_s=now, revision_start_s=rev_start, items=[])
    assert abs(ev.revision_start_s - 3.0) < 1e-9


def main() -> int:
    try:
        check_attribution_overlap_policy()
        check_revision_window_semantics()
    except NotImplementedAssignmentError as e:
        print("week4_incomplete", {"hint": str(e)})
        return 4

    print("week4_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

