# SPEC — Multi-Session Refactor (executable)

> **For the executing session (Sonnet).** This is a one-time refactor of the vault so it can be
> driven by several small, focused sessions (one for SQL, one for Python, etc.) without the sessions
> clobbering each other, and without any session having to load the whole vault. Follow the steps in
> order. Do not improvise structure — everything you need is specified here.
>
> **Author:** planning session, 2026-08-19. **Status:** ready to execute.

---

## 1. Why this refactor (the goal, in one line)

The user wants to split learning across separate sessions to **save tokens**. That only works if
(a) each session loads a *small* startup context, and (b) sessions can't overwrite each other's
files. This refactor delivers both: a tiny **router** for lean startup, and **write-partitioning by
track** so collisions are structurally impossible.

## 2. Verified storage facts (do not re-litigate)

- The cloud workspace (`/home/claude/…`) is **per-session and ephemeral** — never shared. It is
  scratch only.
- The disk vault (`D:\Obsidian\Data Engineering Learn\vault\`) is the **single source of truth**,
  reachable read/write by any session via the device bridge. All shared state lives here.
- The Claude-native "project" layer is **not used** — the `project_write` tool is not available in
  this environment, and even if it were it would fork state away from Obsidian. Ignore it.
- `device_commit_files` has an **mtime guard**: if a file changed on disk since it was staged, the
  commit is rejected unless `force=true`. Partitioned writes mean this rejection never fires in
  normal use — see the hard rules.

## 3. Target structure

### 3.1 Ownership table (this is the contract)

| File / folder | Who READS it | Who WRITES it |
|---|---|---|
| `00_INDEX.md` (new) | every session, first | Maintenance only |
| `01_MASTER-ROADMAP.md` | Maintenance / planning only | Maintenance only |
| `_rules/heart.md`, `_rules/goal.md` | every session (start ritual) | Maintenance only |
| `shared/dialect-map.md`, `shared/lakehouse-map.md` | any (reference) | Maintenance only |
| `shared/glossary.md`, `shared/errors-gotchas.md` | any | **append-only**, any (tag entries) |
| `state/session-log.md` | any | **append-only**, any |
| `sql/**` | SQL session | **SQL session only** |
| `python/**` | Python session | **Python session only** |
| `state/progress-sql.md` (new), `state/handoff-sql.md` (new) | SQL session | SQL session only |
| `state/progress-python.md` (new), `state/handoff-python.md` (new) | Python session | Python session only |
| `shared/qna-sql.md` (new), `shared/qna-python.md` (new) | its track | its track only |

Key property: **the SQL write-set and the Python write-set do not overlap.** Two sessions can run at
the same time and never touch the same file.

### 3.2 Lean startup read-set (the token saving)

- **SQL learning session** reads on startup, and nothing more: `00_INDEX.md` →
  `state/handoff-sql.md` → `state/progress-sql.md` → `_rules/heart.md` → the one current
  `sql/notes/MX-*.md` it is working on.
- **Python learning session**: the mirror image with `python/` files.
- **Do NOT** load `01_MASTER-ROADMAP.md`, the repo-map files (`Repo learning/`), or the other
  track's files in a learning session. Those are Tier-3/4 reference — loading them defeats the whole
  point.

## 4. Execution steps

### Step 1 — Create the router `00_INDEX.md` at vault root

Content:

```md
# 00_INDEX — Session Router (read me first)

> Tiny entry point. Every session reads THIS first, then loads ONLY its track's files.
> Small context per session = saved tokens. Do not load the roadmap or repo-map in a learning session.

## Pick your track

| Session for… | Read to start (only these) | May write (only these) |
|---|---|---|
| **SQL** | `state/handoff-sql.md`, `state/progress-sql.md`, `_rules/heart.md` | `sql/**`, `state/handoff-sql.md`, `state/progress-sql.md`, `shared/qna-sql.md` |
| **Python** | `state/handoff-python.md`, `state/progress-python.md`, `_rules/heart.md` | `python/**`, `state/handoff-python.md`, `state/progress-python.md`, `shared/qna-python.md` |
| **Maintenance / planning** | `01_MASTER-ROADMAP.md`, `_rules/goal.md`, this file | reference files (roadmap, rules, dialect-map, lakehouse-map) |

## Shared — APPEND-ONLY (any session appends, never rewrites; tag each entry [SQL] / [PY])
- `state/session-log.md` — one row per session
- `shared/glossary.md`, `shared/errors-gotchas.md`

## Read-only reference (only a Maintenance session edits these)
- `01_MASTER-ROADMAP.md`, `_rules/heart.md`, `_rules/goal.md`
- `shared/dialect-map.md`, `shared/lakehouse-map.md`
- repo-map files under `Repo learning/`

## Hard rules
1. Never commit a shared/append-only file with `force=true`. On an mtime reject → re-stage, re-read, re-append.
2. A learning session writes ONLY its own track's files (see table). Never the other track's.
3. Sequential is safest. Parallel SQL + Python is safe because their write-sets don't overlap.
```

### Step 2 — Split `state/progress-tracker.md` into per-track files

- Create `state/progress-sql.md` — move the **SQL Modules** table (M0–M9) into it, verbatim, under a
  `# Progress — SQL` heading with a `Last updated:` line.
- Create `state/progress-python.md` — move the **Python Chapters** table (Ch 2–12) **and** the
  **HackerRank / LeetCode** table into it, under `# Progress — Python`.
- Do **not** delete `state/progress-tracker.md` (append-only culture). Instead replace its body with a
  freeze header:
  ```md
  # Progress Tracker — FROZEN (split 2026-08-19)
  > This file is retired. Live progress now lives per-track:
  > - SQL → `state/progress-sql.md`
  > - Python → `state/progress-python.md`
  ```

### Step 3 — Split `state/handoff.md` into per-track files

- Create `state/handoff-sql.md` — the SQL slice of the current handoff (SQL M0 not started; exact next
  step = start SQL Module 0 Orientation; blockers none). Keep the same section shape
  (`Last session` / `Current position` / `Exact next step` / `Blockers`).
- Create `state/handoff-python.md` — the Python slice (Ch 3 done, Ch 4 String Formatting next).
- Freeze `state/handoff.md` with a pointer header (same pattern as Step 2).

### Step 4 — Create per-track Q&A logs

- Create `shared/qna-sql.md` and `shared/qna-python.md`, each with an append-only header:
  ```md
  # Q&A Log — SQL (append-only)
  | Date | Topic | Question | Answer summary |
  |------|-------|----------|----------------|
  ```
- If `shared/qna-log.md` already exists, freeze it with a pointer header (do not delete). If it does
  not exist, ignore — heart.md references it but it may never have been created.

### Step 5 — Update the session ritual in `_rules/heart.md`

Replace the **`## Session ritual`** section (only that section) with the version below. Leave every
other section of heart.md untouched.

```md
## Session ritual (multi-session model)

> Each session is single-track. Read your track's files only — see `00_INDEX.md`.

### Start of every session
1. Read `00_INDEX.md` → confirm which track this session is.
2. Read `state/handoff-<track>.md` and `state/progress-<track>.md`.
3. Read this file (`_rules/heart.md`).
4. Confirm to user: "track: [SQL/Python], last: [X], next: [Y]".
   Do NOT load the roadmap, repo-map, or the other track's files.

### Per topic
(unchanged — see the per-track flows below)

### End of every session
1. Update `state/progress-<track>.md` — status, scores, weak spots.
2. Rewrite `state/handoff-<track>.md` — where we stopped, exact next step.
3. Append one row to `state/session-log.md` (shared, append-only).
4. Append new Q&A to `shared/qna-<track>.md`.

### Write discipline (all sessions)
- Write ONLY your track's files (`00_INDEX.md` ownership table is the authority).
- Never `force=true` on a shared/append-only file. On mtime reject → re-stage, re-read, re-append.
```

Also update the two "Write notes/quiz/problems" ritual references so they point at the per-track
progress/handoff names instead of `progress-tracker.md` / `handoff.md`.

### Step 6 — Update `00_START-HERE.md`

Change its load-order section to point at `00_INDEX.md` as the true first read, and note that
`state/progress-tracker.md` / `state/handoff.md` are frozen and replaced by per-track files. Keep the
big-picture pointer to `01_MASTER-ROADMAP.md`.

## 5. Acceptance checklist (verify before finishing)

- [ ] `00_INDEX.md` exists at vault root with the ownership table and hard rules.
- [ ] `state/progress-sql.md` + `state/progress-python.md` exist; old tracker frozen with pointer.
- [ ] `state/handoff-sql.md` + `state/handoff-python.md` exist; old handoff frozen with pointer.
- [ ] `shared/qna-sql.md` + `shared/qna-python.md` exist.
- [ ] `_rules/heart.md` ritual section updated to per-track + no-`force` rule; rest of file unchanged.
- [ ] `00_START-HERE.md` points at `00_INDEX.md` first.
- [ ] No file was deleted — retired files are frozen with a pointer header (append-only culture kept).
- [ ] Every new/edited file committed to the disk vault (`device_commit_files`, **no** `force=true`).
- [ ] Spot-check: the SQL write-set and Python write-set in the ownership table share zero files.

## 6. The three rules that make it work (restate to user at the end)

1. **Lean read** — each session loads only its track's handoff + progress + heart + current note.
   Roadmap/repo-map are reference, never auto-loaded.
2. **Partitioned write** — a session writes only its own track's files; shared logs are append-only.
3. **No `force=true` on shared files** — on an mtime reject, re-stage and re-append; never overwrite.
