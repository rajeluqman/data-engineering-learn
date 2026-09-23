# Ch.8 — The Trouble with Distributed Systems

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 287–332 (46 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[U]` unresolved

---

## 1. Concepts and definitions

**Partial failure, defined as the core distinguishing feature of distributed systems [S]** (p288): "there may well be some parts of the system that are broken in some unpredictable way, even though other parts of the system are working fine." Explicitly contrasted with single-computer determinism: a single machine is designed to "hide the fuzzy physical reality" and "either it works, or it doesn't," whereas "partial failures are non-deterministic: if you try to do anything involving multiple nodes and the network, it may sometimes work and sometimes unpredictably fail... you may not even know whether something succeeded or not."

**Supercomputers vs. internet-service distributed systems, an explicit named contrast in fault-handling philosophy [S]** (p289–290): a supercomputer "deals with partial failure by letting it escalate into total failure — if any part of the system fails, just let everything crash," checkpointing and restarting the whole cluster. Internet services cannot do this ("making the service unavailable... is not acceptable") and must instead build fault tolerance directly into software, running on commodity (higher-failure-rate) hardware at a scale where "it is reasonable to assume that something is always broken."

**Building reliable systems from unreliable components, an old and explicitly bounded idea [S]** (p291): named examples — error-correcting codes over a noisy channel, and TCP's reliable transport built on unreliable IP (retransmission, deduplication, reordering). Explicit limit: "there is always a limit to how much more reliable it can be" — TCP "cannot magically remove delays in the network."

**Asynchronous packet networks, defined by their total absence of delivery guarantees [S]** (p291–292): "the network gives no guarantees as to when it will arrive, or whether it will arrive at all." Six named indistinguishable failure modes when a request goes unanswered (p292): request lost, request queued, remote node failed, remote node temporarily unresponsive (e.g. long GC pause), response lost, or response delayed — "all of the issues above are indistinguishable in an asynchronous network."

**Timeout, defined as the practical (imperfect) response to this indistinguishability [S]** (p293): "after some time you give up waiting and assume that the response is not going to arrive."

Even so (p293), when a timeout occurs, you still don't know whether the remote node got your request or not. `[D]`

**Network faults in practice, concrete measured evidence against a "networks are basically reliable" assumption [S]** (p293–294): one medium-datacenter study found "about 12 network faults per month, of which half disconnected a single machine, and half disconnected an entire rack"; redundant networking gear "doesn't reduce faults as much as you'd hope, since it doesn't guard against human error," a named major outage cause; a documented case where a switch software upgrade "could trigger a network topology reconfiguration, during which network packets could be delayed for more than a minute"; and a documented asymmetric fault where "a network interface... sometimes drops all inbound packets, but sends outbound packets successfully."

**Network partition, precisely scoped and explicitly disambiguated from Ch.6's usage [S]** (p293): "when one part of the network is cut off from the rest due to a network fault, that is sometimes called a network partition or netsplit." The chapter deliberately prefers the term "network fault" throughout, to avoid confusion with partitions (shards) of a storage system as discussed in Ch.6. `[D]`

**Fault detection's limited, partial feedback channels, four named mechanisms with explicit caveats [S]** (p295–296): OS-level TCP RST/FIN on a dead process (but no way to know how much of an in-flight request was processed); a crash-notification script cooperating with a still-running OS (e.g. HBase); direct query of network-switch management interfaces (unavailable over the internet or in shared datacenters); and router-level ICMP Destination Unreachable, itself "subject to the same limitations as other participants of the network." Explicit synthesis: "even if TCP acknowledges that a packet was delivered, the application may have crashed before handling it. If you want to be sure that a request was successful, you need a positive response from the application itself."

**Timeout-length trade-off, an explicit named dilemma with a cascading-failure risk [S]** (p295): "a long timeout means a long wait until a node is declared dead" and "a short timeout detects faults faster, but carries a higher risk of incorrectly declaring a node dead."

Prematurely declaring nodes dead shifts load onto remaining nodes, and can even cause a cascading failure — in the extreme case, all nodes may declare each other dead, and everything stops working (p295). `[D]`

**The bounded-delay thought experiment and why real systems lack it [S]** (p295): if a network guaranteed max delay `d` and a non-failed node guaranteed response time `r`, a `2d+r` timeout would be provably correct. But "most systems we work with have neither of those guarantees: asynchronous networks have unbounded delays" — making timeout choice fundamentally experimental rather than provably correct. `[D]`

**Network congestion and queueing, five named concrete sources of variable delay [S]** (p296): switch-level output-queue buildup when multiple senders target one destination — packets dropped and re-sent if the queue fills, "even though the network is functioning fine"; OS-level request queueing when all CPU cores are busy; virtual-machine-monitor buffering during a paused VM's CPU-sharing turn; TCP's own flow-control (congestion avoidance) queueing at the sender; and TCP's retransmission-timeout delay, invisible to the application except as added latency. `[D]`

**Synchronous (circuit-switched) vs. asynchronous (packet-switched) networks, an explicit named architectural contrast [S]** (p300–301): a telephone-network circuit reserves "a fixed, guaranteed amount of bandwidth... along the entire route," giving a "bounded delay" with no queueing; datacenter/internet packet networks instead let TCP "opportunistically use whatever network bandwidth is available." Named reason packet switching wins for general use: circuits are "optimized for" constant-bitrate traffic (audio/video calls) but waste capacity on bursty transfers (web pages, email, files) where guessing a bandwidth allocation upfront is either wasteful (too low) or infeasible (too high).

**Latency as a consequence of dynamic resource partitioning, an explicit general framing [S]** (p300): static partitioning (a dedicated circuit, a dedicated CPU allocation) buys predictable latency at the cost of utilization — "your circuit is still allocated the same fixed amount of bandwidth as when the wire is fully utilized" even when otherwise idle.

Dynamic partitioning (TCP's opportunistic sharing, OS thread scheduling) buys better utilization (and thus lower cost per byte/cycle) at the cost of variable delay. Explicit verdict (p300): "variable delays in networks are not a law of nature, but simply the result of a cost-benefit trade-off."

**Time-of-day clocks vs. monotonic clocks, precisely and separately defined [S]** (p302): time-of-day clocks (`clock_gettime(CLOCK_REALTIME)`, `System.currentTimeMillis()`) report wall-clock time since an epoch, synchronized via NTP, but "may be forcibly reset and appear to jump back to a previous point in time" — making them "unsuitable for measuring elapsed time." Monotonic clocks (`CLOCK_MONOTONIC`, `System.nanoTime()`) are "guaranteed to always move forwards," suited to measuring durations, but their absolute value "is meaningless" and cross-machine comparison is invalid.

**Clock synchronization's practical unreliability, eight named concrete failure sources [S]** (p303–304): quartz drift (Google assumes 200ppm, ~17s/day if resynced only daily); forced resets on excessive NTP-server divergence causing visible time jumps; silent firewall-blocked NTP going unnoticed; NTP accuracy itself bounded by network delay (measured ~35ms minimum over the internet, spiking to ~1s under congestion); misconfigured NTP servers reporting wildly wrong time (mitigated by majority-outlier rejection across multiple servers); leap seconds breaking systems not designed for a 59- or 61-second minute (mitigated by smearing the adjustment gradually); VM clock virtualization causing sudden forward jumps after a paused VM resumes; and fully untrusted hardware clocks on user-controlled devices. `[D]`

**Last write wins (LWW) using time-of-day clocks, an explicit named danger with three concrete failure mechanisms [S]** (p306, cross-referenced from Ch.5): a worked multi-leader example shows a causally-later write (client B's increment, dependent on client A's prior write) receiving an earlier timestamp due to clock skew — "in effect, client B's increment operation has been lost."

Three named LWW failure mechanisms, synthesized from the chapter's own list (p306) `[D]`: writes can silently and permanently disappear behind a fast clock until skew elapses; LWW cannot distinguish sequential-but-non-concurrent writes from truly concurrent ones without additional causality tracking (version vectors); and two nodes can independently generate identical timestamps, requiring an arbitrary tiebreaker that can itself violate causality.

**Logical clocks, defined as the safer alternative to physical time-of-day clocks for ordering [S]** (p306): "based on incrementing counters rather than an oscillating quartz crystal," logical clocks "do not measure the time of day, only the relative ordering of events." Time-of-day clocks are correspondingly renamed "physical clocks" in explicit contrast.

**Clock confidence intervals, defined and Google's TrueTime API named as the sole mainstream exception [S]** (p307): "it doesn't make sense to think of a clock reading as a point in time — it is more like a range of times, within a confidence interval" Most systems (e.g. `clock_gettime()`) don't expose this uncertainty at all; TrueTime explicitly reports `[earliest, latest]` bounds, and Spanner uses non-overlapping confidence intervals plus a deliberate commit-wait (equal to the interval width) to guarantee cross-datacenter transaction timestamps reflect true causal order — achievable in practice only via dedicated GPS/atomic clock hardware per datacenter (~7ms synchronization). `[D]`

**Process pauses, defined via a broken leader-lease worked example, with seven named concrete causes [S]** (p310): a lease-holding node believes it's still leader based on a local clock comparison to a lease-expiry time, but an unexpected pause (e.g. 15 seconds) can let the lease expire mid-request without the thread noticing until its next loop iteration — "by which time it may have already done something unsafe by processing the request."

Seven named causes of arbitrary pause length, synthesized from the chapter's own list (p310–312) `[D]`: stop-the-world garbage collection (sometimes minutes, even in "concurrent" collectors); VM suspend/resume (live migration); laptop lid-close suspension; OS/hypervisor context-switch preemption (including cross-VM steal time); synchronous disk I/O blocking (compounded by unexpected access like lazy classloading, or network-backed disks); OS-level paging/swapping (extreme case: thrashing); and a Unix `SIGSTOP` signal.

**Hard real-time systems, defined and explicitly distinguished from casual "real-time" usage, with a named cost trade-off [S]** (p312): systems with a hard response deadline whose violation "may cause serious damage" (aircraft, rockets, robots) require an entire real-time-aware software stack (RTOS, documented worst-case execution times, restricted/disallowed dynamic allocation).

Real-time is explicitly not the same as high performance (p312) `[D]`: real-time systems may have lower throughput, since they have to prioritize timely responses above all else, at the cost of a large amount of additional engineering work.

**GC-pause mitigation techniques, two named practical (non-real-time) approaches [S]** (p312): treating a GC pause like a brief planned outage, warned in advance so traffic can be shifted away before the pause and resumed after (used in latency-sensitive financial trading systems); and periodically restarting processes before long-lived-object accumulation forces a full GC, shifting traffic away first like a rolling upgrade. `[D]`

**Fencing tokens, defined via a broken-lock worked example (the file-corruption bug named as a real HBase issue) [S]** (p315–316): a monotonically increasing number issued alongside every granted lock/lease; the protected resource itself — not the client — must check that an incoming write's token is not lower than the highest token it has already processed, rejecting stale writes from a client that wrongly believes it still holds the lock after a pause caused its lease to expire and be reassigned.

Explicit requirement (p317): "this requires the resource itself to take an active role in checking tokens, and rejecting any writes on which the token has gone backwards"

It is not sufficient to rely on clients checking their lock status themselves (p317). `[D]`

**Byzantine faults, precisely scoped and explicitly excluded from the book's default assumption [S]** (p317): a Byzantine fault is when "a node sends untrue messages to other nodes" — lying, not merely being slow or silent.

The book's standing assumption (p317): "nodes are unreliable but honest: they may be slow or never respond (due to a fault), and their state may be outdated (due to a GC pause or network delays), but we assume that if a node does respond, it is telling the"

Byzantine fault tolerance is named relevant only in specific contexts (aerospace radiation-induced corruption, multi-organization mutually-distrusting systems like blockchain) and explicitly judged impractical for ordinary server-side systems, since a software bug shared across all identically-deployed nodes cannot be defended against by BFT algorithms regardless. `[D]`

**System models, three named timing models and three named node-failure models, explicitly composed for practical use [S]** (p320–321): timing models — synchronous (bounded delay/pause/clock error, unrealistic), partially synchronous, which "behaves like a synchronous system most of the time" but occasionally exceeds its bounds arbitrarily, and asynchronous (no timing assumptions at all, no clock, "very restrictive"). Node-failure models — crash-stop (a node that fails never returns), crash-recovery (nodes may crash and later resume, with stable storage surviving but in-memory state lost), and Byzantine (arbitrary, including malicious behavior). Explicit verdict (p321): "the partially synchronous model with crash-recovery faults is generally the most useful model" for real systems.

**Safety vs. liveness properties, precisely and formally distinguished via a fencing-token example [S]** (p322): safety properties (uniqueness, monotonic sequence for fencing tokens) can be pinned to "a particular point in time at which it was broken," and once violated "the damage is already done" — unrecoverable.

Liveness properties (p322) — availability: "a node that requests a fencing token and does not crash eventually receives a response" — may be unsatisfied at some instant but retain always hope that it may be satisfied in future. Practical asymmetry: distributed algorithms typically require safety to hold unconditionally in all situations of the system model, while liveness properties are allowed explicit caveats such as requiring a majority of nodes to not be crashed. `[D]`

**System models as simplified abstractions, an explicit named limitation with a memorable concrete gap [S]** (p323): quorum algorithms assume stable storage reliably survives crashes, but real disks can silently corrupt, be wiped by misconfiguration, or become unrecognized after a firmware bug — a scenario the formal crash-recovery model doesn't capture.

The theoretical description of an algorithm can declare that certain things are (p323) "assumed not to happen," yet a correct implementation must still include handling for such cases — "even if that handling boils down to printf" reporting failure and exiting, deferring to a human operator. "This is arguably the difference between computer science and software engineering" (p323).

## 2. WHAT / WHY / WHEN

**WHAT:** a systematic catalogue of everything that makes distributed systems categorically harder to reason about than a single machine — unreliable, asynchronous, unbounded-delay networks; clocks that are neither synchronized nor even self-consistent in the face of drift, resets, and NTP failure modes; and process pauses of unbounded and unpredictable length — culminating in formal system models (timing + node-failure assumptions) and the safety/liveness distinction needed to state precisely what any distributed algorithm can actually promise. `[D]`

**WHY it matters:** every fault-tolerance mechanism examined in earlier chapters (replica failover, replication lag, transaction isolation) implicitly assumed away exactly the problems this chapter makes explicit — that a distributed system cannot reliably know whether a remote node has failed, whether its own clock is correct, or whether its own execution has been silently paused — so any protocol claiming a correctness guarantee (in Ch.9's consensus algorithms) must be evaluated against a stated, honest system model rather than an implicit assumption of network and clock reliability. `[D]`

**WHEN to trust synchronized clocks vs. rely purely on logical/causal ordering (p309–311, synthesized across the chapter):** use physical (time-of-day) clocks only for human-facing timestamps and coarse, error-tolerant purposes (log entries, cache-expiry hints); never use them alone to establish a total order across nodes for conflict resolution (LWW) without accepting the named data-loss risk; prefer logical clocks (version vectors, Lamport-style counters) whenever true causal ordering must be preserved, or invest in confidence-interval-aware synchronization (TrueTime-style, with commit-wait) only when the operational cost of dedicated GPS/atomic clock hardware is justified by the guarantee needed (e.g. Spanner-style global transactions).

## 3. Assumptions and prerequisites

- Directly extends Ch.5's replication material (failover, replication lag) and Ch.7's transaction concurrency-control material, explicitly named as having been "too optimistic" — this chapter revisits the same territory assuming maximal pessimism about faults. `[S]` (p287)
- Directly extends Ch.5's leaderless-replication conflict-resolution material (LWW, version vectors), reusing the same worked multi-leader clock-skew example structure. `[S]` (p309)
- Directly extends Ch.6's partitioning terminology, explicitly disambiguating the term from partitioning-as-sharding to avoid a naming collision. `[D]`
- Directly extends Ch.7's snapshot isolation material for the Spanner/TrueTime global-snapshot discussion (distributed monotonic transaction IDs). `[S]` (p307–308)
- Forward-references consensus algorithms, majority-quorum leader election, and the Two/Byzantine Generals framing in full detail to Ch.9 — not yet synthesized in this vault. `[S]` (p292, p299, p318)
- Forward-references ordering guarantees (logical clocks in depth) to a later section of Ch.9 not yet synthesized in this vault. `[S]` (p310)

## 4. Mechanism / key steps

**Fencing-token protection protocol, the chapter's own worked description (p320–321)** `[D]`: a lock/lease service issues a monotonically increasing token alongside every grant → every client write to the protected resource must include its current token → the resource itself (not the client) tracks the highest token it has ever accepted → any incoming write bearing a token lower than that high-water mark is rejected outright, regardless of what the sending client believes about its own lock status → this survives the classic paused-client/reassigned-lease race because the stale client's outdated token is mechanically rejected rather than relying on the paused client to notice its own staleness.

**Spanner's TrueTime commit-wait mechanism for globally-ordered snapshot isolation, the chapter's own worked description (p307–308)** `[D]`: every clock reports a confidence interval `[earliest, latest]` rather than a single value → before committing a read-write transaction, the coordinator deliberately waits out the length of the interval → this guarantees that by the time the transaction is visible, any subsequent transaction's confidence interval cannot overlap with it → non-overlapping intervals give a provable happens-before ordering (`Aearliest < Alatest < Bearliest < Blatest` ⟹ B definitely after A) → the practical cost of this technique is proportional to clock uncertainty, motivating Google's investment in dedicated per-datacenter GPS/atomic clock hardware to keep intervals (and thus wait times) small (~7ms).

## 5. Trade-offs and limitations

- **Bounded, predictable network/clock guarantees are achievable but only via statically-partitioned, dedicated resources at significantly higher cost and lower utilization; dynamic sharing gives better utilization/lower cost at the price of variable, unbounded delays (§1, p302–303):** an explicit, general, named trade-off the chapter treats as the root cause of essentially all network- and clock-unreliability discussed in the chapter — "not a law of nature."
- **Short failure-detection timeouts detect real faults faster but risk false-positive node death (and potential cascading failure); long timeouts are safer but slower to react (§1, p296):** a direct, unavoidable trade-off with no universally correct value, resolvable only experimentally per-environment.
- **Byzantine fault tolerance protects against malicious/lying nodes but at a cost (supermajority requirements, protocol complexity, hardware-level support) the chapter judges disproportionate for ordinary server-side systems where nodes are organizationally trusted (§1, p322–323):** BFT is explicitly scoped to aerospace and multi-organization-trust contexts, not recommended as a general-purpose hardening technique.
- **Requiring safety properties to hold unconditionally, while allowing liveness properties explicit escape-clause caveats, is what makes formal reasoning about distributed algorithms tractable at all (§1, p327–328):** this asymmetric treatment is itself a deliberate simplification — a design choice about which guarantees are worth promising unconditionally, not a discovered law.

## 6. Failure modes and edge cases

- **HBase's real, named distributed-lock file-corruption bug (§1, p320):** an incorrect lock implementation (no fencing) let a paused client, believing it still held a valid lease, write to a file concurrently with the client that had legitimately taken over the lease — "the bug is not theoretical."
- **Silent, undetected clock drift causing "silent and subtle data loss" rather than a visible crash (§1, p306):** unlike a defective CPU or misconfigured network (which fail loudly and get fixed quickly), a defective quartz clock or broken NTP client lets "most things seem to work fine" while gradually drifting further from reality — a failure mode the chapter explicitly contrasts with louder, more diagnosable faults.
- **A "limping" node that degrades rather than cleanly failing, a named harder-to-handle case [S]** (p324): "a Gigabit network interface could suddenly drop to 1 kilobit/s throughput due to a driver bug" — a partial degradation that timeouts and health checks are poorly suited to detect, compared to a clean crash.
- **Asymmetric network faults defeating naive failure detection (§1, p292–294, p321):** a node that can receive but not send (or vice versa) looks identical to a dead node from the perspective of nodes it cannot reach, even though it is "working perfectly well" — explicitly dramatized as the semi-disconnected node "dragged to the graveyard, kicking and screaming."
- **Leap-second-induced crashes, a named historical pattern [S]** (p303): "the fact that leap seconds have crashed many large systems" is explicitly cited as showing how easy it is for incorrect assumptions about clocks to sneak into a system — motivating the smearing mitigation rather than a hard one-second jump. `[D]`

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the fencing-token pattern (§1, §4, p320–321) is directly reusable for any distributed-lock or leader-lease design in this vault's projects — never trust a client's self-reported belief about holding a lock; always require the protected resource to enforce a monotonic token check server-side. `[D]`
- **Build:** the monotonic-vs-time-of-day clock distinction (§1, p303–304) is a directly reusable implementation rule — always use a monotonic clock for measuring elapsed time/timeouts, and never assume time-of-day clock comparisons across machines reflect true event ordering.
- **Maintain:** the clock-drift monitoring discipline (§1, p306) is a directly reusable operational practice — since broken clocks fail silently rather than loudly, any system relying on clock synchronization needs active monitoring of inter-node clock offsets, removing any node whose drift exceeds a threshold.
- **RCA:** an observed "impossible" data loss or ordering violation in a multi-leader or leaderless system using last-write-wins is directly diagnosable against this chapter's three named LWW failure mechanisms (§1, p309–310) before assuming an application bug — check for clock skew, non-concurrent-writes misclassified as concurrent, or timestamp collisions.
- **Optimization:** the timeout-length trade-off framework (§1, p296) is a directly reusable tuning approach for any failure-detection system — favor experimentally-measured, adaptive timeouts (e.g. a Phi Accrual-style detector) over fixed constants, since the chapter shows there is no universally correct static value.

## 8. How to test / verify these claims

- The six indistinguishable network-failure modes (§1, p292) are directly reproducible: use a chaos-engineering tool (e.g. a network fault injector) to independently simulate request loss, response loss, and node unresponsiveness, and confirm a client cannot distinguish them without additional out-of-band information.
- The LWW clock-skew data-loss claim (§1, p309–310) is directly reproducible: run the chapter's own multi-leader worked example (concurrent write and increment with artificially skewed clocks) against a database using time-of-day-clock-based LWW (e.g. Cassandra) and confirm the causally-later write is silently dropped.
- The fencing-token protection claim (§4, p320–321) is directly testable by construction: implement the broken-lock scenario without fencing (reproduce the corruption), then add server-side token enforcement and confirm the stale client's write is rejected instead of corrupting the resource.
- The GC-pause process-pause claim (§1, p313) is directly reproducible: force a long stop-the-world GC pause in a JVM-based service holding a time-bound lease, and confirm the lease can expire and be reassigned before the paused thread resumes and notices.

## 9. Cross-references

- Directly extends [[ch05_replication|Ch.5]]'s replication (failover) and leaderless-replication conflict-resolution (LWW, version vectors) material, reusing and extending the same clock-skew worked example. No contradiction found. `[S]`
- Directly extends [[ch06_partitioning|Ch.6]]'s partitioning terminology, explicitly disambiguating overlapping vocabulary. No contradiction found. `[D]`
- Directly extends [[ch07_transactions|Ch.7]]'s snapshot isolation material via the Spanner/TrueTime global-transaction-ordering discussion. No contradiction found. `[S]`
- Forward-references (not yet synthesized in this vault): [[ch09_consistency_and_consensus|Ch.9]] for consensus algorithms, the Byzantine/Two Generals problem in full formal detail, majority-quorum leader election, and logical-clock ordering guarantees in depth.
- No contradiction found with any already-synthesized source in this vault.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 8-1 through 8-5 (request/response ambiguity diagram, network switch queueing diagram, clock-skew timestamp diagram, broken-lock and fencing-token sequence diagrams) | Structure and content described narratively above where load-bearing (§1, §4); full diagram layouts and exact timing traces not reproduced verbatim. |
| Full numbered reference list (~91 references) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. the datacenter network-fault studies, the HBase lock bug, Google's TrueTime/Spanner clock figures) are captured inline in §1/§6 with attribution context. |
| The Byzantine Generals Problem's full formal treatment and named etymology digression (p318) | The chapter itself defers the formal consensus treatment to Ch.9; this note captures the definitional and scoping content (what a Byzantine fault is, why it's excluded by default) but not the full historical/etymological aside, which is not load-bearing for this vault's DE-Mastery purposes. |
| Detailed vendor/protocol specifics (ISDN frame timing, ATM/InfiniBand technical comparison, Phi Accrual failure detector's internal formula) | Chapter discusses these at an illustrative level only; this note preserves the conceptual point each example makes (bounded vs. unbounded delay; adaptive vs. fixed timeouts) without reproducing protocol-level implementation detail beyond what the chapter itself states. |
