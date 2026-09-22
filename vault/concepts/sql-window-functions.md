# SQL Window Functions

> **One line:** calculating something across a set of rows *without* collapsing them into one row — ranking, running totals, previous/next-row comparisons, all while keeping every original row visible.

**Spread:** 4/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## ⚠️ Same word, different meaning

`PARTITION BY` here is the SQL clause inside `OVER(...)`. It is **not** physical table partitioning, **not** distributed sharding, and **not** a Kafka partition. See [[partitioning-and-clustering]] for the full disambiguation — this is the single most confusable term-collision in the vault.

Likewise, "window" here means *a group of rows selected by `OVER(...)`*. In Streaming Systems, "window" means an *event-time bucket* (fixed/sliding/session). These are related metaphorically (both "group things together") but are different mechanisms entirely — see [[windowing-event-time]].

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| SQL track | [[ansh-lamba-chatgpt-quiz-handoff\|Ansh Lamba]] (76), [[master_sql_data_with_baraa\|Baraa]] (65), [[ansh-lamba-raw-notes\|Ansh Lamba raw]] (64) | The vault's primary teaching material for this concept — `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`/`LEAD()`, frames |
| SQL track | `M5-window-functions` | Dedicated module note |
| Python track | [[pyspark-evidence-map\|PySpark evidence]] | Same functions, Spark DataFrame API instead of raw SQL |
| DDIA | [[ch05_replication\|Ch.5 Replication]], [[ch11_stream_processing\|Ch.11 Stream Processing]] | Passing mentions — window functions as an example of declarative query power |
| Databricks | [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]] | Window functions in a Spark SQL migration context |
| fundamentals_de | [[ch06_storage\|Ch.6 Storage]] | Light touch |

### Your own track notes

- [[lakehouse-map]] — already has `PARTITION BY (window) → Silver → "Window aggregation per entity, e.g. running balance per account"` and `CTE / multi-step → Gold`
- [[errors-gotchas]] — 7 hits, window-function-specific gotchas already logged

---

## The thread

`DENSE_RANK()`/`RANK()`/`ROW_NUMBER()` differ only on ties, and Ansh Lamba's own notes flag this as the single most quizzable concept in the SQL corpus — it's also the exact mechanism behind [[deduplication]]'s "removal side" (`ROW_NUMBER() OVER(PARTITION BY key ORDER BY ...) = 1`). Your `lakehouse-map.md` already generalizes the SQL-textbook exercise into a real pattern: a "running balance per account" is the same `SUM() OVER(PARTITION BY account ORDER BY date)` shape as any quiz question, just applied to production data.

## Related

[[deduplication]] · [[partitioning-and-clustering]] · [[aggregation-and-combiners]] · [[windowing-event-time]]
