# Orchestration & Task Dependencies

> **One line:** deciding what runs, in what order, on what schedule, and what happens when one step fails and others depend on it.

**Spread:** 6/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Airflow | [[ch02_anatomy_of_an_airflow_dag\|Ch.2 Anatomy of a DAG]] | The core vocabulary — DAG, task, trigger rule (heaviest hit count in the vault: 75) |
| Airflow | [[ch06_defining_dependencies_between_tasks\|Ch.6 Defining Dependencies]] | Branching, fan-in/fan-out, trigger rules like `none_failed` |
| Airflow | [[ch01_meet_apache_airflow\|Ch.1 Meet Airflow]] | Why orchestration exists as a discipline separate from the tasks themselves |
| Airflow | [[ch10_testing\|Ch.10 Testing]] | DAG integrity testing — catching broken dependency graphs before production |
| Airflow | [[ch03_time_based_scheduling\|Ch.3 Scheduling]] | The scheduling half of orchestration |
| Databricks | [[ch11_practical_guide_to_serverless_migrations\|Ch.11 Serverless Migrations]], [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]] | Lakeflow Jobs as Databricks' native orchestrator, replacing Airflow/ADF in these case studies |
| fundamentals_de | [[ch02_data_engineering_lifecycle\|Ch.2 DE Lifecycle]], [[ch11_future_of_data_engineering\|Ch.11 Future of DE]] | Orchestration as one of the lifecycle's core undercurrents |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | Where orchestration concerns bleed into stream-processing topology |

### Your own track notes

- [[lakehouse-map]] — 1 hit, room to grow as you connect orchestration choices to layer design

---

## The thread

Airflow gives you the deepest, most explicit vocabulary (DAG, trigger rule, `none_failed`, task clearing) because orchestration *is* Airflow's whole job. Databricks' Lakeflow Jobs case studies (Ch.2, Ch.11) show the same concepts — dependency, retry, schedule — reimplemented as a managed, serverless-native orchestrator. When you read a Databricks case study saying "Lakeflow Jobs," mentally substitute "their DAG," and the Airflow chapters become directly transferable.

## Related

[[backfill-and-reprocessing]] · [[idempotency-and-exactly-once]] · [[testing-and-validation]] · [[serverless-and-compute]]
