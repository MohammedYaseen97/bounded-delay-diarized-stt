## Week 4 — Pseudo-streaming + word attribution + latency instrumentation

### Context
This is the “product feel” week. By now you have (or will soon have) diarization + stabilization outputs. This week turns them into an incremental transcript experience with revision semantics and latency metrics.

### Checklist (deliverables)
- [ ] Wire pseudo-streaming in `scripts/run_stream_demo.py` (chunk → process → emit events)
- [ ] Implement `WordToSpeakerAttributor.attribute` in `src/fusion/attribution.py`
- [ ] Define and document an overlap policy (simple is fine; must be explicit)
- [ ] Emit incremental transcript events that support revisions within last `D` seconds
- [ ] Record per-stage timings and summarize p50/p95 latency (even if rough)

### Reading (due this week; prepares Week 5)
- [ ] Complete the Week 4 reading list and notes in `reading/week4.md`
- [ ] Self-check: `python scripts/check_reading.py --week 4`

### Acceptance criteria / grading focus
- **Semantics**: revision events only touch time `>= now - D`.
- **Correctness**: words are attributed consistently with turns under your policy.
- **Observability**: latency and stage timings are visible in outputs/logs.

### Self-check (automated)
Run:

```bash
python scripts/check_week4_streaming_semantics.py
```

### “Common wrong solutions” (avoid wasting time)
- Attribution by “nearest turn midpoint” without overlap reasoning (fails on boundary cases).
- Implicit overlap policy (“whatever happens”)—you need a rule you can defend.

