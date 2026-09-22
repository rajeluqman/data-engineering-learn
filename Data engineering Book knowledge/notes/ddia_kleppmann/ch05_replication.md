# Ch.5 — Replication

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 167–212 (46 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[U]` unresolved

---

## 1. Concepts and definitions

**Replication, defined and its three named motivations [S]** (p167): "keeping a copy of the same data on multiple machines that are connected via a network." Named reasons: geographic proximity to users (lower latency), continued operation despite partial failure (availability), and scaling read throughput across machines.

**Leader-based replication, the chapter's own three-rule mechanism [S]** (p168–169): one replica is the leader (master/primary) — clients must send writes to it; the other replicas are followers (read replicas/slaves/hot standbys) — the leader sends every write to them "as part of a replication log or change stream," and each follower applies writes "in the same order as they were processed on the leader"; clients may read from the leader or any follower, but "writes are only accepted on the leader."

**Synchronous vs. asynchronous replication, precisely distinguished [S]** (p169–171): synchronous means "the leader waits until follower 1 has confirmed that it received the write before reporting success to the user"; asynchronous means "the leader sends the message, but doesn't wait for a response." Fully synchronous replication to all followers is named impractical: "any one node outage would cause the whole system to grind to a halt." The common compromise is semi-synchronous: exactly one follower is synchronous (promoted from the asynchronous pool if it becomes unavailable), guaranteeing an up-to-date copy on "at least two nodes: the leader and one synchronous follower."

**Setting up a new follower, the chapter's own four-step procedure [S]** (p171): take a consistent snapshot of the leader without locking the whole database; copy the snapshot to the new node; the follower requests all changes since the snapshot's exact log position (PostgreSQL's log sequence number, MySQL's binlog coordinates); the follower applies the backlog and "has caught up."

**Failover, defined and its three-step automatic procedure [S]** (p172–173): "one of the followers needs to be promoted to be the new leader, clients need to be reconfigured to send their writes to the new leader, and the other followers need to start consuming data changes from the new leader." Automatic failover: (1) detect leader failure, almost always via a timeout heuristic since "there is no foolproof way of detecting what has gone wrong"; (2) choose a new leader, either by election among replicas or via a pre-elected controller, favoring the replica with the most up-to-date data; (3) reconfigure clients and ensure the old leader steps down to follower if it rejoins.

**Split brain, defined and named dangerous [S]** (p173): the situation "when two nodes both believe that they are the leader" — if both accept writes with no conflict-resolution process, "data is likely to be lost or corrupted." Some systems use fencing/STONITH ("Shoot The Other Node In The Head") to shut one node down when this is detected.

**Statement-based, WAL-shipping, and logical (row-based) log replication, three named implementation methods with distinct trade-offs [S]** (p175): statement-based forwards the literal SQL statement and breaks on non-determinism (`NOW()`, `RAND()`), auto-increment/order dependence, and non-deterministic triggers/UDFs. WAL shipping reuses the storage engine's own write-ahead log, giving a very compact and exact replication mechanism, but couples replication tightly to storage-engine internals — "if the database changes its storage format from one version to another, it is typically not possible to run different versions of the database software on the leader and the followers" (p175), blocking zero-downtime upgrades. Logical log replication decouples the replication format from storage internals (row-level insert/update/delete records), remaining backward-compatible across software/storage-engine versions and enabling change data capture for external consumers (data warehouses, custom indexes).

**Trigger-based replication, defined by its flexibility-for-overhead trade [S]** (p177): implemented at the application layer via database triggers/stored procedures rather than as a database-engine built-in; needed for partial replication, cross-database-type replication, or custom conflict resolution, but has "greater overheads... and is more prone to bugs and limitations than the database's built-in replication."

**Eventual consistency, precisely scoped [S]** (p177): the temporary inconsistency visible when reading from an asynchronous follower that has fallen behind — "if you stop writing to the database and wait a while, the followers will eventually catch up and become consistent with the leader." "The term eventually is deliberately vague: in general, there is no limit how far a replica can fall behind."

**Read-after-write (read-your-writes) consistency, defined [S]** (p178): "a guarantee that if the user reloads the page, they will always see any updates they submitted themselves." It makes no promise about visibility of other users' writes.

Four named implementation techniques for read-after-write consistency, synthesized from the chapter's own list (p178–179) `[D]`: read user-modifiable data from the leader and everything else from followers; time-since-last-update or replica-lag thresholds to decide leader-vs-follower routing; client-remembered write timestamps (logical or wall-clock) that a chosen replica must have caught up to before serving the read; and datacenter-routing consistency for multi-device cross-device read-after-write.

**Monotonic reads, defined and distinguished from eventual/strong consistency [S]** (p180): "a guarantee that this kind of anomaly does not happen" where "a user sees things moving backwards in time" across successive reads from replicas at different lag. "It's a lesser guarantee than strong consistency, but a stronger guarantee than eventual consistency." Implemented by routing each user consistently to the same replica (e.g. via a hash of user ID).

**Consistent prefix reads, defined via the Mr Poons/Mrs Cake causality example [S]** (p182): the guarantee "that if a sequence of writes happens in a certain order, then anyone reading those writes will see them appear in the same order" — preventing an observer from seeing an answer replicated before the question that caused it, a problem specific to partitioned databases where "different partitions operate independently, so there is no global ordering of writes."

**Multi-leader replication, defined and its core downside named [S]** (p183): more than one node accepts writes, each forwarding its changes to all others, with "each leader simultaneously acts as a follower to the other leaders." Named downside: "the same data may be concurrently modified in two different datacenters, and those write conflicts must be resolved."

**Three named legitimate multi-leader use cases [S]** (p188–191): multi-datacenter operation (each datacenter has a local leader, hiding inter-datacenter latency from users, and tolerating both datacenter outages and inter-datacenter network problems better than single-leader); clients with offline operation (each device is effectively its own "datacenter" with a local leader, syncing asynchronously — calendar apps as the worked example); real-time collaborative editing (Etherpad/Google Docs), which the chapter explicitly reframes as "essentially the same as multi-leader replication between datacenters, taken to the extreme."

**Write conflicts, the biggest multi-leader problem [S]** (p186): illustrated via two users concurrently retitling the same wiki page on different leaders — "this problem does not occur in a single-leader database."

Making conflict detection synchronous would (p187) "lose the main advantage of multi-leader replication: allowing each replica to accept writes independently." Most conflicts are therefore detected only after the fact, asynchronously. `[D]`

**Four named convergent conflict-resolution techniques [S]** (p188): assign each write a unique ID (timestamp/random/UUID/hash) and let the highest-ID write win — "last write wins" (LWW). This technique is "dangerously prone to data loss" (p188). Giving each replica a fixed priority ranking "also implies data loss" (p188); merge values (e.g. alphabetical concatenation); or record the conflict explicitly and resolve it later, possibly via the user.

**Custom conflict resolution's two execution points, on write vs. on read [S]** (p189): on-write handlers (e.g. Bucardo's Perl snippets) run in a background process and cannot prompt a user; on-read approaches (CouchDB's model) surface all conflicting versions to the application at the next read, letting it prompt the user or auto-resolve.

**CRDTs, mergeable persistent data structures, and operational transformation, three named automatic-conflict-resolution research lines [S]** (p189): CRDTs (Riak 2.0) automatically resolve concurrent set/map/list/counter edits via two-way merges; mergeable persistent data structures track history like git and use three-way merges; operational transformation is the algorithm behind Etherpad/Google Docs, designed specifically for concurrently edited ordered lists of characters.

**Replication topology, defined, with three named shapes and their fault-tolerance trade-off [S]** (p191): circular (each node forwards to exactly one other, e.g. MySQL's default), star (one root forwards to all others, generalizable to a tree), and all-to-all (every leader sends to every other). Circular/star topologies are vulnerable to a single node's failure interrupting the whole forwarding chain; all-to-all is more fault-tolerant but can suffer message reordering when some network links are faster than others, with some replication messages effectively overtaking others in transit (p191). `[D]`

**Leaderless replication, defined by its Dynamo lineage and its abandonment of write ordering [S]** (p200): "any replica to directly accept writes from clients," popularized by Amazon's internal Dynamo system and its open-source descendants (Riak, Cassandra, Voldemort — "Dynamo-style"). Unlike a leader, a coordinator (if used) "does not enforce a particular ordering of writes."

**Quorum reads and writes, the chapter's own n/w/r formalism [S]** (p195): "if there are n replicas, every write must be confirmed by w nodes to be considered successful, and we must query at least r nodes for each read... As long as w + r > n, we expect to get an up-to-date value when reading, because at least one of the r nodes we're reading from must be up-to-date." A common configuration sets n odd (3 or 5) and w = r = (n+1)/2 rounded up.

**Six named edge cases where quorums still return stale values despite w+r>n [S]** (p197–198): sloppy quorums breaking the guaranteed w/r node overlap; concurrent writes with no defined "first" requiring a merge, or unsafe timestamp-based LWW under clock skew; a write concurrent with a read leaving it undetermined which value the read returns; a partially-failed write (succeeded on fewer than w replicas) not being rolled back; a node restored from a stale replica dropping the surviving-copy count of a value below w; and generic distributed-timing unluckiness deferred to the linearizability discussion in a later chapter.

**Sloppy quorum and hinted handoff, defined via the borrow-your-neighbor's-couch analogy [S]** (p199): during a network interruption, the database may "accept writes anyway, and write them to some nodes that are reachable but aren't among the n nodes on which the value usually lives" — this is a sloppy quorum. Once connectivity is restored, those borrowed writes are forwarded to their proper "home" nodes: hinted handoff. Explicit consequence: "a sloppy quorum actually isn't a quorum at all in the traditional sense. It's only an assurance of durability."

**The "happens-before" relationship, the chapter's own general definition of concurrency [S]** (p202): "An operation A happens before another operation B if B knows about A, or depends on A, or builds upon A in some way." "In fact, we can simply say that two operations are concurrent if neither happens before the other, i.e. neither knows about the other" (p202). Explicitly decoupled from wall-clock simultaneity, with an explicit analogy to relativistic causality (information cannot outrun the events that caused it).

**Last write wins (LWW), the chapter's own durability-cost warning and its one safe usage pattern [S]** (p202): forces an arbitrary total order via timestamps, discarding all but the highest; "achieves the goal of eventual convergence, but at the cost of durability" since concurrent writes not written last are "silently discarded." The only safe usage the chapter names: write each key exactly once and treat it as immutable thereafter (e.g. UUID-keyed writes in Cassandra), eliminating concurrent updates to the same key entirely.

**Per-key version numbers, the chapter's own single-replica algorithm for tracking siblings [S]** (p205–206): the server increments a per-key version number on every write; a client must read (and receive the current version plus all not-yet-overwritten values) before writing; a write must include the version from that prior read and must merge all values the client received; the server then overwrites everything at or below the submitted version but must keep any value with a higher version as a concurrent sibling.

**Version vectors, the multi-replica generalization [S]** (p207): "a version number per replica as well as per key" — each replica tracks both its own counter and the counters it has seen from every other replica, letting it distinguish overwrites from concurrent siblings without relying on a single global counter. A named variant, the dotted version vector, is used in Riak 2.0.

## 2. WHAT / WHY / WHEN

**WHAT:** the chapter's full taxonomy of replication algorithms — single-leader, multi-leader, and leaderless — organized around one recurring question: given that "all writes must go through the same replica" is not always survivable or fast enough, how does a system reconcile multiple copies of changing data while defining precisely what consistency guarantee (if any) a reader gets. `[D]`

**WHY it matters:** replication's difficulty is entirely about handling *changes* to data over time — "if the data that you're replicating does not change over time, then replication is easy" (p167) — so every technique in the chapter (log formats, quorum parameters, conflict-resolution rules, causality tracking) exists specifically to answer what a reader may legitimately see while writes are still propagating, which is the practical substance behind the abstract term "eventual consistency." `[D]`

**WHEN to choose leader-based vs. multi-leader vs. leaderless, synthesized across the chapter (p167–207):** use single-leader when a simple, strongly-ordered write path within one datacenter is acceptable and read-scaling via asynchronous followers is enough; use multi-leader specifically for multi-datacenter write locality, offline-capable clients, or real-time collaborative editing, accepting the added cost of conflict resolution; use leaderless (Dynamo-style) when high write availability and tunable staleness under partial node failure matter more than any ordering guarantee, and the application can tolerate or explicitly merge sibling values. `[D]`

## 3. Assumptions and prerequisites

- Assumes the dataset is small enough that every node holds a full copy — explicitly deferred to Ch.6 (Partitioning) for datasets too large for one machine. `[S]` (p167)
- Assumes and directly reuses Ch.3's storage-engine internals (LSM-tree compaction log, B-tree write-ahead log) as the substrate for WAL-shipping replication. `[S]` (p176)
- Assumes and directly reuses Ch.4's encoding/decoding vocabulary implicitly (row-based logical logs as a form of change-data-capture encoding), forward-referencing Ch.11 for the full CDC treatment. `[D]`
- Forward-references transaction serializability and snapshot isolation to Ch.7, unreliable-clock and timing-fault detail to Ch.8, and the consensus problem (leader election) and linearizability-quorum edge cases to Ch.9 — all not yet synthesized in this vault. `[D]`

## 4. Mechanism / key steps

**Semi-synchronous replication's self-healing configuration, synthesized from the chapter's own description (p170)** `[D]`: enable synchronous replication on exactly one follower → if that follower becomes unavailable or slow, promote one of the asynchronous followers to synchronous in its place → this guarantees an up-to-date copy always exists on at least two nodes (leader + current synchronous follower) without ever blocking on all followers simultaneously.

**Read-repair mechanism, the chapter's own worked description (p194)** `[D]`: a leaderless read is sent to several replicas in parallel → the client (or coordinator) compares the version numbers/values returned → any replica returning a stale value is sent the newer value directly by the client, on the spot → this only heals values that are actually read, motivating the separate anti-entropy background process for rarely-read keys.

**Sibling-tracking write protocol, the chapter's own five-client shopping-cart worked example (p203–204)** `[D]`: client reads a key, receiving all current (non-overwritten) values plus the latest version number → client merges those values with its own new item → client writes back the merged value tagged with the version number it read → server overwrites every value at or below that version (now known to be merged in) but preserves any value at a higher version as a concurrent sibling → repeat; the true current state is the client-merged union of all outstanding siblings until further overwrites resolve them.

## 5. Trade-offs and limitations

- **Synchronous replication guarantees an up-to-date follower at the cost of write availability; fully asynchronous replication trades durability for continuous write processing (§1, p169–171):** an explicit, direct trade the chapter resolves via the semi-synchronous compromise rather than picking one extreme.
- **WAL-shipping replication is compact and exact but couples the leader and follower to the same storage-engine version, blocking zero-downtime software upgrades; logical log replication decouples this at the cost of a separate log format to maintain (§1, p178–179):** a genuine two-sided trade with no dominant option.
- **Multi-leader replication buys write locality and datacenter/network fault tolerance at the direct cost of needing conflict resolution — a cost the chapter names as often not worth it "within a single datacenter" (§1, p188):** multi-leader is explicitly framed as justified only by specific use cases (multi-datacenter, offline clients, collaborative editing), not a general-purpose upgrade over single-leader.
- **Last write wins achieves convergence but is "dangerously prone to data loss" — a durability cost the chapter treats as acceptable only for caching-like workloads or immutable-key usage patterns (§1, p194, p211–212):** not a neutral default; a deliberate risk trade that must be scoped narrowly.
- **Sloppy quorums increase write availability during network partitions but break the very w+r>n overlap guarantee that quorums are supposed to provide (§1, p207):** an explicit, named contradiction the chapter states outright — "a sloppy quorum actually isn't a quorum at all in the traditional sense."

## 6. Failure modes and edge cases

- **GitHub's primary-key-reuse incident during failover (§1, p173):** a promoted, lagging MySQL follower reused auto-increment primary keys already assigned by the old leader; because those keys were also referenced in a separate Redis store, the collision "resulted in inconsistency between MySQL and Redis, which caused some private data to be disclosed to the wrong users" — a concrete, named cross-system data-loss consequence of naive failover.
- **Split-brain double-shutdown (§1, p173):** the chapter names the risk that a fencing/STONITH mechanism can itself misfire, leaving "both nodes being shut down" — a failure mode of the very safety mechanism meant to prevent split-brain damage.
- **Statement-based replication's non-determinism failures (§1, p176):** `NOW()`/`RAND()` calls, auto-increment/order-dependent statements executed out of order, and non-deterministic triggers/UDFs are each named as concrete ways this replication method silently diverges follower state from the leader.
- **Amazon's shopping-cart conflict-resolution bug (§1, p196):** a real, named production incident where a custom conflict handler preserved added items but not removed items, causing "customers would sometimes see items re-appearing in their cart even though they had previously been removed" — a concrete illustration of how error-prone hand-written conflict resolution is.
- **Union-merge of siblings silently resurrecting deleted items (§1, p215):** if an item is removed from only one sibling cart, a naive union-merge of siblings brings it back — motivating the tombstone marker pattern rather than plain deletion.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the single-leader / multi-leader / leaderless decision framework (§2) is directly reusable as a first-pass architecture decision for any new replicated data store in this vault's projects — start from the use case (write locality need, offline tolerance, staleness tolerance) rather than defaulting to whichever model is most familiar. `[D]`
- **Build:** the semi-synchronous replication configuration pattern (§4, p170) is a directly reusable durability/availability compromise for any leader-based system where full synchronous replication to all followers is judged too fragile.
- **Maintain:** the read-after-write and monotonic-reads implementation techniques (§1, p181–184) are directly reusable operational patterns for diagnosing and fixing "my own write disappeared" or "data went backwards" user-facing bug reports against an asynchronously replicated read path.
- **RCA:** an observed data-loss or reappearing-data incident in a multi-leader or leaderless system is directly diagnosable against the chapter's named conflict-resolution failure patterns (§6) — check for LWW discarding a concurrent write, or a naive union-merge resurrecting a deletion, before assuming an application bug.
- **Optimization:** the quorum n/w/r tuning framework (§1, p202–205) is a directly reusable lever for trading staleness probability against latency and availability in any leaderless-style datastore — favoring smaller w/r for lower latency and higher availability, larger w/r for stronger read-your-writes-like guarantees.

## 8. How to test / verify these claims

- The synchronous-vs-asynchronous replication lag behavior (§1, p169–171) is directly reproducible: configure a database (e.g. PostgreSQL) with one synchronous and one asynchronous follower, kill the asynchronous follower's network connection, and confirm writes still succeed while the synchronous path continues to block correctly if that follower is killed instead.
- The quorum condition w+r>n (§1, p202) is directly testable by construction: set up a 3-node Dynamo-style store (e.g. Cassandra) with n=3, w=2, r=2, take one node offline, and confirm writes and reads both continue to succeed while consistency is (usually) preserved.
- The sibling-version-tracking algorithm (§4, p213–216) is directly reproducible: implement the shopping-cart worked example against a real Riak (or equivalent) cluster, deliberately interleaving concurrent writes from two clients, and confirm that the returned sibling set matches the chapter's Figure 5-13 trace.
- The LWW data-loss claim (§1, p211–212) is directly testable: issue two concurrent writes to the same key in a Cassandra table with default LWW conflict resolution, and confirm one write is silently discarded rather than surfaced as a conflict.

## 9. Cross-references

- Directly extends Ch.3's storage-engine log mechanics (LSM-tree, B-tree WAL) as the concrete substrate for WAL-shipping replication — no contradiction found. `[D]`
- Directly extends Ch.4's discussion of backward/forward compatibility: WAL shipping's storage-engine coupling is the same compatibility problem Ch.4 discusses in the abstract, now applied specifically to replication protocols across software versions. `[D]`
- Forward-references (not yet synthesized in this vault): Ch.6 (partitioning of datasets too large for one machine), Ch.7 (transactions, snapshot isolation, and the consistent-prefix-reads causal-transaction connection), Ch.8 (unreliable clocks and network timing faults underlying failover-timeout and LWW-clock-skew issues), Ch.9 (leader-election consensus and linearizability/quorum edge cases), and Ch.11 (full change-data-capture treatment building on this chapter's logical-log replication).
- No contradiction found with any already-synthesized source in this vault.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 5-1 through 5-14 (leader/follower architecture, synchronous/asynchronous timing diagrams, replication topology diagrams, quorum diagrams, causal-dependency graphs) | Structure and content described narratively above where load-bearing (§1, §4); full diagram layouts not reproduced verbatim. |
| Full numbered reference list (56 references) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. the GitHub incident, the Amazon shopping-cart bug) are captured inline in §1/§6 with attribution context. |
| Detailed vendor-specific configuration syntax (PostgreSQL `synchronous_commit`, Cassandra consistency-level keywords, Riak bucket properties, etc.) | Chapter discusses these at the conceptual level only; this note preserves the conceptual mechanism, not platform-specific configuration commands. |
| The "Version vectors and vector clocks" terminology sidebar's full nuance (p217) | The client-server vs. peer-to-peer distinction is noted in §1 but the chapter itself explicitly declines to go into detail ("We won't go into the details"), so this note does not manufacture detail beyond that. |
