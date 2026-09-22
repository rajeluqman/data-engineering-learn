"""
Dispositions the 595 reading_order_risk flagged pages in FLAG_LEDGER.csv.

Method (EXECUTION_SPEC.md B1): a stratified random sample of 31 pages (seed=42,
~5 per source, all of kimball_dwtoolkit_3e's 1) was drawn and cross-checked against
a second extractor (pdfplumber) -- the second-extractor step the brief requires and
that had never actually been run before this.

Finding: text length agreement was near-total (length ratio >=0.97 on all 31 sampled
pages). The 15/31 pages where the first-50-char prefix differed were individually
inspected; in every inspected case the divergence was a running-header/page-number
ordering artifact (e.g. pypdf: "17Introducing Airflow...", pdfplumber: "Introducing
Airflow 17...") -- NOT scrambled or lost body text. Body content matched between
extractors in all inspected cases.

Conclusion: the reading_order_risk heuristic (embedded image + >200 extracted chars)
over-triggers on ordinary pages that simply contain a running header plus any inline
image (a chart, a logo, a diagram) -- it does not reliably indicate actual reading-order
corruption. Based on this evidence, the remaining un-sampled pages are dispositioned
`deferred` with this finding as the justification, rather than reviewed individually.

This is a bulk deferral grounded in a specific, reproducible sample -- not a guess.
If synthesis of a specific chapter later needs a `reading_order_risk` page reviewed
in more depth, re-open it individually at that time (this ledger is per-page, so any
row can be flipped later without re-running this whole disposition).

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/disposition_reading_order_risk.py"
"""
import csv
import os

AUDIT_DIR = os.path.join(os.path.dirname(__file__), "..", "audit")
LEDGER = os.path.join(AUDIT_DIR, "FLAG_LEDGER.csv")

SAMPLE_SEED = 42
SAMPLED = {
    ("airflow_2e", 47), ("airflow_2e", 119), ("airflow_2e", 198), ("airflow_2e", 211), ("airflow_2e", 269),
    ("database_internals_petrov", 33), ("database_internals_petrov", 43), ("database_internals_petrov", 200),
    ("database_internals_petrov", 216), ("database_internals_petrov", 219),
    ("databricks_big_book_4e", 40), ("databricks_big_book_4e", 59), ("databricks_big_book_4e", 72),
    ("databricks_big_book_4e", 101), ("databricks_big_book_4e", 109),
    ("ddia_kleppmann", 34), ("ddia_kleppmann", 52), ("ddia_kleppmann", 109), ("ddia_kleppmann", 213),
    ("ddia_kleppmann", 361),
    ("fundamentals_de", 36), ("fundamentals_de", 59), ("fundamentals_de", 214), ("fundamentals_de", 269),
    ("fundamentals_de", 296),
    ("kimball_dwtoolkit_3e", 47),
    ("streaming_systems", 116), ("streaming_systems", 126), ("streaming_systems", 366),
    ("streaming_systems", 389), ("streaming_systems", 393),
}
SAMPLE_EVIDENCE = (
    "Sampled + cross-checked with pdfplumber (2nd extractor). Text length ratio >=0.97 "
    "vs pypdf. Where the first-50-char prefix differed, inspection showed a running-"
    "header/page-number ordering artifact only (e.g. header text before vs after body "
    "start) -- body content itself matched. No reading-order corruption of body text found."
)
DEFERRED_EVIDENCE = (
    "Not individually inspected. Deferred based on the 31-page stratified sample "
    "(seed=42, see SAMPLED pages in this script) which found the reading_order_risk "
    "heuristic over-triggers on running-header + inline-image pages without actual body "
    "text corruption. Re-open individually if a specific page becomes relevant during "
    "chapter synthesis."
)


def main():
    with open(LEDGER, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    n_sampled = n_deferred = 0
    for r in rows:
        if r["flag_type"] != "reading_order_risk":
            continue
        key = (r["source_id"], int(r["pdf_page"]))
        if key in SAMPLED:
            r["disposition"] = "reviewed-ok"
            r["evidence"] = SAMPLE_EVIDENCE
            r["decided_on"] = f"this-session-sample-seed{SAMPLE_SEED}"
            n_sampled += 1
        else:
            r["disposition"] = "deferred"
            r["evidence"] = DEFERRED_EVIDENCE
            r["decided_on"] = f"this-session-bulk-defer-based-on-sample-seed{SAMPLE_SEED}"
            n_deferred += 1

    with open(LEDGER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"reading_order_risk: {n_sampled} reviewed-ok (sampled), {n_deferred} deferred (bulk, justified)")


if __name__ == "__main__":
    main()
