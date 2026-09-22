# Materialized Views

> **One line:** a query whose result is physically stored as a table and kept up to date automatically, instead of recomputed on every read.

**Spread:** 4/6 book sources · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch09_production_grade_data_quality_using_sdp\|Ch.9 Data Quality]] | Materialized views combined with `EXPECT` constraints — and a specific gotcha: an `EXPECT`-constrained MV over an `EXPECT`-constrained streaming table disables incremental refresh entirely |
| Databricks | [[ch07_optimizing_materialized_views_recomputes\|Ch.7 Optimizing Materialized View Recomputes]] | The whole chapter — when a MV refreshes incrementally vs. fully, see [[incremental-vs-full-recompute]] |
| Databricks | [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]] | Real production payoff — incrementally updated MVs avoiding full view rebuilds on every new record |
| Streaming Systems | [[ch06_streams_and_tables\|Ch.6 Streams & Tables]], [[ch08_streaming_sql\|Ch.8 Streaming SQL]], [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | The theoretical grounding — a materialized view is exactly the "table" side of the [[streams-and-tables]] duality: a stream, grouped, brought to rest |
| DDIA | [[ch03_storage_and_retrieval\|Ch.3 Storage & Retrieval]], [[ch11_stream_processing\|Ch.11 Stream Processing]] | Materialized views as a caching/derived-data pattern |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | MVs as a serving-layer optimization |

---

## The thread

This concept is where [[streams-and-tables]]'s abstract theory becomes a literal product feature. Streaming Systems Ch.6 defines a "table" as data at rest, produced by *grouping* a stream — a materialized view is precisely that, made concrete: Databricks' own Ch.9 gotcha (MV-over-streaming-table breaking incremental refresh) is a direct real-world instance of a theoretical point Streaming Systems Ch.8 makes about triggering and grouping composition.

## Related

[[incremental-vs-full-recompute]] · [[streams-and-tables]] · [[data-quality]]
