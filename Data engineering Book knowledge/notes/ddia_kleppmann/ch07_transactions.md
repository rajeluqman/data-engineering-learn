# Ch.7 — Transactions

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 235–286 (52 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[U]` unresolved

---

## 1. Concepts and definitions

**Transaction, defined and its purpose named directly [S]** (p236): "a way for an application to group several reads and writes together into a logical unit." Either "the entire transaction succeeds (commit) or it fails (abort, rollback)." Their purpose: "to simplify the programming model for applications accessing a database," letting applications "ignore certain potential error scenarios and concurrency issues, because the database takes care of them instead."

**ACID, the four letters individually redefined by the chapter with explicit caveats [S]** (p238–241): Atomicity is "not about concurrency" — it "describes what happens if a client wants to make several writes, but a fault occurs after some of the writes have been processed," with the guarantee being abortability: on failure, "the database must discard or undo any writes it has made so far." Consistency (p238–239) is "terribly overloaded" across three unrelated meanings (replica consistency, CAP-theorem linearizability, ACID's own "application-specific notion of the database being in a 'good state'") — the chapter's explicit verdict: "consistency (in the ACID sense) is a property of the application," not the database, "the letter C doesn't really belong in ACID." Isolation (p239–240) means "concurrently executing transactions are isolated from each other," formalized classically as serializability — "each transaction can pretend that it is the only transaction running on the entire database" — though "in practice, serializable isolation is rarely used" for performance reasons. Durability (p240) is "the promise that once a transaction has committed successfully, any data it has written will not be forgotten," acknowledging "perfect durability does not exist."

**ACID's marketing-term critique, an explicit named verdict [S]** (p237): "in practice, one database's implementation of ACID does not equal another's implementation."

Today (p238), when a system claims to be ACID compliant, it's unclear what guarantees you can actually expect — the chapter's own conclusion is that ACID has become mostly a marketing term. `[D]`

BASE (Basically Available, Soft state, Eventual consistency) is named even vaguer (p238): its only sensible definition is simply not being ACID. `[D]`

**Replication's durability risks, six named concrete failure scenarios undermining a naive "just replicate" assumption [S]** (p240–241): a correlated fault (power outage, a crash-triggering bug) can take down all replicas simultaneously, losing in-memory-only data; asynchronous replication can lose recent writes when a leader fails; SSDs can silently violate their own guarantees on sudden power loss, "even fsync isn't guaranteed to work correctly"; storage-engine/filesystem interactions can corrupt files after a crash; data can gradually corrupt on disk undetected, contaminating replicas and recent backups alike; and a powered-off SSD can begin losing data within weeks depending on temperature.

**Single-object vs. multi-object operations, precisely distinguished [S]** (p243–246): multi-object transactions coordinate writes across several rows/documents/records — needed to keep foreign-key references valid, keep denormalized data in sync (the chapter's own worked email-unread-counter example), and keep secondary indexes consistent with the underlying data. Single-object atomicity/isolation is what "storage engines almost universally aim to provide" even without full transactions — implemented via a crash-recovery log (atomicity) and a per-object lock (isolation) — and single-object operations like atomic increment or compare-and-set are explicitly warned against being marketed as "lightweight transactions" or "ACID," since "a transaction is usually understood as a mechanism for grouping multiple operations on multiple objects into one unit of execution."

**Read committed, the chapter's own two-guarantee definition [S]** (p246–248): "you will only see data that has been committed (no dirty reads)" and "you will only overwrite data that has been committed (no dirty writes)." Dirty writes are prevented via row-level locks held until commit/abort; dirty reads are prevented not via read locks (which would let one long write block many reads) but by the database remembering both the old committed value and the new uncommitted value, serving the old value to concurrent readers until commit.

**Read skew (non-repeatable reads), defined via Alice's two-account worked example [S]** (p251): reading account balances at different points mid-transfer makes it "appears as though she only has a total of $900 in her accounts — it seems that $100 have vanished into thin air."

Read skew is considered acceptable under read committed isolation (p251), since "the account balances that Alice saw were indeed committed at the time when she read them" — but it is unacceptable for two named use cases: backups (a copy spanning hours can mix old and new data, creating a permanently inconsistent restore point) and long-running analytic/integrity-check queries, which "are likely to return nonsensical results if they observe parts of the database at different points in time" (p251).

**Snapshot isolation (MVCC), the chapter's own definition [S]** (p252): "each transaction reads from a consistent snapshot of the database, that is, all the data that was committed in the database at a particular point in time."

Its performance mantra (p252): "a key principle of snapshot isolation is readers never block writers, and writers never block readers."

Implemented by tagging every row with `created_by`/`deleted_by` transaction IDs and applying four explicit visibility rules (p254): ignore writes from transactions still in-progress at the reader's start time; ignore writes from aborted transactions; ignore writes from transactions with a later ID than the reader; show everything else. `[D]`

**The "repeatable read" naming confusion, an explicit named historical accident [S]** (p254–255): PostgreSQL and MySQL call their snapshot isolation implementation "repeatable read" purely to claim SQL-standard compliance, since the standard predates snapshot isolation and only defines a vaguer, ambiguous "repeatable read." Oracle calls its (weaker) snapshot isolation "serializable"; IBM DB2 uses "repeatable read" to mean actual serializability. Explicit verdict: "nobody really knows what repeatable read means."

**Lost update, defined via the read-modify-write-cycle pattern, with four named prevention techniques [S]** (p255–258): occurs when "two transactions do this concurrently, one of the modifications can be lost, because the second write does not include the first modification." Techniques: atomic write operations (best when applicable, e.g. `UPDATE counters SET value = value + 1`, implemented via cursor-stability locking); explicit application-level locking (`SELECT ... FOR UPDATE`) when built-in atomic operations aren't expressive enough; automatic lost-update detection (available in PostgreSQL repeatable read, Oracle serializable, SQL Server snapshot isolation, but explicitly not in MySQL/InnoDB repeatable read); and compare-and-set, with an explicit warning that it is only safe "if the database allows the WHERE clause to read from an old snapshot" it can silently fail to prevent the very race it's meant to stop.

**Write skew, defined via the on-call-doctors worked example [S]** (p260): "it is neither a dirty write nor a lost update, because the two transactions are updating two different objects"

Write skew generalizes lost update (p261): "you can think of write skew as a generalization of lost update. Write skew can occur if two transactions read the same objects, and then update some of those objects"

Four named real-world instances beyond the doctors example, synthesized from the chapter's own list (p263–264) `[D]`: meeting-room double-booking, multiplayer-game piece collisions, username-claiming races, and double-spending via concurrently-inserted spending items that individually look safe.

**Phantoms, the mechanism underlying write-skew's hardest cases [S]** (p264): "a write in one transaction changes the result of a search query in another transaction, is called a phantom"

Distinguished from the doctors case (p264): when the anomaly involves checking for the absence of rows, a row-level lock has nothing to attach to, since there is no existing row to lock — this is what makes phantom-driven write skew categorically harder than row-level lost updates. `[D]`

**Materializing conflicts, an explicit last-resort technique with a named ugliness verdict [S]** (p264): artificially pre-creating lock-target rows (e.g. a room × 15-minute-slot table) purely so phantoms have something concrete to lock. "It can be hard and error-prone to figure out how to materialize conflicts, and it's ugly to let a concurrency control mechanism leak into the application data model."

"For those reasons, materializing conflicts should be considered a last resort if no alternative is possible" (p264).

**Serializability, the chapter's own strongest-isolation definition [S]** (p265): "the end result is the same as if they had executed one at a time, serially, without any concurrency." Thus "the database prevents all possible race conditions" (p265).

The three named implementation techniques (p265): literal serial execution; two-phase locking (2PL), "for several decades... the only viable option"; and optimistic techniques such as serializable snapshot isolation (SSI).

**Actual serial execution, its two enabling changes and its stored-procedure requirement [S]** (p266–267): made viable circa 2007 by cheap-enough RAM to keep the active dataset in memory, plus the recognition that OLTP transactions are typically short. Because network round-trips between an interactive client and server would leave a single thread idle most of the time, serial-execution systems (VoltDB/H-Store, Redis, Datomic) require the entire transaction be submitted up front as a stored procedure rather than run interactively.

**Serial execution's partitioning-throughput trade-off, an explicit named hard limit [S]** (p269): partitioning lets each CPU core own its own partition and transaction thread, scaling linearly for single-partition transactions, but cross-partition transactions have additional coordination overhead.

VoltDB is named as achieving only (p269) "about 1,000 cross-partition writes per second."

This is (p269) "orders of magnitude below its single-partition transaction throughput, and cannot be increased by adding more machines"

**Two-phase locking (2PL), defined by its stronger-than-dirty-write-prevention lock rules [S]** (p270): readers use shared locks, writers use exclusive locks, and critically "a reader must also block a writer, and vice versa" — the direct inverse of snapshot isolation's mantra. The "two-phase" name comes from lock acquisition happening throughout execution (phase one) and all locks releasing together only at commit/abort (phase two). `[D]`

**2PL's named performance downside and its deadlock cost [S]** (p271): "transaction throughput and response times of queries are significantly worse under two-phase locking than under weak isolation." This is due to acquisition/release overhead and, more importantly, reduced concurrency — one slow or lock-heavy transaction can stall a whole queue with no upper wait bound, since traditional databases don't limit transaction duration. `[D]`

Deadlocks (p272) "occur much more frequently under 2PL serializable" — each one requiring a full transaction retry. `[D]`

**Predicate locks and their practical index-range-lock approximation [S]** (p272): a predicate lock conceptually attaches to "all objects that match some search condition," including objects that don't yet exist, solving the phantom problem.

Unfortunately (p273), "predicate locks do not perform well." The practical compromise, index-range locking, deliberately over-approximates the predicate by attaching a shared lock to an index entry or range — safe, "because any write that matches the original predicate will definitely also match the approximations" (p273) — falling back to a full-table lock if no suitable index exists.

**Serializable snapshot isolation (SSI), defined as an optimistic technique layered on ordinary snapshot isolation [S]** (p274): "optimistic in this context means that instead of blocking if something"

potentially dangerous happens, transactions continue anyway, in the hope that everything will turn out alright (p275). `[D]`

When a transaction wants to commit (p274), the database checks whether isolation was violated; if so, the transaction is aborted and has to be retried. First described in 2008; used in PostgreSQL (since 9.1) and, distributed, in FoundationDB.

**SSI's two named conflict-detection mechanisms [S]** (p276–278): detecting stale MVCC reads (a transaction's snapshot ignored a write that has since committed, invalidating any premise built on that read — deferred to commit time rather than the read itself, since a read-only transaction never needs to abort for this reason) and detecting writes that affect prior reads (index-range "lock" entries act as tripwires notifying, not blocking, other transactions when their previously-read data is later modified — whichever transaction commits first wins, the other aborts). `[D]`

**SSI's performance profile relative to the other two serializable techniques, an explicit named comparison [S]** (p278): "one transaction doesn't need to block waiting for locks held by another transaction" — readers and writers never block each other, giving predictable low-variance query latency.

Unlike serial execution (p279), SSI is not capped at one CPU core, since FoundationDB distributes conflict detection across machines. Its main sensitivity: high abort rates under long-running read-write transactions, since more time spent means more opportunity to conflict — but "SSI is probably less sensitive to slow transactions than two-phase locking or serial execution" (p279).

## 2. WHAT / WHY / WHEN

**WHAT:** the chapter's full taxonomy of transactional guarantees (ACID, precisely redefined) and concurrency-control mechanisms — from the weakest practical isolation level (read committed) through snapshot isolation to full serializability via three distinct implementation strategies — organized around a single recurring question: which named race conditions (dirty read, dirty write, read skew, lost update, write skew, phantom) does a given isolation level actually prevent. `[D]`

**WHY it matters:** transactions exist purely to let application developers "pretend that certain concurrency problems and certain kinds of hardware and software fault don't exist" (p279), collapsing a large space of partial-failure and race-condition bugs into a single "abort and retry" pattern — but the chapter's central warning is that most systems in practice use isolation levels weaker than full serializability, so knowing exactly which anomalies a chosen isolation level does *not* prevent is a prerequisite for reasoning correctly about an application's actual safety, not an academic nicety. `[D]`

**WHEN to accept weaker isolation vs. pay for serializability, synthesized across the chapter (p246–284):** read committed suffices when only dirty reads/writes are a risk and the application never makes a decision based on a query result that must still hold true at commit time; snapshot isolation is right for long-running read-only workloads (backups, analytics) and moderate write conflict, but explicitly does not protect against write skew or phantom-driven anomalies (double-booking, double-spending, uniqueness-adjacent races) — those require either explicit `SELECT FOR UPDATE` locking, a unique constraint if the invariant reduces to one, or true serializable isolation (2PL, serial execution, or SSI) when the invariant spans multiple objects/rows.

## 3. Assumptions and prerequisites

- Directly extends Ch.5's replication material for the durability discussion (asynchronous replication's write-loss risk) and for conflict resolution's connection to lost updates in multi-leader/leaderless systems. `[S]` (p241, p258)
- Directly extends Ch.6's partitioning material for the serial-execution throughput discussion (single-partition vs. cross-partition transaction cost) and the secondary-index cross-partition coordination cost. `[S]` (p271)
- Directly extends Ch.3's storage-engine internals (write-ahead logging for atomicity, B-tree structures reused by append-only/copy-on-write MVCC implementations like CouchDB/Datomic/LMDB). `[S]` (p236, p254–255)
- Forward-references distributed transactions, two-phase commit (2PC, explicitly distinguished from 2PL), and generalizing single-node serializability techniques to distributed databases, all to Ch.9 — not yet synthesized in this vault. `[D]`

## 4. Mechanism / key steps

**Snapshot isolation's MVCC visibility check, the chapter's own worked PostgreSQL-style description (p252–253)** `[D]`: every row carries `created_by` and `deleted_by` transaction-ID fields, never overwritten in place — an update becomes an internal delete-plus-create pair → at transaction start, the database snapshots the set of in-progress transaction IDs → on read, a row is visible only if its creator committed before the reader started and (if deleted) its deleter had not committed before the reader started → garbage collection later reclaims rows no longer visible to any active transaction.

**Two-phase locking's shared/exclusive lock protocol, the chapter's own worked description (p273)** `[D]`: a transaction wanting to read acquires a shared lock (compatible with other shared locks, blocked by any exclusive lock); a transaction wanting to write acquires an exclusive lock (blocked by any existing lock, shared or exclusive); a read-then-write transaction upgrades shared to exclusive; every lock, once acquired, is held until the transaction's final commit or abort — never released early — which is the "two-phase" structure (acquisition phase, then release phase).

**SSI's dual-detection commit-time check, the chapter's own worked two-doctor example (p281–283)** `[D]`: a transaction reads from an ordinary MVCC snapshot as usual → the database separately tracks (a) which in-progress transactions' writes were ignored due to visibility rules, and (b) which other transactions have read data that this transaction's own writes are now modifying → at commit time, if either tracked condition indicates the read transaction's premise may now be false, the transaction is aborted and must be retried → only transactions that pass this check are allowed to commit, guaranteeing the result matches some serial execution order.

## 5. Trade-offs and limitations

- **Weak isolation levels (read committed, snapshot isolation) perform far better than serializable isolation but leave the application responsible for detecting and preventing lost updates, write skew, and phantoms (§1, p249, p260–265):** the chapter frames this as the central practical trade-off of the entire chapter — performance bought at the cost of correctness reasoning being pushed onto the application developer.
- **Two-phase locking guarantees full serializability but at a severe, unbounded-latency performance cost under contention, with deadlocks adding further wasted retry work (§1, p273–274):** a direct, named cost the chapter credits as the historical reason weak isolation levels proliferated despite their correctness gaps.
- **Serial execution eliminates concurrency-control overhead entirely but caps throughput at a single CPU core (or requires perfect partitioning), and cross-partition transactions remain orders of magnitude slower than single-partition ones (§1, p267, p271):** the trade-off is structural, not tunable — it only works when the workload is genuinely small-and-fast or cleanly partitionable.
- **Serializable snapshot isolation avoids blocking entirely (unlike 2PL) and isn't capped at one core (unlike serial execution), but its abort rate rises with transaction duration and contention, making it a poor fit for long-running read-write transactions (§1, p284–285):** SSI is explicitly framed as the newest and most promising of the three, but not a strictly dominant replacement — its performance is workload-dependent in a different way than the other two.

## 6. Failure modes and edge cases

- **Read skew corrupting backups and analytic queries, a concrete named consequence distinct from the transient case (§1, p250):** unlike Alice's temporarily-vanished $100 (which reappears on refresh), a backup or long-running integrity check that captures pre- and post-transfer state simultaneously bakes the inconsistency in permanently — "if you need to restore from such a backup, the inconsistencies... become permanent."
- **Compare-and-set silently failing to prevent lost updates on a stale snapshot (§1, p258):** "if the database allows the `WHERE` clause to read from an old snapshot, this statement may not prevent lost updates, because the condition may be true even though another concurrent write is occurring" — a concrete, named case where a technique marketed as a safe primitive is unsafe depending on implementation.
- **Phantom-driven write skew defeating row-level locking entirely (§1, p264–265):** in the meeting-room, username-claiming, and double-spending examples, the anomaly involves checking for the *absence* of a matching row, so there is no existing row for `SELECT FOR UPDATE` to lock — a structurally different and harder failure mode than the doctors example, requiring index-range locks or materialized conflict rows instead.
- **Retrying a transaction that actually succeeded, causing a duplicate side effect (§1, p249, the abort-handling discussion):** if the network fails while the server is acknowledging a successful commit, the client retries a transaction that already took effect — "unless you have an additional application-level deduplication mechanism in place," this silently double-applies the operation (e.g. sending a duplicate email, deferred explicitly to Ch.9's 2PC discussion for cross-system side effects).
- **Retrying under overload making things worse, a named anti-pattern [S]** (p246): "if the error is due to overload, retrying the transaction will make the problem worse, not better." This motivates limited retries, exponential backoff, and distinguishing overload errors from other transient errors. `[D]`

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the isolation-level decision framework (§2) is directly reusable for choosing a transaction isolation level for any new schema/workload in this vault's projects — explicitly check whether the application's invariants span multiple rows (write-skew risk) before assuming snapshot isolation or read committed is sufficient. `[D]`
- **Build:** the atomic-operation-first hierarchy (§1, p255–256: atomic operations > explicit locking > automatic lost-update detection > compare-and-set with its stated caveat) is a directly reusable decision order for implementing any read-modify-write cycle safely.
- **Maintain:** the "data outlives code"-adjacent replication-durability checklist (§1, p240–241) is a directly reusable pre-mortem checklist when auditing whether a system's durability claims actually hold under correlated faults, SSD power loss, or silent disk corruption.
- **RCA:** an observed "impossible" data inconsistency (e.g. an invariant spanning multiple rows silently violated, or denormalized data drifting out of sync) is directly diagnosable against the write-skew and phantom patterns (§1, §6) before assuming an application logic bug — check whether the isolation level in use actually prevents that specific anomaly class.
- **Optimization:** the three-way serializability-technique trade-off (§1, §5: serial execution vs. 2PL vs. SSI) is a directly reusable framework for choosing a concurrency-control strategy under a known workload shape — favor serial execution for small in-memory partitionable workloads, SSI for read-heavy or low-contention workloads needing full serializability without 2PL's blocking cost, and 2PL only when neither alternative is available or contention is genuinely severe enough that optimistic retry overhead would dominate.

## 8. How to test / verify these claims

- The lost-update race condition (§1, p239, Figure 7-1) is directly reproducible: run two concurrent read-modify-write counter-increment transactions against a database at read committed isolation and confirm the final counter value undercounts the true number of increments.
- The read-skew anomaly (§1, p249–250) is directly reproducible: run a concurrent funds-transfer transaction against a two-account balance read at read committed isolation, timing the reads to straddle the transfer, and confirm the observed total is transiently wrong.
- The write-skew anomaly (§1, p260–261) is directly reproducible using the chapter's own doctors example: run two concurrent "go off-call if 2+ on call" transactions under snapshot isolation and confirm both succeed, leaving zero doctors on call.
- The automatic lost-update detection claim (§1, p256) is directly testable by comparing behavior across databases: run the same concurrent counter read-modify-write cycle under PostgreSQL's repeatable read (should abort one transaction) versus MySQL/InnoDB's repeatable read (should silently lose the update, per the chapter's explicit claim).
- The SSI abort-under-contention claim (§1, p283) is directly testable: run many concurrent conflicting read-write transactions against a PostgreSQL database at serializable isolation (its SSI implementation) and measure the abort rate as contention increases.

## 9. Cross-references

- Directly extends Ch.5's replication durability and conflict-resolution material — read committed/snapshot isolation lost-update prevention explicitly does not carry over to multi-leader/leaderless replicated systems, which instead rely on sibling-merging (Ch.5's own mechanism). No contradiction found. `[S]`
- Directly extends Ch.6's partitioning material for the serial-execution and cross-partition transaction cost discussion. No contradiction found. `[S]`
- Directly extends Ch.3's storage-engine internals (WAL for atomicity; B-tree append-only/copy-on-write variants reused by MVCC implementations). No contradiction found. `[S]`
- Forward-references (not yet synthesized in this vault): Ch.9 for distributed transactions, two-phase commit (2PC, explicitly distinguished from 2PL), and generalizing this chapter's single-node serializability techniques across multiple nodes; Ch.8 for network-unreliability context underlying the "retry after ambiguous failure" discussion.
- No contradiction found with any already-synthesized source in this vault.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 7-1 through 7-11 (race-condition timing diagrams, MVCC row-versioning diagram, index-range-lock and SSI conflict-detection diagrams) | Structure and content described narratively above where load-bearing (§1, §4); full diagram layouts and exact timing traces not reproduced verbatim. |
| Full worked SQL examples (Examples 7-1, 7-2: `SELECT ... FOR UPDATE` locking patterns for the multiplayer-game and meeting-room cases) | Mechanism and intent captured in prose in §1/§4; the literal SQL statements are illustrative syntax, not separately reproduced in full given their length. |
| Full numbered reference list (~54 references) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. the SSD power-fault research, the System R/ACID coinage history) are captured inline in §1 with attribution context. |
| Detailed vendor-by-vendor isolation-level compatibility matrix beyond the specific named examples already captured (e.g. exhaustive cross-database comparison tables cited to reference [22]) | The chapter itself defers full detail to that external reference; this note captures only the chapter's own named vendor examples (Oracle, PostgreSQL, MySQL/InnoDB, SQL Server, DB2), not a manufactured exhaustive matrix. |
