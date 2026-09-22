# Ch.1 — Streaming 101

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 22–47 (26 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Streaming system (precise definition)** [S]: "A type of data processing engine that is designed with infinite datasets in mind."
(p24)

**Bounded / unbounded data** [S]: "A type of dataset that is finite in size."

"A type of dataset that is infinite in size (at least theoretically)."
(p24)

**Table / stream (constitution)** [S]: "A holistic view of a dataset at a specific point in time."

"An element-by-element view of the evolution of a dataset over time."
(p24-25)

**Event time vs. processing time** [S]: "This is the time at which events actually occurred."

"This is the time at which events are observed in the system."
(p29)

**Windowing** [S]: "Windowing is simply the notion of taking a data source (either unbounded or bounded), and chopping it up along temporal boundaries into finite chunks for processing."
(p39)

**Aligned vs. unaligned windows** [D]: aligned windows apply the same window boundaries across an entire dataset; unaligned windows vary per subset of data (e.g. per key), as with sessions.

**Lambda Architecture** [S]: "the basic idea is that you run a streaming system alongside a batch system, both performing essentially the same calculation. The streaming system gives you low-latency, inaccurate results... and some time later a batch system rolls along and provides you with correct output."
(p25)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter establishes precise terminology for streaming/unbounded data processing (streaming system, bounded/unbounded, table/stream), argues that well-designed streaming systems are a strict superset of batch capability given correctness and time-reasoning tools, introduces the event-time/processing-time distinction and skew, and surveys the major data-processing patterns (time-agnostic, approximation, processing-time windowing, event-time windowing).

**WHY** [S]: "Businesses crave ever-more timely insights into their data, and switching to streaming is a good way to achieve lower latency... The massive, unbounded datasets that are increasingly common in modern business are more easily tamed using a system designed for such never-ending volumes of data."
(p22)

**WHEN** [D]: use time-agnostic processing (filtering, inner joins) when logic is purely data-driven with no temporal semantics (§ time-agnostic processing); use processing-time windowing for monitoring/rate use cases where you want to characterize the pipeline's observed behavior rather than reconstruct real-world event timing (p41); use event-time windowing whenever correctness with respect to when events actually happened matters, accepting its buffering and completeness costs (p42-45).

## 3. Assumptions and prerequisites

- Assumes the reader has encountered the informal, overloaded use of "streaming" in industry and is willing to adopt the book's narrower, precise definition instead (p22-23).
- Assumes basic familiarity with MapReduce-style batch processing and Lambda Architecture as historical context, both of which the chapter explicitly contrasts against (p25-26).
- Assumes strong consistency (exactly-once/effectively-once semantics) is achievable and is treated as a baseline requirement, not an aspiration: "To reiterate—because this point is important: strong consistency is"
(p27) — the source continues on p28: "required for exactly-once processing, which is required for correctness, which is a requirement for any system that's going to have a chance at meeting or exceeding the capabilities of batch systems." [D] (paraphrase of the continuation, not quoted verbatim due to a page break).

## 4. Mechanism / key steps

1. Classify a dataset along two orthogonal dimensions before choosing a processing strategy: cardinality (bounded vs. unbounded) and constitution (table vs. stream) (p24-25).

2. Process bounded data with a straightforward run of a batch (or streaming) engine over the finite dataset (p33, Figure 1-2).

3. Process unbounded data with a batch engine by slicing it into fixed windows first (e.g. via directory/file naming conventions encoding the window), accepting that a completeness problem remains (late/delayed events) requiring mitigation such as delayed processing or reprocessing on late data (p33-34).

4. Recognize that session-based windowing breaks down further under batch processing, since sessions get split across batch boundaries unless batch size is increased (raising latency) or extra stitching logic is added (raising complexity) (p35).

5. Classify unbounded streaming-processing approaches into four categories: time-agnostic (filtering, inner joins), approximation algorithms (approximate Top-N, streaming k-means), processing-time windowing, and event-time windowing (p35-36).

6. Implement time-agnostic filtering by evaluating each record independently against a predicate as it arrives, with no dependency on ordering or skew (p36-37, Figure 1-5).

7. Implement a time-agnostic inner join by buffering an element from one source in persistent state until a matching element from the other source arrives, only then emitting the joined record (p37-38, Figure 1-6) — note that outer joins reintroduce a temporal element via a required timeout policy (p38).

8. Choose among windowing strategies: fixed/tumbling windows (fixed-size, typically aligned), sliding/hopping windows (fixed length + fixed period, generalizing fixed windows), and sessions (dynamic, unaligned, terminated by an inactivity gap) (p39-41, Figure 1-8).

9. Implement processing-time windowing by buffering incoming data for a fixed processing-time duration (e.g. 5 minutes) and emitting everything observed in that interval as one window, with perfect and trivial completeness knowledge since the system itself defines window boundaries (p40-42).

10. Implement event-time windowing by grouping data according to the event times they carry, regardless of arrival order, requiring a "temporal shuffle" and a mechanism (e.g. watermarks, covered in later chapters) to estimate window completeness (p44-46, Figures 1-10 and 1-11).

## 5. Trade-offs and limitations

- The Lambda Architecture "gave you a way to have your proverbial cake and eat it too," but "maintaining a Lambda system is a hassle: you need to build, provision, and maintain two independent versions of your pipeline and then also somehow merge the results from the two pipelines at the end."
(p26)
- Approximation algorithms are "low overhead and designed for unbounded data," but "a limited set of them exist, the algorithms themselves are often complicated... and their approximate nature limits their utility"; their error bounds often assume in-order arrival, which breaks under unordered event-time-skewed data (p38).
- Processing-time windowing is simple with trivial completeness judgment, but "if the data in question have event times associated with them, those data must arrive in event-time order if the processing-time windows are to reflect the reality of when those events actually happened" — a condition rarely met by real distributed sources (p41-42).
- Event-time windowing gives correct, skew-robust results but requires windows to "often live longer (in processing time) than the actual length of the window itself"
(p44), incurring more buffering, and it faces an unsolvable completeness problem: "we often have no good way of knowing when we've seen all of the data for a given window."
(p44)

## 6. Failure modes and edge cases

- **Mobile/offline data arriving with large event-time skew**: "data might arrive with an event-time skew of minutes, hours, days, weeks, or more. It's essentially impossible to draw any sort of useful inferences from such a dataset when windowed by processing time."
(p42)
- **Silent skew increase from network degradation**: a globally healthy-looking pipeline can suddenly exhibit much greater event-time skew if a transcontinental network link degrades, silently invalidating processing-time-windowed results without any explicit failure signal (p42).
- **Sessions split across batch boundaries**: naive batch-based session computation produces artificially split sessions at batch edges unless mitigated by larger batches (higher latency) or extra stitching logic (higher complexity) (p35, Figure 1-4).
- **Unresolvable outer-join completeness**: "after you've seen one side of the join, how do you know whether the other side is ever going to arrive or not?"
(p37) Forces a timeout-based (inherently time-dependent) resolution.

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: pick windowing strategy based on what correctness question the pipeline must answer — monitoring/rate questions about data as observed fit processing-time windows; questions about what actually happened, when, require event-time windows (p41-42).
- **Build** [D]: treat strong consistency (checkpointed, failure-tolerant persistent state) as a non-negotiable baseline for any streaming system meant to replace or supersede batch, not an optional enhancement (p27-28).
- **Maintain** [D]: watch for silent event-time skew growth in production pipelines (e.g. from transcontinental network degradation) since it can invalidate processing-time-windowed results without triggering any explicit error (p42).
- **RCA** [D]: if event-time-sensitive results look wrong intermittently, check whether the pipeline uses processing-time windowing on out-of-order data before assuming a logic bug — the described skew-vs-lag mismatch is a well-known root cause class (p41-42).
- **Optimization** [D]: for aggregations that don't require the full input set buffered (e.g. sum, average), compute incrementally with a small intermediate aggregate in persistent state rather than buffering the entire window's raw data, mitigating event-time windowing's buffering cost (p44).

## 8. How to test/verify these claims

- Reproduce the processing-time-vs-event-time skew diagram's core claim (Figure 1-1, p29-30) by plotting real pipeline event-time completeness against wall-clock processing time and confirming the two diverge under realistic network/system conditions.
- Verify the time-agnostic filtering/join claims by implementing both against unordered, variably-skewed synthetic data and confirming correctness is unaffected by ordering (p36-38).
- Verify the processing-time-window correctness failure by feeding out-of-order event-time data into a processing-time-windowed pipeline and confirming windows misclassify late-arriving events, versus an event-time-windowed pipeline correctly reassigning them (p44-45, Figure 1-10).

## 9. Cross-references

- Chapter 3 (watermarks) and Chapter 4 (advanced windowing): referenced for the mechanisms estimating event-time window completeness (p45).
- Chapter 5 (exactly-once and side effects): referenced for a deeper treatment of consistency guarantees and the exactly-once/effectively-once terminology (p28, p47).
- Chapter 6, 8, 9 (streams and tables, streaming SQL, streaming joins): referenced for the deeper table/stream constitution relationship only briefly introduced here (p25, p46).
- Blog posts "Streaming 101"/"Streaming 102" (Tyler Akidau) and Jay Kreps's "Questioning the Lambda Architecture" / "Why local state is a fundamental primitive in stream processing," cited as direct sources this chapter is based on (p22, p26, p27).
- MillWheel, Spark Streaming, and Flink snapshotting papers, cited for further detail on strong-consistency mechanisms (p28).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 1-1 through 1-11 (time-domain plots, windowing diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Footnote-level asides (microbatch definition, exactly-once terminology nuance, axis-choice rationale in Figure 1-1) | Secondary clarifications captured at the level needed for the chapter's main argument; full footnote text not reproduced verbatim. |
