# Ch.2 — Migrating Apache Spark ETL Workloads to Databricks

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Dinesh Kumar)
**PDF page range:** 17–21 (5 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Three migration strategies** [S]: "choosing the right strategy: Lift-and-Shift, Refactor or Re-architect. Each option has its trade-offs regarding effort, flexibility and long-term scalability."

(p17)

**Lift-and-Shift** [S]: "the quickest strategy, involving minimal changes to workloads. It lets you immediately leverage Databricks performance and cost benefits, delivering a fast ROI. While it may not be a fully optimized architecture, it accelerates value realization."

(p17)

**Unity Catalog (migration context)** [S]: "the foundation for unifying governance, providing fine-grained permissions across catalogs, schemas, tables, views and columns. It also captures runtime data lineage, enables easy data discovery via the catalog explorer and allows for monitoring through audit logs."

(p18)

**Spark Declarative Pipelines (SDP), migration role** [S]: "simplifies building and managing streaming pipelines by allowing you to use SQL or Python in a declarative format. It automatically handles orchestration, retries and dependencies."

(p19)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter is a migration playbook covering assessment/planning, security/governance setup, code refactoring, streaming-pipeline migration, storage/cluster optimization, testing/validation, and orchestration/monitoring for moving Apache Spark ETL workloads onto Databricks.

**WHY** [S]: "Migrating Spark ETL workloads to Databricks unlocks faster performance, lowers costs and enhances scalability."

(p17)

**WHEN** [D]: apply this playbook when planning an on-premises or other-cloud Spark ETL estate's move to Databricks; the three-tier strategy choice (Lift-and-Shift/Refactor/Re-architect) is explicitly meant to be selected per-workload based on available effort and the target level of optimization, not applied uniformly.

## 3. Assumptions and prerequisites

- [U] This is vendor-authored guidance (a named Databricks author, not an independent third party), so specific tool/feature recommendations (Remorph Transpile, BladeBridge, Remorph Reconcile) reflect the vendor's own tooling ecosystem rather than a neutral survey of migration tools.
- Assumes an existing Spark ETL estate with identifiable batch and streaming workloads, plus documented jobs/workflows/parameters/resource-utilization/execution-frequency/data-consumer metadata as migration planning inputs (p17).
- Assumes familiarity with baseline Databricks/lakehouse concepts (Delta Lake, Unity Catalog, Lakeflow) introduced in the prior chapter of this same source, not re-derived here.

## 4. Mechanism / key steps

1. Assess and plan the migration: inventory existing workloads (classified batch vs. streaming, with jobs/workflows/parameters/resource-utilization/execution-frequency/data-consumer documentation), determine compatibility (identify proprietary/environment-specific features and cloud/service dependencies), and set migration objectives (cost, governance, performance, scalability, architecture simplicity) before choosing a migration strategy (p17).

2. Set up security and governance ahead of scale-out: adopt Unity Catalog for fine-grained permissions/lineage/discovery/audit logging plus built-in data masking and row-level security; use identity federation (Azure AD/Okta) with SCIM provisioning for centralized user/group management and SSO; consider a Data Mesh architecture for federated, domain-owned governance; use Terraform templates to automate and standardize resource deployment (p18).

3. Refactor and optimize code for Databricks compatibility: audit and streamline pipelines for components that may not integrate seamlessly (custom JARs, Hive UDFs, infrastructure-specific configurations), and use automated SQL-conversion tools (Remorph Transpile, BladeBridge) plus Delta Lake's ACID transactions and schema enforcement to modernize data-processing logic (p18).

4. Migrate streaming pipelines using four purpose-built components: Spark Declarative Pipelines (declarative SQL/Python pipeline definition with automatic orchestration/retries/dependency handling, data quality checks, schema evolution, multi-catalog publishing), Auto Loader (incremental cloud-storage ingestion with automatic schema inference/evolution), Structured Streaming (Spark-native streaming with, combined with Delta Lake, low-latency processing/exactly-once semantics/ACID compliance), and Lakeflow Connect (managed connectors for SaaS/database sources via Unity Catalog and serverless compute) (p19).

5. Optimize data storage and access: address small-file issues via auto compaction/optimized writes plus manual `OPTIMIZE`, use Liquid Clustering/Z-Ordering for predicted-field-based data organization, use Delta Caching and the Photon execution engine to reduce query latency, and use predictive optimization to remove manual maintenance-operation management for Unity-Catalog-managed tables (p20).

6. Optimize cluster configuration: use job clusters for ephemeral workloads to minimize idle cost, match VM type to workload shape (memory-optimized for cache-heavy, compute-optimized for high-throughput transformations), enable autoscaling, and use serverless compute for ad hoc queries/BI dashboards to eliminate cluster-management overhead (p20).

7. Test and validate the migration: automate data-accuracy and pipeline-dependency testing (Remorph Reconcile, DataCompy, SQLglot) and benchmark key performance metrics, running new and legacy systems side by side in a phased rollout before full cutover (p21).

8. Migrate orchestration into Lakeflow Jobs incrementally: use the native `DatabricksRunNowOperator` to keep existing Apache Airflow DAGs working during transition, then progressively move workflows to Databricks' native visual interface and YAML-based configuration (p21).

9. Monitor and optimize post-migration using built-in tools (Spark UI, Databricks Metrics UI, System Tables, Cluster Event Logs) to right-size clusters, refine autoscaling, and optimize partitioning/caching as workloads stabilize (p21).

## 5. Trade-offs and limitations

- The three migration strategies trade off effort against architectural quality: Lift-and-Shift is fastest but explicitly "may not be a fully optimized architecture," positioned as a stepping stone ("sets the stage for future enhancements") rather than an end state (p17).
- Job clusters minimize idle cost for ephemeral workloads but implicitly are less suited to persistent/interactive workloads, for which the chapter instead recommends autoscaling clusters or serverless compute — the chapter presents cluster-type choice as workload-dependent, not one-size-fits-all (p20).
- Using `DatabricksRunNowOperator` to keep existing Airflow DAGs working is explicitly framed as a transitional measure ("Over time, consider moving workflows to the Databricks native visual interface"), implying a long-term intent to retire the Airflow-based orchestration rather than run it indefinitely alongside Lakeflow Jobs (p21).

## 6. Failure modes and edge cases

- **Untranslated proprietary/environment-specific features silently breaking on migration**: without an explicit compatibility-determination step, "proprietary or environment-specific features that might not directly translate to Databricks" can cause migrated workloads to fail or behave incorrectly (p17).
- **Custom JARs and Hive UDFs causing instability post-Lift-and-Shift**: the chapter warns that "legacy code might impact performance and stability" if components like "custom JARs, Hive UDFs and infrastructure-specific configurations" are not proactively audited and refactored for the cloud-native environment (p18).
- **Small-file proliferation degrading performance**: without auto compaction, optimized writes, or manual `OPTIMIZE`, growing data volumes on Delta Lake accumulate small-file overhead that degrades query performance (p20).
- **Cutting over without a phased validation period**: skipping a side-by-side run of new and legacy systems removes the safety net the chapter identifies as key to "a low-risk migration with minimal disruption"

(p21), raising the risk of undetected data-accuracy or functional regressions.

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: choose Lift-and-Shift, Refactor, or Re-architect per workload based on documented objectives (cost, governance, performance, scalability, architecture simplicity) from the assessment phase, rather than applying one strategy uniformly across a heterogeneous workload inventory (p17).
- **Build** [D]: proactively refactor custom JARs, Hive UDFs, and infrastructure-specific configuration before or during migration rather than deferring this work, since the chapter identifies these as the specific components most likely to cause post-migration instability (p18).
- **Maintain** [D]: treat `DatabricksRunNowOperator`-based Airflow integration as a bridge, with an explicit plan to migrate workflows to Lakeflow Jobs' native interface/YAML configuration over time, rather than a permanent dual-orchestration setup (p21).
- **RCA** [D]: if a migrated pipeline shows unexpected query latency or resource cost after cutover, check for unaddressed small-file accumulation (missing auto-compaction/OPTIMIZE) and cluster-type mismatch (e.g., compute-optimized VMs used for cache-heavy workloads) before assuming the issue is code-level (p20).
- **Optimization** [D]: adopt Liquid Clustering/Z-Ordering, Delta Caching, Photon, and predictive optimization together as a bundled post-migration storage-optimization pass, and use the built-in monitoring tools (Spark UI, Metrics UI, System Tables, Cluster Event Logs) to drive iterative right-sizing rather than one-time tuning (p20-21).

## 8. How to test/verify these claims

- Verify migration correctness by running Remorph Reconcile, DataCompy, or SQLglot-based automated comparisons between legacy and migrated pipeline outputs during the phased rollout period the chapter recommends (p21).
- Verify the small-file-compaction claim by measuring query latency and file-count metrics on a Delta table before and after enabling auto compaction/optimized writes or running manual `OPTIMIZE`, per the chapter's stated purpose for these features (p20).
- Verify cluster-cost claims by comparing idle-time cost between job clusters and always-on interactive clusters for the same ephemeral workload, per the chapter's stated rationale for using job clusters (p20).
- Cross-check vendor-specific tool claims (Remorph Transpile, BladeBridge, Lakeflow Connect's "fast, scalable and cost-effective" ingestion) against independent benchmarks or Databricks' own technical documentation, since this chapter's claims are vendor-authored and not independently benchmarked in-chapter (p18-19).

## 9. Cross-references

- [[ch01_introduction_to_data_engineering_on_databricks|Ch.1]] (Introduction to Data Engineering on Databricks): introduces Lakeflow Connect, Spark Declarative Pipelines, and Lakeflow Jobs at a conceptual level; this chapter applies them specifically to migration scenarios.
- [[ch06_implement_cdc_and_scd_type_2_with_lakeflow|Ch.6]] (Implement CDC Data Load and SCD Type 2 With Lakeflow) and [[ch07_optimizing_materialized_views_recomputes|Ch.7]] (Optimizing Materialized Views Recomputes), per `audit/CHAPTER_MAP.csv`: later chapters covering specific Lakeflow-based patterns referenced here only at a high level (streaming migration, storage optimization).
- External Databricks documentation referenced but not reproduced: migration strategy documentation, performance-efficiency/tune-file-size/delta-vacuum best practices, cluster configuration and cost-optimization guides, and dashboard/system-tables documentation (p17, p20-21).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Named external documentation links (e.g., "please check out our documentation here," "cluster configuration," "cost optimization for the data lakehouse") | The source text references these as hyperlinks without reproducing their content; not fabricated or followed since this synthesis is scoped to the PDF's own text (p17, p20-21). |
| Full bullet-by-bullet restatement of "Key optimizations" and "Best practices" bullet lists beyond mechanism/implications already captured | Content is captured as mechanism steps in §4 and implications in §7; restating verbatim would duplicate rather than add information. |
