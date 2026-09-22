# Persistent State Management

> **One line:** the memory a long-running pipeline needs to keep between records — without it, a streaming job can't do anything beyond stateless row-by-row transforms.

**Spread:** 3/6 book sources · Python track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch07_practicalities_of_persistent_state\|Ch.7 Persistent State]] | The dedicated, deepest treatment — raw grouping, incremental combining (`CombineFn`), and full generalized state with timers |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | Historical context — how different systems (Flink, Dataflow) implemented state persistence and recovery differently |
| Streaming Systems | [[ch01_streaming_101\|Ch.1 Streaming 101]], [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]] | State as a prerequisite concept referenced before it's formally introduced |
| DDIA | [[ch01_reliable_scalable_maintainable_applications\|Ch.1 Reliable, Scalable, Maintainable Applications]] | The foundational reliability framing state management serves |
| Airflow | [[ch17_airflow_deployment_options\|Ch.17 Deployment Options]] | Light touch — metastore/scheduler state as an operational concern |

---

## The thread

This is Streaming Systems Ch.7's chapter to own — nothing else in the vault attempts its depth. Its escalation ladder (raw grouping → incremental combining → full generalized state with timers) is worth internalizing as a design decision, not just chapter structure: default to the cheapest option that works, and only reach for full state-with-timers when a genuine requirement (like the chapter's conversion-attribution example) demands it. [[checkpointing-and-recovery]] is the other half of this concept — state is only useful if it survives a failure, which is exactly what checkpointing exists to guarantee.

## Related

[[checkpointing-and-recovery]] · [[aggregation-and-combiners]] · [[batch-vs-streaming]] · [[streams-and-tables]]
