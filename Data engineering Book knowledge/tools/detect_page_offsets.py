"""
G1 (part 1): detects each source's printed-page-number offset and fills
PAGE_MANIFEST.csv's `printed_page_label` column.

WHY THIS EXISTS: every attached book numbers its printed pages differently from its
physical PDF page index, and the offset differs PER SOURCE (measured: Kimball -36,
Airflow -30, Fundamentals -25, DDIA -22, Databricks 0). Notes cite page numbers; if
the basis isn't recorded and stated, a reader opening the physical book lands dozens
of pages away from the cited text, and the error is invisible to every other check
in this project.

METHOD: sample pages across the body of the book, pull candidate folio numbers from
the first and last text line of each page, compute (pdf_page - printed_page) for
each, and take the mode. The offset is only accepted if it holds for a clear majority
of sampled pages -- otherwise the source is recorded as `unresolved` rather than
guessed (No-Guess Rule). Front matter (roman numerals) is not resolved by this pass
and is left blank.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/detect_page_offsets.py"
"""
import csv
import io
import json
import os
import re
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from pypdf import PdfReader

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
AUDIT_DIR = os.path.join(BOOK_DIR, "audit")

FILE_MAP = {
    "airflow_2e": "Data Pipelines with Apache Airflow, 2nd Edition.pdf",
    "database_internals_petrov": "Database Internals alex petrov.pdf",
    "fundamentals_de": "Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf",
    "ddia_kleppmann": "Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf",
    "kimball_dwtoolkit_3e": "Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf",
    "streaming_systems": "streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf",
    "databricks_big_book_4e": "Big-Book-of-Data-Engineering-4th-Edition.pdf",
}

# Offset must hold for at least this share of pages where a folio was found,
# otherwise the source is recorded unresolved instead of guessed.
CONFIDENCE_THRESHOLD = 0.60
MIN_SAMPLES = 20


def candidate_offsets(reader, pdf_page):
    """Folio numbers usually sit alone on the first or last text line of a page."""
    try:
        text = reader.pages[pdf_page - 1].extract_text() or ""
    except Exception:
        return []
    lines = [ln.strip() for ln in text.strip().split("\n") if ln.strip()]
    if not lines:
        return []
    out = []
    for line in (lines[0], lines[-1]):
        # a folio line is mostly the number, possibly with a running header/footer
        for m in re.finditer(r"\b(\d{1,4})\b", line):
            printed = int(m.group(1))
            if 0 < printed < pdf_page:  # printed page always <= pdf page here
                out.append(pdf_page - printed)
    return out


def main():
    results = {}
    for sid, fname in FILE_MAP.items():
        reader = PdfReader(os.path.join(BOOK_DIR, fname))
        n = len(reader.pages)
        # sample the body of the book, skipping front matter and back matter
        lo, hi = int(n * 0.25), int(n * 0.85)
        votes = Counter()
        pages_with_folio = 0
        for pdf_page in range(lo, hi, max(1, (hi - lo) // 120)):
            cands = candidate_offsets(reader, pdf_page)
            if cands:
                pages_with_folio += 1
                # a page contributes at most one vote per distinct candidate
                for c in set(cands):
                    votes[c] += 1

        if not votes or pages_with_folio < MIN_SAMPLES:
            results[sid] = {"offset": None, "status": "unresolved",
                            "reason": f"only {pages_with_folio} sampled pages yielded a folio candidate "
                                      f"(need >= {MIN_SAMPLES})"}
            continue

        best, best_count = votes.most_common(1)[0]
        share = best_count / pages_with_folio
        if share >= CONFIDENCE_THRESHOLD:
            results[sid] = {"offset": best, "status": "measured",
                            "confidence": round(share, 2),
                            "sampled_pages_with_folio": pages_with_folio}
        else:
            results[sid] = {"offset": None, "status": "unresolved",
                            "reason": f"best candidate offset {best} held for only "
                                      f"{share:.0%} of {pages_with_folio} sampled pages "
                                      f"(threshold {CONFIDENCE_THRESHOLD:.0%})"}

    # databricks was verified by hand this project: printed == pdf (offset 0),
    # confirmed by opening every TOC-listed start page. Record that explicitly
    # rather than letting a weak heuristic overwrite a hand-verified fact.
    results["databricks_big_book_4e"] = {
        "offset": 0, "status": "measured", "confidence": 1.0,
        "note": "hand-verified: all 16 printed TOC page numbers opened and matched pdf page index",
    }

    out_path = os.path.join(AUDIT_DIR, "page_offsets.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # ---- fill printed_page_label in PAGE_MANIFEST.csv ----
    manifest_path = os.path.join(AUDIT_DIR, "PAGE_MANIFEST.csv")
    with open(manifest_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = rows[0].keys()

    filled = 0
    for r in rows:
        info = results.get(r["source_id"], {})
        off = info.get("offset")
        if off is None:
            r["printed_page_label"] = ""
            continue
        printed = int(r["pdf_page"]) - off
        # pages before the offset kicks in are front matter (roman numerals etc.);
        # leave blank rather than emit a wrong or negative label
        r["printed_page_label"] = str(printed) if printed >= 1 else ""
        if r["printed_page_label"]:
            filled += 1

    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {out_path}")
    for sid, info in sorted(results.items()):
        if info["status"] == "measured":
            print(f"  {sid:<26} offset={info['offset']:<4} (pdf - printed)  confidence={info.get('confidence')}")
        else:
            print(f"  {sid:<26} UNRESOLVED -- {info.get('reason', info.get('note',''))}")
    print(f"printed_page_label filled for {filled} / {len(rows)} manifest rows")


if __name__ == "__main__":
    main()
