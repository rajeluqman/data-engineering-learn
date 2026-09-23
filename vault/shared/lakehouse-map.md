# Lakehouse Map — SQL Concept → Medallion Architecture

Reference project: rajeluqman/banking-multisource-lakehouse

> Each row links to a `vault/concepts/` hub with the cross-book theory behind it —
> what all 6 books + the SQL/Python tracks say about that pattern, and any
> same-word-different-meaning traps to watch for.

| SQL Concept | Lakehouse Layer | Pattern | Notes | Concept Hub |
|-------------|----------------|---------|-------|-------------|
| Dedup / ROW_NUMBER | Silver | Deduplication on ingest | Partition by business key, order by load timestamp | [[deduplication]] |
| MERGE / UPSERT | Gold | SCD Type 1 — update existing, insert new | Snowflake MERGE, Databricks MERGE INTO | [[slowly-changing-dimensions]] |
| Watermark (MAX timestamp) | Bronze→Silver | Incremental load | Track last loaded timestamp per source table — ⚠️ this is the *simplified bookmark* sense, not the streaming-completeness sense | [[watermarks]] |
| Surrogate key | Gold (dimension) | Auto-increment ID as primary key | Natural key stays as business key | [[keys-surrogate-natural]] |
| External table | Bronze | Read raw files without moving data | Parquet/Delta on ADLS/S3 | [[medallion-layering]] |
| Managed table | Silver/Gold | Full Spark/Snowflake ownership | Data moved into warehouse storage | [[medallion-layering]] |
| Partition BY (DDL) | Silver/Gold | Partition by date or region | Reduces scan cost — ⚠️ physical partitioning, not the SQL window clause below | [[partitioning-and-clustering]] |
| PARTITION BY (window) | Silver | Window aggregation per entity | e.g. running balance per account | [[sql-window-functions]] |
| CTE / multi-step | Gold | Complex transformation chain | Prefer CTE for readability in dbt | — |
| dbt ref() | Gold | Modular SQL dependencies | ref('dim_customer') instead of hardcode | [[lineage-and-governance]] |
| CDC / change tracking | Bronze | Capture only what changed since last read | Change tracking (has PK, cheaper) vs. full CDC (no PK) | [[change-data-capture]] |
| SCD Type 2 (`__START_AT`/`__END_AT`) | Gold (dimension) | New row per version, old row expired | Needs a surrogate key — a natural key can't represent two versions as two rows | [[slowly-changing-dimensions]] |
| Materialized view | Gold | Precomputed, auto-refreshed query result | Incremental refresh breaks if stacked over another `EXPECT`-constrained streaming source | [[materialized-views]] |
| `OPTIMIZE` / auto-compaction | Silver/Gold | Merge small files, reclaim space | Same idea as an LSM-tree compaction, applied to Parquet/Delta files | [[file-layout-and-compaction]] |
| Idempotent write (delete-then-insert) | Bronze/Silver | Safe to rerun without duplicating | Required before any task can be safely backfilled | [[idempotency-and-exactly-once]] |
| `EXPECT` / `CHECK` constraint | Silver | Row-level quality gate, drop/warn/quarantine | SQL-DDL-time version is `CHECK`; pipeline-time version can warn instead of reject | [[data-quality]] |

*Append new mappings as modules progress.*
