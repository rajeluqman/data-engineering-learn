# Idempotency & Exactly-Once

> **One line:** running the same operation twice (by accident, retry, or rerun) produces the same result as running it once.

**Spread:** 5/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once & Side Effects]] | The theoretical deep-dive — the whole chapter, dedup-by-ID, checkpointing nondeterministic steps |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | How Storm/Spark/Flink/Dataflow each solved (or didn't solve) exactly-once historically |
| Streaming Systems | [[ch01_streaming_101\|Ch.1 Streaming 101]], [[ch08_streaming_sql\|Ch.8 Streaming SQL]] | Exactly-once as a foundational property assumed by later chapters |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | The distributed-systems framing — exactly-once vs. at-least-once vs. at-most-once delivery |
| Airflow | [[ch03_time_based_scheduling\|Ch.3 Scheduling]] | The **practical, operational** side: idempotent tasks as a hard requirement for safe backfill/rerun |
| Airflow | [[ch13_project_finding_the_fastest_way_to_get_around_nyc\|Ch.13 NYC Project]] | Execution-date-tagged delete-then-insert as a concrete idempotent-write pattern |
| Airflow | [[ch12_best_practices\|Ch.12 Best Practices]] | Idempotency named as a core best practice, not an edge case |
| fundamentals_de | [[ch05_data_generation_source_systems\|Ch.5 Data Generation & Source Systems]] | Idempotency framed from the source-system side |
| Databricks | [[ch01_introduction_to_data_engineering_on_databricks\|Ch.1 Introduction]], [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]] | Lighter touch — exactly-once semantics inherited from Structured Streaming |

---

## The thread

This is the theory/practice pair of the vault. Streaming Systems Ch.5 answers "how do you build a system that *guarantees* exactly-once?" (checkpointing, dedup-by-ID, Bloom filters). Airflow Ch.3/Ch.13 answers the practitioner's version: "how do I write a *task* so that rerunning it is safe?" (idempotent writes, partition-overwrite, delete-then-insert). You rarely get to build the Streaming-Systems-grade guarantee yourself — but you build idempotent tasks constantly, and Airflow's chapters are the direct playbook.

## Related

[[deduplication]] · [[checkpointing-and-recovery]] · [[backfill-and-reprocessing]] · [[change-data-capture]]
