# Joins

> **One line:** combining rows from two datasets that share a key — the same relational-algebra operation, whether both sides are static tables or one side is a never-ending stream.

**Spread:** 3/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch09_streaming_joins\|Ch.9 Streaming Joins]] | The deepest, most rigorous treatment (28 hits) — the central claim: *every* join is a streaming join at heart; `INNER`/`LEFT`/`RIGHT`/`FULL` are all filtered views of one `FULL OUTER` join |
| Streaming Systems | [[ch01_streaming_101\|Ch.1 Streaming 101]], [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]], [[ch08_streaming_sql\|Ch.8 Streaming SQL]] | Joins woven into the broader streaming model |
| Kimball | [[ch08_customer_relationship_management\|Ch.8 CRM]] | Fact-to-fact join warnings — an explicit, named hard failure mode when done incorrectly |
| Kimball | [[ch02_dimensional_modeling_techniques_overview\|Ch.2 Dimensional Modeling Techniques]] | Join cardinality as it affects dimensional design |
| Databricks | [[ch07_optimizing_materialized_views_recomputes\|Ch.7 Materialized View Recomputes]] | Complex joins named as one of the specific triggers that force a full (not incremental) recompute |

### Your own track notes

- SQL track — heaviest coverage: [[master_sql_data_with_baraa\|Baraa]] (82), plus dedicated `M3-joins-set-ops` module, both quiz sets, Ansh Lamba notes
- [[dialect-map]], [[errors-gotchas]] — join-specific dialect quirks already logged

---

## The thread

Your SQL-track join fundamentals (`INNER`/`LEFT`/`RIGHT`/`FULL`, set operations) are the static-table special case of what Streaming Systems Ch.9 generalizes fully: a `SEMI` join (mentioned in your own SQL notes as "kind of weird") turns out to be exactly the mechanism that solves [[deduplication]]'s N:M-cardinality fan-out problem — the same join type shows up in both places for the same reason. Kimball's fact-to-fact join warning is a *dimensional-modeling-specific* instance of a cardinality mistake: joining two fact tables directly without a shared conformed dimension multiplies rows unpredictably, which is a special case of the general join-cardinality awareness Streaming Systems Ch.9 builds from scratch.

## Related

[[deduplication]] · [[dimensional-modeling]] · [[streams-and-tables]] · [[windowing-event-time]]
