## Week 5 — “Production signal” without production scope (CLI-only)

### Context
You’re targeting a role that expects you to ship and maintain systems. This week delivers the **signal** (reproducible, observable, testable) while staying **pure CLI** (no Docker, no network services, no monitoring stack).

### Checklist (deliverables)
- [ ] Ensure `pytest` suite runs (unit tests + smoke imports)
- [ ] Ensure `scripts/run_offline_pipeline.py --help` and `scripts/run_stream_demo.py --help` work
- [ ] Emit **structured artifacts** per run (JSON output + timing summary + config used)
- [ ] Add unit tests for the two regression magnets: stabilizer + attribution edge cases
- [ ] Write a short runbook section (debugging ladder + tuning knobs + “what broke last time”)

### Reading (due this week; prepares Week 6)
- [ ] Complete the Week 5 reading list and notes in `reading/week5.md`
- [ ] Self-check: `python scripts/check_reading.py --week 5`

### Acceptance criteria / grading focus
- **Reproducibility**: same config produces same behavior in toy mode.
- **Operability**: when something is wrong, you can locate the failing stage quickly via artifacts/timings.
- **Maintainability**: small interfaces, readable outputs, and tests for edge cases.

### Self-check (automated)
Run:

```bash
bash scripts/check_week5_packaging.sh
```

### “Common wrong solutions” (avoid wasting time)
- Spending a week on Docker/CI/network services while the core algorithm is shaky.
- No tests for the stabilizer and attribution—those are the two places regressions hide.

