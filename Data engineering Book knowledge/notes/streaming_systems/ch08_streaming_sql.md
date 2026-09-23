# Ch.8 — Streaming SQL

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 249–312 (64 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Relation (closure property)** [S]: "applying any operator from the relational algebra to any valid relation always yields another relation."

(p250)

**Time-varying relation (TVR)** [S]: "a time-varying relation is really just the evolution of a classic relation over time"

(p251).

Rendered as "three-dimensional tables with x- and y-axes as before, but an additional z-axis capturing different versions of the two-dimensional table over time"

(p252).

**Table rendering of a TVR** [D]: observing a TVR at a specific point in time yields a classic point-in-time relation (a table), analogous to the SQL 2011 standard's "temporal tables" plus `AS OF SYSTEM TIME` (p257-258).

**Stream rendering of a TVR** [S]: a `STREAM` query captures "an event-by-event stream capturing the evolution of the time-varying relation over time," using a `Sys.Undo` column to mark retraction rows.

(p259-260)

**Stream/table duality** [S]: "a complete time-varying relation is both a table and a stream at the same time; tables and streams are simply different physical manifestations of the same concept."

(p264-265)

**SCAN-AND-STREAM trigger** [S]: a materialized-view trigger that "starts out like a SCAN trigger, emitting the full contents of the table at a point in time into a stream," then "continues to also trigger all subsequent modifications to the input table, yielding an unbounded stream."

(p281)

## 2. WHAT / WHY / WHEN

**WHAT** [S]: the chapter defines time-varying relations as the conceptual key to integrating streaming into SQL, analyzes the Beam Model's stream bias and classic SQL's table bias via stream/table theory, and proposes concrete SQL language extensions (stream/table selection, temporal operators) with defaults to make robust streaming SQL natural.

**WHY** [S]: "most of what we'll discuss in this chapter is still purely hypothetical as of the time of writing"

(p249).

The goal is to close a real industry gap, since "it's basically impossible to name any existing streaming SQL implementation that has achieved truly broad adoption"

(p251) due to systems historically breaking the relational-algebra closure property when adding streaming support.

**WHEN** [D]: apply time-varying-relation reasoning and the stream/table-selection defaults whenever designing or evaluating a SQL dialect's streaming extensions, or when deciding what a given streaming SQL system's default output rendering (table vs. stream) and default trigger/accumulation semantics should be.

## 3. Assumptions and prerequisites

- Prerequisite: chapter 6's streams-and-tables theory (data at rest vs. data in motion, nongrouping/grouping/ungrouping operations), directly reused as the analytical framework for this chapter (p256, p265-281).
- Prerequisite: chapter 2/3's what/where/when/how questions (transformations, windowing, triggers, accumulation), each explicitly remapped onto proposed SQL extensions (p282-306).
- Assumes the described language extensions (`TABLE`/`STREAM`/`TVR` keywords, `EMIT WHEN`, `Sys.Undo`/`Sys.MTime`/`Sys.EmitTiming`/`Sys.EmitIndex`) are hypothetical proposals, explicitly not implemented in any real system as described, though "some pieces are already implemented in systems like Apache Calcite, Apache Flink, and Apache Beam" (p249).
- Assumes the vision synthesizes "a collaborative discussion between the Calcite, Flink, and Beam communities" begun in 2017, not a single system's actual specification (p249-250).

## 4. Mechanism / key steps

1. Establish relational algebra's closure property as the design constraint: any streaming SQL extension must ensure "the full set of operators from classic relational algebra remain valid when applied to time-varying relations," preserving closure (p254).

2. Define time-varying relations concretely: model a raw dataset's evolution as a sequence of classic relations, each valid over a disjoint, contiguous, half-open time interval (e.g., `[12:03, 12:07)`), such that applying any relational operator to a TVR is equivalent to applying it independently to each classic relation in the sequence (p251-255).

3. Map TVRs onto stream/table theory from chapter 6: a `TABLE` rendering yields the point-in-time snapshot for the observation time; a `STREAM` rendering yields "the sequence of changes" between consecutive snapshots, using `Sys.Undo` to flag retraction rows representing previously reported values now superseded (p256-264).

4. Diagnose the Beam Model's inherent stream bias by overlaying logical and physical pipeline views: because `PCollections` (Beam's data-flow objects) are always streams, tables exist only implicitly (hidden behind sources/sinks or grouping/triggering operations), and triggers must be predeclared (forward-propagating) rather than post-declared (backward-propagating) as of Beam 2.x (p266-270).

5. Diagnose classic SQL's inherent table bias by decomposing a `GROUP BY` query into SCAN (implicit table→stream trigger) → SELECT (nongrouping) → GROUP BY (grouping, stream→table), showing that any materialized intermediate result forces an implicit stream→table conversion even for queries not ending in an explicit grouping operation (e.g., an appended `HAVING` clause) (p270-278).

6. Show that materialized views already provide a form of stream processing in SQL without altering its table bias, by substituting a `SCAN-AND-STREAM` trigger for a plain `SCAN` trigger — the only change needed in the physical execution plan (p278-281).

7. Introduce stream/table selection extensions: `TABLE`/`STREAM`/`TVR` keywords to explicitly choose a query's output rendering, with defaults chosen to minimize explicit use — "If all of the inputs are tables, the output is a TABLE. If any of the inputs are streams, the output is a STREAM" (p283).

8. Introduce temporal operators covering the where/when/how questions: explicit windowing constructs (encapsulating window-computation math and enabling concise session-window expression); an `EMIT WHEN <condition>` trigger clause (e.g., `EMIT WHEN WATERMARK PAST <column>`, optionally combined with `AND THEN AFTER <duration>` for late firings); and default accumulating-and-retracting-mode semantics exposed via a `Sys.Undo` column, toggled off simply by not selecting that column (p284-306).

9. Justify per-record triggering as the SQL-ish default (rather than the Beam Model's single-watermark default) on grounds of simplicity (matching materialized-view semantics) and fidelity (full-fidelity stream rendering, no information lost), while acknowledging its cost downside for high-cardinality aggregates (p293-294).

## 5. Trade-offs and limitations

- Per-record triggering as a default is simple and full-fidelity but costly: "triggers are always applied after a grouping operation, and the nature of grouping often presents an opportunity to reduce the cardinality of data flowing through the system" — defaulting to per-record triggering forfeits that cardinality reduction (p294).
- Watermark triggers give exactly one output per window but "the main downside here is the late data problem due to the use of a heuristic watermark," requiring a combined watermark-plus-late-firing trigger for correctness under late data (p297).
- Accumulating mode (without retractions) is "plain broken for any query/pipeline with a sequence of two or more grouping operations due to over counting"

(p301), making accumulating-and-retracting mode the only sound general default.
- Discarding mode is valuable only for "very simple pipelines that partially aggregate high-volume input data via a single grouping operation and then write them into a storage system" that itself supports aggregation; "outside of those relatively narrow use cases, discarding mode is confusing and error-prone" and the source argues it is not worth adding directly to SQL (p306).
- Explicit windowing constructs are not strictly necessary (ad hoc `GROUP BY`-based windowing already works) but are valuable because they "encapsulate the window-computation math" and make session windows expressible without "a tangled mess of analytic functions, self joins, and array unnesting" (p292-293).

## 6. Failure modes and edge cases

- **Non-idempotent incremental writes without retractions**: writing incremental session-window results to an external key/value store (e.g., HBase) without retractions requires manually detecting which old sessions a new session supersedes, "at significant additional cost, and with a loss of idempotence, which would ultimately leave you unable to provide end-to-end, exactly-once semantics"

(p304).

The source states plainly that this approach "is just not practical"

(p304) for that use case.

- **Late data silently omitted under a bare watermark trigger**: relying solely on `EMIT WHEN WATERMARK PAST <column>` without a late-firing companion trigger means any data arriving after the heuristic watermark passes is never reflected in the emitted stream (p297).
- **Misreading SQL's table bias as a batch-only limitation**: assuming SQL cannot support streaming just because it is table-biased ignores that materialized views already provide streaming via a `SCAN-AND-STREAM` trigger substitution, with no change to the table-biased execution model (p278-281).
- **Confusing a data-driven `EMIT WHEN` proposal with a `HAVING` clause**: a hypothetical `EMIT WHEN Score > 10` construct is, on inspection, equivalent to per-record triggering followed by a `HAVING Score > 10` filter — treating it as a distinct new primitive would be redundant (p300-301).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when designing streaming SQL extensions, preserve the relational-algebra closure property as a hard constraint rather than bolting on separate stream-specific operators, per the source's own diagnosis of why prior streaming SQL systems failed to gain adoption (p250-251).
- **Build** [D]: default new streaming-SQL-like systems to per-record triggering and accumulating-and-retracting mode (toggle retractions off via column projection) rather than requiring explicit trigger/accumulation-mode configuration for common cases, matching the source's recommended defaults (p293-294, p301-306).
- **Maintain** [D]: when a downstream sink needs idempotent incremental writes of grouped/session-windowed results (e.g., to HBase or a similar KV store), ensure the upstream pipeline emits retractions (`Sys.Undo`-equivalent) rather than building custom overlap-detection logic in the sink (p302-305).
- **RCA** [D]: if a streaming aggregation with more than one serial grouping operation is producing overcounted results, check whether the pipeline is running in accumulating mode without retractions — the source identifies this exact combination as "plain broken" (p301).
- **Optimization** [D]: use discarding mode only in the narrow case of a single grouping operation feeding a sink that itself supports aggregation, since it is not a safe general default (p306).

## 8. How to test/verify these claims

- Reproduce the closure-property claim by applying multiple relational operators (filter, group-by/sum) to the same worked TVR example and confirming each yields a valid, well-formed TVR — per the source's own worked filtering and grouping examples over the Julie/Frank score dataset (p254-256).
- Reproduce the stream/table duality claim by rendering the same grouped TVR as both a `TABLE` and a `STREAM` at the same observation times and confirming they encode equivalent information (full history vs. delta-of-changes), per the source's own side-by-side comparison (p259-265).
- Verify the accumulating-mode overcounting failure by constructing a pipeline with two serial grouping operations run in accumulating (non-retracting) mode and confirming inputs are counted multiple times, contrasted with the same pipeline in accumulating-and-retracting mode (p301).
- Verify the retraction-based idempotent-sink claim by running the session-window example both without retractions (Example 8-7) and with retractions (Example 8-8) against a downstream store, confirming only the retracting version allows correct incremental writes without custom overlap logic (p303-306).

## 9. Cross-references

- [[ch02_what_where_when_how|Chapter 2]]: the what/where/when/how questions and the original team-score summation dataset, reused as the running example for temporal-operator proposals (p284-306).
- [[ch03_watermarks|Chapter 3]]: watermark mechanics, reused as the basis for the proposed `EMIT WHEN WATERMARK PAST <column>` trigger clause (p296-298).
- [[ch06_streams_and_tables|Chapter 6]]: streams-and-tables theory, the direct analytical foundation for diagnosing the Beam Model's and SQL's respective biases (p256, p265-281).
- [[ch09_streaming_joins|Chapter 9]] (Streaming Joins): named as covering "strong temporal join support"

(p251), a capability existing streaming SQL implementations were noted as lacking.
- Apache Calcite, Apache Flink, and Apache Beam communities' 2017 joint discussion, credited as the origin of the hypothetical language-extension vision presented in this chapter (p249-250).
- SQL 2011 standard's "temporal tables" and `AS OF SYSTEM TIME` construct, cited as existing precedent for time-varying-relation-like functionality already in SQL (p258).
- Apache Flink's `undo`/`redo` nomenclature, credited as the naming inspiration for the `Sys.Undo` column (p310, footnote).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 8-1 through 8-14 (stream/table bias diagrams, TVR/table/stream renderings, trigger-timing visualizations) | Visual content; described narratively where relevant, not reproduced. |
| Full worked TVR/table/stream ASCII-art renderings for every intermediate example step (dozens of tables across p251-306) | Represented in §4 as mechanism steps and in §8 as verification methods rather than reproducing every intermediate rendering; the pattern (table/stream duality, retraction rows) is captured once in full and referenced thereafter. |
| Full Beam Java code for Examples 8-1 through 8-8 | Reproduced only as prose mechanism/example references in §4-§6; these mirror pipelines already covered in chapters 2, 3, and 6, restated here in a SQL-comparison context. |
