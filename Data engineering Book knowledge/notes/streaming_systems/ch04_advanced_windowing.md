# Ch.4 — Advanced Windowing

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 124–148 (25 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Processing-time windowing (in an event-time-first model)** [S]: two methods — "Ignore event time (i.e., use a global window spanning all of event time) and use triggers to provide snapshots of that window in the processing-time axis."

"Assign ingress times as the event times for data as they arrive, and use normal event-time windowing from there on."
(p125)

**Session window (recap)** [S]: "Sessions are a special type of window that captures a period of activity in the data that is terminated by a gap of inactivity."
(p131)

**Data-driven window** [S]: "the location and sizes of the windows are a direct consequence of the input data themselves, rather than being based on some predefined pattern within time, as are fixed and sliding windows."
(p132)

**Custom windowing strategy (Beam)** [S]: "a custom windowing strategy consists of two things:"
(p136)

"Window assignment"

"(Optional) window merging"
(p136-137).

**Proto-session** [D]: the initial, single-record window each element is assigned before any merging occurs in a session-windowing strategy.

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter covers processing-time windowing implemented within an event-time-first model, a detailed session-windowing worked example with merging/retractions, and three real-world custom windowing strategies (unaligned fixed windows, per-element fixed windows, bounded sessions) built on Beam's window-assignment/window-merging primitives.

**WHY** [D]: to show both when processing-time windowing is legitimately appropriate versus actively harmful, and to demonstrate that custom windowing (a rarely-supported feature industry-wide) solves several real production use cases with only small code changes versus being impractical or impossible otherwise.

**WHEN** [S]: "For certain use cases, such as usage monitoring (e.g., web service traffic QPS), for which you want to analyze an incoming stream of data as it's observed, processing-time windowing is absolutely the appropriate approach to take. For use cases for which the time that events happened is important (e.g., analyzing user behavior trends, billing, scoring, etc.), processing-time windowing is absolutely the wrong approach to take."
(p124)

## 3. Assumptions and prerequisites

- Prerequisite: the early/on-time/late trigger and accumulation/retraction mechanics from chapter 2, directly reused for the session-windowing worked example (p134, reusing "the early/late code with retractions enabled from Example 2-10").
- Prerequisite: watermark mechanics from chapter 3, underlying why ingress-time processing-time windowing can achieve a perfect watermark (p129-130).
- Assumes Beam's custom-windowing API (`WindowFn`, `assignWindow`, `mergeWindows`) as the concrete vehicle, noting "Most systems today don't support custom windowing to the degree that it's supported in Beam" (p136) — Apache Flink is noted as the only other system with comparably deep custom-windowing support (footnote to p136).

## 4. Mechanism / key steps

1. Implement processing-time windowing via triggers: use a global event-time window, trigger periodically in processing time (`Repeatedly(AlignedDelay(ONE_MINUTE))`), and use discarding accumulation mode so each pane behaves as an independent processing-time "window" (p127-128, Example 4-1).

2. Implement processing-time windowing via ingress time: overwrite each element's event time with its arrival (ingress) time via a `DoFn` using `outputWithTimestamp`, then apply standard event-time fixed windowing — this affords a perfect watermark since event time now equals processing time by construction (p129-130, Example 4-2).

3. Confirm both processing-time windowing methods are order-sensitive by comparing outputs across two different observation orderings of the same underlying events: unlike event-time windowing (whose final results — 14, 18, 3, 12 — remain identical regardless of arrival order), both processing-time methods produce different results (12/18/18 vs. 7/36/5) depending on arrival order (p126-131, Figures 4-2 through 4-4).

4. Construct session windows incrementally and out-of-order-safely by assigning each incoming record its own proto-session window (spanning its event time plus the gap duration), then merging any overlapping proto-/session-windows together as new data arrives, emitting retractions for any previously-materialized sub-sessions absorbed into a larger merged session (p132-136, Figure 4-5 through 4-7, Example 4-3).

5. Define a custom windowing strategy in Beam via a `WindowFn` subclass implementing `assignWindow` (place each element into an initial window) and, optionally, `mergeWindows` (merge overlapping windows at grouping time) (p136-137).

6. Implement unaligned fixed windows by adding a per-key hash-based phase shift (`perKeyShift = hash(key) % size`) to the standard fixed-window assignment logic, keeping windows aligned within a key but staggered across keys, spreading window-completion load over time instead of bursting all keys' windows simultaneously (p138-140, Examples 4-5 through 4-7).

7. Implement per-element/per-key fixed windows by reading the desired window size from metadata carried on each element itself (`c.element().getWindowSize()`) rather than a single global window-size parameter, supporting arbitrary customer-specified aggregation granularity without forking the pipeline per size option (p141-142, Examples 4-8/4-9).

8. Implement bounded sessions by extending the standard session `WindowFn`'s merge logic to check whether a merge candidate's total span would exceed a configured `maxSize`, and if so, flushing the current merge group and starting a new one instead of continuing to merge (p143-146, Examples 4-10 through 4-12).

## 5. Trade-offs and limitations

- Processing-time windowing via triggers vs. via ingress time are "more or less equivalent" but differ in multistage pipelines: the triggers method slices windows independently per stage (data can shift between windows N-1/N/N+1 across stages), while the ingress-time method keeps a datum in the same window N throughout the pipeline via cross-stage watermark/microbatch synchronization (p125-126).
- "the big downside of processing-time windowing is"
(p125) that the contents of the windows change when the observation order of the inputs changes (p125) — event-time windowing is order-agnostic in the limit, processing-time windowing is not; using processing-time windowing when event time matters makes results "meaningless" (p131).
- Unaligned fixed windows trade cross-key window comparability for spread-out completion load: "the windows for elements with different keys will (typically) be unaligned, thus spreading window completion load out at the cost of also making comparisons across keys somewhat less meaningful."
(p139-140)
- Bounded sessions require custom logic since "given the variations in types of limits (some use cases care about total session size in event time, some care about total element count, some care about element density, etc.), it's difficult to provide a clean and concise API for bounded sessions."
(p144)
- Without native bounded-session support, the only recourse is post-hoc decomposition of already-grown sessions downstream, which "would obviate the benefits of incremental aggregation... increasing cost" and defeats spam-protection goals since "the sessions would first need to grow to their full sizes before being chopped or truncated."
(p146)

## 6. Failure modes and edge cases

- **Synchronized burst load from aligned fixed windows**: with standard fixed windows, "all of the active windows from noon to 1 PM become complete at around the same time, which means that once an hour the system is hit with a massive load of windows to materialize" — problematic as key cardinality N grows into the thousands or millions (p138-139).
- **Silent semantic drift under processing-time windowing**: because the contents of processing-time windows change when the observation order of the inputs changes (p125), a system relying on processing-time windowing for event-time-sensitive logic (billing, user-behavior analysis) can silently produce different, incorrect results purely due to arrival-order variance across otherwise-identical event sets (p131).
- **Unbounded session growth as a spam vector**: without a bounded-sessions mechanism, a single pathological input stream could grow a session indefinitely, both delaying materialization of results and providing no built-in defense against intentional abuse (p144).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: explicitly decide, per use case, whether as-observed (processing-time) or as-it-happened (event-time) semantics are required before choosing a windowing strategy — the two are not interchangeable for correctness-sensitive use cases (p124, p131).
- **Build** [D]: when a system provides custom-windowing support, prefer small, targeted `WindowFn` modifications (per-key phase shift, per-element size, bounded merge) over forking the pipeline per configuration option, since the source's own worked examples show this requires only a few changed lines (p138-146).
- **Maintain** [D]: if a pipeline exhibits periodic load spikes at fixed-window boundaries (e.g. hourly), consider unaligned fixed windows (per-key phase shift) to spread completion load evenly, trading away cross-key window comparability (p138-140).
- **RCA** [D]: if a downstream aggregate that should be order-independent produces different results across reprocessing runs, check whether the pipeline is (perhaps inadvertently) using processing-time windowing instead of event-time windowing, since that is the specific, diagnosable root cause the chapter identifies for this symptom (p126, p131).
- **Optimization** [D]: use bounded sessions to cap both worst-case materialization latency and worst-case per-session resource consumption, rather than allowing sessions to grow unbounded and truncating them after the fact (p144-146).

## 8. How to test/verify these claims

- Reproduce the order-sensitivity claim directly: run the same nine-record dataset under two different observation orderings (Figure 4-1) through event-time windowing (Example unchanged from ch.2) and confirm identical final results (14, 18, 3, 12), then run both processing-time methods (Examples 4-1, 4-2) and confirm the results differ by ordering (12/18/18 vs. 7/36/5) (p126-131).
- Verify unaligned fixed windows' load-spreading effect by running Example 4-7 across multiple keys with a maximal phase-shift configuration and confirming panes for different keys no longer materialize simultaneously, per Figure 4-9 (p140-141).
- Verify per-element fixed windows by tagging different elements with different window-size metadata (Example 4-9) and confirming each key's windows reflect its own configured size, per Figure 4-10 (p142).
- Verify bounded sessions by comparing the same input dataset's session-merging behavior under unbounded sessions (chapter 2's Example 2-7/Figure 2-7, spanning nearly five minutes) against bounded sessions with `maxSize=THREE_MINUTES` (Example 4-12), confirming the large session is split into two shorter ones (2:00 and 2:53) (p145-146, Figure 4-11).

## 9. Cross-references

- Chapter 2: early/on-time/late triggers and accumulation-and-retracting mode, directly reused for the session-windowing example (p134).
- Chapter 3: watermark mechanics underlying why ingress-time windowing achieves a perfect watermark (p129-130).
- Chapter 5 (exactly-once and side effects, authored by Reuven): named as the next chapter, closing out Part I (p147).
- Chapter 6 (streams and tables): named as the start of Part II (p147).
- Chapter 7: referenced regarding incremental aggregation cost, relevant to the bounded-sessions discussion (p146).
- Blog post describing manual session-building on Spark Streaming 1.x, cited as a contrast case showing the manual effort avoided by native session/custom-windowing support (p136).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 4-1 through 4-11 (time-lapse diagrams, windowing diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Java implementations of `FixedWindows`, `UnalignedFixedWindows`, `PerElementFixedWindows`, `Sessions`, and `BoundedSessions` (Examples 4-4, 4-6, 4-8, 4-10, 4-11) | The source itself states the point of showing this code "isn't so much to teach you how custom windowing functions are implemented... it's really to show the ease with which you can support new use [cases] via custom windowing" (p144); the key logic changes are captured in prose in §4 instead of reproducing full class bodies. |
