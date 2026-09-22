"""
Builds audit/SOURCE_REGISTER.csv — identity record for each attached PDF.
Run with the D-drive venv: .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/build_source_register.py"

Every field here is either measured in this session (hash, page count) or a finding
with an explicit evidence page. Nothing here is carried over from filenames or memory.
"""
import csv
import hashlib
import glob
import os

from pypdf import PdfReader

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
AUDIT_DIR = os.path.join(BOOK_DIR, "audit")

SOURCE_ID_MAP = {
    "Data Pipelines with Apache Airflow, 2nd Edition.pdf": "airflow_2e",
    "Database Internals alex petrov.pdf": "database_internals_petrov",
    "Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf": "fundamentals_de",
    "Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf": "ddia_kleppmann",
    "Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf": "kimball_dwtoolkit_3e",
    "streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf": "streaming_systems",
    "Big-Book-of-Data-Engineering-4th-Edition.pdf": "databricks_big_book_4e",
}

FINDINGS = {
    "Database Internals alex petrov.pdf": {
        "source_id": "database_internals_petrov",
        "claimed_title": "Database Internals",
        "claimed_author": "Alex Petrov",
        "source_type": "secondary_summary",
        "verified_title": "Bookey summary of Database Internals (Alex Petrov)",
        "evidence": (
            "p3 'About the book', p4 'About the author', p6 'Summary Content List', "
            "p8 'Chapter 1 Summary : I. Storage Engines / Section Summary', "
            "p15 'Chapter 2 Summary ... Section Content' -- body text itself calls every "
            "chapter a 'Summary'. 29/238 pages (p5,22,35,46,59,74,90,94,99,104,109,114,119,"
            "124,127,140,154,168,183,197,211,218,221,224,227,230,233,236,238) are full-page "
            "Bookey app advertisements -- OCR + visual review (p35) confirms 'Scan to Download', "
            "'Try Bookey App', 'App Store Editors Choice', 'Free Trial with Bookey'."
        ),
        "note": "NOT the original Alex Petrov book. Excluded from coverage of the original text; "
                "tracked only as a secondary summary product.",
    },
    "Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf": {
        "source_id": "ddia_kleppmann",
        "claimed_title": "Designing Data-Intensive Applications",
        "claimed_author": "Martin Kleppmann",
        "source_type": "early_release",
        "verified_title": "Designing Data-Intensive Applications -- early-release edition (ends at Chapter 11)",
        "evidence": (
            "Printed Table of Contents (pdf p7-12) lists chapters 1-11 only; p12 ends with "
            "'Fault tolerance / Summary / x | Table of Contents' after ch.11, no Chapter 12 "
            "entry anywhere in the TOC. Body: 'CHAPTER 11 Stream Processing' begins pdf p447 "
            "and the References section (numbered [22]-[79], latest dated cites June/July 2016) "
            "starts pdf p487 and runs to the final page (491). No Chapter 12 heading found "
            "anywhere in the file. Filename says '(2017)' but content structure (TOC + latest "
            "citation dates) is consistent with the 2016 early-release, not the finished 2017 "
            "first edition which adds Chapter 12 'The Future of Data Systems'."
        ),
        "note": "Do not add Chapter 12 content to this file's chapter map -- it is not present. "
                "If Chapter 12 material is needed, it must come from a separately registered source.",
    },
    "Big-Book-of-Data-Engineering-4th-Edition.pdf": {
        "source_id": "databricks_big_book_4e",
        "claimed_title": "Big Book of Data Engineering, 4th Edition",
        "claimed_author": "Databricks",
        "source_type": "vendor_compilation",
        "verified_title": "Big Book of Data Engineering, 4th Edition (Databricks)",
        "evidence": (
            "TOC (pdf p2) reads 'Optimizing Materialized Views Recomputes' (page 74 in the doc). "
            "Chapter heading itself (pdf p74) confirms the same wording: 'Optimizing Materialized "
            "Views Recomputes / By Andrea Tardif and Justin Edrington'. A prior catalog "
            "(DATA_ENGINEERING_MASTER_LIBRARY_SOURCE_OF_TRUTH.md) recorded this as "
            "'Optimizing Materialized Views Recomputation' -- that is a transcription error, "
            "corrected here against the source file."
        ),
        "note": "123 pages -- vendor compilation of guidance chapters + case studies, not a book "
                "in the traditional sense. Already labeled correctly as 'vendor compilation' in "
                "the prior catalog's own register (section 5), just not in the chapter title.",
    },
    "Data Pipelines with Apache Airflow, 2nd Edition.pdf": {
        "source_id": "airflow_2e",
        "claimed_title": "Data Pipelines with Apache Airflow, Second Edition",
        "claimed_author": "Julian de Ruiter, Ismael Cabral, Kris Geusebroek, Daniel van der Ende, Bas Harenslak",
        "source_type": "original_book_confirmed",
        "verified_title": "Data Pipelines with Apache Airflow, Second Edition (Manning)",
        "evidence": (
            "p1 'MANNING SECOND EDITION ... Julian de Ruiter, Ismael Cabral, Kris Geusebroek, "
            "Daniel van der Ende, Bas Harenslak' matches filename and author claim exactly. "
            "p6 Manning ordering/copyright boilerplate. p7-8 'brief contents' lists Parts 1-4 "
            "through 'appendix B' ending at printed page ~482, matching the prior catalog's "
            "17-chapter + 2-appendix structure. Back matter p512-514 is a genuine alphabetical "
            "index (not truncated). p2-3 contain a sponsor ad (Astro) and MEAP-style praise "
            "quotes ahead of the title page -- normal Manning front-matter, not a sign of "
            "an incomplete or different edition."
        ),
        "note": "Confirmed complete and matches filename claim. 514 pages measured.",
    },
    "Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf": {
        "source_id": "fundamentals_de",
        "claimed_title": "Fundamentals of Data Engineering",
        "claimed_author": "Joe Reis and Matt Housley",
        "source_type": "original_book_confirmed",
        "verified_title": "Fundamentals of Data Engineering (O'Reilly, 2022)",
        "evidence": (
            "p7 copyright page: 'ISBN 978-1-098-10830-4 ... Fundamentals of Data Engineering "
            "by Joe Reis and Matt Housley Copyright (c) 2022 Joseph Reis and Matthew Housley. "
            "... Published by O'Reilly Media, Inc.' -- exact match to filename and claimed "
            "authors. p8-10 full Table of Contents matches the prior catalog's chapter list. "
            "p444 'About the Authors' + p445 O'Reilly back-cover boilerplate confirm a genuine, "
            "complete ending -- not truncated."
        ),
        "note": "Confirmed complete and matches filename claim. 445 pages measured.",
    },
    "Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf": {
        "source_id": "kimball_dwtoolkit_3e",
        "claimed_title": "The Data Warehouse Toolkit, 3rd Edition",
        "claimed_author": "Ralph Kimball and Margy Ross",
        "source_type": "original_book_confirmed",
        "verified_title": "The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling, Third Edition (Wiley, 2013)",
        "evidence": (
            "p6 copyright page: 'The Data Warehouse Toolkit: The Definitive Guide to "
            "Dimensional Modeling, Third Edition ... Published by John Wiley & Sons, Inc. "
            "... Copyright (c) 2013 by Ralph Kimball and Margy Ross' -- exact match. p11 full "
            "Contents starting 'Introduction ... 1 Data Warehousing, Business Intelligence, "
            "and Dimensional Modeling Primer' matches the prior catalog's 21-chapter list. "
            "p599-601 end in a genuine alphabetical Index and Kimball Group back-cover "
            "boilerplate -- not truncated."
        ),
        "note": "Confirmed complete and matches filename claim. 601 pages measured.",
    },
    "streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf": {
        "source_id": "streaming_systems",
        "claimed_title": "Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing",
        "claimed_author": "Tyler Akidau, Slava Chernyak, and Reuven Lax",
        "source_type": "original_book_confirmed",
        "verified_title": "Streaming Systems (O'Reilly, 2018, first edition)",
        "evidence": (
            "p3 copyright page: 'Streaming Systems by Tyler Akidau, Slava Chernyak, and "
            "Reuven Lax. Copyright (c) 2018 Tyler Akidau, Slava Chernyak, and Reuven Lax. "
            "All rights reserved.' p4: ISBN 9781491983874 printed in the file. "
            "(NOT cross-checked against O'Reilly's public catalog -- no external lookup was "
            "performed; the ISBN is recorded as present in the file, not as externally verified.)  p455 'About the Authors' + p456 'Colophon' (brown "
            "trout cover animal) confirm a genuine, complete O'Reilly back matter -- not "
            "truncated."
        ),
        "note": "Confirmed complete and matches filename claim. 456 pages measured.",
    },
}

rows = []
for path in sorted(glob.glob(os.path.join(BOOK_DIR, "*.pdf"))):
    fname = os.path.basename(path)
    data = open(path, "rb").read()
    sha256 = hashlib.sha256(data).hexdigest()
    reader = PdfReader(path)
    n = len(reader.pages)
    meta = reader.metadata or {}
    finding = FINDINGS.get(fname, {})
    rows.append({
        "source_id": SOURCE_ID_MAP.get(fname, os.path.splitext(fname)[0].replace(" ", "_")),
        "exact_filename": fname,
        "sha256": sha256,
        "pdf_page_count_measured": n,
        "pdf_metadata_title": (meta.get("/Title") or ""),
        "pdf_metadata_author": (meta.get("/Author") or ""),
        "source_type": finding.get("source_type", "original_book_unverified"),
        "verified_title_or_status": finding.get("verified_title", "unverified: cover/copyright/title-page not yet read in full; page count and hash measured only"),
        "evidence_page_refs": finding.get("evidence", "NOT YET AUDITED beyond hash/page-count -- cover, copyright page, and TOC still need to be opened and compared to filename claim"),
        "note": finding.get("note", "identity audit pending for this file"),
    })

out_path = os.path.join(AUDIT_DIR, "SOURCE_REGISTER.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[
        "source_id", "exact_filename", "sha256", "pdf_page_count_measured",
        "pdf_metadata_title", "pdf_metadata_author", "source_type",
        "verified_title_or_status", "evidence_page_refs", "note",
    ])
    w.writeheader()
    w.writerows(rows)

print(f"wrote {len(rows)} rows to {out_path}")
for r in rows:
    print(f"  {r['source_id']}: {r['source_type']} -- {r['pdf_page_count_measured']} pages -- sha256[:16]={r['sha256'][:16]}")
