# Concept Hub Build Spec — execution handoff

> **Status:** design locked on Opus, execution intended on Sonnet.
> **Read this file first.** Everything needed to execute is here or in the generated artifacts.
> Do not re-derive the concept map — it is already measured.

---

## Locked decisions (already approved — do not re-ask)

| Decision | Choice |
|---|---|
| Hub location | `vault/concepts/` (study-side, **not** under `notes/`) |
| Granularity | ~30 concepts |
| Hub shape | Full shape — see canonical exemplar below |
| Build order | **Hubs first**, §9 wikilink retrofit **last** |

**Canonical exemplar:** [[deduplication]] — already written and approved. Copy its section
structure exactly: one-line definition → spread line → framing/"two faces" table (only where a
real split exists) → per-source *Where it appears* tables → *Your own track notes* → *The thread*
→ *Same word, different meaning* → *Related* wikilinks.

---

## Input artifacts (all regenerable)

| File | What it is |
|---|---|
| `_index.generated.md` | Human-readable spread report + per-concept chapter evidence |
| `_index.generated.json` | Machine-readable concept → source → file → hit-count mapping |
| `_digest.generated.txt` | Compact per-concept digest (top 5 files per source) — **use this while writing** |
| `vault/state/build_concept_index.py` | Generator. Re-run after adding sources: `python vault/state/build_concept_index.py` |

Scan covered **138 files**: 90 audited book chapters + `vault/sql/` + `vault/python/` + `vault/shared/`.

---

## ⚠️ Non-negotiable methodology

1. **The mapping is measured; the prose is yours.** Chapter lists come from `_digest.generated.txt`.
   Never invent a chapter that isn't in the digest.
2. **No-Guess Rule applies.** Do not assert page numbers or detailed chapter content you have not
   read. Describe the *angle* at a confidence level the link lets the reader verify. It is fine to
   be general; it is not fine to be specifically wrong.
3. **Hit count ≠ relevance.** Verify sense before claiming coverage (see collisions below).
4. **Low-hit sources may be noise.** Example: `fundamentals_de` scored 1 hit for Deduplication —
   that is *not* substantive coverage and was deliberately omitted from the dedup hub. Apply the
   same judgement elsewhere.

---

## ⚠️ Confirmed term-sense collisions — never fuse these

Verified by grepping actual context, not assumed:

| Term | Distinct senses found |
|---|---|
| **partition** | Kimball = physical table partitioning · DDIA Ch.6 = distributed sharding · SQL = `PARTITION BY` window clause · Kafka partitions · plain English ("type 2 responses perfectly partition history") |
| **transaction** | Kimball = *fact-table grain type* ("transaction, periodic snapshot, accumulating snapshot") · DDIA Ch.7 = ACID transaction |
| **window** | SQL `OVER(PARTITION BY …)` · Streaming Systems = event-time bucketing |
| **watermark** | `lakehouse-map.md` = `MAX(timestamp)` incremental-load bookmark · Streaming Systems Ch.3 = input-completeness metric |

Each affected hub **must** carry a *Same word, different meaning* block. Fusing these would
actively teach something false — this is the single biggest quality risk in the whole build.

---

## Two concepts needing MANUAL sourcing (pattern bias, not genuinely narrow)

The generator flagged these as single-source, but that is **vocabulary bias in the search
patterns**, not reality. Do not demote them — source them by hand.

- **Medallion / Layered Architecture** — 579 hits but all in `databricks_big_book_4e`, because
  Bronze/Silver/Gold is Databricks vocabulary. The *concept* also appears as staging layers in
  Kimball ETL chapters and architecture layering in `fundamentals_de`. Widen manually.
- **Streams & Tables Duality** — matched only `streaming_systems` on literal phrasing, but DDIA
  Ch.11 covers the same duality in different words. Widen manually.

---

## Worklist — 32 cross-cutting concepts

Ordered by measured cross-book spread. `deduplication` is **done**.

### 6/6 sources
`data-quality` · `partitioning-and-clustering` ⚠️ · `checkpointing-and-recovery` ·
`transactions-and-consistency` ⚠️ · ~~`deduplication`~~ ✅ · `orchestration-and-dependencies` ·
`keys-surrogate-natural` · `lineage-and-governance` · `backfill-and-reprocessing` ·
`testing-and-validation`

### 5/6 sources
`file-layout-and-compaction` · `idempotency-and-exactly-once` · `security-and-access-control` ·
`replication-and-distribution` · `ingestion-patterns` · `change-data-capture` ·
`batch-vs-streaming` · `event-time-vs-processing-time` · `schema-evolution`

### 4/6 sources
`aggregation-and-combiners` · `incremental-vs-full-recompute` · `sql-window-functions` ⚠️ ·
`materialized-views`

### 3/6 sources
`slowly-changing-dimensions` · `dimensional-modeling` · `watermarks` ⚠️ · `joins` ·
`windowing-event-time` ⚠️ · `serverless-and-compute` · `late-data` · `cost-management` ·
`state-management`

### Manual widening required
`medallion-layering` · `streams-and-tables`

⚠️ = carries a known term-sense collision; disambiguation block is mandatory.

---

## After the hubs: Layer 0 retrofit + Layer 2 bridges

**Layer 0 — §9 wikilink retrofit (do LAST).**
- Edit **only** the `## 9. Cross-references` section of the 90 notes under
  `Data engineering Book knowledge/notes/`. Convert intra-book prose refs to `[[wikilinks]]`.
- Touch nothing in §1–§8, no page numbers, no quotes.
- **Test on one file first**, then run the gate:
  `python tools/verify_citations.py <file>` → expect no `^FAIL`
- After the batch, run the full gate from the book dir and require `13/13 checks passed` /
  `VERIFY_ALL: PASS`:
  `python tools/verify_all.py` (runs long — background it)

### 🔴 Rollback — REQUIRED before the retrofit

**Verified risk:** `git ls-files "Data engineering Book knowledge/"` returns **0**. The entire
90-note corpus is **untracked**. `git checkout` cannot restore it. There is currently no safety
net for a batch edit across all 90 files.

Before touching any note, do **one** of these:

```bash
# Option A (preferred) — commit the corpus first, so git can restore it
git add "Data engineering Book knowledge/" && git commit -m "Snapshot 90 gate-verified notes before §9 retrofit"

# Option B — plain filesystem snapshot
cp -r "Data engineering Book knowledge/notes" "Data engineering Book knowledge/notes.pre-retrofit.bak"
```

Rollback if `verify_all.py` fails after the batch: restore from the commit/backup, re-run
`verify_all.py` to confirm `13/13`, then retry on a smaller batch.

**Layer 2 — bridges.**
- Populate the **already-existing, currently empty** `vault/shared/glossary.md`
  (format is already declared in its header: `Term | Track | Definition | Note file`).
- Extend the **already-existing** `vault/shared/lakehouse-map.md` with new concept→layer rows.
- Do **not** create a competing glossary system.

---

## 🚫 Hard scope boundaries

- **Never** place a `.md` file under `Data engineering Book knowledge/notes/` —
  `build_full.py` globs `notes/**/*.md` recursively **and asserts no orphans**. A stray file
  breaks the build or silently pollutes `MASTER_CONTEXT_FULL.md`.
- **Never** touch `vault/DE-Mastery/` — user-owned, session-read-only per `CLAUDE.md`.
- **Never** edit §1–§8 of any gate-verified chapter note.
- **Never** rewrite `MASTER_CONTEXT.md` by hand — it is generated.
- English on disk, always (per `_rules/heart.md`).
