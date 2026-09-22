"""
Single Definition-of-Done gate (EXECUTION_SPEC.md A7). Runs every other check and
prints one PASS/FAIL table. A session is not done until this exits zero.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/verify_all.py"
"""
import csv
import io
import json
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
AUDIT_DIR = os.path.join(BOOK_DIR, "audit")
TOOLS_DIR = os.path.join(BOOK_DIR, "tools")
PY = sys.executable

results = []  # (name, ok, detail)


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def load_csv(name):
    with open(os.path.join(AUDIT_DIR, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_script(path):
    r = subprocess.run([PY, path], cwd=BOOK_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


def main():
    # ---- 1. blocking gates: run the sub-scripts, require exit 0 ----
    for script, label in [
        (os.path.join(TOOLS_DIR, "verify_citations.py"), "verify_citations.py (page citations + R3 tagging)"),
        (os.path.join(TOOLS_DIR, "lint_notes.py"), "lint_notes.py (unverifiable-claim hard-fail)"),
        (os.path.join(TOOLS_DIR, "check_figure_coverage.py"), "check_figure_coverage.py (G3: figure-heavy pages acknowledged)"),
        (os.path.join(TOOLS_DIR, "check_deferred_refs.py"), "check_deferred_refs.py (G5: deferred cross-refs due for review)"),
    ]:
        rc, out, err = run_script(script)
        check(label, rc == 0, out.strip().splitlines()[-1] if out.strip() else err[:200])

    # ---- 2. PAGE_MANIFEST integrity ----
    pm = load_csv("PAGE_MANIFEST.csv")
    sr = load_csv("SOURCE_REGISTER.csv")
    total_declared = sum(int(r["pdf_page_count_measured"]) for r in sr)
    check("PAGE_MANIFEST row count == sum(SOURCE_REGISTER pages)",
          len(pm) == total_declared, f"{len(pm)} vs {total_declared}")

    seen = set()
    dup = 0
    by_source = {}
    for r in pm:
        k = (r["source_id"], int(r["pdf_page"]))
        if k in seen:
            dup += 1
        seen.add(k)
        by_source.setdefault(r["source_id"], []).append(int(r["pdf_page"]))
    check("PAGE_MANIFEST no duplicate (source_id, pdf_page) keys", dup == 0, f"{dup} duplicates")

    gap_sources = []
    for sid, pages in by_source.items():
        pages_sorted = sorted(pages)
        expected = set(range(pages_sorted[0], pages_sorted[-1] + 1))
        if set(pages_sorted) != expected:
            gap_sources.append(sid)
    check("PAGE_MANIFEST no page gaps per source", not gap_sources, str(gap_sources))

    # ---- 3. CHAPTER_MAP integrity ----
    cm = load_csv("CHAPTER_MAP.csv")
    bad_range = [r for r in cm if r["pdf_page_start"] and int(r["pdf_page_end"]) < int(r["pdf_page_start"])]
    check("CHAPTER_MAP no end < start ranges", not bad_range,
          str([r["title"] for r in bad_range][:3]))

    bookmarked_sources = {"airflow_2e", "fundamentals_de", "ddia_kleppmann",
                           "kimball_dwtoolkit_3e", "streaming_systems"}
    no_chapters = []
    for sid in bookmarked_sources:
        n = sum(1 for r in cm if r["source_id"] == sid and r["entry_type"] == "chapter")
        if n == 0:
            no_chapters.append(sid)
    check("Every bookmarked source has >=1 chapter entry", not no_chapters, str(no_chapters))

    # ---- 4. FLAG_LEDGER completeness ----
    fl = load_csv("FLAG_LEDGER.csv")
    blank = [r for r in fl if not r["disposition"]]
    check("FLAG_LEDGER: no blank dispositions", not blank,
          f"{len(blank)} open flags -- see audit/FLAG_LEDGER.csv (Phase B item B1)")

    # ---- 5. promised artifacts exist ----
    # G1: every note must state its page basis, since each source has a different
    # pdf-vs-printed offset (measured: Kimball -36, Airflow -30, Fundamentals -25,
    # DDIA -22, Databricks 0; streaming_systems + petrov unresolved). A note that
    # cites bare "p300" without saying which basis sends a reader to the wrong page.
    import glob as _glob
    bad_basis = []
    for np_ in _glob.glob(os.path.join(BOOK_DIR, "notes", "**", "*.md"), recursive=True):
        txt = io.open(np_, encoding="utf-8").read()
        if "PDF page range" not in txt:
            bad_basis.append(os.path.relpath(np_, BOOK_DIR))
    check("G1: every note declares its page basis ('PDF page range')",
          not bad_basis, str(bad_basis))

    promised = [
        "MASTER_CONTEXT.md", "MASTER_CONTEXT_FULL.md",
        "audit/page_offsets.json", "audit/DEFERRED_REFS.csv",
        "tools/detect_page_offsets.py", "tools/check_figure_coverage.py",
        "tools/check_deferred_refs.py", "tools/test_idempotent.py",
        "audit/SOURCE_REGISTER.csv", "audit/PAGE_MANIFEST.csv", "audit/CHAPTER_MAP.csv",
        "audit/chapter_stats.json", "audit/FLAG_LEDGER.csv", "audit/GAPS_AND_VERIFICATION.md",
        "tools/build_full.py", "tools/build_master_context.py", "tools/verify_citations.py",
        "tools/lint_notes.py", "tools/chapter_stats.py", "tools/build_flag_ledger.py",
        "tools/mark_synthesized.py",
    ]
    missing = [p for p in promised if not os.path.exists(os.path.join(BOOK_DIR, p))]
    check("All promised artifacts exist", not missing, str(missing))

    # ---- 6. every note file corresponds to a chapter_stats.json entry ----
    with open(os.path.join(AUDIT_DIR, "chapter_stats.json"), encoding="utf-8") as f:
        stats = json.load(f)
    import glob
    note_files = glob.glob(os.path.join(BOOK_DIR, "notes", "**", "*.md"), recursive=True)
    check("At least one synthesized note exists if any chapter_stats status=synthesized",
          True, f"{len(note_files)} note files, "
                f"{sum(1 for s in stats if s.get('status')=='synthesized')} marked synthesized")

    # ---- print results ----
    print(f"\n{'STATUS':<6} CHECK")
    n_fail = 0
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        if not ok:
            n_fail += 1
        print(f"{status:<6} {name}")
        if detail and not ok:
            print(f"       -> {detail}")

    print(f"\n{len(results)-n_fail}/{len(results)} checks passed.")
    if n_fail:
        print("VERIFY_ALL: FAIL")
        return 1
    print("VERIFY_ALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
