# Ch.1 — Reliable, Scalable and Maintainable Applications

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 23–46 (24 pages, including endnotes) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session) — first chapter of `ddia_kleppmann`
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Data-intensive vs. compute-intensive, the book's opening distinction [S]** (p23): "Many applications today are data-intensive, as opposed to compute-intensive. Raw CPU power is rarely a limiting factor for these applications — bigger problems are usually the amount of data, the complexity of data, and the speed at which it is changing."

**Data systems as a blurred-boundary umbrella term, not a fixed taxonomy [S]** (p24): "there are data stores that are also used as message queues (Redis), and there are message queues with database-like durability guarantees (Kafka). The boundaries between the categories are becoming blurred." This drives a named structural consequence: when a service combines several general-purpose tools, "you have essentially created a new, special-purpose data system from smaller, general-purpose components... You are now not only an application developer, but also a data system designer."

**Three core concerns the book organizes around, each formally defined [S]** (p26): **Reliability** — "The system should continue to work correctly... even in the face of adversity (hardware or software faults, and even human error)." **Scalability** — "As the system grows (in data volume, traffic volume or complexity), there should be reasonable ways of dealing with that growth." **Maintainability** — "Over time, many different people will work on the system... and they should all be able to work on it productively."

**Fault vs. failure, an explicit and precise distinction [S]** (p27): "A fault is usually defined as one component of the system deviating from its spec, whereas a failure is when the system as a whole stops providing the required service to the user. It is impossible to reduce the probability of a fault to zero; therefore it is usually best to design fault tolerance mechanisms that prevent faults from causing failures."

**Deliberately inducing faults to strengthen fault tolerance, an explicit counter-intuitive practice [S]** (p27): "in such fault-tolerant systems, it can make sense to increase the rate of faults by triggering them deliberately — for example, by randomly killing individual processes without warning."

"The Netflix chaos monkey" is an example of this approach (p27).

Justification follows (p27): "Many critical bugs are actually due to poor error" handling; "by deliberately inducing faults, you ensure that the fault-tolerance machinery is continually exercised and tested."

**Prevention preferred over cure specifically for security [S]** (p27): "Although we generally prefer tolerating faults over preventing faults, there are cases where prevention is better than cure (e.g. because no cure exists). This is the case with security matters... if an attacker has compromised a system and gained access to sensitive data, that event cannot be undone."

**Hardware fault statistics, a concrete named figure and its consequence [S]** (p27): "Hard disks are reported as having a mean time to failure (MTTF) of about 10 to 50 years." "Thus, on a storage cluster with 10,000 disks, we should expect on average one disk to die per day."

**Cloud elasticity's reliability trade-off, an explicit named cause [S]** (p28): "in some" cloud "platforms such as Amazon Web Services it is fairly common for virtual machine instances to become unavailable without warning" (p28), "as the platform is designed to prioritize flexibility and elasticity" over single-machine reliability (p28).

**Software faults are correlated, unlike hardware faults, an explicit contrast [S]** (p28): "We usually think of hardware faults as being random and independent from each other:" one machine's disk failing does not imply that another machine's disk is going to fail.

"Another class of fault is a systematic error within the system" (p28). "Such faults are harder to anticipate, and because they are correlated across nodes, they tend to cause many more system failures than uncorrelated" hardware faults (p28).

Named concrete example (p28): "consider the leap second on June 30, 2012 that caused many applications to hang simultaneously, due to a bug in the Linux kernel" as reported in the cited source.

**Software fault root cause, an explicit pattern [S]** (p29): "The bugs that cause these kinds of software fault often lie dormant for a long time until they are triggered by an unusual set of circumstances... it is revealed that the software is making some kind of assumption about its environment — and while that assumption is usually true, it eventually stops being true for some reason."

**Human error as the leading cause of outages, a named empirical finding [S]** (p29): "one study of large internet services found that configuration errors by operators were the leading cause of outages, whereas hardware faults (servers or network) played a role in only 10–25% of outages" as reported in the cited study (p29).

**Five named combined approaches for making systems reliable despite unreliable humans [S]** (p29–30): minimize error opportunities via well-designed abstractions/APIs (with an explicit named tension: "if the interfaces are too restrictive, people will work around them, negating their benefit"); decouple mistake-prone areas from failure-causing areas via full-featured non-production sandboxes; test thoroughly at all levels; enable quick, easy recovery (fast rollback, gradual rollout, recomputation tools); and set up detailed monitoring/telemetry providing "early warning signals."

**Reliability's stakes extend beyond critical systems, an explicit worked example [S]** (p30): "Consider a parent who stores all pictures and videos of their children in your photo application. How would they feel if that database was suddenly corrupted?" A named explicit exception: reliability may be deliberately sacrificed "to reduce development cost (e.g. when developing a prototype product for an unproven market)... but we should be very conscious of when we are cutting corners."

**Scalability defined as a question, not a static label [S]** (p31): "it is meaningless to say" X is scalable "or" Y doesn't scale. "Rather, discussing scalability means to discuss the question: if the system grows in a particular way, what are our options for coping with the growth?"

**Load parameters, defined and application-specific [S]** (p31): "Load can be described with a few numbers which we call load parameters. The best choice of parameters depends on the architecture of your system: perhaps it's requests per second to a webserver, ratio of reads to writes in a database, the number of simultaneously active users in a chat room, the hit rate on a cache, or something else."

**Twitter fan-out worked case study, the chapter's own extended example [S]** (p31–33): two operations — post tweet (4.6k req/s average, 12k peak) and home timeline (300k req/s) — with two architectural approaches: (1) query-time join across tweets/users/follows tables, simple but "the systems struggled to keep up with the load of home timeline queries"; (2) precomputed per-user home timeline caches ("mailboxes"), fanning out each tweet to all followers at write time — 4.6k tweet writes become 345k timeline writes/sec, and a single celebrity tweet can generate "over 30 million writes to home timelines." Twitter's final resolution is a named hybrid: fan out normally for most users, but fetch celebrity tweets separately at read time and merge — "This hybrid approach is able to deliver consistently good performance."

**Throughput vs. response time, scoped by system type [S]** (p33): "In a batch-processing system such as Hadoop, we usually care about throughput — the number of records we can process per second, or the total time it takes to run a job on a dataset of a certain size."

"In online systems, the response time of a service is usually more important" (p33).

**Latency vs. response time, precisely distinguished [S]** (p34): "The response time is what the client sees: besides the actual time to process the request (the service time), it includes network delays and queueing delays. Latency is the duration that a request is waiting to be handled — during which it is latent, awaiting" service.

**Response time as a distribution, not a single number, with percentile definitions [S]**: the median is "the half-way point" (p34); "if your" median response time is 200 ms, that means "half your requests return in less than 200 ms, and half your requests take longer than that" (p35).

Higher percentiles — abbreviated p95, p99, p999 — are "the response time thresholds at which 95%, 99% or 99.9% of requests are faster than that particular threshold" (p35).

An explicit multi-request caveat follows (p35): "if the user makes several requests (over the course of a session, or because several resources are included in a single page), the probability that at least one of them is slower than the median is much greater than 50%."

**High percentiles matter because of who they affect, a named empirical justification [S]** (p35): "Amazon describes response time requirements for internal services in terms of the 99.9th percentile, even though it only affects 1 in 1,000 requests. This is because the customers with the slowest requests are often those who have made many purchases — i.e. the most valuable customers." Named concrete costs of latency: "a 100 ms increase in response time reduces sales by 1%" and "a 1-second slowdown reduces a customer satisfaction metric by 16%." An explicit cost/benefit boundary: "optimizing the 99.99th percentile... was deemed too expensive and not yield enough benefit for Amazon's purposes."

**SLOs/SLAs defined with a concrete worked example [S]** (p35): "a SLA may state that the service is considered to be up if it has a median response time of less than 200 ms and a 99th percentile under 1 s... and the service may be required to be up at least 99.9% of the time."

**Head-of-line blocking, defined with its measurement implication [S]** (p35): "As a server can only process a small number of things in parallel (limited for example by its number of CPU cores), it only takes a small number of slow requests to hold up" the processing of subsequent requests (p36) — "an effect sometimes known as head-of-line blocking."

Direct methodological consequence (p36): "it is important to measure response times on the client side."

Load-testing clients must not wait for prior responses before issuing the next request, or (p36) "that behavior has the effect of artificially keeping the queues shorter in the test than they would be in reality, which skews the" measurements.

**Tail amplification across parallel backend calls, an explicit named effect [S]** (p36): "Even if you make the calls in parallel, the end-user request still needs to wait for the slowest of the parallel calls to complete... Even if only a small percentage of backend calls are slow, the chance of getting a slow call increases if an end-user request requires multiple backend calls, and so a higher proportion of end-user requests end up being slow."

**Percentile aggregation, an explicit named mathematical error and its fix [S]** (p36): "averaging percentiles, e.g. to reduce the time resolution or to combine data from several machines, is mathematically meaningless — the right way of aggregating response time data is to add the" histograms. Named efficient percentile-approximation algorithms: forward decay, t-digest, HdrHistogram.

**Scaling up vs. scaling out, defined with an explicit named architectural term [S]** (p37): "scaling up (vertical scaling, moving to a more powerful machine)" vs. "scaling out (horizontal scaling, distributing the load across multiple smaller machines)... also known as a shared nothing architecture." Explicit pragmatic middle ground: "good architectures usually involve a pragmatic mixture of approaches."

**Elastic vs. manually scaled systems, an explicit trade-off [S]** (p37): "An elastic system can be useful if load is highly unpredictable, but manually scaled systems are simpler and may have fewer operational" surprises.

**Stateful distribution named as categorically harder than stateless [S]** (p38): "While distributing stateless services across multiple machines is fairly straightforward, taking stateful data systems from a single node to a distributed setup can introduce a lot of additional complexity. For this reason, common wisdom until recently was to keep your database on a single node (scale up) until scaling cost or high-availability requirements forced you to make it distributed."

**No universal scalable architecture, an explicit named myth rejection [S]** (p38): "there is no such thing as a generic, one-size-fits-all scalable architecture (informally known as magic scaling sauce)." A concrete illustrative contrast: "a system that is designed to handle 100,000 requests per second, each 1 kB in size, looks very different from a system that is designed for three requests per minute, each 2 GB in size — even though the two systems have the same data throughput."

**Premature scaling risk, an explicit named cost [S]** (p38): "If those assumptions turn out to be wrong, the engineering effort for scaling is at best wasted, and at worst counter-productive. In an early-stage startup or an unproven product it's usually more important to be able to iterate quickly on product features, than it is to scale to some hypothetical future load."

**Maintainability's three design principles, each formally defined [S]** (p39): **Operability** — "Make it easy for operations teams to keep the system running smoothly." **Simplicity** — "Make it easy for new engineers to understand the system, by removing as much complexity as possible from the system," explicitly distinguished from UI simplicity. **Evolvability** — "Make it easy for engineers in future to make changes to the system, adapting it for unanticipated use cases as requirements change," also called extensibility, modifiability, or plasticity.

**Good operations vs. good software, an explicit asymmetry quoted directly [S]** (p39): "good operations can often work around the limitations of bad (or incomplete) software, but good software cannot run reliably with bad" operations.

**Accidental vs. inherent complexity, a precise definition attributed to Moseley and Marks [S]** (p41): "complexity as accidental if it is not inherent in the problem that the software solves (as seen by the users), but arises only from the implementation." Direct implication: "Making a system simpler does not necessarily mean reducing its functionality; it can also mean removing accidental complexity."

**Abstraction as the primary tool against accidental complexity, with two named examples [S]** (p41): "high-level programming languages are abstractions that hide machine code, CPU registers and syscalls. SQL is an abstraction that hides complex on-disk and in-memory data structures, concurrent requests from other clients, and inconsistencies after crashes." An explicit named limitation for this book's domain: "in the field of distributed systems, although there are many good algorithms, it is much less clear how we should be packaging them into abstractions that help us keep the complexity of the system at a manageable level."

**Evolvability tied directly to simplicity and named as the data-systems-level analogue of agility [S]** (p42): "The ease with which you can modify a data system, and adapt it to changing requirements, is closely linked to its simplicity and its abstractions... we will use a different word to refer to agility on a data system level:" evolvability.

## 2. WHAT / WHY / WHEN

**WHAT:** The book's foundational chapter, establishing data-intensive applications as the book's subject, and defining the three organizing concerns — reliability (faults: hardware, software, human), scalability (load description via load parameters, the Twitter fan-out case study, performance description via throughput/response-time/percentiles, scaling-up vs. scaling-out approaches), and maintainability (operability, simplicity/accidental-complexity-removal via abstraction, evolvability) — that structure the rest of the book. `[D]`

**WHY it matters:** the chapter explicitly sets up its own methodology: rather than offering "quick answers" to reliability, scalability, or maintainability, it commits to examining "patterns and techniques which keep re-appearing in various different kinds of application" across the rest of the book — meaning every later chapter's specific technique should be read as an instance of one or more of these three concerns. `[D]`

**WHEN to trigger faults deliberately (chaos engineering) vs. simply harden against them (p27):** deliberately induce faults specifically to continuously exercise and validate fault-tolerance machinery that would otherwise sit untested until a real (and possibly mishandled) fault occurs — appropriate once basic fault-tolerance mechanisms already exist, not as a substitute for building them.

**WHEN to scale out vs. scale up, and elastic vs. manual scaling (p37–38):** scale up while a single more-powerful machine remains simpler and sufficiently cost-effective; scale out once workload intensity exceeds what a single high-end machine can economically handle. Use elastic (automatic) scaling specifically when load is highly unpredictable; prefer manual scaling when predictability of operational behavior matters more than automatic responsiveness.

## 3. Assumptions and prerequisites

- Assumes no prior chapters (this is the book's first chapter) — instead, this chapter itself is explicitly assumed by later chapters, with direct forward-references to a later Rebalancing partitions section and to Part III's discussion of composite systems like Figure 1-1. `[D]`
- Assumes general familiarity with relational databases (SQL join syntax used directly in the Twitter worked example, p31) and basic distributed systems vocabulary (CPU, RAM, network) without redefining them.

## 4. Mechanism / key steps

**Twitter's home timeline architecture evolution, the chapter's own three-stage worked example (p31–33):**
1. **Approach 1 (query-time fan-in):** posting a tweet is a simple insert into a global tweets table; reading a home timeline requires a live join across `tweets`, `users`, and `follows` tables for every request — simple to build, but "the systems struggled to keep up with the load of home timeline queries" given 300k reads/sec against 4.6k writes/sec.
2. **Approach 2 (write-time fan-out):** each home timeline is materialized as a precomputed per-user cache; posting a tweet looks up all followers and inserts the new tweet into each of their cached timelines — read requests become cheap, but write amplification is severe (4.6k tweet writes → 345k timeline writes/sec on average, and up to 30 million writes for a single celebrity tweet).
3. **Hybrid approach (final production state):** most users' tweets are fanned out at write time as in approach 2; a small number of very-high-follower-count users are excluded from fan-out, with their tweets fetched separately at read time and merged into the timeline as in approach 1 — combining the read-time cheapness of approach 2 for ordinary users with avoidance of approach 2's write-amplification blowup for celebrities.

**Percentile-based dashboard monitoring, the chapter's own described process (p36):** maintain a rolling window of response times (e.g. last ten minutes) → every minute, compute median and target percentiles over that window → plot on a monitoring dashboard → for efficiency at scale, use approximation algorithms (forward decay, t-digest, HdrHistogram) rather than naively sorting the full response-time list each time → when combining percentile data across time windows or machines, aggregate the underlying histograms, never average the percentile values directly.

## 5. Trade-offs and limitations

- **Restrictive error-preventing interfaces can backfire (§1, p29–30):** "if the interfaces are too restrictive, people will work around them, negating their benefit, so this is a tricky balance to get right" — a named, genuine design tension rather than a simple "more restriction is safer" rule.
- **Elastic scaling trades operational predictability for responsiveness to unpredictable load (§1, p37):** manual scaling is explicitly preferred when operational simplicity and predictability outweigh the convenience of automatic elasticity.
- **Investing in scalability ahead of validated need is explicitly named as a potential net negative (§1, p38):** for early-stage or unproven products, engineering effort spent scaling for a load level that never materializes is "at best wasted, and at worst counter-productive" compared to feature iteration speed.
- **The 99.99th percentile is an explicit named example of a point past which optimization stops paying off (§1, p35):** high-percentile optimization has diminishing returns and increasing difficulty, since extreme tail latency "is easily affected by random events outside of your control."

## 6. Failure modes and edge cases

- **Cascading failures, a named explicit software fault pattern (§1, p29):** "a small fault in one component triggers a fault in another component, which in turn triggers further faults" — a concrete, nameable failure mode distinct from an isolated single-component bug.
- **Load-testing clients that wait for each response before issuing the next request (§1, p35–36):** named directly as producing artificially optimistic latency measurements by suppressing the queueing effects that would occur under real, independent request arrival.
- **Assuming average/mean response time reflects "typical" user experience (§1, p34):** explicitly rejected — the mean "doesn't tell you how many users actually experienced that delay," making percentiles the more meaningful metric for user-facing latency claims.
- **A dormant software assumption silently becoming false (§1, p29):** the named general mechanism behind long-latent software bugs — code correctness depended on an environmental assumption that eventually stopped holding.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the three-concern framework (reliability, scalability, maintainability) is directly usable as a structured lens for evaluating any new system design in this vault's projects, and the fault/failure distinction (§1, p27) directly informs where to invest fault-tolerance engineering effort — at the fault-to-failure boundary, not at eliminating faults entirely. `[D]`
- **Build:** the load-parameter-first approach to scalability discussion (§1, p31) is a directly reusable discipline: before proposing any scaling solution, first identify and quantify the specific load parameters (not a vague "more traffic") that are actually growing.
- **Maintain:** the accidental-vs-inherent complexity distinction (§1, p41) is a directly reusable diagnostic for any system refactoring decision — ask whether complexity being removed is genuinely implementation-derived (removable) or reflects real problem complexity the users care about (not removable without losing functionality).
- **RCA:** the human-error-as-leading-outage-cause finding (§1, p29) is a directly reusable prior when investigating a production incident — check configuration changes before assuming a hardware or software root cause, especially for large internet-scale services.
- **Optimization:** the percentile-histogram-aggregation rule (§1, p36) is a directly reusable correctness rule for any monitoring/observability pipeline that aggregates latency data across time windows or machines — never average percentiles directly.

## 8. How to test / verify these claims

- The percentile-aggregation-by-averaging error (§1, p36) is directly demonstrable: construct two response-time distributions with different shapes, average their p99 values, and compare against the true p99 of the combined histogram to show the discrepancy.
- The head-of-line-blocking/client-side-measurement claim (§1, p35–36) is directly testable: run a load test with a client that waits for each response before sending the next request, then compare measured latency distribution against one from an independent-arrival-rate load generator.
- The tail-amplification-across-parallel-calls effect (§1, p36) is directly reproducible: simulate N parallel backend calls each with a small independent probability of being slow, and show the probability of the overall request being slow grows with N.
- The MTTF-based disk failure rate calculation (§1, p27, "one disk to die per day" on a 10,000-disk cluster with 10–50 year MTTF) is a directly reproducible arithmetic check: 10,000 disks / (10–50 years × 365 days) ≈ 0.5–2.7 failures/day, consistent with the stated "about one disk per day."

## 9. Cross-references

- This is the first chapter of `ddia_kleppmann`; no backward cross-references within the source exist. Forward-references within this same source: a later Rebalancing partitions section and Part III's treatment of composite multi-component systems like the one in Figure 1-1 — both not yet synthesized. `[D]`
- No contradiction with any other already-synthesized source in this vault was found; this chapter's reliability/scalability/maintainability framework is complementary to (and does not overlap in claims with) the dimensional-modeling-focused `kimball_dwtoolkit_3e` material already synthesized.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figure 1-1 (composite data system architecture diagram), 1-2 (Twitter relational schema diagram), 1-3 (Twitter fan-out pipeline diagram), 1-4 (response time percentile illustration), 1-5 (parallel backend call latency diagram) | Structure and content described narratively above where load-bearing (§1, §4); full diagrams not reproduced verbatim. |
| Full nine-item "good operations team" checklist and seven-item "good operability" checklist (p39–40) | Representative items and the overall operability framing captured in §1; the complete verbatim checklists are not reproduced. |
| Full numbered reference list (34 references, p21–23 of chapter / p43–46 of PDF) | Citation metadata only (author names, publication venues, dates); not treated as substantive content requiring synthesis, though several individually notable claims sourced from specific references (e.g. Amazon's response-time/sales-impact study, the Netflix chaos monkey) are captured inline in §1 with their attribution context. |
