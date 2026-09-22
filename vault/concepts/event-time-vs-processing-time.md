# Event Time vs Processing Time

> **One line:** *when a thing actually happened* vs. *when your system found out about it* — the distinction that makes out-of-order data solvable instead of just confusing.

**Spread:** 5/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## The two clocks

| | **Event time** | **Processing time** |
|---|---|---|
| **Definition** | Timestamp embedded in the data itself (e.g. when a sensor reading occurred) | Wall-clock time when your system observes/processes the record |
| **Why they diverge** | Network delay, retries, offline devices, backfilled files | — |
| **What depends on it** | [[watermarks]], [[windowing-event-time]], correctness of "as of" queries | Throughput/latency metrics, simple monitoring |

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch04_advanced_windowing\|Ch.4 Advanced Windowing]], [[ch03_watermarks\|Ch.3 Watermarks]], [[ch01_streaming_101\|Ch.1 Streaming 101]] | Overwhelmingly the vault's home for this concept (46+45+42 hits) — the entire theoretical model is built on this one distinction |
| Streaming Systems | [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]], [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | The "when" question in the four-question model is *entirely* about this distinction |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | The distributed-systems framing — why you can never fully trust processing time |
| Databricks | [[ch14_cincinnati_reds_case_study\|Ch.14 Cincinnati Reds]] | Real-time sports analytics — a domain where the gap between the two clocks has direct business cost |
| fundamentals_de | [[ch05_data_generation_source_systems\|Ch.5 Data Generation & Source Systems]], [[ch07_ingestion\|Ch.7 Ingestion]] | Where the two clocks first diverge — at the source |
| Airflow | [[ch01_meet_apache_airflow\|Ch.1 Meet Airflow]] | Light touch — `execution_date` semantics brush against this distinction |

---

## The thread

Streaming Systems doesn't just mention this distinction — it's the entire book's organizing axis. Once you accept that event time and processing time are different clocks that drift apart unpredictably, [[watermarks]] (a bet about how far behind event time might be) and [[windowing-event-time]] (grouping by event time despite arrival disorder) both become inevitable, not clever. fundamentals_de's ingestion chapter shows *why* the drift happens in the first place — it's not a processing artifact, it's baked in from the moment data leaves the source system.

## Related

[[watermarks]] · [[windowing-event-time]] · [[late-data]] · [[streams-and-tables]]
