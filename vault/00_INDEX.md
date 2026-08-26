# 00_INDEX — Session Router (read me first)

> Tiny entry point. Every session reads THIS first, then loads ONLY its track's files.
> Small context per session = saved tokens. Do not load the roadmap or repo-map in a learning session.

## Pick your track

| Session for… | Read to start (only these) | May write (only these) |
|---|---|---|
| **SQL** | `state/handoff-sql.md`, `state/progress-sql.md`, `_rules/heart.md` | `sql/**`, `state/handoff-sql.md`, `state/progress-sql.md`, `shared/qna-sql.md` |
| **Python** | `state/handoff-python.md`, `state/progress-python.md`, `_rules/heart.md` | `python/**`, `state/handoff-python.md`, `state/progress-python.md`, `shared/qna-python.md` |
| **Power BI** | `state/handoff-powerbi.md`, `state/progress-powerbi.md`, `_rules/heart.md` | `Microsoft Power BI Developer and Architect/**`, `state/handoff-powerbi.md`, `state/progress-powerbi.md`, `shared/qna-powerbi.md` |
| **Maintenance / planning** | `01_MASTER-ROADMAP.md`, `_rules/goal.md`, this file | reference files (roadmap, rules, dialect-map, lakehouse-map), root `CLAUDE.md`, `.claude/**` |

> Teaching pedagogy for any track lives in the `cikgu` skill (`.claude/skills/cikgu/SKILL.md`).
> Invoke it with `/cikgu`. It reads this table — it never overrides it.

## Shared — APPEND-ONLY (any session appends, never rewrites; tag each entry [SQL] / [PY] / [PBI])
- `state/session-log.md` — one row per session
- `shared/glossary.md`, `shared/errors-gotchas.md`

## Read-only reference (only a Maintenance session edits these)
- `01_MASTER-ROADMAP.md`, `_rules/heart.md`, `_rules/goal.md`, `_rules/topic-template.md`
- `shared/dialect-map.md`, `shared/lakehouse-map.md`
- `shared/gym-and-troubleshooting-doctrine.md` — dormant until Tier 3 (see roadmap)
- repo-map files under `Repo learning/`

## User-only — no session writes here, ever
- `DE-Mastery/**` — per `DE-Mastery/MASTER_CONTEXT.md`, Raja Luqman updates these himself.
  Sessions may READ them (especially `Interview-Prep/` before any resume/interview claim).

## Frozen — do not write, do not read for status
- `00_START-HERE.md`, `state/handoff.md`, `state/progress-tracker.md`

## Hard rules
1. Never commit a shared/append-only file with `force=true`. On an mtime reject → re-stage, re-read, re-append.
2. A learning session writes ONLY its own track's files (see table). Never another track's.
3. Sequential is safest. Parallel tracks are safe because their write-sets don't overlap.
4. A module's status flips to ✅ only when the Definition of Done in `_rules/heart.md` is met — all three gates.
