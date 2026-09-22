"""
G3: figure-coverage check.

WHY THIS EXISTS: a note can pass every citation check and still silently miss the
chapter's actual argument, because in this corpus a lot of the argument lives in
diagrams that the text layer does not carry. Proven, not hypothetical:
  - Kimball Fig 9-4 (the HR bus matrix) extracts as a scrambled list of "X" marks
    with the row/column grid lost.
  - 7 pages in streaming_systems are figure-caption-only (FLAG_LEDGER `reviewed-issue`).
Citation verification cannot detect ABSENCE. This check can.

WHAT IT DOES: for every chapter marked `synthesized`, find pages inside its page
range that are figure-heavy (a page whose extracted text is short relative to the
chapter's own average AND that carries an embedded image, plus any page the
FLAG_LEDGER already marked `reviewed-issue`). Require the note to acknowledge them:
either the page number appears in the note, or the note's Exclusions table mentions
a figure/diagram. Otherwise FAIL -- the note may be silently under-covering.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/check_figure_coverage.py"
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

# A page is "figure-heavy" if it has an embedded image and its text is under this
# fraction of the chapter's mean chars/page.
SHORT_PAGE_RATIO = 0.45
FIGURE_WORDS = re.compile(r"figure|diagram|chart|schema diagram|bus matrix", re.I)


def load_manifest():
    with open(os.path.join(AUDIT_DIR, "PAGE_MANIFEST.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by = {}
    for r in rows:
        by.setdefault(r["source_id"], {})[int(r["pdf_page"])] = r
    return by


def load_flagged_issue_pages():
    path = os.path.join(AUDIT_DIR, "FLAG_LEDGER.csv")
    out = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("disposition") == "reviewed-issue":
                    out.add((r["source_id"], int(r["pdf_page"])))
    return out


FILE_MAP = {
    "airflow_2e": "Data Pipelines with Apache Airflow, 2nd Edition.pdf",
    "database_internals_petrov": "Database Internals alex petrov.pdf",
    "fundamentals_de": "Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf",
    "ddia_kleppmann": "Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf",
    "kimball_dwtoolkit_3e": "Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf",
    "streaming_systems": "streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf",
    "databricks_big_book_4e": "Big-Book-of-Data-Engineering-4th-Edition.pdf",
}
CAPTION_RE = re.compile(r"Figure\s+\d+[-–]\d+")


def caption_pages_for(sid, lo, hi, cache):
    """Pages in [lo,hi] whose text contains a 'Figure N-M' caption.

    This is the signal that survives when get_images() sees nothing (vector
    diagrams, as in the whole Kimball source) and when a figure is inline on a
    page otherwise full of body text. Only the chapter's own page range is read,
    so this stays cheap."""
    key = (sid, lo, hi)
    if key in cache:
        return cache[key]
    from pypdf import PdfReader
    out = set()
    fname = FILE_MAP.get(sid)
    if fname:
        reader = PdfReader(os.path.join(BOOK_DIR, fname))
        for pn in range(lo, min(hi, len(reader.pages)) + 1):
            try:
                t = reader.pages[pn - 1].extract_text() or ""
            except Exception:
                t = ""
            if CAPTION_RE.search(t):
                out.add(pn)
    cache[key] = out
    return out


def notes_by_source():
    out = {}
    for p in glob.glob(os.path.join(NOTES_DIR, "**", "*.md"), recursive=True):
        sid = os.path.relpath(p, NOTES_DIR).split(os.sep)[0]
        out.setdefault(sid, []).append(p)
    return out


def main():
    with open(os.path.join(AUDIT_DIR, "chapter_stats.json"), encoding="utf-8") as f:
        stats = json.load(f)
    manifest = load_manifest()
    issue_pages = load_flagged_issue_pages()
    notes = notes_by_source()

    problems = []
    checked = 0
    caption_cache = {}

    for ch in stats:
        if ch.get("status") != "synthesized":
            continue
        checked += 1
        sid = ch["source_id"]
        s, e = ch["pdf_page_start"], ch["pdf_page_end"]
        pages = manifest.get(sid, {})
        span = [pages[p] for p in range(s, e + 1) if p in pages]
        if not span:
            continue
        counts = [int(r["text_char_count"]) for r in span]
        mean = sum(counts) / max(len(counts), 1)
        cap_pages = caption_pages_for(sid, s, e, caption_cache)

        figure_pages = []
        for r in span:
            pn = int(r["pdf_page"])
            short_and_image = (
                r["image_present"] == "True"
                and int(r["text_char_count"]) < mean * SHORT_PAGE_RATIO
            )
            # AUDIT FIX: the short-page+image rule alone detected ZERO pages across
            # all 7 chapters synthesized so far -- including a 44-page chapter with
            # 18 figures, and the Kimball chapter whose bus matrix is KNOWN to
            # extract as scrambled text. Two blind spots caused it:
            #   (a) `image_present` is False for the ENTIRE kimball_dwtoolkit_3e
            #       source (1 image flag in 601 pages) because its diagrams are
            #       vector/text-box drawings that pypdf's get_images() cannot see;
            #   (b) in-line figures sit on pages full of body text, so the page
            #       never drops below the short-page threshold.
            # So the check passed 7/7 while verifying nothing. A figure caption in
            # the page text is the signal that actually survives both cases.
            has_figure_caption = pn in cap_pages
            if short_and_image or has_figure_caption or (sid, pn) in issue_pages:
                figure_pages.append(pn)
        if not figure_pages:
            continue

        # find the note covering this chapter (match on its declared page range)
        note_text = None
        note_path = None
        for p in notes.get(sid, []):
            txt = io.open(p, encoding="utf-8").read()
            if re.search(rf"\b{s}\s*[–-]\s*{e}\b", txt):
                note_text, note_path = txt, p
                break
        if note_text is None:
            problems.append((sid, ch["chapter_title"][:40], figure_pages,
                             "no note found declaring this page range"))
            continue

        acknowledged = FIGURE_WORDS.search(note_text) is not None
        mentioned = [pn for pn in figure_pages if re.search(rf"\bp{pn}\b", note_text)]
        if not acknowledged and not mentioned:
            problems.append((sid, ch["chapter_title"][:40], figure_pages,
                             f"{os.path.basename(note_path)} never mentions a figure/diagram "
                             f"nor any of these pages"))

    print(f"Chapters checked (synthesized only): {checked}")
    if problems:
        print(f"\nFIGURE-COVERAGE PROBLEMS: {len(problems)}")
        for sid, title, pgs, why in problems:
            print(f"  FAIL {sid} | {title} | figure-heavy pages {pgs[:8]}{'...' if len(pgs) > 8 else ''}")
            print(f"       -> {why}")
        return 1
    print("PASS: every synthesized chapter with figure-heavy pages acknowledges them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
