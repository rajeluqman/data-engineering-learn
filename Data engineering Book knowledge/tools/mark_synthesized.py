"""
Marks a chapter as status=synthesized in both CHAPTER_MAP.csv and chapter_stats.json.
Run this as the last step of writing a note (EXECUTION_SPEC.md C3 step 5).

Usage:
  .tools/venv/Scripts/python.exe tools/mark_synthesized.py <source_id> "<title substring>"

Matches by source_id + case-insensitive substring of the title (must match exactly one
row in CHAPTER_MAP.csv, or it refuses to guess).
"""
import csv
import json
import os
import sys

AUDIT_DIR = os.path.join(os.path.dirname(__file__), "..", "audit")
CHAPTER_MAP = os.path.join(AUDIT_DIR, "CHAPTER_MAP.csv")
CHAPTER_STATS = os.path.join(AUDIT_DIR, "chapter_stats.json")


def main():
    if len(sys.argv) != 3:
        print("usage: mark_synthesized.py <source_id> \"<title substring>\"")
        return 1
    sid, needle = sys.argv[1], sys.argv[2].lower()

    with open(CHAPTER_MAP, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fieldnames = rows[0].keys() if rows else []

    matches = [r for r in rows if r["source_id"] == sid and needle in r["title"].lower()]
    if len(matches) != 1:
        print(f"REFUSING: found {len(matches)} matching rows for source_id={sid!r} title~={needle!r}")
        for m in matches:
            print("  ", m["title"])
        return 1

    for r in rows:
        if r is matches[0]:
            r["status"] = "synthesized"

    with open(CHAPTER_MAP, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    if os.path.exists(CHAPTER_STATS):
        with open(CHAPTER_STATS, encoding="utf-8") as f:
            stats = json.load(f)
        n = 0
        for s in stats:
            if s["source_id"] == sid and needle in s["chapter_title"].lower():
                s["status"] = "synthesized"
                n += 1
        with open(CHAPTER_STATS, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"chapter_stats.json: updated {n} record(s)")

    print(f"CHAPTER_MAP.csv: marked synthesized -> {matches[0]['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
