# Gym & Troubleshooting Doctrine — reference only, DORMANT until Tier 3

> **Status: not active.** Ported from `pharma_novartis_sttm` (the only one of the user's 21
> repos that fully built this) during the 2026-08-26 cross-repo scan and merge. It captures the
> *method*, not the infrastructure — see §3. It stays dormant until `01_MASTER-ROADMAP.md`'s
> Tier 3 exit gate is met (Tier 1 SQL/Python foundation complete first — that sequencing is
> locked, see the roadmap). No session should build against this doctrine before then.
>
> Cross-reference: `DE-Mastery/Interview-Prep/integrity-rules.md` Rule 2 already states the
> governing framing for this whole doctrine — **"training drill, BUKAN production."** Don't
> restate that rule here; read it there.

## 1. Why this exists (and why it's not active yet)

Two of the user's repos (`banking-multisource-lakehouse`, `creative_intelligence_lab`)
deliberately **rejected** building a gym like this — for a single production-focused repo, a
full sabotage-drill apparatus is over-scope, and both explicitly said so in their sign-offs.
That reasoning does not transfer here: this vault's entire purpose is deliberate practice, so a
graded hands-on drill mechanism is exactly on-scope — just not yet, because Tier 1 (SQL/Python)
isn't done and the roadmap explicitly locks the order.

## 2. The transferable method (this is the actual value)

Four disciplines, all about **grading the method, not the answer or the clock**:

1. **Observability-first.** Before touching anything, ask "what does the signal say?" — not
   "let me start changing things and see."
2. **Hypothesis log before running anything.** Write `hypothesis → test → predicted output`
   *before* running the test. The gap between predicted and actual is the actual lesson.
   Thrashing (random changes, no prediction) is the failure mode this exists to kill.
3. **Evidence-gate.** No claim is accepted without `command + output`. "I think it's X" is not
   a diagnosis until there's a command that proves it.
4. **Recovery is graded too.** Finding the cause isn't done — done means recovering safely
   (idempotent fix, verify before re-enabling, reconcile counts). A fix that causes a second
   failure fails the recovery grade even if the diagnosis was right.

## 3. Infrastructure: optional, only if a real pipeline exists to sabotage

Pharma's version needed a 3-layer safety mechanism because it fences a pipeline holding real
cloud credentials:
- Isolated storage/target (never the real prod bucket/warehouse).
- A fail-closed preflight check (aborts if the environment could touch anything real).
- A throwaway branch per drill, discarded after.

This vault's Tier 4 plan is rebuilding the 10 repos from scratch for practice — a different
risk profile with no live credentials to fence off by default. **Don't build this apparatus
speculatively.** If a future session stands up a real pipeline worth sabotaging (e.g. rebuilding
one of the Tier 4 repos far enough that it touches real cloud resources), adopt the 3-layer
pattern then, scaled to whatever actually needs fencing.

## 4. Difficulty ladder — the concept, generalized

Separate **what breaks** from **how hard it is to find**. The same underlying bug can be an
easy drill or a hard one depending on how far the symptom is presented from the root cause.

| Axis | Low level | High level |
|---|---|---|
| Symptom distance | at/near the root | far (a business KPI, not a stack trace) |
| Causes | single | compound / contributing |
| Red herrings | none | misleading-but-innocent signals present |
| Theatre (severity tags, fake alerts) | none | present at the highest levels only |
| Recovery risk | trivial re-run | idempotency trap, ordering matters |

A rough L1→L10 shape: L1-L2 = symptom at/near root, evidence-gate is the only skill being
drilled. L3-L6 = trace backward one or more hops, recovery starts being graded. L7-L8 = a red
herring or induced time-pressure is added on top. L9-L10 = compound causes, and a naive fix
makes things worse before it gets better. Build the actual catalogue of failures when Tier 3
opens and there's a real pipeline to draw failure modes from — don't invent one now.

## 5. Troubleshooting card format (adopt when Tier 3 opens)

```
### <ID> — <symptom, stated far from the root cause>
- Phase        : where in the pipeline this surfaces
- Symptom      : what a stakeholder/monitor/log sees FIRST — not the underlying bug
- Diagnosis    : where to look + the exact command/query that proves it
- Root cause   : the actual defect, ranked if more than one candidate
- Fix/Recovery : the action, plus backfill/rerun if relevant
- Evidence     : file:line of the guard, or "no guard yet + where one would go"
- Junior mistake: the plausible-but-wrong first move
- Soundbite    : one line, interview-ready summary
```

## 6. Authoring rule — the part that keeps this honest

**A card is written only after a real incident happens** — while rebuilding a Tier 4 repo, a
real bug, a real wrong-result query, a real broken pipeline step. Never author a card from an
imagined scenario. This is the same discipline `banking-multisource-lakehouse` and
`creative_intelligence_lab` used to keep their (deliberately stub) troubleshooting libraries
honest, and it's the same family of rule as `DE-Mastery/Interview-Prep/integrity-rules.md` —
don't claim evidence you don't have. A format this structured is persuasive-looking even when
empty; the authoring rule is what stops it from being used to manufacture war stories.
