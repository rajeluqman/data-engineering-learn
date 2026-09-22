# Partitioning & Clustering

> **One line:** splitting data (or work) into smaller pieces so a system doesn't have to scan/move/coordinate everything at once.

**Spread:** 6/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## ⚠️ Same word, different meaning — read this first

"Partition" is the single most overloaded term in this vault. Four genuinely different ideas share the name:

| Sense | Meaning | Where taught |
|---|---|---|
| **Physical table partitioning** | Splitting a table's storage by a key (e.g. by date) so queries can skip irrelevant files | Kimball, Databricks, fundamentals_de |
| **Distributed sharding** | Splitting *data across machines* in a distributed system, each partition owned/served by different nodes | DDIA Ch.6 (dedicated chapter) |
| **SQL window clause** | `PARTITION BY` inside `OVER(...)` — resets a window function's calculation per group, nothing to do with physical storage | SQL track, `sql-window-functions` |
| **Kafka/streaming partitions** | An ordered, append-only log shard that determines parallelism and ordering guarantees | Streaming Systems, Airflow (Kafka connectors) |

**Do not treat these as the same concept just because the word matches.** DDIA Ch.6's rebalancing algorithms have nothing to teach you about `PARTITION BY id ORDER BY score` in a SQL window function, and vice versa.

---

## Where it appears

### Physical/storage partitioning

| Source | Chapter | Angle |
|---|---|---|
| DDIA | [[ch06_partitioning\|Ch.6 Partitioning]] | The dedicated deep-dive — by key range, by hash, rebalancing, request routing (**this is the sharding sense**) |
| Kimball | [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Partitioning fact tables for load/purge management |
| fundamentals_de | [[ch06_storage\|Ch.6 Storage]] | Partitioning as a storage-layer performance lever |
| Databricks | [[ch12_ifood_case_study\|Ch.12 iFood]] | Liquid Clustering replacing traditional partitioning at scale |
| Airflow | [[ch03_time_based_scheduling\|Ch.3 Scheduling]] | Partition-overwrite as the idempotent-write pattern (ties into [[deduplication]]) |

### SQL window-function sense

| Source | Chapter | Angle |
|---|---|---|
| SQL track | [[master_sql_data_with_baraa\|Baraa]], [[ansh-lamba-raw-notes\|Ansh Lamba]] | `PARTITION BY` resetting `ROW_NUMBER()`/`RANK()`/running totals per group — see [[sql-window-functions]] |

### Distributed/streaming sense

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]], [[ch06_streams_and_tables\|Ch.6 Streams & Tables]] | Log partitions as the unit of ordering/parallelism |

### Your own track notes

- [[lakehouse-map]] — already has `PARTITION BY (DDL)` and `PARTITION BY (window)` as **two separate rows** — your own notes already caught this collision before this hub existed

---

## The thread

Every "partitioning" technique in this vault is answering the same underlying question — *"how do I avoid touching data I don't need to?"* — but at wildly different layers: disk files (physical), machines (DDIA sharding), or a single query's result set (SQL window). Recognizing which layer a given "partition" lives at is more valuable than memorizing any one technique.

## Related

[[file-layout-and-compaction]] · [[sql-window-functions]] · [[replication-and-distribution]] · [[deduplication]] · [[dimensional-modeling]]
