# Execution Spec — DE Master Library (handoff to executing agent)

**Read this before touching anything.** It exists because the first pass produced seven
distinct classes of silent error, all found only by a later adversarial audit. Every
guardrail below maps to a specific defect that actually occurred in this project — none
of them are hypothetical. Full defect record: `audit/GAPS_AND_VERIFICATION.md` §3c and §7.

Governing rule: `vault/_rules/heart.md` → **No-Guess Rule**.
Language: artifacts on disk in English; progress briefs to the user in BM rojak.

---

## ▶ NEXT TASK (read this first)

**State:** 7 / 90 in-scope chapters synthesized (35 / 562 effort units).
`tools/verify_all.py` → **13/13 PASS**. Phases A, A+, B complete. Phase C in progress
(this session added Ch.2, Ch.3, Appendix A, Appendix B on top of the 3 pilots).

**Do this next — `fundamentals_de` Ch.4, then Ch.5, then Ch.6, in that order:**

| Chapter | PDF pages | Size | Words (measured) |
|---|---|---:|---:|
| Ch.4 Choosing Technologies Across the DE Lifecycle | 140–177 | 38pp, long | 14,333 |
| Ch.5 Data Generation in Source Systems | 180–213 | 34pp, long | 12,064 |
| Ch.6 Storage | 214–257 | 44pp, long | 16,116 |

**Scope boundary: do a maximum of 2–3 chapters per session, and stop.** Unchanged
from before — confirmed again this session. Ch.2 and Ch.3 alone required fixing
15 + 15 citation errors after first-draft writing, all traceable to one root cause:
**page numbers were transcribed from memory/paraphrase instead of read directly off
the `--- PDF PAGE NN ---` marker in the extraction at the moment of writing each
claim.** See C4 below — this is now the single highest-value habit to get right.

**Read `tools/GAPS_AND_VERIFICATION.md` §7d (if present) or this session's final
report for the full incident writeup before starting.**

---

## 0. The seven defect classes this spec defends against

| # | What went wrong (actually happened) | Structural defence |
|---|---|---|
| 1 | One structural assumption applied to heterogeneous sources — "level-1 bookmark = chapter" was true for 3 of 5 sources; 2 sources ended up with **zero** chapters in the map | Per-source config + build-time `assert` |
| 2 | Page citations written from memory of reading; 4 of 12 checked were wrong | `verify_citations.py`, blocking |
| 3 | Unmeasured number stated as measured ("~4,700 words", actually 10,698) — and it was the basis of the effort estimate | Numbers injected from script output, never typed |
| 4 | 595 pages flagged by the manifest, then silently abandoned; never disclosed | `FLAG_LEDGER.csv` with mandatory disposition |
| 5 | Status document contradicted itself (§4 said "0 synthesized" while §3b said 2 done) | Status sections generated, not hand-written |
| 6 | External claims presented as evidence ("ISBN matches the O'Reilly catalog") with no lookup ever performed | `lint_notes.py` provenance enforcement |
| 7 | Promised deliverable (`build_full.py`) simply never built, while notes accumulated | `verify_all.py` gate lists promised artifacts |

---

## Phase A — Build the guardrails FIRST (blocking; no synthesis until green)

Do **not** synthesise more chapters before Phase A passes. Every chapter written under
the old process inherits the defects and has to be re-audited by hand — which is exactly
what just cost a full session.

### A1. `tools/verify_citations.py` (blocking gate)

Contract:
- Scan `notes/**/*.md`. For each citation of the form `(pN)`, `(pN–pM)`, `(pN, pM)`,
  find quoted text (`"..."`) in the same sentence or bullet.
- Resolve `source_id` from the note's path, open that PDF, extract the cited page(s).
- Compare with this normaliser (all of it is required — a weaker one produced two
  false accusations during the audit):
  - curly → straight quotes (U+2019/2018/201C/201D)
  - all dash variants (U+2010–U+2014) → `-`
  - strip bullet/object chars (U+2022, U+25A0, U+FFFC)
  - join hyphen-broken line wraps: `re.sub(r'-\s+', '', s)`
  - collapse whitespace, lowercase
- A range citation passes if the quote is found on **any** page in the range.
- Output: table of `PASS/FAIL | claimed | actual | note:line`. **Exit non-zero on any FAIL.**
- Unquoted page citations are reported separately as `UNVERIFIABLE` (not a failure, but
  counted — see rule R3).

### A2. `tools/chapter_stats.py` (number source of truth)

Emits `audit/chapter_stats.json`, one record per `in_synthesis_scope` chapter:
`source_id, chapter_title, pdf_page_start, pdf_page_end, page_count, word_count,
subsection_count, band`. Word count is `len(text.split())` over the exact page range.

**No number describing a chapter may be typed by hand into any note.** Notes read from
this file. `verify_all.py` re-derives and compares.

### A3. `audit/FLAG_LEDGER.csv` + `tools/build_flag_ledger.py`

One row per flagged page, carried over from `PAGE_MANIFEST.csv`:
`source_id, pdf_page, flag_type, disposition, evidence, decided_on`

`flag_type` ∈ `reading_order_risk` (595 rows) | `low_text` (20 rows) | `zero_text` (72,
already dispositioned) | future flags.

`disposition` is **mandatory** and ∈:
- `reviewed-ok` — checked, no issue (evidence required: what was checked, how)
- `reviewed-issue` — problem found (must also appear in GAPS)
- `deferred` — explicitly not doing it (reason required)

The point is not to force review of all 595. It is to make silent abandonment
impossible. `verify_all.py` fails on any blank disposition.

### A4. `tools/lint_notes.py` (provenance enforcement)

- Every claim bullet/paragraph must end with a provenance tag `[S] [D] [N] [U]`.
- Flag sentences asserting facts about things **not in the corpus** — patterns like
  "matches the … catalog", "the original book …", "the industry standard …",
  "as of <year> the market …" — unless tagged `[U]` or containing an explicit
  "NOT CHECKED" clause. This is defect class 6.
- Flag any number written as `~N` or "roughly" where `chapter_stats.json` has an exact
  value. This is defect class 3.

### A5. `tools/build_full.py` (the promised generator)

- Concatenates `notes/**` in fixed order: source order below, chapter order by
  `pdf_page_start`. Full note bodies, not links.
- Header warns the file is generated and records each note's SHA-256.
- **Asserts**: every chapter with `status: synthesized` in the chapter map appears in the
  output; every note file on disk maps to a chapter-map entry (no orphans). Fail loudly.

### A6. `tools/build_master_context.py`

`MASTER_CONTEXT.md` = router + inventory + source status + coverage + unresolved.
Everything factual is **generated** from `SOURCE_REGISTER.csv`, `PAGE_MANIFEST.csv`,
`CHAPTER_MAP.csv`, `chapter_stats.json`, `FLAG_LEDGER.csv`. Hand-written prose lives
only inside `<!-- PROSE:START -->` / `<!-- PROSE:END -->` blocks the generator preserves.
This is defect class 5 — a hand-maintained status table went stale within one session.

### A7. `tools/verify_all.py` — the single Definition-of-Done gate

Runs A1, A2 cross-check, A3 completeness, A4, A5 assertions, plus:
- `PAGE_MANIFEST` row count == sum of `SOURCE_REGISTER` page counts == 2,868
- no duplicate `(source_id, pdf_page)`, no page gaps
- no chapter-map row with `pdf_page_end < pdf_page_start`
- every bookmarked source has ≥ 1 chapter
- promised-artifact existence list (catches defect class 7)

Prints one PASS/FAIL table. **A session is not done until this exits zero.**

---

## Phase B — Clear the outstanding debt (before bulk synthesis)

| # | Task | Acceptance |
|---|---|---|
| B1 | Disposition all 615 open flags (595 `reading_order_risk` + 20 `low_text`) | No blank disposition in `FLAG_LEDGER.csv`. Bulk `deferred` with a written reason is acceptable *if* justified — e.g. the heuristic is known to over-trigger on figure-heavy pages; prove it by sampling ~20 and recording the result, then defer the rest citing that sample. |
| B2 | Second-extractor cross-check | Run `pdfplumber` (and/or `pdftotext`) on a defined subset — minimum: all `low_text` pages + a sample of `reading_order_risk` pages. Record agreement/divergence in the ledger. Set `extraction_method` accordingly. Currently all 2,796 pages say `pypdf` with no cross-check anywhere. |
| B3 | Printed-page labels | Fill `printed_page_label` in `PAGE_MANIFEST.csv`, or record per-source the front-matter offset + numbering scheme and derive it. Currently empty for all 2,868 rows. |
| B4 | Web corpus carried into this project | Copy all 10 rows verbatim (tracking params intact) from `DATA_ENGINEERING_MASTER_LIBRARY_SOURCE_OF_TRUTH.md` §4 into `MASTER_CONTEXT.md`, marked `PENDING_INPUT` for scope. No crawling. |
| B5 | Re-verify the 2 existing pilot notes under A1/A4 | Both must pass the new gates. They were corrected by hand during the audit; the gates have never actually run on them. |

---

## Phase C — Synthesis

### C1. Third pilot FIRST: one *medium* chapter (11–25 pages)

The effort model rests on two pilots (4pp and 30pp). The **medium band is entirely
unmeasured**, yet it carries 26 entries / 130 units = 23% of remaining work. Do one
medium chapter (suggest `kimball_dwtoolkit_3e` Ch.3 "Retail Sales") and recalibrate
before committing to a schedule. Do not state a session count before this.

### C2. Source order (user-set, unchanged)

`fundamentals_de` → `kimball_dwtoolkit_3e` → `ddia_kleppmann` → `airflow_2e` →
`streaming_systems` → `databricks_big_book_4e` → `database_internals_petrov`
(secondary, excluded from original-book coverage).

### C3. Per-chapter loop (the unit of work) — CURRENT PROCEDURE

Run everything with the D-drive venv: `.tools/venv/Scripts/python.exe`.
Work from the `"Data engineering Book knowledge"` directory.

1. **Pick the chapter and read its measured stats** from `audit/chapter_stats.json`
   (`pdf_page_start`, `pdf_page_end`, `page_count`, `word_count`, `band`).
   Never compute or estimate a chapter size by hand (R1).
2. **Extract exactly that page range** to a scratch file under `audit/_scratch_*.txt`,
   read it, then delete the scratch file when the note is written.
3. **If the chapter contains figure-heavy pages** — check `audit/FLAG_LEDGER.csv` for
   `reviewed-issue` rows in the range, and for Kimball/Streaming assume there are some —
   **render those pages to PNG and actually look at them** before writing. The text layer
   does not carry diagram content. Use pymupdf `get_pixmap(dpi=150)` into
   `audit/render_cache/`, then Read the image.
4. **Write the note** to `notes/<source_id>/<chapter_slug>.md` with the standard shape:
   the 9 sections + a declared Exclusions table. Header must state
   `**PDF page range:** N–M` (G1 requires this string) and the measured word count.
5. **Run the gate**: `tools/verify_all.py`. Fix until it exits 0. Do not mark anything
   done while it is red.
6. **Mark synthesized**: `tools/mark_synthesized.py <source_id> "<title substring>"`.
7. **Regenerate**: `tools/build_full.py` then `tools/build_master_context.py`.
8. **Re-run `tools/verify_all.py`** after regeneration — it must still be green.

**Never** edit `MASTER_CONTEXT.md` (outside its `PROSE` blocks) or
`MASTER_CONTEXT_FULL.md` by hand. Edit notes, regenerate.

Run `tools/test_idempotent.py` **only** after changing a generator — it takes several
minutes and is deliberately not part of `verify_all.py`.

### C4. Conventions learned the hard way (violating these produces gate failures)

- **Quote marks mean verbatim-from-source and nothing else.** Do not use them for
  emphasis or for your own terminology. Writing `"mechanism"` about your own framing
  made `verify_citations.py` treat it as a source quote and fail — twice.
- **Never invent quote-boundary punctuation.** If the source sentence continues with a
  comma or semicolon, do not close the quote with a period to make it fit your sentence.
  This was the single most frequent defect (5+ instances).
- **No bracket substitution inside quotes.** `"while they [Snowflake, BigQuery] can
  read..."` is not verbatim. Quote exactly and name the referent outside the quote.
- **Ellipsis elision is allowed** — `"A... B"` — the verifier splits on `...` and checks
  each segment independently on the same page.
- **Every page citation needs either a quotable anchor or a `[D]`/`[U]` tag.** Untagged
  anchorless citations are a hard FAIL (G2/R3).
- **`[D]` is only correct when no quote anchor exists — never as a way to clear R3.**
  An audit found two Ch.2 claims downgraded to `[D]` when a verbatim quote sat on the
  page already cited. That satisfies the gate while losing information: the reader can
  no longer tell the book asserts it. Search the page for an anchor first; downgrade
  only after that fails.
- **Annotated citations are checked now too.** `(p61, Figure 2-8)` and
  `(p57, citing X)` used to be invisible to `verify_citations.py`; six wrong citations
  hid there through every green gate. The regex was widened. Do not assume a form is
  safe because the gate is green — check that the checker can actually see it.
- **All page numbers in notes are PDF page indices**, not printed folio numbers. The two
  differ by a per-source offset (see G1 table). Do not mix them.
- **Write the page citation at the moment you read the claim off the `--- PDF PAGE NN
  ---` scratch marker, not afterward from memory.** This is the single highest-cost
  defect found in this project: writing Ch.2's note from a mental summary of the
  extraction, then adding page numbers by recalling roughly where each fact was,
  produced 15 wrong citations in one chapter (all off by a handful of pages — one
  paragraph's worth of drift, not a systematic offset). Ch.3's note, written by keeping
  the raw extraction open and copying the `--- PDF PAGE NN ---` number directly onto
  each claim as it was drafted, still needed 15 fixes on a chapter twice as dense --
  proportionally better, but confirms this is a per-claim discipline problem, not
  something a smarter regex will catch upstream. Budget real time for the
  `verify_citations.py` fix-up pass on every chapter; it is not optional overhead, it
  is part of the work.
- **When the gate goes red, the first hypothesis is that the tool is wrong**, not the
  note. In this project the checker has been at fault several times (apostrophe
  normalisation, bullet merging, ligature spacing, staleness-vs-idempotency). Verify the
  claim against the source by hand before "fixing" a note to satisfy a possibly-broken
  check.

---

## Phase A+ — second-generation guardrails (G1–G5), built after Phase C started

The first guardrail set (A1–A7) caught citation and state errors. A later review found
five defect classes it could *not* catch. These close them. Each one maps to a defect
that actually occurred or to a measured, concrete risk — none are speculative.

### G1 — Page-basis disambiguation (`tools/detect_page_offsets.py`)

**Problem it solves:** every source numbers its printed pages differently from its PDF
index, and the offset differs per source. Measured this session:

| source | pdf − printed | how established |
|---|---:|---|
| `kimball_dwtoolkit_3e` | −36 | folio sampling, 79% agreement |
| `airflow_2e` | −30 | folio sampling, 100% |
| `fundamentals_de` | −25 | folio sampling, 100% |
| `ddia_kleppmann` | −22 | folio sampling, 99% |
| `databricks_big_book_4e` | 0 | hand-verified, all 16 TOC start pages opened |
| `streaming_systems` | **unresolved** | best candidate held for only 6% of samples |
| `database_internals_petrov` | **unresolved** | best candidate held for only 7% of samples |

A bare citation of "p300" therefore points a reader to a page up to 36 off. The tool
fills `printed_page_label` in `PAGE_MANIFEST.csv` (2,061 / 2,868 rows; front matter and
the two unresolved sources correctly left blank rather than guessed), and `verify_all.py`
now requires every note to declare its page basis. **All page citations in notes are PDF
page indices unless a note says otherwise.**

### G2 — R3 enforced: unverifiable citations must be tagged (`verify_citations.py`)

**Problem it solves:** a page citation with no quotable anchor cannot be machine-checked
at all. 11 such citations existed, all presented as `[S]` source-supported — the single
largest silent-error surface, and one that grows linearly with every new chapter.
Now a hard FAIL unless the claim carries `[D]` (interpretation) or `[U]` (unresolved).
Result: 11 violations → 0, with each one either given a real quote anchor or honestly
downgraded to `[D]`.

### G3 — Figure-coverage check (`tools/check_figure_coverage.py`)

**Problem it solves:** citation checks verify what a note *says*; nothing detects what a
note *omits*. In this corpus a lot of the argument lives in diagrams the text layer does
not carry — proven, not hypothetical: Kimball's Fig 9-4 bus matrix extracts as scrambled
"X" marks, and 7 `streaming_systems` pages are figure-caption-only. Roughly 30 remaining
chapters (Kimball's schema diagrams, Streaming's windowing/watermark figures) are exposed.
The tool finds figure-heavy pages inside each synthesized chapter's range and requires the
note to acknowledge them or declare them in its Exclusions table.

### G4 — Idempotency test (`tools/test_idempotent.py`)

**Problem it solves:** re-running `build_chapter_map.py` after a bug fix once silently
reset all synthesized markers to `located`, destroying progress; it was caught by luck.
The test hashes every artifact, runs all generators twice, and fails if run 2 differs
from run 1.

**Design note learned the hard way:** the first version compared "disk now" vs "after one
run", which also fires when an artifact is merely stale — it produced exactly such a false
alarm on `MASTER_CONTEXT_FULL.md`. Comparing run 1 vs run 2 absorbs staleness so only
genuine non-determinism or state destruction fails. This test is slow (it reads all 2,868
pages several times) and is therefore **not** wired into `verify_all.py` — run it after
changing any generator, not after every chapter.

### G5 — Deferred cross-reference register (`tools/check_deferred_refs.py`)

**Problem it solves:** notes legitimately defer to chapters not yet written (Kimball Ch.9
leans on Ch.5/Ch.7 SCD material). Nothing brought those back for review once the target
was synthesized, so a later note could contradict an earlier one unnoticed. No tool can
check semantic consistency — but this one guarantees the question is re-asked at the right
moment. Deferrals are recorded in `audit/DEFERRED_REFS.csv`; when a target chapter becomes
`synthesized`, the deferral is reported as DUE FOR REVIEW and blocks the gate until marked
`reviewed`.

### Withdrawn from this spec: `audit/checkpoints/`

Phase C3 step 6 originally promised per-source resume checkpoints keyed on file hash.
**This is withdrawn deliberately, not forgotten.** `CHAPTER_MAP.csv`'s `status` column is
already the resume state, and it is now protected against wipe (see G4 and the
`PRIOR_STATUS` carry-forward in `build_chapter_map.py`). Building a second state artifact
would create exactly the kind of duplicate that drifts — the same failure mode that made
`chapter_stats.json` stop tracking `status` independently.

---

## Standing rules for the executing agent

- **R1 — Never type a measured number.** Pages, words, counts, sizes come from script
  output. If a script doesn't produce it, write the script or write "not measured".
- **R2 — Never cite a page you haven't verified this session.** A1 is cheap; run it.
- **R3 — Every page-cited claim needs a quotable anchor**, or it must be downgraded to
  `[D]` (interpretation). Paraphrase with a page number and no quote is unverifiable and
  is how the four bad citations got in.
- **R4 — A flag raised is a debt.** Same session: disposition it or write it to the
  ledger as `deferred` with a reason. Never leave it hanging.
- **R5 — Structure is per-source until proven otherwise.** Never apply one structural
  rule across all 7 sources without verifying it holds for each and asserting it in code.
- **R6 — Status text is generated.** If you find yourself hand-editing a coverage table,
  stop and fix the generator instead.
- **R7 — Report gaps in the same breath as progress.** The audit's worst finding wasn't
  a wrong number, it was 595 abandoned flags that no document mentioned.

---

## What these guardrails do NOT catch (stated honestly)

- **Semantic misreading.** A note can cite the right page, quote it correctly, and still
  misunderstand the argument. No script catches this. Mitigation: after each source is
  finished, a second pass spot-audits 2 chapters for meaning, not mechanics.
- **Paraphrased claims.** A1 verifies quoted anchors only; `[D]` claims are unverifiable
  by construction. That is why R3 forces the downgrade to be explicit.
- **Omission.** Nothing detects a concept the note simply left out. The per-chapter
  exclusion table is the partial defence — it forces omissions to be declared.
- **Band multipliers.** 1×/5×/9× is a fit to two data points. After C1 it is three.
  It remains an estimate and should never be reported as a schedule.
