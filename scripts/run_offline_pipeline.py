from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from audio.io import load_audio_mono  # noqa: E402
from common.timing import StageTimings  # noqa: E402
from schemas.types import DiarizedTranscript, SpeakerTurn, SpeechSegment, Word  # noqa: E402
from toy.toy_asr import ToyAsrBackend  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Offline diarized STT pipeline (scaffold).")
    ap.add_argument("--audio", type=str, required=True)
    ap.add_argument("--out_json", type=str, default="out.json")
    args = ap.parse_args()

    timings = StageTimings()
    with timings.time("audio_load"):
        audio = load_audio_mono(Path(args.audio))

    # NOTE: This is a *hook* script. Full diarization wiring is your work across weeks.
    # For now we produce a minimal artifact so you can plug in modules incrementally.
    segments = [SpeechSegment(0.0, audio.duration_s, audio_id=Path(args.audio).stem)]

    # Toy ASR backend (deterministic; real ASR integration is part of your later work)
    asr = ToyAsrBackend()
    with timings.time("asr_toy"):
        words = asr.transcribe(audio.samples, audio.sample_rate, segments)

    # Placeholder turns (replace with your diarization + stabilizer + attribution outputs)
    turns = [SpeakerTurn(0.0, audio.duration_s, "S0")]

    obj = DiarizedTranscript(
        audio_id=Path(args.audio).stem,
        words=list(words),
        turns=turns,
        meta={"timings": timings.summary(), "asr": "toy", "sr": audio.sample_rate},
    )

    out = {
        "audio_id": obj.audio_id,
        "words": [asdict(w) for w in obj.words],
        "turns": [asdict(t) for t in obj.turns],
        "meta": obj.meta,
    }
    Path(args.out_json).write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print("wrote", args.out_json)
    print("timings", json.dumps(timings.summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

