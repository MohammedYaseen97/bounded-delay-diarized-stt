## Streaming diarized STT — assignment framework (Week 0–6)

This file is the “professor handout.” It tells you what to implement each week, and how to self-grade using the check scripts in `scripts/`.

For weekly checklists (“assignment PDFs”), see `assignments/INDEX.md`.

### Rubric (every week)
- **Correctness (50%)**: check scripts pass; semantics match spec.
- **Research signal (20%)**: you can explain tradeoffs (esp. Week 3+), and you produce at least one plot/ablation when asked.
- **Engineering signal (20%)**: reproducible runs, clean interfaces, structured logs, timings.
- **Write-up (10%)**: short notes: what changed, what broke, what you learned.

### Week gates

#### Week 0 — Setup + primer
- **Goal**: remove unknown-unknowns.
- **Pass condition**: `python scripts/check_week0.py` exits 0.
- **Reading gate**: `python scripts/check_reading.py --week 0` exits 0.

#### Week 1 — Offline E2E wiring + output schema
- **Goal**: wire the pipeline and lock down output shapes.
- **Pass condition**: `python scripts/check_week1_offline_e2e.py` exits 0.
- **Reading gate**: `python scripts/check_reading.py --week 1` exits 0.

#### Week 2 — VAD segmentation + online tracking baseline
- **Goal**: implement segmentation and online speaker tracking.
- **Pass condition**: `python scripts/check_week2_vad_and_tracking.py` exits 0.
- **Reading gate**: `python scripts/check_reading.py --week 2` exits 0.

#### Week 3 — Bounded-delay stabilizer (core research)
- **Goal**: implement `D`-bounded revisions + switch penalty, and make the tradeoff measurable.
- **Pass condition**: `python scripts/check_week3_stabilizer.py` exits 0.
- **Reading gate**: `python scripts/check_reading.py --week 3` exits 0.

#### Week 4 — Pseudo-streaming + attribution + latency instrumentation
- **Goal**: make it feel like a product: incremental events, revisions, per-word speaker attribution.
- **Pass condition**: `python scripts/check_week4_streaming_semantics.py` exits 0.
- **Reading gate**: `python scripts/check_reading.py --week 4` exits 0.

#### Week 5 — “Production signal” (CLI-only)
- **Goal**: reproducible runs + artifacts/timings + tests + runbook (no Docker/services).
- **Pass condition**: `bash scripts/check_week5_packaging.sh` exits 0.
- **Reading gate**: `python scripts/check_reading.py --week 5` exits 0.

#### Week 6 — Report + polish
- **Goal**: plots + ablations + error analysis + demo script.
- **Pass condition**: `python scripts/check_week6_report_artifacts.py` exits 0 after you generate `reports/`.
- **Reading gate**: `python scripts/check_reading.py --week 6` exits 0.

