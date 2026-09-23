# Ch.2 — The What, Where, When, and How of Data Processing

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 48–84 (37 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Trigger** [S]: "A trigger is a mechanism for declaring when the output for a window should be materialized relative to some external signal."
(p50)

**Watermark** [S]: "A watermark is a notion of input completeness with"
(p50) [D] (source continues "respect to event times. A watermark with value of time X makes the statement: 'all input data with event times less than X have been observed'" across a line wrap and a nested quotation).

**Accumulation mode** [S]: "An accumulation mode specifies the relationship between multiple results that are observed for the same window."
(p50-51)

**The four questions** [S]: "What results are calculated?... Where in event time are results calculated?... When in processing time are results materialized?... How do refinements of results relate?"
(p51-52)

**Pane** [S]: "Each specific output for a window is referred to as a pane of the window."
(p60)

**Perfect vs. heuristic watermark** [S]: "For the case in which we have perfect knowledge of all of the input data, it's possible to construct a perfect watermark."

"For many distributed input sources, perfect knowledge of the input data is impractical, in which case the next best option is to provide a heuristic watermark."
(p66)

**Early/on-time/late trigger** [S]: "This is known as the early/on-time/late trigger because it partitions the panes that are materialized by the compound trigger into three categories:"
(p70)

**Allowed lateness** [S]: "any real-world out-of-order processing system needs to provide some way to bound the lifetimes of the windows it's processing."
(p73)

"A clean and concise way of doing this is by defining a horizon on the allowed lateness within the system"
(p73).

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter builds out the Beam Model's five core concepts (event/processing time, windowing, triggers, watermarks, accumulation) through one running worked example (per-team score summation), organized around four framing questions: what, where, when, how.

**WHY** [S]: "we're now going to focus further on the data processing patterns from Chapter 1, but in more detail, and within the context of concrete examples... these are the tools for reasoning about time that truly get you beyond classic batch processing."
(p48)

**WHEN** [D]: use repeated update triggers when periodic, eventually-consistent refinement is acceptable and no explicit completeness signal is needed (materialized-view-style use cases); use watermark/completeness triggers (alone or combined into early/on-time/late) when reasoning about missing data (e.g. outer joins, anomaly detection) requires an explicit "input is believed complete" signal; use allowed lateness whenever the keyspace/window count is unbounded and persistent state must eventually be garbage collected; choose accumulation mode (discarding/accumulating/accumulating-and-retracting) based on whether the downstream consumer aggregates deltas itself, overwrites by key, or needs to reconcile against re-keyed/merged windows.

## 3. Assumptions and prerequisites

- Prerequisite: event time vs. processing time and windowing (fixed/sliding/sessions) from chapter 1, directly extended here (p49, "We've already covered two of them").
- Uses Apache Beam Java pseudocode and time-lapse diagrams throughout as the concrete vehicle for every concept, chosen because "it most completely embodies the concepts described in this book" rather than because the book is about Beam specifically (p48-49).
- Assumes the running example: a mobile game team-score summation over nine records with explicit `EventTime`/`ProcTime` columns (p52-53, the "UserScores" table).

## 4. Mechanism / key steps

1. Run the baseline unwindowed batch pipeline (`Sum.integersPerKey()` with no windowing) which accumulates all input before producing a single output once all data has been seen (p56-57, Example 2-1, Figure 2-3).

2. Add fixed two-minute windowing (`Window.into(FixedWindows.of(TWO_MINUTES))`) to a batch pipeline, producing one output per window once all input is consumed (p58-59, Example 2-2, Figure 2-5).

3. Add a per-record repeated-update trigger (`triggering(Repeatedly(AfterCount(1)))`) to get multiple panes per window on a streaming engine, converging toward correctness over time but at the cost of high chattiness for high-volume keys (p61-62, Example 2-3, Figure 2-6).

4. Reduce chattiness with a processing-time-delay repeated trigger, either aligned (`AlignedDelay`, all windows update simultaneously — effectively microbatching, bursty load) or unaligned (`UnalignedDelay`, load spread evenly across time; generally preferred at scale) (p62-63, Examples 2-4/2-5, Figures 2-7/2-8).

5. Add a watermark-based completeness trigger (`triggering(AfterWatermark())`) to materialize a window's output only once the watermark asserts the window's input is complete, enabling correct reasoning about missing data (p66-68, Example 2-6, Figure 2-10).

6. Combine both trigger types into an early/on-time/late trigger: `AfterWatermark().withEarlyFirings(AlignedDelay(...)).withLateFirings(AfterCount(1))` — early panes give low-latency speculative updates before the watermark passes, a single on-time pane asserts completeness, and late panes handle any data arriving after the watermark incorrectly advanced past it (p70-72, Example 2-7, Figure 2-11).

7. Bound per-window state lifetime with allowed lateness (`.withAllowedLateness(ONE_MINUTE)`), closing (discarding all state for) a window once the watermark passes its lateness horizon, dropping any data that arrives even later (p73-75, Example 2-8, Figure 2-12).

8. Choose an accumulation mode for how successive panes relate: `discardingFiredPanes()` (each pane is independent; downstream must sum panes itself) (p78-79, Example 2-9, Figure 2-13); default accumulating mode (each pane includes all prior data, safe to overwrite) (p76-77); or `accumulatingAndRetractingFiredPanes()` (each new pane also emits an explicit retraction of the prior pane's value, needed for re-keying or window-merging consumers) (p79-80, Example 2-10).

## 5. Trade-offs and limitations

- Per-record triggering "is that it's quite chatty."
(p61) Particularly harmful for high-volume keys, and aggregations that reduce stream cardinality mitigate this.
- Aligned processing-time delays are predictable but "results in bursty workloads that often require greater peak provisioning"
(p62), while unaligned delays spread load more evenly with the same average latency.
- Watermarks that are too slow delay output even when a specific window's data is actually complete, since "the late arriving 9 holds back the watermark for all the subsequent windows" (p68-69); watermarks that are too fast (heuristic-only) cause premature, incorrect materialization when late data arrives afterward (p69-70). "You simply cannot get both low latency and correctness out of a system that relies solely on notions of completeness."
(p69-70)
- Choosing accumulation mode trades cost against consumer convenience: "the modes in the order presented (discarding, accumulating, accumulating and retracting) are each successively more expensive in terms of storage and computation costs."
(p80)
- High (Spark Structured Streaming style) watermarks are "more prone to incorrectly discarding data" than low watermarks, though they can work adequately if skew stays within a constant delta (p73-74).

## 6. Failure modes and edge cases

- **Heuristic watermark advancing too early**: if the algorithm omits a value from its completeness estimate, the watermark can pass the end of a window before all its data has arrived, producing an outright incorrect result (the book's worked example produces 5 instead of the correct 14) (p67-68).
- **Long time-to-first-output under watermark-only triggering**: in the worked example, the second window took "nearly seven minutes from the time the first value in the window occurs until we see any results" using only a completeness trigger, motivating the early/on-time/late combination (p68-69).
- **Unbounded state growth without allowed lateness**: "when dealing with an unbounded data source, it's often not practical to keep state (including metadata) for a given window indefinitely; we'll eventually run out of disk space" without a lateness horizon bounding window lifetime (p72-73).
- **Retraction-blind downstream regrouping**: if a downstream consumer regroups data by a different dimension without retraction support, a superseding value "can't just overwrite the old value" because it may land in a different group entirely — silently leaving stale data behind (p76-77).
- **Processing-time-based garbage collection vulnerable to pipeline stalls**: specifying the lateness horizon in processing time (rather than event time) "would leave the garbage collection policy vulnerable to issues within the pipeline itself (e.g., workers crashing, causing the pipeline to stall for a few minutes)," which could prematurely close windows that hadn't actually had a chance to receive their late data (p73).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: frame every unbounded-data pipeline design decision through the four questions (what/where/when/how) — transformation, windowing strategy, trigger/watermark policy, and accumulation mode — as an explicit, separately-tunable set of knobs rather than a single monolithic choice (p51-52).
- **Build** [D]: default to unaligned processing-time delays over aligned ones for repeated-update triggers at scale, since they avoid bursty, simultaneously-firing workloads (p62-63).
- **Maintain** [D]: always pair a heuristic watermark with an explicit allowed-lateness horizon in production, since indefinite state retention is not viable for genuinely unbounded keyspaces (p72-73) — except for the specific case of a tractably bounded keyspace with global aggregates, where no lateness horizon is needed (p75-76).
- **RCA** [D]: if a windowed aggregate's output looks wrong for a period and then "self-corrects" later, check for a heuristic watermark that advanced early and then received late data past that point — this is the "too fast" watermark failure mode, not necessarily an application bug (p69-70).
- **Optimization** [D]: use discarding accumulation mode when the downstream system already aggregates deltas (lower storage/compute cost); use accumulating-and-retracting only when downstream re-keying or window merging genuinely requires explicit retractions, since it's the most expensive mode (p80).

## 8. How to test/verify these claims

- Reproduce the perfect-vs-heuristic-watermark divergence by running the same nine-record dataset (p52-53) through both watermark implementations and confirming the heuristic version produces an incorrect early result (5 instead of 14) for the first window while the perfect version does not (p67-68, Figure 2-10).
- Verify the early/on-time/late trigger's time-to-first-output improvement by comparing the pure-watermark pipeline (Example 2-6) against the combined pipeline (Example 2-7) on the same dataset and confirming the reduction from ~7 minutes to ~3.5 minutes for the second window (p71).
- Verify allowed-lateness behavior by running Example 2-8 with a one-minute lateness horizon and confirming a late value arriving within the horizon (the described value 6) is incorporated, while one arriving beyond it (value 9) is dropped (p74-75, Figure 2-12).
- Verify the three accumulation modes' arithmetic directly against Table 2-1 (p77-78): discarding mode's final pane value (9) undercounts vs. the correct sum (12), accumulating mode's pane-sum (15) overcounts, and accumulating-and-retracting gives the correct answer (12) under both interpretations.

## 9. Cross-references

- [[ch01_streaming_101|Chapter 1]]: event time/processing time distinction and basic windowing definitions, directly extended throughout this chapter (p48-49).
- [[ch03_watermarks|Chapter 3]] (watermarks deep dive, authored by "Slava"): referenced repeatedly as the detailed treatment of watermark internals only introduced at a conceptual level here (p50, p61, p66).
- [[ch08_streaming_sql|Chapter 8]] (streaming SQL / time-varying relations): referenced for a detailed example of retraction handling under dynamic window merging (p77).
- streamingbook.net: cited as the source of fully animated versions of this chapter's time-lapse diagrams (p56).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 2-1 through 2-14 (time-lapse diagrams, windowing diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Apache Beam Java pseudocode syntax details beyond what's needed to convey each concept | Representative code snippets cited per step; the source itself notes this is "pseudocode" simplified for clarity (p54), not exact production Beam API. |
| Full Table 2-1 layout | Values and their interpretation captured in prose in §8; full table reproducible from the source PDF directly. |
