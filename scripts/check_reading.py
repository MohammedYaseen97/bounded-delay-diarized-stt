from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_HEADINGS = [
    r"^###\s+Checklist",
    r"^###\s+Key takeaways",
    r"^###\s+Terms I can now explain",
    r"^###\s+Questions / confusions",
]


def count_checked_boxes(text: str) -> tuple[int, int]:
    total = len(re.findall(r"^- \[[ xX]\] ", text, flags=re.MULTILINE))
    checked = len(re.findall(r"^- \[[xX]\] ", text, flags=re.MULTILINE))
    return checked, total


def main() -> int:
    ap = argparse.ArgumentParser(description="Check that weekly reading notes are filled (lightweight).")
    ap.add_argument("--week", type=int, required=True, help="Week number 0..6")
    args = ap.parse_args()

    if args.week < 0 or args.week > 6:
        raise SystemExit("week must be 0..6")

    path = Path("reading") / f"week{args.week}.md"
    if not path.exists():
        print("reading_incomplete", {"missing": str(path)})
        return 10

    text = path.read_text(encoding="utf-8", errors="replace")

    missing = [h for h in REQUIRED_HEADINGS if re.search(h, text, flags=re.MULTILINE) is None]
    if missing:
        print("reading_incomplete", {"missing_headings_regex": missing})
        return 11

    checked, total = count_checked_boxes(text)
    if total > 0 and checked == 0:
        print("reading_incomplete", {"hint": "No checklist items checked. Mark what you finished.", "file": str(path)})
        return 12

    # Ensure TODO placeholders are reduced (not perfect, but catches empty files)
    todo_count = len(re.findall(r"\bTODO\b", text))
    if todo_count >= 6:
        print("reading_incomplete", {"hint": "Too many TODO placeholders; add real notes.", "file": str(path)})
        return 13

    print("reading_ok", {"file": str(path), "checked": checked, "total": total})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

