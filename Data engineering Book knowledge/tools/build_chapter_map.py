"""
Builds the per-source chapter/section map required by step 5 of the task brief:
  title | pdf_page_range | printed_page_range | entry_type | status | notes

CORRECTED 2nd revision. The first revision had a structural defect: it took every
level-1 bookmark as a "chapter". That is only true for 3 of the 5 bookmarked sources.
In `airflow_2e` and `fundamentals_de` the level-1 entries are front matter and PART
containers, and the actual chapters sit at level 2 — so those two sources previously
had ZERO chapters in the map, while 150-200 page "Parts" were counted as single
chapters and Cover/Index/Colophon were counted as synthesis work.

This version therefore:
  1. Declares, per source, which outline level actually holds chapters (verified by
     inspecting each outline, not assumed).
  2. Emits an `entry_type` column: front_matter | part | chapter | appendix | back_matter.
     Front/back matter is still recorded (page accounting must stay complete) but is
     explicitly marked out of synthesis scope.
  3. Fixes the end-page bug where two bookmarks pointing at the same page produced an
     end page lower than the start page (e.g. fundamentals_de "About the Authors"
     p444-443).

Sources without bookmarks (database_internals_petrov, databricks_big_book_4e) are built
from the printed contents page read directly from the file.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/build_chapter_map.py"
"""
import csv
import json
import os
import re

import pymupdf as fitz

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
AUDIT_DIR = os.path.join(BOOK_DIR, "audit")
MAP_DIR = os.path.join(AUDIT_DIR, "chapter_maps")
os.makedirs(MAP_DIR, exist_ok=True)

# (filename, outline level that actually holds chapters) -- verified per source by
# counting chapter-looking titles at each level; see GAPS_AND_VERIFICATION.md 3b.
BOOKMARK_SOURCES = {
    "airflow_2e": ("Data Pipelines with Apache Airflow, 2nd Edition.pdf", 2),
    "fundamentals_de": ("Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf", 2),
    "ddia_kleppmann": ("Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf", 1),
    "kimball_dwtoolkit_3e": ("Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf", 1),
    "streaming_systems": ("streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf", 1),
}

CHAPTER_PAT = re.compile(r"^\s*(chapter\s+\d+|\d+\s*[.\s]\s*\S|\d+\.)", re.I)
APPENDIX_PAT = re.compile(r"^\s*appendix\s+[A-Za-z]", re.I)
PART_PAT = re.compile(r"^\s*(part\s+[IVX\d]+|[IVX]+\.\s)", re.I)
FRONT_BACK = (
    "cover", "copyright", "title page", "contents", "brief contents", "preface",
    "foreword", "acknowledg", "about this book", "about the author", "about the cover",
    "index", "colophon", "advertisement", "table of contents", "dedication",
)


def classify(title):
    t = title.strip().lower()
    if any(k in t for k in FRONT_BACK):
        return "back_matter" if ("index" in t or "colophon" in t or "advertisement" in t
                                 or "about the author" in t) else "front_matter"
    if APPENDIX_PAT.match(title.strip()):
        return "appendix"
    if PART_PAT.match(title.strip()):
        return "part"
    if CHAPTER_PAT.match(title.strip()):
        return "chapter"
    return "other"


def load_prior_status():
    """Preserve 'synthesized' status across rebuilds, keyed by (source_id, title).
    Without this, re-running this script (e.g. after fixing a mapping bug) silently
    resets every chapter back to 'located', discarding synthesis progress recorded
    by mark_synthesized.py -- this happened once in this project; see
    GAPS_AND_VERIFICATION.md for the incident."""
    prior = {}
    out_path = os.path.join(AUDIT_DIR, "CHAPTER_MAP.csv")
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("status") == "synthesized":
                    prior[(r["source_id"], r["title"])] = "synthesized"
    return prior


PRIOR_STATUS = load_prior_status()

rows = []

for sid, (fname, chapter_level) in BOOKMARK_SOURCES.items():
    path = os.path.join(BOOK_DIR, fname)
    doc = fitz.open(path)
    toc = doc.get_toc(simple=True)
    n = len(doc)
    doc.close()

    with open(os.path.join(MAP_DIR, f"{sid}_full_outline.json"), "w", encoding="utf-8") as f:
        json.dump([{"level": lvl, "title": t, "pdf_page": pg} for lvl, t, pg in toc],
                  f, indent=2, ensure_ascii=False)

    # Keep every level-1 entry (front/back matter, parts, appendices) plus every
    # level==chapter_level entry that actually LOOKS like a chapter heading.
    #
    # Bug fixed here (see GAPS_AND_VERIFICATION.md): for fundamentals_de, an
    # appendix's own subsections ("Serialization Formats", "Compression: gzip...")
    # sit at the SAME bookmark level as "Chapter N" entries (both level 2), because
    # the appendix itself is level 1 with its subsections one level down. Including
    # every level==chapter_level entry unconditionally made those subsections compete
    # as siblings of the appendix in the sorted "kept" list, truncating the appendix's
    # own page range to just its first page. Filtering level==chapter_level entries
    # to only those matching CHAPTER_PAT excludes non-chapter subsections while still
    # keeping every level-1 entry (so the appendix's own line is never dropped, and
    # its true end page is now the next level-1 entry, not an internal subsection).
    kept = [(lvl, t.strip(), pg) for lvl, t, pg in toc
            if lvl == 1 or (lvl == chapter_level and CHAPTER_PAT.match(t.strip()))]
    kept.sort(key=lambda x: x[2])

    for i, (lvl, title, pg_start) in enumerate(kept):
        etype = classify(title)
        # A PART container's pages are covered by its own chapters; don't double-count.
        # End page = next entry's start - 1, but never below start (fixes the p444-443 bug).
        nxt = kept[i + 1][2] if i + 1 < len(kept) else n + 1
        pg_end = max(nxt - 1, pg_start)
        rows.append({
            "source_id": sid,
            "title": title,
            "entry_type": etype,
            "pdf_page_start": pg_start,
            "pdf_page_end": pg_end,
            "printed_page_range": "",
            "in_synthesis_scope": etype in ("chapter", "appendix"),
            "status": PRIOR_STATUS.get((sid, title), "located"),
            "notes": "",
        })

# ---- database_internals_petrov: printed "Summary Content List" (pdf p6), no bookmarks ----
petrov_entries = [
    "I. Storage Engines", "1. Introduction and Overview", "2. B-Tree Basics",
    "3. File Formats", "4. Implementing B-Trees",
    "5. Transaction Processing and Recovery", "6. B-Tree Variants",
    "7. Log-Structured Storage", "Part I Conclusion", "II. Distributed Systems",
    "8. Introduction and Overview", "9. Failure Detection", "10. Leader Election",
    "11. Replication and Consistency", "12. Anti-Entropy and Dissemination",
]
for title in petrov_entries:
    rows.append({
        "source_id": "database_internals_petrov",
        "title": f"[Bookey chapter-summary] {title}",
        "entry_type": "chapter",
        "pdf_page_start": "",
        "pdf_page_end": "",
        "printed_page_range": "",
        "in_synthesis_scope": False,
        "status": "unresolved",
        "notes": "Bookey summary chapter, NOT the original Petrov book chapter. The numbers "
                 "1-15 in the source's 'Summary Content List' are Bookey's internal index, "
                 "not pdf pages; exact page boundaries not determined. Excluded from "
                 "synthesis scope -- see GAPS_AND_VERIFICATION.md section 2.1.",
    })

# ---- databricks_big_book_4e: printed TOC (pdf p2), no bookmarks ----
# Printed page numbers verified this session to equal physical pdf pages (offset 0) by
# opening every listed start page.
databricks_entries = [
    ("Introduction to Data Engineering on Databricks", 10),
    ("Migrating Apache Spark ETL Workloads to Databricks", 17),
    ("How Observability in Lakeflow Helps You Build Reliable Data Pipelines", 22),
    ("A Cost Maturity Journey With Databricks", 27),
    ("Lakeflow Connect: Efficient and Easy Data Ingestion Using the Microsoft SQL Server Connector", 46),
    ("Implement CDC Data Load and SCD Type 2 With Lakeflow", 62),
    ("Optimizing Materialized Views Recomputes", 74),
    ("Reverse ETL With Lakebase: Activate Your Lakehouse Data for Operational Analytics", 82),
    ("Production-Grade Data Quality Using Spark Declarative Pipelines", 86),
    ("Collaborative Data Engineering Made Simple With Databricks Asset Bundles", 94),
    ("A Practical Guide to Serverless Migrations", 99),
    ("iFood: Transforming Data to Elevate Food Deliveries and Experiences", 106),
    ("NFCU: Using Real-Time Data to Trailblaze Member Personalization", 110),
    ("Cincinnati Reds: Winning On and Off the Field With Cutting-Edge Baseball Analytics", 114),
    ("Porsche Holding: Unifying Customer Data to Drive a New Automotive Experience", 117),
    ("Hinge Health: Developing Personalized Care Plans to Improve Patient Outcomes", 120),
]
# pdf p1-9 (cover + contents + section dividers) are not covered by the printed TOC.
rows.append({
    "source_id": "databricks_big_book_4e", "title": "Cover, Contents and section dividers",
    "entry_type": "front_matter", "pdf_page_start": 1, "pdf_page_end": 9,
    "printed_page_range": "1-9", "in_synthesis_scope": False, "status": "located",
    "notes": "Not listed in the printed TOC; recorded so all 123 pages are attributable.",
})
for idx, (title, pg_start) in enumerate(databricks_entries):
    pg_end = (databricks_entries[idx + 1][1] - 1) if idx + 1 < len(databricks_entries) else 123
    rows.append({
        "source_id": "databricks_big_book_4e", "title": title, "entry_type": "chapter",
        "pdf_page_start": pg_start, "pdf_page_end": pg_end,
        "printed_page_range": f"{pg_start}-{pg_end}", "in_synthesis_scope": True,
        "status": PRIOR_STATUS.get(("databricks_big_book_4e", title), "located"),
        "notes": "printed page == physical pdf page (offset 0), verified by opening this start page" if idx == 0 else "",
    })

out_path = os.path.join(AUDIT_DIR, "CHAPTER_MAP.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[
        "source_id", "title", "entry_type", "pdf_page_start", "pdf_page_end",
        "printed_page_range", "in_synthesis_scope", "status", "notes",
    ])
    w.writeheader()
    w.writerows(rows)

# ---- integrity assertions: fail loudly rather than emit a quietly broken map ----
bad = [r for r in rows if r["pdf_page_start"] != "" and int(r["pdf_page_end"]) < int(r["pdf_page_start"])]
assert not bad, f"end page < start page in {len(bad)} rows: {bad[:3]}"
for sid in BOOKMARK_SOURCES:
    chaps = [r for r in rows if r["source_id"] == sid and r["entry_type"] == "chapter"]
    assert chaps, f"{sid}: chapter map contains ZERO chapters -- wrong outline level?"

print(f"wrote {len(rows)} rows to {out_path}")
from collections import Counter
for sid in list(BOOKMARK_SOURCES) + ["databricks_big_book_4e", "database_internals_petrov"]:
    c = Counter(r["entry_type"] for r in rows if r["source_id"] == sid)
    ins = sum(1 for r in rows if r["source_id"] == sid and r["in_synthesis_scope"])
    print(f"  {sid:<26} {dict(c)}  in_synthesis_scope={ins}")
print(f"TOTAL in synthesis scope: {sum(1 for r in rows if r['in_synthesis_scope'])}")
