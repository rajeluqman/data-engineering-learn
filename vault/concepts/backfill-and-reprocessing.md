# Backfill & Reprocessing

> **One line:** running a pipeline against data from the past — either because it never ran for that period, or because you need to correct it.

**Spread:** 6/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Airflow | [[ch03_time_based_scheduling\|Ch.3 Scheduling]] | The heaviest treatment in the vault (37 hits) — `catchup`, backfill semantics tied directly to idempotency |
| Airflow | [[ch01_meet_apache_airflow\|Ch.1 Meet Airflow]] | Backfill as a headline Airflow capability |
| Airflow | [[ch13_project_finding_the_fastest_way_to_get_around_nyc\|Ch.13 NYC Project]], [[ch02_anatomy_of_an_airflow_dag\|Ch.2 Anatomy of a DAG]], [[ch06_defining_dependencies_between_tasks\|Ch.6 Defining Dependencies]] | Backfill in practice — throttling, dependency handling |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | Reprocessing as replaying a durable log from an earlier offset |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]], [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]] | Replay as a building block for exactly-once guarantees, not just a recovery tool |
| Kimball | [[ch04_inventory\|Ch.4 Inventory]], [[ch11_telecommunications\|Ch.11 Telecommunications]], [[ch05_procurement\|Ch.5 Procurement]] | Historical restatement in specific fact-table designs |
| fundamentals_de | [[ch06_storage\|Ch.6 Storage]] | Storage-layer implications of reprocessing (retention, replayability) |
| Databricks | [[ch07_optimizing_materialized_views_recomputes\|Ch.7 Materialized View Recomputes]], [[ch09_production_grade_data_quality_using_sdp\|Ch.9 Data Quality]] | Recompute as the materialized-view-specific flavor of reprocessing |

---

## The thread

Backfill only works safely if the task being backfilled is [[idempotency-and-exactly-once|idempotent]] — Airflow Ch.3 says this explicitly and ties the two concepts together in the same breath. DDIA and Streaming Systems generalize the same idea to log replay: a Kafka-style durable log lets you "backfill" a stream consumer by resetting its offset, which is structurally the same operation as an Airflow backfill, just at a different layer. Databricks' "recompute" (Ch.7) is the materialized-view-specific case — same underlying question (do I redo everything, or just what changed?) covered from [[incremental-vs-full-recompute]].

## Related

[[idempotency-and-exactly-once]] · [[incremental-vs-full-recompute]] · [[checkpointing-and-recovery]] · [[deduplication]]
