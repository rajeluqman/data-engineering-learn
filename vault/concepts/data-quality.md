# Data Quality & Expectations

> **One line:** making sure the data flowing through a pipeline is correct, complete, and consistent — not just that the pipeline "ran successfully."

**Spread:** 6/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## The core split

| | **Declarative checks** | **Process-level rigor** |
|---|---|---|
| **Idea** | Write a rule; the engine enforces it (and can drop/quarantine/warn) | Design the ETL process itself so bad data can't slip through unnoticed |
| **Granularity** | Row-level, column-level | Pipeline-level, subsystem-level |
| **Where taught** | Databricks (heaviest), Airflow (task-level) | Kimball ETL subsystems |

Databricks' `EXPECT` constraints are the sharpest, most concrete version of the declarative side. Kimball frames data quality as an entire named ETL subsystem category, not a bolt-on check.

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch09_production_grade_data_quality_using_sdp\|Ch.9 Production-Grade Data Quality]] | The deepest single treatment in the vault — `EXPECT` constraints, drop/warn/quarantine actions |
| Databricks | [[ch12_ifood_case_study\|Ch.12 iFood]] | Real-world scale case for quality gates on ingestion |
| Kimball | [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Quality checks as a named phase in ETL system design |
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | Data quality as one of the 34 ETL subsystems |
| Airflow | [[ch10_testing\|Ch.10 Testing]] | Quality-as-testing: DAG integrity + data assertions |
| DDIA | [[ch09_consistency_and_consensus\|Ch.9 Consistency & Consensus]] | Correctness guarantees as the theoretical floor under any quality check |
| Streaming Systems | scattered across ch01, ch03, ch07, ch08, ch09 | Quality concerns surface as watermark/completeness correctness, not a dedicated chapter |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | Data quality as part of the transformation layer's job |

### Your own track notes

- SQL track — [[master_sql_data_with_baraa\|Baraa]], plus quiz drills `M11-cp1-3-drill-2-quiz`, `M11-cp1-3-ddl-dql-joins-dml-quiz` exercise constraint-style thinking (`NOT NULL`, `CHECK`, `UNIQUE`)

---

## The thread

The SQL-level constraints you already know (`NOT NULL`, `CHECK`, `UNIQUE`, foreign keys) are the ancestor of Databricks' `EXPECT` — same idea, moved from schema-definition-time into pipeline-execution-time, with an explicit action (drop/warn/quarantine) attached. Kimball's contribution is organizational: it insists data quality is a *subsystem* you design for, not a check you remember to add.

---

## ⚠️ Same word, different meaning

- **"Constraint"** in SQL DDL (`CHECK`, `NOT NULL`) is a *schema-time* guarantee enforced by the database engine on every write. Databricks `EXPECT` is a *pipeline-time* guarantee enforced per-batch, with configurable action — a stricter DB constraint can't "warn and keep the row," but `EXPECT` can.

## Related

[[deduplication]] · [[schema-evolution]] · [[testing-and-validation]] · [[incremental-vs-full-recompute]] · [[keys-surrogate-natural]]
