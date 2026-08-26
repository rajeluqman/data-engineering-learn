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
6. Write notes → `sql/notes/MX-topic.md` (append)
7. Write quiz → `sql/quiz/MX-topic-quiz.md` (new file per topic)
8. Write problems → `sql/problems/MX-topic-problems.md` (append)
9. Update `state/progress-sql.md` — module status, scores, weak spots

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
