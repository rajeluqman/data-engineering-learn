# Surrogate, Natural & Business Keys

> **One line:** deciding what uniquely identifies a row — and whether that identifier should come from the source system or be invented by the warehouse.

**Spread:** 6/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## The core distinction

| | **Natural / business key** | **Surrogate key** |
|---|---|---|
| **Origin** | Comes from the source system (e.g. a customer's account number) | Invented by the warehouse (auto-increment integer) |
| **Stability** | Can change, be reused, or collide across source systems | Never changes once assigned |
| **Used for** | Joining back to the source, human readability | Joining within the warehouse, enabling SCD history |

Kimball is unambiguous that surrogate keys are what make [[slowly-changing-dimensions|SCD Type 2]] possible at all — a natural key alone can't represent "two different versions of the same customer" as two distinct joinable rows.

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | Surrogate key generation as its own named ETL subsystem |
| Kimball | [[ch02_dimensional_modeling_techniques_overview\|Ch.2 Dimensional Modeling Techniques]] | Why surrogate keys are non-negotiable for SCD Type 2 |
| Kimball | [[ch03_retail_sales\|Ch.3 Retail Sales]], [[ch05_procurement\|Ch.5 Procurement]] | Worked examples of surrogate-keyed dimensions |
| Kimball | [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Where key generation sits in the build sequence |
| DDIA | [[ch03_storage_and_retrieval\|Ch.3 Storage & Retrieval]], [[ch06_partitioning\|Ch.6 Partitioning]] | Keys as the physical-access mechanism (index/partition key), a different concern than dimensional identity |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | Key strategy as part of the modeling layer |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]] | Primary-key-aware CDC — change tracking recommended specifically *when a primary key exists* |
| Streaming Systems | [[ch06_streams_and_tables\|Ch.6 Streams & Tables]] | Keys as the grouping unit for stream-to-table conversion |

### Your own track notes

- [[lakehouse-map]] — `Surrogate key → Gold (dimension) → "Auto-increment ID as primary key. Natural key stays as business key."` — already states the exact rule
- SQL track — heaviest coverage: [[master_sql_data_with_baraa\|Baraa]], plus both quiz drills

---

## The thread

Your `lakehouse-map.md` already has the rule you need: surrogate key in the warehouse, natural key preserved as an attribute. Kimball explains *why* (SCD Type 2 needs a stable join target that can have multiple versions per natural key). Databricks Ch.5's CDC connector shows the operational payoff: a table *with* a natural primary key gets the cheaper "change tracking" sync mode; one *without* needs full CDC — the key strategy you chose upstream changes your ingestion cost downstream.

## Related

[[slowly-changing-dimensions]] · [[dimensional-modeling]] · [[change-data-capture]] · [[deduplication]]
