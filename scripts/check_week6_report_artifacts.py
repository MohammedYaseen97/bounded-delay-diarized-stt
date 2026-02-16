from __future__ import annotations

"""
Week 6 check: report artifacts exist and are structured.

This is intentionally light-weight: it checks presence/shape, not plot quality.
It should pass once you generate the final report artifacts.
"""

import argparse
from pathlib import Path


REQUIRED_PLOTS = [
    "flip_rate_vs_D.png",
    "der_vs_D.png",
    "latency_vs_D.png",
]

REQUIRED_REPORT_SECTIONS = [
    "## Summary",
    "## Method",
    "## Results",
    "## Ablations",
    "## Error analysis",
    "## Limitations",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports_dir", type=str, default="reports")
    args = ap.parse_args()

    rdir = Path(args.reports_dir)
    report = rdir / "REPORT.md"

    missing = [p for p in REQUIRED_PLOTS if not (rdir / p).exists()]
    if missing:
        print("week6_incomplete", {"missing_plots": missing, "hint": "Generate plots into reports/ with required names."})
        return 6

    if not report.exists():
        print("week6_incomplete", {"missing": str(report), "hint": "Generate reports/REPORT.md"})
        return 6

    text = report.read_text(encoding="utf-8", errors="replace")
    missing_sections = [s for s in REQUIRED_REPORT_SECTIONS if s not in text]
    if missing_sections:
        print("week6_incomplete", {"missing_sections": missing_sections})
        return 6

    print("week6_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

