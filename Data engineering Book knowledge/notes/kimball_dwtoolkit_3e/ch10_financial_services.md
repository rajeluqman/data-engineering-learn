# Ch.10 — Financial Services

**Source:** `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd ed., Kimball & Ross, Wiley)
**PDF page range:** 317–332 (16 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Scope disclaimer, stated up front [S]** (p317): "industry focused chapters like this one are not intended to provide full-scale industry solutions... the techniques are certainly applicable to other businesses. If you don't work in financial services, you still need to read this chapter."

**Dimension triage / the "too few dimensions" trap [S]** (p320): "most dimensional models end up with between five and 20 dimensions. If you are at or below the low end of this range, you should be suspicious that dimensions may have been inadvertently left out of the design." The chapter's own checklist of commonly-missing dimension types to check for: causal dimensions, multiple date dimensions, degenerate dimensions, role-playing dimensions, status dimensions, an audit dimension, junk dimensions — all cross-referenced to their originating chapters (Ch.3, Ch.4, Ch.6). A general test is given: "Any descriptive attribute that is single-valued in the presence of the measurements in the fact table is a good candidate to be added to an existing dimension or to be its own dimension" (p320).

**Supertype and subtype fact/dimension schemas, the chapter's central technique [S]** (p321): "in this chapter we use the basic object-oriented terms supertype and subtype to refer respectively to the single fact table covering all possible account types, as well as the multiple fact tables containing specific details of each individual account type. In past writings these have been called core and custom fact tables, but it is time to change to the more familiar and accepted terminology."

The supertype table provides "the global view, including the ability to slice and dice all accounts simultaneously, regardless of their product type" (p329).

Each subtype table is "limited to just" one line of business (p329), and "must also contain the supertype facts and attributes to avoid joining tables from the supertype and subtype schemas for the complete set of facts and attributes" (p330).

**Account status as a full dimension, not an embedded code [S]** (p322): "Rather than whipsawing the large account dimension, or merely embedding a cryptic status code or abbreviation directly in the fact table, we treat status as a full-fledged dimension with descriptive status decodes, groupings, and status reason descriptions... you could consider the account status dimension to be another example of a mini-dimension."

**Household dimension, why it's kept separate from account [S]** (p323): "In a large bank, the account dimension is huge, with easily over 10 million rows that group into several million households... given the changing nature of the relationship between accounts and households, you elect to use the fact table to capture the relationship, rather than merely including the household attributes on each account dimension row. In this way, you avoid using the type 2 slowly changing dimension technique with a 10-million row account dimension."

**Account-to-customer bridge table with weighting factors [S]** (p323): "an account can have one, two, or more individual account holders." "This is another classic example of a multivalued dimension." "At a minimum, the primary key of the bridge table consists of the surrogate account and customer keys."

"You assign a numerical weighting factor to each account holder such that the sum of all the weighting factors is exactly 1.00" (p324).

Two report types follow directly from this: applying the weighting factor produces what the chapter calls a correctly weighted report, while skipping it produces an impact report (p324).

"Business users understand impact analyses may result in overcounting because the facts are associated with both account holders" (p324).

**Bridge table over grain change, the chapter's own three-part justification for not multiplying facts physically [S]** (p324): changing the fact grain to account-holder level and physically multiplying facts by weighting factor "is rarely done for three reasons. First, the size of the fact table would be multiplied by the average number of account holders. Second, some fact tables have more than one multivalued dimension... Finally, you may want to see the unallocated numbers, and it is hard to reconstruct these if the allocations have been combined physically with the numeric facts."

**Mini-dimension for a bridge-linked entity, an explicit extension of the type-4 mini-dimension pattern [S]** (p327): when the entity reached through a bridge table (here, customer) is itself a rapidly changing monster dimension, "the solution is to add a foreign key reference in the bridge table to the demographics dimension, as shown in Figure 10-6."

The resulting composite key is described directly: "the key for the bridge table now consists of the account key, customer key, and demographics key" (p327), and change tracking on that key can be restricted to align with the fact table's own grain (here, month-end).

**Dynamic value banding of facts, an explicit SQL-capability gap named directly [S]** (p328): "SQL has no generalization of the GROUP BY clause that clumps additive values into ranges." Fix: a band definition table joined to the fact table "using a pair of less-than and greater-than joins," letting users redefine bands at query time; "the report uses the band range name as the row header and sorts the report on the sort order attribute."

**Value-band query performance warning, an explicit named risk [S]** (p328): "A value band query is by definition very lightly constrained... you may need to place an index directly on the balance fact. The performance of a query that constrains or groups on the value of a fact-like balance will be improved enormously if the DBMS can efficiently sort and compress the individual fact."

This indexing approach is attributed directly: "This approach was pioneered by the Sybase IQ columnar database product in the early 1990s and is now becoming a standard indexing option on several of the competing columnar DBMSs" (p328).

**Supertype fact table's own hard content limit, an explicit rule for the "Swiss cheese" failure it prevents [S]** (p329): "You cannot accommodate incompatible facts in the supertype fact table because there may be several hundred of these facts when all the possible account types are considered." Trying to force line-of-business-specific facts/attributes into the shared tables instead "would resemble Swiss cheese, littered with data holes."

**Subtype account dimension as a shrunken conformed dimension [S]** (p330): "The keys of the subtype account dimensions are the same keys used in the supertype account dimension, which contains all possible account keys."

Each subtype account dimension is explicitly described as "a shrunken conformed dimension with a subset of rows from the supertype" account dimension table (p330).

**Hot swappable dimensions [S]** (p332): "A brokerage house may have many clients who track the stock market. All of them access the same fact table of daily high-low-close stock prices. But each client has a confidential set of attributes describing each stock. The brokerage house can support this multi-client situation by having a separate copy of the stock dimension for each client, which is joined to the single fact table at query time. We call these hot swappable dimensions."

The named implementation cost is stated directly: "referential integrity constraints between the fact table and the various stock dimension tables probably must be turned off to allow the switches to occur on an individual query basis" (p332).

## 2. WHAT / WHY / WHEN

**WHAT:** A retail-banking case study built around a monthly account-balance snapshot fact table, used as the vehicle to teach seven techniques: dimension triage, household dimensions, bridge tables with weighting factors, mini-dimensions attached through a bridge table, dynamic value banding, supertype/subtype schemas for heterogeneous products, and hot swappable dimensions. `[D]`

**WHY it matters:** every technique here is explicitly framed as portable beyond banking — the supertype/subtype pattern is directly generalized to "a technology company that sells hardware, software, and services" (p331), and dimension triage, bridge tables, and mini-dimensions are all reused verbatim from earlier chapters (Ch.3–Ch.8) rather than reinvented, making this chapter primarily an integration exercise across the whole book's technique set applied to one difficult domain (heterogeneous products sharing one customer base). `[D]`

**WHEN to build a supertype/subtype family of schemas vs. a single fact table (p330–331):** build supertype-only when the business processes and metrics genuinely don't vary by product line (e.g. new-account solicitation counts); add subtype fact tables specifically for "fact tables where a single logical row contains many product-specific facts" that differ sharply by line of business (e.g. checking vs. certificates of deposit) (p331).

The chapter states plainly that "it makes less sense to combine data from more than one subtype schema, because by definition, the accounts' facts and attributes are disjointed" (p330).

**WHEN to add a bridge-linked mini-dimension vs. a plain type-4 mini-dimension (p326–327):** use the plain type-4 pattern when the volatile attribute set belongs to an entity that already has its own direct foreign key in the fact table; use the bridge-embedded variant specifically when that volatile entity (customer) is reached only through a multivalued bridge table, so the demographics key must live in the bridge table's own composite key rather than in the fact table.

## 3. Assumptions and prerequisites

- Assumes causal dimensions from Ch.3 (Retail Sales), multiple date dimensions from Ch.4 (Inventory), degenerate/role-playing/junk dimensions and audit dimension from Ch.3/Ch.6 (Order Management) — all directly cited in the dimension-triage checklist (p320). `[S]`
- Assumes mini-dimension mechanics (type 4, banded attribute values) from Ch.5 (Procurement) and Ch.4 — directly reused and extended here for the bridge-embedded variant (p322, p325–326). `[S]`
- Assumes bridge table time-stamping for time-variant relationships from Ch.7 (Accounting): "The time stamping of bridge table rows, as discussed in Chapter 7: Accounting, for time-variant relationships is also applicable in this scenario" (p323). `[S]`
- Assumes customer-dimension attribute volatility discussion from Ch.8 (Customer Relationship Management), directly invoked for the "rapidly changing monster dimension" framing (p326). `[S]`
- Assumes semi-additive fact handling (average, not sum, over time) from Ch.4's inventory balances, directly reapplied to account balances: "Remember account balances are just like inventory balances in that they are not additive across any measure of time" (p321). `[S]`

## 4. Mechanism / key steps

**Dimension triage applied to the initial two-dimension design (p319–321):** start from grain declaration (one row per account per month) → notice the naive design collapses branch, product, household, and customer into the account dimension → recognize this violates natural business groupings and risks unmanageable type-2 row growth in a huge account dimension → split branch and product into their own dimensions because they change "slowly, but on different rhythms" (p320) and users think of them as distinct → apply the checklist of commonly-missing dimension types → arrive at the seven-dimension supertype schema (month, branch, account, primary customer, product, account status, household).

**Bridge table with weighting factor construction (p323–324):** for each account with N account holders, create N bridge rows, each carrying a weighting factor such that all weights for that account sum to exactly 1.00 → to produce a correctly weighted report, multiply fact values by the weighting factor at query time via the bridge join → to produce an impact report, join without applying weights, accepting overcounting as an understood trade-off → optionally wrap both variants in SQL views so BI tools see what looks like a normal fact-to-dimension join.

**Supertype/subtype schema construction (p329–331):** build one supertype fact table + supertype account/product dimensions carrying only facts and attributes common across all lines of business → for each line of business needing deep analysis, build a subtype fact table (widened with LOB-specific facts, but still containing the supertype facts too) and a subtype account/product dimension (a shrunken conformed dimension using the exact same surrogate keys as the supertype table, filtered to just that LOB's accounts) → business users choose either the supertype schema (cross-product analysis) or exactly one subtype schema (LOB-specific analysis), never combining subtype schemas directly.

## 5. Trade-offs and limitations

- **Household vs. account as separate dimensions is explicitly called a judgment call, not a hard rule (p323):** "The decision to treat account and household as separate dimensions is somewhat a matter of the designer's prerogative" — justified here specifically by account-dimension size (10M+ rows) and household-membership volatility, not as a universal pattern.
- **Weighting-factor bridge tables can grow to "hundreds of millions of rows" (p325–326)** when both account and customer dimensions are type-2 and the bridge accumulates history — the chapter's own stated motivation for embedding a demographics mini-dimension key directly in the bridge rather than in the customer dimension.
- **Banded mini-dimension attributes lose discrete precision, an explicitly named two-case exception (p326):** "data mining analysis often requires discrete values rather than fixed bands to be effective," and "a limited number of power analysts may want to analyze the discrete values" — fix is to keep the banded mini-dimension attribute for routine reporting while also storing the raw discrete value as a fact, "uniquely labeled so that they are distinguishable," with an explicit reminder to "carefully balance the incremental value... versus the cost in terms of additional complexity for both the ETL processing and BI presentation."
- **Hot swappable dimensions require disabling referential integrity (p332):** a direct, named operational cost of the technique, not a free convenience.

## 6. Failure modes and edge cases

- **Overcollapsing dimensions into one giant account table, a named anti-pattern with two concrete failure consequences (p319–320):** "it does not adequately reflect the natural business dimensions" (usability failure) and creates "type 2 slowly changing dimension effects potentially causing this huge dimension to mushroom into something unmanageable" (performance/storage failure).
- **Forcing all line-of-business facts and attributes into shared supertype tables, the named "Swiss cheese" failure (p329):** "you would end up with hundreds of special facts, most of which would have null values in any specific row... The resulting tables would resemble Swiss cheese, littered with data holes."
- **Impact reports silently double-counting shared account balances across joint holders (p324):** a named, expected consequence of skipping weighting factors, not a bug: "Business users understand impact analyses may result in overcounting because the facts are associated with both account holders." The report's semantics must be clearly labeled to prevent misinterpretation.
- **Physically multiplying facts by weighting factor at ingestion time, three named concrete costs if attempted anyway (p324):** fact table size multiplied by average account-holder count, combinatorial blowup when more than one multivalued dimension exists on the same fact table, and loss of the ability to recover unallocated (pre-weighting) totals.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the dimension-triage checklist (§1/§4, "five and 20 dimensions" heuristic plus the seven named dimension types to check for) is a directly reusable design review step for any new fact table in this vault's projects, not specific to banking. `[D]`
- **Build:** the supertype/subtype pattern (§4) directly informs any schema serving heterogeneous product/service lines against one shared customer base — the specific rule that subtype tables must duplicate supertype facts/attributes (to avoid cross-schema joins) is a concrete, reusable build constraint.
- **Maintain:** the bridge-embedded mini-dimension technique (§4, p326–327) is a directly reusable maintenance pattern whenever a multivalued-bridge-linked dimension itself becomes a rapidly changing monster dimension.
- **RCA:** a report showing inflated totals when summarizing by individual account holder is a direct diagnostic match for the impact-report overcounting failure mode (§6) — check whether weighting factors were applied before assuming a data-quality bug.
- **Optimization:** the value-band query performance warning (§1, p328) is a directly reusable optimization hypothesis for any lightly-constrained, large-scan reporting query — consider columnar/compressed indexing on the constrained fact column rather than assuming the band-table join itself is the bottleneck.

## 8. How to test / verify these claims

- The weighted-vs-impact report distinction (§4) is directly testable: construct a small joint-account dataset with known weighting factors, and confirm the weighted-report sum matches the unweighted account total while the impact-report sum (by individual) exceeds it exactly by the shared-account overlap.
- The supertype/subtype key-consistency claim (§1, p330) is directly testable: confirm that a given account's surrogate key is identical across the supertype and subtype account dimension tables.
- The bridge-table weighting-factor-sums-to-1.00 invariant (§1, p324) is a directly testable data-quality constraint on any bridge table implementing this pattern.

## 9. Cross-references

- Directly extends the mini-dimension technique from [[ch05_procurement|Ch.5]] (Procurement) and [[ch04_inventory|Ch.4]] (Inventory), the bridge-table time-stamping technique from [[ch07_accounting|Ch.7]] (Accounting), and the customer-dimension volatility discussion from [[ch08_customer_relationship_management|Ch.8]] (Customer Relationship Management) — this chapter's bridge-embedded mini-dimension design is a genuinely new combination not previously synthesized, and is fully consistent with the individual techniques as described in those earlier chapters. No contradiction found.
- The dimension-triage checklist restates (without contradiction) degenerate dimensions, role-playing dimensions, junk dimensions, and the audit dimension exactly as synthesized from [[ch03_retail_sales|Ch.3]] and [[ch06_order_management|Ch.6]].
- The supertype/subtype terminology explicitly supersedes the earlier "core and custom fact tables" terminology used in the same book's own past writings (p321) — noted here as the book's own internal terminology update, not a vault inconsistency.
- No forward-references to not-yet-synthesized chapters were found in this chapter's body.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 10-1 through 10-9 (bus matrix snippet, schema diagrams, dynamic value band report) | Structure and content described narratively above where load-bearing (§1, §4); full diagrams and the bus-matrix X-grid not reproduced verbatim. |
| Full checking-account subtype fact/dimension attribute lists ("+10 more facts," "+12 more attributes," p330) | Representative attributes captured in §1/§4; the book's own truncated lists are not expanded since the full lists are not present in the source itself. |
| Chapter summary closing remarks (p332) | Restates points already captured in §1/§2; not separately reproduced. |
