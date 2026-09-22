"""
Lints notes/**/*.md for provenance discipline (EXECUTION_SPEC.md A4).

Checks:
1. Every substantive bullet/paragraph line ends with a provenance tag `[S]`/`[D]`/
   `[N]`/`[U]` (checked on lines that look like claims: start with "- " or contain
   a page citation, and are not headers/tables/code).
2. Flags "unverifiable external claim" patterns (comparisons to things not in the
   corpus) unless the line is tagged `[U]` or contains "NOT CHECKED" / "not checked"
   / "no lookup" / "no comparison" (i.e. the claim is explicitly disclaimed).
3. Flags hedged/approximate numbers ("~123", "roughly", "about N", "approx") where
   chapter_stats.json has an exact figure for that chapter -- hand-typed approximate
   numbers are how a wrong word count got past review before.

This is a lint, not a hard gate on its own for #1/#3 (reported as WARN) but #2 is a
hard FAIL, since it's the exact defect class (unverifiable-external-claim-as-evidence)
found in the audit.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/lint_notes.py"
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NOTES_DIR = os.path.join(os.path.dirname(__file__), "..", "notes")

TAG_RE = re.compile(r"`\[(S|D|N|U)\]`")
CLAIM_LINE_RE = re.compile(r"^\s*-\s+\S|\(p\.?\s*\d+")
SKIP_LINE_RE = re.compile(r"^\s*(#|\||```|<!--|\*\*Source|\*\*PDF|\*\*Chapter|\*\*Synthesis|\*\*Provenance|\*\*Author)")

EXTERNAL_CLAIM_PATTERNS = [
    re.compile(r"matches the .*(catalog|database|registry)", re.I),
    re.compile(r"the original (book|edition)\b(?!.*not (in hand|checked|available))", re.I),
    re.compile(r"the industry[- ]standard\b", re.I),
    re.compile(r"\bas of \d{4}\b.{0,40}(market|industry)", re.I),
    re.compile(r"(?<!not )(?<!not as )independently verified\b", re.I),
]
DISCLAIM_RE = re.compile(
    r"not checked|no lookup|no comparison|not in hand|NOT CHECKED|"
    r"without checking|don't cite|do not cite|not the industry|"
    r'not\s+["“]|no benchmark|unverifiable',
    re.I,
)

HEDGE_RE = re.compile(r"~\s*\d|(?:\bapprox(?:imately)?\.?\b|\broughly\b|\babout\s+\d)", re.I)


def main():
    files = sorted(glob.glob(os.path.join(NOTES_DIR, "**", "*.md"), recursive=True))
    if not files:
        print("No note files found under notes/.")
        return 0

    hard_fail = 0
    warn = 0

    for path in files:
        rel = os.path.relpath(path, os.path.join(NOTES_DIR, ".."))
        with io.open(path, encoding="utf-8") as f:
            lines = f.readlines()

        in_code = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code or SKIP_LINE_RE.match(line):
                continue

            # #2 hard fail: unverifiable external claim without disclaimer
            for pat in EXTERNAL_CLAIM_PATTERNS:
                if pat.search(line) and not DISCLAIM_RE.search(line) and "[U]" not in line:
                    print(f"FAIL  {rel}:{i}  unverifiable external claim without disclaimer/[U]: {line.strip()[:100]}")
                    hard_fail += 1

            # #1 warn: claim-like line missing a provenance tag
            if CLAIM_LINE_RE.match(line) and not TAG_RE.search(line):
                # multi-line bullets: tag often on a later line of the same bullet;
                # only warn if this line ends a paragraph (blank line or next bullet follows)
                nxt = lines[i] if i < len(lines) else ""
                if nxt.strip() == "" or nxt.strip().startswith("-") or nxt.strip().startswith("#"):
                    print(f"WARN  {rel}:{i}  claim line has no provenance tag nearby: {line.strip()[:100]}")
                    warn += 1

            # #3 warn: hedged number where an exact one likely exists
            if HEDGE_RE.search(line) and re.search(r"\d", line):
                print(f"WARN  {rel}:{i}  hedged/approximate number -- check chapter_stats.json for exact value: {line.strip()[:100]}")
                warn += 1

    print(f"\nhard FAIL: {hard_fail}   WARN: {warn}")
    if hard_fail:
        print("FAIL: unverifiable external claims found without disclaimer.")
        return 1
    print("PASS: no unverifiable external claims found (warnings are informational).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
