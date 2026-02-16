## Week 3 — Bounded-delay stabilizer (core research)

### Context
This is the “research week.” Your baseline (Week 2) will flip speaker IDs in streaming. The goal now is to make speaker labels **feel stable** to a user, while staying low-latency.

You are implementing a **bounded revision policy**:
- output older than `now - D` is frozen
- output within last `D` seconds can be revised

### Checklist (deliverables)
- [ ] Implement `SwitchCostBoundedDelayStabilizer.update` in `src/stabilization/bounded_delay.py`
- [ ] Ensure “finalization boundary” semantics are correct (`< now - D` must never change)
- [ ] Make switch penalty a knob; run at least 3 values of `D` in experiments later
- [ ] Write a 1–2 paragraph explanation: what the stabilizer optimizes and why it reduces flips

### Reading (due this week; prepares Week 4)
- [ ] Complete the Week 3 reading list and notes in `reading/week3.md`
- [ ] Self-check: `python scripts/check_reading.py --week 3`

### Acceptance criteria / grading focus
- **Hard constraint**: frozen prefix (`< now - D`) never changes across updates.
- **Stability**: increasing switch penalty should not increase flip-rate on a flip-heavy synthetic case.
- **Clarity**: you can explain the tradeoff of stability vs delay vs DER.

### Self-check (automated)
Run:

```bash
python scripts/check_week3_stabilizer.py
```

### “Common wrong solutions” (avoid wasting time)
- Rewriting the entire past on every update (violates bounded-delay).
- Applying a penalty but still allowing arbitrary relabeling of the frozen prefix.
- Confusing “speaker label mapping” with “speaker segmentation” (these are different levers).

