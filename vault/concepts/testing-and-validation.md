# Testing & Pipeline Validation

> **One line:** proving a pipeline does what you think it does, before production finds out otherwise.

**Spread:** 6/6 book sources · Python track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Airflow | [[ch10_testing\|Ch.10 Testing]] | The dedicated, deepest chapter — DAG integrity tests, `DagBag`, mocking hooks, real-container integration tests |
| Databricks | [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]], [[ch10_collaborative_data_engineering_with_dabs\|Ch.10 Collaborative DE with DABs]] | Testing as part of a CI/CD-worthy migration and multi-developer workflow |
| Kimball | [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Testing as an explicit ETL system design phase |
| Kimball | [[ch15_electronic_commerce\|Ch.15 Electronic Commerce]] | Domain-specific validation scenarios |
| DDIA | [[ch04_encoding_and_evolution\|Ch.4 Encoding & Evolution]], [[ch05_replication\|Ch.5 Replication]], [[ch10_batch_processing\|Ch.10 Batch Processing]], [[ch11_stream_processing\|Ch.11 Stream Processing]] | Testing mentioned lightly across chapters, not a dedicated topic |
| Streaming Systems | [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]], [[ch07_practicalities_of_persistent_state\|Ch.7 Persistent State]] | Verification-by-construction — "how to test/verify these claims" is a fixed section in every chapter of this book |
| fundamentals_de | [[ch03_designing_good_data_architecture\|Ch.3 Designing Good Data Architecture]] | Testing as an architectural quality attribute |

### Your own track notes

- [[gym-and-troubleshooting-doctrine]] — your own doctrine already treats verification as a discipline

---

## The thread

Airflow Ch.10 is the only chapter in the vault that teaches testing as a full discipline (unit tests with mocked hooks, DAG integrity via `DagBag`, real-container integration tests via `pytest-docker-tools`) — treat it as the reference chapter. Everywhere else, "testing" is really *verification*: Streaming Systems' insistence on a "how to test/verify these claims" section per chapter is the same instinct as Airflow's `DagBag` test, just applied to a theoretical claim instead of a DAG.

## Related

[[data-quality]] · [[orchestration-and-dependencies]] · [[idempotency-and-exactly-once]]
