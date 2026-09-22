"""
Dispositions the 20 low_text flagged pages in FLAG_LEDGER.csv, based on direct
inspection of each page's actual extracted text this session (see
audit/_lowtext_check.txt for the raw check). All 20 were reviewed individually
(small enough to check every one, unlike the 595 reading_order_risk pages).

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/disposition_low_text.py"
"""
import csv
import os

AUDIT_DIR = os.path.join(os.path.dirname(__file__), "..", "audit")
LEDGER = os.path.join(AUDIT_DIR, "FLAG_LEDGER.csv")

# (source_id, pdf_page): (disposition, evidence)
DECISIONS = {
    ("database_internals_petrov", 1): ("reviewed-ok", "Cover/title page: 'Database Internals PDF Alex Petrov' -- title only, no body text expected."),
    ("database_internals_petrov", 108): ("reviewed-ok", "End-of-page sentence fragment continuing from prior page; low count is a page-break artifact, not missing content."),
    ("fundamentals_de", 26): ("reviewed-ok", "PART divider page: 'PART I Foundation and Building Blocks' -- structural, no body content expected."),
    ("fundamentals_de", 178): ("reviewed-ok", "PART divider page: 'PART II The Data Engineering Lifecycle in Depth'."),
    ("fundamentals_de", 392): ("reviewed-ok", "PART divider page: 'PART III Security, Privacy, and the Future of Data Engineering'."),
    ("ddia_kleppmann", 5): ("reviewed-ok", "Half-title page: 'Martin Kleppmann Boston Designing Data-Intensive Applications' -- title only."),
    ("kimball_dwtoolkit_3e", 3): ("reviewed-ok", "Half-title page: 'The Data Warehouse Toolkit' -- title only."),
    ("streaming_systems", 21): ("reviewed-ok", "PART divider page: 'Part I. The Beam Model'."),
    ("streaming_systems", 89): ("reviewed-issue", "Figure-only page (Figure 3-2, windowed summation diagram) -- only the caption text is extractable; the diagram's visual content itself is not represented as text. Per task brief section 6: explain diagram meaning with reference to original page rather than treating caption as full coverage. NOT yet explained in a synthesis note -- deferred to when streaming_systems Ch.3 is synthesized."),
    ("streaming_systems", 114): ("reviewed-issue", "Figure-only page (Figure 3-17, key-range assignment diagram) -- same figure-caption-only situation as p89."),
    ("streaming_systems", 173): ("reviewed-ok", "PART divider page: 'Part II. Streams and Tables'."),
    ("streaming_systems", 181): ("reviewed-issue", "Figure-only page (Figure 6-1, MapReduce phases diagram) -- caption-only extraction, diagram content not captured as text."),
    ("streaming_systems", 267): ("reviewed-issue", "Figure-only page (Figure 8-1, stream bias diagram) -- caption-only."),
    ("streaming_systems", 274): ("reviewed-issue", "Figure-only page (Figure 8-3, query-splitting diagram) -- caption-only."),
    ("streaming_systems", 276): ("reviewed-issue", "Figure-only page (Figure 8-4, table bias diagram) -- caption-only."),
    ("streaming_systems", 280): ("reviewed-issue", "Figure-only page (Figure 8-5, materialized views diagram) -- caption-only."),
    ("databricks_big_book_4e", 3): ("reviewed-ok", "Section-opener page: '01 Introduction to Data Engineering on Databricks' -- title only."),
    ("databricks_big_book_4e", 7): ("reviewed-ok", "Page-number-only page ('7 BIG BOOK OF DATA ENGINEERING' running header/footer) -- confirmed genuinely near-blank."),
    ("databricks_big_book_4e", 16): ("reviewed-ok", "Section-opener page: '02 Guidance and Best Practices' -- title only."),
    ("databricks_big_book_4e", 105): ("reviewed-ok", "Section-opener page: '03 Case Studies' -- title only."),
}


def main():
    with open(LEDGER, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    n = 0
    for r in rows:
        key = (r["source_id"], int(r["pdf_page"]))
        if r["flag_type"] == "low_text" and key in DECISIONS:
            disp, ev = DECISIONS[key]
            r["disposition"] = disp
            r["evidence"] = ev
            r["decided_on"] = "this-session-individual-review"
            n += 1

    with open(LEDGER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"dispositioned {n} low_text rows")
    issues = [k for k, v in DECISIONS.items() if v[0] == "reviewed-issue"]
    print(f"reviewed-issue (figure-caption-only, real gap for future synthesis): {len(issues)}")


if __name__ == "__main__":
    main()
