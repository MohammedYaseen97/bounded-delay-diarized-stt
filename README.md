## Streaming diarized STT (assignment harness)

This repo is structured like a professor-style assignment: you implement the core algorithms, while the repo provides stable interfaces + week-by-week checks so you can self-grade.

### Quickstart

- **Install (core dev)**:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- **Run checks** (these will fail until you complete the TODOs for each week):

```bash
python scripts/check_week0.py
python scripts/check_week1_offline_e2e.py
python scripts/check_week2_vad_and_tracking.py
python scripts/check_week3_stabilizer.py
python scripts/check_week4_streaming_semantics.py
python scripts/check_week6_report_artifacts.py
```

### Key idea

The stabilizer is allowed to revise speaker labels only within a rolling window of `D` seconds. Anything older than `now - D` is frozen.

