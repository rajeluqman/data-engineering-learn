# Streams & Tables Duality

> **One line:** a stream and a table are two views of the same thing — a table is a snapshot of a stream integrated over time; a stream is the sequence of changes you'd need to replay to reconstruct that table.

**Spread:** widened manually — the automated scanner found this phrasing only in `streaming_systems`, but the same duality is DDIA Ch.11's central claim in different vocabulary. See methodology note in [[_BUILD-SPEC|the build spec]].

---

## ⚠️ Why the automated scan missed this

This is the clearest example in the whole build of why hit-count alone is dangerous. The regex patterns searched for literal phrases like "streams and tables" and "data at rest" — vocabulary specific to Streaming Systems. DDIA Ch.11 makes the *identical* claim using completely different words: "the truth is the log; the database is a cache of a subset of the log." Same idea, zero shared vocabulary, so the scanner scored it as single-source. It isn't.

---

## Where it appears

| Source | Chapter | Angle (verified by reading, not just grep) |
|---|---|---|
| Streaming Systems | [[ch06_streams_and_tables\|Ch.6 Streams & Tables]] | The formal treatment — tables are "data at rest," streams are "data in motion"; every pipeline operation is nongrouping (stream→stream), grouping (stream→table), or ungrouping/triggering (table→stream) |
| Streaming Systems | [[ch08_streaming_sql\|Ch.8 Streaming SQL]] | Applies the duality to SQL — a time-varying relation renders as either a `TABLE` or a `STREAM` |
| Streaming Systems | [[ch09_streaming_joins\|Ch.9 Streaming Joins]] | Joins reframed through the same lens |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] (p467–468) | The same duality stated via calculus: "application state is what you get when you integrate an event stream over time, and a change stream is what you get when you differentiate the state by time." Quotes Pat Helland: "the truth is the log" |
| DDIA | [[ch11_stream_processing\|Ch.11]] (p461–462) | Change Data Capture explicitly described as "turning one database's replication log into a public, consumable stream" — this is the table→stream direction, named CDC instead of "triggering" |

---

## The thread

Both books arrive at the same conclusion from opposite directions. Streaming Systems builds it top-down as pipeline theory: grouping brings data to rest, triggering puts it back in motion. DDIA builds it bottom-up from database internals: a database's replication log *is* the stream; the queryable table is just a cached, materialized view of that log at a point in time. [[change-data-capture|CDC]] is the literal engineering technique that exploits this duality — it's how you turn "table" (a database) into "stream" (a change feed) in production, which is exactly the table→stream direction both books describe theoretically.

## Related

[[change-data-capture]] · [[materialized-views]] · [[batch-vs-streaming]] · [[state-management]]
