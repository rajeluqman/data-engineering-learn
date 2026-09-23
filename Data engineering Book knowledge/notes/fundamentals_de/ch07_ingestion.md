# Ch.7 — Ingestion

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 258–295 (38 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 13,557
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Data ingestion vs. data integration [S]** (p259): "data ingestion is data movement from point A to B," while "data integration combines data from disparate sources into a new dataset" — the chapter's own worked example is combining CRM, ad-analytics, and web-analytics data into a user profile, then using reverse ETL to send it back to the CRM.

**Data pipeline, the chapter's formal definition [S]** (p260): "A data pipeline is the combination of architecture, systems, and processes that move data through the stages of the data engineering lifecycle" — explicitly called "deliberately fluid—and intentionally vague."

**Bounded vs. unbounded data [S]** (p261): "Unbounded data is data as it exists in reality, as events happen ... ongoing and flowing. Bounded data is a convenient way of bucketing data across some sort of boundary." Chapter's own mantra: "All data is unbounded until it's bounded" (p261).

**Batch vs. micro-batch vs. real-time ingestion frequency [S]** (p262): the chapter explicitly hedges the "real-time" label — "no ingestion system is genuinely real-time... It is more accurate to speak of near real-time, but we often use real-time for brevity."

**Synchronous vs. asynchronous ingestion [S]** (p263–264): synchronous — "the source, ingestion, and destination have complex dependencies and are tightly coupled," where "if process A fails, processes B and C cannot start"; asynchronous — "dependencies can now operate at the level of individual events," with each pipeline stage processing items "as they become available in parallel."

**Payload characteristics: kind, shape, size, schema, metadata [S]** (p266–269): "kind consists of type and format"; "shape... describes its dimensions" (worked examples given per data type: tabular rows×columns, JSON key-value/nesting depth, unstructured text word/char/byte counts, image width/height/RGB depth, audio channels/sample depth/rate/length); size is "the number of bytes of a payload," reducible via compression or chunking.

**Schema registry [S]** (p268): "a metadata repository used to maintain schema and data type integrity in the face of constantly changing schemas," tracking "schema versions and history."

**Push vs. pull vs. poll [S]** (p269): push — "a source system sending data to a target"; pull — "a target reading data directly from a source"; poll — "periodically checking a data source for any changes," then pulling when changes are detected.

**Snapshot vs. differential (incremental) extraction [S]** (p271): full snapshots grab "the entire current state of the source system on each update read"; differential updates "pull only the updates and changes since the last read" — the chapter notes "full snapshot reads remain extremely common because of their simplicity" despite differential being more efficient.

**Dead-letter queue [S]** (p274–275): "segregates problematic events from events that can be accepted by the consumer" — used to diagnose ingestion errors and reprocess events "after fixing the underlying cause."

**Time to live (TTL) [S]** (p274): "maximum message retention time" — configurable per platform; the chapter's own worked comparison: "Google Cloud Pub/Sub supports retention periods of up to 7 days. Amazon Kinesis Data Streams retention can be turned up to 365 days. Kafka can be configured for indefinite retention, limited by available disk space."

**CDC — batch-oriented vs. continuous [S]** (p277–278): batch-oriented CDC queries an `updated_at` field to find rows changed since a timestamp, but "we don't necessarily obtain all changes that were applied to these rows" (the chapter's own worked bank-account example: 5 debit-card withdrawals in 24 hours yield only the last recorded balance). Continuous CDC "treats each write to the database as an event," typically via log-based CDC reading "the database binary log."

**Bastion host [S]** (p284): "Application databases should never be directly exposed on the internet. Instead, engineers can set up a bastion host—i.e., an intermediate host instance that can connect to the database in question." Reachable only via SSH tunnel, per the chapter's own mechanism description. `[D]` gloss on the tunnel-access detail.

**Webhook, "reverse API" [S]** (p284–285): "the data provider defines an API request specification, but the data provider makes API calls rather than receiving them; it's the data consumer's responsibility to provide an API endpoint for the provider to call."

**Transfer appliance [S]** (p286): a physical device for moving very large data volumes ("100 TB or more") — named examples: AWS Snowball, and the extreme case, "AWS even offers Snowmobile, a transfer appliance sent to you in a semitrailer!"

## 2. WHAT / WHY / WHEN

**WHAT:** The chapter covers the ingestion phase of the lifecycle: the eight key engineering considerations (bounded/unbounded, frequency, sync/async, serialization, throughput/scalability, reliability/durability, payload, push/pull/poll), the major batch and streaming ingestion patterns, a survey of concrete ingestion methods (JDBC/ODBC, CDC, APIs, message queues, object storage, EDI, shell/SSH/SFTP, webhooks, web scraping, transfer appliances, data sharing), stakeholder relationships, and the undercurrents applied to ingestion. `[D]`

**WHY it matters:** framed directly in the Conclusion: "ingestion will likely consume a significant part of your energy and effort. At the heart, ingestion is plumbing... ensuring that data flows consistently and securely to its destination" (p294), while the exciting downstream applications "cannot happen without it." `[S]`

**WHEN to use managed data connectors over custom-built ones (the chapter's own explicit recommendation, p282):** "We suggest using managed connector platforms instead of creating and managing your connectors" and "The creation and management of data connectors is largely undifferentiated heavy lifting these days and should be outsourced whenever possible." Custom connection work should be reserved "for APIs that aren't well supported by existing frameworks" (p280).

**WHEN to reach for a transfer appliance vs. network transfer (p286):** the chapter's own threshold — "consider using a transfer appliance if your data size hovers around 100 TB" — with a hard caveat that appliances are for one-time migration events, not "ongoing workloads" (p287).

## 3. Assumptions and prerequisites

- Assumes bounded/unbounded vocabulary from Ch.3: "As you might recall from Chapter 3, data comes in two forms: bounded and unbounded" (p261). `[S]`
- Assumes CDC, message/stream, and event-streaming-platform concepts from Ch.5/Ch.6: "This section covers issues you should consider when ingesting events, drawing on topics covered in Chapters 5 and 6" (p273). `[S]`
- Assumes push/pull framing already introduced in Ch.2: "We mentioned push versus pull when we introduced the data engineering lifecycle in Chapter 2" (p269). `[S]`
- Explicitly defers ETL/ELT depth and data-integration/reverse-ETL depth to later chapters: "We cover ETL and ELT in greater detail in Chapter 8" (p271); "data integration more fully in Chapter 8... reverse ETL is covered in Chapter 9" (p259). `[S]`

## 4. Mechanism / key steps

**Log-based continuous CDC (p278):** database write → binary log records the change sequentially → a CDC tool (e.g. Debezium) reads the log → events are forwarded to a target platform (the chapter's example: Kafka via Debezium) — contrasted with batch-oriented CDC's periodic `updated_at`-filtered query approach (§1). `[D]` (this note's own step-sequencing of the chapter's mechanism, not a verbatim quote.)

**Asynchronous event-pipeline example, AWS (p264):** web application emits events into Kinesis Data Streams (acting as a buffer) → Apache Beam reads the stream, parses/enriches events → forwards to a second Kinesis stream → Kinesis Data Firehose rolls up events and writes objects to S3. The chapter's own framing: the first Kinesis stream "acts as the shock absorber, moderating the load so that event rate spikes will not overwhelm downstream processing."

**JDBC-based ingestion pattern, the chapter's own recommended composition (p277):** a reader process connects to a source database via JDBC → extracted data is written into multiple objects (e.g. Parquet/ORC/Avro files) → orchestration triggers ingestion of those objects into the downstream target system via an API call. `[D]` (this note's own step-sequencing of the chapter's mechanism, not a verbatim quote.)

## 5. Trade-offs and limitations

- **Synchronous ingestion's failure-cascade cost, a named real incident (p263–264):** "At one company, the transformation process itself was a series of dozens of tightly coupled synchronous workflows, with the entire process taking over 24 hours to finish. If any step of that transformation pipeline failed, the whole transformation process had to be restarted from the beginning!" — diagnosis took "over a week."
- **Batch-oriented CDC's information loss, worked example (p277–278):** "when we run a query to return all rows in the account table that changed in the last 24 hours, we'll see records for each account that recorded a transaction... Our query will return only the last account balance recorded" — intermediate transactions are silently lost unless an insert-only schema is used.
- **JDBC/ODBC's structural limitation for modern data shapes (p276):** "These connection standards struggle with nested data, and they send data as rows" — and (p277) "columns from columnar databases must be reserialized as rows."
- **CSV's named error-proneness (p283):** "CSV is still ubiquitous and highly error prone... Engineers must stipulate the delimiter, quote characters, and escaping... CSV also doesn't natively encode schema information or directly support nested structures."
- **Webhook architecture's fragility, stated directly (p285):** "Webhook-based data ingestion architectures can be brittle, difficult to maintain, and inefficient" — mitigated only by "appropriate off-the-shelf tools."
- **Web scraping's legal/operational risk, stated directly (p286):** "Don't inadvertently create a denial-of-service (DoS) attack, and don't get your IP address blocked" and "generating DoS attacks can entail legal consequences"

## 6. Failure modes and edge cases

- **Message size limits as a silent ingestion failure point (p274):** "Amazon Kinesis supports a maximum message size of 1 MB. Kafka defaults to this maximum size but can be configured for a maximum of 20 MB or more" — events exceeding these limits require explicit handling (e.g. routing to a dead-letter queue, §1).
- **Late-arriving data corrupting time-based analysis (p273):** "Suppose you assume that ingestion or process time is the same as the event time. You may get some strange results if your reports or analysis depend on an accurate portrayal of when events occur" — the chapter's fix is an explicit cutoff time for late data.
- **Silent, prolonged pipeline failure, a named real incident (p291):** "an ingestion pipeline failure wasn't detected for six months" — the chapter's own example of the cost of weak or nonexistent monitoring at the ingestion stage.
- **The "not provided" search-term regression, a named public incident (p292):** Google's 2011 withholding of search-term referrer data is cited as an example of an immediately visible, non-silent data regression — contrasted with the more dangerous silent regressions that "may go unnoticed."
- **CDC resource contention on production systems (p279):** "CDC consumes various database resources, such as memory, disk bandwidth, storage, CPU time, and network bandwidth. Engineers should work with production teams and run tests before turning on CDC on production systems to avoid operational problems."

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the eight engineering-consideration checklist (§1/§2) is a directly reusable pre-build architecture review checklist for any new ingestion pipeline in this vault's projects. `[D]`
- **Build:** the "reserve custom connector work for unsupported APIs" rule (§2) is a concrete build-vs-buy gate specific to ingestion tooling, extending Ch.4's general build-vs-buy framework to this lifecycle stage. `[D]`
- **Maintain:** the schema-change communication discipline (p289–290, "Schema changes") is a concrete maintenance practice — the chapter explicitly proposes a Git-branching-inspired model for schema evolution ("each developer could maintain their processed branch of the code and then merge to or from other branches") as an alternative to either rigid command-and-control review or blind auto-recreation of target tables. `[S]`
- **RCA:** the DataOps monitoring checklist (p291, "What should you monitor? Uptime, latency, and data volumes processed") is a direct incident-investigation starting point for any ingestion-pipeline outage postmortem.
- **Optimization:** the batch-size/insert-pattern warning (p272, "Inserts, Updates, and Batch Size") — many small-batch inserts/updates are named as an anti-pattern for columnar databases specifically — is a directly checkable performance-review item before assuming a slow load is a capacity problem rather than an access-pattern problem.

## 8. How to test / verify these claims

- The batch-oriented-CDC information-loss claim (§5) is directly testable: run periodic `updated_at`-filtered queries against a table receiving multiple writes per interval, and confirm intermediate states are missing — a mechanically reproducible test, not just a hypothetical.
- The message-size-limit claims (§6, Kinesis 1MB / Kafka default) are directly checkable against current AWS/Kafka documentation, and are `[S]` as reported in 2022 but `[U]` as to whether defaults have since changed.
- The dead-letter-queue mechanism (§1) is testable by deliberately sending an oversized or malformed event through a configured pipeline and confirming it's rerouted rather than blocking the queue.
- The TTL retention-period figures (§1: Pub/Sub 7 days, Kinesis up to 365 days, Kafka indefinite/disk-bound) are checkable against each vendor's current documentation — vendor limits are subject to change.

## 9. Cross-references

- Directly extends `fundamentals_de` [[ch03_designing_good_data_architecture|Ch.3]] (bounded/unbounded, ETL/ELT), [[ch05_data_generation_source_systems|Ch.5]] (CDC, message/stream distinction, APIs, webhooks), [[ch06_storage|Ch.6]] (object storage, data sharing) — all previously synthesized in this vault, no contradiction found.
- Forward-references [[ch08_queries_modeling_transformation|Ch.8]] (data integration and ETL/ELT depth, p259/p271) and [[ch09_serving_data|Ch.9]] (reverse ETL, p259) — neither yet synthesized. Flagged for `check_deferred_refs.py`.
- The webhook definition here ("reverse API") is consistent with, and directly cross-references, the webhook material already summarized in the [[ch05_data_generation_source_systems|Ch.5]] note's WHEN-to-use-NoSQL and API sections — no contradiction. `[D]`
- The CDC-and-replication material here (p280–281) extends the write-ahead-log CDC mechanism already synthesized in [[ch05_data_generation_source_systems|Ch.5]] §4 — this chapter adds the batch-vs-continuous CDC distinction and the bank-account worked failure case that [[ch05_data_generation_source_systems|Ch.5]] did not cover; complementary, not duplicative. `[D]`

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 7-1 through 7-15 (ingestion overview, bounded/unbounded, batch/streaming frequency spectrum, sync/async pipeline diagrams, time-interval and size-based batch diagrams, push/pull/poll diagrams, dead-letter-queue diagram, JDBC ingestion architecture, webhook architecture) | Captions and content described narratively above where load-bearing (§1, §4); diagrams not rendered to image for this chapter, consistent with the project-wide `reading_order_risk` finding. |
| Detailed sub-listings of "Ways to Ingest Data" methods not already covered above (Shell, SSH, SFTP/SCP, Web Interface mechanics, EDI mechanics) | Covered at summary/definitional level in §1 where load-bearing (bastion host); full operational detail per method not reproduced, as these are largely procedural/tooling descriptions rather than falsifiable technical claims requiring citation-level synthesis. |
| "Additional Resources" list (p295, 5 external links) | Bibliography, not chapter content — not synthesized. |
| Footnoted external sources (Karl Hughes's "plumbing" quote source, Andy Petrella's "Datastrophes" article, Danny Sullivan's "not provided" MarTech article) | Quoted or referenced where load-bearing (§6); source documents not independently retrieved beyond what this chapter quotes. |
| Full "Whom You'll Work With" subsections (Upstream/Downstream Stakeholders, p262–263/p285–286) | Organizational-role content, summarized at a high level via §2/§7 rather than reproduced in full — largely restates the general upstream/downstream stakeholder framing already established in earlier chapters, applied specifically to ingestion. |
