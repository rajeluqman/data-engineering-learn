# Ch.7 — Optimizing Materialized Views Recomputes

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Andrea Tardif and Justin Edrington)
**PDF page range:** 74–81 (8 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Materialized View (MV)** [S]: "store precomputed query results as managed tables, allowing users to access complex or frequently used data much faster by avoiding repeated computation of the same queries."

(p74)

**Full recompute** [S]: "overwrites the results in the MV by reprocessing all available data from the source. This can become costly and time-consuming since it requires reprocessing the entire underlying dataset, even if only a small portion has changed."

(p74)

**Enzyme engine** [S]: "efficiently keeps MVs up to date by tracking how new data affects the query results and only updating what is necessary. It utilizes an internal cost model to select among various techniques."

(p74)

**Row tracking (Delta table feature)** [S]: "helps detect which rows have changed since the last MV refresh. It enables Databricks to track row-level lineage in a Delta table and is required for specific incremental updates to materialized views."

(p75)

**`PLAN_NOT_DETERMINISTIC`** [S]: the event-log issue type reported when a non-deterministic expression (e.g., `Rand`) prevents incrementalization: `"issue_type": "PLAN_NOT_DETERMINISTIC", "prevent_incrementalization": true`.

(p78)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter explains how the Enzyme engine decides between incremental and full recomputes for Spark Declarative Pipelines materialized views, demonstrates detecting unexpected full recomputes via the pipeline event log, and shows how to refactor an MV definition to restore incremental refresh.

**WHY** [S]: "many still face challenges in making their ETL pipelines operationally efficient"

(p74), and unnecessary full recomputes waste compute cost and slow data freshness.

**WHEN** [D]: apply this chapter's diagnostic approach whenever a materialized view's refresh cost or latency is higher than expected, or proactively when designing new MVs, to avoid non-deterministic functions and overly complex joins that force full recomputes.

## 3. Assumptions and prerequisites

- [U] This is vendor-authored technical content by named Databricks employees describing Databricks' own Enzyme engine; specific behavioral claims (which functions/join types force full recompute, cost-model internals) reflect the product's behavior at time of writing.
- Requires row tracking enabled on source Delta tables (`delta.enableRowTracking = 'true'`) as a prerequisite for incremental MV updates; deletion vectors (`delta.enableDeletionVectors = 'true'`) are optional but recommended to avoid full-file rewrites on deletes (p75).
- Assumes familiarity with Spark Declarative Pipelines (SDP) and Databricks SQL (DBSQL) MVs. The chapter states "DBSQL MVs launch a managed serverless SDP that is coupled to the MV under the hood"

(p76), so both interfaces behave equivalently under the hood.
- The chapter's own worked examples progress from a small (5-row) demonstration to a billion-row-scale benchmark, explicitly noting "in most cases, the data ingestion is much larger than inserting five rows" (p79) — small-scale examples are for illustrating mechanism, not representative of production cost magnitude.

## 4. Mechanism / key steps

1. Enzyme selects between incremental and full refresh using an internal cost model, generally preferring full refresh "when there are major changes in the underlying data, especially if records have been deleted or modified in ways that the cost model can efficiently compute and apply the incremental change" and incremental refresh "when changes are relatively minor and the source tables are frequently updated" (p74).

2. Enable the Delta table features required for incrementalization on source tables: `delta.enableRowTracking = 'true'` (required) and `delta.enableDeletionVectors = 'true'` (optional, avoids full-file rewrites on row deletion) via `ALTER TABLE ... SET TBLPROPERTIES` (p75).

3. Diagnose refresh behavior via the pipeline event log: query `event_type = 'planning_information'` and inspect the `message` field for `GROUP_AGGREGATE` (incremental refresh occurred) versus `COMPLETE_RECOMPUTE` (full recompute occurred), as demonstrated across a sequence of pipeline runs (p76-78).

4. Reproduce a forced full recompute by adding a non-deterministic function (e.g., `RANDOM()`) directly to the MV's `SELECT` clause; the event log's `planning_information` JSON then reports `"issue_type": "PLAN_NOT_DETERMINISTIC", "prevent_incrementalization": true` for the offending expression (p77-78).

5. Restore incremental refresh by moving non-deterministic value generation out of the MV definition and into the source table itself (i.e., compute the random/dynamic value once at ingestion time, then reference it as a static column in the MV query), which the chapter demonstrates returns the pipeline to `GROUP_AGGREGATE` behavior (p78).

6. Recognize the three documented conditions that automatically trigger a full refresh: use of non-deterministic functions (e.g., `UUID()`, `RANDOM()`), MVs involving complex joins (cross, full outer, semi, anti, or large numbers of joins), or Enzyme's cost model independently determining a full recompute is cheaper (p79).

7. Validate cost/performance impact at production scale: insert 1 billion rows into the initial load and 10 million rows per subsequent run, compare an incremental refresh against a forced full recompute, and use `list_pipeline_events` joined with the billing system table (on `dlt_update_id`) to compute per-update cost — the chapter reports the incremental refresh was "twice as fast and cheaper" than the full refresh at this scale (p79).

8. Monitor refresh behavior operationally using the pipeline event log, the SDP UI, and a provided open-source accelerator tool that uses the Databricks SDK to retrieve pipelines/event details across a workspace and produce an AI/BI dashboard of refresh patterns (p79-80).

## 5. Trade-offs and limitations

- Full refresh is sometimes genuinely the cheaper/correct choice (major source changes, deletions/modifications the cost model can't cleanly incrementalize) — the chapter frames the incremental-vs-full decision as cost-model-driven, not a case where incremental is always preferable (p74).
- Complex joins (cross, full outer, semi, anti, or large numbers of joins) force full recompute regardless of how minor the underlying data change is, meaning MV query design has a direct, sometimes non-obvious, cost consequence (p79).
- Moving non-deterministic value generation into the source table (the chapter's recommended fix) changes where and when that value is computed — this is a semantic change (value fixed at ingestion time rather than recomputed at query time), not merely a performance optimization, and should be evaluated against the actual use case's requirements (p78).
- Deletion vectors are optional, not required, for incrementalization; skipping them still allows row-tracking-based incremental refresh but forces full-file rewrites on deletes instead of the lighter-weight deletion-vector mechanism (p75).

## 6. Failure modes and edge cases

- **Unnoticed full recomputes silently inflating cost**: without event-log monitoring, an MV that has drifted into always performing `COMPLETE_RECOMPUTE` (e.g., due to an added non-deterministic function) can accumulate "increased compute costs," "slower data freshness for downstream applications," and "pipeline bottlenecks as data volumes scale" without any explicit error being raised (p80).
- **Adding a non-deterministic function to an existing incrementally-refreshing MV**: this silently converts the MV to full-recompute-only behavior going forward, as demonstrated by the chapter's own run-by-run event log trace (runs 1-2 incremental, runs 3-4 full recompute after the non-deterministic function and MV definition change) (p77).
- **Missing row tracking on source tables**: without `delta.enableRowTracking = 'true'`, the platform cannot perform the row-level lineage tracking that incremental MV updates depend on, forcing full recompute regardless of query determinism (p75).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when designing a new MV, default to deterministic expressions and simple join patterns (avoiding cross/full outer/semi/anti joins where possible) to keep the MV eligible for incremental refresh from the start, per the chapter's own best-practices list (p80).
- **Build** [D]: enable row tracking (and deletion vectors, where deletes are expected) on source Delta tables as a standard step before building any MV pipeline intended to refresh incrementally (p75).
- **Maintain** [D]: if a use case genuinely requires a non-deterministic or dynamic value in an MV, compute and store that value once in the source table rather than in the MV's `SELECT` clause, to preserve incremental-refresh eligibility (p78).
- **RCA** [D]: if MV refresh costs or latency increase unexpectedly, query the pipeline event log's `planning_information` events first to check for a `COMPLETE_RECOMPUTE` pattern and its stated reason (e.g., `PLAN_NOT_DETERMINISTIC`) before investigating other causes (p76-78).
- **Optimization** [D]: use the chapter's provided accelerator tool (Databricks SDK-based, AI/BI dashboard) to continuously monitor refresh-type patterns across all pipelines in a workspace, rather than manually querying event logs per-pipeline, to catch unexpected full recomputes at scale (p80).

## 8. How to test/verify these claims

- Reproduce the chapter's own worked example: create an MV with deterministic aggregation logic, confirm incremental (`GROUP_AGGREGATE`) refresh via the event log, then add `RANDOM()` to the MV and confirm the event log reports `COMPLETE_RECOMPUTE` with `PLAN_NOT_DETERMINISTIC`, then move the random value to the source table and confirm incremental refresh resumes (p76-78).
- Verify the incremental-vs-full cost/speed claim at scale by replicating the billion-row initial load / 10-million-row incremental insert benchmark, comparing per-update cost and duration between a natural incremental refresh and a forced full recompute via `list_pipeline_events` joined to the billing system table on `dlt_update_id` (p79).
- Verify the complex-join full-recompute trigger by constructing an MV using a full outer or semi/anti join and confirming the event log reports `COMPLETE_RECOMPUTE` even when the underlying source change is minor (p79).
- Cross-check the "incremental refresh compatible functions" list against current Databricks documentation, since the chapter references but does not enumerate the full list in-text (p79).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces Spark Declarative Pipelines at a conceptual level; this chapter details Enzyme's specific refresh-decision mechanics.
- Ch.3 (How Observability in Lakeflow Helps You Build Reliable Data Pipelines): the pipeline event log and AI/BI dashboard monitoring pattern used here directly parallels that chapter's observability approach.
- Ch.4 (A Cost Maturity Journey With Databricks): the `list_pipeline_events`-joined-to-billing-system-table cost-computation technique parallels that chapter's system-tables-based cost reporting.
- Ch.6 (Implement CDC Data Load and SCD Type 2 With Lakeflow): both chapters use Spark Declarative Pipelines' underlying incremental-computation mechanisms (Enzyme here, `apply_changes_from_snapshot` there) for different purposes.
- External GitHub resource referenced but not reproduced: the `monitoring-declarative-pipeline-refresh-behavior` accelerator tool repository and the `MV_Incremental_Technical_Breakdown.ipynb` example notebook (p75, p80).
- Databricks documentation referenced but not reproduced: "Load and process data incrementally with Spark Declarative Pipelines flows" and "Incremental refresh for materialized views" (p81).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Full Python/SDK code for pipeline creation (`w.pipelines.create`, `EventLogSpec`, etc.) | Reproduced only as named mechanism steps in §4; the code is illustrative API usage tied to a specific SDK version. |
| Full event-log run tables (runs 1-5 with message/flow-type/explanation columns) | Represented as the core mechanism narrative in §4 (GROUP_AGGREGATE vs. COMPLETE_RECOMPUTE progression) rather than reproduced as tables; the underlying pattern is fully captured. |
| Embedded diagrams and dashboard screenshots (Enzyme decision diagram, cost/performance bar graph, accelerator dashboard example) | Visual content; described narratively where relevant, not reproduced. |
