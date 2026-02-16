from __future__ import annotations

"""
Week 1 check: offline E2E wiring + output schema shape.

This uses toy backends so it does not require real ASR/embeddings.
It is expected to fail until you implement the missing assignment components:
- diarization tracker (Week 2)
- stabilizer (Week 3)
- attribution (Week 4)

But the *schema + wiring* should be in place by end of Week 1.
"""

import json
from dataclasses import asdict

import numpy as np

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from schemas.types import DiarizedTranscript, SpeakerTurn, SpeechSegment  # noqa: E402
from toy.toy_asr import ToyAsrBackend  # noqa: E402


def render_minimal_json(audio_id: str, turns: list[SpeakerTurn], words: list[dict]) -> dict:
    return {
        "audio_id": audio_id,
        "turns": [asdict(t) for t in turns],
        "words": words,
        "meta": {"toy": True},
    }


def main() -> int:
    # synthetic "audio"
    sr = 16000
    samples = np.zeros((sr * 3,), dtype=np.float32)  # 3s silence; not used by toy ASR

    segments = [
        SpeechSegment(0.0, 1.0, audio_id="toy"),
        SpeechSegment(1.2, 2.2, audio_id="toy"),
    ]

    # toy ASR produces words within segments
    asr = ToyAsrBackend()
    words = [asdict(w) for w in asr.transcribe(samples, sr, segments)]

    # Week1 only checks schema wiring. We'll invent provisional turns for now.
    turns = [
        SpeakerTurn(0.0, 1.0, "S0"),
        SpeakerTurn(1.2, 2.2, "S1"),
    ]

    obj = render_minimal_json("toy", turns, words)

    # schema-ish checks (minimal)
    assert obj["audio_id"] == "toy"
    assert isinstance(obj["turns"], list) and len(obj["turns"]) == 2
    assert isinstance(obj["words"], list) and len(obj["words"]) == 4
    for w in obj["words"]:
        assert w["start_s"] <= w["end_s"]
        assert isinstance(w["text"], str) and w["text"]

    # deterministic JSON encoding
    s1 = json.dumps(obj, sort_keys=True)
    s2 = json.dumps(obj, sort_keys=True)
    assert s1 == s2

    # Also validate dataclass container exists for later weeks
    dt = DiarizedTranscript(audio_id="toy", words=[], turns=[])
    assert dt.audio_id == "toy"

    print("week1_ok", {"note": "Schema+toy wiring OK. Real diarization/stabilization comes later."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

