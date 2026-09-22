# Transactions & Consistency

> **One line:** guarantees about what a reader can see and when — from ACID's single-database promises to the weaker guarantees distributed systems settle for.

**Spread:** 6/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## ⚠️ Same word, different meaning — read this first

**"Transaction" means something entirely different in Kimball than everywhere else in this vault.**

| Sense | Meaning | Where taught |
|---|---|---|
| **ACID transaction** | A unit of work with atomicity/consistency/isolation/durability guarantees | DDIA (dedicated chapter), Databricks, Airflow idempotency patterns |
| **Fact-table grain type** | One of three named grain categories — "transaction, periodic snapshot, and accumulating snapshot" — describing *what a row represents*, not a database guarantee at all | Kimball |

A "transaction fact table" in Kimball has nothing to do with `BEGIN`/`COMMIT`. It means one row per business event (e.g. one row per sale). Confusing the two is an easy, embarrassing interview mistake.

---

## Where it appears

### ACID / distributed-systems sense

| Source | Chapter | Angle |
|---|---|---|
| DDIA | [[ch07_transactions\|Ch.7 Transactions]] | The canonical treatment — isolation levels, anomalies, serializability |
| DDIA | [[ch09_consistency_and_consensus\|Ch.9 Consistency & Consensus]] | Consistency models beyond a single transaction — linearizability, consensus |
| DDIA | [[ch05_replication\|Ch.5 Replication]] | Consistency guarantees under replication lag |
| DDIA | [[ch08_trouble_with_distributed_systems\|Ch.8 Trouble with Distributed Systems]] | Why guarantees are hard to keep in practice |
| Databricks | [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]], [[ch06_implement_cdc_and_scd_type_2_with_lakeflow\|Ch.6 CDC + SCD2]] | Delta Lake's ACID guarantees on top of object storage |
| fundamentals_de | [[ch06_storage\|Ch.6 Storage]] | Where transactional guarantees fit in the storage layer |

### Kimball's grain-type sense

| Source | Chapter | Angle |
|---|---|---|
| Kimball | [[ch16_insurance\|Ch.16 Insurance]], [[ch04_inventory\|Ch.4 Inventory]], [[ch08_customer_relationship_management\|Ch.8 CRM]], [[ch03_retail_sales\|Ch.3 Retail Sales]] | Transaction fact tables as one of the three grain types, contrasted with periodic/accumulating snapshot |

### Your own track notes

- SQL track — [[master_sql_data_with_baraa\|Baraa]] `M8-programmable` covers `BEGIN`/`COMMIT`/`ROLLBACK` (the ACID sense)

---

## The thread

If you're reasoning about *correctness under concurrency or failure*, you're in DDIA's world. If you're reasoning about *what one fact-table row represents* (an event vs. a periodic state vs. a running balance), you're in Kimball's world — a completely separate axis. Databricks' Delta Lake ACID guarantees are the practical bridge: they let a lakehouse table behave with DDIA-style transactional guarantees while still being modeled with Kimball-style grain choices.

## Related

[[checkpointing-and-recovery]] · [[replication-and-distribution]] · [[dimensional-modeling]] · [[idempotency-and-exactly-once]]
