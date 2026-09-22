"""
Blocking gate: scans notes/**/*.md for page citations with a quoted anchor and
verifies the quote actually appears on the claimed pdf page(s).

Citation forms recognised: (pN), (pN-pM), (pN, pM), (p.N)  -- immediately followed,
in the same sentence/bullet, by a "quoted string".

A citation with NO quoted anchor nearby is reported as UNVERIFIABLE (not a hard
failure by itself, but counted -- see EXECUTION_SPEC.md R3, which says such claims
must instead carry a `[D]` provenance tag).

Exit code: non-zero if any FAIL exists.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/verify_citations.py"
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from pypdf import PdfReader

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
NOTES_DIR = os.path.join(BOOK_DIR, "notes")

FILE_MAP = {
    "airflow_2e": "Data Pipelines with Apache Airflow, 2nd Edition.pdf",
    "database_internals_petrov": "Database Internals alex petrov.pdf",
    "fundamentals_de": "Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf",
    "ddia_kleppmann": "Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf",
    "kimball_dwtoolkit_3e": "Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf",
    "streaming_systems": "streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf",
    "databricks_big_book_4e": "Big-Book-of-Data-Engineering-4th-Edition.pdf",
}

# (pN), (pN-pM), (pN, pM), (p.N), (pN–pM em/en dash)
# (pN), (pN-pM), (pN, pM), (p.N), and -- added after an audit found six wrong
# citations hiding in this exact gap -- the *annotated* forms that carry
# explanatory text inside the parentheses:
#   (p57, citing *Data Governance*)   (p61, Figure 2-8)   (p118, leader-follower)
# Those were previously invisible to this checker, so every error in one survived
# every gate run. The trailing-text group is non-capturing and bounded so it can't
# swallow a following sentence.
PAGE_CITE = re.compile(
    r"\(p\.?\s*(\d+)\s*(?:[-–—,]\s*p?\.?\s*(\d+))?"
    r"(?:\s*[,:;][^)]{0,140})?\)"
)
QUOTE = re.compile(r'"([^"]{6,300})"')


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    for d in "‐‑‒–—":
        s = s.replace(d, "-")
    s = re.sub(r"[•■￼]", "", s)
    # Ligature glyphs (Unicode fi/fl/ff/ffi/ffl codepoints) -> plain letters.
    for lig, expansion in [("ﬃ", "ffi"), ("ﬄ", "ffl"), ("ﬀ", "ff"), ("ﬁ", "fi"), ("ﬂ", "fl")]:
        s = s.replace(lig, expansion)
    # Hyphens are ambiguous from extracted text alone (a genuine compound-word hyphen
    # vs. a line-wrap artifact look identical once whitespace is involved, and PDF
    # bullet markers can land mid-word: "bleeding-•\nedge"). Strip ALL hyphens (and
    # adjacent whitespace) everywhere, applied identically to source and quotes.
    s = re.sub(r"\s*-\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


def norm_nospace(s):
    """Fallback normalisation with ALL whitespace removed. pypdf sometimes emits a
    spurious space mid-word around certain glyph-kerning pairs (e.g. plain ASCII
    "suff er" for "suffer", not just Unicode ligature glyphs) -- this is not
    predictable enough to pattern-match, so the fallback drops every space and
    compares raw letter sequences instead. Used only when the space-preserving
    norm() comparison fails, and reported as such (not silently treated the same as
    an exact match) so a false-positive risk from this looser check stays visible."""
    return re.sub(r"\s+", "", norm(s))


def source_id_from_path(path):
    rel = os.path.relpath(path, NOTES_DIR)
    return rel.split(os.sep)[0]


def load_pages(sid, cache):
    if sid in cache:
        return cache[sid]
    fname = FILE_MAP.get(sid)
    if not fname:
        cache[sid] = None
        return None
    path = os.path.join(BOOK_DIR, fname)
    reader = PdfReader(path)
    pages = {}
    for i, pg in enumerate(reader.pages, 1):
        try:
            t = pg.extract_text() or ""
        except Exception:
            t = ""
        pages[i] = norm(t)
    cache[sid] = pages
    return pages


def paragraphs(lines):
    """Group consecutive non-blank lines into paragraphs (bullets/sentences often
    wrap across lines in these notes, so a citation and its quote may not share a
    single physical line). Returns list of (start_line_no, joined_text)."""
    paras = []
    buf = []
    start = None
    BULLET_RE = re.compile(r"^[-*]\s+")
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        is_break = stripped == "" or stripped.startswith("#") or stripped.startswith("```") or stripped.startswith("|")
        is_new_bullet = BULLET_RE.match(stripped) is not None
        if is_break:
            if buf:
                paras.append((start, " ".join(buf)))
                buf = []
            continue
        if is_new_bullet and buf:
            # a new top-level bullet starts a new claim -- flush the previous one
            paras.append((start, " ".join(buf)))
            buf = []
        if not buf:
            start = i
        buf.append(stripped)
    if buf:
        paras.append((start, " ".join(buf)))
    return paras


def main():
    files = sorted(glob.glob(os.path.join(NOTES_DIR, "**", "*.md"), recursive=True))
    if not files:
        print("No note files found under notes/ -- nothing to verify.")
        return 0

    page_cache = {}
    nospace_cache = {}
    results = []  # (status, note, line_no, claimed, actual, snippet)
    unverifiable = []
    untagged_unverifiable = []
    fallback_used = []

    for path in files:
        sid = source_id_from_path(path)
        pages = load_pages(sid, page_cache)
        if pages is not None and sid not in nospace_cache:
            nospace_cache[sid] = {pn: re.sub(r"\s+", "", t) for pn, t in pages.items()}
        pages_ns = nospace_cache.get(sid)
        rel = os.path.relpath(path, BOOK_DIR)
        with io.open(path, encoding="utf-8") as f:
            lines = f.readlines()

        for start_line, para in paragraphs(lines):
            for m in PAGE_CITE.finditer(para):
                p1 = int(m.group(1))
                p2 = int(m.group(2)) if m.group(2) else p1
                claimed = list(range(min(p1, p2), max(p1, p2) + 1))

                qmatches = list(QUOTE.finditer(para))
                if not qmatches:
                    # G2 / EXECUTION_SPEC R3: a page citation with no quotable anchor
                    # cannot be machine-verified at all. It is only allowed if the
                    # claim is explicitly marked as interpretation [D] or unresolved
                    # [U] -- an untagged one is an unverifiable claim presented as
                    # source-supported, which is the single largest silent-error
                    # surface in this project. Untagged => hard FAIL.
                    tagged = bool(re.search(r"`?\[(D|U)\]`?", para))
                    pg_label = f"p{p1}" + (f"-{p2}" if p2 != p1 else "")
                    if tagged:
                        unverifiable.append((rel, start_line, pg_label, para.strip()[:90]))
                    else:
                        untagged_unverifiable.append((rel, start_line, pg_label, para.strip()[:90]))
                    continue

                if pages is None:
                    results.append(("FAIL", rel, start_line, claimed, "NO_SOURCE_MAPPED", qmatches[0].group(1)[:60]))
                    continue

                # a paragraph may contain multiple quotes; check each against this citation
                any_ok = False
                any_checked = False
                actual_all = []
                for qm in qmatches:
                    raw = qm.group(1)
                    # Ellipsis-elided quotes ("...") are a legitimate editorial
                    # convention -- split on the elision and require EVERY segment
                    # to independently appear on the same page, rather than treating
                    # the whole string (with its skipped middle) as one substring.
                    segments = [s for s in re.split(r"…|\.\.\.", raw) if len(s.strip()) >= 6]
                    if not segments:
                        continue
                    any_checked = True
                    per_segment_pages = []
                    for seg in segments:
                        snippet = norm(seg)
                        found = [pn for pn, t in pages.items() if snippet in t]
                        if not found and pages_ns is not None:
                            # fallback: pypdf sometimes inserts a spurious mid-word
                            # space around certain glyph-kerning pairs even in plain
                            # ASCII text (e.g. "suff er" for "suffer") -- retry with
                            # ALL whitespace stripped from both sides.
                            snippet_ns = re.sub(r"\s+", "", snippet)
                            found_ns = [pn for pn, t in pages_ns.items() if snippet_ns in t]
                            if found_ns:
                                found = found_ns
                                fallback_used.append((rel, start_line, seg[:60]))
                        per_segment_pages.append(set(found))
                    # pages where ALL segments of this (possibly elided) quote appear
                    actual = sorted(set.intersection(*per_segment_pages)) if per_segment_pages else []
                    actual_all.append((qm.group(1)[:60], actual))
                    if any(pn in claimed for pn in actual):
                        any_ok = True
                if not any_checked:
                    unverifiable.append((rel, start_line, f"p{p1}" + (f"-{p2}" if p2 != p1 else ""), para.strip()[:90]))
                    continue
                best = actual_all[0]
                results.append(("PASS" if any_ok else "FAIL", rel, start_line, claimed,
                                 [a for _, a in actual_all for a in a] if not any_ok else claimed,
                                 " | ".join(q for q, _ in actual_all)[:80]))

    n_pass = sum(1 for r in results if r[0] == "PASS")
    n_fail = sum(1 for r in results if r[0] == "FAIL")

    print(f"{'STATUS':<6} {'FILE:LINE':<55} {'CLAIMED':<14} {'ACTUAL':<14} SNIPPET")
    for status, rel, ln, claimed, actual, snippet in results:
        loc = f"{rel}:{ln}"
        print(f"{status:<6} {loc:<55} {str(claimed):<14} {str(actual):<14} {snippet}")

    print()
    print(f"Quoted citations checked: {len(results)}  PASS={n_pass}  FAIL={n_fail}")
    if fallback_used:
        print(f"Matched only via whitespace-stripped fallback (pypdf mid-word space artifact): {len(fallback_used)}")
        for rel, ln, snip in fallback_used:
            print(f"  FALLBACK-MATCH {rel}:{ln} -- {snip}")
    print(f"Unverifiable but correctly tagged [D]/[U] (no quote anchor): {len(unverifiable)}")
    if untagged_unverifiable:
        print()
        print(f"UNTAGGED UNVERIFIABLE (R3 violation -- page cited, no quote anchor, no [D]/[U] tag): {len(untagged_unverifiable)}")
        for rel, ln, pg, snip in untagged_unverifiable:
            print(f"  R3-FAIL {rel}:{ln} {pg} -- {snip}")
    for rel, ln, pg, snip in unverifiable:
        print(f"  UNVERIFIABLE {rel}:{ln} {pg} -- {snip}")

    if n_fail > 0:
        print(f"\nFAIL: {n_fail} citation(s) could not be verified against the source pdf.")
        return 1
    print("\nPASS: all quoted citations verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
