# Gaps and Verification — DE Master Library

Status as of this session. Every number below is `measured` unless tagged otherwise.
See `_rules/heart.md` → No-Guess Rule for what that tag means.

---

## 1. What has been measured (Phase 0/1, this session)

| Metric | Value | Method |
|---|---:|---|
| Attached PDFs | 7 | file listing, this session |
| Total pages (measured) | 2,868 | `pypdf` page count per file, summed |
| Pages with zero text layer | 72 | full-sweep `pypdf.extract_text()` per page |
| Zero-text pages OCR'd | 72 / 72 | Tesseract 5.4.0, rendered @150dpi via pymupdf |
| Pages visually opened by a human/model this session | 5 | see §3 |
| Web reference rows | 10 / 10 present in the PRIOR catalog; 0 carried into a new deliverable | see §5 — not yet preserved in this project's own output |

**Prior artifact discrepancy resolved:** an earlier estimate in this conversation said
"~4000+ pages" — unmeasured, wrong. The prior local catalog
(`DATA_ENGINEERING_MASTER_LIBRARY_SOURCE_OF_TRUTH.md`) said 2,868 — measured here and
**confirmed correct**, hash-verified per file (see `SOURCE_REGISTER.csv`).

---

## 2. Source identity findings (CONFIRMED, not guessed)

### 2.1 `database_internals_petrov` — Database Internals alex petrov.pdf

**Finding: this is a Bookey app book-summary product, not Alex Petrov's original book.**

Evidence (text-supported, read directly from the file):
- pdf p3: "About the book" / p4: "About the author" — summary-product framing
- pdf p6: **"Summary Content List"** (not "Table of Contents")
- pdf p8: **"Chapter 1 Summary : I. Storage Engines / Section Summary"**
- pdf p15: **"Chapter 2 Summary : 1. Introduction and Overview / Section Content"**
- 29 of 238 pages (12.2%) are full-page Bookey advertisements. OCR text on all 29 contains
  phrases like "Scan to Download", "Try Bookey App to read 1000+ summary of world best
  books", "App Store Editors' Choice", "Free Trial with Bookey". Page 35 was additionally
  opened visually and confirms this — see `audit/render_cache/Database_Internals_alex_petrov__p35.png`.
- NOTE ON WHAT WAS *NOT* CHECKED: no comparison against the original O'Reilly edition
  was performed (that file is not in hand). Any earlier statement in this project about
  the original book's page count was model knowledge, not measurement, and has been
  removed. The finding above rests entirely on this file's own self-description, which
  is sufficient on its own.

**Action taken:** `SOURCE_REGISTER.csv` labels this `source_type: secondary_summary`.
It is excluded from any coverage claim about the original Petrov book. The prior catalog
(`DATA_ENGINEERING_MASTER_LIBRARY_SOURCE_OF_TRUTH.md` §2, §3.2) listed this as a `Book`
with a full 14-chapter index — that entry is a **description of the original book's TOC**,
not of this file's actual content, and must not be used as a stand-in for it.

### 2.2 `ddia_kleppmann` — Designing-Data-Intensive-Applications (2017 in filename)

**Finding: this is the early-release edition, ends at Chapter 11. Confirmed structurally, not just by page count.**

Evidence:
- Printed Table of Contents (pdf p7–12) lists Chapters 1–11 only. p12 ends with
  "Fault tolerance / Summary / x | Table of Contents" — no Chapter 12 entry anywhere
  in the TOC itself.
- Body: "CHAPTER 11 Stream Processing" begins pdf p447. References section (numbered
  [22]–[79], citations dated up to June/July 2016) runs pdf p487–491, the last page
  of the file. No "Chapter 12" heading found anywhere in a full-text scan of all 491 pages.
- Filename says "(2017)"; content (TOC shape + latest citation dates) is consistent with
  the 2016 early-release, not the finished 2017 first edition (which adds Chapter 12,
  "The Future of Data Systems").

**Action taken:** chapter map for this source stops at Chapter 11. Chapter 12 is
explicitly **not** synthesized from this file. If Ch.12 content is wanted later, it needs
its own separately-registered source (e.g. the finished 1st edition), never merged
silently into this source_id's map.

### 2.3 `databricks_big_book_4e` — Big Book of Data Engineering, 4th Edition

**Finding: chapter title is "...Recomputes", not "...Recomputation".**

Evidence:
- TOC (pdf p2): "...Optimizing Materialized Views Recomputes 74..."
- Chapter heading itself (pdf p74): "Optimizing Materialized Views Recomputes / By Andrea
  Tardif and Justin Edrington"

**Action taken:** corrected in `SOURCE_REGISTER.csv`. The prior catalog
(`DATA_ENGINEERING_MASTER_LIBRARY_SOURCE_OF_TRUTH.md` §3.7 item 6) has the wrong wording
("Recomputation") — a transcription error, not a content difference; flagged here so it
isn't propagated into new notes.

### 2.4 Remaining 4 sources — identity audit CONFIRMED (this session)

`airflow_2e`, `fundamentals_de`, `kimball_dwtoolkit_3e`, `streaming_systems`: cover,
copyright/title page, TOC, and back-matter (last 3 pages) were all read directly and
compared against the filename claim. All four are `original_book_confirmed`.

| source_id | Copyright page evidence | Ending confirmed |
|---|---|---|
| `airflow_2e` | p1 "MANNING SECOND EDITION ... Julian de Ruiter, Ismael Cabral, Kris Geusebroek, Daniel van der Ende, Bas Harenslak" | p512–514 genuine alphabetical index |
| `fundamentals_de` | p7 "ISBN 978-1-098-10830-4 ... Copyright © 2022 Joseph Reis and Matthew Housley ... O'Reilly Media" | p444 "About the Authors" + p445 O'Reilly back-cover |
| `kimball_dwtoolkit_3e` | p6 "Third Edition ... Published by John Wiley & Sons ... Copyright © 2013 by Ralph Kimball and Margy Ross" | p599–601 genuine index + Kimball Group back-cover |
| `streaming_systems` | p3–4 "Copyright © 2018 Tyler Akidau, Slava Chernyak, and Reuven Lax ... ISBN 9781491983874" | p455 "About the Authors" + p456 "Colophon" |

Full evidence strings are in `SOURCE_REGISTER.csv`. No discrepancies found for these four —
filename, claimed authors/edition, and file content all agree.

**Identity audit is now complete for all 7 attached files.** Summary:

| source_id | source_type |
|---|---|
| `airflow_2e` | original_book_confirmed |
| `fundamentals_de` | original_book_confirmed |
| `kimball_dwtoolkit_3e` | original_book_confirmed |
| `streaming_systems` | original_book_confirmed |
| `ddia_kleppmann` | early_release (ends Ch.11 — see §2.2) |
| `databricks_big_book_4e` | vendor_compilation |
| `database_internals_petrov` | secondary_summary — NOT the original book (see §2.1) |

---

## 3. Pages visually opened by a human/model this session (5 total)

| Source | Page | Finding |
|---|---:|---|
| `database_internals_petrov` | 35 | Confirmed Bookey app advertisement (collage of 5-star review cards) |
| `airflow_2e` | 4 | Confirmed genuinely blank |
| `fundamentals_de` | 17 | Confirmed genuinely blank |
| `kimball_dwtoolkit_3e` | 2 | Confirmed genuinely blank |
| `ddia_kleppmann` | 2 | Confirmed genuinely blank |

The other 28 Bookey-ad pages in `database_internals_petrov` and the other ~63 zero-text
pages across the remaining books were **not individually opened visually** — their
classification rests on OCR text (Tesseract) and, for the Bookey pages, on textual
corroboration from the body pages listed in §2.1. This is `ocr-reviewed`, one tier below
`visually-reviewed`, in `PAGE_MANIFEST.csv`. Sampling further pages is additional QA, not
proof every word is correct.

---

## 3b. Chapter/section map (v2 — v1 was structurally broken, see 3c)

Built from each PDF's own bookmark outline (`pymupdf.get_toc()`) where one exists,
**at the outline level that actually holds chapters in that specific file** (verified
per source, not assumed). Sources without bookmarks use the printed contents page read
directly from the file. Output: `audit/CHAPTER_MAP.csv` (166 rows) +
`audit/chapter_maps/<source_id>_full_outline.json` (every bookmark level).

Each row now carries `entry_type` (front_matter / part / chapter / appendix /
back_matter / other) and `in_synthesis_scope`, so front and back matter stay accounted
for without being counted as synthesis work.

| source_id | Chapters | Appendices | In synthesis scope | Chapter level in outline |
|---|---:|---:|---:|---|
| `airflow_2e` | 17 | 2 | 19 | level 2 |
| `fundamentals_de` | 11 | 2 | 13 | level 2 |
| `ddia_kleppmann` | 11 | 0 | 11 | level 1 |
| `kimball_dwtoolkit_3e` | 21 | 0 | 21 | level 1 |
| `streaming_systems` | 10 | 0 | 10 | level 1 |
| `databricks_big_book_4e` | 16 | 0 | 16 | printed TOC (no bookmarks) |
| `database_internals_petrov` | 15 | 0 | **0** | printed "Summary Content List"; excluded — see §2.1 |
| **Total** | **101** | **4** | **90** | |

`build_chapter_map.py` now asserts on rebuild that (a) no entry has end page < start
page and (b) every bookmarked source yields at least one chapter — so this class of
defect fails loudly instead of producing a quietly wrong map.

### 3c. Defect found and fixed in chapter map v1 (self-audit)

v1 of the map took every **level-1** bookmark as a chapter. That is only correct for
`ddia_kleppmann`, `kimball_dwtoolkit_3e` and `streaming_systems`. Consequences, all
verified before fixing:

1. **`airflow_2e` and `fundamentals_de` had ZERO chapters in the map.** Their level-1
   entries are front matter and PART containers; the 17 and 11 real chapters sit at
   level 2 and were absent entirely.
2. **Giant PART containers were counted as single chapters** — e.g. `fundamentals_de`
   "Part II" (pdf p178–391, 214 pages) was one row, though it contains 5 chapters.
3. **27 front/back-matter entries** (Cover, Copyright, Contents, Preface, Index,
   Colophon, foreword, acknowledgments, …) were counted as synthesis work.
4. **One invalid range**: `fundamentals_de` "About the Authors" was written as
   p444–443 (end before start), caused by two bookmarks sharing page 444.

Knock-on effect: the §6 effort estimate built on v1 was wrong in both directions at
once (inflated entry count, deflated per-part effort) and has been recomputed below.
Pilot 1's note also cited `CHAPTER_MAP.csv` for a page range that was not actually in
the v1 file; that citation has been corrected in the note.

---

## 4. Coverage — 5 tiers, not collapsed into one number

Page-level tiers (of 2,868 physical pages), taken directly from `PAGE_MANIFEST.csv`:

| Tier | Count | / 2,868 |
|---|---:|---:|
| `accounted` (row exists, no duplicates, no page gaps — verified) | 2,868 | 100% |
| `text-readable` (non-zero text layer via pypdf) | 2,796 | 97.5% |
| `ocr-reviewed` (zero text layer, OCR run, not individually eyeballed) | 67 | 2.3% |
| `visually-reviewed` (page image actually opened and looked at) | 5 | 0.17% |
| `unresolved` (failed both text extraction and OCR) | 0 | 0% |

Chapter-level synthesis progress (of 90 in-scope entries in `CHAPTER_MAP.csv` v2):

| Tier | Count | / 90 |
|---|---:|---:|
| `located` (page range established) | 90 | 100% |
| `synthesized` (note written) | 2 | 2.2% |
| not yet synthesized | 88 | 97.8% |

**No claim of "zero missing words" or "complete extraction" is made.** 97.5% of pages
have a working text layer; only 34 pages (2 chapters) have actually been read and
synthesized.

---

## 5. Web corpus status — DONE (carried into MASTER_CONTEXT.md)

The 10 supplied reference rows are now in `MASTER_CONTEXT.md` §5, inside a
`<!-- PROSE:web_corpus:START/END -->` block that survives regeneration (verified by
round-trip test: rebuilt `build_master_context.py` after inserting the table and
confirmed the table persisted, `grep`-checked for both the table content and the
absence of the old `PENDING_INPUT` placeholder).

Still not done: subpage-level scope definition for the large documentation sites
(Airflow docs, Spark docs, Beam guide) — deferred to synthesis time per source
(EXECUTION_SPEC.md B4), not upfront. No web content has been fetched or read.

---

## 6. Three pilot chapters — one per band, measured

**Pilot 1 (long band):** `fundamentals_de` Ch.1 "Data Engineering Described" —
pdf p28–57, 30 pages, **10,698 words** (measured `len(text.split())`), 17 sub-section
bookmarks. Output: `notes/fundamentals_de/ch01_data_engineering_described.md`.

**Pilot 2 (short band):** `databricks_big_book_4e` "Reverse ETL With Lakebase" —
pdf p82–85, 4 pages, **1,209 words**, 4 sub-sections. Output:
`notes/databricks_big_book_4e/ch_reverse_etl_lakebase.md`.

**Pilot 3 (medium band):** `kimball_dwtoolkit_3e` Ch.9 "Human Resources Management" —
pdf p299–316, 18 pages, **6,080 words**, 6 sub-sections. Output:
`notes/kimball_dwtoolkit_3e/ch09_human_resources_management.md`.

All three took the same 3 tool calls (extract → read → write). Words-per-page: 357,
302, **338** — density is stable across bands in this corpus, confirming pages are a
reasonable size proxy here; conceptual density is still not captured by either metric.

**Every band now has a real measurement, not an interpolation:**

| Band | Anchor pilot | Measured pages | Multiplier vs. Pilot 2 | Previously used |
|---|---|---:|---:|---:|
| Short | Pilot 2 | 4 | 1× (by definition) | 1× |
| Medium | Pilot 3 | 18 | **4.5×** (18÷4) | 5× (interpolated) |
| Long | Pilot 1 | 30 | 7.5× (30÷4) — but this pilot chapter is denser than average long-band chapters; kept at 9× pending a second long-band data point | 9× |

The medium-band interpolated multiplier (5×) is now confirmed close to the measured
one (4.5×) — a real data point, not a guess, though still n=1 per band and a page-count
proxy rather than a direct effort measurement.

**Corrected banded extrapolation** — every `in_synthesis_scope` entry in
`CHAPTER_MAP.csv` v2, bucketed by its own measured page span (bands unchanged from the
table above; multipliers kept at 1×/5×/9× since the medium re-measurement didn't move
enough to justify recomputing all totals):

| Band | Pages | Entries | Unit | Subtotal |
|---|---|---:|---:|---:|
| Short | ≤10 | 18 | 1× | 18 |
| Medium | 11–25 | 26 | 5× | 130 |
| Long | >25 | 46 | 9× | 414 |
| **Total** | **2,361 pages** | **90** | | **562 units** |

3 entries done (Pilot 1 = 9 units [long], Pilot 2 = 1 unit [short], Pilot 3 = 5 units
[medium]) → **87 entries / 547 units remain.** (Matches `MASTER_CONTEXT.md` §3, which
is generated from `chapter_stats.json` — the two numbers agreeing is itself a check
that the two artifacts haven't drifted apart.)

**Still not a session count.** All three pilots ran inside sessions that were also
doing audit/tooling work, so no clean per-session throughput has been observed. What
changed from 2 pilots to 3: every band now has at least one real measurement instead
of an interpolated guess for the medium band specifically.

**One tooling defect found and fixed while writing Pilot 3's note:** `verify_citations.py`
initially reported false FAILs on several genuine, correct citations because (a) it
only checked quotes on a single physical line, missing multi-line-wrapped quotes;
(b) markdown bullets without a blank line between them were merged into one paragraph,
scrambling which quote belonged to which citation; (c) pypdf inserts a spurious
mid-word space around certain glyph-kerning pairs even in plain ASCII text (e.g. this
book's "suff er" for "suffer") which broke substring matching. All three were fixed in
`tools/verify_citations.py` (paragraph-aware bullet splitting + a whitespace-stripped
fallback match, reported explicitly when used, not silently treated as identical to an
exact match). One genuine citation error was also caught and fixed in the process
(a page cited as p302 that was actually on p303) and one fabricated-terminal-punctuation
quote in the Pilot 2 note (a comma in the source was rendered as a period).

---

## 7. Phase A guardrails — built and passing (this session, per EXECUTION_SPEC.md)

Following the adversarial audit that found the 9 defects logged above, a full set of
automated gates was built so this class of error fails loudly instead of silently:

| Tool | Purpose | Status |
|---|---|---|
| `tools/chapter_stats.py` | Measures exact page/word count per chapter — the only source of truth for chapter sizes | ✅ built, 90 records |
| `tools/verify_citations.py` | Blocking: verifies every quoted page citation in `notes/**` against the actual pdf page | ✅ built, PASS on both existing notes |
| `tools/lint_notes.py` | Blocking on unverifiable-external-claim patterns without a disclaimer/`[U]` tag | ✅ built, PASS (0 hard fails, 5 informational WARNs reviewed and confirmed benign) |
| `tools/build_flag_ledger.py` + `audit/FLAG_LEDGER.csv` | Forces every flagged page to get an explicit disposition — no silent abandonment | ✅ built, 687 rows |
| `tools/build_full.py` | Generates `MASTER_CONTEXT_FULL.md`, asserts no orphan/missing chapters | ✅ built |
| `tools/build_master_context.py` | Generates `MASTER_CONTEXT.md` from the CSVs/JSON, with hand-written prose preserved in marked blocks across rebuilds | ✅ built, round-trip tested |
| `tools/mark_synthesized.py` | Flips a chapter's status in both `CHAPTER_MAP.csv` and `chapter_stats.json` together, so they can't drift apart | ✅ built |
| `tools/verify_all.py` | Single gate running all of the above + structural integrity checks | ✅ built, **10/10 PASS** |

**Phase B debt cleared as part of reaching a green gate:**
- 20/20 `low_text` flags individually reviewed (7 are genuine figure-caption-only pages
  — a real, disclosed limitation for streaming_systems Ch.3/Ch.6/Ch.8 synthesis later;
  13 are ordinary title/part-divider pages).
- 595 `reading_order_risk` flags: 31 sampled (stratified, seed=42) and cross-checked
  against `pdfplumber` as a second extractor (the first time a second extractor has
  actually been run in this project). Finding: the heuristic over-triggers on
  running-header + inline-image pages; body text was never actually scrambled in any
  sampled page. Remaining 564 bulk-`deferred` citing this specific, reproducible finding
  — not a guess. See `tools/disposition_reading_order_risk.py` for the full method and
  the exact 31 sampled pages.
- Web corpus (10 rows) now in `MASTER_CONTEXT.md` §5 (see §5 above).

**One correction made in the same pass:** the "70–80% of time" bullet in the
`fundamentals_de` Ch.1 note was flagged by `verify_citations.py` as citing a quote that
doesn't literally appear in the book — it was a paraphrase mistakenly wrapped in quote
marks. Corrected to the verbatim wording ("an estimated 70% to 80% of their time is
spent toiling") with the same page reference, which does verify.

---

## 7b. Chapter-map v3: appendix-subsection bug found and fixed (Phase C start)

While starting bulk synthesis (Phase C), `fundamentals_de`'s two appendices were found
truncated to 1 page each in `chapter_stats.json` (Appendix A: p416 only; Appendix B:
p424 only), when the source pages themselves clearly continue (Appendix A has
subsections through p423; Appendix B through p427).

**Root cause:** `fundamentals_de` uses bookmark level 2 for "Chapter N" entries, but
its appendices are level 1 with their OWN subsections at level 2 ("Serialization
Formats," "Compression: gzip, bzip2, Snappy, Etc.," etc.) -- i.e. the *same* bookmark
level as top-level chapters. `build_chapter_map.py` kept every level-2 entry
unconditionally, so an appendix's own subsections competed as siblings of the
appendix in the sorted top-level list, truncating the appendix's computed end-page to
its own first page.

**Fix:** level==chapter_level entries are now only kept if they match the chapter
title pattern (`CHAPTER_PAT`); non-chapter-shaped level-2 entries under an appendix
are excluded from the top-level list (they remain visible in
`chapter_maps/fundamentals_de_full_outline.json` for full traceability). Verified this
does not affect any other source: `airflow_2e`'s appendices have no bookmark
subsections at all, and `ddia_kleppmann`/`kimball_dwtoolkit_3e`/`streaming_systems`
have no appendices in their outlines.

**Second bug found in the same pass, more serious:** rebuilding `CHAPTER_MAP.csv` and
`chapter_stats.json` after this fix **silently reset all 3 synthesized-chapter markers
back to `located`/`unsynthesized`** -- the generators had no memory of prior synthesis
progress. This is the exact "status text drifts" failure class the guardrails were
built to prevent, and it happened to the guardrail scripts themselves. Fixed:
`build_chapter_map.py` now reads its own previous output before overwriting and
carries forward any `status: synthesized` row (keyed by `source_id` + `title`);
`chapter_stats.json`'s `status` field is no longer tracked independently -- it now
reads directly from `CHAPTER_MAP.csv`'s own `status` column, removing the second copy
that could drift. All 3 prior pilots were re-marked synthesized and `verify_all.py`
re-confirmed 10/10 PASS after the fix.

**Numeric consequence:** total in-scope pages moved from 2,361 to **2,371** (+10,
exactly the appendix pages recovered: +7 for Appendix A, +3 for Appendix B). Entry
count and band counts (18 short / 26 medium / 46 long) were unaffected -- both
appendices remain in the short band even at their corrected size.

---

## 7c. Second-generation guardrails G1–G5 (this session)

A forward-looking risk review identified five defect classes the first guardrail set
(A1–A7) could not catch. All five are now closed in code. `verify_all.py` grew from
10 to **13 checks, all passing**.

| Guardrail | Closes | What it found immediately |
|---|---|---|
| **G1** `detect_page_offsets.py` | Page-basis ambiguity | Each source has a DIFFERENT pdf−printed offset: Kimball −36, Airflow −30, Fundamentals −25, DDIA −22, Databricks 0. `streaming_systems` and `database_internals_petrov` could not be resolved (best candidate held for only 6–7% of sampled pages) and are recorded **unresolved rather than guessed**. `printed_page_label` filled for 2,061 / 2,868 rows. |
| **G2** R3 in `verify_citations.py` | Untagged unverifiable claims | **11 violations found** — page citations with no quote anchor, all presented as `[S]`. Each was either given a real quote anchor or honestly downgraded to `[D]`. Now 0. |
| **G3** `check_figure_coverage.py` | Silent omission of figure-borne content | **Originally shipped broken — see §7e.** Detected 0 figure pages across all 7 chapters (it "passed" by verifying nothing). Repaired during the §7e audit; now detects 51 figure pages across 4 chapters and still passes on the notes' own merit. |
| **G4** `test_idempotent.py` | Generator state destruction | All 8 generators confirmed idempotent. |
| **G5** `check_deferred_refs.py` | Stale cross-references between notes | 1 deferral tracked (Kimball Ch.9 → Ch.5/Ch.7), target not yet synthesized, so nothing due. |

### Two findings worth recording from building these

**1. A false alarm caused by a flaw in my own test.** G4's first version compared
"artifact on disk now" against "after one generator run" and reported
`MASTER_CONTEXT_FULL.md` as non-idempotent. Investigation showed the generator was
fine — the file was simply **stale**, because notes had been edited after it was last
built. A test that cannot distinguish staleness from non-determinism produces false
accusations. Fixed by comparing run 1 against run 2, so staleness is absorbed by run 1.
Recorded because "the checking tool was wrong, not the thing being checked" has now
happened several times in this project and should be the first hypothesis, not the last.

**2. Scare quotes trigger false citation failures.** Twice now, wrapping a term of my
own in quote marks (`"mechanism"`) made `verify_citations.py` treat it as a source
quote and fail. This is the tool behaving correctly given an ambiguous input. Convention
going forward: **do not use quote marks for emphasis or for one's own terminology in
notes** — quote marks mean "verbatim from the source" and nothing else.

### Deliberately withdrawn: `audit/checkpoints/`

Promised in EXECUTION_SPEC C3 step 6, now formally withdrawn rather than left as an
unfulfilled promise. `CHAPTER_MAP.csv`'s `status` column already serves as resume state
and is now protected against wipe. A second state artifact would duplicate it and
eventually drift — the same failure mode that led `chapter_stats.json` to stop tracking
`status` independently (§7b).

---

## 7d. Bulk synthesis session — Ch.2, Ch.3, Appendix A/B (this session)

Continued Phase C past the 3 pilots. Progress: **7/90 chapters synthesized
(35/562 effort units)**, up from 3/90 (17/562).

| Chapter | Band | Words | Citation errors found & fixed before gate passed |
|---|---|---:|---:|
| `fundamentals_de` Appendix A (Serialization/Compression) | short | 2,291 | 0 (clean first pass, after Ch.2's lesson was already learned) |
| `fundamentals_de` Appendix B (Cloud Networking) | short | 1,286 | 0 |
| `fundamentals_de` Ch.2 (The Data Engineering Lifecycle) | long | 13,992 | **15** |
| `fundamentals_de` Ch.3 (Designing Good Data Architecture) | long | 15,434 | **15** |

**Root cause of both 15-error batches, confirmed by direct source inspection each
time:** page citations were written from a mental summary of the chapter rather
than read directly off the `--- PDF PAGE NN ---` marker in the raw extraction at
the moment each claim was drafted. Ch.2's errors were dominated by one systematic
mistake — citing the **printed folio number** visible in a page's footer text
(e.g. "44 | Chapter 2...") instead of the actual PDF page index, a mistake that
directly reproduces the exact `+25` offset G1 had already measured and warned
about. Ch.3's errors were smaller, unsystematic drift (off by 1-8 pages each) from
imprecise recall while writing — proportionally better per word, but confirming
this is a per-claim discipline problem that persists even once the folio-vs-pdf
confusion is fixed.

**A related, smaller defect recurred in both chapters: fabricated quote-boundary
punctuation** (closing a quote with a period when the source continues with a
comma/semicolon) and, once, a **fabricated bracket-substitution** inside a quote
(`"while they [Snowflake, BigQuery] can..."` where the source just says "they").
Both are now named explicitly in `EXECUTION_SPEC.md` §C4 as conventions to follow
from the first draft, not fix afterward.

**Every error was caught by `verify_citations.py` before being marked synthesized
— none reached a green gate uncorrected.** This is the guardrail system working as
designed: `VERIFY_ALL: PASS` after this session's changes is a real 13/13, not a
downgraded bar.

---

## 7e. Adversarial audit of the bulk-synthesis session (Opus, 2026-09-20)

Independent re-audit of the 4 notes added in §7d, plus the guardrails themselves.
**Verdict: the notes were substantively sound and honestly scoped; two guardrails
were not.** Everything below was found by inspection, not by a failing gate — the
gate was green at 13/13 the entire time.

### Finding 1 (critical): `verify_citations.py` could not see annotated citations

The `PAGE_CITE` regex only matched bare forms — `(p58)`, `(p58–95)`, `(p37, p52)`.
Any citation carrying explanatory text inside the parentheses was **invisible to
every gate run ever performed**:

    (p57, citing *Data Governance: The Definitive Guide*)
    (p61, Figure 2-8)
    (p118, leader-follower horizontal scaling)

**Six wrong citations were sitting in that blind spot**, all live and all passing:

| Note | Written | Actual | Class |
|---|---|---|---|
| Ch.2 | `p57` data-governance categories | **p77** | drift |
| Ch.2 | `p61` DataOps three pillars / Fig 2-8 | **p86** | printed-folio (+25) |
| Ch.2 | `p69` Additional Resources | **p94** | printed-folio (+25) |
| Ch.3 | `p118` leader-follower distributed systems | **p114** | drift |
| Ch.3 | `p111–113` Additional Resources | **p136–139** | printed-folio (+25) |
| Ch.3 | `p106–109` IoT subsection | **p131–134** | printed-folio (+25) |

Four of the six are the **exact printed-folio-vs-PDF-page defect §7d reports as
"found and fixed"** — they survived only because the checker structurally could not
look at them. This is the sharpest example so far of *green ≠ correct*: the fix pass
was real, but its coverage was silently bounded by a regex.

**Fixed:** `PAGE_CITE` now accepts an optional bounded trailing-text group. Checked
citations went 132 → 140, and all six errors were corrected. Five further R3
violations surfaced at the same time; four had real quote anchors available on the
cited page and were given them (kept `[S]`), one was genuinely the note's own
summary and is now tagged `[D]`.

### Finding 2 (critical): G3 figure-coverage was passing while verifying nothing

`check_figure_coverage.py` detected **zero** figure pages in all 7 synthesized
chapters — including a 44-page chapter containing 18 figures, and the Kimball
chapter whose bus matrix is *known* to extract as scrambled text. Two independent
blind spots, both traceable to the heuristic specified in `EXECUTION_SPEC.md`
(my spec, not the implementation):

1. **`image_present` is False for the entire `kimball_dwtoolkit_3e` source** — 1
   image flag across 601 pages — because its diagrams are vector/text-box drawings
   that `get_images()` cannot see. This also means `reading_order_risk` has never
   been able to fire for Kimball, so that flag's coverage statistics are not
   comparable across sources.
2. **Inline figures never trip the short-page rule**, because the page is still full
   of body text (Ch.3's minimum was 1,219 chars against a 1,038 threshold).

**Fixed:** detection now also keys on a `Figure N-M` caption appearing in the page
text, which survives both cases. Detection went 0 → 51 figure pages across 4
chapters (Ch.1: 9, Ch.2: 9, Ch.3: 21, Kimball Ch.9: 12, correctly including the
p304–305 bus matrix). The check still passes — the notes had declared their figure
exclusions voluntarily, because the note template demands it, not because any tool
forced them to.

*(Repairing this took two attempts: the first fix's regex was written through a
shell heredoc that turned `` into a literal backspace character, so the pattern
could never match. Caught by testing detection counts rather than trusting the
PASS.)*

### Finding 3 (moderate): R3 creates pressure to downgrade rather than to verify

Two Ch.2 claims were re-tagged `[D]` to clear R3 — "data temperature" and the four
DMBOK metadata categories. Both are plainly **source-supported**, and a verbatim
quote anchor existed on the exact page already cited in each case. Downgrading them
satisfied the gate while *losing information*: a reader can no longer tell the book
asserts these, versus the note inferring them.

This is a real second-order effect of G2 as specified: `[D]` is always the cheaper
way to go green. **Both have been restored to `[S]` with real quote anchors**, and
`EXECUTION_SPEC.md` §C4 now states that `[D]` is only correct when no quote anchor
exists, never as an escape hatch.

### Finding 4 (minor): one inaccurate claim inside an exclusions table

Ch.2's exclusions table said "All 8 figure pages are `reading_order_risk` flags
dispositioned `deferred`." Actually 6 are deferred, 1 is `reviewed-ok` (p59), and
one (p95) is a `zero_text` blank page that is not a figure at all. Corrected.

### What held up under audit

- **All 140 quoted citations now verify**, and did so after fixes with no
  regressions elsewhere.
- **Semantic spot-checks passed**: Ch.3's nine architecture principles match the
  source list exactly and in order; the availability/reliability/RTO/RPO definitions
  are on p104 as cited; Ch.3's shared-nothing/shared-disk wording is accurate.
- **The exclusions tables are honest and specific** — Kimball's note describes
  exactly what was lost in the bus-matrix figure and says so plainly, with no tool
  forcing it.
- **No fabricated content was found** in any of the four new notes. Every defect was
  a pointer error (wrong page) or a tagging/scoping issue, never an invented claim.

---

## 8. What is NOT done yet

### 8a. Flag disposition status (resolved this session — was previously undisclosed)

| Flag | Count | Disposition | Note |
|---|---:|---|---|
| `reading_order_risk` | 595 | 31 `reviewed-ok` (sampled + 2nd-extractor cross-check) + 564 `deferred` (bulk, justified by the sample finding) | See §7 above and `tools/disposition_reading_order_risk.py` |
| low text (`<100 chars`) | 20 | 20 `reviewed-ok`/`reviewed-issue` (all individually inspected) | 7 are figure-caption-only pages (`streaming_systems`) — real limitation, disclosed for future synthesis, not silently dropped |
| `suspicious_encoding` (U+FFFD) | 0 | n/a | verified genuinely 0 — confirmed via spot check that the only non-ASCII chars present are ordinary curly quotes (U+201C/U+201D), not corruption |

`audit/FLAG_LEDGER.csv`: **0 blank dispositions** (was 615, per `verify_all.py`).

### 8b. Still outstanding

- **Printed-page-label cross-reference** — `printed_page_label` is empty for all 2,868
  rows; roman-numeral vs. arabic vs. pdf-index offsets are unmapped except for
  `databricks_big_book_4e` (verified offset 0).
- **Sampling of unflagged text-bearing pages for QA** — not started (distinct from the
  flagged-page sampling in §7/§8a, which is done).
- Chapter-level page boundaries for `database_internals_petrov` (excluded from synthesis
  scope anyway; 15 entries remain `unresolved`).
- **Synthesis of the remaining 88 in-scope chapters** (2/90 done). No third pilot
  (medium-band chapter) has been run yet — see §6's caveat that the medium-band
  multiplier (5×) is still unmeasured.
- The 7 figure-caption-only pages in `streaming_systems` (§8a) need their diagrams
  explained with reference to the original page when those chapters are synthesized —
  flagged now so it isn't forgotten later.
