# Batch vs Streaming

> **One line:** processing data in scheduled chunks (batch) vs. as it arrives (streaming) — and the vault's clearest thesis: this distinction is less fundamental than it looks.

**Spread:** 5/6 book sources · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch01_streaming_101\|Ch.1 Streaming 101]] | Opens the book by directly attacking the batch/streaming distinction as overstated |
| Streaming Systems | [[ch07_practicalities_of_persistent_state\|Ch.7 Persistent State]], [[ch09_streaming_joins\|Ch.9 Streaming Joins]], [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]] | Shows batch operations (joins, aggregation, state) reframed as streaming operations with different triggering |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | The distributed-systems argument for the same convergence thesis |
| fundamentals_de | [[ch07_ingestion\|Ch.7 Ingestion]] | Practical trade-offs — when batch is still the right operational choice |
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]], [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Kimball is unapologetically batch-native — written before streaming was mainstream, worth noticing as a contrast |
| Databricks | [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]], [[ch15_porsche_holding_case_study\|Ch.15 Porsche Holding]] | Spark Declarative Pipelines explicitly supports *both* modes from one codebase |

---

## The thread — this is the vault's biggest cross-book claim

Streaming Systems Ch.1 states outright: batch is just a special case of streaming with bounded input. Its own [[streams-and-tables|streams-and-tables]] chapter later proves this formally — a MapReduce batch job decomposes into the exact same table→stream→table sequence a streaming job does. Databricks' unified batch+streaming API (Spark Declarative Pipelines) is the *industrial* proof of the same claim: one pipeline definition, two execution modes. Kimball, by contrast, was written from a purely batch worldview — reading it *after* Streaming Systems is a good way to notice which of its assumptions (nightly loads, fixed windows of "today's data") are batch-specific rather than universal.

## Related

[[streams-and-tables]] · [[windowing-event-time]] · [[state-management]] · [[incremental-vs-full-recompute]]
