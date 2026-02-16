from __future__ import annotations

"""
Week 3 check: bounded-delay stabilizer semantics + switch-penalty behavior.

Expected to FAIL until you implement:
- `stabilization/bounded_delay.py` (SwitchCostBoundedDelayStabilizer)
"""

from collections import Counter

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from common.errors import NotImplementedAssignmentError  # noqa: E402
from schemas.types import SpeakerTurn  # noqa: E402
from stabilization.bounded_delay import SwitchCostBoundedDelayStabilizer  # noqa: E402


def flip_rate(turns: list[SpeakerTurn]) -> int:
    # flip count across consecutive turns
    flips = 0
    for a, b in zip(turns, turns[1:]):
        if a.speaker_id != b.speaker_id:
            flips += 1
    return flips


def check_finalization_boundary() -> None:
    stab = SwitchCostBoundedDelayStabilizer(D_s=1.0, switch_cost=1.0)

    # Provisional turns cover 0..4 seconds.
    provisional = [
        SpeakerTurn(0.0, 1.0, "A"),
        SpeakerTurn(1.0, 2.0, "B"),
        SpeakerTurn(2.0, 3.0, "A"),
        SpeakerTurn(3.0, 4.0, "B"),
    ]

    out = stab.update(now_s=4.0, provisional_turns=provisional)
    assert abs(out.revision_start_s - 3.0) < 1e-6, "revision_start_s should be now - D"
    # Anything strictly before 3.0 must be frozen across subsequent updates.
    out2 = stab.update(now_s=4.5, provisional_turns=provisional)
    frozen1 = [t for t in out.turns if t.end_s <= 3.0 + 1e-9]
    frozen2 = [t for t in out2.turns if t.end_s <= 3.5 - 1.0 + 1e-9]  # now - D = 3.5
    assert frozen1, "Expected some frozen turns."
    assert frozen1 == frozen2[: len(frozen1)], "Frozen prefix must not change."


def check_switch_penalty_monotonic() -> None:
    # A flip-heavy provisional timeline
    provisional = [
        SpeakerTurn(0.0, 0.5, "A"),
        SpeakerTurn(0.5, 1.0, "B"),
        SpeakerTurn(1.0, 1.5, "A"),
        SpeakerTurn(1.5, 2.0, "B"),
        SpeakerTurn(2.0, 2.5, "A"),
        SpeakerTurn(2.5, 3.0, "B"),
    ]

    # With higher switch cost, flip-rate should not increase on this synthetic fixture.
    out_low = SwitchCostBoundedDelayStabilizer(D_s=3.0, switch_cost=0.0).update(3.0, provisional).turns
    out_hi = SwitchCostBoundedDelayStabilizer(D_s=3.0, switch_cost=10.0).update(3.0, provisional).turns
    assert flip_rate(out_hi) <= flip_rate(out_low), {"low": flip_rate(out_low), "hi": flip_rate(out_hi)}

    # And speaker IDs used should be a subset of the originals (no new IDs invented here)
    c = Counter([t.speaker_id for t in out_hi])
    assert set(c.keys()).issubset({"A", "B"})


def main() -> int:
    try:
        check_finalization_boundary()
        check_switch_penalty_monotonic()
    except NotImplementedAssignmentError as e:
        print("week3_incomplete", {"hint": str(e)})
        return 3

    print("week3_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

