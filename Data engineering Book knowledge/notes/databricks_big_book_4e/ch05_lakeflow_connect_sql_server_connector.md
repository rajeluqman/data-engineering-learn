# Ch.5 — Lakeflow Connect: Efficient and Easy Data Ingestion Using the Microsoft SQL Server Connector

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Andrea Tardif, Prasanna Selvaraj, Hector Bustamante, and Phanitha Kommareddi)
**PDF page range:** 46–61 (16 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**CDC vs. change tracking (CT)** [S]: "CDC provides historical change information about insert, update and delete operations, and when the actual data has changed. Change tracking identifies which rows were modified in a table without capturing the actual data changes themselves."

(p47)

**When to use CT vs. CDC** [S]: "Databricks recommends using change tracking for any table with a primary key to minimize the load on the source database. For source tables without a primary key, use CDC."

(p47)

**Ingestion gateway** [S]: "extracts snapshots, change logs and metadata from the source database" and "lands in a UC Volume, a storage abstraction best for registering non-tabular datasets."

(p48)

**Compute split for Lakeflow Connect** [S]: "while the ingestion pipeline can run on serverless compute, the ingestion gateway for database connectors currently operates on classic compute to simplify connections to the database source. As a result, users might see a combination of classic and serverless Spark Declarative Pipelines DBU charges."

(p59)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter is a technical walkthrough of Lakeflow Connect's SQL Server connector — its architectural prerequisites (region/feature compatibility, CDC/CT requirements, governance/networking), a full worked example configuring ingestion from Azure SQL Server, a real-world case study, and operational best practices (orchestration, cost tracking).

**WHY** [S]: "Maintaining these processes [custom connectors, data prep, enrichment] quickly becomes complex and brittle, slowing down innovation. That's why Databricks developed Lakeflow Connect."

(p46)

**WHEN** [D]: applicable when an organization needs to replicate on-premises or cloud SQL Server data (Azure SQL Database/Managed Instance, RDS for SQL Server, SQL Server on GCP, SQL Server on VMs/EC2, or on-prem via ExpressRoute/Direct Connect) into a Unity-Catalog-governed Databricks lakehouse with minimal custom connector engineering.

## 3. Assumptions and prerequisites

- [U] This is vendor-authored product documentation/tutorial content (four named Databricks employees describing Databricks' own connector); specific behavioral and pricing claims reflect the vendor's own product at time of writing, not independent verification.
- Requires SQL Server 2012+ for change tracking (2016+ recommended); requires SQL Server 2012+ for CDC, with versions earlier than 2016 additionally requiring the Enterprise edition (p49).
- Requires specific Unity Catalog permissions before pipeline creation: `CREATE CONNECTION` on the metastore, `USE CATALOG` on the target catalog, `USE SCHEMA`/`CREATE TABLE`/`CREATE VOLUME` (or `CREATE SCHEMA`), and either unrestricted cluster-creation permission or a custom compute policy via `MANAGE COMPUTE POLICIES` (p48).
- Assumes serverless compute is enabled in the target region; if not, the chapter directs readers to "work with your Databricks Account Team to request help prioritizing development or deployment in that region" (p47).
- Assumes a dedicated database service account is configured for Databricks ingestion, separate from other application credentials (p49, p58).

## 4. Mechanism / key steps

1. Assess architectural fit using four key considerations: region/feature compatibility (does the target region support serverless compute for this connector), change data capture/tracking integration availability on the source, Unity Catalog compatibility, and private networking security requirements (p46-48).

2. Configure Unity Catalog permissions for the ingestion principal (user or service principal): `CREATE CONNECTION` on the metastore, `USE CATALOG` on the target catalog, schema/table/volume creation rights, and compute-policy permissions for the gateway ingestion process (p48).

3. Prepare the SQL Server source: confirm SQL Server version compatibility, configure a dedicated service account, validate cloud-specific privilege requirements, and enable change tracking (`ALTER DATABASE ... SET CHANGE_TRACKING = ON`) and/or CDC (`EXEC sys.sp_cdc_enable_table`) on the relevant tables (p49-50).

4. Configure the SQL Server connector in Databricks via the UI (or equivalently via Databricks Asset Bundles/DABs as code): (a) set up the ingestion gateway with a name, catalog, and schema for the UC Volume; (b) configure the ingestion pipeline and create the SQL Server connection (via UI or `CREATE CONNECTION ... TYPE SQLSERVER`); (c) select tables for replication — whole-schema ingestion for exploration/migration, individual-table ingestion for use-case-specific workflows; (d) configure the destination catalog/schema in UC; (e) configure schedule and failure notifications (p50-53).

5. Validate the pipeline: check the gateway pipeline's event log for `update_progress` entries confirming successful source ingestion, verify sync status (insert/update/UPSERT operation counts), and browse the replicated target table in the destination catalog/schema (p54).

6. Test CDC and schema evolution end-to-end: perform insert/update/delete operations on the source table and confirm they propagate to the Delta target table after the next pipeline run; alter the source table schema (add a column) and confirm the new column appears appended in the target table after re-triggering the pipeline (p55-56).

7. Monitor continuously via the pipeline UI's event log (data quality checks, pipeline progress, data lineage), checking entries such as maturity-level indicators (e.g., `STABLE`, indicating an unchanged schema) (p56-57).

8. Operate the pipeline per Databricks' recommendations: schedule with at least a five-minute interval between executions to balance freshness against cost/overlap risk; use task dependencies within a job so downstream workloads wait for ingestion completion; understand that an overrunning pipeline run causes the next scheduled trigger to be skipped (job-like behavior) (p58).

9. Track cost via system tables: query `system.billing.usage` joined to `system.billing.list_prices`, filtered by `billing_origin_product = 'LAKEFLOW_CONNECT'` and a specific `dlt_pipeline_id`, to compute DBU count and DBU cost per pipeline per day (p59).

## 5. Trade-offs and limitations

- Change tracking minimizes source-database load but only captures which rows changed, not the actual change history — CDC captures full historical change detail (including for tables without a primary key) at presumably higher source overhead, making the CT/CDC choice a load-vs-detail trade-off (p47).
- Whole-schema ingestion is convenient for exploration/migration but the chapter recommends splitting ingestion across multiple pipelines "if the schema is large or exceeds the allowed number of tables per pipeline"

(p52), implying whole-schema ingestion doesn't scale unconditionally.

- The gateway currently runs on classic compute (not serverless) even though the ingestion pipeline itself can run serverless, so cost visibility requires tracking a mix of classic and serverless DBU charges rather than a single unified line item (p59).

- Change tracking's retention window (e.g., `CHANGE_RETENTION = 3 DAYS`) bounds how long an ingestion gateway can be offline before requiring a full refresh: "A full refresh will be required if your gateway is offline longer than the set time"

(p50), making retention duration a direct availability/cost trade-off.

## 6. Failure modes and edge cases

- **Gateway offline longer than the change-tracking retention window**: forces a full refresh of the source table rather than a resumable incremental sync, since change-tracking data older than the retention period is auto-cleaned (`AUTO_CLEANUP = ON` by default) (p50).
- **Overlapping scheduled runs**: "if the pipeline is still running when the next refresh is scheduled"

(p58), the next trigger is skipped rather than queued or run concurrently — a job-like behavior that could mask a pipeline that has grown too slow to keep up with its own schedule.
- **Exceeding the per-pipeline table limit with whole-schema ingestion**: attempting to ingest a schema that "exceeds the allowed number of tables per pipeline" without splitting into multiple pipelines will hit a connector limit and degrade performance, per the chapter's own recommendation to split in this case (p52).
- **Credential exposure risk if not using UC-managed credentials**: the chapter specifically calls out that UC Service and Storage Credentials "are never exposed in logs or hardcoded into SQL ingestion pipelines" as a security property — implying that bypassing UC-managed credential storage (e.g., hardcoding credentials) would reintroduce this exposure risk (p48).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: choose change tracking for primary-keyed tables and CDC for tables without a primary key as the default rule, per the chapter's explicit recommendation, rather than defaulting to CDC universally (which the chapter implies carries more source-side overhead) (p47).
- **Build** [D]: use Databricks Asset Bundles (DABs) to define ingestion gateway and pipeline configuration as code (two YAML files: a workflow file and a pipeline definition file) rather than only UI-based configuration, for repeatability and consistency across environments, per the chapter's own best-practice recommendation (p59, Appendix).
- **Maintain** [D]: configure each ingestion gateway's service account with access scoped only to the replicated source database (least privilege), and maintain at least a five-minute scheduling interval between ingestion runs to avoid cost/overlap issues, per the chapter's stated best practices (p58-59).
- **RCA** [D]: if a pipeline is silently not refreshing on schedule, check whether a prior run is still in progress (causing the next trigger to be skipped) before assuming a scheduling or connectivity failure (p58).
- **Optimization** [D]: split large-schema ingestion across multiple pipelines rather than ingesting an oversized single schema, and use targeted individual-table ingestion (rather than whole-schema) for use-case-specific downstream consumers like a single ML model or dashboard, to reduce unnecessary ingestion volume (p52).

## 8. How to test/verify these claims

- Reproduce the chapter's own worked example: enable CT/CDC on an Azure SQL Server table, configure the connector end-to-end (gateway → pipeline → table selection → destination → schedule), and confirm the initial full load plus subsequent incremental UPSERT-based syncs behave as described (p49-54).
- Verify CDC/schema-evolution propagation by performing insert/update/delete operations and a column addition on the source table, then confirming both the data changes and the new column appear correctly in the target Delta table after the next pipeline run (p55-56).
- Verify the classic-vs-serverless compute cost-split claim by running the provided system-table query against `system.billing.usage`/`system.billing.list_prices` for a real Lakeflow Connect pipeline and confirming both classic (gateway) and serverless (pipeline) DBU charges appear (p59).
- Verify the overlapping-run-skip behavior by deliberately scheduling a pipeline run to overlap with a still-running prior execution and confirming the next trigger is skipped rather than queued (p58).

## 9. Cross-references

- [[ch01_introduction_to_data_engineering_on_databricks|Ch.1]] (Introduction to Data Engineering on Databricks): introduces Lakeflow Connect and Auto Loader at a conceptual level; this chapter is the detailed SQL Server-specific implementation.
- [[ch03_observability_in_lakeflow|Ch.3]] (How Observability in Lakeflow Helps You Build Reliable Data Pipelines): the pipeline event log, data lineage, and System-Tables-based monitoring referenced here overlap directly with that chapter's observability content.
- [[ch04_cost_maturity_journey_with_databricks|Ch.4]] (A Cost Maturity Journey With Databricks): the system-tables-based cost query pattern here (`system.billing.usage` joined to `system.billing.list_prices`) directly parallels that chapter's cost-reporting mechanism.
- [[ch06_implement_cdc_and_scd_type_2_with_lakeflow|Ch.6]] in `audit/CHAPTER_MAP.csv` ("Implement CDC Data Load and SCD Type 2 With Lakeflow"): likely builds directly on this chapter's CDC ingestion foundation for downstream SCD Type 2 dimensional modeling.
- External Databricks documentation referenced but not reproduced: SQL version requirements, connector limits, per-cloud privilege requirements (AWS/Azure/GCP), event log schema documentation, and official Lakeflow Connect pricing documentation (p47-60).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Embedded product screenshots (Azure SQL Server UI, Databricks UI configuration screens at each step, Pipeline Event Log UI/JSON, UC target table views) | Visual content; described narratively where relevant, not reproduced. |
| Full DABs YAML appendix (workflow file, pipeline definition file) | Reproduced only as a named mechanism/build-practice reference in §4/§7; the exact YAML is illustrative, version-specific configuration syntax, not an independently verifiable conceptual claim. |
| Full permission-table reproduction (Permission type / Reason / Documentation columns, p48) | Captured as prose mechanism steps in §3/§4 rather than reproduced as a table; content is fully represented without the tabular formatting. |
