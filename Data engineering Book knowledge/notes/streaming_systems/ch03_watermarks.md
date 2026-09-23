# Ch.3 — Watermarks

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 85–123 (39 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Watermark (formal definition)** [S]: "The watermark is a monotonically increasing timestamp of the oldest work not yet completed."
(p88)

**Completeness property** [S]: "If the watermark has advanced past some timestamp T, we are guaranteed by its monotonic property that no more processing will occur for on-time (nonlate data) events at or before T. Therefore, we can correctly emit any aggregations at or before T."
(p88)

**Visibility property** [S]: "If a message is stuck in our pipeline for any reason, the watermark cannot advance. Furthermore, we will be able to find the source of the problem by examining the message that is preventing the watermark from advancing."
(p88)

**Input watermark / output watermark** [S]: "An input watermark, which captures the progress of everything upstream of that stage." "An output watermark, which captures the progress of the stage itself, and is essentially defined as the minimum of the stage's input watermark and the event times of all nonlate data active messages within the stage."
(p95)

**Percentile watermark** [S]: "Instead of considering the minimum point of the distribution, we could take any percentile of the distribution and say that we are guaranteed to have processed this percentage of all events with earlier timestamps."
(p106)

**Processing-time watermark** [S]: "We define the processing-time watermark in the exact same way as we have defined the event-time watermark, except instead of using the event-time timestamp of oldest work not yet completed, we use the processing-time timestamp of the oldest operation not yet completed."
(p109)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter defines watermarks rigorously from the underlying-mechanics perspective — their formal definition and two guarantee properties, how they're created at sources (perfect vs. heuristic), how they propagate across multi-stage pipelines via input/output watermark composition, how output-timestamp choice affects propagation, percentile and processing-time watermark variants, and real-system case studies (Cloud Dataflow, Flink, Cloud Pub/Sub).

**WHY** [S]: "We wish to solve the general problem of when it is safe to call an event-time window closed, meaning that the window does not expect any more data."
(p85)

**WHEN** [D]: use perfect watermark creation when the source has known structural bounds (ingress timestamping, a static set of monotonically-ordered log partitions); use heuristic watermark creation for arbitrary distributed/dynamic sources (dynamic log sets, Cloud Pub/Sub, mobile devices) accepting some late data; use percentile watermarks when "mostly correct" is acceptable and faster/smoother progress matters more than strict completeness; use processing-time watermarks (alongside event-time watermarks) specifically to distinguish a genuinely stuck system from normally buffered/delayed data.

## 3. Assumptions and prerequisites

- Prerequisite: watermarks as introduced conceptually in chapter 2 (perfect vs. heuristic, and the too-slow/too-fast trade-offs), which this chapter re-derives from first principles at the mechanics level (p85, p88-89).
- Assumes "each message has an associated logical event timestamp."
(p86) Described as reasonable "in the context of continuously arriving unbounded data because this implies the continuous generation of input data."
(p86)
- Assumes multi-stage pipeline structure (per-user then per-team aggregation, etc.) as the basis for discussing watermark propagation across stages (p94).

## 4. Mechanism / key steps

1. Reject naive completeness heuristics before arriving at the watermark definition: processing-time-based windowing fails because "processing and event times are almost never equal" (p85), and a raw message-processing rate metric fails because "rate does not tell us when we have seen all of the messages for a particular time interval" and can't catch a single stuck message (p86).

2. Derive the watermark from the distribution of in-flight vs. completed message event times: "the leftmost edge of the"
(p87) in-flight distribution defines the oldest unprocessed event time, which is the watermark value (p86-88, Figure 3-1).

3. Create a perfect watermark at a source with either (a) ingress timestamping — assigning the current processing time as the event time, giving perfect but event-time-meaningless tracking (p90-91), or (b) a static set of time-ordered log partitions — tracking the minimum event time of unprocessed data across all known partitions (p90-91).

4. Create a heuristic watermark at a source with structural knowledge such as growth rates and network topology for dynamic log sets (p92), or a purpose-built estimator for a source with no ordering guarantees, e.g. Cloud Pub/Sub (p92-93, detailed case study).

5. Propagate watermarks unchanged in kind through the pipeline: "perfect watermarks will remain perfect downstream, and heuristic watermarks will remain strictly as heuristic as they were when established."
(p93)

6. Compute a stage's input watermark as the minimum of the output watermarks of all upstream sources/stages, and its output watermark as the minimum of its input watermark and the event times of all its own active (buffered, in-state, in-flight) nonlate messages (p95) — track this per buffer type (per-source, per-external-input, per-state-component, per-output-buffer) for finer-grained visibility (p96-97).

7. Compute per-stage event-time lag by subtracting a stage's output watermark from its input watermark, giving the minimum delay that stage introduces (p95-96).

8. Choose an output timestamp for a materialized window — end of window (safest, smoothest watermark progression), timestamp of the first nonlate element (most conservative, but delays downstream watermark progress), or the timestamp of a specific chosen element (e.g. the query side of a query-click join) (p101-102).

9. Apply Beam's special-cased output-timestamp rule for overlapping (sliding) windows — ensuring window N+1's output timestamp always exceeds window N's end — to avoid unnecessarily delayed, batched emission of otherwise-independent overlapping windows (p105-106).

10. Compute a percentile watermark by tracking a chosen percentile of the active event-time distribution rather than its strict minimum, trading completeness precision for faster/smoother watermark advancement (p106-108, Figure 3-11).

11. Compute a processing-time watermark identically to the event-time watermark but over the processing-time timestamp of the oldest incomplete operation, enabling the pipeline to distinguish normally buffered data (event-time watermark delayed, processing-time watermark stable) from a genuinely stuck system (both delayed) (p108-112).

12. Implement Cloud Pub/Sub source watermarking via a dual-subscription scheme: a "base subscription" for actual message consumption and a "tracking subscription" (kept nearly backlog-free) used purely to estimate the event-time distribution of the base subscription's backlog, combined with a fixed "estimation band" (≥10 seconds) tolerance for source-side reordering (p118-121).

## 5. Trade-offs and limitations

- Perfect watermarks via ingress timestamping are easy but "the watermark has no correlation to the event times of the data themselves; those event times were effectively discarded" (p90-91).
- Choosing the earliest-element output timestamp keeps watermarks conservative but "watermark progress will likely be more hindered" — demonstrated directly by comparing Figures 3-5 and 3-6, where end-of-window timestamps propagate the downstream watermark noticeably faster (p101-104).
- Percentile watermarks trade completeness for latency: lower percentiles trigger earlier but "with the trade-off of marking more data as late" — in the book's worked example, moving from 100th to 33rd percentile shifts materialization from 12:08 to 12:06 processing time but includes only 4 of 10 events instead of all 10 (p107-108).
- Centralized watermark aggregation (Cloud Dataflow): "the watermark aggregator serves as a"
(p115).

This single source of truth about the watermark is useful for debugging/monitoring and for building watermarks that need global source information, but introduces a potential availability bottleneck; in-band watermark propagation (Flink) achieves lower latency, no single point of failure, and inherent scalability, but loses that centralized single-source-of-truth view (p116-118).
- The Cloud Pub/Sub dual-subscription heuristic "produces possibly an overly conservative watermark, one that advances"
(p121) too slowly, since it considers all messages ahead of the base subscription's oldest unacknowledged message, including some already-acknowledged ones (p121-122).

## 6. Failure modes and edge cases

- **Stuck message blocks the watermark indefinitely (by design)**: the visibility property means "if a message is stuck in our pipeline for any reason, the watermark cannot advance."
(p88) This is diagnostically useful but will halt downstream progress until resolved.
- **Sliding-window output-timestamp cascade delay**: using the earliest-element timestamp naively for overlapping windows causes windows to complete only in a delayed cascade (all three windows emitting "in one swoop" only after the last one completes), rather than each emitting as soon as it's individually ready — addressed by Beam's N+1-greater-than-end-of-N rule (p104-106).
- **Ambiguity between data delay and system delay**: relying solely on the event-time watermark, "we cannot distinguish between a system that is processing data from an hour ago quickly and without delay, and a system that is attempting to process real-time data and has been delayed for an hour while doing so" — resolved by also tracking the processing-time watermark (p108-109).
- **Sparse/infrequent Pub/Sub data stalling the watermark**: "In the case that we have not seen data on the subscription in more than two minutes (and there's no backlog), we advance the watermark to near real time" as an explicit fallback heuristic to keep the pipeline making progress (p121-122).
- **Premature watermark advancement from lease violations**: in Cloud Dataflow, a watermark update must be validated against the worker's persistent-state lease, since "advancing the watermark prematurely will turn on-time data into late data" if a non-owning worker's update were admitted (p115).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: choose perfect vs. heuristic watermark creation based on genuine structural knowledge of the source (static partitioned logs vs. arbitrary distributed input), not convenience — perfect watermarks eliminate late-data handling entirely but are only available for a narrow class of sources (p90-93).
- **Build** [D]: default output timestamps to end-of-window unless a specific use case (conservative watermarking, or a specific-element choice like query-vs-click) requires otherwise, since end-of-window gives "the smoothest watermark progression" (p101).
- **Maintain** [D]: expose per-buffer-type watermarks (per-source, per-external-input, per-state, per-output-buffer) in production monitoring, since this "provides better visibility into the behavior of the system" and directly supports diagnosing which specific component is stuck (p96-97).
- **RCA** [D]: when event-time watermark delay grows, check the processing-time watermark before escalating — a stable processing-time watermark with a growing event-time watermark indicates normal buffering (e.g. waiting for a window boundary), while both growing together indicates an actual stuck operation requiring intervention (p109-112).
- **Optimization** [D]: consider percentile watermarks when the business logic tolerates mostly-correct results, to get materially smoother/faster watermark progression by excluding long-tail outliers from the completeness calculation (p106-108).

## 8. How to test/verify these claims

- Reproduce the perfect-vs-heuristic watermark distinction by constructing both watermark types over the same input distribution (Figure 3-2, p89) and confirming the heuristic version admits late data while the perfect version does not.
- Verify input/output watermark composition by building the two-stage session-length example (Examples 3-1/3-2, p97-99) and confirming the second stage's input watermark equals the minimum of the two upstream stages' output watermarks (p99-100, Figure 3-5).
- Reproduce the output-timestamp propagation-speed difference by running the identical pipeline with end-of-window vs. earliest-element timestamps (Examples 3-2/3-3) and comparing downstream watermark advancement speed directly (p103-104, Figures 3-7/3-8).
- Reproduce the percentile-watermark latency/completeness trade-off numerically against the book's own worked example: confirm the 33rd/66th/100th percentile watermarks materialize the [12:00, 12:02) window with 4, 7, and 10 events respectively at processing times 12:06, 12:07, and 12:08 (p107-108).
- Verify the processing-time-vs-event-time watermark distinction by simulating both a genuinely stuck pipeline stage and a normally-buffering one, and confirming only the former shows a growing processing-time watermark (p109-112, Figures 3-12 through 3-15).

## 9. Cross-references

- [[ch02_what_where_when_how|Chapter 2]]: watermarks introduced conceptually (perfect/heuristic, too-slow/too-fast trade-offs), re-derived rigorously here (p85, p88-89, p121-122).
- [[ch05_exactly_once_and_side_effects|Chapter 5]] (exactly-once and side effects, authored by "Reuven"): referenced for further discussion of using the processing-time watermark for garbage collection of temporary state (p111-112).
- [[ch04_advanced_windowing|Chapter 4]] (advanced windowing): referenced as the next application of the watermark mechanics developed here (p122).
- [[ch06_streams_and_tables|Chapter 6]] (streams and tables): referenced regarding the effects of grouping on pipeline shapes (p94).
- Flink documentation, cited for further detail on Flink's in-band watermark implementation (p123).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 3-1 through 3-20 (distribution diagrams, time-lapse diagrams, system architecture diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Apache Beam Java pseudocode for Examples 3-1 through 3-3 | Representative code snippets and their behavioral consequences cited; the source itself notes this is simplified pseudocode, not production API (consistent with chapter 2's convention). |
| Full internal details of Google Cloud Dataflow's centralized watermark aggregator implementation | Representative mechanism (per-range watermark minimum, lease validation) captured; deeper implementation specifics are proprietary/beyond the source's own stated scope. |
