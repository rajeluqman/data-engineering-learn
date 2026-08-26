# CLAUDE.md — Data Engineering Learn Vault

> Auto-loaded context untuk Claude Code sessions. Jangan delete.
> Router sebenar untuk per-session load order = `vault/00_INDEX.md`. Baca fail tu dulu, pilih
> track, then baca hanya file track tu — jangan load seluruh vault setiap session.

---

## 🎯 Goal

Belajar SQL/Python/Power BI dari beginner sampai DE-level, plus tutup gap real-world guna
`vault/DE-Mastery/` (SRE Playbook dipetakan ke 10 repo sebenar). Target: boleh handle real
project — data warehouse, incremental load, platform SQL (Databricks/Snowflake).

Big picture / tier sequencing → `vault/01_MASTER-ROADMAP.md`.

---

## 🧭 Tracks

| Track | Content | State files | Status |
|---|---|---|---|
| **SQL** | `vault/sql/` | `state/progress-sql.md`, `state/handoff-sql.md` | Active — see Sources below |
| **Python** | `vault/python/` | `state/progress-python.md`, `state/handoff-python.md` | Active |
| **Power BI** | `vault/Microsoft Power BI Developer and Architect/` | `state/progress-powerbi.md`, `state/handoff-powerbi.md` | Registered, not started |
| **DE-Mastery** | `vault/DE-Mastery/` | `DE-Mastery/Progress-Tracker.md` | User-owned — sessions read only, never write `MASTER_CONTEXT.md` |

Full read/write ownership per track → `vault/00_INDEX.md` (this is the authority, not this file).

---

## 📂 Vault Structure

```
.claude/
  skills/cikgu/   ← teaching pedagogy (analogy, hint style, DoD gate) — /cikgu

vault/
  00_INDEX.md     ← session router, READ FIRST
  01_MASTER-ROADMAP.md
  _rules/
    heart.md      ← the session ritual + Definition of Done (authoritative)
    goal.md
    topic-template.md   ← fixed 7-section shape for every topic note
  sql/, python/, Microsoft Power BI Developer and Architect/
  DE-Mastery/     ← user-owned, sessions read-only
  shared/
    dialect-map.md, errors-gotchas.md, glossary.md
    gym-and-troubleshooting-doctrine.md   ← dormant until Tier 3
  state/
    progress-<track>.md, handoff-<track>.md   ← update every session end
```

---

## 📚 SQL Sources

| Module | Topic | Source | Timestamp |
|--------|-------|--------|-----------|
| M0 | Orientation | Baraa — Master SQL with Data | 07:38 |
| M1 | DQL Core | Baraa | 34:01 |
| M2 | DDL/DML + Keys | Baraa | 01:32:31 |
| M3 | Joins & Set Ops | Baraa | 02:47:57 |
| M4 | Functions | Baraa | 04:52:58 |
| M5 | Window Functions | Baraa | 08:50:11 |
| M6 | Subqueries & CTE | Baraa | 12:58:04 |
| M7 | Advanced Objects (Views/CTAS/Temp) | Baraa | 15:35:02 |
| M8 | Programmable Objects (SP/Trigger) | Baraa | 17:27:04 |
| M9 | Performance & Optimisation | Baraa | 18:23:42 |
| M10 | DE Project: Data Warehouse | Baraa | 23:21:04 |
| M11 | DE Platform SQL | Ansh Lamba — Big Data Engineer SQL | — |

Video Baraa: https://www.youtube.com/watch?v=SSKVgrwhzus

> This table is the live source of truth for SQL module/timestamp mapping. `_rules/goal.md`
> carries an older, superseded version — see the note appended there. Teach each module
> anchored on its transcript/timestamp above — the timestamp is the starting point to source
> real examples from, not a literal transcript reading.

---

## 📍 Current Position

Baca `vault/state/progress-<track>.md` dan `vault/state/handoff-<track>.md` (track yang
berkenaan) untuk latest position sebelum mula.

---

## 📋 Session Rules

Full ritual (per-topic flow, quiz rules, Definition of Done, end-of-session writes) lives in
`vault/_rules/heart.md` — that is the authoritative version, followed exactly, not restated here.

Teaching pedagogy (analogy discipline, hint style, evolution ladder, interview drill) →
`.claude/skills/cikgu/SKILL.md`, invoked with `/cikgu`. It plugs into heart.md's flow; it does
not replace it.

**One rule worth stating twice because it's cross-track:** before generating any resume bullet
or interview-answer claim, in ANY track, check `vault/DE-Mastery/Interview-Prep/defend-or-drop.md`
and `integrity-rules.md` first. Never claim evidence that isn't actually cited there.

### Format note (applies to every track)
- Bahasa: BM casual (lah, je, kan) + technical terms kekal English
- Setiap concept: WHAT → WHY → WHEN (bila nak guna dalam DE project) — full shape in
  `_rules/topic-template.md`

---

## ⚡ Quick Commands

- **"teruskan"** → baca handoff track semasa, sambung dari last position
- **"quiz M[n]"** → buat drill untuk module tu
- **"isi M[n]"** → fill note file untuk module tu dari transcript
- **"update state"** → update progress + handoff files sekarang
- **"/cikgu"** → load teaching-pedagogy skill untuk session ni
