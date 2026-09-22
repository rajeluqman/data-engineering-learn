# Ch.6 — Implement CDC Data Load and SCD Type 2 With Lakeflow

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Cary Moore)
**PDF page range:** 62–73 (12 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Three primary data warehousing tasks** [S]: "1. Ingest data from the source, 2. Populate and transform data for reporting, 3. Leverage Slowly Changing Dimensions Type II methodology (maintain history)."

(p62)

**"Poor man's" CDC** [S]: implementations "such as 'Last Update Date,' other date filters or difference operations, are often performed due to a lack of control on the source database," with "deficiencies in capturing deletes in the source data, requiring additional operations to determine those transactions."

(p62)

**Gateway pipeline** [S]: "Creates a staging volume, connects to your SQL Server database, extracts a snapshot and change data and stores it in the staging volume... It's recommended to run the gateway as a continuous pipeline to avoid gaps in change data due to change log retention policies on the source database."

(p66)

**Ingest pipeline** [S]: "Applies the initial snapshot and subsequent change data from the gateway pipeline (stored in the staging volume) into destination streaming tables. It's important to note that only one ingestion pipeline per gateway is supported."

(p66)

**SCD Type 2 tracking columns** [S]: "our SCD table now has '__START_AT' and '__END_AT' columns used to determine the 'current' value."

(p72)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter walks through implementing end-to-end CDC-based ingestion from SQL Server into a Bronze/Silver medallion architecture on Databricks, using Lakeflow Connect for ingestion and Spark Declarative Pipelines' `apply_changes_from_snapshot` capability to build an SCD Type 2 Silver table.

**WHY** [S]: "Before Databricks, developers would need a separate tool for each function and have to maintain them, adding a lot of complexity."

(p62)

**WHEN** [D]: applicable when a data warehouse project needs to preserve historical versions of changing dimension records (customers, accounts, etc.) sourced from a CDC/CT-enabled SQL Server database, without assembling separate ingestion, transformation, and history-tracking tools.

## 3. Assumptions and prerequisites

- [U] This is vendor-authored tutorial content by a named Databricks employee; specific product-capability claims (e.g., "native SCD type 2 is on the roadmap") reflect the product's state at time of writing and should be re-verified against current documentation before relying on them.
- Requires a SQL Server source with either change tracking or CDC enabled, and a dedicated database user with read/execute privileges on the necessary procedures and change logs (p62).
- Assumes a Unity Catalog environment where the connection-setup step creates a foreign catalog (for query federation) distinct from the managed catalog required for ingestion — these are explicitly not interchangeable (p65, p67).
- Assumes familiarity with the Databricks Medallion architecture (Bronze/Silver/Gold layers) as a prerequisite organizing concept, used here without full re-derivation (p71).

## 4. Mechanism / key steps

1. Enable CDC or change tracking on the SQL Server source: create a dedicated database user with read/execute privileges on necessary procedures and change logs, then decide between change tracking (captures that rows changed, not the operations) and CDC (captures every operation) per source-table needs (p62).

2. Create an external connection in Databricks to the SQL Server instance via Catalog > External Data > Connections, selecting an auth type (username/password or OAuth), certificate options, and "Read only" application intent (p63-64).

3. Create a foreign catalog during connection setup, mapping the SQL Server database to a Unity Catalog catalog — this catalog is for query federation via Lakehouse Federation and is explicitly not reusable as the ingestion pipeline's managed catalog (p65, p67).

4. Create the two-part ingestion pipeline: a gateway pipeline (creates a staging volume, connects to the source, extracts snapshot + change data into staging; recommended to run continuously to avoid gaps from source-side change-log retention limits) and an ingest pipeline (applies snapshot + change data from staging into destination streaming tables; one ingest pipeline per gateway, requiring multiple gateway-ingest pairs for multiple destination catalogs/schemas) (p66-70).

5. Select source tables (whole schema or individual tables) and configure the destination schema, schedule, and notification settings for the ingestion pipeline, then save and run to launch both gateway and ingest pipelines together (p68-70).

6. Structure the target as a Bronze/Silver medallion layout: Bronze holds the raw replicated tables (customers, transactions) as ingested; Silver applies SCD Type 2 change tracking on top of the Bronze data (no Gold layer used, since the chapter's scope is CDC/SCD demonstration only) (p71).

7. Implement SCD Type 2 via a Spark Declarative Pipeline using the `apply_changes_from_snapshot` capability (since native SCD Type 2 support is, per the chapter, on Databricks' roadmap rather than yet available): read from the replicated Bronze customer table and apply changes from the last version into a new SCD Type 2 Silver table, which gains `__START_AT`/`__END_AT` columns to determine the current record version (p71-72).

8. Validate the SCD Type 2 behavior by updating a source record's attribute (e.g., customer email), running the ingest + SCD Type 2 pipeline, and confirming the Silver table reflects the new value alongside correct `__START_AT`/`__END_AT` boundaries for both the old and new record versions (p72).

## 5. Trade-offs and limitations

- "Poor man's" CDC approaches (date-filter or diff-based) avoid needing source-database-level CDC/CT support but are deficient at capturing deletes, requiring extra logic to detect them — genuine CDC/CT avoids this gap but requires source-database configuration access (p62).
- Running the gateway pipeline continuously avoids gaps in change data caused by source-side change-log retention policies, implying that running it on a less-frequent schedule risks losing changes that fall outside the retention window before the gateway next runs (p66).
- Only one ingest pipeline is supported per gateway; writing to multiple destination catalogs/schemas requires multiple full gateway-ingest pipeline pairs, multiplying the operational surface area for multi-destination use cases (p66).
- Native SCD Type 2 support is described as roadmap-only at time of writing, so the chapter's `apply_changes_from_snapshot`-based approach is a workaround, not the eventual first-class mechanism — readers should check current documentation for whether native support has since shipped (p71).

## 6. Failure modes and edge cases

- **Attempting to reuse the connection-setup foreign catalog as the ingestion catalog**: the chapter explicitly warns "the catalog created during the connection setup cannot be used, as that is a foreign catalog for query federation, and the ingestion requires a managed catalog" — doing so would misconfigure the ingestion pipeline (p67).
- **Gateway running on an infrequent schedule against a source with limited change-log retention**: risks silently losing changes that age out of the source's change log before the gateway captures them, since the chapter frames continuous gateway operation as the mitigation for exactly this gap (p66).
- **Assuming a single ingest pipeline can serve multiple destination catalogs/schemas**: this is explicitly unsupported ("only one ingestion pipeline per gateway is supported"), so attempting it without creating additional gateway-ingest pairs would fail to route data to the intended additional destinations (p66).
- **Deletes going undetected under "poor man's" CDC**: date-filter or diff-based pseudo-CDC methods do not naturally surface deleted source rows, requiring separate logic to detect and propagate deletes that genuine CDC captures natively (p62).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: structure CDC-based ingestion into a Bronze (raw replicated) / Silver (SCD Type 2) layout as the default pattern for tracking historical changes to source dimension data, reserving Gold for downstream aggregation/reporting needs beyond this chapter's scope (p71).
- **Build** [D]: use genuine SQL Server CDC or change tracking rather than "poor man's" date-filter/diff-based approaches whenever source-database-level access is available, specifically to avoid the delete-detection gap inherent to the latter (p62).
- **Maintain** [D]: run the gateway pipeline continuously (not on a periodic batch schedule) whenever the source database's change-log retention window is short relative to the desired ingestion cadence, to avoid silently dropped changes (p66).
- **RCA** [D]: if an SCD Type 2 table shows a gap in historical versions or a missing change, check whether the gateway pipeline's schedule allowed a source change-log retention window to lapse before the gateway captured the change, rather than assuming an SCD-layer logic bug (p66).
- **Optimization** [D]: when multiple destination catalogs/schemas are needed, deliberately provision multiple gateway-ingest pipeline pairs up front rather than attempting to force a single pipeline to serve multiple destinations, since the platform enforces a strict one-ingest-pipeline-per-gateway relationship (p66).

## 8. How to test/verify these claims

- Reproduce the chapter's own worked example: enable CDC/CT on a SQL Server source, configure the connection/gateway/ingest pipelines, build the Bronze→Silver SCD Type 2 pipeline via `apply_changes_from_snapshot`, then update a source record's attribute and confirm the Silver table reflects both the new value and correct `__START_AT`/`__END_AT` boundaries on the old and new rows (p72).
- Verify the delete-detection gap in "poor man's" CDC by deleting a row from a source table under a date-filter-based ingestion approach and confirming the deletion is not automatically reflected downstream without additional logic, contrasted with genuine CDC/CT-based ingestion (p62).
- Verify the gateway continuous-operation claim by configuring a gateway on a periodic (non-continuous) schedule against a source with a short change-log retention window, and confirming changes made and retired within that window are lost, versus preserved under continuous gateway operation (p66).
- Verify the one-ingest-pipeline-per-gateway constraint by attempting to configure a second ingest pipeline against an existing gateway targeting a different destination catalog, and confirming the platform requires a separate gateway-ingest pair instead (p66).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces Lakeflow Connect and Spark Declarative Pipelines at a conceptual level, both directly applied here.
- Ch.5 (Lakeflow Connect: SQL Server Connector): provides the detailed connector setup and CDC/CT configuration this chapter builds directly upon (gateway/ingest pipeline architecture, CDC/CT enablement steps overlap substantially).
- Ch.7 in `audit/CHAPTER_MAP.csv` ("Optimizing Materialized Views Recomputes"): likely a natural next step for optimizing the Silver/Gold transformation layer once CDC/SCD ingestion is in place.
- Kimball dimensional modeling SCD Type 1/2/3 concepts (already synthesized in `kimball_dwtoolkit_3e` ch.1-2 of this vault): this chapter is a concrete Databricks-native implementation of the SCD Type 2 pattern described conceptually there.
- External SQL Server CDC/CT documentation referenced but not reproduced, for privilege requirements and CDC-vs-CT decision guidance (p62).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Embedded product screenshots (connection-creation UI, catalog-creation UI, gateway/ingest pipeline configuration screens, pipeline run results, SCD table query output) | Visual content; described narratively where relevant, not reproduced. |
| Full `apply_changes_from_snapshot` code/configuration syntax | Referenced as a named mechanism in §4 rather than reproduced verbatim; the chapter itself notes only a subset of its options are used in this example, and exact syntax is version-specific. |
