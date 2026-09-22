# Aggregation & Combiners

> **One line:** collapsing many rows/events into fewer summary values — and doing it efficiently by combining partial results instead of re-scanning everything.

**Spread:** 4/6 book sources · SQL + shared tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch07_practicalities_of_persistent_state\|Ch.7 Persistent State]] | The technical core — `CombineFn`, incremental combining, why associativity/commutativity make parallel partial aggregation safe |
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]], [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]], [[ch08_streaming_sql\|Ch.8 Streaming SQL]], [[ch06_streams_and_tables\|Ch.6 Streams & Tables]] | Combiner lifting as a named MapReduce-lineage optimization, revisited at each layer |
| Kimball | [[ch07_accounting\|Ch.7 Accounting]], [[ch13_education\|Ch.13 Education]], [[ch15_electronic_commerce\|Ch.15 Electronic Commerce]], [[ch09_human_resources_management\|Ch.9 HR]], [[ch16_insurance\|Ch.16 Insurance]] | Aggregate fact tables and pre-computed summary rollups, evenly spread across every industry chapter |
| DDIA | [[ch02_data_models_and_query_languages\|Ch.2 Data Models & Query Languages]], [[ch10_batch_processing\|Ch.10 Batch Processing]] | Aggregation as a MapReduce Reduce-phase operation — the theoretical root |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | Aggregation as a transformation-layer responsibility |

### Your own track notes

- [[errors-gotchas]] — 8 hits, aggregation-related gotchas already logged
- SQL track — heaviest coverage: [[master_sql_data_with_baraa\|Baraa]] (127), `M1-dql-core` (29, `GROUP BY`/`SUM`/`AVG` fundamentals)

---

## The thread

Your SQL `GROUP BY`/`SUM`/`AVG` (M1) is the single-machine version of what Streaming Systems Ch.7 calls a `CombineFn` — the same commutative/associative requirement applies, it's just invisible on one machine because there's nothing to parallelize. DDIA's MapReduce Reduce phase is the distributed middle ground. Kimball's aggregate fact tables are the *pre-computed, stored* version of the same idea: instead of aggregating at query time, aggregate once at load time and store the result as its own table.

## Related

[[sql-window-functions]] · [[dimensional-modeling]] · [[materialized-views]] · [[incremental-vs-full-recompute]]
