## Week 6 — Report + polish (interview-ready)

### Context
This week is about turning work into a clear research + engineering story. The output should look like: “I can build systems and I can reason about speech tradeoffs.”

### Checklist (deliverables)
- [ ] Generate final plots into `reports/`:
  - `flip_rate_vs_D.png`
  - `der_vs_D.png`
  - `latency_vs_D.png`
- [ ] Write `reports/REPORT.md` with required sections:
  - Summary, Method, Results, Ablations, Error analysis, Limitations
- [ ] Do a robustness pass (pick 3 failure modes and document what happens)
- [ ] Prepare a 10–15 minute demo script flow (what you’ll show + what you’ll say)

### Reading (due this week; wrap-up)
- [ ] Complete the Week 6 wrap-up notes in `reading/week6.md`
- [ ] Self-check: `python scripts/check_reading.py --week 6`

### Acceptance criteria / grading focus
- **Clarity**: tradeoffs are explicit; plots are interpretable.
- **Honesty**: limitations are concrete and correct (not generic).
- **Story**: you can explain the stabilizer and why bounded delay matters.

### Self-check (automated)
Run after generating `reports/`:

```bash
python scripts/check_week6_report_artifacts.py
```

