# Ch.8 — Queries, Modeling, and Transformation

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 296–361 (66 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 24,272
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**DDL/DML/DCL/TCL, the chapter's four SQL command families [S]** (p298–299): DDL "defines the state of objects in your database" (CREATE, DROP, UPDATE); DML is for adding/altering data (SELECT, INSERT, UPDATE, DELETE, COPY, MERGE); DCL "allow[s] you to control access to the database objects" (GRANT, DENY, REVOKE); TCL "supports commands that control the details of transactions" (COMMIT, ROLLBACK).

**The life of a query, four steps [S]** (p300): the database engine "compiles the SQL, parsing the code to check for proper" semantics, converts it "into bytecode," the "query optimizer analyzes the bytecode to determine how to execute the query," and finally "the query is executed, and results are produced."

**Row explosion [S]** (p301): "This occurs when we have a large number of many-to-many matches... Suppose the join key in table A has the value this repeated five times, and the join key in table B contains this same value repeated 10 times... This creates 5 × 10 = 50 rows in the output."

**Query commit models, three named database examples [S]** (p303–304): PostgreSQL uses ACID transactions requiring "row locking (blocking reads and writes to certain rows)"; BigQuery uses "a point-in-time full table commit model" where "BigQuery allows only one write operation at a time" (no write concurrency, though internally parallel); MongoDB is "a variable-consistency database" that "will unceremoniously and silently discard writes if it gets overwhelmed with traffic" in certain modes.

**Vacuuming [S]** (p305): the process to "remove these dead records" left behind by updates/deletes; the chapter's own comparative note: "BigQuery utilizes a fixed seven-day history window. Databricks generally retains data indefinitely until it is manually vacuumed" and "In Snowflake, users cannot directly vacuum. Instead, they control a 'time-travel' interval."

**Kappa architecture applied to queries [S]** (p307–308): "treat all data like events and store these events as a stream rather than a table," retaining events "during a more extended retention period" (months or years) so data "can be directly queried from this storage" — contrasted with the fast-follower CDC pattern, which "doesn't fundamentally rethink batch query patterns."

**Streaming windows — session, fixed-time, sliding [S]** (p308–310): session window "groups events that occur close together, and filters out periods of inactivity" (chapter's own example: 5-minute inactivity gap); fixed-time (tumbling) window "features fixed time periods that run on a fixed schedule" (example: closing every 20 seconds); sliding windows are "bucketed into windows of fixed time length, where separate windows might overlap" (example: a 60-second window generated every 30 seconds).

**Watermark [S]** (p310): "a threshold used by a window to determine whether data in a window is within the established time interval or whether it's considered late."

**Conceptual, logical, physical data models [S]** (p314): conceptual "contains business logic and rules and describes the system's data"; logical "details how the conceptual model will be implemented in practice by adding significantly more detail"; physical "defines how the logical model will be implemented in a database system."

**Grain [S]** (p315): "the resolution at which data is stored and queried," typically at "the level of a primary key in a table." The chapter's own explicit rule: "you should strive to model your data at the lowest level of grain possible... it's generally impossible to restore details that have been aggregated away."

**Normalization / normal forms, Codd's definitions [S]** (p315–316): normalization "enforces strict control over the relationships of tables and columns... to remove the redundancy of data within a database and ensure referential integrity" — "don't repeat yourself (DRY) applied to data." First three normal forms defined verbatim: 1NF "Each column is unique and has a single value. The table has a unique primary key"; 2NF "requirements of 1NF, plus partial dependencies are removed"; 3NF "requirements of 2NF, plus each table contains only relevant fields related to its primary key and has no transitive dependencies."

**Inmon's data warehouse definition [S]** (p320): "A data warehouse is a subject-oriented, integrated, nonvolatile, and time-variant collection of data in support of management's decisions" — the four parts: subject-oriented, integrated, nonvolatile, time-variant.

**Kimball star schema — facts and dimensions [S]** (p322–324): fact tables contain "factual, quantitative, and event-related data," are "immutable," "narrow and long," and "don't reference other fact tables; they reference only dimensions." Dimension tables are "typically wide and short," providing "attributes and relational context," and are "denormalized, with the possibility of duplicate data."

**Slowly changing dimension (SCD) types 1–3 [S]** (p324–325): Type 1 "overwrite[s] existing dimension records" (no history); Type 2 "keep[s] a full history of dimension records" via a new row per change (using `EFF_StartDate`/`EFF_EndDate`); Type 3 "creates a new field" rather than a new row on change. "Type 1 is the default behavior of most data warehouses, and Type 2 is the one we most commonly see used in practice."

**Data Vault — hubs, links, satellites [S]** (p326–329): "a hub stores business keys, a link maintains relationships among business keys, and a satellite represents a business key's attributes and context." A hub is "insert-only, and data is not altered in a hub. Once data is loaded into a hub, it's permanent." Standard hub fields: hash key, load date, record source, business key(s).

**Wide denormalized tables [S]** (p330–331): "a highly denormalized and very wide collection of many fields, typically created in a columnar database," where "nulls take up virtually no space in a columnar database" (unlike relational databases, where "the database allocates a fixed amount of space for each field entry").

**Broadcast join vs. shuffle hash join [S]** (p336): broadcast join — "one large table distributed across nodes and one small table that can easily fit on a single node," where the engine "broadcasts the small table" out to all nodes; shuffle hash join — used "if neither table is small enough to fit on a single node," using a hashing scheme "to repartition data by join key" (p336).

**Copy on write (COW) [S]** (p342): "If one record in a file is changed or deleted, the whole file must be rewritten with the new changes" — the underlying mechanism explaining why upsert/merge is expensive in file-based (columnar/data lake) systems versus row-based databases.

**MapReduce, the canonical mechanism [S]** (p347–348): "a collection of map tasks that read individual data blocks scattered across the nodes, followed by a shuffle that redistributes result data across the cluster and a reduce step that aggregates data on each node." The map phase is "a nearly perfect example of embarrassing parallelism."

**Materialized view vs. view vs. federated query vs. data virtualization [S]** (p348–350): a view "is just a query that references other tables," computed fresh each time; a materialized view "does some or all of the view computation in advance"; a federated query "allows an OLAP database to select from an external data source"; data virtualization "typically entails a data processing and query system that doesn't store data internally" (named examples: Trino, Presto).

**Query pushdown [S]** (p351): "Query pushdown aims to move as much work as possible to the source databases." — reducing both compute at the virtualization layer and data transferred across the network.

## 2. WHAT / WHY / WHEN

**WHAT:** The chapter covers three tightly linked topics: (1) queries — how they execute, how to optimize them, and streaming query patterns; (2) data modeling — conceptual/logical/physical models, normalization, and the three major batch-modeling approaches (Inmon, Kimball, Data Vault) plus wide tables and the (unsettled) state of streaming data modeling; (3) transformations — batch and streaming transformation patterns, update patterns (truncate-and-reload, insert-only, delete, upsert/merge), and virtualization techniques (views, materialized views, federation, data virtualization). `[D]`

**WHY it matters:** the chapter's own framing at the outset: "In this chapter, you'll learn how to make data useful... you'll have the tools to turn raw data ingredients into something consumable by downstream stakeholders" (p296). `[S]`

**WHEN to prejoin data vs. join at query time (p300–301):** "If you find that analytics queries are joining the same data repeatedly, it often makes sense to join the data in advance" — via widened tables/prejoined tables or materialized views over frequently repeated join patterns.

**WHEN to choose Inmon vs. Kimball vs. Data Vault (the chapter's own comparative framing, p319–329):** Inmon for a normalized, integrated, single-source-of-truth enterprise warehouse with department-specific data marts fed downstream; Kimball for faster iteration with a bottom-up, business-process-oriented star schema directly in the warehouse (accepting redundancy); Data Vault for agility and auditability when source-system structure must be preserved separately from interpreted business logic, especially amid fast-changing source schemas. The chapter notes these "can be combined" and "start with Data Vault and then add a Kimball star schema alongside it" (p319).

**WHEN to avoid SQL for batch transformations in Spark (the chapter's own three-question checklist, p332–333):** "1. How difficult is it to code the transformation in SQL? 2. How readable and maintainable will the resulting SQL code be? 3. Should some of the transformation code be pushed into a custom library for future reuse?" — with word-stemming given as the chapter's own worked example of a transformation better suited to native code than SQL.

## 3. Assumptions and prerequisites

- Assumes SQL fluency and the primary/foreign-key vocabulary: "This chapter assumes you have an understanding of the SQL language and related concepts like primary and foreign keys" (p297). `[S]`
- Assumes CRUD from Ch.5: "Recall our conversation in Chapter 5 about CRUD" (p298). `[S]`
- Assumes ETL/ELT and data warehouse framing from Ch.3, and consistency vocabulary (dirty reads, ACID) from Ch.5/Ch.6: "As we discussed in Chapter 3, a widespread transformation pattern" (p336); "Refer to Chapter 6 for a deeper discussion of consistency" (p305). `[S]`
- Assumes Kappa/Lambda architecture terminology from Ch.3: "recall the Kappa architecture we discussed in Chapter 3" (p307). `[S]`
- Assumes MapReduce and Hadoop/GFS framing from Ch.6: "the open source analogue technology of GFS that we introduced in Chapter 6" (p347). `[S]`
- Explicitly defers metrics/semantic layer depth to Ch.9: "We discuss semantic and metrics layers in more detail in Chapter 9" (p346). `[S]`

## 4. Mechanism / key steps

**Distributed join execution, shuffle hash join (p335–336):** tables A and B are initially partitioned across nodes with no relation to the join key → a hashing scheme repartitions the join key into N parts → data is reshuffled so each node holds one partition of both tables → the local partitions on each node are joined. Broadcast join skips the shuffle when one table is small enough to replicate to every node. `[D]` (this note's own step-sequencing of the chapter's mechanism, not a verbatim quote.)

**MapReduce's map/shuffle/reduce sequence, the chapter's own worked example (p346–347):** SQL `SELECT COUNT(*), user_id FROM user_events GROUP BY user_id` → one map task per data block computes a partial count per `user_id` within that block → shuffle step redistributes partial results by key hash so each key lands on exactly one node → reduce step sums the partial counts per key on that node → results are collected across nodes for the final output. `[D]` (this note's own step-sequencing of the chapter's mechanism, not a verbatim quote.)

**Upsert/merge under copy-on-write (p341–342):** a source record set is matched against a target table by key → on a match, "the target record gets updated (replaced by the new record)" (p342) → on no match, "the database inserts the new record" (p342). The chapter notes COW granularity varies by system (partition, cluster, or block level), which is the real lever for controlling update cost. `[D]` (this note's own step-sequencing of the COW mechanism.)

**Query pushdown in a data-virtualization layer (p351):** a query joining Snowflake and MySQL data is submitted to the virtualization engine (e.g. Trino) → the engine identifies filter predicates that can be evaluated at the source → those predicates are pushed down and executed inside MySQL/Snowflake directly → only the reduced result set crosses the network to be joined/finalized in the virtualization layer. `[D]` (this note's own step-sequencing of the chapter's mechanism, not a verbatim quote.)

## 5. Trade-offs and limitations

- **PostgreSQL's row-locking cost, stated directly (p304):** "requires row locking (blocking reads and writes to certain rows), which can degrade performance in various ways. PostgreSQL is not optimized for large scans or the massive amounts of data appropriate for large-scale analytics applications."
- **MongoDB's high-write-performance trade-off, stated directly (p304):** in certain modes, "the database will unceremoniously and silently discard writes if it gets overwhelmed with traffic" — explicitly framed as acceptable for IoT-style measurement collection but "not a great fit for applications that need to capture exact data and statistics."
- **Insert-only's query-time cost (p340–341):** "it can be extremely computationally expensive to find the latest record at query time" — mitigated by combining an insert-only history table with a truncate-and-reload current-state table.
- **Data Vault's deferred business logic (§1):** "there's no notion of good, bad, or conformed data in a Data Vault" (p326) and "the business logic is created and interpreted when the data from these tables is queried" (p330) — an explicit trade-off of flexibility against upfront interpretability.
- **Wide tables' update cost and lost business logic, stated directly (p331):** "The biggest criticism is as you blend your data, you lose the business logic in your analytics. Another downside is the performance of updates to things like an element in an array, which can be very painful."
- **Derived-data consistency risk, cited to an external critique (p346):** "if the company updates its attribution model, this change may need to be merged into many ETL scripts for reporting" and "Updated scripts must also be validated for consistency and accuracy" — footnoted to Michael Blaha's "Be Careful with Derived Data."
- **Near-real-time merges against columnar warehouses, a named operational failure (p343):** "We've seen systems fall weeks behind on updates, where an approach that simply merged every hour would make much more sense" — a direct warning against porting row-database CDC-merge cadences onto columnar systems.

## 6. Failure modes and edge cases

- **Row explosion causing query failure, worked example (§1, p301):** repeated join-key values on both sides of a join can multiply row counts combinatorially, "generat[ing] enough rows to consume a massive quantity of database resources or even cause a query to fail" — the chapter notes predicate reordering by the optimizer can mitigate this if it runs before the explosion, but "a row explosion in an early query stage may cause the query to fail" if it doesn't.
- **`SELECT *` production outage, a named real incident (p306, footnote 3):** "an incident involving a new analyst at a large grocery store chain running SELECT * on a production database and bringing down a critical inventory database for three days."
- **Single-row inserts into columnar OLAP, an explicit anti-pattern (p341):** "engineers transitioning from row-oriented systems attempt to use single-row inserts. This antipattern puts a massive load on the system... causes data to be written in many separate files; this is extremely inefficient for subsequent reads, and the data must be reclustered later."
- **Streaming schema drift breaking downstream consumers (p333):** "an IoT device that recently upgraded its firmware and introduced a new field" and "it's possible that your downstream destination data warehouse or processing pipeline isn't aware of this change and breaks" — the chapter's named worked example of streaming schema evolution risk.
- **PySpark UDF performance cliff (p339, footnote 15):** "We've seen JavaScript UDFs increase query time from a few minutes to several hours" — a concrete, quantified failure mode for careless UDF use.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the conceptual→logical→physical modeling continuum (§1) is a directly reusable design-review gate — a new data model should be validated at the conceptual (business logic/ER) level with stakeholders before physical implementation decisions are made. `[D]`
- **Build:** the "model at the lowest grain possible" rule (§1, p315) is a concrete, source-backed build constraint — build systems should default to the finest available grain since aggregation is always possible downstream but disaggregation is not.
- **Maintain:** the vacuuming comparison table across BigQuery/Snowflake/Databricks/Redshift (§1) is a directly reusable maintenance checklist per platform when a vault project adopts any of these warehouses.
- **RCA:** the row-explosion mechanism (§6) is a direct diagnostic hypothesis for any "query suddenly consumed all cluster resources" incident involving a join — check for repeated join-key values before assuming a data-volume or infrastructure problem. `[D]`
- **Optimization:** the broadcast-vs-shuffle-hash-join distinction (§1/§4) is a directly checkable query-plan review item — confirming whether a query optimizer chose (or could have chosen) a broadcast join for a small-table join is a concrete performance-tuning lever.

## 8. How to test / verify these claims

- The row-explosion mechanism (§5/§6) is directly reproducible: construct two tables with a repeated join key on each side and observe the multiplicative row-count blowup in a test database — a mechanically verifiable claim, not just a warning.
- The BigQuery/Snowflake/Databricks vacuuming behaviors (§1) are checkable against each vendor's current documentation; the specific numbers given (BigQuery's 7-day history window) are `[S]` as of the book's 2022 writing but `[U]` as to whether they still hold today.
- The COW-based upsert cost claim (§4/§5) is testable empirically: benchmark single-record updates against a columnar/data-lake table of varying partition granularity and observe file-rewrite cost scale with partition size, not row count.
- The broadcast-join vs. shuffle-hash-join choice (§1/§4) is directly checkable via a query engine's own explain plan — confirming which join strategy the optimizer selected for a given query is a mechanically verifiable fact, not an inference.

## 9. Cross-references

- Directly extends `fundamentals_de` Ch.3 (ETL/ELT, Kappa/Lambda architecture, data mesh), Ch.5 (CRUD, ACID, transactions), Ch.6 (consistency, columnar storage, Hadoop/GFS/MapReduce lineage, single-/multi-tenant), Ch.7 (CDC as a query-pattern building block, schema evolution) — all previously synthesized, no contradiction found.
- Forward-references Ch.9 (semantic/metrics layers, p340; serving stage generally) and Ch.11 (streaming data modeling's unsettled future, p321; the "live data stack," p347) — neither yet synthesized. Flagged for `check_deferred_refs.py`.
- The Kimball star-schema/fact/dimension material here (§1) is the first place in this vault's fundamentals_de notes to directly parallel the already-synthesized `kimball_dwtoolkit_3e` Ch.9 (Human Resources Management) note — both describe fact/dimension/SCD mechanics; no contradiction observed, and this chapter's treatment is explicitly framed as "cursory" compared to the dedicated Kimball text (p320). Flagged for `check_deferred_refs.py` as a consistency check once more `kimball_dwtoolkit_3e` chapters are synthesized.
- The Data Vault material here (§1) is the vault's first exposure to hub/link/satellite modeling — no existing note to cross-check against yet.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 8-1 through 8-21 (transformation-value diagram, life-of-a-query diagram, window diagrams, star-schema/Data-Vault diagrams, join diagrams, federated-query diagram, streaming-DAG diagram) | Captions and content described narratively above where load-bearing (§1, §4); diagrams not rendered to image for this chapter, consistent with the project-wide `reading_order_risk` finding. |
| Full worked normalization example (Tables 8-1 through 8-8, the OrderDetail→1NF→2NF→3NF walkthrough) | The normal-form definitions and their meaning are captured in §1; the full multi-table worked example is not reproduced verbatim here to avoid unnecessary duplication of source tables. |
| Full worked Data Vault example (Tables 8-14 through 8-20, hub/link/satellite population with hash keys) | Hub/link/satellite mechanics captured in §1; the specific populated sample tables are not reproduced. |
| Detailed "Whom You'll Work With" subsections (Upstream/Downstream Stakeholders, p329–330) | Organizational-role content, summarized at a high level via §2/§7 rather than reproduced in full — largely restates the general stakeholder framing already established in earlier chapters, applied specifically to queries/modeling/transformation. |
| "Additional Resources" list (p335, p360–361, ~30 external links) | Bibliography, not chapter content — not synthesized. |
| Footnoted external sources (Inmon's and Kimball's books, Codd's normalization paper, Blaha's derived-data critique, Stancil's metrics-layer article, the Spark stream-join blog post, the Pulsar-vs-Kafka blog post) | Quoted or referenced where load-bearing (§1, §5); source documents not independently retrieved beyond what this chapter quotes. |
| Data wrangling tools section (p335–336) and the worked Spark-pipeline example (p341–342, Airflow+Spark+S3+Delta Lake) | Descriptive/procedural content rather than falsifiable technical claims requiring citation-level synthesis; summarized at a high level in §2 rather than reproduced in full. |
