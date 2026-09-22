"""
G5: deferred cross-reference register.

WHY THIS EXISTS: notes legitimately defer to chapters that aren't written yet --
e.g. the Kimball Ch.9 note says its SCD material "builds on Ch.5 / Ch.7 (not yet
synthesized)". Nothing currently brings those back for review once the deferred
chapter IS synthesized, so a later note could contradict an earlier one and nobody
would notice. No tool can check semantic consistency, but a tool CAN guarantee the
question gets re-asked at the right moment.

WHAT IT DOES: scans notes for deferral phrases ("not yet synthesized", "when those
are done", "revisit ... once"), records each (note -> deferred target) pair in
audit/DEFERRED_REFS.csv, and reports any deferral whose target chapter is NOW
synthesized -- those are DUE FOR REVIEW. Existing rows keep their `reviewed`
marking across runs, so clearing one is durable.

Exit code is non-zero only when a deferral is due for review and not yet marked
reviewed -- i.e. it blocks silently leaving a known-stale cross-reference.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/check_deferred_refs.py"
"""
import csv
import glob
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
AUDIT_DIR = os.path.join(BOOK_DIR, "audit")
NOTES_DIR = os.path.join(BOOK_DIR, "notes")
REGISTER = os.path.join(AUDIT_DIR, "DEFERRED_REFS.csv")

FIELDS = ["note", "deferred_to_source", "deferred_to_chapter_hint", "context", "reviewed"]

# Sentences that signal "this note is leaning on something not yet written"
DEFERRAL_RE = re.compile(
    r"[^.\n]*\b(not yet synthesized|once (?:those|these|they) (?:are|exist)|"
    r"revisit(?:ed)? .{0,40}once|when (?:those|these) are (?:done|written|synthesized))\b[^.\n]*\.",
    re.I,
)
# Chapter hints inside that sentence: "Ch.5", "Chapter 7", "Ch.5/Ch.7"
CHAPTER_HINT_RE = re.compile(r"\bCh(?:apter)?\.?\s*(\d{1,2})\b", re.I)


def load_prior():
    prior = {}
    if os.path.exists(REGISTER):
        with open(REGISTER, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = (r["note"], r["deferred_to_source"], r["deferred_to_chapter_hint"])
                prior[key] = r.get("reviewed", "")
    return prior


def chapter_is_synthesized(stats, sid, chapter_number):
    for s in stats:
        if s["source_id"] != sid:
            continue
        m = re.search(r"\b(\d{1,2})\b", s["chapter_title"])
        if m and int(m.group(1)) == chapter_number and s.get("status") == "synthesized":
            return True
    return False


def main():
    with open(os.path.join(AUDIT_DIR, "chapter_stats.json"), encoding="utf-8") as f:
        stats = json.load(f)
    prior = load_prior()

    rows = []
    for path in sorted(glob.glob(os.path.join(NOTES_DIR, "**", "*.md"), recursive=True)):
        sid = os.path.relpath(path, NOTES_DIR).split(os.sep)[0]
        rel = os.path.relpath(path, BOOK_DIR)
        text = io.open(path, encoding="utf-8").read()
        for m in DEFERRAL_RE.finditer(text):
            sentence = " ".join(m.group(0).split())
            hints = CHAPTER_HINT_RE.findall(sentence)
            if not hints:
                hints = [""]
            for h in set(hints):
                key = (rel, sid, h)
                rows.append({
                    "note": rel,
                    "deferred_to_source": sid,
                    "deferred_to_chapter_hint": h,
                    "context": sentence[:180],
                    "reviewed": prior.get(key, ""),
                })

    # de-duplicate
    seen = set()
    deduped = []
    for r in rows:
        k = (r["note"], r["deferred_to_source"], r["deferred_to_chapter_hint"])
        if k in seen:
            continue
        seen.add(k)
        deduped.append(r)

    with open(REGISTER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(deduped)

    due = []
    for r in deduped:
        if r["reviewed"].strip():
            continue
        h = r["deferred_to_chapter_hint"]
        if h and chapter_is_synthesized(stats, r["deferred_to_source"], int(h)):
            due.append(r)

    print(f"wrote {REGISTER}")
    print(f"deferred cross-references tracked: {len(deduped)}")
    print(f"  already reviewed: {sum(1 for r in deduped if r['reviewed'].strip())}")
    print(f"  target not yet synthesized (nothing to do yet): "
          f"{len(deduped) - len(due) - sum(1 for r in deduped if r['reviewed'].strip())}")

    if due:
        print(f"\nDUE FOR REVIEW: {len(due)} deferral(s) whose target chapter is now synthesized:")
        for r in due:
            print(f"  {r['note']} -> {r['deferred_to_source']} Ch.{r['deferred_to_chapter_hint']}")
            print(f"     context: {r['context'][:120]}")
        print("\nRe-read both notes for contradiction, then set `reviewed` in "
              "audit/DEFERRED_REFS.csv (e.g. 'checked-<date>') to clear this.")
        return 1

    print("PASS: no deferred cross-reference is currently due for review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
