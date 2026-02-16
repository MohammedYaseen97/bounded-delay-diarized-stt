from __future__ import annotations

"""
Week 2 check: VAD segmentation + online speaker tracking baseline.

This is expected to FAIL until you implement:
- `vad/segmenter.py` (HysteresisHangoverSegmenter)
- `diarization/online_tracker.py` (PrototypeOnlineSpeakerTracker)
"""

import numpy as np

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from common.errors import NotImplementedAssignmentError  # noqa: E402
from diarization.online_tracker import PrototypeOnlineSpeakerTracker  # noqa: E402
from schemas.types import SpeechSegment  # noqa: E402
from toy.toy_embeddings import ToyEmbeddingExtractor  # noqa: E402
from vad.interfaces import VadFrameProbs  # noqa: E402
from vad.segmenter import HysteresisHangoverSegmenter  # noqa: E402


def check_segmenter() -> None:
    # Frame hop = 0.1s, 30 frames => 3.0s
    hop = 0.1
    p = np.array(
        # 0.0-0.4s silence
        [0.1, 0.2, 0.1, 0.2]
        # 0.4-1.6s speech-ish
        + [0.7, 0.8, 0.75, 0.7, 0.65, 0.7, 0.6, 0.55]
        # 1.6-2.0s drop
        + [0.3, 0.2, 0.3, 0.2]
        # 2.0-2.6s speech again
        + [0.7, 0.72, 0.7, 0.68, 0.7, 0.65]
        # 2.6-3.0s silence
        + [0.1, 0.1, 0.2, 0.1],
        dtype=np.float32,
    )
    probs = VadFrameProbs(frame_hop_s=hop, p_speech=p)

    seg = HysteresisHangoverSegmenter(
        start_threshold=0.6,
        end_threshold=0.4,
        hangover_s=0.2,
        min_segment_s=0.3,
        max_segment_s=10.0,
    )
    segments = seg.probs_to_segments(probs, audio_id="toy")

    # Expected: two segments roughly around [0.4, ~1.8] and [2.0, ~2.8]
    assert len(segments) == 2, f"Expected 2 segments, got {len(segments)}: {segments}"
    s0, s1 = segments
    assert abs(s0.start_s - 0.4) < 0.15, s0
    assert s0.end_s > 1.5 and s0.end_s < 2.1, s0
    assert abs(s1.start_s - 2.0) < 0.15, s1
    assert s1.end_s > 2.4 and s1.end_s < 3.0, s1


def check_online_tracking() -> None:
    # Two speakers alternating in four segments.
    segments = [
        SpeechSegment(0.0, 1.0, "toy"),
        SpeechSegment(1.0, 2.0, "toy"),
        SpeechSegment(2.0, 3.0, "toy"),
        SpeechSegment(3.0, 4.0, "toy"),
    ]
    seg_to_spk = {
        (0.0, 1.0): 0,
        (1.0, 2.0): 1,
        (2.0, 3.0): 0,
        (3.0, 4.0): 1,
    }
    emb = ToyEmbeddingExtractor(segment_to_speaker=seg_to_spk, dim=4).embed_segments(
        samples=np.zeros((16000 * 4,), dtype=np.float32),
        sample_rate=16000,
        segments=segments,
    )

    tracker = PrototypeOnlineSpeakerTracker(cosine_threshold=0.25, max_speakers=5, ema_alpha=0.3)
    hyp = tracker.assign(segments, emb)

    # Expected: exactly 2 speaker IDs used, and alternating assignment.
    spk_ids = [t.speaker_id for t in hyp.turns]
    assert len(hyp.turns) == 4
    assert len(set(spk_ids)) == 2, f"Expected 2 speakers, got: {set(spk_ids)}"
    assert spk_ids[0] == spk_ids[2], "Speaker 0 and 2 should match"
    assert spk_ids[1] == spk_ids[3], "Speaker 1 and 3 should match"
    assert spk_ids[0] != spk_ids[1], "Different speakers should be different IDs"


def main() -> int:
    try:
        check_segmenter()
        check_online_tracking()
    except NotImplementedAssignmentError as e:
        print("week2_incomplete", {"hint": str(e)})
        return 2

    print("week2_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

