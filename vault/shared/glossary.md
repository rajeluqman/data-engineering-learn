# A — Glossary

Cross-track index: SQL + Python + Lakehouse.
Format: Term | Track | Short definition | Note file
Sorted alphabetically. Append new terms as you encounter them.

> Rows below link to `vault/concepts/` hub notes — each hub cross-references all 6 books
> + the SQL/Python tracks for that concept, with disambiguation where a term collides
> across sources (marked ⚠️). See [[_BUILD-SPEC|the build spec]] for how the hub layer
> was built.

| Term | Track | Definition | Note file |
|------|-------|------------|-----------|
| Aggregation & Combiners | SQL, Lakehouse | Collapsing many rows into summary values, efficiently, via combinable partial aggregates | [[aggregation-and-combiners]] |
| Backfill & Reprocessing | SQL, Lakehouse | Running a pipeline against past data, either to fill a gap or correct history | [[backfill-and-reprocessing]] |
| Batch vs Streaming | Lakehouse | Scheduled-chunk vs. arrival-time processing — the vault's thesis: less fundamental a split than it looks | [[batch-vs-streaming]] |
| Change Data Capture (CDC) | Lakehouse | Capturing only what changed in a source since last read, instead of re-reading everything | [[change-data-capture]] |
| Checkpointing & Fault Recovery | Lakehouse | Saving enough state that a failure costs minutes, not the whole job | [[checkpointing-and-recovery]] |
| Cost Management & FinOps | Lakehouse | Deliberately attributing, monitoring, and controlling platform spend | [[cost-management]] |
| Data Quality & Expectations | SQL, Lakehouse | Making sure data is correct/complete/consistent, not just "the pipeline ran" | [[data-quality]] |
| Deduplication | SQL, Python, Lakehouse | Getting exactly one row per real-world thing — by removal or by prevention | [[deduplication]] |
| Dimensional Modeling & Grain | SQL, Lakehouse | Facts + dimensions design; grain = what one fact-table row represents | [[dimensional-modeling]] |
| Event Time vs Processing Time | Lakehouse | When a thing happened vs. when your system found out — the axis Streaming Systems is built on | [[event-time-vs-processing-time]] |
| File Layout & Compaction | SQL, Python, Lakehouse | How data sits on disk as files, and why small files quietly kill performance | [[file-layout-and-compaction]] |
| Idempotency & Exactly-Once | SQL, Python, Lakehouse | Running an operation twice produces the same result as running it once | [[idempotency-and-exactly-once]] |
| Incremental vs Full Recompute | SQL, Lakehouse | Reprocess only what changed, or rebuild the whole result from scratch | [[incremental-vs-full-recompute]] |
| Ingestion Patterns & Connectors | SQL, Python | Getting data from a source system into the platform — the first, fragile link | [[ingestion-patterns]] |
| Joins | SQL | Combining rows on a shared key — static-table and streaming joins are the same operation | [[joins]] |
| Late Data & Allowed Lateness | Lakehouse | What to do when a record arrives after you already emitted its window's result | [[late-data]] |
| Lineage & Governance | SQL, Python | Knowing where data came from and who can touch it, and proving both | [[lineage-and-governance]] |
| Materialized Views | Lakehouse | A query's result physically stored as a table, kept up to date automatically | [[materialized-views]] |
| Medallion / Layered Architecture | Lakehouse | Bronze/Silver/Gold — or Kimball's staging/presentation split, same discipline | [[medallion-layering]] |
| Orchestration & Task Dependencies | SQL | Deciding what runs, in what order, and what happens when a step fails | [[orchestration-and-dependencies]] |
| ⚠️ Partitioning & Clustering | SQL, Python, Lakehouse | The most overloaded term in the vault — physical storage, distributed sharding, SQL `PARTITION BY`, and Kafka partitions are 4 different things | [[partitioning-and-clustering]] |
| Replication & Distributed Coordination | SQL | Keeping copies in sync across machines, and agreeing on one truth | [[replication-and-distribution]] |
| Schema Evolution & Compatibility | SQL | Changing a data structure's shape without breaking readers/writers | [[schema-evolution]] |
| Security & Access Control | SQL | Who can touch which data, enforced by the platform, not by convention | [[security-and-access-control]] |
| Serverless & Compute Sizing | Lakehouse | Paying only for actual processing time instead of provisioned idle capacity | [[serverless-and-compute]] |
| Slowly Changing Dimensions (SCD) | SQL, Python | What happens when a dimension attribute changes — overwrite, keep history, or hybrid | [[slowly-changing-dimensions]] |
| ⚠️ SQL Window Functions | SQL, Python | `OVER(PARTITION BY ...)` — ranking, running totals, LAG/LEAD. Not the same "window" as event-time buckets | [[sql-window-functions]] |
| Streams & Tables Duality | Lakehouse | A table is a stream integrated over time; a stream is a table differentiated over time | [[streams-and-tables]] |
| Persistent State Management | Python, Lakehouse | The memory a long-running pipeline needs between records | [[state-management]] |
| Testing & Pipeline Validation | Python | Proving a pipeline does what you think, before production finds out otherwise | [[testing-and-validation]] |
| ⚠️ Transactions & Consistency | SQL | ACID guarantees (DDIA sense) — **not** Kimball's "transaction fact table" grain type | [[transactions-and-consistency]] |
| ⚠️ Watermarks | Lakehouse | Input-completeness metric (Streaming Systems) — a stricter idea than the `MAX(timestamp)` load bookmark in [[lakehouse-map]] | [[watermarks]] |
| ⚠️ Windowing (event-time buckets) | Lakehouse | Grouping unbounded data by *when it happened*. Not the SQL window-function sense | [[windowing-event-time]] |
| Surrogate, Natural & Business Keys | SQL, Python | What uniquely identifies a row — invented by the warehouse, or inherited from the source | [[keys-surrogate-natural]] |
