# Topic Template — fixed shape for every topic note

> One consistent shape per topic across every track, so the brain doesn't re-learn a new
> layout each time and a note is scannable later. Lives beside `quiz-template.html` — same
> role (a fixed shape to fill), same folder.

## The 7 sections, in order

1. **Definition** — one or two sentences, plain language, no jargon left unexplained.
2. **Analogy** — one real-world mapping carrying relationship + purpose + limitation (see
   `.claude/skills/cikgu/SKILL.md`'s analogy-discipline seed set). Drop it once the mapping lands.
3. **Visual / code example** — the smallest example that shows the concept doing its job.
4. **Line-by-line walkthrough** — what each clause/line does and why it's in that order.
5. **Short exercise** — one small task the user does immediately, not just reads.
6. **Interview question** — one question this topic would actually generate, with what a
   strong answer covers (not necessarily the full answer — that's a drill, see cikgu's
   C-P-I-D-I-R section).
7. **Real-world DE application** — where this shows up in an actual pipeline (Bronze/Silver/
   Gold, dedup, incremental load, etc.) — the WHEN in heart.md's WHAT→WHY→WHEN rule.

## Rule: floor, not cage

All 7 sections appear in every topic note. If a section genuinely doesn't apply (a topic with
no natural analogy, or no realistic interview angle yet), write the section header and a single
line: `— not applicable: <one-line reason>`. Never force a section that would just be filler —
that's worse than skipping it honestly. But never silently drop a section either; the `—` line
is what keeps the shape predictable even when a section is empty.

## Worked example (retrofitted from existing `sql/notes/M1-dql-core.md` content)

```md
## GROUP BY — Aggregation

### 1. Definition
GROUP BY collapses many rows into one row per distinct value of a column, so an aggregate
function (COUNT, SUM, AVG...) can compute one number per group instead of one per row.

### 2. Analogy
Sorting a pile of receipts into one envelope per category, then writing the total on the
front of each envelope. Limitation: once sorted into envelopes, you can't see individual
receipts anymore in that view — same as GROUP BY hiding the individual rows behind the
aggregate.

### 3. Visual / code example
    SELECT category, SUM(unit_price) AS total_sales
    FROM dim_product
    GROUP BY category;

### 4. Line-by-line walkthrough
- `GROUP BY category` — collapse rows sharing the same category value into one group.
- `SUM(unit_price)` — per group, add up unit_price across every row that landed in it.
- `SELECT category, ...` — category is safe to select ungrouped because it's the group key;
  any other non-aggregate column would error (see errors-gotchas SQL-010).

### 5. Short exercise
Write a query: total quantity sold per product, only products with total > 50, highest first.
(Answer key already exists: `sql/quiz/checkpoints/drill-M1-business-decode.md` Round 1.)

### 6. Interview question
"Walk me through what happens when you add a WHERE and a HAVING to the same GROUP BY query —
what's the execution order and why does it matter?" A strong answer names the FROM → WHERE →
GROUP BY → HAVING → SELECT → ORDER BY order and explains WHERE can't see aggregates yet.

### 7. Real-world DE application
Every Gold-layer fact table rollup (daily sales per store, transactions per customer) is a
GROUP BY at its core — this is the same shape as a dbt mart model's final SELECT.
```
