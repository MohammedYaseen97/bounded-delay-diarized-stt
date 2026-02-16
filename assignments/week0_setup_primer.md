## Week 0 — Setup + “speech systems primer”

### Context
This week exists to eliminate unknown-unknowns so Week 1 doesn’t turn into debugging environment/audio IO instead of building the pipeline.

### Outcomes (what you should be able to say by end of Week 0)
- You can explain the pipeline at a block-diagram level (“what goes in/out of each module”).
- You can load audio, compute duration, and chunk it with correct timestamps.
- You have a rough latency budget and know what you will measure (RTF, p50/p95 latency).

### Checklist (deliverables)
- [ ] Create venv and install `requirements.txt`
- [ ] Run the Week 0 check script successfully
- [ ] Write a 1-page glossary in the repo (your own words; avoid copy-paste)
- [ ] Choose a “gold set” plan (even if you don’t have the data yet): where it will come from + target duration

### Reading (due this week; prepares Week 1)
- [ ] Complete the Week 0 reading list and notes in `reading/week0.md`
- [ ] Self-check: `python scripts/check_reading.py --week 0`

### Acceptance criteria / grading focus
- **Correctness**: chunking timestamps are monotonic and match audio duration.
- **Engineering**: you can run the check script from a clean shell and it succeeds.
- **Understanding**: glossary is meaningful (not just definitions).

### Self-check (automated)
Run:

```bash
python scripts/check_week0.py
```

Optional with real audio:

```bash
python scripts/check_week0.py --audio path/to/file.wav
```

### Notes (non-handholding guardrails)
- Don’t implement resampling yet unless you must. Keep sample rates consistent for now.
- Don’t overthink chunk sizes; choose something reasonable (e.g., chunk 1.0s, hop 0.5s) and move on.

