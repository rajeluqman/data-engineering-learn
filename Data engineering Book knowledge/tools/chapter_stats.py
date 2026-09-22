"""
Emits audit/chapter_stats.json — one record per in_synthesis_scope chapter in
CHAPTER_MAP.csv, with page_count and word_count MEASURED from the actual pdf pages.

This is the single source of truth for chapter sizes. No note may state a page count
or word count by hand -- it must be read from this file (see EXECUTION_SPEC.md R1).

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/chapter_stats.py"
"""
import csv
import json
import os

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


def band(pages):
    if pages <= 10:
        return "short"
    if pages <= 25:
        return "medium"
    return "long"


def main():
    with open(os.path.join(AUDIT_DIR, "CHAPTER_MAP.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    readers = {}
    records = []
    for r in rows:
        if r["in_synthesis_scope"] != "True":
            continue
        sid = r["source_id"]
        if sid not in readers:
            readers[sid] = PdfReader(os.path.join(BOOK_DIR, FILE_MAP[sid]))
        reader = readers[sid]
        s, e = int(r["pdf_page_start"]), int(r["pdf_page_end"])
        words = 0
        for pn in range(s, e + 1):
            try:
                t = reader.pages[pn - 1].extract_text() or ""
            except Exception:
                t = ""
            words += len(t.split())
        pages = e - s + 1
        records.append({
            "source_id": sid,
            "chapter_title": r["title"],
            "pdf_page_start": s,
            "pdf_page_end": e,
            "page_count": pages,
            "word_count": words,
            "band": band(pages),
            # Read status directly from CHAPTER_MAP.csv rather than tracking it
            # independently -- CHAPTER_MAP.csv is the source of truth (updated by
            # mark_synthesized.py) and duplicating the field here was what let the
            # two files drift apart when build_chapter_map.py was re-run. See
            # GAPS_AND_VERIFICATION.md for the incident.
            "status": r.get("status", "located"),
        })

    out_path = os.path.join(AUDIT_DIR, "chapter_stats.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"wrote {len(records)} chapter records to {out_path}")
    from collections import Counter
    print("bands:", dict(Counter(r["band"] for r in records)))
    print("total pages:", sum(r["page_count"] for r in records))
    print("total words:", sum(r["word_count"] for r in records))


if __name__ == "__main__":
    main()
