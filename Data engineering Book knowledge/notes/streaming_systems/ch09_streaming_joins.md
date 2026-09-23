# Ch.9 — Streaming Joins

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 313–359 (47 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Core thesis** [S]: "at their hearts, all joins are streaming joins"

(p313), since "joins are just a specific type of grouping operation" and "grouping operations always consume a stream and yield a table."

**FULL OUTER join (as the conceptual base)** [S]: "the result of FULL OUTER–joining two datasets is essentially the full list of rows in both datasets, with rows in the two datasets that share the same join key combined together, but unmatched rows for either side included unjoined."

(p316)

**SEMI join cardinality subtlety** [S]: "because the values on the M side are not being returned, the SEMI join simply predicates the join condition on there being any matching row on the right, rather than repeatedly yielding a new result for every matching row."

(p327)

**Temporal validity window** [S]: validity windows apply "in situations in which the rows in a relation effectively slice time into regions wherein a given value is valid."

(p340)

**Shrinking window** [S]: "Validity windows must be able to shrink over time, thereby diminishing the reach of their validity and splitting any data contained therein across the two new windows."

(p344)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: the chapter analyzes all SQL join types (FULL OUTER, LEFT/RIGHT OUTER, INNER, ANTI, SEMI, CROSS) as variations of a single grouping-based pattern under stream/table/TVR theory, then covers windowed joins — fixed windows and the more advanced temporal validity windows — as extensions of the same core idea.

**WHY** [S]: joins have historically seemed intimidating because "the language of joins is expressive and expansive," compounded by "the dimension of time that streaming brings to the table"

(p313); the chapter's goal is to show that "after you understand the central ideas and themes of joins, the broader landscape...becomes so much more accessible" (p313).

**WHEN** [D]: apply unwindowed (global-window, per-record-triggered) joins by default; add fixed windowing when a business need requires partitioning by a time boundary (e.g., daily billing) or when a watermark-based reference point is needed to time out unmatched outer-join rows; apply temporal validity windows specifically when a relation's rows each define a "valid until superseded" time region (e.g., a table of currency conversion rates).

## 3. Assumptions and prerequisites

- Prerequisite: chapter 6's stream/table theory (grouping operations consume streams and yield tables), the direct basis for the chapter's core "all joins are streaming joins" thesis (p313).
- Prerequisite: chapter 8's time-varying relation (TVR) vocabulary and `TABLE`/`STREAM`/`TVR` keywords plus `Sys.Undo`/`Sys.EmitTime` system columns, used throughout to render every join example in table, TVR, and stream form (p317-319).
- Prerequisite: watermark mechanics (chapters 2-3), reused as the mechanism for timing out unmatched outer-join rows once a window's watermark passes (p334-335).
- Assumes, for most of the chapter, equi-joins with at most 1:1 cardinality for simplicity, before relaxing to arbitrary N:M cardinality specifically to illustrate SEMI join semantics (p315, p326-330).
- Assumes the language extensions used (`VALIDITY_WINDOW`, `WINDOW_START`/`WINDOW_END`) are hypothetical, and explicitly notes "no existing streaming system today supports natively" windows that can split/shrink over time as validity windows require (p357-358).

## 4. Mechanism / key steps

1. Establish the FULL OUTER join as the conceptual base case: it includes every row from both input datasets, with matched rows combined and unmatched rows padded with `null` on the missing side (p316-317).

2. Render a join's evolution using all three TVR physical forms — a point-in-time `TABLE` snapshot, the full `TVR` sequence of interval-scoped snapshots, and a `STREAM` of deltas (including `Sys.Undo` retraction rows for values later superseded) — showing all three are equivalent views of the same underlying data (p317-319).

3. Derive every other join type as a filtered subset of the FULL OUTER join: LEFT OUTER removes unjoined-right rows; RIGHT OUTER removes unjoined-left rows; INNER removes all unjoined rows from either side (the intersection of LEFT and RIGHT OUTER); ANTI keeps only the unjoined rows (INNER's complement); CROSS is FULL OUTER with a vacuously true join predicate (p315-316, p361-372 mechanism per type).

4. Handle SEMI joins' N:M-cardinality subtlety by predicating on existence of any matching row on the dropped side rather than de-duplicating one column of an otherwise-duplicating INNER join result — demonstrated by contrasting `INNER JOIN` (which duplicates the kept side's rows once per match) against `SEMI JOIN` (which keeps each kept-side row exactly once) on a dataset with explicit N:M cardinality labels (p326-333).

5. Apply fixed windowing to a join by adding window equality to the join predicate (e.g., `Left.Num = Right.Num AND Left.Window = Right.Window`), which scopes matching to rows falling in the same time window and changes which rows are considered joined versus permanently unjoined (p335-339).

6. Use a window's watermark as a reference point to time out unmatched outer-join rows: once the watermark passes the end of the window, the system can safely materialize any still-unjoined rows as final, since unbounded input otherwise provides no such completeness signal (p334-335).

7. Construct temporal validity windows incrementally from a stream of rate-change events, where each new row narrows (shrinks) the validity region of the row(s) before it — demonstrated via a `VALIDITY_WINDOW(EventTime)` grouping construct that produces windows like `[12:00, 12:03)`, `[12:03, 12:06)`, `[12:06, +inf)` from raw currency-rate arrival timestamps (p340-345).

8. Perform a temporal validity join by first computing the validity-windowed version of the rate relation, then joining it to an orders relation using window-boundary predicates (`WINDOW_START(Window) <= EventTime AND EventTime < WINDOW_END(Window)`), correctly attributing each order to the exchange rate valid at its event time even under out-of-order arrival on both sides of the join (p346-349).

## 5. Trade-offs and limitations

- The FULL-OUTER-plus-filter mental model is conceptual, not necessarily an efficient implementation: "there are many different ways to implement each of these types of joins, some of which are likely much more efficient than performing an actual FULL OUTER join and then filtering down its results" (p358, footnote).
- ANTI joins are retraction-heavy: "the ANTI join is as heavy on retractions as the INNER join is light"

(p325), since rows that eventually do join must first appear (falsely) as unjoined and then be retracted.
- Temporal validity windows require a windowing framework supporting windows that shrink and split data across two new windows over time — a capability the source states "Beam does not currently provide," describing its own reference implementation as only "a partial implementation" that "only works if the windows exist in isolation" (p358, footnote).
- A single new input row to a validity-windowed relation can force "transactional modifications to multiple output rows"

(p343), which the source likens to the multirow transactions already seen in building up session windows — a correctness requirement, not merely a convenience concern.
- Windowing a join versus leaving it unwindowed is a real trade-off, not merely stylistic: unwindowed joins keep matching globally in scope (useful when a match could arrive arbitrarily late), while fixed windowing intentionally excludes matches that fall in different time buckets even if they would otherwise satisfy the join key (p335-339).

## 6. Failure modes and edge cases

- **Assuming SEMI join behaves like a de-duplicated INNER join in the N:M>1 case**: because SEMI join simply checks for existence of any match rather than de-duplicating INNER's row-per-match output, treating them as interchangeable when the dropped side has multiple matches per key produces different row counts and different retraction behavior (p326-330).
- **Waiting indefinitely for outer-join completeness on unbounded data without a windowed watermark reference**: without windowing plus a watermark, there is no principled point at which to materialize an unmatched outer-join row as final, since unbounded input never technically completes (p334-335).
- **Out-of-order arrival corrupting naive validity-window construction**: because "every time a new rate arrives, the previous rate changes from being valid forever to being valid until the arrival time of the new rate"

(p341), and this problem compounds under out-of-order arrival, naively building validity windows without accounting for retroactive region-splitting produces an inconsistent or stale view.
- **Complex multi-row updates from a single new validity-window input**: a system that assumes one new record triggers at most one row-level update will miscompute validity-windowed relations, since a single new rate arrival can require simultaneous updates to two existing rows' validity boundaries (p343).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when designing a join-heavy streaming pipeline, default to unwindowed (global-window) joins with per-record or watermark-based triggering unless a specific business need (time-bucketed matching) or performance constraint calls for fixed windowing, per the chapter's own framing of windowing as optional, not mandatory, for streaming joins (p334-335).
- **Build** [D]: when implementing a SEMI join over data with N:M cardinality, verify the implementation checks for match existence rather than reusing INNER-join logic with a projection dropping columns — a naive reuse would silently produce duplicate rows (p326-330).
- **Maintain** [D]: any pipeline consuming a currency-rate-like current-value-valid-until-superseded relation should be modeled explicitly as a temporal-validity-windowed relation and joined via window-boundary predicates, rather than joining against only the latest known rate, to remain correct under out-of-order and late-arriving rate updates (p346-349).
- **RCA** [D]: if a downstream outer join never resolves unmatched rows for unbounded data, check whether the join lacks both windowing and a watermark-based completeness reference — the chapter identifies this exact combination as required to time out unmatched rows (p334-335).
- **Optimization** [D]: do not assume a literal FULL-OUTER-join-then-filter execution strategy is required for the other join types; the conceptual derivation is for understanding semantics, and real systems should choose more efficient physical implementations based on query shape and data distribution (p358, footnote).

## 8. How to test/verify these claims

- Reproduce the FULL-OUTER-as-base-case claim by deriving LEFT OUTER, RIGHT OUTER, INNER, and ANTI from a single FULL OUTER join result via row filtering, and confirming each matches the join type's independently defined semantics on the same `Left`/`Right` example datasets (p316-326).
- Verify the SEMI join cardinality behavior by running both `INNER JOIN` and `SEMI JOIN` against the N:M `LeftNM`/`RightNM` datasets and confirming INNER produces duplicate rows for cardinality-M>1 keys while SEMI does not (p326-333).
- Verify the fixed-windowed-join claim by comparing the unwindowed and 5-minute-fixed-windowed renderings of the same `Left`/`Right` join and confirming rows falling in different windows (e.g., L2/R2) are treated as unjoined in the windowed version but joined in the unwindowed version (p335-339).
- Verify the temporal validity join's correctness under out-of-order arrival by replaying the `YenRates`/`YenOrders` example in a different arrival order and confirming the final joined `TABLE` snapshot still correctly attributes each order to its event-time-valid rate, despite differing intermediate `STREAM`/TVR evolution (p346-352).

## 9. Cross-references

- [[ch06_streams_and_tables|Chapter 6]]: stream/table theory (grouping = stream→table), the direct conceptual foundation for "all joins are streaming joins" (p313).
- [[ch08_streaming_sql|Chapter 8]]: TVR theory and the `TABLE`/`STREAM`/`TVR`/`Sys.Undo`/`Sys.EmitTime` vocabulary, used throughout to render every join example (p317-319).
- Chapters 2 and 3: watermark mechanics, reused for timing out unmatched windowed outer-join rows (p334-335).
- Julian Hyde's "Streams, joins, and temporal tables" document, credited as the source of "the example data and the temporal join use case motivating it," lifted "almost wholesale" (p358, footnote).
- [[ch10_evolution_of_large_scale_data_processing|Chapter 10]] (The Evolution of Large-Scale Data Processing): not explicitly cross-referenced within this chapter's visible text, but follows as the book's closing chapter per `CHAPTER_MAP.csv` sequencing.

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figure 9-1 (temporal validity windowing animation) | Visual content; described narratively in §4/§6, not reproduced. |
| Full side-by-side ASCII-art join-result tables for every join type (FULL OUTER/LEFT/RIGHT/INNER/ANTI/SEMI, unwindowed and windowed, on both the simple and N:M-cardinality datasets) | Represented in §4 as mechanism steps and in §8 as verification methods; the derivation pattern (filter FULL OUTER) is captured once in full rather than reproducing dozens of near-identical result tables. |
| Full SQL/Beam code for every worked example (Examples/queries across p313-359, including the standard-SQL three-way self-join sidebar for validity windows) | Reproduced only as prose mechanism steps; these are illustrative hypothetical-SQL renderings, explicitly marked by the source as not implemented in any real system as described (p249, carried into this chapter). |
