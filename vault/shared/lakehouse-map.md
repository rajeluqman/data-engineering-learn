# Lakehouse Map — SQL Concept → Medallion Architecture

Reference project: rajeluqman/banking-multisource-lakehouse

| SQL Concept | Lakehouse Layer | Pattern | Notes |
|-------------|----------------|---------|-------|
| Dedup / ROW_NUMBER | Silver | Deduplication on ingest | Partition by business key, order by load timestamp |
| MERGE / UPSERT | Gold | SCD Type 1 — update existing, insert new | Snowflake MERGE, Databricks MERGE INTO |
| Watermark (MAX timestamp) | Bronze→Silver | Incremental load | Track last loaded timestamp per source table |
| Surrogate key | Gold (dimension) | Auto-increment ID as primary key | Natural key stays as business key |
| External table | Bronze | Read raw files without moving data | Parquet/Delta on ADLS/S3 |
| Managed table | Silver/Gold | Full Spark/Snowflake ownership | Data moved into warehouse storage |
| Partition BY (DDL) | Silver/Gold | Partition by date or region | Reduces scan cost |
| PARTITION BY (window) | Silver | Window aggregation per entity | e.g. running balance per account |
| CTE / multi-step | Gold | Complex transformation chain | Prefer CTE for readability in dbt |
| dbt ref() | Gold | Modular SQL dependencies | ref('dim_customer') instead of hardcode |

*Append new mappings as modules progress.*
