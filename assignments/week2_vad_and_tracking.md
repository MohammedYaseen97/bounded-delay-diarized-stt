## Week 2 — VAD segmentation + online diarization baseline

### Context
This is the “baseline week.” You implement the first real speech-system decisions:
- what counts as a segment (segmentation policy)
- how speakers are tracked online (prototypes + gating + lifecycle)

You are optimizing for a baseline that is **deterministic**, **bounded**, and **measurable**. Not perfect diarization.

### Checklist (deliverables)
- [ ] Implement `HysteresisHangoverSegmenter.probs_to_segments` in `src/vad/segmenter.py`
- [ ] Implement `PrototypeOnlineSpeakerTracker.assign` in `src/diarization/online_tracker.py`
- [ ] Document your key thresholds and why they exist (short note in code/docstring)
- [ ] Produce baseline metrics on your gold set (flip-rate at minimum; DER if labeled)

### Reading (due this week; prepares Week 3)
- [ ] Complete the Week 2 reading list and notes in `reading/week2.md`
- [ ] Self-check: `python scripts/check_reading.py --week 2`

### Acceptance criteria / grading focus
- **Correctness**:
  - segmenter respects hysteresis and hangover semantics
  - tracker assigns stable speaker IDs for a simple 2-speaker alternating case
- **Bounded behavior**:
  - tracker does not create unbounded new speakers on small noise
  - thresholds are explicit knobs
- **Determinism**:
  - fixed seed/config produces identical assignments

### Self-check (automated)
Run:

```bash
python scripts/check_week2_vad_and_tracking.py
```

### “Common wrong solutions” (avoid wasting time)
- Segments too short: you’ll explode speaker switching and make embeddings unreliable.
- No hangover: you’ll split turns on every micro-pause.
- Over-eager new-speaker creation: you’ll fragment speakers into many IDs.

