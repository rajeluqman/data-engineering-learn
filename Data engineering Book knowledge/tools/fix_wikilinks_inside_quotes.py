#!/usr/bin/env python3
"""
One-time repair for tools/retrofit_cross_ref_wikilinks.py's blind spot: it linked
chapter references that also occurred *inside* a verbatim double-quoted PDF citation,
corrupting the quote text that verify_citations.py matches against the source PDF.

This script finds any [[target|display]] wikilink whose span falls inside a "..."
quoted string and unwraps it back to plain `display` text. Wikilinks outside quotes
(the correct, intended retrofit) are left untouched.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(HERE, "..", "notes")

LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_.-]+)\|([^\]]+)\]\]")
QUOTE_RE = re.compile(r'"[^"]*"')


def quoted_spans(text):
    return [(m.start(), m.end()) for m in QUOTE_RE.finditer(text)]


def fix_line(line):
    spans = quoted_spans(line)
    if not spans:
        return line, 0

    def repl(m):
        if any(s <= m.start() < e for s, e in spans):
            return m.group(2)  # unwrap: keep only the display text
        return m.group(0)  # leave as-is

    new_line = LINK_RE.sub(repl, line)
    n_fixed = len(LINK_RE.findall(line)) - len(LINK_RE.findall(new_line))
    return new_line, max(n_fixed, 0)


def main():
    total_files = 0
    total_fixed = 0
    for source_id in sorted(os.listdir(NOTES_DIR)):
        sdir = os.path.join(NOTES_DIR, source_id)
        if not os.path.isdir(sdir):
            continue
        for fn in sorted(os.listdir(sdir)):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(sdir, fn)
            with io.open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            changed = False
            file_fixed = 0
            for i, line in enumerate(lines):
                new_line, n = fix_line(line)
                if n:
                    lines[i] = new_line
                    changed = True
                    file_fixed += n
            if changed:
                with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.writelines(lines)
                total_files += 1
                total_fixed += file_fixed
                print("FIXED  %-90s  unwrapped=%d" % (os.path.join(source_id, fn), file_fixed))
    print()
    print("files fixed: %d" % total_files)
    print("links unwrapped: %d" % total_fixed)


if __name__ == "__main__":
    main()
