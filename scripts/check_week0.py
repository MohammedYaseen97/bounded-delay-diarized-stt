from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

from scripts._bootstrap import add_src_to_path


add_src_to_path()

from audio.chunking import iter_chunks  # noqa: E402
from audio.io import generate_sine, load_audio_mono  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", type=str, default="", help="Path to an audio file. If omitted, uses a synthetic sine.")
    ap.add_argument("--chunk_s", type=float, default=1.0)
    ap.add_argument("--hop_s", type=float, default=0.5)
    args = ap.parse_args()

    if args.audio:
        audio = load_audio_mono(Path(args.audio))
    else:
        audio = generate_sine(duration_s=2.2, sr=16000, freq_hz=220.0)

    chunks = list(iter_chunks(audio.samples, audio.sample_rate, chunk_s=args.chunk_s, hop_s=args.hop_s))
    assert chunks, "No chunks produced."

    # monotonic timestamps
    last_end = -math.inf
    for c in chunks:
        assert c.start_s >= 0
        assert c.end_s > c.start_s
        assert c.end_s >= last_end - 1e-9, "Chunk end times must be non-decreasing."
        last_end = c.end_s

    # duration sanity
    approx_end = chunks[-1].end_s
    err = abs(approx_end - audio.duration_s)
    assert err < max(0.02, 2.0 / audio.sample_rate), f"Chunking end mismatch: {err:.6f}s"

    # print stats (human visible)
    total_samples = sum(int(c.samples.shape[0]) for c in chunks)
    print("week0_ok", {
        "sr": audio.sample_rate,
        "duration_s": round(audio.duration_s, 4),
        "num_chunks": len(chunks),
        "first_chunk": (round(chunks[0].start_s, 3), round(chunks[0].end_s, 3)),
        "last_chunk": (round(chunks[-1].start_s, 3), round(chunks[-1].end_s, 3)),
        "sum_chunk_samples": total_samples,
        "note": "Overlap means sum_chunk_samples > num_audio_samples is normal.",
    })

    # extra: basic numerical sanity (no NaNs)
    assert not np.isnan(audio.samples).any()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

