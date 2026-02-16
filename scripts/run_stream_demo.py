from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from audio.chunking import iter_chunks  # noqa: E402
from audio.io import load_audio_mono  # noqa: E402
from common.timing import StageTimings  # noqa: E402
from schemas.types import TranscriptEvent  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Pseudo-streaming demo (CLI).")
    ap.add_argument("--audio", type=str, required=True)
    ap.add_argument("--chunk_s", type=float, default=1.0)
    ap.add_argument("--hop_s", type=float, default=0.5)
    ap.add_argument("--D", type=float, default=1.0, help="Revision window in seconds.")
    args = ap.parse_args()

    timings = StageTimings()
    audio = load_audio_mono(Path(args.audio))

    # This script is a scaffold: you will wire VAD/embeddings/diarization/stabilizer/ASR over time.
    # For now it emits timing + placeholder events so you can focus on Week 4 semantics later.
    now_s = 0.0
    for chunk in iter_chunks(audio.samples, audio.sample_rate, chunk_s=args.chunk_s, hop_s=args.hop_s):
        with timings.time("chunk_loop"):
            now_s = chunk.end_s
            ev = TranscriptEvent(
                type="revision",
                now_s=now_s,
                revision_start_s=max(0.0, now_s - args.D),
                items=[],
            )
            print(json.dumps(asdict(ev), sort_keys=True))

    print("timings", json.dumps(timings.summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

