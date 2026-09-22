# Ch.5 — Exactly-Once and Side Effects

**Source:** `streaming_systems` (Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing, Akidau/Chernyak/Lax, O'Reilly)
**PDF page range:** 149–172 (24 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Accuracy vs. completeness** [D]: accuracy concerns whether the values a pipeline produces are correct (no duplication, no loss, no corruption); completeness concerns whether all the data that will ever arrive has arrived — the chapter is chiefly about accuracy under retries and failures, not about completeness (windowing/triggers territory from earlier chapters).

**Side effect** [S]: "any changes in state that occur as a result of executing a data processing pipeline, whether external, such as writing data to some third-party API, or internal, such as maintaining some form of custom index based on data observed."

(p150)

**Nonidempotent side effect** [D]: a side effect whose repeated execution with the same logical input produces a different or duplicated result than executing it once — the core hazard exactly-once guarantees must neutralize.

**Upstream backup** [S]: "buffer data at each stage until it is durably processed by the next downstream stage."

(p151)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter explains why exactly-once semantics matter for streaming pipelines, how Dataflow implements exactly-once processing across shuffle boundaries and at sources/sinks, and contrasts this approach with how Spark Streaming and Apache Flink achieve their own exactly-once guarantees.

**WHY** [S]: "Correctness in a data processing system is ultimately about reliability. Any failure to reliably produce correct data implies that either the results are inaccurate (missing, duplicated, or otherwise incorrect data) or, best case, unpredictably delayed."

(p149)

**WHEN** [D]: exactly-once processing matters whenever a pipeline's side effects (writes to external systems, aggregation state) must not be duplicated or lost on worker failure/retry — i.e., essentially any production streaming pipeline with real consequences for double-counted or missing records (billing, inventory, alerting).

## 3. Assumptions and prerequisites

- Prerequisite: familiarity with the Lambda Architecture critique from chapter 1, which this chapter reframes in terms of accuracy/consistency/complexity/unpredictability/latency costs (p149-150).
- Assumes a shuffle-based distributed execution model (Dataflow) as the primary running example, with Spark Streaming's microbatch/RDD model and Flink's distributed-snapshot model presented as contrasting architectures (p168-170).
- Assumes familiarity with checkpointing as a general fault-tolerance primitive, reused here to make otherwise-nondeterministic operations replay deterministically (p152-153, p160).

## 4. Mechanism / key steps

1. Detect and drop duplicate records introduced by retried RPCs during shuffle by attaching a unique ID to every record sent over a shuffle RPC and having the receiver check that ID against a catalog of already-processed IDs before accepting it, dropping the record if it is already present (p151-152, Figure 5-2).

2. Make the ID-catalog approach practical at scale by checkpointing the catalog of processed IDs so retries after a crash still see the correct dedup state, and by garbage-collecting old IDs once they can no longer recur (p152-153, p157-158).

3. Ensure retried computations are deterministic (a prerequisite for dedup-by-ID to work) by checkpointing the results of any nondeterministic step (e.g., a random number, a UUID) immediately after it runs, so retries replay the checkpointed value instead of recomputing a new nondeterministic result (p153).

4. Optimize the graph to reduce checkpoint overhead via fusion (chaining compatible operations together so intermediate results need not be checkpointed) and combiner lifting (partial aggregation before shuffle to reduce the volume of state that must be deduplicated) (p154).

5. Reduce the cost of duplicate-ID lookups using Bloom filters bucketed by processing-time windows (e.g., 10-minute buckets): a new record's ID is checked only against the Bloom filter(s) for buckets it could plausibly belong to, avoiding a full-catalog scan, at the cost of Bloom filters' false-positive rate (p154-157, Figure 5-5).

6. Garbage-collect the ID catalog using processing-time watermarks: once a processing-time watermark passes a given bucket, no further legitimate retries (network remnants) for that bucket's records can arrive, so its Bloom filter/catalog entries can be safely discarded (p157-158).

7. Handle exactly-once at sources by distinguishing deterministic sources (files, Kafka — replay yields the same record with the same identity) from nondeterministic sources (Cloud Pub/Sub — replay may yield different delivery attempts), and for the latter, requiring the source to expose a stable per-record ID via `UnboundedReader.getCurrentRecordId` so Dataflow can dedup at the source boundary (p158-160).

8. Handle exactly-once at sinks by isolating the nonidempotent step (e.g., generating a random shard/UUID/temp filename) behind a `Reshuffle`, so that retries downstream of the reshuffle always see the same shuffled value, then perform the actual external write/rename as an idempotent operation (file rename, BigQuery insert tagged with a stable ID) (p160-167, Examples 5-2 through 5-5).

9. Implement the `@RequiresStableInput` annotation to mark a `DoFn` as needing its input checkpointed before execution, guaranteeing that any retry of that `DoFn` sees byte-for-byte the same input rather than a potentially different upstream recomputation (p160-161).

## 5. Trade-offs and limitations

- Checkpointing every nondeterministic operation adds persistent-storage I/O overhead on the critical path; the source mitigates this via fusion and combiner lifting but does not eliminate it (p154).
- Bloom-filter-based dedup trades exactness for space/time efficiency: "In theory, we could dispense with startup scans entirely by lazily building the Bloom filter for a bucket only when a threshold number of records show up with timestamps in that bucket."

(p171, footnote) — implying the chosen bucketed-Bloom-filter design is itself a considered efficiency/complexity trade-off, not the only possible approach.

- Dataflow's exactly-once transport is more complex than Flink's specifically because Dataflow load-balances tasks dynamically across workers, whereas "tasks in Dataflow are constantly load balanced between workers (and the set of workers is constantly growing and shrinking), so Dataflow is unable to make this assumption. This forces Dataflow to implement a much more complex transport layer in order to provide exactly-once processing."

(p170)

- Flink's snapshot-based approach assumes failures are rare and snapshots complete quickly: "Failures are assumed to be rare,"

(p169) as a rollback is costly (reverting the whole pipeline to the last snapshot), and it "remains to be seen whether this causes issues on very large clusters where the failure rate will likely increase, as will the time needed to complete a snapshot" (p169).

- Spark Streaming's microbatch/RDD approach "can cause increased latency to output—especially for deep pipelines and high input volumes—and often careful tuning is required to achieve desired latency"

(p168), since each RDD batch introduces its own latency at every pipeline stage.

## 6. Failure modes and edge cases

- **Nonidempotent side effect executed twice**: without dedup, a retried task (after a crash or RPC failure) that performs a nonidempotent side effect (e.g., an external API call without a dedup key) will apply that effect more than once, corrupting downstream state (p150).
- **Nondeterministic retry producing a different result**: if a nondeterministic operation (random ID generation) is not checkpointed, a retry may generate a *different* random value than the original attempt, breaking the ID-based dedup mechanism that assumes retries reproduce identical records (p153).
- **Network remnants**: stale, delayed copies of previously-retried RPCs can arrive well after their originating attempt is considered complete; the ID catalog must be retained long enough (governed by the processing-time watermark) to still catch and drop these before garbage collection (p157-158).
- **BigQuery duplicate-ID collision if UUID generation is not reshuffled**: if the UUID used for BigQuery's streaming-insert dedup ID is regenerated on every retry (not stabilized via `Reshuffle`), retries produce different insert IDs, defeating BigQuery's own duplicate-filtering capability, causing duplicate rows (p166-167, Example 5-5).
- **Flink pipeline rollback losing "tentative" state**: "any state modifications not yet in a snapshot must be considered tentative" (p169) — a Flink worker failure between snapshots rolls the whole pipeline back to the last complete snapshot, discarding any tentative (unsnapshotted) progress.

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when integrating with an external sink that supports a dedup/idempotency key (BigQuery streaming insert IDs, idempotent file rename), design the pipeline so the ID/key is generated once and stabilized via a reshuffle/checkpoint before the actual write, per the source's own worked sink examples (p160-167).
- **Build** [D]: isolate nonidempotent operations (random ID generation, sharding decisions) as their own step immediately followed by a `Reshuffle` or checkpoint, so that everything downstream of that point is guaranteed deterministic under retry (p160, p166-167).
- **Maintain** [D]: if adopting a new external sink, verify it exposes some notion of a stable dedup key (as BigQuery does) before assuming exactly-once semantics can be achieved for that sink — the source explicitly builds its idempotent-sink pattern around this capability (p166-167).
- **RCA** [D]: if a downstream system exhibits occasional duplicate records or events despite an exactly-once pipeline design, check whether any step between the source and that duplication point performs a nonidempotent operation without checkpointing/reshuffling it first (p160-162).
- **Optimization** [D]: prefer fusion and combiner lifting to reduce the total volume of state requiring checkpointing/dedup rather than checkpointing every intermediate step uniformly, and prefer time-bucketed Bloom filters over full-catalog scans for duplicate-ID checks at scale (p154-157).

## 8. How to test/verify these claims

- Verify the shuffle-dedup mechanism by forcing an RPC retry (e.g., via fault injection) between two Dataflow stages and confirming the receiving stage's ID catalog correctly drops the duplicate, per the source's ID-catalog-and-Figure-5-2 mechanism (p151-152).
- Verify determinism-via-checkpointing by forcing a retry of a step that generates a random value (e.g., Example 5-1's random-number generation) and confirming the retried execution reuses the checkpointed value rather than generating a new one (p153).
- Verify the BigQuery sink's exactly-once behavior by forcing a retry after the `Reshuffle` in Example 5-5 and confirming the same UUID is reused for the retried insert, allowing BigQuery's dedup-by-ID to filter the duplicate (p166-167).
- Verify the file sink's exactly-once behavior by forcing a retry of `WriteTempFile` in Example 5-4 and confirming `Finalize`'s idempotent rename step sees the same `FileResult` bundle across retries, per the source's own reasoning: "After the `GroupByKey` completes, the `Finalize` step will always see the same bundles across retries. Because file rename is idempotent, this give us an exactly-once sink."

(p166)

- Cross-check the three systems' architectural trade-off claims (Dataflow/Spark/Flink) against their respective public documentation on checkpointing, RDD-based microbatching, and Chandy-Lamport-style distributed snapshots, since the source's comparison is a summary rather than an implementation-level proof (p168-170).

## 9. Cross-references

- Chapter 1: Lambda Architecture critique (Inaccuracy/Inconsistency/Complexity/Unpredictability), reframed here as the motivating case for exactly-once processing plus an added Latency dimension (p149-150).
- Chapter 2/3: watermark mechanics, reused here in processing-time form for ID-catalog garbage collection (p157-158).

The source's own footnote distinguishes this explicitly: "this is not the custom user-supplied timestamp used for windowing"

(p171, footnote).
- Chapter 6 (streams and tables): named as the start of Part II, following this chapter's close of Part I (source's chapter sequencing per `CHAPTER_MAP.csv`).
- Apache Beam's `SplittableDoFn` API, noted in the source's footnote as "a new, more-flexible API"

(p171, footnote) — flagged by the source itself as time-bound, being available only at the time of writing for use cases touched on in this chapter.

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 5-1 through 5-5 (shuffle/dedup/Bloom-filter diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Java pseudocode for Examples 5-1 through 5-5 (shuffle dedup, file sink, BigQuery sink) | Reproduced only as prose mechanism steps in §4; the source's own examples are illustrative pseudocode, not complete runnable implementations. |
| Detailed internals of Flink's Chandy-Lamport snapshot algorithm and Spark's RDD lineage/checkpoint internals | Presented at the level of detail the source itself gives (comparative summary); deeper treatment is out of scope for this chapter's own content. |
