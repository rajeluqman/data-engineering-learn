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
