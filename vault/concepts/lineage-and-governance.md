# Lineage & Governance

> **One line:** knowing where data came from, who can touch it, and being able to prove both.

**Spread:** 6/6 book sources · SQL + Python tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]] | Unity Catalog as the governance foundation for a migration |
| Databricks | [[ch01_introduction_to_data_engineering_on_databricks\|Ch.1 Introduction]], [[ch11_practical_guide_to_serverless_migrations\|Ch.11 Serverless Migrations]] | Governance as a platform-level concern, not a bolt-on |
| Databricks | [[ch03_observability_in_lakeflow\|Ch.3 Observability]] | Lineage as an observability output — trace a value back to its source table |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]] | Governance carried through the ingestion connector itself |
| Kimball | [[ch21_big_data_analytics\|Ch.21 Big Data Analytics]] | Governance concerns specific to big-data-scale analytics |
| Kimball | [[ch04_inventory\|Ch.4 Inventory]] | Lineage as a data-quality/trust prerequisite |
| fundamentals_de | [[ch02_data_engineering_lifecycle\|Ch.2 DE Lifecycle]], [[ch09_serving_data\|Ch.9 Serving Data]] | Governance across the full lifecycle, not just storage |
| DDIA | [[ch10_batch_processing\|Ch.10 Batch Processing]] | Lineage as a natural byproduct of batch job dependency graphs |
| Airflow | [[ch01_meet_apache_airflow\|Ch.1 Meet Airflow]] | Orchestration graphs as an implicit lineage record |
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]], [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | Lineage concerns are thin here — mentioned, not developed |

---

## The thread

Lineage and governance show up differently depending on how "batch" or "managed" the platform is. In Airflow/DDIA, lineage is *implicit* — you reconstruct it from the DAG structure or job dependency graph. In Databricks (Unity Catalog), lineage is *explicit and queryable* — a platform feature, not something you infer. Kimball's angle is orthogonal: governance as a trust prerequisite for the business actually using the warehouse's numbers.

## Related

[[data-quality]] · [[security-and-access-control]] · [[orchestration-and-dependencies]] · [[change-data-capture]]
