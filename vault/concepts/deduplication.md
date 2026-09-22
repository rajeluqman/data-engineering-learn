# Deduplication

> **One line:** getting exactly one row per real-world thing — either by *removing* duplicates that already exist, or by *designing* so they are never created.

**Spread:** 6/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## ⚠️ Two faces of the same problem

This is the key insight the corpus reveals, and it is easy to miss because the two camps rarely use each other's vocabulary.

| | **Removal** (curative) | **Prevention** (preventive) |
|---|---|---|
| **Assumption** | Duplicates already exist in the data | Duplicates are created by *how the pipeline runs* |
| **Trigger** | Multi-source merge, replayed feed, dirty source | Task rerun, backfill, retry after crash |
| **Technique** | `ROW_NUMBER() OVER (PARTITION BY key ORDER BY …) = 1`, `APPLY CHANGES`, survivorship rules | Idempotent writes, partition-overwrite, dedup-by-ID, exactly-once |
| **Where taught** | SQL track, Kimball ETL, Databricks | Airflow, Streaming Systems |

If you only learn the removal side, you will keep writing pipelines that *manufacture* the duplicates you then have to strip. That is the actual lesson hiding across these six books.

---

## Where it appears

### Removal side

| Source | Chapter | Angle |
|---|---|---|
| SQL track | [[ansh-lamba-chatgpt-quiz-handoff\|Ansh Lamba — dedup scenario]] | `ROW_NUMBER() OVER (PARTITION BY id ORDER BY id DESC)` then filter `= 1`. Explicitly framed as "scenario 2 — removing duplicate" |
| SQL track | [[master_sql_data_with_baraa\|Baraa — Master SQL]] | Heaviest coverage in the whole vault by hit count |
| Databricks | [[ch13_nfcu_case_study\|Ch.13 NFCU]] | `APPLY CHANGES` called **twice** — dedup at raw ingest *and* again on the derived login table |
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | Dedup as a named ETL subsystem, tied to conforming/survivorship |
| Kimball | [[ch20_etl_system_design_and_development_process_and_tasks\|Ch.20 ETL Design]] | Where dedup sits in the build sequence |
| Streaming Systems | [[ch09_streaming_joins\|Ch.9 Streaming Joins]] | Duplicate rows from N:M join cardinality — `SEMI` join avoids the fan-out |

### Prevention side

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch05_exactly_once_and_side_effects\|Ch.5 Exactly-Once]] | The deepest treatment: dedup-by-unique-ID, Bloom-filter catalogs, GC of the ID catalog |
| Airflow | [[ch03_time_based_scheduling\|Ch.3 Scheduling]] | Non-idempotent append silently duplicates a day's events on *every* rerun; partition-overwrite is the fix |
| Airflow | [[ch13_project_finding_the_fastest_way_to_get_around_nyc\|Ch.13 NYC Project]] | Execution-date-tagged delete-then-insert as the idempotent write pattern |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | Duplicate suppression as a fault-tolerance property |
| Streaming Systems | [[ch07_practicalities_of_persistent_state\|Ch.7 Persistent State]] | State needed to *remember* what was already seen |

### Your own track notes

- [[lakehouse-map]] — already maps `Dedup / ROW_NUMBER → Silver layer → "partition by business key, order by load timestamp"`
- [[pyspark-evidence-map]] — PySpark-side evidence
- [[errors-gotchas]] — recorded gotchas

---

## The thread

The same `PARTITION BY business_key ORDER BY load_ts` shape you learned in Ansh Lamba is *literally* the Silver-layer pattern in your own `lakehouse-map.md`, is what Databricks NFCU expresses as `APPLY CHANGES`, and is what Kimball calls a dedup subsystem. One idea, four vocabularies.

Streaming Systems Ch.5 then asks the harder question: *why is there a duplicate at all?* Its answer — attach a unique ID at the source, keep a catalog, garbage-collect it — is the prevention-side mirror of the same concern.

---

## ⚠️ Same word, different meaning

- **`PARTITION BY`** here is the SQL *window-function* clause. It is **not** physical table partitioning (Kimball), **not** distributed sharding (DDIA Ch.6), and **not** Kafka partitions. See [[partitioning-and-clustering]] for the disambiguation.

## Related

[[idempotency-and-exactly-once]] · [[change-data-capture]] · [[keys-surrogate-natural]] · [[sql-window-functions]] · [[backfill-and-reprocessing]]
