## Week 5 — Productionization (bounded, CLI-first)

### Context
You’re targeting a role that expects you to ship and maintain systems. This week turns the project into something you can run repeatedly, observe, and debug without heroics.

### Checklist (deliverables)
- [ ] Ensure `pytest` suite runs (unit tests + smoke imports)
- [ ] Ensure `scripts/run_offline_pipeline.py --help` and `scripts/run_stream_demo.py --help` work
- [ ] Produce structured outputs suitable for debugging (timings, configs used)
- [ ] Write a short runbook section (where to look when it breaks)

### Reading (due this week; prepares Week 6)
- [ ] Complete the Week 5 reading list and notes in `reading/week5.md`
- [ ] Self-check: `python scripts/check_reading.py --week 5`

### Acceptance criteria / grading focus
- **Reproducibility**: same config produces same behavior in toy mode.
- **Maintainability**: small interfaces, readable logs/timings, tests for edge cases.

### Self-check (automated)
Run:

```bash
bash scripts/check_week5_packaging.sh
```

### “Common wrong solutions” (avoid wasting time)
- Spending a week on Docker/CI polish while the core algorithm is shaky.
- No tests for the stabilizer and attribution—those are the two places regressions hide.

