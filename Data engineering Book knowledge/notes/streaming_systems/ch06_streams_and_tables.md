# Ch.6 — Streams and Tables

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 174–214 (41 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Tables (independent definition)** [S]: "Tables are data at rest."

(p177)

**Streams (independent definition)** [S]: "Streams are data in motion."

(p177)

**Special Theory of Stream and Table Relativity** [S]: "Streams → tables: The aggregation of a stream of updates over time yields a table."

"Tables → streams: The observation of changes to a table over time yields a stream."

(p176)

**Nongrouping operation** [S]: "These operations (as we saw in Map and Reduce) simply accept a stream of records and produce a new, transformed stream of records on the other side."

(p186)

**Grouping operation** [S]: "These operations (as we saw in MapWrite and ReduceWrite) accept a stream of records and group them together in some way, thereby transforming the stream into a table."

(p186)

**Ungrouping (triggering) operation** [D]: the table-to-stream conversion counterpart to grouping — a trigger fires against a table, pulling data at rest back into motion as a stream.

## 2. WHAT / WHY / WHEN

**WHAT** [S]: "the point of this chapter is twofold: To try to describe the relationship between the Beam Model...and the theory of 'streams and tables'...[and] to bombard you with bad physics analogies."

(p174-175)

**WHY** [S]: "a clear understanding of how they relate is particularly informative when considering how robust stream processing concepts might be cleanly integrated into SQL"

(p175)

**WHEN** [D]: apply streams-and-tables reasoning whenever deciding how to expose intermediate pipeline state directly as a queryable table (avoiding a redundant sink), or when reasoning about how batch and streaming pipelines relate conceptually rather than assuming they are fundamentally different execution models.

## 3. Assumptions and prerequisites

- Prerequisite: the four what/where/when/how questions (transformations, windowing, triggers, accumulation) from chapters 2-4, each explicitly remapped onto the streams/tables framework in this chapter's own structure (p185-200).
- Assumes familiarity with the Beam Model's `PCollection`/`Window`/`Trigger`/`CombineFn` API surface, used as the concrete running example throughout (Examples 6-1 through 6-6).
- Draws on prior database-systems concepts (append-only logs, materialized views, database triggers) as the historical origin of streams/tables theory, attributed by the source to "Martin Kleppmann and Jay"

(p174) — [D] (source continues, naming Kreps, on p175, across a page break).

## 4. Mechanism / key steps

1. Derive the stream-to-table direction from the database world: an append-only transaction log (the stream) is serially applied to materialize a table, so "the table is just the result of applying the transaction log of updates found in the stream" (p175).

2. Derive the table-to-stream direction via materialized views: a materialized view's changelog captures every change made to the source table, which is exactly what a "stream" is in this framework (p175-176).

3. Analyze a classic bounded MapReduce job as a six-stage streams/tables pipeline (MapRead, Map, MapWrite, ReduceRead, Reduce, ReduceWrite), showing the topology TABLE → STREAM → STREAM → TABLE → STREAM → STREAM → TABLE — i.e., that even batch processing over bounded data is streams and tables under the covers (p178-184, Figures 6-1/6-2).

4. Generalize batch processing into a four-step repeating pattern: "Tables are read in their entirety to become streams."

"Streams are processed into new streams until a grouping operation is hit."

"Grouping turns the stream into a table."

(p185), and repeat until the pipeline runs out of stages.

5. Remap the four what/where/when/how questions onto streams/tables: transformations (what) split into nongrouping (stream→stream) and grouping (stream→table) categories (p186-187); windowing (where) folds the window into an implicit (or, for merging windows, hierarchical) composite grouping key (p190-193); triggers (when) are the ungrouping operations that convert a table back into a stream, directly analogous to classic database triggers (p193-198); accumulation (how) determines whether the resulting stream carries deltas, full values, or values-plus-retractions (p199-200).

6. Walk a full pipeline (team-score summation with early/on-time/late triggering) from its logical plan (Figure 6-13) through a physical execution plan (Figure 6-14), classifying each physical operation (`ReadFromSource`, `Parse`, `AssignWindows`, `GroupMergeAndCombine`, `Trigger`, `WriteToSink`) as stream→stream, stream→table, or table→stream (p200-207).

7. State the General Theory of Stream and Table Relativity: data processing pipelines consist of tables, streams, and operations upon them; operations are exactly one of stream→stream (nongrouping), stream→table (grouping, incorporating windowing/merging), table→stream (ungrouping/triggering, incorporating watermarks and accumulation mode), or table→table, which the source states does not exist (p208-209).

## 5. Trade-offs and limitations

- Serving results directly from a pipeline's internal state table (rather than materializing to a separate sink) "saves on compute resources by not requiring an additional sink stage in the pipeline to materialize the outputs"

(p189).

But this requires care: "you need to take care to ensure that only the data processing pipeline has the ability to make modifications to the table"

(p189), since external modification breaks consistency guarantees.
- Merging windows require treating key+window as a hierarchical composite key (key as root, window as child) rather than a flat composite key, because "the system doesn't really treat the key/window pair as a flat composite key" — this is necessary "to provide the strong consistency needed for correctness guarantees," making key (not key+window) the unit of atomicity/parallelization (p191-192).
- Trigger names deliberately make weak guarantees (e.g., `AfterWatermark` "makes no guarantees how far beyond the end of the window the watermark may be when it fires") because "it's essentially impossible to guarantee that an AfterWatermark trigger will fire while the watermark is precisely at the end of any given window" except in extremely limited circumstances (p197-198).
- Classic batch systems support only a single trigger type in practice (input-complete), since "most existing batch processing systems have been designed with this lock-step read-process-group-write-repeat sequence in mind"

(p197), limiting where finer-grained triggering could even manifest.

## 6. Failure modes and edge cases

- **External mutation of a served state table**: if any actor other than the pipeline itself writes to the state table being served directly as query output, "all bets are off regarding consistency guarantees" (p189).
- **Confusing partitioning with grouping**: partitioning-by-key alone ensures records with the same key reach the same machine but "doesn't do anything to actually bring the data to rest"

(p207) — records remain in motion (a stream), so treating a partition step as if it were a grouping step would misdiagnose where data actually settle, per the source's own distinction footnoted at p212.
- **Keyless ReduceWrite output misunderstood as ungrouped**: when Reduce output has no user-supplied key, the system implicitly assigns each record a unique key (akin to `AUTO_INCREMENT`) and groups each record with itself — a naive reading might assume no grouping occurs at all, but a group-by-key operation conceptually still happens (p182-183).
- **Assuming trigger timing precision that isn't guaranteed**: relying on `AfterWatermark` or `AfterCount(N)` to fire at an exact instant or exact count is a misuse of the trigger semantics, since both only provide a lower-bound guarantee, not a precise one (p197-198).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when a pipeline's grouping stage produces the pipeline's final output, consider exposing that internal state table directly for serving rather than adding a redundant sink stage — provided the pipeline retains sole write access to that table (p189).
- **Build** [D]: when implementing or debugging a custom windowing/merging strategy, model the grouping key as hierarchical (key, then window as child) rather than flat, matching how real systems achieve atomicity/consistency for window merges (p191-192).
- **Maintain** [D]: when integrating streams/tables reasoning into a system's SQL layer (the source's own stated motivation, p175), map grouping operations to SQL `GROUP BY`/aggregation semantics and triggers to SQL materialized-view refresh semantics as the natural translation points.
- **RCA** [D]: if a pipeline stage appears to neither aggregate nor filter records but downstream consumers see unexpected latency or batching, check whether it is a grouping (stream→table) stage — the source's own classification is a direct diagnostic tool for finding where data unexpectedly comes to rest (p206-207).
- **Optimization** [D]: exploit the fact that grouping operations are the only stages requiring persistent/checkpointed storage — prefer fusing chains of nongrouping (stream→stream) operations together to avoid unnecessary serialization/network overhead, matching the source's own description of physical-plan fusion (p204-205).

## 8. How to test/verify these claims

- Reproduce the MapReduce streams/tables topology claim by instrumenting a real MapReduce (or Beam batch) job's six conceptual phases and confirming the TABLE → STREAM → STREAM → TABLE → STREAM → STREAM → TABLE pattern described in Figure 6-2 (p178-184).
- Verify the nongrouping/grouping/ungrouping operation taxonomy by tracing the physical execution plan of a real Beam pipeline (Figure 6-14) and confirming each named physical operation (`Parse`, `AssignWindows`, `GroupMergeAndCombine`, `Trigger`, `WriteToSink`) matches its predicted stream→stream / stream→table / table→stream classification (p204-207).
- Verify the "no table→table operations exist" claim by attempting to construct a counterexample pipeline stage that transforms one table directly into another table without an intervening stream — per the source's own reasoning, this should be impossible because "it's not possible for data to go from rest and back to rest without being put into motion" (p209).
- Verify the trigger-as-ungrouping claim experimentally by comparing the per-record-trigger visualization (Figure 6-8) against the watermark-completeness-trigger visualization (Figure 6-10) on the same input, confirming both show data being pulled out of the state table into a stream, differing only in when/how much is pulled (p193-196).

## 9. Cross-references

- Chapter 1: cardinality vs. constitution dimensions, with this chapter finally addressing the previously-deferred constitution (stream vs. table) dimension (p174).
- Chapter 2: the four what/where/when/how questions and the original team-score summation example, directly reused and reframed throughout this chapter (p185-200).
- Chapter 3: watermark mechanics, reused here as the completeness signal driving `AfterWatermark` triggers in the streams/tables framing (p195, p209).
- Chapter 8 (Streaming SQL): named as the chapter where this streams/tables theory is applied to integrating streaming concepts into SQL (p175).
- "The Dataflow Model" paper, section 2.2.2, referenced for a closer treatment of window-merging semantics (p192).
- Prior work by Julian Hyde (streams as derivatives of tables, tables as integrals of streams, p177) and the Kafka/Flink communities' "folks championing stream processors as a database"

(p189) framing, both credited as origins/parallel articulations of this chapter's theory.

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 6-1 through 6-14 (event-time/processing-time diagrams, streams-and-tables topology diagrams, logical/physical plan diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Java/Beam code for Examples 6-1 through 6-6 | Reproduced only as prose mechanism steps in §4; these are the same running pipeline example from chapter 2, reframed, not new implementation content. |
| Extended physics-analogy narrative framing ("Special/General Theory of Stream and Table Relativity" humor, footnoted asides) | Rhetorical device; the underlying technical claims are captured directly in §1/§4/§7 without the analogy's narrative wrapper. |
