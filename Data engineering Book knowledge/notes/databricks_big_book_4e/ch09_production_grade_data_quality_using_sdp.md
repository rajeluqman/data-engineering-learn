# Ch.9 — Production-Grade Data Quality Using Spark Declarative Pipelines

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Matt Holzapfel)
**PDF page range:** 86–93 (8 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Expectations** [S]: quality constraints applied via "standard SQL Boolean statements" that "apply data quality checks on each record passing through a query," letting teams "capture data quality metrics and automatically take action when issues are found."

(p86-87)

**Two-tier data quality framework design principle** [S]: "Alarm bells go off when there is clearly an issue" (automatic isolation of bad data) versus "Potential issues are flagged so workflows can be built around them" (human review for ambiguous outliers).

(p87)

**Materialized view + streaming table with `EXPECT` limitation** [S]: "when you define a Databricks SQL materialized view directly over a streaming live table that has an EXPECT constraint, the system can't use change data feed to compute 'what's new' vs. 'what's already been processed.' As a result, every REFRESH will re-scan and re-process the entire source."

(p89)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter demonstrates using Spark Declarative Pipelines' `EXPECT` constraints ("expectations") to detect and handle six categories of data quality issues (invalid, incomplete, missing, inconsistent, stale, inaccurate data), including drop-row, warn-only, and quarantine-based violation handling patterns.

**WHY** [S]: "Good data quality isn't just a nice-to-have — it's a necessity, especially in regulated industries like financial services... The success of these AI initiatives relies on high-quality data."

(p86)

**WHEN** [D]: apply expectations-based data quality checks whenever building batch or streaming pipelines where undetected upstream drift (schema changes, new allowed values, truncation, silent data corruption) could otherwise propagate downstream and require costly multi-team root-cause investigation — particularly salient in regulated industries where such issues "can trigger regulatory reviews" (p86).

## 3. Assumptions and prerequisites

- [U] This is vendor-authored technical content by a named Databricks employee describing Databricks' own `EXPECT`/expectations feature; framework recommendations reflect "best practices we've seen" (p86) rather than an independently validated methodology.
- Assumes familiarity with Spark Declarative Pipelines' SQL (`CREATE STREAMING TABLE`, `CREATE OR REFRESH MATERIALIZED VIEW`) and Python (`@dlt.table`, `@dlt.expect_all_or_drop`) authoring surfaces (p88-92).
- Assumes each SDP pipeline has an event log storage location configured, since expectation pass/fail metrics are written there and consumed via the Lakeflow UI or a custom AI/BI dashboard (p87-88).
- The chapter's own worked examples are domain-specific (financial services client onboarding, email marketing prospects) but the underlying patterns (drop-row, warn, quarantine) are presented as general-purpose (p88-93).

## 4. Mechanism / key steps

1. Detect **invalid data** by applying a format/structure constraint with `ON VIOLATION DROP ROW` (e.g., `CONSTRAINT `Emails must contain @` EXPECT (email_address LIKE '%@%') ON VIOLATION DROP ROW`), preventing structurally malformed records from flowing downstream (p88).

2. Detect **incomplete data** (e.g., truncated values) by adding an additional constraint to the same streaming table definition (e.g., checking an email address doesn't end with `@`), stacking multiple `EXPECT` clauses on one table (p89).

3. Detect **missing data** by requiring at least one of several optional fields to be non-null (e.g., `email_address IS NOT NULL or full_address IS NOT NULL or phone_number IS NOT NULL`) on a materialized view, dropping rows that fail (p89).

4. Detect **inconsistent data** by comparing incoming values against a dynamically computed historical statistical range (e.g., mean + 4 standard deviations of `net_worth` over the trailing 180 days, computed via a `bounds` CTE) and flagging/rejecting outliers via an `EXPECT (amount BETWEEN lower_bound AND upper_bound)` constraint on a materialized view built by cross-joining new records with the computed bounds (p90).

5. Detect **stale data** with a warn-only (non-dropping) constraint (e.g., `EXPECT (timestamp >= CURRENT_DATE() - INTERVAL 90 DAYS)` with no `ON VIOLATION` clause specified, i.e., default warn/track behavior), since old data can be legitimate (restatements, backfills) and shouldn't be automatically discarded, only monitored (p90).

6. Detect **inaccurate data** by externalizing validation logic into a rules table (`data_accuracy_rules`, with `name`/`constraint`/`tag` columns) that can be evolved and applied retroactively across many datasets, then loading and applying those rules programmatically via `@dlt.expect_all_or_drop(get_rules('validity'))` in a Python-defined DLT table function (p91-92).

7. Implement quarantine-based handling (rather than drop) for ambiguous violations: tag each row with an `is_quarantined` boolean via an `EXPECT` constraint used for classification rather than dropping, partition the quarantine table by that flag, then split into separate `valid_*`/`invalid_*` downstream streaming tables for differentiated processing (human review for quarantined records) (p92).

## 5. Trade-offs and limitations

- Layering an `EXPECT`-constrained materialized view directly on top of a streaming table with its own `EXPECT` constraint disables incremental refresh: "every REFRESH will re-scan and re-process the entire source, not just the newest data" — the chapter's workaround is to apply `EXPECT` checks upstream and write validated data to a static Delta table instead (p89).
- Drop-row handling (`ON VIOLATION DROP ROW`) is appropriate for clear-cut invalid/incomplete/missing data but inappropriate for ambiguous cases (e.g., statistical outliers, inaccurate-but-plausible data), where the chapter recommends flagging/quarantining for human review instead of automatic rejection (p87, p92).
- Rule-based inaccurate-data detection has no "silver bullet": rules must be "continuously evolve[d]" as new inaccuracy patterns are discovered (e.g., sentinel values like `"9999999999"` for refused income disclosure), meaning this category of data quality issue is inherently reactive/iterative rather than solvable via a fixed rule set (p91).

## 6. Failure modes and edge cases

- **Silent pipeline "success" masking data quality degradation**: "data pipelines often continue to execute normally despite their polluted nature. ETL jobs complete successfully, dashboards update on schedule and everything looks green" — without expectations, there is no signal distinguishing a healthy run from one processing corrupted upstream data (p86).
- **Multi-team, multi-week root-cause investigations**: in the worst case, "the issue lingers for weeks and requires a multi-team investigation to identify and resolve the root cause," with regulated-industry pipelines additionally facing "detailed root cause analyses" and potential "regulatory reviews" (p86).
- **Unintended full re-processing from stacking EXPECT-constrained MV over EXPECT-constrained streaming table**: as described above, this specific composition pattern silently disables incremental refresh, inflating compute cost on every refresh without an explicit error (p89).
- **Automatically dropping ambiguous but potentially legitimate data**: applying a hard drop-row rule to genuinely ambiguous cases (e.g., a large but real net-worth value, or legitimately stale backfilled data) risks discarding valid records — the chapter's flag/quarantine pattern exists specifically to avoid this failure mode (p87, p90, p92).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: design the data quality framework's response tier (auto-drop vs. flag-for-review) based on how unambiguous a violation is, per the chapter's own two-tier principle — reserve automatic dropping for clear-cut violations and route ambiguous ones to human review via quarantine (p87).
- **Build** [D]: externalize accuracy-related validation rules into a dedicated rules table (rather than hardcoding them into pipeline SQL/Python) so they can be updated and retroactively reapplied across datasets as new inaccuracy patterns are discovered, per the chapter's `data_accuracy_rules` pattern (p91).
- **Maintain** [D]: avoid layering an `EXPECT`-constrained materialized view directly over an `EXPECT`-constrained streaming table; instead apply expectations upstream and materialize validated data into a static Delta table, to preserve incremental refresh behavior (p89).
- **RCA** [D]: when investigating a downstream data-quality complaint, first check the SDP pipeline's event log (expectation pass/fail counts per table) rather than manually inspecting data, since this is the chapter's own recommended first line of diagnostic visibility (p87-88).
- **Optimization** [D]: build a centralized AI/BI dashboard over the event log tables across pipelines rather than checking the Lakeflow UI per-pipeline, to make data quality monitoring broadly visible and reduce the time to detect drift (p88).

## 8. How to test/verify these claims

- Reproduce the invalid/incomplete/missing-data examples by creating the chapter's own streaming tables and materialized views with the given `EXPECT` constraints, feeding in deliberately malformed records, and confirming rows are dropped/passed as described (p88-89).
- Verify the incremental-refresh-breaking claim by constructing the specific pattern (MV with `EXPECT` over a streaming table with `EXPECT`) and confirming via query plan or event log that a full re-scan occurs on refresh, contrasted with the upstream-validation-into-static-table workaround (p89).
- Verify the quarantine pattern by feeding both deliverable and non-deliverable welcome-email records through the `clients_profile_quarantine` table and confirming they correctly route to `valid_client_profiles` versus `invalid_client_profiles` (p92).
- Verify the statistical-outlier detection by feeding a `net_worth` value more than 4 standard deviations above the 180-day historical mean and confirming the `validated_net_worth` constraint flags/rejects it as expected (p90).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces Spark Declarative Pipelines' data-quality-check capability at a conceptual level; this chapter provides the detailed implementation patterns.
- Ch.3 (How Observability in Lakeflow Helps You Build Reliable Data Pipelines): the pipeline event log and AI/BI dashboard monitoring pattern used here directly parallels that chapter's general observability approach, applied specifically to data quality metrics.
- Ch.7 (Optimizing Materialized Views Recomputes): the incremental-vs-full-refresh mechanics referenced here (change data feed, `REFRESH` behavior) directly parallel that chapter's Enzyme-engine discussion of what forces a full recompute.
- Databricks documentation referenced but not reproduced: details on accessing the event log table and its full list of available attributes (p87).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Full Python DLT code for the rules-table loading pattern (`get_rules`, `@dlt.expect_all_or_drop`) | Reproduced only as a named mechanism step in §4; the exact code has some apparent transcription artifacts in the source PDF text extraction (garbled ordering/casing across p91-92) and is illustrative API usage rather than an independently verifiable conceptual claim. |
| Full SQL for the quarantine table partitioning and downstream valid/invalid table split | Reproduced only as a named mechanism step in §4; the pattern (tag, partition, split) is fully captured without the verbatim SQL. |
