# Ch.5 — Procurement

**Source:** `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd ed., Kimball & Ross, Wiley)
**PDF page range:** 177–202 (26 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 9,492
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Blended vs. separate transaction fact tables, four decision considerations [S]** (p180): (1) users' analytic requirements and which approach "most naturally aligns with their business-centric perspective"; (2) whether there are "really multiple unique business processes" (evidenced by separate control numbers per step); (3) whether "multiple source systems [are] capturing metrics with unique granularities"; (4) "the dimensionality of the facts" — whether dimensions apply unevenly across transaction types. All four pointed toward separate fact tables in the chapter's own procurement case study.

**Procurement pipeline accumulating snapshot [S]** (p183): crosses purchase order → warehouse receipt → vendor invoice → vendor payment, useful "if the business is interested in monitoring product movement as it proceeds through the procurement pipeline (including the duration of each stage)." Explicit scoping rule: "If the process is a continuous flow that never really ends, it is not a good candidate for an accumulating snapshot."

**Type 0 (Retain Original) [S]** (p184): "the dimension attribute value never changes, so facts are always grouped by this original value" and it is "appropriate for any attribute labeled" original, "such as customer original credit score." Durable supernatural keys are explicitly always type 0.

**Type 1 (Overwrite), with named side effects [S]** (p185–186): "you overwrite the old attribute value in the dimension row, replacing it with the current value." Named consequences: (a) "the same BI applications can produce different results before versus after the type 1 attribute change"; (b) "any preexisting aggregations based on the department value need to be rebuilt"; (c) if deployed via OLAP cube on a hierarchical rollup attribute, "the cube likely needs to be reprocessed."

**Type 2 (Add New Row), the "predominant" and "safest" technique [S]** (p186–188): "a new product dimension row for IntelliKidz is inserted to reflect the new department attribute value... type 2 responses perfectly partition or segment history to account for the change." Explicitly: "there is no need to revisit preexisting aggregation tables when using the type 2 technique... OLAP cubes do not need to be reprocessed." Worked example: a $500 January + $100 February IntelliKidz sale reports as $600-under-Strategy if type 1, but $500-Education/$100-Strategy if type 2.

**Type 2 effective/expiration date mechanics [S]** (p188–189): new dimension row uses "the expiration date... set to December 31, 9999" for the current row, avoiding a null so `BETWEEN` can reliably find the row valid on a given date; the old row's expiration date is set "just prior to the effective date of the new row leaving no gaps."

**Type 1 attributes inside a Type 2 dimension, an explicit mixing case [S]** (p189): "when type 1 and type 2 are both used in a dimension, sometimes a type 1 attribute change necessitates updating multiple dimension rows" (e.g. correcting a product-introduction-date attribute on both the old and new type-2 profile rows).

**Type 3 (Add New Attribute), the "alternate realities" technique [S]** (p190–191): "you do not issue a new dimension row, but rather add a new column to capture the attribute change" — the original attribute is overwritten (type 1 behavior) to the current value while a new "prior" column preserves the old value; "the pair of current and prior attribute values are regarded as true at the same time." Explicitly infrequently used, and unsuitable for unpredictable per-row changes (e.g. a customer's home state) — "These unpredictable changes are typically handled best with type 2 instead." Best suited to en-masse, predictable reorganizations (e.g. sales-territory or product-line restructuring).

**Type 4 (Add Mini-Dimension) [S]** (p192–194): splits "frequently analyzed or frequently changing attributes into a separate dimension" — one row per unique combination of banded attribute values (e.g. age band × income band × purchase-frequency-score), not one row per entity. Continuously variable attributes are "converted to banded ranges" specifically to bound the mini-dimension's row count; the chapter's own worked upper-bound example: 5 attributes × 10 values each = 100,000 possible rows.

**Type 5 (Mini-Dimension + Type 1 Outrigger) [S]** (p196): "add a current mini-dimension key as an attribute in the primary dimension" — itself handled as type 1 (overwritten on every profile change, never tracked as type 2, since that would reintroduce the row-explosion problem type 4 was built to avoid).

**Type 6 (Add Type 1 Attributes to Type 2 Dimension) [S]** (p196–198): combines "a new row to capture the change (type 2) and add a new column to track the current assignment (type 3), where subsequent changes are handled as a type 1 response" — every historical row for a given durable entity gets its "current" column overwritten whenever a new type-2 change occurs, so all rows converge on the same current value while each row's "historic" column preserves what was true at the time.

**Type 7 (Dual Type 1 and Type 2 Dimensions) [S]** (p198–200): the fact table carries both the type-2 surrogate key and the durable natural key; the durable key joins to a type-1 "current" view of the dimension (built from the most-current type-2 rows), letting the same schema answer both as-was (via surrogate key) and as-is (via durable key) queries without adding extra columns to the base dimension — the chapter's own trade-off: "type 7 invariably requires less ETL effort" than type 6 but costs "the additional column carried in the fact table."

**Type 7 for arbitrary point-in-time (as-of) reporting [S]** (p200): filter the type-2 dimension by effective/expiration dates to find the profile valid on any chosen historical date, then join that filtered set to the fact table via the durable key — as if defining "the meaning of" current "on-the-fly." Explicitly flagged: "only unveil this capability to a limited, highly analytic audience; this embellishment is not for the timid."

## 2. WHAT / WHY / WHEN

**WHAT:** The book's third case study (procurement), used to (a) work through the blended-vs-separate transaction fact table design decision and a cross-process accumulating snapshot, and (b) give the fullest treatment in the book of all eight slowly changing dimension techniques (types 0–7), including three advanced hybrids (5, 6, 7). `[D]`

**WHY it matters:** framed directly by the chapter's own governance emphasis: "Dimensional designers must proactively work with the business's data governance representatives to determine the appropriate change-handling strategy... business users may assume the DW/BI system will allow them to see the impact of every attribute value change" (p183–184) — SCD strategy is a business decision, not a default IT setting. `[S]`

**WHEN to use each SCD type, the chapter's own explicit guidance collected:** `[D]` (this note's own synthesis across the chapter's per-type discussions.)

Type 0 for attributes that are permanently fixed by definition (original values, most date-dimension attributes); Type 1 for insignificant corrections or where no value exists in retaining history (p186). `[D]`

Type 2 as the default choice, called "the safest response" (p188), used specifically when "the business is not absolutely certain about the SCD business rules for an attribute" — since type 1-to-type-2 reversal is far harder than the reverse.

Type 3 only for predictable, en-masse reorganizations needing dual current/prior views concurrently, never for unpredictable per-row changes (p191). `[D]`

Type 4 specifically when "the rate of change speeds up" within a large multimillion-row dimension and browsing/query performance is threatened (p192).

Types 5–7 only when the business explicitly needs both current and historically-accurate profiles simultaneously and has confirmed the added complexity is worth it — the chapter's own caution: "You should not pursue these options unless the business agrees they are needed" (p195).

## 3. Assumptions and prerequisites

- Assumes surrogate/durable key vocabulary from Ch.3: "As we staunchly advocated in Chapter 3, the dimension table's primary key is a surrogate key" (p185).

"You'd be vulnerable to the entire list of potential operational issues discussed in Chapter 3" (p189). `[S]`
- Assumes bus matrix and conformed dimension vocabulary from Ch.4: this chapter's Figure 5-2 bus matrix embellishment (atomic granularity/metrics columns) directly extends Ch.4's matrix format. `[S]`
- Assumes SCD types 1–3 as prior, book-recognized vocabulary before this chapter formally extends the numbering: "Kimball method followers are likely already familiar with SCD types 1, 2, and 3" (p184). `[S]`
- Forward-references the detailed implementation bus matrix to Ch.16 (Insurance, p181), multiple mini-dimensions per fact table to Ch.10 (Financial Services, p194–195), dynamic value banding of facts to Ch.10 (p193), and surrogate-key ETL workflow to Ch.19/Ch.20 (p189). `[D]` (this note's own summary of the chapter's forward-references.)

## 4. Mechanism / key steps

**Type 6's row-update propagation on a new type-2 change (p197–198, the chapter's own worked IntelliKidz example):** a department-reassignment event occurs → a new dimension row is inserted (type 2 behavior) with both "historic" and "current" department columns set to the new value → every *other* existing row sharing the same durable product identity has its "current" column overwritten (not its "historic" column) to the new value → the result is that querying by "historic department" correctly segments facts by the department in effect at the time, while querying by "current department" rolls up all historical facts — old and new — under today's organizational structure.

**Type 7 "as of" point-in-time query (p200):** choose an arbitrary historical date → filter the type-2 dimension's rows by `effective_date <= chosen_date AND expiration_date >= chosen_date` to isolate exactly one row per durable key (the profile valid on that date) → join this filtered row set to the fact table via the durable key → aggregate facts using that filtered dimension's attributes, effectively defining a custom "current" as of any chosen moment rather than only today.

## 5. Trade-offs and limitations

- **Type 1's default-choice risk, an explicit warning (p186):** "too often DW/BI teams use a type 1 response as the default for dealing with slowly changing dimensions and end up totally missing the mark if the business needs to track historical changes accurately. After you implement a type 1, it's difficult to change course in the future."
- **Multiple vs. single procurement fact tables' true ETL cost, an explicit correction of intuition (p181):** "Some would argue this approach increases the complexity of the ETL processes. Actually, it may simplify the ETL activities. Loading the operational data from separate source systems into separate fact tables likely requires less complex ETL processing than attempting to integrate data from the multiple sources into a single fact table."
- **Type 4 mini-dimension banding's rigidity, stated directly (p193):** "changing to more discreet bands (such as $30,000–34,999) at a later time is difficult" — the value-banding decision, once implemented, resists later refinement.
- **Type 5's dual-access-path confusion risk (p196):** "presenting users with two avenues for accessing demographic data, through either the mini-dimension or outrigger, can deliver more functionality and complexity than some can handle."
- **Type 6 vs. Type 7's structural trade-off, stated directly (p198–199):** type 6 "spawns more attribute columns in a single dimension table" but needs no extra fact-table column; type 7 "invariably requires less ETL effort" (the current-attribute table is just a view) but costs "the additional column carried in the fact table" and, if that column is avoided by joining through the type-2 dimension instead, "would likely negatively impact query performance for current reporting" — there is no cost-free version of this capability.
- **Hybrid SCD techniques' general complexity warning, stated as an explicit governance gate (p195):** "the price paid for greater analytic flexibility is often greater complexity." "You should not pursue these options unless the business agrees they are needed."

## 6. Failure modes and edge cases

- **Generalizing dimension labels across a blended transaction fact table, a named legibility cost (p181):** if procurement transactions were forced into one blended fact table, "purchase order date and receipt date would likely have been generalized to simply transaction date. Likewise, purchasing agent and receiving clerk would become employee" — a concrete illustration of information loss from over-generalized dimension design.
- **Type 3 misapplied to unpredictable changes, a named failure mode (p191):** "There would be no benefit in reporting facts based on a prior home state attribute that reflects a change from 10 days ago for some customers or 10 years ago for others" — type 3's dual-current-values design assumes a shared, meaningful "before/after" moment, which unpredictable per-entity changes don't have.
- **Un-banded mini-dimensions exploding in size, a named consequence (p193):** "If you stored income at a specific dollar and cents value in the mini-dimension, when combined with the other demographic attributes, you could end up with as many rows in the mini-dimension as in the customer dimension itself" — defeating the entire purpose of the type 4 technique.
- **Forgetting to filter Type 7's dimension by effective/expiration dates during as-of queries, an explicit named error (p200):** "you must filter on the row effective and expiration dates, or you'll have multiple type 2 rows for each durable key" — producing incorrect fan-out in the join to the fact table.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the four-consideration blended-vs-separate fact table checklist (§1) is a directly reusable design decision framework for any new multi-step business process in this vault's projects, extending the general principle already established in Ch.4's inventory-transaction dimensionality discussion. `[D]`
- **Build:** the Type 2 effective/expiration-date-with-no-nulls pattern (§1, p188–189) is a concrete, source-backed ETL build requirement — always default the expiration date to a far-future sentinel (e.g. 9999-12-31), never null, so `BETWEEN`-style queries work reliably.
- **Maintain:** the Type 1 aggregate-rebuild obligation (§1/§5) is a concrete maintenance checklist item — any type 1 attribute change on a hierarchical rollup column must trigger a rebuild of dependent aggregate tables/OLAP cubes, not just the base dimension update.
- **RCA:** the "same report gives different numbers before/after a type 1 change" failure mode (§5) is a direct diagnostic hypothesis for "why did this month-over-month comparison suddenly change" investigations — check for a recent type 1 overwrite on a grouping attribute before assuming a data-quality bug.
- **Optimization:** the mini-dimension row-count upper-bound calculation (§1, attributes × values per attribute) is a directly reusable sizing exercise before committing to a type 4 design — confirm the combinatorial row count stays well below the base dimension's row count before implementing.

## 8. How to test / verify these claims

- The Type 2 "reports look identical whether generated before or after the change" claim (§1) is directly testable: run the same historical report before and after inserting a type-2 change, and confirm identical results for pre-change date ranges.
- The mini-dimension row-count bound (§1, 5 attributes × 10 values = 100,000) is directly recomputable arithmetic — not an unverifiable claim.
- The Type 7 "as of" query mechanism (§4) is directly testable by constructing a small type-2 dimension with known effective/expiration date ranges and confirming the date-filtered join produces exactly one row per durable key for any chosen historical date.
- The claim that separate fact tables "may simplify" ETL versus a blended table (§5) is presented as the authors' own field-experience correction of a common intuition, not a formal benchmark — `[S]` as the book's stated position, `[U]` as a universally measured result across all ETL toolchains.

## 9. Cross-references

- Directly extends and is fully consistent with the already-synthesized `kimball_dwtoolkit_3e` [[ch01_dw_bi_dimensional_modeling_primer|Ch.1]] (SCD types 1–3 introduced at a glossary level), [[ch02_dimensional_modeling_techniques_overview|Ch.2]] (SCD types 0, 4–7 defined at glossary level), [[ch03_retail_sales|Ch.3]] (surrogate/durable keys, degenerate dimensions), and [[ch04_inventory|Ch.4]] (bus matrix, accumulating snapshots) — this chapter is the fullest worked treatment of the complete SCD 0–7 taxonomy in the book, giving concrete worked examples (IntelliKidz, demographic mini-dimensions) for techniques [[ch02_dimensional_modeling_techniques_overview|Ch.2]] only defined abstractly. No contradiction found.
- The SCD types 1–3 material here is fully consistent with the independently-synthesized summary already given in `fundamentals_de` [[ch08_customer_relationship_management|Ch.8]] §1 — that source's brief treatment ("Type 1 is the default behavior of most data warehouses, and Type 2 is the one we most commonly see used in practice") is directly corroborated by this chapter's own guidance (Type 2 as the "safest" and "predominant" choice). No contradiction; this chapter is now the vault's authoritative, fullest source for SCD mechanics.
- Forward-references within this same source to [[ch10_financial_services|Ch.10]] (Financial Services — multiple mini-dimensions, dynamic value banding, supertype/subtype schemas), [[ch16_insurance|Ch.16]] (Insurance — detailed implementation bus matrix), and [[ch19_etl_subsystems_and_techniques|Ch.19]]/20 (ETL Subsystems — surrogate key administration workflow) — none yet synthesized. Flagged for `check_deferred_refs.py`.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 5-1 through 5-17 (procurement schema diagrams, bus matrix snippet, multiple fact table diagrams, accumulating snapshot schema, all SCD sample-row tables, SCD summary table) | Captions and content described narratively above where load-bearing (§1, §4); diagrams and full sample-row tables not reproduced verbatim for this chapter. |
| Full procurement analytic-requirements bullet list (p178, vendor performance metrics) | Representative items captured in §1's context; complete list not reproduced verbatim. |
| Multiple Type 3 attributes variant detail (p192, annual department-reassignment example) | The core Type 3 mechanism and its "alternate realities" framing are captured in §1; this variant (multiple year-stamped type-3 columns) is a direct extension not separately elaborated to avoid redundant detail. |
| Full SCD summary table (Figure 5-17) | The per-type dimension-action/fact-impact summary is already captured type-by-type in §1; the consolidated table itself is not reproduced verbatim. |
| Chapter summary closing remarks (p201) | Restates points already captured in §1/§2; not separately reproduced. |
