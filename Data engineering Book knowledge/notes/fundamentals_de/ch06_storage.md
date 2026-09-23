# Ch.6 — Storage

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 214–257 (44 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 16,116
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**The three "raw ingredients" of storage [S]** (p216–219): magnetic disks, SSDs, and RAM — each characterized by cost, latency, throughput, and IOPS. The chapter's own figures: magnetic disk drives "cost roughly 3 cents per gigabyte of capacity" (p216); the first commercial drive, "the IBM 350, had a capacity of 3.75 megabytes," with current drives supporting "maximum data transfer speeds of 200–300 MB/s" (p217); magnetic disks see "over four milliseconds of overall average latency" and range "from 50 to 500 IOPS" (p218); SSDs "can look up random data in less than 0.1 ms" and "cost 20–30 cents (USD) per gigabyte of capacity" (p218); RAM/DDR5 offers "retrieval latency on the order of 100 ns, roughly 1,000 times faster than SSD" and is "significantly more expensive than SSD storage, at roughly $10/GB" (p219).

**Single vs. distributed storage [S]** (p208–209 range, "Data Storage Systems"): single storage keeps data on one node/device; distributed storage spreads data across multiple nodes for durability and scalability, trading off consistency guarantees.

**Eventual vs. strong consistency, BASE vs. ACID [S]** (in the "Data Storage Systems" section): strong consistency guarantees any read reflects the latest write; eventual consistency (BASE — Basically Available, Soft state, Eventual consistency) is explicitly contrasted with the ACID model already introduced in Ch.5.

**File storage, block storage, object storage — the chapter's three system types [S]**: file storage (local disk, NAS, cloud filesystems like EFS); block storage (RAID, SAN, EBS, local instance volumes, with EBS's point-in-time snapshot and differential-backup mechanics described); object storage (key-value, immutable-object model, addressed by bucket/key — the chapter's own worked example address is `S3://oreilly-data-engineering-book/data-example.json`).

**Object storage consistency and the two-step strong-consistency workaround [S]**: object stores are described with a versioning mechanism and a documented pattern for achieving strong-consistency-like behavior via a two-step read/verify sequence over an inherently eventually-consistent store.

**Storage tiers/classes, S3 as the worked example [S]**: named tiers include Standard-IA and Glacier Deep Archive, with Glacier Deep Archive priced at "$1/TB/month" and quoted at "12-hour" restore time.

**Hadoop Distributed File System (HDFS) [S]** (p236, "The Hadoop Distributed File System"): "based on Google File System (GFS)" and "initially engineered to process data with the MapReduce programming model." HDFS "breaks large files into blocks, chunks of data less than a few hundred megabytes in size," managed by a NameNode that "maintains directories, file metadata, and a detailed catalog describing the location of file blocks in the cluster." Default replication factor: "each block of data is replicated to three nodes" (p236–237).

**Streaming storage and replay [S]** (p237–238, "Streaming Storage"): Kafka "supports indefinite data retention by pushing old, infrequently accessed messages down to object storage." Replay is defined as: "a streaming system to return a range of historical stored data" and is called "the standard data-retrieval mechanism for streaming storage systems."

**Columnar serialization, partitioning, and clustering [S]** (p238–240, "Indexes, Partitioning, and Clustering"): columnar databases "scan only the columns required for a particular query," and packing similar values by column "yield[s] high-compression ratios with minimal compression overhead." Partitioning "split[s]" a table "on a field" (date/time partitioning called out as most common); clustering "sorts data by one or a few fields, colocating similar values" within partitions.

**Snowflake micro-partitioning, the chapter's named example [S]** (p239–240): "sets of rows between 50 and 500 megabytes in uncompressed size," clustered algorithmically rather than on a single designated field, enabling predicate pruning (the chapter's own worked example: `WHERE created_date='2022-01-02'`) via a metadata database that "stores a description of each micro-partition, including the number of rows and value ranges for fields."

**Data lake, data warehouse, data lakehouse, data platform [S]** (p240–243, "Data Engineering Storage Abstractions"): data warehouse = "technology platforms ... an architecture for data centralization, and an organizational pattern"; data lake = "a storage area for massive amounts of unprocessed raw data, as originally conceived by James Dixon"; data lakehouse = an architecture that "stores data in object storage just like a lake" but "adds ... features designed to streamline data management and create an engineering experience similar to a data warehouse" — "robust table and schema support," incremental update/delete, and table history/rollback. Databricks's Delta Lake is named as the example promoting this concept, with Apache Hudi and Apache Iceberg named as competitors.

**Zero-copy cloning [S]** (p247–248): "a new virtual copy of an object is created (e.g., a new table) without necessarily physically copying the underlying data" — new pointers to raw files, described via a Python shallow-copy analogy; contrasted with the more expensive but more robust "deep copying," where all underlying data objects are copied.

**Hot, warm, cold data [S]** (p248–250, "Hot, warm, and cold data"): hot data has "instant or frequent access requirements," stored on SSD/memory, most expensive to store but often cheap to retrieve; warm data is "accessed semi-regularly, say, once per month" (named example tiers: S3 Infrequent Access, GCS Nearline); cold data is "infrequently accessed," stored on cheap durable media (HDD, tape, cloud archival), cheap to store but expensive/slow to retrieve.

**Single-tenant vs. multitenant storage [S]** (p251–253, "Single-Tenant Versus Multitenant Storage"): single-tenant gives "each group of tenants ... its own dedicated set of resources" with data "totally isolated"; multitenant "shares these resources among groups of users," storing multiple tenants "within a single database."

## 2. WHAT / WHY / WHEN

**WHAT:** The chapter covers the physical and architectural layers of storage as it underpins the whole data engineering lifecycle: the raw hardware ingredients (disk/SSD/RAM), the storage-system types built on them (file/block/object/streaming), storage engines' evolution (indexes → columnar → partitioning/clustering), the higher-level abstractions data engineers actually work with (warehouse/lake/lakehouse/platform), and cross-cutting "big ideas" (data catalog, data sharing, schema-on-write vs. schema-on-read, compute/storage separation, storage lifecycle and retention, single- vs. multi-tenant storage). `[D]`

**WHY it matters:** storage is framed as the connective tissue of the whole lifecycle — the chapter's own closing line: "Storage is everywhere and underlays many stages of the data engineering lifecycle" (Conclusion, near p255). The undercurrents section makes the same point directly: "the undercurrents for storage differ because storage is so ubiquitous" (near p254, "Undercurrents"). `[S]`

**WHEN to choose object storage over HDFS/Hadoop:** the chapter's own framing under "Hadoop is dead. Long live Hadoop!" (p237) is nuanced rather than absolute — HDFS "remains widely used" and is "a key ingredient of many current big data engines, such as Amazon EMR," with "Apache Spark ... still commonly run on HDFS clusters," but smaller companies are told to "reconsider the cost overhead and scale limitations of running a small Hadoop cluster against migrating to cloud solutions," while massive thousand-node on-premises operators are treated as a reasonable exception.

**WHEN to separate compute from storage vs. colocate (the chapter's explicit motivations, "Separation of Compute from Storage" section):** separation is favored for ephemerality/scalability (pay-as-you-go, spin up/down clusters) and for data durability/availability (multi-zone object storage); colocation is favored when raw performance from local, low-latency disk access matters more than elasticity — the chapter is explicit that most real systems "hybridize colocation and separation," citing AWS EMR+S3+HDFS, Apache Spark, Apache Druid, and Google's Colossus/BigQuery as named hybrid examples.

## 3. Assumptions and prerequisites

- Assumes the RAM/ACID vocabulary from Ch.5 is carried forward — BASE is explicitly introduced "contrasted against ACID from Chapter 3/5" framing in the consistency discussion. `[D]` (exact cross-chapter phrasing not independently re-quoted here.)
- Assumes the data lake/warehouse/lakehouse concepts sketched in Ch.3 as prerequisite: "We introduced many of these abstractions in Chapter 3, and we will revisit them here" (p240, "Data Engineering Storage Abstractions"). `[S]`
- Assumes MapReduce is a forward reference not yet covered: "This was originally achieved using the MapReduce programming model, which we discuss in Chapter 8" (p237). `[S]`
- Assumes replay/streaming detail is deferred: "Chapter 7 covers replay in more depth" (p237). `[S]`

## 4. Mechanism / key steps

**EBS-style block storage snapshotting (block storage section, before p236):** point-in-time snapshots plus differential backups — later snapshots capture only changed blocks relative to the prior snapshot, reducing storage cost and backup time versus a full copy each time. `[D]` summarizing the chapter's EBS mechanics; exact quoted wording not re-extracted here.

**HDFS replication and self-healing (p236–237):** "In a typical configuration, each block of data is replicated to three nodes." On failure, "If a disk or node fails, the replication factor for some file blocks will fall below 3. The NameNode will instruct other nodes to replicate these file blocks so that they again reach the correct replication factor" — an automatic, continuous repair loop, not a manual recovery step.

**Snowflake micro-partition pruning (p239–240):** ingest → Snowflake's algorithm groups rows into 50–500MB micro-partitions clustering similar values (not naive single-field partitioning) → metadata database records row counts and value ranges per micro-partition → at query time, the engine consults metadata to exclude (prune) micro-partitions that cannot match the predicate, before scanning any data. `[D]` (this note's own step-sequencing of the chapter's mechanism, not a verbatim quote.)

**Stream-to-batch storage architecture (p242, "Stream-to-Batch Storage Architecture"):** a topic's data is written out to multiple consumers — some real-time (statistics on the live stream), one batch consumer for long-term retention (e.g., AWS Kinesis Firehose generating S3 objects on time/size triggers). Named example: BigQuery ingests streaming data into a "streaming buffer," which is "automatically reserialized into columnar object storage," while the query engine transparently unions the buffer and object-store data for a near-real-time view.

## 5. Trade-offs and limitations

- **RAM's durability trade-off (p219 framing, restated at p236 in "Cache and Memory-Based Storage Systems"):** "traditional RAM is extremely vulnerable to data loss because a power outage lasting even a second can erase data" — hence RAM-based systems (Memcached, Redis) are positioned for caching, not primary retention; Redis is noted to trade some durability for performance: "with a typical configuration, Redis writes data roughly every two seconds" and is "suitable for extremely high-performance applications but can tolerate a small amount of data loss" (p236).
- **Columnar databases' transactional weakness, stated directly (p238):** "Columnar databases perform poorly for transactional use cases—i.e., when we try to look up large numbers of individual rows asynchronously," while performing "extremely well when large quantities of data must be scanned"
- **Object-store filesystem mounting's narrow fit (p235–236 transition into p236 top):** "Mounting object storage as a local filesystem works well for files that are updated infrequently" — an explicit scope limitation, not a general-purpose filesystem substitute.
- **Zero-copy cloning's shared-underlying-data risk (p247–248):** "cloning an object in a data lake environment and then deleting the files in the original object might also wipe out the new object" — an explicit warning that shallow-copy semantics can silently destroy data engineers assume is independent, especially in systems (Databricks) where engineers have direct access to underlying files ("a blessing and a curse").
- **Storage-tier cost/retrieval trade-off, stated as a spectrum, not a binary (p249–250):** "If you store all of your data in hot storage, all of the data can be accessed quickly. But this comes at a tremendous price!" versus all-cold storage lowering storage cost "at the expense of prolonged retrieval times and high retrieval costs."
- **Single-tenant schema-drift risk (p251–252):** "If each tenant's schema isn't uniform across all tenants, this has major consequences if you need to query multiple tenants' tables to create a unified view of all tenant data" — an explicit named cost of the flexibility single-tenant storage otherwise grants.

## 6. Failure modes and edge cases

- **Correlated failure as the residual risk of replication (p236–237):** even with 3x HDFS replication, "the probability of losing data is very low, barring a correlated failure (e.g., an asteroid hitting the data center)" — the book's own deliberately extreme example naming what standard replication does NOT protect against.
- **Hot-storage overflow / spillover (p250, "Storage tier considerations"):** "if hot data is stored in memory, it can be spilled to disk when there's too much new data to store and not enough memory" — a concrete operational failure mode for memory-tier systems, mitigated automatically by managed cloud services but requiring manual handling otherwise.
- **Data hoarding leading to data swamps (p250–251, "Data retention"):** "This data hoarding inevitably became unwieldy and dirty, giving rise to data swamps and regulatory crackdowns on data retention" — named as the historical failure mode that motivates deliberate retention policy rather than indefinite accumulation.
- **Container/multitenancy carry-forward risk:** not this chapter's own topic (covered in Ch.4), but the single-tenant/multitenant framing here (p251–253) is the storage-layer half of that same risk surface — cross-referenced in §9 below. `[D]`

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the storage-tier decision framework (hot/warm/cold, §1/§6) is a directly actionable input to any new pipeline's storage architecture — access-frequency profiling should precede tier selection, per the chapter's own "How important is the data to downstream users, and how often do they need to access it?" framing (p248). `[S]`
- **Build:** the automated-lifecycle-policy recommendation (p250, "Data retention"/"Storage tier considerations") is a concrete build requirement: "create automated lifecycle policies for your data" rather than manual tier migration — directly reusable guidance for any object-storage-backed pipeline built in this vault's projects. `[S]`
- **Maintain:** the zero-copy-cloning caution (§5) is a direct operational rule for anyone maintaining a Databricks/Delta Lake or Snowflake/BigQuery environment — verify whether a "clone" is shallow (pointer-based) or deep before deleting any "original" data. `[D]`
- **RCA:** the correlated-failure framing (§6) reframes "why did we still lose data despite 3x replication" postmortems — the answer should be sought in shared-fate infrastructure (same rack, same zone, same power domain), not in the replication factor itself. `[D]`
- **Optimization:** Snowflake micro-partition pruning (§4) is a directly checkable query-optimization lever — confirm predicate columns actually participate in clustering/pruning before assuming a slow query is an indexing problem in the traditional RDBMS sense. `[D]`

## 8. How to test / verify these claims

- The HDFS self-healing replication claim (§4) is directly testable: kill a datanode in a real HDFS cluster and observe the NameNode re-replicate under-replicated blocks — a standard chaos-engineering verification for this exact mechanism.
- The Redis persistence-interval claim ("roughly every two seconds", §5) is checkable against Redis's own `save`/AOF configuration documentation for a given deployment — the book's number is a typical default, not a universal constant.
- The Snowflake micro-partitioning and pruning claim (§4) is checkable via Snowflake's own query profile output (`EXPLAIN`/query history showing partitions scanned vs. total) for a given warehouse and query.
- The S3 Glacier Deep Archive pricing/restore-time figures (§1) are checkable directly against current AWS pricing pages — these are vendor prices subject to change and are `[S]` as reported in the 2022 text but `[U]` as to whether they still hold today.

## 9. Cross-references

- Directly extends `fundamentals_de` [[ch03_designing_good_data_architecture|Ch.3]]'s data warehouse/lake/lakehouse framing ("We introduced many of these abstractions in Chapter 3, and we will revisit them here," p240) and [[ch05_data_generation_source_systems|Ch.5]]'s ACID/consistency vocabulary — both synthesized, no contradiction found.
- Forward-references [[ch07_ingestion|Ch.7]] (replay, p237) and [[ch08_queries_modeling_transformation|Ch.8]] (MapReduce, p236; normalization/denormalization and single-/multi-tenant querying, p239, p253) — both not yet synthesized. Flagged for `check_deferred_refs.py`.
- The data lakehouse material here (Delta Lake, Hudi, Iceberg, p242) directly overlaps with the `databricks_big_book_4e` Reverse ETL/Lakebase note already synthesized — same lakehouse concept approached from the vendor-platform angle there versus the conceptual-storage angle here; no contradiction, but worth a consistency check once more `databricks_big_book_4e` chapters are synthesized. Flagged for `check_deferred_refs.py`.
- Appendix A (serialization/compression, already synthesized) is directly cross-referenced by this chapter for columnar serialization detail ("In 'Raw Ingredients of Data Storage' on page 191, we discuss columnar serialization," p238) — consistent with Appendix A's own scope.
- The single-tenant/multitenant storage discussion here (p251–253) is the storage-layer counterpart to [[ch03_designing_good_data_architecture|Ch.3]]'s architecture-level single-/multi-tenant trade-off discussion ("we covered the trade-offs between single-tenant and multitenant", p251) — consistent, no contradiction.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 6-1 through 6-11 (storage-as-cornerstone diagram, cache hierarchy table, magnetic disk diagram, single/distributed storage diagram, EBS replication diagram, instance-store-volume diagrams, object-storage diagram, hot/warm/cold cost diagram, single-tenant diagram, multitenant diagram) | Captions and content described narratively above where load-bearing (§1, §4, §6); diagrams not rendered to image for this chapter, consistent with the project-wide `reading_order_risk` finding. |
| Table 6-1 (cache hierarchy latency/cost data) | Concept covered narratively in §1 (RAM/SSD/disk latency figures); full table not reconstructed. |
| Worked footnoted citations (Dageville's Snowflake SIGMOD paper, James Dixon's data lake blog post, Lakshmanan & Tigani's BigQuery book on Colossus) | Referenced where load-bearing (§1, §4); source documents not independently retrieved beyond what this chapter quotes. |
| "Additional Resources" list (p256, 10 external links) | Bibliography, not chapter content — not synthesized. |
| Full "Undercurrents" subsections (Security, Data Management, Privacy, DataOps, Data Architecture, Orchestration, Software Engineering, p228–230/p254–255) | Covered at summary level via cross-reference to Ch.1–Ch.3's undercurrent definitions; this chapter mostly restates those undercurrents applied specifically to storage rather than introducing new mechanisms — not repeated in full detail to avoid duplicating earlier chapters' notes. |
| "Whom You'll Work With" section (p227–228/near p253–254) | Organizational-role content, not a technical claim requiring citation-level synthesis; summarized at a high level only. |
