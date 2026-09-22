# Maintenance Log

> Save-file for Maintenance / planning sessions, parallel to `state/progress-<track>.md`.
> Append-only. Registered in `00_INDEX.md`'s ownership table.
> Every structural change to a track directory is logged here with the contradiction that
> justified it (`00_INDEX.md` hard rule 5).

---

## 2026-08-30 — Coverage audit + Definition-of-Done gate 2 rebuild

**Trigger.** A public case study — Nasrul Hazim, *"All 112 Cards Drew Perfectly. All 161
Relations Were Gone"* (dev.to) and the companion toolkit repo `nasrulhazim/claude` — was
reviewed for what transfers into this vault. Two of its principles were applied to the vault
itself rather than merely noted:

- **"Read the result, not the instructions."** The router (`00_INDEX.md`) and root `CLAUDE.md`
  are the *instructions*; what is actually on disk is the *result*. They had drifted apart.
- **"A gate that cannot fail isn't a gate — it's decoration with a green tick on it."**
  Definition-of-Done gate 2 was structurally incapable of failing.

**Integrity note.** The ERD work in that article is Nasrul's, not this vault's. Per
`DE-Mastery/Interview-Prep/integrity-rules.md`, the only defensible claim arising from this
session is: *"I applied a published coverage-check pattern to my own learning vault — here are
the seven drifts it caught."* That is defensible because it actually happened, and the audit
output below is the evidence.

### Drifts found and closed

| # | Type | Finding | Action |
|---|---|---|---|
| 1 | `stale()` | `00_INDEX.md:26` declared *"repo-map files under `Repo learning/`"* — the folder does not exist | Pointer removed |
| 2 | `duplicate()` | Two M8 notes: `M8-programmable.md` (source anchor, correct post-realignment scope) and `M8-programmable-objects.md` (no source header, still carried M7's *Views & Materialised Views*) | Deleted `M8-programmable-objects.md` — superseded pre-realignment copy |
| 3 | `stale()` | `M9-platform-sql.md` was titled *"M9 — Platform SQL"*, but `CLAUDE.md` maps M9 = *Performance* and M11 = *DE Platform SQL*. Its content duplicated `M11-de-platform.md` | Deleted `M9-platform-sql.md` — leftover from the 2026-08-26 M7–M11 realignment |
| 4 | `stale()` | `python/master-doc.md:13` pointed C at `shared/qna-log.md`; the router says `shared/qna-python.md` | Pointer corrected; `qna-log.md` frozen with a supersession header (it held zero entries) |
| 5 | Gate | `heart.md` required every quiz as `.md` **and** `.html`; both folders held zero quizzes | Re-classified and rebuilt — see below |
| 6 | `stale()` **(new, found mid-session)** | `python/master-doc.md:7` pointed at `state/progress-tracker.md`, which `00_INDEX.md` lists under **Frozen — do not write, do not read for status** | Pointer corrected to `state/progress-python.md` |
| 7 | Gate **(new, found mid-session)** | `_rules/quiz-template.html` printed *"Good job! Move to next module."* at **70%**, contradicting the **80%** DoD gate in `heart.md` — the runnable artifact would have green-ticked a score the rule calls "not done yet" | Template rewritten to the three-band model (<70 / 70–79 / >=80) |

### Correction to the original finding on drift 5

The first pass reported this as *"the HTML step is being silently skipped."* That was too
strong. The audit shows **both** quiz folders are empty — `.md` and `.html` alike — and SQL M1
is the only module in progress with its quiz not yet authored. So the accurate statement is
that the rule has **never been exercised**, not that it has been violated. The structural
problem is real but different: nothing would have caught a `.md`-only quiz if one had been
written. That is what the rebuild below fixes.

### Definition-of-Done gate 2 — rebuilt as an evidence gate

Before: quiz >= 80%, self-reported. `heart.md` admitted in its own text that a session could not
verify a score it wasn't told. A gate whose only input is an unverifiable spoken number cannot
fail.

After:

- `_rules/quiz-template.html` now emits a **result receipt** on the result screen:
  `RECEIPT m1-dql-core · 8/10 (80%) · 2026-08-30 · wrong: Q3(T2), Q7(T3) · chk 4f2a`
- The `chk` is a checksum over the quiz slug, the answer pattern and the score, so an edited
  number no longer matches its own receipt.
- Gate 2 now accepts **the receipt**, not a spoken score. Pasted under `## Quiz Receipts` in
  `state/progress-<track>.md`.
- The `wrong:` list feeds the **Weak spots** column directly — the receipt's real daily value
  is the weak-spot signal, not the policing.
- The `.md` → `.html` render is now stated as **two deliberate steps** with different failure
  modes (the same decoupling reasoning as banking ADR-011), and a `.md`-only quiz is explicitly
  declared incapable of flipping a status.

**Stated limit, deliberately not oversold:** this is **tamper-evident, not tamper-proof**.
A session still cannot observe a quiz being taken. What changed is that the frictionless path
to a green tick is gone, and gates 1 and 3 fail independently, so a faked receipt alone flips
nothing. `heart.md` now says this in those words.

### Files changed

| File | Change |
|---|---|
| `00_INDEX.md` | Stale `Repo learning/` pointer removed; `state/maintenance-log.md` registered; **hard rule 5** added — Maintenance may delete/rename a stale or duplicate *file* in a track dir, and correct a *pointer line*, but never edit track note content |
| `_rules/heart.md` | Quiz-storage rule rewritten (two steps, receipt-producing); gate 2 rewritten as an evidence gate; "Honesty limit" replaced with an accurate "Evidence limit" |
| `_rules/quiz-template.html` | Receipt block + checksum + copy button; three-band result message (150 → 206 lines) |
| `python/master-doc.md` | Two stale pointers corrected (drift 4, drift 6) |
| `shared/qna-log.md` | Frozen with supersession header |
| `sql/notes/M8-programmable-objects.md` | **Deleted** (rule 5 — superseded duplicate) |
| `sql/notes/M9-platform-sql.md` | **Deleted** (rule 5 — superseded by M11) |
| `sql/quiz/html/README.md` | Receipt instructions added |
| `python/quiz/html/README.md` | **Created** — the path `heart.md` now names had no directory behind it |

### Post-fix audit output

```
stale():      only MX-/ChX- filename placeholders remain (audit needs a placeholder-ignore rule)
unmapped():   none
duplicate():  M7 -> [M7-advanced-objects.md, M7-de-scenarios.md]   <- open, see below
gate():       SQL quiz .md 0 · .html 0 · PY quiz .md 0 · .html 0   <- expected, none authored yet
receipt emitter present in template: True
```

### Open — deliberately not actioned

- **M7 has two notes.** `M7-advanced-objects.md` is the module note (source-anchored, Baraa
  15:35:02). `M7-de-scenarios.md` is supplementary cross-module DE material (dedup, watermark,
  SCD/MERGE) that maps to no module row. It is not a duplicate and deleting it would destroy
  intended content — **user's call**, not a maintenance decision.
- **The audit is still a throwaway script**, not a skill. Until it is packaged, drift can
  return silently. This is the single highest-value next item.

---

## Progress snapshot — 2026-08-30

### Framework (this session's scope)

| Item | Status |
|---|---|
| Router vs disk consistency | Done — 7/7 closed, audit re-run clean |
| DoD gate 1 — teach-back | Open — honesty contract (unchanged, by design) |
| DoD gate 2 — quiz >= 80% | Done — upgraded to evidence gate (receipt + checksum) |
| DoD gate 3 — >= 3 exercises | Open — honesty contract (unchanged, by design) |
| Maintenance write authority | Done — formalised as `00_INDEX.md` hard rule 5 |
| `vault-audit` skill | Open — next session |
| Quick Commands → `.claude/commands/` | Open — after vault-audit |
| `cikgu` split into `references/` | Done — built by a parallel session, verified + trimmed in entry (b) below |

### Learning tracks (unchanged this session — no track content was taught)

| Track | Position | DoD counters |
|---|---|---|
| SQL | M1 DQL Core, in progress — GROUP BY / HAVING drill | teach-back ☐ · quiz — · exercises 0/3 |
| Python | Ch 2–3 done (pre-DoD); next Ch 4 String Formatting | not started |
| Power BI | Registered, not started | — |
| DE-Mastery | User-owned, read-only. P1 gap = formal SLO/error budget | — |

**Note on cost.** This was framework work, not learning. SQL M1 still sits at `0/3 exercises`
with teach-back unchecked. The remaining framework items are worth one focused session, not a
running project — the vault exists to teach SQL and Python, not to be maintained.

### Next actions, in order

1. **Learning session (SQL)** — finish the GROUP BY/HAVING drill, author the M1 quiz as `.md`,
   render it to `.html`, sit it, paste the receipt. This exercises the rebuilt gate 2 end to
   end for the first time and is the only way to know it actually works.
2. **Maintenance session** — package the audit script as `.claude/skills/vault-audit/`
   (`unmapped()` / `stale()` / `duplicate()` / `gate()`), with a placeholder-ignore rule for
   `MX-`/`ChX-` patterns. Bilingual triggers: `"audit vault"`, `"vault dah lari"`.
3. **Maintenance session** — convert the four Quick Commands in `CLAUDE.md` ("teruskan",
   "quiz M[n]", "isi M[n]", "update state") into `.claude/commands/`.
4. **Deferred** — split `cikgu` along the `references/` pattern only once it feels heavy.
5. **Tier 4, blocked** — apply `unmapped()`/`stale()` to the banking MDM crosswalk. Blocked
   because banking is not part of this vault and the roadmap locks the sequence.

---

## 2026-08-30 (b) — cikgu three-tier verification + provenance moved out of the hot path

**Context.** A token-economy study of `nasrulhazim/claude` (cloned at `f183b50`, v2.4.0,
measured with `tiktoken cl100k_base`) established that the saving in that repo comes from the
**Claude Code skills platform**, not from any technique the repo claims — it never mentions
tokens, context windows, or progressive disclosure anywhere in 194 files. The measured shape:
66.6% of its 461,163-token corpus sits in `references/` and never loads unless asked for.

The same measurement was then run against this vault, where the `cikgu` split had already been
built by a parallel session.

**Measured result — the pattern is working here.**

| Tier | Cost | Loads when |
|---|---|---|
| frontmatter description | **96 tok** | every session, every track |
| `SKILL.md` | 2,305 tok (was 2,677) | `/cikgu` invoked |
| `references/language.md` | 2,393 tok | rendering rojak |
| `references/explanation-pattern.md` | 1,284 tok | structuring an explanation |
| `references/teaching-method.md` | 1,009 tok | checking comprehension |
| `references/provenance.md` | ~700 tok | never during teaching |

Against the alternative of pasting the material into `CLAUDE.md` (auto-loaded, 21,585 tok):
**99.6% cheaper** on a session that doesn't teach, **76.1% cheaper** on one that does.

**Change made.** The `## Provenance` block was moved out of `SKILL.md` into
`references/provenance.md`. It is history — it informs no runtime decision, yet it was being
paid on every single `/cikgu` invocation. `SKILL.md` 2,677 -> 2,305 tok (**-13.9% per
invocation**). `references/provenance.md` also now carries the phase-2 backlog table.

**Router updated.** `00_INDEX.md` now states the three-tier contract explicitly, including the
rule that matters most: never read the whole `references/` folder up front, which would throw
away the entire saving.

**Correction to an earlier estimate.** The prior session's note projected "~80 tokens" for the
description. Measured: **96**. The conclusion is unaffected.

**Open — phase 2.** §12–27 and §41–46 of `CIKGU_Malaysian_BM_Rojak_Teaching_System.md`
(~26 sections) are still unimported, staged as four planned reference files. Table in
`references/provenance.md`. This is a content-import decision, not maintenance — user's call.

**Open — source docs.** `CIKGU_Malaysian_BM_Rojak_Teaching_System.md` (7,954 tok) and
`spoken-malaysian.md` (4,903 tok) sit unrouted in the repo root. They cost nothing (nothing
loads them) and they are still needed as phase-2 sources. Moving them under
`.claude/skills/cikgu/references/_source/` would tidy the root — not done, because one was open
in the editor and it is the user's file to place.


---

## 2026-08-30 — D-5: English promoted to default language for all sessions

Owner decision, recorded as D-5 in `vault/SPEC_framework-supervisor.md`. Scope confirmed by the
owner as **all sessions, not only teaching**: English is the first choice even when the prompt
itself is in Malay. BM rojak is demoted from default spoken register to an unblock layer that
fires for one point, on a comprehension signal, then reverts.

This supersedes the earlier same-day change that had moved explanations from written-English
into the spoken-BM list. Written-to-disk output was English before and after — that half never
changed.

**Files changed (4):**

| File | Change |
|---|---|
| `_rules/heart.md` | Language section rewritten as two layers: Layer 1 English default (explicitly including Malay-language prompts), Layer 2 BM rojak unblock with named triggers, one-point scope, and a return-to-English rule. Supersession note appended. |
| `CLAUDE.md` | Rewritten in English (it was itself mostly BM rojak, which contradicted the rule it carried). Format note replaced with the two-layer rule. Added `SPEC_framework-supervisor.md` to Goal and to the structure map. |
| `.claude/skills/cikgu/SKILL.md` | Frontmatter description updated (this is the always-loaded tier, so the old "BM rojak rendering" phrasing was mis-signalling on every session). Language section rewritten; `references/language.md` re-scoped in the load table to "only when the unblock layer fires"; the reason-first and naturalness-gate rules re-scoped to the unblock layer, plus a new note that English here means engineer-to-engineer, not documentation prose. |
| `.claude/skills/cikgu/references/language.md` | Header rewritten to state the scope change and the load trigger. "Formality switch" section replaced with "Returning to English". The rendering craft itself left untouched — it is still exact, just invoked less often. |

**Not changed, deliberately.** `explanation-pattern.md` and `teaching-method.md` govern
explanation shape and comprehension checking, which are language-independent. Their trigger
phrases (e.g. the reset protocol for "aku tak faham") stay valid — that phrase is now also the
signal that fires the unblock layer, so it does double duty rather than needing a rewrite.

**Open — root source docs.** `CIKGU_Malaysian_BM_Rojak_Teaching_System.md` and
`spoken-malaysian.md` still sit unrouted in the repo root. Under D-5 they are reference material
for the unblock layer rather than the primary teaching system, which strengthens the earlier
note that they belong under `.claude/skills/cikgu/references/_source/`. Still not moved —
still the user's file to place.

---

## 2026-09-03 — DE Fault Lab registered as a new track

**Why.** A new project (production-failure catalogue + fault-injection runbook across 5 source
systems on real GCP) needed a home. It is not a learning track — it produces an artefact rather
than progressing through modules — but it needs session continuity like one, so it was registered
with its own directory and state files rather than being appended to an existing track.

**Owner decisions taken this session (4):** doc + injection playbook (not scaffold code) · real
GCP (not local Docker) · new track at `vault/projects/de-fault-lab/` (not a root SPEC file) ·
markdown cards + compact index (not wide tables, not an HTML artifact).

**Files changed (2 router files):**

| File | Change |
|---|---|
| `00_INDEX.md` | New track row: reads `state/handoff-fault-lab.md`, `state/progress-fault-lab.md`, `projects/de-fault-lab/00_PROBLEM-MATRIX.md`; writes `projects/de-fault-lab/**` plus its two state files. Note added that it is a project track, and that a session loads only the one layer file it is working in. |
| `CLAUDE.md` | New row in the Tracks table pointing at the project directory and its state files. |

**Files created (10):** `projects/de-fault-lab/` — `00_PROBLEM-MATRIX.md`, `01_ripple-map.md`,
`L0-sources.md`, `L1-landing.md`, `L2-bronze.md`, `L3-silver.md`, `L4-gold.md`,
`02_injection-runbook.md`; plus `state/handoff-fault-lab.md`, `state/progress-fault-lab.md`.

**Not changed, deliberately.** No track file, rule file, or `DE-Mastery/**` content was touched.
The project reads `DE-Mastery/Interview-Prep/integrity-rules.md` as the governing rule for its
citation standard but does not write there.

**Open — carried in the handoff, not resolved here.** Whether to force the catalogue to exactly
6 problems per layer (currently 34, with the deviation and its rationale recorded); whether to
add an explicit Origin/Detect/Resolve/Prove line to `L0-sources.md` for consistency with the
other four layer files; and Databricks vs Dataproc, which changes two card recommendations.

---

## 2026-09-04 — Routing: vault had no path to the banking repo's knowledge

**Contradiction that justified the change.** `00_INDEX.md` routes the **DE Fault Lab** track only
to vault-side files, but that track has been operating against a real repo
(`banking-multisource-lakehouse`) since 2026-09-04. Six real incidents, all their evidence, the
troubleshooting cards and the incident→BREAK map live in that repo and were unreachable from this
router — a session entering through `00_INDEX.md` would not have found them.

**Changed (pointer only, no track content).** The DE Fault Lab row now also names
`<banking-repo>/learning/KNOWLEDGE-MAP.md`, plus a short note stating the split: **the vault holds
the catalogue and session state; the repo holds the incidents and their proof.** No prose,
example, exercise or status inside any track note was touched.

**Why a pointer and not a copy.** Duplicating incident detail into the vault would create a second
source of truth that drifts. The repo's ledger (`learning/INCIDENTS.jsonl`) and `evidence/` are
canonical; this router only needs to reach them.


---

## 2026-09-23 — Concept hub layer: the 90-chapter corpus had no cross-book index

**Contradiction that justified the change.** The `Data engineering Book knowledge/` corpus
reached 90 gate-verified chapter notes across 6 sources, but every note's §9 Cross-references
pointed only *within its own book*. Only 4 of 90 notes contained any `[[wikilink]]`, so the
corpus was effectively invisible to Obsidian's graph and unreachable from the learning tracks.
Meanwhile `shared/glossary.md` had been declared a "Cross-track index" since 2026-08-18 but was
still empty, and `shared/lakehouse-map.md` already carried the *same idea* in miniature
(SQL concept → medallion layer) with an explicit "append new mappings as modules progress" note.
The intent existed in three places; the connecting layer did not.

**Changed.**
- **New:** `concepts/` — 34 cross-cutting concept hubs, each mapping one idea across all 6 books
  plus the SQL/Python tracks. Built from a *measured* concept→chapter index
  (`state/build_concept_index.py`, scanning 138 files), not from recall, per the No-Guess Rule.
  `concepts/_BUILD-SPEC.md` records the method and how to extend it.
- **Reference files (Maintenance-owned):** `00_INDEX.md` gained one entry registering
  `concepts/` in the read-only reference block; `shared/lakehouse-map.md` gained a Concept Hub
  column plus 6 rows for patterns it lacked (CDC, SCD2, materialized views, compaction,
  idempotent write, EXPECT/CHECK); `shared/glossary.md` populated with the 34 terms.
  No track note's prose, examples, exercises or status was touched.
- **Book corpus (`notes/**`):** §9 Cross-references only — 438 intra-book chapter mentions
  wrapped in `[[wikilinks]]`. Verified mechanically: all 250 changed lines are byte-identical
  once link markup is stripped, so no audited content changed. `verify_all.py` 13/13 PASS,
  confirmed by two independent runs.

**Why a separate layer and not edits to the notes.** The 90 notes are gate-verified artifacts
under `verify_citations.py`; rewriting their prose to add cross-book commentary would put audited
text at risk and couple each note to every other. A hub layer inverts that — notes stay
untouched, the hubs carry the connections, and regenerating the index cannot corrupt a note.

**Known trap recorded, not silently resolved.** Four terms carry different meanings across
sources and are explicitly disambiguated per hub rather than merged: **partition** (physical
storage / DDIA sharding / SQL `PARTITION BY` / Kafka), **transaction** (ACID vs Kimball's
fact-table grain type), **window** (SQL `OVER()` vs event-time bucket), **watermark**
(`lakehouse-map`'s `MAX(timestamp)` load bookmark vs Streaming Systems' completeness metric).
Fusing these on a name match would teach something false; the hit-count scan alone would have.

**Also corrected here.** The snapshot commit initially staged the source PDFs and 44MB of
regenerable `audit/render_cache/*.png`; both were removed and `.gitignore` extended so neither
can re-enter the repo.
