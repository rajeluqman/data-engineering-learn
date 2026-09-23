#!/usr/bin/env python3
"""
Retrofits [[wikilinks]] into the '## 9. Cross-references' section of every note under
notes/<source_id>/*.md, linking same-source chapter mentions ("Ch.3", "Chapter 3", etc.)
to their actual chapter file.

Safety design: this script NEVER rewrites prose. It only wraps an already-matched
chapter-reference token in [[filename|<original token text>]] markup. The visible text
on the page is unchanged; only Obsidian link syntax is added around it. Nothing outside
'## 9. Cross-references' is touched. No page numbers, quotes, or other sections are read
or altered.

Usage:
  python tools/retrofit_cross_ref_wikilinks.py --check          # dry run, report only
  python tools/retrofit_cross_ref_wikilinks.py --file <path>    # apply to one file
  python tools/retrofit_cross_ref_wikilinks.py --apply          # apply to all 90 notes
"""

import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.abspath(os.path.join(HERE, ".."))
NOTES_DIR = os.path.join(BOOK_DIR, "notes")

# Manual filename overrides for chapters whose file doesn't follow chNN_slug.md
# (source_id, chapter_number) -> filename stem (no .md)
OVERRIDES = {
    ("databricks_big_book_4e", 8): "ch_reverse_etl_lakebase",
}

CHAPTER_FILE_RE = re.compile(r"^ch0?(\d+)_", re.IGNORECASE)


def build_chapter_map():
    """source_id -> {chapter_number(int): filename_stem}"""
    mapping = {}
    for source_id in sorted(os.listdir(NOTES_DIR)):
        sdir = os.path.join(NOTES_DIR, source_id)
        if not os.path.isdir(sdir):
            continue
        chmap = {}
        for fn in os.listdir(sdir):
            if not fn.endswith(".md"):
                continue
            stem = fn[:-3]
            m = CHAPTER_FILE_RE.match(stem)
            if m:
                chmap[int(m.group(1))] = stem
        for (src, num), stem in OVERRIDES.items():
            if src == source_id:
                chmap[num] = stem
        mapping[source_id] = chmap
    return mapping


# Matches "Ch.3", "Ch. 3", "Ch3", "Chapter 3" — NOT "p.34" or standalone numbers.
# Word-boundary guarded so it won't match inside an existing [[...]] target segment
# (we additionally skip spans already inside [[ ]] via the has_link_span check below).
CHAPTER_REF_RE = re.compile(
    r"\bCh(?:apter)?\.?\s*(\d{1,2})\b(?!\s*[\]|])",
    re.IGNORECASE,
)


def find_section_span(text, heading="## 9. Cross-references"):
    start = text.find(heading)
    if start == -1:
        return None
    # section ends at the next '## ' heading, or '---' on its own line, or EOF
    rest = text[start + len(heading):]
    end_rel = len(rest)
    for m in re.finditer(r"\n## |\n---\s*\n", rest):
        end_rel = m.start()
        break
    return start, start + len(heading) + end_rel


QUOTED_SPAN_RE = re.compile(r'"[^"]*"')


def existing_link_spans(section_text):
    """Character ranges already inside [[...]] so we don't double-wrap."""
    return [(m.start(), m.end()) for m in re.finditer(r"\[\[.*?\]\]", section_text)]


def quoted_spans(section_text):
    """Character ranges inside "..." verbatim PDF quotes — never link inside these,
    since verify_citations.py matches this exact text against the source PDF."""
    return [(m.start(), m.end()) for m in QUOTED_SPAN_RE.finditer(section_text)]


def in_any_span(pos, spans):
    return any(s <= pos < e for s, e in spans)


def retrofit_section(section_text, chmap):
    """Wrap same-source chapter refs in [[filename|original text]]. Returns (new_text, n_linked, n_skipped)."""
    spans = existing_link_spans(section_text) + quoted_spans(section_text)
    out = []
    last = 0
    n_linked = 0
    n_skipped = 0
    for m in CHAPTER_REF_RE.finditer(section_text):
        if in_any_span(m.start(), spans):
            continue
        num = int(m.group(1))
        target = chmap.get(num)
        out.append(section_text[last:m.start()])
        original = m.group(0)
        if target:
            out.append("[[%s|%s]]" % (target, original))
            n_linked += 1
        else:
            out.append(original)
            n_skipped += 1
        last = m.end()
    out.append(section_text[last:])
    return "".join(out), n_linked, n_skipped


def process_file(path, chmap, apply_changes):
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    span = find_section_span(text)
    if span is None:
        return None  # no §9 section found
    s, e = span
    section = text[s:e]
    new_section, n_linked, n_skipped = retrofit_section(section, chmap)
    changed = new_section != section
    if changed and apply_changes:
        new_text = text[:s] + new_section + text[e:]
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
    return {"changed": changed, "linked": n_linked, "skipped": n_skipped}


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="dry run, report only")
    g.add_argument("--file", help="apply to a single file (relative to notes/ or absolute)")
    g.add_argument("--apply", action="store_true", help="apply to all notes")
    args = ap.parse_args()

    chapter_map = build_chapter_map()

    if args.file:
        path = args.file
        if not os.path.isabs(path):
            path = os.path.join(NOTES_DIR, path) if not path.startswith(NOTES_DIR) else path
        source_id = os.path.basename(os.path.dirname(path))
        result = process_file(path, chapter_map.get(source_id, {}), apply_changes=True)
        print(path, "->", result)
        return

    apply_changes = args.apply
    total_files = 0
    total_changed = 0
    total_linked = 0
    total_skipped = 0
    for source_id in sorted(chapter_map):
        sdir = os.path.join(NOTES_DIR, source_id)
        chmap = chapter_map[source_id]
        for fn in sorted(os.listdir(sdir)):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(sdir, fn)
            result = process_file(path, chmap, apply_changes=apply_changes)
            if result is None:
                continue
            total_files += 1
            if result["changed"]:
                total_changed += 1
                total_linked += result["linked"]
                total_skipped += result["skipped"]
                mode = "APPLIED" if apply_changes else "WOULD CHANGE"
                print("%s  %-70s  linked=%d skipped=%d" % (
                    mode, os.path.join(source_id, fn), result["linked"], result["skipped"]))

    print()
    print("files scanned: %d" % total_files)
    print("files changed: %d" % total_changed)
    print("chapter refs linked: %d" % total_linked)
    print("chapter refs skipped (no matching file): %d" % total_skipped)
    if not apply_changes:
        print("\n(dry run — re-run with --apply to write changes)")


if __name__ == "__main__":
    main()
