# Ch.6 — Partitioning

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 213–234 (22 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[U]` unresolved

---

## 1. Concepts and definitions

**Partitioning, defined [S]** (p213): "a way of intentionally breaking a large database down into smaller ones."

An explicit footnote warns this has (p213) "nothing to do with network partitions (netsplits), a type of fault in the network between nodes" — deferred to Ch.8.

**Skew and hot spots, precisely defined [S]** (p215): "If the partitioning is unfair, so that some partitions have more data or queries than others, we call it skewed." "A partition with disproportionately high load is called a hot spot." In the extreme, "nine out of ten nodes are idle, and your bottleneck is the single busy node."

**Key-range partitioning, defined via the paper-encyclopedia analogy [S]** (p215–216): "assign a continuous range of keys (from some minimum to some maximum) to each partition, like the volumes of a paper encyclopedia." Range boundaries "are not necessarily evenly spaced, because your data may not be evenly distributed" — they "need to adapt to the data" to distribute it evenly, chosen either manually or automatically.

**Key-range partitioning's range-scan advantage, worked via a sensor-timestamp example [S]** (p216–217): "we can keep keys in sorted order... range scans are easy" — e.g. fetching all readings from a given month directly. But if the key is a raw timestamp, "all the writes end up going to the same partition (the one for today), so that partition can be overloaded with writes while others sit idle." Fix: prefix the timestamp with a discriminating field (e.g. sensor name) so writes spread across partitions, at the cost of needing a separate range query per discriminator.

**Hash partitioning, defined and its trade-off named directly [S]** (p217–218): "a good hash function takes skewed data and makes it uniformly distributed" — assigning each partition a range of hashes rather than a range of keys. "This technique is good at distributing keys fairly among the partitions," but "we also lost a nice property of key-range partitioning: the ability to do efficient range queries" (p218) since "keys that were once adjacent are now scattered across all the partitions."

**Consistent hashing, precisely scoped and explicitly named a confusing misnomer for databases [S]** (p218): "a way of evenly distributing load across an internet-wide system of caches, such as a CDN," using randomly chosen boundaries to avoid central coordination. "This particular approach actually doesn't work very well for databases... so it is rarely used in practice." The chapter's own recommendation: "it's best to avoid the term consistent hashing, and just call it hash partitioning instead."

**Cassandra's compound-key compromise between key-range and hash partitioning [S]** (p218–219): only the first part of a compound primary key is hashed to pick the partition; the remaining columns form a concatenated sort index within that partition. Worked example: with primary key `(user_id, update_timestamp)`, "you can efficiently retrieve all updates made by a particular user within some time interval, sorted by timestamp" (p218), while different users are spread across different partitions.

**Skewed workloads that hashing cannot fix, the celebrity-user worked example [S]** (p219–220): "in the extreme case where all reads and writes are for the same key, you still end up with all requests being routed to the same partition" — "hashing the key doesn't help, as the hash of two identical IDs is still the same." Named mitigation: append a small random number (e.g. two digits) to a known-hot key, splitting its writes across 100 keys, at the cost of reads needing to fan out and combine all 100, plus bookkeeping to know which keys were split.

**Document-partitioned (local) secondary indexes, defined via the used-car-listing example [S]** (p220–221): "each partition maintains its own secondary indexes, covering only the documents in that partition." Writes touch only one partition, but "reading from a document-partitioned index requires care" — since matching records can be scattered across partitions, a query must "send the query to all partitions, and combine all the results" — a pattern named scatter/gather, which "is prone to tail latency amplification."

**Term-partitioned (global) secondary indexes, defined and their write/read trade-off directly stated [S]** (p222): "a global index... can be partitioned differently from the primary key index," partitioned either by the term itself (useful for range scans) or by a hash of the term (more even load). Advantage: "a client only needs to make a request to the partition containing the term that it wants" for reads. Named downside: "writes are now slower and more complicated, because a write to a single document may now affect multiple partitions of the index."

**Global secondary index update latency, an explicit consistency caveat [S]** (p222): keeping a term-partitioned index perfectly up to date would require "a distributed transaction across all partitions affected by a write, which is not supported in all databases"

In practice (p222), "updates to global secondary indexes are often asynchronous" — Amazon DynamoDB is named as updating within a fraction of a second normally, but potentially experiencing longer propagation delays in case of infrastructure faults. `[D]`

**Rebalancing, defined and its three named minimum requirements [S]** (p223): "the process of moving data around between nodes in the cluster is called rebalancing." After rebalancing, load should be shared fairly; during rebalancing, the database should keep accepting reads and writes; and rebalancing should not move more data than necessary.

**Hash-mod-N rebalancing, explicitly named the wrong approach, with a worked numeric example [S]** (p223–224): "the problem with the mod N approach is that if the number of nodes N changes, most of the keys would need to be moved from one node to another." Worked example: `hash(key)=123456` moves from node 6 (mod 10) to node 3 (mod 11) to node 0 (mod 12) as the cluster grows by one node at a time — "that makes rebalancing excessively expensive."

**Fixed number of partitions, the chapter's own preferred rebalancing strategy for hash partitioning [S]** (p224): "create many more partitions than there are nodes, and assign several partitions to each node" (e.g. 1,000 partitions across 10 nodes). Adding a node lets it "steal a few partitions from every existing node." Crucially, "only entire partitions are moved between nodes... the assignment of keys to partitions does not change" — only which node owns which partition. This also allows manually weighting more powerful nodes with more partitions.

**Dynamic partitioning, the chapter's own mechanism for key-range partitioning [S]** (p225): "when a partition grows to exceed a configured size... it is split into two partitions so that approximately half of the data ends up on each side of the split," and shrinking, deleted-heavy partitions "can be merged with an adjacent partition" — explicitly likened to B-tree node splitting/merging.

**Pre-splitting, a named mitigation for dynamic partitioning's cold-start problem [S]** (p226): "an empty database starts off with a single partition... all writes have to be processed by a single node while the other nodes sit idle" until the first split. HBase and MongoDB let an administrator configure an initial partition set on an empty database to avoid this.

**Automatic vs. manual rebalancing, an explicit availability-vs-safety trade-off with a named cascading-failure risk [S]** (p226–227): fully automatic rebalancing reduces operational burden but "can be unpredictable" and dangerous when combined with automatic failure detection — "one node is overloaded and is temporarily slow to respond... the other nodes conclude that the overloaded node is dead, and automatically rebalance the cluster to move load away from it," which can overload the remaining nodes and "cause a cascading failure." The chapter's own conclusion: "it can be a good thing to have a human in the loop for rebalancing."

**Request routing, defined as an instance of the general service-discovery problem, with three named approaches [S]** (p227–228): (1) let clients contact any node via a load balancer, and have that node forward the request if it doesn't own the relevant partition; (2) send all requests through a dedicated routing tier that itself does no data processing; (3) require clients to be partition-aware and connect directly to the correct node. In all three, "the key problem is: how does the component making the routing decision... learn about changes in the assignment of partitions to nodes?"

**ZooKeeper-based cluster metadata coordination, the chapter's own worked description [S]** (p228): "many distributed data systems rely on a separate coordination service such as ZooKeeper to keep track of this cluster metadata"

"Each node registers itself in ZooKeeper, and ZooKeeper maintains the authoritative mapping of partitions to nodes" (p228), notifying subscribed routing tiers or clients on any change. LinkedIn's Espresso (via Helix), HBase, SolrCloud, and Kafka are named examples; MongoDB uses its own config-server equivalent instead.

**Gossip-protocol routing, Cassandra/Riak's alternative to a coordination service [S]** (p229): nodes "use a gossip protocol among the nodes to disseminate and agree on any changes in cluster state," letting requests be sent to any node which then forwards internally — "this puts more complexity in the database nodes, but avoids the dependency on an external coordination service such as ZooKeeper."

## 2. WHAT / WHY / WHEN

**WHAT:** the chapter's full taxonomy of ways to split a single logical dataset across many machines — key-range vs. hash partitioning of primary data, document- vs. term-partitioned secondary indexes, and the rebalancing/routing machinery needed to keep such a partitioned system correct and load-balanced as nodes are added or removed. `[D]`

**WHY it matters:** replication (Ch.5) alone cannot help once a dataset or its query throughput exceeds what a single machine can store or serve; partitioning is explicitly framed as replication's complement — "for very large datasets, or very high query throughput, that is not sufficient: we also need to break the data up into partitions" (p213) — and the two concerns compose independently, since "the choice of partitioning scheme is mostly independent of the choice of replication scheme" (p214). `[S]`

**WHEN to choose key-range vs. hash partitioning (p215–219, synthesized across the chapter):** favor key-range partitioning when efficient range scans on the primary key are a first-class requirement (e.g. time-series data queried by date range), accepting the risk of write hot spots on monotonically increasing keys unless mitigated (e.g. prefixing with a discriminator); favor hash partitioning when even load distribution matters more than range-scan support, accepting that range queries on the primary key become a full scatter/gather or are unsupported entirely.

**WHEN to choose document-partitioned vs. term-partitioned secondary indexes (p220–223, synthesized across the chapter):** favor document-partitioned (local) indexes when writes must stay cheap and single-partition, and read-side scatter/gather latency is acceptable; favor term-partitioned (global) indexes when secondary-index reads must be served from a single partition and the workload can tolerate both slower, multi-partition writes and (in most real systems) asynchronous index staleness.

## 3. Assumptions and prerequisites

- Directly extends Ch.5's replication material, explicitly stating the two concerns are independent and that "everything we discussed in Chapter 5 about replication of databases applies equally to replication of partitions" — this chapter deliberately ignores replication to isolate partitioning concerns. `[S]` (p214)
- Assumes and directly reuses Ch.3's B-tree and SSTable/LSM-tree sorted-storage mechanics, both for within-partition key ordering under key-range partitioning and for the dynamic-partitioning split/merge analogy to B-tree nodes. `[S]` (p216, p225)
- Forward-references distributed transactions across partitions to Ch.7 (the chapter's own footnote iii points to its "multi-object transactions" section), and distributed consensus protocols underlying reliable request routing to Ch.9 — both not yet synthesized in this vault. `[D]`
- Forward-references parallel query execution techniques for data-warehouse-style analytics to Ch.10 — not yet synthesized in this vault. `[D]`

## 4. Mechanism / key steps

**Fixed-number-of-partitions rebalancing procedure, the chapter's own worked description (p224)** `[D]`: at cluster setup, create a partition count much larger than the expected node count (e.g. 1,000 partitions for 10 nodes) → assign a roughly even share of partitions to each node → when a node is added, it takes over a few partitions from each existing node until the distribution is even again → when a node is removed, its partitions are redistributed to the remaining nodes → throughout, the assignment of individual keys to partitions never changes, only the assignment of whole partitions to nodes, keeping data movement proportional to the rebalancing delta rather than the full dataset.

**Dynamic partitioning's split/merge cycle for key-range partitioning, the chapter's own worked description (p225)** `[D]`: a partition accumulates writes until it exceeds a configured size threshold (e.g. 10GB on HBase) → the partition is split into two, each covering half the original key range → one half may be transferred to a different node to rebalance load, moved via the underlying distributed filesystem (e.g. HDFS for HBase) → conversely, if deletions shrink a partition below a threshold, it can be merged back with an adjacent partition.

## 5. Trade-offs and limitations

- **Key-range partitioning enables efficient range scans but is vulnerable to write hot spots on sequentially increasing keys; hash partitioning distributes load evenly but destroys range-scan efficiency entirely (§1, p216–218):** a direct, unavoidable two-sided trade with no dominant strategy — Cassandra's compound-key compromise (§1, p218–219) only partially resolves it by hashing just the first key component.
- **Document-partitioned secondary indexes keep writes cheap (single partition) but make reads expensive (scatter/gather across all partitions); term-partitioned (global) indexes make reads cheap (single partition) but make writes expensive (potentially many partitions touched) (§1, p220–222):** an explicit, named inversion of the same cost between the two approaches.
- **Fully automatic rebalancing reduces operational toil but risks a cascading failure when combined with automatic failure detection under load (§1, p226–227):** the chapter explicitly favors a human-in-the-loop compromise over full automation, trading operational speed for safety.
- **A fixed number of partitions is operationally simple but caps the maximum future cluster size and wastes overhead if set too high; dynamic partitioning removes that cap but suffers a cold-start single-partition bottleneck on an empty database unless pre-split (§1, p224–226):** neither strategy dominates — the choice depends on whether the workload needs key-range partitioning (which favors dynamic) or hash partitioning (which favors fixed).

## 6. Failure modes and edge cases

- **Celebrity-user hot spots surviving hash partitioning entirely (§1, p219–220):** a real, named production pattern — "a celebrity user with millions of followers may cause a storm of activity" — where hashing provides zero mitigation because the hash of one repeatedly-written key is always the same value, routing every request to the same partition regardless of hash quality.
- **Global secondary index staleness after a write (§1, p223):** a read of a term-partitioned index shortly after a write may not yet reflect that write, since most real systems update global indexes asynchronously rather than transactionally — a concrete, named eventual-consistency gap distinct from the primary-key data path.
- **Automatic-rebalancing-triggered cascading failure (§1, p226–227):** a temporarily overloaded (not actually dead) node gets misdiagnosed as failed by automatic health checks, triggering an automatic rebalance that shifts more load onto already-strained remaining nodes, "potentially overloading more nodes and causing a cascading failure" — a self-inflicted failure mode of the automation meant to prevent downtime.
- **Application-implemented secondary indexes drifting out of sync with primary data (§1, p220, footnote iii):** if a database supports only key-value access and an application hand-rolls a value-to-ID index mapping itself, "race conditions and intermittent write failures... can very easily cause the data to go out of sync" — deferred explicitly to Ch.7's multi-object transaction discussion.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the key-range-vs-hash and document-vs-term-index decision frameworks (§2) are directly reusable as first-pass sharding-strategy decisions for any new partitioned datastore in this vault's projects, driven by whether range scans on the partition key are a real workload requirement. `[D]`
- **Build:** the fixed-number-of-partitions rebalancing pattern (§4, p224) is a directly reusable design choice for any hash-partitioned system anticipating future node growth — provisioning partition count well above the expected eventual node count avoids the hash-mod-N rebalancing trap.
- **Maintain:** the pre-splitting mitigation (§1, p226) is a directly reusable operational technique for any dynamically-partitioned system where the expected key distribution is knowable in advance, avoiding the empty-database single-node bottleneck.
- **RCA:** a cluster observed to enter escalating overload immediately after a partial node slowdown is directly diagnosable against the automatic-rebalancing cascading-failure pattern (§6, p226–227) — check whether automatic rebalancing was triggered by a false-positive failure detection before assuming a capacity problem.
- **Optimization:** the document-vs-term secondary-index trade-off (§1, p220–222) is a directly reusable lever for tuning read/write cost balance in any partitioned system with secondary indexes — favor document-partitioned indexes for write-heavy workloads, term-partitioned for read-heavy ones where read latency dominates.

## 8. How to test / verify these claims

- The hash-mod-N rebalancing cost claim (§1, p223–224) is directly reproducible: compute `hash(key) mod N` for a fixed key across N=10, 11, 12 and confirm the assigned node changes almost every time, versus a fixed-partition-count scheme where only whole-partition ownership moves.
- The document-partitioned scatter/gather read cost (§1, p221) is directly testable: populate a document-partitioned datastore (e.g. MongoDB or Elasticsearch) across several shards, run a secondary-index query, and confirm via query profiling that it fans out to every shard rather than a single one.
- The celebrity-hot-spot claim (§1, p219–220) is directly testable by construction: hash-partition a key-value store, direct a large volume of writes at a single key, and confirm all writes land on one partition/node regardless of hash function quality; then apply the random-suffix mitigation and confirm the writes spread across multiple partitions.
- The global-index asynchronous-staleness claim (§1, p223) is directly testable against a real system (e.g. DynamoDB): write an item, immediately query its global secondary index, and confirm the update is not always instantaneously visible.

## 9. Cross-references

- Directly extends Ch.5's replication material — explicitly stated as an independent, orthogonal concern that composes with partitioning without altering it. No contradiction found. `[S]`
- Directly extends Ch.3's B-tree and SSTable sorted-storage mechanics, reused both for within-partition ordering and as an explicit structural analogy for dynamic partition splitting/merging. `[S]`
- Forward-references (not yet synthesized in this vault): Ch.7 (distributed/multi-object transactions needed for consistent secondary-index maintenance and cross-partition writes), Ch.9 (consensus protocols underlying reliable partition-assignment agreement), and Ch.10 (parallel query execution for analytic/MPP workloads).
- No contradiction found with any already-synthesized source in this vault.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 6-1 through 6-8 (replication+partitioning combination diagram, encyclopedia key-range diagram, hash-partitioning diagram, document/term secondary-index diagrams, rebalancing-migration diagram, ZooKeeper/routing-tier architecture diagrams) | Structure and content described narratively above where load-bearing (§1, §4); full diagram layouts not reproduced verbatim. |
| Full numbered reference list (30 references) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. the Twitter/Bieber celebrity-load reference, DynamoDB's documented index-propagation behavior) are captured inline in §1/§6 with attribution context. |
| Parallel query execution's detailed MPP optimizer mechanics (p229–230) | The chapter itself defers this to Ch.10 and external literature ("please see the literature references"); this note captures only the chapter's own framing-level mention, not manufactured MPP internals beyond what the chapter states. |
