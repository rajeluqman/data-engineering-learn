# Heart — Operating Rules

## Language

- All course CONTENT (notes, quiz, explanations, problems): **English**
- Technical nouns always English (query, schema, pipeline, table, column, etc.)
- Chat with user: **Bahasa Malaysia casual** (lah, je, kan, tu, ni)
- Switch to fuller BM with school-level analogies ONLY when user says
  something is hard to understand. Return to English after.

## Doc conventions

- A = glossary (`shared/glossary.md`)
- B = notes (`sql/notes/` or `python/notes/`)
- C = Q&A log (`shared/qna-<track>.md`)
- D = quiz bank (`sql/quiz/` or `python/quiz/`)
- **APPEND-ONLY** — never overwrite or delete existing content. Only add.

## Session ritual (multi-session model)

> Each session is single-track. Read your track's files only — see `00_INDEX.md`.

### Start of every session
1. Read `00_INDEX.md` → confirm which track this session is.
2. Read `state/handoff-<track>.md` and `state/progress-<track>.md`.
3. Read this file (`_rules/heart.md`).
4. Confirm to user: "track: [SQL/Python], last: [X], next: [Y]".
   Do NOT load the roadmap, repo-map, or the other track's files.

### Per topic (SQL)
1. Teach concept — anchor on ANSI SQL, tag dialect differences
2. Quiz — 3-tier MCQ (user runs in Chat tab, not Cowork)
3. One DE problem (pipeline / dedup / incremental / lakehouse context)
4. One DA problem (business requirement messy → convert to SQL)
5. One hack/pitfall
6. Write notes → `sql/notes/MX-topic.md` (append), shaped per `_rules/topic-template.md`'s
   7 sections
7. Write quiz → `sql/quiz/MX-topic-quiz.md` (new file per topic)
8. Write problems → `sql/problems/MX-topic-problems.md` (append)
9. Update `state/progress-sql.md` — module status (per the Definition of Done below, never on
   feel), scores, weak spots

### Per topic (Python)
- Same flow, files go to `python/` equivalents
- Quiz per topic (not per chapter) — Ch 8 splits into 2 quizzes; Ch 1 skip
- Update `state/progress-python.md` — chapter status, scores, weak spots

### End of every session
1. Update `state/progress-<track>.md` — status, scores, weak spots.
2. Rewrite `state/handoff-<track>.md` — where we stopped, exact next step.
3. Append one row to `state/session-log.md` (shared, append-only).
4. Append new Q&A to `shared/qna-<track>.md`.

### Write discipline (all sessions)
- Write ONLY your track's files (`00_INDEX.md` ownership table is the authority).
- Never `force=true` on a shared/append-only file. On mtime reject → re-stage, re-read, re-append.

## Quiz rules

- Format: interactive MCQ, 4 options, instant feedback, score counter
- User runs quiz in **Chat tab** (widget), not Cowork
- Store each quiz as `.md` in `sql/quiz/` or `python/quiz/`
- Also store as `.html` in `sql/quiz/html/` using `_rules/quiz-template.html`
- Question types: predict-the-output, spot-the-bug, fill-in-the-blank,
  trace-the-state
- Last question every quiz = write-it-yourself (user types code, Claude reviews)
- 3-tier difficulty per quiz:
  - Tier 1: Recall / fundamental
  - Tier 2: Applied DE/DA scenario
  - Tier 3: Senior / interview curveball
- Checkpoint quiz every 3–4 modules (stored in `sql/quiz/checkpoints/`)
- Adaptive: if score < 70%, flag weak spot in progress-tracker, revisit before next module

## Definition of Done — when a module/chapter/course actually flips to ✅

A topic's status becomes ✅ only when **all three** gates pass. Any one alone is gameable —
each catches a different failure mode:

1. **Teach-back** — user explains the concept in their own words, no notes open. Catches
   "I recognise it but can't produce it."
2. **Quiz ≥ 80%** (8/10) — a higher bar than the 70% remedial-flag above. That gap (70–79%) is
   deliberate: it means "not failing, not done yet — keep drilling," not the same thing as
   "complete." Catches gaps across the topic's surface, not just the parts practiced.
3. **≥ 3 coding/practice exercises completed** — catches "I understand it but can't type it,"
   the exact gap `.claude/skills/cikgu/SKILL.md`'s Plan-in-Comments-Then-Fill method exists
   to bridge.

Track progress per gate as counters in `state/progress-<track>.md` (teach-back ☐/✅, quiz score,
exercises n/3) — not as a single status word. The status column only ever shows ✅ once all
three read done.

**Honesty limit:** quiz scores are self-reported — quizzes render as `.md`/`.html` and are taken
outside the session, so a session cannot verify a score it wasn't told. This gate is an honesty
contract, same family as `DE-Mastery/Interview-Prep/integrity-rules.md` — don't claim a gate
passed without it actually having happened.

**Existing modules marked ✅ before this rule existed** (e.g. SQL M0) keep their status but are
tagged `(pre-DoD)` in `progress-sql.md` — not silently re-opened, not silently laundered into a
gated pass either. Re-gating them is the user's call, not automatic.

## SQL dialect rules

- Anchor: ANSI SQL
- Tag differences for: MySQL · MS SQL Server · PostgreSQL · Snowflake · Teradata · Spark SQL
- Flag `QUALIFY` (Snowflake) where it replaces subquery
- Flag `TOP` (MSSQL) vs `LIMIT` (MySQL/PostgreSQL)
- Flag `FULL JOIN` not supported in MySQL (use UNION workaround)

## DE mapping (connect SQL concepts to lakehouse)

- Dedup → Silver layer (ROW_NUMBER + PARTITION BY key)
- SCD Type 1 / MERGE → Gold layer
- Watermark → incremental load pattern
- Surrogate key → auto-increment ID in Gold dimension table
- Reference project: rajeluqman/banking-multisource-lakehouse (medallion architecture)

## Python rules

- Video: YouTube ZvU7lupoXQE (5h 27m, 12 chapters)
- Master doc synced from Google Docs ID: 1tke_GvXJX9klF1o-kzom0yj60_p-dRhjeZ8g_t3VkCU
- Quiz per TOPIC not per chapter
- Ch 1 skip, Ch 8 splits into 2 quizzes
- Progress tracked in `state/progress-python.md`
