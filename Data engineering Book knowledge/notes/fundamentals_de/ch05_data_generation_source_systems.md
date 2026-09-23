# Ch.5 — Data Generation in Source Systems

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 180–213 (34 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 12,064
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**OLTP vs. OLAP [S]** (p182, p184): OLTP ("online transaction processing") systems "read and write individual data records at a high rate" with "low latency and high concurrency"; OLAP ("online analytical processing") systems are "built to run large analytics queries" and are "typically inefficient at handling lookups of individual records" — any query "typically involves scanning a minimal data block, often 100 MB or more in size."

**ACID [S]** (p183): atomicity, consistency, isolation, durability. Consistency: "any database read will return the last written version of the retrieved item." Isolation: concurrent updates leave "the end database state ... consistent with the sequential execution of these updates in the order they were submitted." Durability: "committed data will never be lost, even in the event of power loss."

**Change Data Capture (CDC) [S]** (p184): "a method for extracting each change event (insert, update, delete) that occurs in a database," used "to replicate between databases in near real time or create an event stream for downstream processing."

**CRUD vs. insert-only [S]** (p187–188): CRUD ("create, read, update, and delete") updates records in place; the insert-only pattern instead "retains history directly in a table" by inserting "new records ... with a timestamp indicating when they were created" rather than updating — reading the current value means "you would look up the latest record under that ID."

**Message vs. stream, the chapter's central distinction [S]** (p188–189, p192): "A message is raw data communicated across two or more systems" and, once delivered, "is removed from the queue"; "a stream is an append-only log of event records" persisted "over a long retention window — often weeks or months — allowing for complex operations."

**Three types of time [S]** (p189–190): event time ("when an event is generated in a source system"), ingestion time ("when an event is ingested from source systems into a message queue, cache, memory, object storage, a database"), and process time ("how long the data took to process").

**Data contract [S]** (p207, quoting James Denmore): "a written agreement between the owner of a source system and the team ingesting data from that system" — "the contract should state what data is being extracted, via what method (full, incremental), how often, as well as who ... are the contacts for both the source system and the ingestion".

**Hotspotting [S]** (p206): "a disproportionate number of messages delivered to one partition" — the chapter's own worked example is using US state as a stream partition key, where population-heavy states (California, Texas, Florida, New York) would overwhelm their partitions.

## 2. WHAT / WHY / WHEN

**WHAT:** The first deep-dive chapter of Part II, covering how data is generated in source systems — file/API/database patterns, NoSQL database types, API paradigms (REST/GraphQL/webhooks/gRPC), message queues and event-streaming platforms, stakeholder relationships, and the undercurrents as they apply specifically to source systems. `[D]`

**WHY it matters:** the chapter's opening framing is explicit about scope-shrinkage over time: "The basic plumbing tasks of data engineering — moving data from A to B — will simplify dramatically" while "it will remain critical to understand the nature of data as it's created in source systems" (p181) — i.e. the chapter argues the durable skill here is understanding source semantics, not building connectors. `[S]`

**WHEN to use which NoSQL type (the chapter's own explicit guidance, collected):**
- Key-value: "in-memory key-value databases are popular for caching session data ... where ultra-fast lookup and high concurrency are required" (p194).
- Document stores: when data is naturally nested/JSON-shaped and joins aren't required; explicit caution that "the same data must be stored in multiple documents spread across numerous collections" if related data can't fit in one document (p195).
- Wide-column: "petabytes of data, millions of requests per second, and sub-10ms latency" workloads — "popular in ecommerce, fintech, ad tech, IoT, and real-time personalization" (p196–197).
- Graph: "indicated when we care about understanding complex traversals between elements" (p197), with the chapter's own worked example (multi-hop follower networks) showing why a document store becomes impractical for that query shape.
- Time-series: high-velocity, timestamp-ordered data (IoT, logs, ad tech, fintech), explicitly "not great for BI use cases" (p199) because joins are uncommon.

## 3. Assumptions and prerequisites

- Assumes ACID vocabulary is carried forward from Ch.3: "as you may recall from Chapter 3" (p183). `[S]`
- Assumes REST terminology from Ch.4: "As noted in Chapter 4, REST stands for representational state transfer" (p199). `[S]`
- The chapter explicitly scopes its own shelf life: "Source System Practical Details ... will have a shorter shelf life than the main ideas discussed previously; popular API frameworks, databases, and other details will continue to change rapidly" (p190–191) — the book itself flags the database/API-specific material as more likely to date than the conceptual framing (OLTP/OLAP, CDC, message-vs-stream). `[S]`

## 4. Mechanism / key steps

**CDC via database write-ahead logs (p185–186):** the database server "receives write and update requests to a database table, storing each operation in the log before acknowledging the request" — the acknowledgment carries "a log-associated guarantee: even if the server fails, it can recover its state on reboot by completing the unfinished work from the logs." This same log is what CDC tooling reads to generate an event stream.

**Stream partitioning by key (p205–206):** messages are assigned to partitions by a partition key (the chapter's own example: numeric ID modulo 3 → 3 partitions); "messages with the same partition key will always end up in the same partition" — enabling ordered, co-located processing (e.g. routing all messages from one IoT device to the same consumer) while risking hotspotting if the key distribution is skewed.

**Message delivery semantics (p203–204):** exactly-once ("after the subscriber acknowledges the message, the message disappears and won't be delivered again") vs. at-least-once (may be "consumed by multiple subscribers or by the same subscriber more than once"). The chapter's own resolution: design for idempotency so "the outcome of processing a message once is identical to the outcome of processing it multiple times," since even exactly-once systems can double-process if a consumer crashes after processing but before acknowledging.

## 5. Trade-offs and limitations

- **Insert-only's two named costs (p188):** tables "can grow quite large" since every change is a new row, and current-state lookups become expensive because they require "running MAX(created_timestamp)" — explicitly called out as costly "if hundreds or thousands of records are under a single ID."
- **Document stores' consistency trade-off, stated directly (p195–196):** "document stores are generally not ACID compliant, unlike relational databases" and "many document stores are eventually consistent" — flexibility in schema is explicitly framed as "a blessing and a curse," since ungoverned schema evolution can make databases "become absolute nightmares to manage and query."
- **Wide-column databases' query limitation (p196–197):** "they do not support complex queries. They have only a single index (the row key) for lookups" — forcing a secondary analytics system for anything beyond that access pattern.
- **REST's incompleteness as a spec, with a cited critique (p200):** "REST is in no way a full specification... developers utilizing an API must gain a significant amount of domain knowledge to build applications" — footnoted to an external critique ("RESTful APIs: The Big Lie").
- **Message-queue ordering is not guaranteed by default (p204):** "don't assume that your messages will be delivered in order unless your message queue technology guarantees it" — named explicitly as something engineers must design around, not assume away.

## 6. Failure modes and edge cases

- **OLTP-for-analytics anti-pattern (p183–184):** "small companies run analytics directly on an OLTP. This pattern works in the short term but is ultimately not scalable" — degradation comes from "structural limitations of OLTP or resource contention with competing transactional workloads."
- **Full-scan cost on document/wide-column stores (p196–197):** "engineers generally must run a full scan to extract all data from a collection" for analytics; the chapter names both the performance cost ("the scan often slows the database as it runs") and a direct cost consequence: "many serverless cloud offerings charge a significant fee for each full scan."
- **Double-processing despite exactly-once guarantees (p204):** "a consumer might fully process a message but fail right before acknowledging processing" — the message gets redelivered and reprocessed even under an exactly-once contract, which is why the book insists on idempotency regardless of the delivery guarantee chosen.
- **Hotspotting from a naive partition key (§1)** — the state-population example is the chapter's own worked failure case for partition-key design.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the message-vs-stream distinction (§1) is a direct architecture decision point — if downstream consumers need historical replay or aggregation over many events, a stream/event-log technology is required; a message queue alone (which removes messages after delivery) cannot serve that need. `[D]`
- **Build:** the three-times-timestamping discipline (event/ingestion/process time, §1) is a concrete instrumentation requirement for any pipeline being built in this vault's projects — the chapter is explicit: "Always include timestamps for each phase through which an event travels" (p190). `[S]`
- **Maintain:** the data-contract and SLA/SLO framing (p207–208) gives a concrete artifact to request from upstream teams before depending on a source system in production — not just a nice-to-have, per the chapter's own worked SLA/SLO example (99% uptime). `[D]`
- **RCA:** the DataOps section's own diagnostic questions (p209–210) — "when the application database you depend on for CDC exceeds its I/O capacity... how will that affect your ability to receive data" — are a direct incident-investigation checklist for upstream-caused pipeline failures.
- **Optimization:** the wide-column/document-store full-scan cost warning (§6) is a concrete cost-review checkpoint before choosing a naive extraction strategy against either database type.

## 8. How to test / verify these claims

- The write-ahead-log CDC mechanism (§4) is directly testable against any specific database's documentation — whether it exposes a binlog/WAL-based CDC mechanism is a checkable, binary fact for a given technology choice.
- The idempotency claim about exactly-once delivery (§6) is testable by fault injection: kill a consumer between processing and acknowledging a message, and confirm the message is redelivered — this is a standard chaos-engineering test for any message-queue-backed pipeline.
- The NoSQL history section (p192–193, Eric Evans's 2009 blog post on naming "NoSQL") is a directly attributed, quotable primary source — checkable by reading that source directly, not independently verified in this synthesis. `[S]` claim, `[D]` flag on verification status.

## 9. Cross-references

- Directly extends `fundamentals_de` [[ch03_designing_good_data_architecture|Ch.3]] (ACID vocabulary) and [[ch04_choosing_technologies|Ch.4]] (REST terminology) — both synthesized, no contradiction found.
- Explicitly revisits [[ch03_designing_good_data_architecture|Ch.3]]'s data mesh material when discussing data sharing (p202, footnoted to the same Fowler/Dehghani article family) — consistent with the [[ch03_designing_good_data_architecture|Ch.3]] note's own description. `[D]` 
- Reverse ETL is mentioned again here (p202, p212–213) in the CRM-data-sharing context, consistent with its treatment in [[ch02_data_engineering_lifecycle|Ch.2]] (lifecycle stage) and the `databricks_big_book_4e` Lakebase note (vendor product) — three sources now touching the same concept from different angles; worth a consistency check once more chapters accumulate. Flagged for `check_deferred_refs.py`. `[D]`
- The Airflow-orchestration integration question (p211, "if you're using an orchestration framework like Airflow, does it make sense to integrate it with the upstream application team?") connects to [[ch04_choosing_technologies|Ch.4]]'s Airflow distributed-monolith critique — not a contradiction, but the same tool discussed in two different risk contexts.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 5-1 through 5-12 (source-system lifecycle diagram, atomic-transaction diagram, database-log diagram, message/stream diagrams, event/ingestion/process-time diagram, RDBMS row-storage diagram, social-network graph, message-queue diagram, stream-partition diagram, stakeholder diagram) | Captions described narratively above where load-bearing (§1, §4); diagrams not rendered to image for this chapter, consistent with the project-wide `reading_order_risk` finding (header/image-ordering artifact, not corrupted body text). |
| Worked JSON document example (p195–196, the "users" collection with favorite_bands arrays) | The document-store schema concept it illustrates is covered in §1; the literal example payload was not reproduced verbatim here to avoid unnecessary duplication of source text. |
| Table 5-1 (insert-only record versions) and Table 5-2 (RDBMS-vs-document terminology mapping) | Concepts covered narratively in §1/§5; tables not reconstructed in full. |
| "Additional Resources" list (p213, 8 external links) | Bibliography, not chapter content — not synthesized. |
| Footnoted external sources (Eric Evans's NoSQL blog post, Kleppmann's DDIA citation on graph databases, graph-database market-size report, REST critique article, Denmore's data-contract definition, Fowler's data-mesh article) | Quoted or referenced where load-bearing (§1, §5, §8); the source documents themselves were not independently retrieved beyond what this chapter quotes. |
