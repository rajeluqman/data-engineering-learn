# File Layout & Compaction

> **One line:** how data sits on disk/object storage as actual files — and why too many small files quietly kills query performance.

**Spread:** 5/6 book sources · SQL + Python tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]] | Heaviest coverage — `OPTIMIZE`, auto-compaction, Liquid Clustering as file-layout levers |
| Databricks | [[ch13_nfcu_case_study\|Ch.13 NFCU]] | Automatic optimize/compact/vacuum credited with eliminating the "small file problem" at scale |
| Databricks | [[ch04_cost_maturity_journey_with_databricks\|Ch.4 Cost Maturity]] | File layout as a direct cost lever, not just a performance one |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]], [[ch03_storage_and_retrieval\|Ch.3 Storage & Retrieval]] | The storage-engine theory underneath compaction (LSM-trees, SSTables) |
| Kimball | [[ch01_dw_bi_dimensional_modeling_primer\|Ch.1 DW/BI Primer]] | File/storage layout as a foundational warehouse design concern |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | File layout's effect on query/transformation cost |
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]] | File-sink write patterns (temp file → atomic rename) — a correctness concern, not just performance |

---

## The thread

DDIA Ch.3 gives you the *theory* (LSM-trees compact because sequential writes are cheap and merges reclaim space); Databricks gives you the *practice* (Delta Lake's `OPTIMIZE`/auto-compaction is an LSM-adjacent idea applied to Parquet files on object storage). NFCU's case study is the payoff: automatic compaction is credited with directly improving query performance by avoiding the small-file problem — the exact failure mode DDIA's LSM-tree chapter warns about from the other direction.

## Related

[[partitioning-and-clustering]] · [[incremental-vs-full-recompute]] · [[cost-management]]
