# Checkpointing & Fault Recovery

> **One line:** periodically saving enough state that a failure costs you minutes of reprocessing, not the whole job.

**Spread:** 6/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]] | Heaviest treatment — checkpointing as the mechanism that makes nondeterministic operations replay-safe |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | Flink's snapshot/savepoint model vs. Dataflow's approach — two competing checkpoint architectures |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | Checkpointing as fault-tolerance primitive across stream processors |
| DDIA | [[ch07_transactions\|Ch.7 Transactions]] | The transactional-recovery ancestor of stream checkpointing |
| DDIA | [[ch10_batch_processing\|Ch.10 Batch Processing]] | Batch's answer: reprocess from durable input instead of checkpointing |
| DDIA | [[ch08_trouble_with_distributed_systems\|Ch.8 Trouble with Distributed Systems]] | Why recovery is hard — clocks, partial failures, network issues |
| Databricks | [[ch06_implement_cdc_and_scd_type_2_with_lakeflow\|Ch.6 CDC + SCD2]] | Gateway pipeline checkpoint/retention window — how long you can be offline before a full refresh is forced |
| Kimball | [[ch16_insurance\|Ch.16 Insurance]], [[ch04_inventory\|Ch.4 Inventory]] | Recovery/restatement scenarios in specific industry fact-table designs |
| Airflow | [[ch02_anatomy_of_an_airflow_dag\|Ch.2 Anatomy of a DAG]] | Task-clearing as Airflow's manual recovery mechanism |

### Your own track notes

- [[gym-and-troubleshooting-doctrine]] — your own troubleshooting playbook already has 6 hits here
- SQL track — `ansh-lamba-raw-notes`, `ansh-lamba-chatgpt-quiz-handoff` (transaction rollback / recovery framing)

---

## The thread

DDIA Ch.7/Ch.8 gives you the *why* (partial failures are unavoidable in distributed systems), Streaming Systems Ch.5 gives you the *mechanism* (checkpoint before any nondeterministic step so a retry replays deterministically), and Airflow gives you the *operational* version (clear a failed task, it reruns from the last successful state). Databricks' CDC gateway retention window is the same idea with a hard deadline attached: checkpoint too infrequently relative to your source's retention, and recovery degrades from "resume" to "full reload."

---

## ⚠️ Same word, different meaning

- **"Snapshot"** means a Flink distributed checkpoint (Streaming Systems Ch.10) in one context and a point-in-time *table read* (Databricks CDC gateway) in another — same word, one is a fault-tolerance artifact, the other is a data-extraction technique.

## Related

[[idempotency-and-exactly-once]] · [[backfill-and-reprocessing]] · [[state-management]] · [[replication-and-distribution]] · [[change-data-capture]]
