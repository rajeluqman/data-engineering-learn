# Windowing (event-time buckets)

> **One line:** grouping unbounded, endlessly-arriving data into finite chunks by *when it happened*, so you can compute an aggregate at all.

**Spread:** 3/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## ⚠️ Same word, different meaning

This "window" is **not** the SQL `OVER(...)` window from [[sql-window-functions]]. A SQL window groups a *bounded, already-fully-available* result set by a column. An event-time window groups an *unbounded, still-arriving* stream by a time range — the data for a given window might not even be fully present yet when you first see it. They share a name because both "group rows together," but the mechanisms, guarantees, and failure modes are unrelated. See [[sql-window-functions]] for the other sense.

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch04_advanced_windowing\|Ch.4 Advanced Windowing]] | The dedicated deep-dive (57 hits) — fixed, sliding, session, and custom windowing strategies |
| Streaming Systems | [[ch09_streaming_joins\|Ch.9 Streaming Joins]] | Windowing applied to bound join scope — without it, a streaming join never "completes" |
| Streaming Systems | [[ch01_streaming_101\|Ch.1 Streaming 101]], [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]] | Windowing as the "where" question in the four-question streaming model |
| Streaming Systems | [[ch08_streaming_sql\|Ch.8 Streaming SQL]] | Windowing expressed in SQL via `TUMBLE`/`HOP`/session syntax |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | Names the same window types (tumbling, hopping, sliding, session) with a concise selection rule for each |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | Windowing as a transformation-layer concern |

---

## The thread

DDIA Ch.11's one-paragraph summary ("tumbling for simple fixed periods, hopping for smoothed overlapping periods, sliding for a genuinely moving recent interval, session windows for per-user activity-burst grouping") is the fastest way to get oriented before tackling Streaming Systems Ch.4's much deeper treatment of the same four window types plus custom windowing strategies. Windowing only matters because of the [[event-time-vs-processing-time|event-time vs. processing-time]] split — if every event arrived instantly and in order, you wouldn't need a window concept at all, you'd just group by a column like any SQL query.

## Related

[[event-time-vs-processing-time]] · [[watermarks]] · [[late-data]] · [[sql-window-functions]] · [[streams-and-tables]]
