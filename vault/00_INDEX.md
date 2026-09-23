# 00_INDEX — Session Router (read me first)

> Tiny entry point. Every session reads THIS first, then loads ONLY its track's files.
> Small context per session = saved tokens. Do not load the roadmap or repo-map in a learning session.

## Pick your track

| Session for… | Read to start (only these) | May write (only these) |
|---|---|---|
| **SQL** | `state/handoff-sql.md`, `state/progress-sql.md`, `_rules/heart.md` | `sql/**`, `state/handoff-sql.md`, `state/progress-sql.md`, `shared/qna-sql.md` |
| **Python** | `state/handoff-python.md`, `state/progress-python.md`, `_rules/heart.md` | `python/**`, `state/handoff-python.md`, `state/progress-python.md`, `shared/qna-python.md` |
| **Power BI** | `state/handoff-powerbi.md`, `state/progress-powerbi.md`, `_rules/heart.md` | `Microsoft Power BI Developer and Architect/**`, `state/handoff-powerbi.md`, `state/progress-powerbi.md`, `shared/qna-powerbi.md` |
| **DE Fault Lab** | `state/handoff-fault-lab.md`, `state/progress-fault-lab.md`, `projects/de-fault-lab/00_PROBLEM-MATRIX.md` — **and, for the banking repo it now targets, `<banking-repo>/learning/KNOWLEDGE-MAP.md` (retrieval by topic/incident/layer + current open state + next action)** | `projects/de-fault-lab/**`, `state/handoff-fault-lab.md`, `state/progress-fault-lab.md` |
| **Maintenance / planning** | `01_MASTER-ROADMAP.md`, `_rules/goal.md`, this file | reference files (roadmap, rules, dialect-map, lakehouse-map), root `CLAUDE.md`, `.claude/**`, `state/maintenance-log.md` |

> **The DE Fault Lab now operates against a real repo**, `rajeluqman/banking-multisource-lakehouse`
> (locally `d:/Obsidian/repos-rajeluqman/banking-multisource-lakehouse`). Its engineering
> knowledge — six real `discovered` incidents, evidence, troubleshooting cards and the
> real-incident → future-BREAK map — lives in that repo, routed from
> `learning/KNOWLEDGE-MAP.md`. This vault holds the *catalogue and session state*; the repo holds
> the *incidents and proof*. Do not duplicate one into the other.

> **DE Fault Lab** is a project track, not a learning track — it produces an artefact (a fault
> catalogue and injection runbook) rather than progressing through modules. Load only the layer
> file you are working in (`L0`–`L4`), never all five.

> Teaching pedagogy for any track lives in the `cikgu` skill (`.claude/skills/cikgu/SKILL.md`).
> Invoke it with `/cikgu`. It reads this table — it never overrides it.
> The skill is **three-tier by design**: its frontmatter description (~96 tok) is the only part
> loaded every session; `SKILL.md` loads when `/cikgu` is invoked; `references/*.md` load one
> at a time, only when the situation calls for that one. Never read the whole `references/`
> folder up front — that throws away the entire point of the split.

## Shared — APPEND-ONLY (any session appends, never rewrites; tag each entry [SQL] / [PY] / [PBI])
- `state/session-log.md` — one row per session
- `shared/glossary.md`, `shared/errors-gotchas.md`

## Read-only reference (only a Maintenance session edits these)
- `01_MASTER-ROADMAP.md`, `_rules/heart.md`, `_rules/goal.md`, `_rules/topic-template.md`
- `shared/dialect-map.md`, `shared/lakehouse-map.md`
- `concepts/*.md` — 34 cross-cutting concept hubs connecting the `Data engineering Book
  knowledge/notes/` corpus (6 books, 90 chapters) to each other and to `sql/`/`python/`.
  Built from a measured concept→chapter index (`state/build_concept_index.py`), not
  recall. Any session may open a hub when a topic matches; only Maintenance edits/adds
  hubs. See `concepts/_BUILD-SPEC.md` for how the set was built and how to extend it.
- `shared/gym-and-troubleshooting-doctrine.md` — dormant until Tier 3 (see roadmap)

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
5. **Structural cleanup** — a Maintenance session may delete or rename a *stale or duplicate file*
   inside a track directory (`sql/**`, `python/**`, ...) when it contradicts this router or the
   source table in root `CLAUDE.md`. It may **never edit the content** of a track note — that
   stays the track session's alone — the one exception being a **pointer line** (a path or
   file reference) inside a track file that contradicts this router, which Maintenance may
   correct. Never prose, examples, exercises, or status. Every such change is logged in
   `state/maintenance-log.md` with the contradiction that justified it.
