## Week 1 — Offline E2E wiring + output schema

### Context
This week is about **wiring** and **interfaces**. You are not trying to win diarization yet. The goal is: the project can run end-to-end in a deterministic toy mode, producing artifacts with stable schemas.

### Checklist (deliverables)
- [ ] Understand the repo contract: `src/{vad,embeddings,diarization,stabilization,asr,fusion,schemas}`
- [ ] Produce an offline JSON output artifact (schema-stable)
- [ ] Produce a human-readable transcript rendering (MD/TXT) from the same output
- [ ] Ensure the run logs per-stage timings (even if stages are stubbed)

### Reading (due this week; prepares Week 2)
- [ ] Complete the Week 1 reading list and notes in `reading/week1.md`
- [ ] Self-check: `python scripts/check_reading.py --week 1`

### Acceptance criteria / grading focus
- **Correctness**: output timestamps are monotonic and data structures are coherent.
- **Engineering**: output schema is stable and versionable (don’t change fields every day).
- **Reproducibility**: toy mode is deterministic.

### Self-check (automated)
Run:

```bash
python scripts/check_week1_offline_e2e.py
```

### Reflection questions (write 5–10 lines)
- What are the “interfaces that must never change” after Week 1?
- Where could latency blow up later, given the pipeline structure?

