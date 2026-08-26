# Master Roadmap — Foundation → Project

> **Purpose.** The big-picture map of the whole learning journey, end to end. The vault
> (`sql/`, `python/`) teaches the foundation. The three repo-map files
> (`PATTERN_LIBRARY.md`, `PROJECT_TECHNICAL_MAP.md`, `LEARNING_PATH.md`) document the
> destination — the 10 built repos. This file is the road *between* them: it names every
> tier, in order, so at any point you know where you are, what's next, and what you can't
> touch yet.
>
> **Golden rule of this roadmap:** each tier uses only what a lower tier already taught.
> Never jump a tier. Copying repo code you can't defend is the single worst interview risk.
>
> Last verified against vault + repo-map: 2026-08-19 (full local clone walk of all 10 repos).

---

## The 4 tiers at a glance

```
TIER 1  FOUNDATION            SQL M0–M9  +  Python Ch2–12          ← YOU ARE HERE (SQL M0)
   │    (vault: sql/, python/)                                        finish this fully first
   ▼
TIER 2  DIMENSIONAL MODELING  Kimball star schema, SCD2 concept    ← SQL-native, no new engine
   │    (Pattern 14, Pattern 4 as concepts)
   ▼
TIER 3  DE CORE               Cloud storage → PySpark → Delta →     ← THE MISSING MIDDLE
   │    (the bridge, 7 skills) Medallion → dbt → GE → Airflow          nothing of this in vault yet
   ▼
TIER 4  PROJECT REBUILD       home-credit → paysim → olist → …      ← build order in LEARNING_PATH.md
        (the 10 repos)         … → banking capstone (LAST)             banking is the finish line
```

The practice ladder (HackerRank 30 easy → LeetCode 50) runs as a **parallel fluency rail**
alongside Tier 1–2 — it builds SQL speed, it is not a tier of its own.

---

## Tier 1 — Foundation (current)

**Where it lives:** `sql/notes/`, `sql/quiz/`, `python/notes/`, `python/quiz/`
**Status:** SQL M0 not started (bootcamp video YimMzb0mHkI). Python Ch2–3 done.

SQL modules M0–M9 and Python chapters Ch2–12 as already scaffolded in `_rules/goal.md`.
No change to that plan — it is sound. Two things worth knowing about how it feeds upward:

- **SQL M9 (Platform SQL — external table, Spark SQL, dbt/Jinja) is the hinge into Tier 3.**
  It is the one foundation module that already reaches into DE-core territory. Treat it as
  the handshake between tiers, not just the last SQL module.
- **SQL M7 (DE Real-Time Scenarios) previews Tier 2–3** — dedup, incremental, nth-value.
  Those are the same techniques Pattern 8 and Pattern 13 implement in the repos.

**Exit gate (Tier 1 → Tier 2):** SQL M9 done + Python Ch12 done, quiz scores consistently
≥70%. Any module flagged <70% in `progress-tracker.md` gets revisited before you move.

---

## Tier 2 — Dimensional modeling (Kimball)

**New skill, no new tool** — this is pure SQL thinking, which is why it sits right after Tier 1.

What to learn: fact vs dimension, **grain** (the one hardest idea — one row means what,
exactly), surrogate key vs business/natural key, star schema, SCD **Type 2** as a concept
(preserve history, don't overwrite), and the **bridge table** for genuine many-to-many.

**Maps to:** Pattern 14 (star schema + bridge) and Pattern 4 (SCD2) in `PATTERN_LIBRARY.md`.
Every repo's Gold layer is built on this. `home-credit-pipeline`'s `fact_loan_application.sql`
and `banking`'s `bridge_customer_account.py` are the concrete examples — but you learn the
*concept* here first, engine-free.

**Already in the vault:** `shared/lakehouse-map.md` is a working head-start on this tier —
it already maps SQL concepts (surrogate key, PARTITION BY window, dedup) to medallion layers.
Extend it as you go.

**Exit gate:** you can design a star schema for a messy business requirement on a whiteboard —
name the fact grain, the dimensions, the surrogate keys — without looking anything up.

---

## Tier 3 — DE core (the missing middle)

**This is the tier that does not exist in the vault yet, and the reason the structure felt
incomplete.** Seven skills, in dependency order — each one needs the one before it. Learn
them in this order; do not shuffle.

| # | Skill | What it is | Repos that use it | Pattern |
|---|-------|-----------|-------------------|---------|
| 1 | **Cloud storage + Parquet** | Data lake concept, columnar format, S3 / ADLS Gen2 / OneLake | all 10 | 1 |
| 2 | **PySpark (DataFrame API)** | The compute engine — the biggest single skill here | home-credit, olist, paysim, banking, migration_fiber, migration_creative | — |
| 3 | **Delta Lake** | ACID on the lake — MERGE upsert, time travel | olist, paysim, banking, home-credit | 5, 4, 13 |
| 4 | **Medallion architecture** | Bronze→Silver→Gold as the organizing principle | 7 of 10 | 1 |
| 5 | **dbt** | SQL transformation framework — staging→intermediate→mart, tests, multi-target | home-credit, paysim, olist, pharma, creative, banking | 6, 7 |
| 6 | **Great Expectations** | Data-quality gates per layer, WARN vs hard-fail | home-credit, olist, paysim, pharma, volve | 7 |
| 7 | **Airflow** | Orchestration — tie every step into one pipeline | nearly all | 15 |

**Why this exact order.** You cannot understand Pattern 5 (Delta MERGE for SCD2) before you
(a) understand SCD2 as a concept — Tier 2, and (b) know PySpark + Delta — skills 2–3 here.
dbt (skill 5) is SQL-based, so it slots in naturally once your SQL is strong. Airflow (skill 7)
comes last because it orchestrates everything the earlier skills produce — orchestrating
nothing teaches nothing.

**Platforms are picked up *inside* skills 2–7, not studied separately:** AWS Glue
(home-credit), Databricks (paysim, olist, volve, banking), Microsoft Fabric (the two migration
repos), Snowflake serving (most), DuckDB as $0 dev target (pharma, creative).

**Supporting ops skills** (learn just-in-time, not as a blocking tier): Docker (local dev
stacks), GitHub Actions CI/CD (most repos), Terraform (**banking only** — the single repo with
IaC, so defer it until the capstone).

**The one non-Spark case — know it, don't let it confuse the order.**
`Volve-Sensor-Production-Analytics-Pipeline` runs medallion patterns in **SQL over a Databricks
SQL Warehouse, zero PySpark**, by a documented cost decision (its ADR-002). Study Volve for
*"when NOT to reach for Spark"* — after you know Spark, so you understand what it's choosing
against.

**Exit gate (Tier 3 → Tier 4):** you can, on a blank machine, stand up a tiny Bronze→Silver→Gold
Delta pipeline in PySpark, gate it with one GE check, and trigger it from one Airflow DAG —
from scratch, no repo open.

---

## Tier 4 — Project rebuild (the 10 repos)

Now, and only now, the destination. **Follow the exact build order in `LEARNING_PATH.md`** —
it is ordered so each repo assumes only patterns an earlier repo taught:

```
Tier 0  home-credit-pipeline      (1 ADR — simplest, START HERE)
        paysim-fraud-pipeline     (1 ADR — adds hybrid PySpark+dbt, Delta MERGE)
Tier 1  olist-ecommerce-pipeline  (2 ADRs — SCD2 as real DeltaTable.merge())
Tier 2  migration_fiber_home_credit_risk  (13 ADRs — study the diff vs home-credit)
Tier 3  pharma_novartis_sttm      (10 ADRs + 62-card cheatsheet — read it directly)
Tier 4  creative_intelligence_lab (13 ADRs — your real EZCOM work, GenAI ETL)
        migration_creative_intelligence_lab  (8 ADRs — the Fabric diff)
Tier 5  Volve-Sensor…-Pipeline    (7 inline ADRs — the SQL-only, no-Spark case)
Tier 6  banking-multisource-lakehouse  (+ airflow-dag)  ← CAPSTONE, LAST
```

**⚠ banking is the finish line, not the entry.** It is the résumé headline, so the instinct is
to start there. Don't. It assumes 5-source extraction (Pattern 2), MDM at scale (Pattern 3),
Terraform, and the two-repo control-plane/data-plane split (Pattern 15) — every one of which
only makes sense after the earlier tiers. `LEARNING_PATH.md` says it explicitly: *study this
last.*

**If time is short**, the three highest-value repos are `banking` (+ its airflow-dag),
`migration_fiber_home_credit_risk`, and `pharma_novartis_sttm` — together 14 of the 17 patterns.
But "short path" still means after Tier 3, not instead of it.

---

## How the three repo-map files fit

They are the **answer key for Tier 3–4**, not reading for Tier 1–2:

- **`PATTERN_LIBRARY.md`** — the 17 techniques, each with a "junior mistake → why it bites"
  frame. Read a pattern the moment Tier 3 or 4 introduces it, not before.
- **`PROJECT_TECHNICAL_MAP.md`** — every file in every repo. Your lookup when rebuilding, so no
  file is a mystery you'd have to reverse-engineer in an interview.
- **`LEARNING_PATH.md`** — the build order above, plus the honest gap list (banking's MDM overlap
  is manufactured; Volve has zero tests; pharma's "SLA Gym" DAGs are self-authored drills). Know
  those caveats before an interview surfaces them.

---

## Alignment notes — what was checked, what to correct

Verified this roadmap against the live vault. Findings:

1. **`_rules/goal.md` "Future tracks" points at banking as the lakehouse entry ("Phase 1–6").**
   Misaligned with the build order — banking is the **capstone (Tier 4 last)**, not the start.
   This roadmap supersedes that line. (goal.md is append-only, so it's left as-is; treat *this*
   file as the authority on sequencing.)
2. **`_rules/heart.md` DE-mapping cites only `banking-multisource-lakehouse` as the reference
   project.** Same issue — fine as a *concept* illustration, but the rebuild path starts at
   `home-credit-pipeline`. No edit needed; just don't read heart.md's single reference as the
   starting repo.
3. **Tier 3 (DE core) is entirely absent from the vault as a track** — confirmed. goal.md jumps
   straight from SQL/Python to "Lakehouse: banking." That gap is exactly what this roadmap fills.
   When Tier 1 nears completion, scaffold a `de-core/` track mirroring the `sql/` layout.
4. **Python foundation ≠ DE-Python.** The bootcamp (Ch2–12) is general Python. The repos lean on
   **pandas, PySpark Python API, boto3, requests, datetime, logging, pathlib** — the same "gap
   topics" already flagged in `python/master-doc.md`. Fold these into Tier 3 skill 2, or a short
   Python-for-DE add-on after Ch12. Not a foundation blocker; a Tier-3 prerequisite.
5. **`shared/dialect-map.md` has no DuckDB row.** DuckDB is the $0 dev target in `pharma` and
   `creative_intelligence_lab`. Minor — add a DuckDB column when you reach Tier 3 skill 5 (dbt).
6. **Oracle correctly absent.** Genuine gap per résumé strategy; the dialect map already carries
   the bridge dialects (PostgreSQL, MS SQL Server / T-SQL, MySQL, Teradata, Snowflake). Aligned —
   leave Oracle out.

**Net:** foundation (Tier 1–2) is well-built and correctly sequenced. The only structural hole
was Tier 3, plus the "banking = start" mislabel. Both are addressed here.

---

## Sequencing decision (locked)

Per your call: **finish foundation fully before DE core.** SQL M0–M9 + Python Ch2–12 complete,
quizzes ≥70%, *then* open Tier 2, *then* Tier 3, *then* Tier 4. No parallel DE-core track while
SQL is still in progress. This file is the map; the immediate next action never changes until a
tier's exit gate is met — right now that's simply: continue SQL M0 on the bootcamp video.

---

## GitHub verification (2026-08-19, full local clone walk)

All 10 repos were cloned locally and walked directory-by-directory — ADR counts, file inventory,
and the key line citations checked against ground truth (not the earlier raw-file spot-check pass).

**Confirmed true (ground truth):**
- All 10 repos exist, are public, and match their described architecture.
- Banking: 4-layer medallion (Landing→Bronze→Silver→Gold), Databricks + Delta + Unity Catalog,
  Snowflake serving, and **5 real extractors** in `pipeline/extract/` — `postgres_extract.py`,
  `mssql_extract.py`, `teradata_extract.py`, `salesforce_extract.py`, `obp_client.py`.
- `migration_fiber` ADR-008 = `ADR-008-retire-dbt-warehouse-tsql.md` — the dbt-retirement story
  (Pattern 4 correction) is real.
- olist SCD2 via `DeltaTable.merge()` — confirmed at `transform_silver.py:307-321` (customers) and
  `426-437` (sellers), with `is_current`/`valid_to` expiry exactly as described. Line citation accurate.
- pharma **62-card cheatsheet — confirmed.** `cheatsheets/optimization/00_INDEX.md:47` states
  "Layer cards total: 62 across layers 01–09" (+100 orchestration techniques).
- Volve **7 inline ADRs, 0 tests — confirmed.** ADR-001–007 live as sections in
  `docs/ARCHITECTURE.md §6`; `tests/` holds only a placeholder `HOW_IT_WORKS.txt`, no real tests.
- ADR counts that match: creative = 13 (ADR-001–013), migration_creative = 8, home-credit = 1,
  paysim = 1.

**Corrected (repo-map numbers were wrong — fix before an interview):**
- **Banking ADR count.** `LEARNING_PATH.md` says **13**; actual is **12** (`governance/ADR/` holds
  ADR-000 through ADR-011, plus a template). Off by one.
- **`migration_fiber` ADR count.** `LEARNING_PATH.md` says **14 ("deepest ADR trail")**; actual is
  **13** (ADR-001–013, with a duplicate ADR-004 number). The **14 is wrong** — but the "deepest
  trail" ranking still holds: 13 is tied-deepest with creative (also 13); banking sits behind at 12.
- **Banking source count.** Repo-map's "4 heterogeneous sources / 4-way split" is wrong — there are
  **5 sources / 5 extractors**. Defensible framing: **5 sources, 4 distinct extraction patterns**
  (Postgres + MSSQL both use watermark). Never say "4 sources."

**Counting caveats (convention, not error):**
- olist "2 ADRs" = 1 real ADR (ADR-001) + 1 template file. pharma "10 ADRs" = 9 ADR documents
  (ADR-001–007, with 005 and 006 each reused for a second decision) + 1 template. Both are defensible
  if you count the template — but say the real number in an interview.
- **Client naming.** pharma README frames it as **"Helvetia Pharma,"** not Novartis (folder is
  `pharma_novartis_sttm`). Cosmetic, but don't state the wrong client name.

**Verdict.** After the full local walk, the repo-map is **more accurate than the earlier raw-file
pass suggested** — pharma's 62 cards, Volve's 7 inline ADRs, creative's 13 ADRs, and the olist line
citation are all correct (an earlier check hit a stale local clone of creative and misread it as 5).
Only three hard number errors survive: **banking = 12 ADRs (not 13)**, **migration_fiber = 13 (not
14)**, and the **5-not-4 banking source count**. Fix those three and the map is interview-safe.
