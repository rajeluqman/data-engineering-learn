# Incremental vs Full Recompute

> **One line:** when new data arrives, do you reprocess only what changed, or rebuild the whole result from scratch?

**Spread:** 4/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch07_optimizing_materialized_views_recomputes\|Ch.7 Optimizing Materialized View Recomputes]] | The dedicated technical deep-dive — the Enzyme engine's cost model for choosing incremental vs. full, and what *forces* a full recompute (non-deterministic functions, complex joins) |
| Databricks | [[ch09_production_grade_data_quality_using_sdp\|Ch.9 Data Quality]], [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]], [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]] | Where the incremental/full choice shows up operationally |
| Airflow | [[ch03_time_based_scheduling\|Ch.3 Scheduling]], [[ch12_best_practices\|Ch.12 Best Practices]] | The scheduling-level version: process only the new interval's data, not the whole table |
| Kimball | [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Incremental load as a named ETL design decision |
| Streaming Systems | [[ch07_practicalities_of_persistent_state\|Ch.7 Persistent State]], [[ch04_advanced_windowing\|Ch.4 Advanced Windowing]] | The state-management machinery that *makes* incremental processing possible |

---

## The thread

Databricks Ch.7 is the single most concrete artifact for this concept in the whole vault: it names the *exact* triggers that force a full recompute (non-deterministic functions like `RAND()`, complex/multi-way joins) — a concrete, checkable list you can hold every other source's vaguer "sometimes you need a full refresh" advice against. Airflow's interval-scoped processing (Ch.3) is the scheduling-layer version of the same idea: don't reprocess the whole table, reprocess this run's slice. Streaming Systems Ch.7's `CombineFn`/persistent-state machinery is *why* incremental processing is even possible — you need somewhere to keep the "state so far" between runs.

## Related

[[materialized-views]] · [[backfill-and-reprocessing]] · [[state-management]] · [[checkpointing-and-recovery]]
