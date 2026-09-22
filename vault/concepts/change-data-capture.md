# Change Data Capture & Change Tracking

> **One line:** capturing what *changed* in a source system since you last looked, instead of re-reading everything.

**Spread:** 5/6 book sources · SQL + Python tracks · verified via `vault/state/build_concept_index.py`

---

## CDC vs. change tracking — not the same thing

Databricks' own case studies draw this distinction explicitly, and it's worth internalizing before reading further:

| | **Change Tracking (CT)** | **CDC** |
|---|---|---|
| **Captures** | *Which* rows changed | The *actual* operations (insert/update/delete) and values |
| **Best for** | Tables **with** a primary key — lower source load | Tables **without** a primary key |
| **Cost** | Cheaper on the source database | More overhead |

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch06_implement_cdc_and_scd_type_2_with_lakeflow\|Ch.6 CDC + SCD2]] | The core technical walkthrough — CDC feeding directly into SCD Type 2 |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]] | CDC-vs-CT decision rule stated explicitly, tied to primary-key presence |
| Databricks | [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]] | CDC at extreme scale — Debezium + Kafka across 2,000+ Postgres tables |
| Databricks | [[ch13_nfcu_case_study\|Ch.13 NFCU]] | `APPLY CHANGES` as the CDC-dedup mechanism, used twice in one pipeline |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | CDC's theoretical home — "the database as the log," change streams as the log's output |
| fundamentals_de | [[ch07_ingestion\|Ch.7 Ingestion]], [[ch05_data_generation_source_systems\|Ch.5 Data Generation & Source Systems]] | CDC as one ingestion pattern among several |
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | CDC framed as an ETL extraction subsystem |

---

## The thread

DDIA Ch.11's framing — "treat the database as a stream of changes" — is the theoretical justification for everything Databricks Ch.6 does mechanically. The change log Debezium reads from Postgres (Hinge Health, Ch.16) *is* the log DDIA describes; CDC isn't a separate technique from stream processing, it's stream processing with a database as the source. Once CDC lands the changes, [[slowly-changing-dimensions|SCD Type 2]] is what turns them into queryable history — Databricks Ch.6 shows exactly that handoff.

## Related

[[slowly-changing-dimensions]] · [[ingestion-patterns]] · [[deduplication]] · [[schema-evolution]] · [[keys-surrogate-natural]]
