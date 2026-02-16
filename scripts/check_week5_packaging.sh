#!/usr/bin/env bash
set -euo pipefail

echo "[week5] running unit tests"
python -m pytest -q

echo "[week5] checking that required scripts exist"
test -f "scripts/run_offline_pipeline.py" || { echo "missing scripts/run_offline_pipeline.py"; exit 5; }
test -f "scripts/run_stream_demo.py" || { echo "missing scripts/run_stream_demo.py"; exit 5; }

echo "[week5] checking logs/metrics output contract (dry-run)"
# This is a dry-run: the scripts should create artifacts when run with real audio.
# For now we only ensure they can be imported/executed with --help.
python scripts/run_offline_pipeline.py --help >/dev/null
python scripts/run_stream_demo.py --help >/dev/null

echo "week5_ok"

