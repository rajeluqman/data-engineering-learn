# Late Data & Allowed Lateness

> **One line:** what do you do when a record arrives *after* you already emitted a result for the time window it belongs to?

**Spread:** 3/6 book sources · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]] | The core mechanism — allowed lateness as a configurable horizon, past which late data is simply dropped rather than reprocessed forever |
| Streaming Systems | [[ch03_watermarks\|Ch.3 Watermarks]] | Late data as the direct consequence of a heuristic (imperfect) [[watermarks|watermark]] |
| Streaming Systems | [[ch08_streaming_sql\|Ch.8 Streaming SQL]], [[ch01_streaming_101\|Ch.1 Streaming 101]], [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | Late-firing triggers as the SQL-level and historical answer to the same problem |
| Kimball | [[ch14_healthcare\|Ch.14 Healthcare]], [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | Late-arriving *facts and dimensions* in a batch ETL context — a related but distinct problem: a dimension row arriving after its associated fact |
| fundamentals_de | [[ch02_data_engineering_lifecycle\|Ch.2 DE Lifecycle]], [[ch07_ingestion\|Ch.7 Ingestion]] | Late data as an ingestion-design consideration |

---

## The thread

Kimball's "late-arriving dimension" problem (a fact row lands before the dimension row it should join to) predates streaming theory entirely, but it's the exact same underlying issue Streaming Systems formalizes: *something needed for a correct result hasn't shown up yet, and you have to decide whether to wait, guess, or fix it later.* Streaming Systems' contribution is turning Kimball's ad hoc "reprocess later" fix into a first-class, configurable mechanism (allowed lateness + late-firing triggers) with an explicit trade-off between correctness and resource cost.

## Related

[[watermarks]] · [[event-time-vs-processing-time]] · [[windowing-event-time]] · [[backfill-and-reprocessing]]
