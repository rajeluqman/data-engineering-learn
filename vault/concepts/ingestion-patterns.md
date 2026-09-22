# Ingestion Patterns & Connectors

> **One line:** getting data from a source system into your platform — the first, and often most fragile, link in the pipeline.

**Spread:** 5/6 book sources · SQL + Python tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]] | Managed connector deep-dive — gateway/ingest pipeline split, CDC/CT setup |
| Databricks | [[ch15_porsche_holding_case_study\|Ch.15 Porsche Holding]], [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]] | Build-vs-buy: managed connector (Salesforce) vs. custom ingestion (Fivetran + Debezium at 10x scale) |
| Databricks | [[ch01_introduction_to_data_engineering_on_databricks\|Ch.1 Introduction]], [[ch13_nfcu_case_study\|Ch.13 NFCU]] | Auto Loader / Event Hubs as ingestion entry points |
| fundamentals_de | [[ch07_ingestion\|Ch.7 Ingestion]] | The dedicated theoretical chapter — batch vs. streaming ingestion trade-offs |
| Airflow | [[ch07_triggering_workflows_with_external_input\|Ch.7 Triggering Workflows with External Input]] | Sensor-based and event-driven ingestion triggers |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | The log-based ingestion model (Kafka) underneath most managed connectors |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | Historical context — how ingestion patterns evolved with the systems built to handle them |

---

## The thread

Hinge Health's case study (Ch.16) is the most instructive single artifact here: they hand-built ingestion (Debezium + Kafka + S3) at scale, then explicitly diagnosed the S3 intermediary hop as the bottleneck and removed it — arriving, through hard experience, at exactly the architecture fundamentals_de Ch.7 recommends as the default (stream directly from the log, skip unnecessary staging). Porsche's case (Ch.15) is the mirror image: choosing the managed connector *up front* instead of learning this lesson the hard way.

## Related

[[change-data-capture]] · [[schema-evolution]] · [[batch-vs-streaming]]
