# Ch.9 — Human Resources Management

**Source:** `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd Edition, Kimball & Ross, Wiley 2013)
**PDF page range:** 299–316 (18 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (pilot #3 — medium band, this session)
**Word count (measured, `chapter_stats.json`):** 6,080
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Factless fact table [S]** (p300): a fact table with no numeric metrics, used to
record that an event occurred. The chapter's opening example is an employee-profile
transaction table — "the fact table is factless" because "no numeric metrics are
associated with changes made to employee profiles."

**Type 2 slowly changing dimension (SCD) applied to HR [S]** (p301): the chapter's
core recommended design is to fold profile-change tracking directly into the employee
dimension via type 2 rows, rather than a separate transaction fact table — "the
employee dimension contains a snapshot of the employee profile characteristics
following the employee's profile change," with the transaction type recast as a
"change reason attribute" on the dimension itself.

**Employee headcount periodic snapshot [S]** (p303–304, Figure 9-3): a monthly grain
fact table (Month × Employee × Organization) carrying additive counts (new hires,
transfers, promotions, salary paid) and semi-additive balances (vacation days balance,
which "must be averaged across the month dimension after adding across the other
dimensions").

**Recursive employee hierarchy (manager rollup) [S]** (p307–310): three named
techniques for representing the employee→manager relationship — (1) a role-playing
manager foreign key directly on the fact table, (2) a role-playing manager outrigger
on the employee dimension, (3) a management-hierarchy bridge table for variable-depth
rollups ("one row for each manager and each employee who is directly or indirectly in
their management chain").

**Multivalued skill keyword attribute [S]** (p310–313): two competing designs for an
open-ended, variable-cardinality attribute (technical skills) — a bridge table
("Skill Keyword Bridge") versus a delimited text-string attribute directly on the
dimension ("Skill Keyword Text String"), with an explicit trade-off worked through in
SQL for both.

## 2. WHAT / WHY / WHEN

**WHAT:** A worked, cross-industry dimensional-modeling case chapter (the ninth in a
run of case-study chapters, following the same book-wide pattern of a business
vignette → schema design → refinement). It reuses and re-applies techniques from
earlier chapters (Ch.5 SCD techniques, Ch.7 recursive hierarchies) to the HR domain
rather than introducing net-new theory. `[D]`

**WHY it matters for a DE project:** the "additive complacency" warning (p299 — "It
is easy for dimensional modelers to get lulled into a kind of additive complacency")
is a design-review heuristic: HR data (unlike sales/transaction data in most prior
chapters) is dominated by *profile state*, not additive events, so a modeler who
defaults to a transaction fact table for every business process will over-engineer
the schema. This is a transferable review question for this vault: "is this actually
an event, or is it a profile that should live on a type-2 dimension?" `[D]`

**WHEN to reach for the bridge-table approach vs. the flat text-string approach**
(p312–313, the chapter's own explicit trade-off): use the bridge table when queries
need to *count by keyword* ("it doesn't support queries that count by skill keyword"
is stated as the flat string's limitation); use the delimited string when the
AND/OR query pattern must be simple SQL and per-keyword counting is not required. `[S]`

## 3. Assumptions and prerequisites

- This chapter assumes familiarity with type 1/type 2 SCD mechanics from earlier in
  the book (explicitly deferred: "As discussed in Chapter 5: Procurement with the
  coverage of slowly changing dimension techniques…", p301) and with recursive
  hierarchy handling from Ch.7 (explicitly deferred: "the alternative approaches
  discussed in Chapter 7 for handling recursive hierarchies…", p309–310). This note
  does not re-derive those techniques — see the Ch.5/Ch.7 notes when they exist. `[S]`
- Assumes a relational or OLAP-tool-backed BI layer; the recursive-hierarchy section
  explicitly contrasts OLAP-native parent/child hierarchy support against
  relational-only approaches (Oracle `CONNECT BY`, SQL recursive CTEs), calling both
  relational approaches "virtually unworkable for business users armed with a BI
  reporting tool" (p309). `[S]`

## 4. Mechanism / key steps

**Employee profile tracking, arrived at by elimination (p300–301):**
1. Naive design: a transaction-grained factless fact table (Figure 9-1) with one row
   per profile-change event, joined to a type-2 employee dimension.
2. Problem identified in-text: the fact table and the type-2 dimension end up with
   "the same number of rows" and are "almost always joined to one another" — a signal
   that "dimensional modeling alarms should be going off."
3. Resolution: eliminate the separate fact table; embed the transaction-type
   description directly as a "change reason" attribute on the type-2 employee
   dimension (Figure 9-2).

**Recursive manager hierarchy, three options with an explicit escalation path
(p307–310):**
1. Manager key as a second role-playing FK directly on every fact table needing
   manager rollup — simplest, but "these dual foreign keys must be embedded in every
   fact table."
2. Manager key as an attribute/outrigger on the employee dimension itself — avoids
   fact-table duplication, but raises a type-1-vs-type-2 design decision (see §6).
3. Bridge table for arbitrary-depth rollups, with an explicit trade-off noted between
   using surrogate keys (accurate history, but "rapid growth" when senior managers'
   profiles change) versus durable natural keys (slower growth, "quite challenging
   to navigate").

## 5. Trade-offs and limitations

- **Vendor/packaged HR data models** (p306–307): the chapter is explicitly skeptical.
  Direct claims: packaged solutions introduce abstractions that "can feel like a
  foreign language for less-immersed functional managers," and a packaged model can
  "become another isolated stovepipe data set" if it can't conform to existing master
  data. The chapter's cost-benefit challenge is pointed: "is this knowledge worth the
  price tag" when "you could likely gain the same insight by spending a few weeks with
  the business users." `[S]` — this is an opinionated, not neutral, position from the
  authors, consistent with Kimball's dimensional-modeling-first stance across the book.
- **Manager-key-as-type-2 has a cascading-update failure mode** (p308, worked
  example with named individuals "Abby" and "Hayden"): if the manager's own dimension
  row changes for *any* type-2 reason (e.g., a home-address change) and the manager
  foreign key is itself type 2, "a type 2 change in her profile would ripple through
  the entire table" — for a CEO, this means "replicating a new profile row for every
  employee." This is a concrete, source-supported cautionary example, not a
  hypothetical added by this synthesis. `[S]`
- **The bridge-table approach for hierarchies has real cost**: "the bridge table is
  somewhat challenging to build, plus it contains many rows, so query performance can
  suffer" (p310), and reversing direction (aggregate up vs. drill down) requires the
  join paths to be reversed. `[S]`

## 6. Failure modes and edge cases named explicitly in the text

- Treating every HR event as a change to the employee dimension: "you probably
  shouldn't use the employee dimension to track every employee review event, every
  benefit participation event, or every professional development event" (p303) — the
  chapter's own corrective to over-applying its own §4 technique.
- Text comments stored directly in the fact table: explicitly rejected — "freeform
  text fields shouldn't be stored in the fact table because they just add bulky
  clutter" (p314); the recommended fix is a separate comments dimension or an
  attribute on a transaction-grained dimension, chosen by comment cardinality
  relative to transaction count.
- Case-sensitivity in the skill-keyword text-string search: "Is it UNIX or Unix or
  unix?" (p312) — resolved by coercing to uppercase before matching.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the "additive complacency" check (§2) and the "is this actually an
  event" question are reusable review heuristics for any new fact-table proposal in
  this vault's projects, not just HR data. `[D]`
- **Maintain:** the CEO-cascading-update failure mode (§5) is a concrete regression
  test to write for any schema using a type-2 self-referencing hierarchy key — verify
  that changing a top-of-hierarchy row does not explode into N new rows for every
  descendant. `[D]`
- **Optimization:** the bridge-table-vs-text-string decision (§2 WHEN) is a direct,
  reusable rule of thumb for any multivalued-attribute design: pick based on whether
  per-value counting queries are required. `[D]`

## 8. How to test / verify these claims

- The cascading-update failure mode is directly testable: build a small fixture with
  a 3-level manager hierarchy using a type-2 self-referencing key, change the
  top-level manager's profile, and assert how many new dimension rows are produced.
  This is exactly the kind of fixture this vault already builds for SCD testing
  (see `[[pyspark-local-testing-gotchas]]` for the local testing environment notes). `[D]`
- The bridge-table query-performance claim ("many rows, so query performance can
  suffer," p310) is a claim about a specific, unspecified workload — not independently
  verified in this chapter; would need an actual row-count/query-plan measurement
  against a real bridge table to confirm for a specific project. `[U]`

## 9. Cross-references

- Builds on SCD technique chapters ([[ch05_procurement|Ch.5]] Procurement — not yet synthesized) and
  recursive-hierarchy technique chapters ([[ch07_accounting|Ch.7]] Accounting — not yet synthesized). This
  note should be revisited once those are done, to confirm nothing here contradicts
  the earlier chapters' framing.
- The vendor-solution skepticism (§5) is a useful counterpoint to weigh against
  `databricks_big_book_4e`'s vendor-authored chapters (already flagged in that
  source's own notes as reading vendor material with an explicit skeptical lens).

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 9-1 through 9-10 (schema diagrams) | Described in prose above (their structural content, e.g. keys/attributes), but the diagrams themselves were not re-drawn; table column lists were read from the extracted text layer, not from a rendered image. |
| Full bus-matrix table (Figure 9-4, p304–305) | The extracted text for this figure is a jumbled list of process names and X-marks with lost row/column alignment (a table-in-image or complex-table extraction limitation) — the *concepts* (which HR processes need which fact-table type) are covered narratively above from the surrounding prose, but the matrix's exact process×role grid was not reconstructed. This is a `reading_order_risk`-class limitation on this specific figure page, not covered by this session's broader deferred sample. |

## Effort measurement — third data point (medium band, No-Guess Rule)

| | Pilot 1 (long) | Pilot 2 (short) | Pilot 3 (medium, this note) |
|---|---:|---:|---:|
| PDF pages | 30 | 4 | 18 |
| Words (measured) | 10,698 | 1,209 | 6,080 |
| Tool calls (extract→read→write) | 3 | 3 | 3 |

Words-per-page: 357 (pilot 1), 302 (pilot 2), **338** (pilot 3) — consistent with the
prior finding that word density is fairly stable across this corpus regardless of
band. The medium-band multiplier used in `audit/GAPS_AND_VERIFICATION.md` §6 (5×,
interpolated between the 1× short and 9× long anchors) can now be checked against a
real measurement: 18 pages / 4 pages (pilot 2) = 4.5×, close to the interpolated 5×.
This is one data point, not a validated band average, but it does not contradict the
existing estimate — see GAPS §6 for the updated effort table.
