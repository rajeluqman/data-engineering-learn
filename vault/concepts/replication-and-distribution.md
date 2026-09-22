# Replication & Distributed Coordination

> **One line:** keeping copies of the same data on multiple machines in sync, and agreeing on a single truth when machines disagree.

**Spread:** 5/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| DDIA | [[ch05_replication\|Ch.5 Replication]] | The dedicated, exhaustive treatment (174 hits) — leader/follower, sync/async, conflict resolution |
| DDIA | [[ch09_consistency_and_consensus\|Ch.9 Consistency & Consensus]] | What replication *guarantees* actually mean and how consensus algorithms achieve them |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]], [[ch08_trouble_with_distributed_systems\|Ch.8 Trouble with Distributed Systems]], [[ch06_partitioning\|Ch.6 Partitioning]] | Replication as it intersects streaming, failure modes, and sharding |
| Databricks | [[ch03_observability_in_lakeflow\|Ch.3 Observability]] | Lighter, applied touch — monitoring replicated/synced pipeline state |
| fundamentals_de | [[ch06_storage\|Ch.6 Storage]] | Replication at the storage-layer level |
| Kimball | [[ch18_dimensional_modeling_process_and_tasks\|Ch.18 Dimensional Modeling Process]] | Replication concerns for distributing warehouse copies |
| Airflow | [[ch15_operating_airflow_in_production\|Ch.15 Operating Airflow in Production]] | Multiple-scheduler replication for production HA |

---

## The thread

This is DDIA's chapter to teach — nothing else in the vault comes close to its depth. Treat the other sources as *applications* of DDIA's theory: Airflow's multi-scheduler HA setup (Ch.15) is leader/follower coordination in miniature; Kimball's distributed-warehouse-copy concern (Ch.18) is replication applied to an analytical, not transactional, workload.

## Related

[[checkpointing-and-recovery]] · [[transactions-and-consistency]] · [[partitioning-and-clustering]]
