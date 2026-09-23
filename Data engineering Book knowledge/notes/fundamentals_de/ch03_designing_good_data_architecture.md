# Ch.3 — Designing Good Data Architecture

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 96–139 (44 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 15,434
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Enterprise architecture, the book's own definition [S]** (p98): after surveying
TOGAF, Gartner, and EABOK definitions, the authors settle on: "Enterprise
architecture is the design of systems to support change in the enterprise, achieved
by flexible and reversible decisions reached through careful evaluation of
trade-offs."

**Data architecture, the book's own definition [S]** (p100): "Data architecture is
the design of systems to support the evolving data needs of an enterprise, achieved
by flexible and reversible decisions reached through a careful evaluation of
trade-offs" — explicitly a specialization of the enterprise-architecture definition
above, inheriting the same "flexible and reversible" framing.

**One-way vs. two-way doors [S]** (p98–99, attributed to Jeff Bezos): a one-way door
is "a decision that is almost impossible to reverse" (example given: Amazon selling
or shutting down AWS); a two-way door is "an easily reversible decision" (example:
requiring DynamoDB for a new microservices database, reversible if it doesn't work
out).

**Operational vs. technical architecture [S]** (p101): "operational architecture
describes what needs to be done, and technical architecture details how it will
happen." Operational covers people/process/technology functional requirements;
technical covers how data is ingested, stored, transformed, served.

**The nine principles of data engineering architecture [S]** (p102–103, the
chapter's own numbered list, expanding on the AWS Well-Architected Framework and
Google Cloud's Five Principles for Cloud-Native Architecture): (1) choose common
components wisely, (2) plan for failure, (3) architect for scalability, (4)
architecture is leadership, (5) always be architecting, (6) build loosely coupled
systems, (7) make reversible decisions, (8) prioritize security, (9) embrace FinOps.

**Four failure-scenario terms [S]** (p104): Availability ("the percentage of time
an IT service or component is in an operable state"), Reliability ("the system's
probability of meeting defined standards... during a specified interval"), Recovery
Time Objective / RTO ("the maximum acceptable time for a service or system
outage"), Recovery Point Objective / RPO ("the maximum acceptable data loss").

**Domain vs. service [S]** (p112, quoting Eric Evans for "domain"): a domain is "the
real-world subject area for which you're architecting"; a service is "a set of
functionality whose goal is to accomplish a task." A domain can contain (and share)
multiple services.

**Shared-nothing vs. shared-disk architecture [S]** (p117): shared-nothing —
"a single node handles each request", "other nodes do not share resources"; shared
disk — nodes "share the same disk and memory accessible by all nodes", used "when
you want shared resources if a random node failure occurs."

## 2. WHAT / WHY / WHEN

**WHAT:** This chapter builds the book's architecture vocabulary from first
principles (enterprise architecture → data architecture → 9 principles) and then
surveys architecture patterns by example (data warehouse, data lake, lakehouse,
modern data stack, Lambda, Kappa, Dataflow model, IoT, data mesh) — explicitly "by
no means exhaustive," chosen to "expose you to some of the most common data
architecture patterns" (p123). `[D]`

**WHY it matters:** the chapter's most load-bearing, repeated claim is that
architecture quality is fundamentally about *managing change*, not picking the
"best" technology — "Never shoot for the best architecture, but rather the least
worst architecture" (p101, quoting Richards & Ford). This reframes architecture
review from "did they choose the right tool" to "can this be changed cheaply when
requirements change." `[D]`

**WHEN to use which pattern (the chapter's own explicit guidance, collected):**
- Lambda architecture: the book actively steers away from it — "Lambda isn't our
  first recommendation if you're trying to combine streaming and batch data for
  analytics" and "technology and practices have moved on" (p130). `[S]`
- Kappa architecture: acknowledged as theoretically elegant but "we haven't seen it
  widely adopted", citing cost/complexity of streaming at scale (p130). `[S]`
- Monolith vs. microservices: "monoliths aren't necessarily bad" and "it might make
  sense to start with one" when moving fast, "just be prepared to break it into
  smaller pieces eventually" (p119). `[S]`
- Brownfield migration: prefer the strangler pattern (incremental replacement) over
  "an all-at-once or big-bang overhaul" (p121), which the book says "often leads to
  disaster" (p122). `[S]`

## 3. Assumptions and prerequisites

- Assumes familiarity with Ch.1's undercurrents and Ch.2's lifecycle stages — this
  chapter is explicitly the deep dive on the "data architecture" undercurrent named
  in both prior chapters. `[S]`
- The distributed-systems material (p114, leader-follower horizontal scaling)
  explicitly defers deeper treatment to an external source: "Martin Kleppmann's
  Designing Data-Intensive Applications (O'Reilly) is an excellent resource" (p114)
  — that source (`ddia_kleppmann`) is in this project's corpus but not yet
  synthesized; this note's distributed-systems claims should be cross-checked once
  it is.
- The FinOps section (p112) explicitly notes its own novelty: "FinOps is a recently
  formalized practice", and "the FinOps Foundation was started only in 2019" — reading
  this material assumes it as an emerging discipline circa the book's 2022
  publication, not settled practice. `[S]`

## 4. Mechanism / key steps

**The strangler pattern for brownfield migration (p122):** named and
attributed (Martin Fowler); mechanism per the chapter: "new systems slowly and
incrementally replace a legacy architecture's components" -- "eventually, the legacy
architecture is completely replaced." Explicit advantage stated: "targeted and
surgical approach of deprecating one piece of a system at a time", allowing
reversible decisions while assessing impact on dependent systems.

**Traditional data warehouse ETL workflow (p123–124):** Extract (pull from source
systems) → Transform (clean, standardize, apply business logic "in a highly modeled
form") → Load (push into the warehouse; data lands in "multiple data marts" per
line of business).

**ELT variant (p124–125):** data moves "more or less directly from production
systems into a staging area in the data warehouse" in raw form; transformation
happens *inside* the warehouse afterward, using its own compute — explicitly framed
as taking "advantage of the massive computational power of cloud data warehouses."

**Lambda architecture's three independent layers (p129):** batch layer
(precomputed/aggregated views, e.g. in a data warehouse) + speed/streaming layer
(lowest-latency serving, "usually a NoSQL database") + serving layer (combines
query results from both). The chapter's own criticism of this mechanism is in §5.

**Data mesh's four components (p134, attributed to Zhamak Dehghani):**
"Domain-oriented decentralized data ownership and architecture"; data as a product;
self-serve data infrastructure as a platform; federated computational governance.

## 5. Trade-offs and limitations

- **Common-components principle is explicitly a balancing act (p103–104):** the
  book warns against both extremes — under-standardizing wastes effort, but
  "architects should avoid decisions that will hamper the productivity of engineers
  working on domain-specific problems by forcing them into one-size-fits-all
  technology solutions." `[S]`
- **Loose coupling has an organizational cost the chapter names directly (p115):**
  "it's easy for decentralized teams to build systems whose data may not be usable
  by their peers" — loose coupling requires deliberately to "assign common
  standards, ownership, responsibility, and accountability", it doesn't emerge for
  free. `[S]`
- **Single-tier architecture's explicit failure mode (p116):** "if the server,
  the database, or the application fails, the entire architecture fails" — stated as
  acceptable for prototyping/testing only, "not advised for production uses." (p116)
- **Lambda architecture's core criticism, in the book's own words (p130):**
  "Managing multiple systems with different codebases is as difficult as it sounds,
  creating error-prone systems with code and data that are extremely difficult to
  reconcile."
- **Data lake 1.0's documented failure pattern (p126–127):** explicit list of
  symptoms — "terms such as data swamp, dark data, and WORN were coined," "the
  original data lake concept was essentially write-only, creating huge headaches
  with the arrival of regulations such as GDPR," and the costs of Hadoop cluster
  management "ballooned" despite the promise of avoiding "multimillion-dollar
  contracts for proprietary MPP systems." A full, source-supported case against
  treating "data lake" as inherently cheaper or simpler than a warehouse. `[S]`

## 6. Failure modes and edge cases

- **Big-bang brownfield rewrites (p122):** "this path often leads to disaster, with
  many irreversible and costly decisions" — the book's own named anti-pattern,
  countered by the strangler pattern (§4).
- **Resume-driven development on greenfield projects (p122):** "a temptation to do
  resume-driven development, stacking up impressive new technologies without
  prioritizing the project's ultimate goals" — an explicitly named organizational
  failure mode, not a technical one.
- **Noisy-neighbor problem in multitenancy (p119–120):** "will high usage from one
  tenant degrade performance for other tenants?" — named as one of exactly two
  factors (with security/isolation) that must be evaluated for any multitenant
  design decision.
- **S3 bucket public-access breaches (p109–110):** "Numerous data breaches have
  resulted from the simple error of configuring Amazon S3 buckets with public
  access" — cited as the concrete consequence of data engineers not treating
  themselves as security engineers under the cloud's shared-responsibility model.
- **Cost attacks via public data sharing (p111):** the book explicitly names this
  as a DDoS analogy — "excessive downloads from S3 buckets can drive spending
  through the roof and threaten a small startup with bankruptcy" — recommending
  requester-pays policies or active spend monitoring as mitigations.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the nine principles (§1) are a directly reusable architecture-review
  checklist, more concrete than Ch.2's stage-level question lists since each
  principle names a specific failure mode to check against (e.g. principle 2 maps
  directly to the availability/reliability/RTO/RPO vocabulary in §1). `[D]`
- **Build:** the strangler-pattern mechanism (§4) is the chapter's explicit
  recommended approach for any brownfield rebuild in this vault's projects,
  over a full-rewrite approach the book calls disaster-prone. `[D]`
- **Maintain:** the "always be architecting" principle (p105–106) implies
  architecture review is not a one-time gate but a recurring practice — "data
  architects don't serve in their role simply to maintain the existing state." `[D]`
- **RCA:** the availability/reliability relationship stated explicitly (p114) —
  "low reliability can lead to low availability... elasticity improves
  reliability" — gives a concrete causal chain to check first when an incident
  investigation needs to distinguish a reliability problem from a capacity problem.
  `[D]`
- **Optimization/FinOps:** the shift from thinking "in terms of performance
  engineering" on "a fixed set of resources" to actively monitoring cloud spend as
  a first-class operational metric (p111) is a concrete, source-grounded argument
  for building cost dashboards into any cloud pipeline from the start, not as an
  afterthought. `[D]`

## 8. How to test / verify these claims

- The one-way/two-way door framework and the nine principles are presented as the
  authors' synthesis of external frameworks (TOGAF, Gartner, EABOK, AWS
  Well-Architected, Google Cloud's Five Principles) plus their own judgment — not
  independently falsifiable claims, but each external framework named is a
  checkable, named source. `[S]` claim, `[D]` flag on treating the synthesis itself
  as anything other than this book's opinion.
- The data lake 1.0 failure narrative (§5) is presented as a widely observed
  industry pattern rather than a single documented case study — directionally
  consistent with well-known industry discourse (the terms "data swamp" and "WORN"
  are independently attested elsewhere in the field) but not sourced to a specific
  measured study in this chapter. `[S]` claim, `[D]` flag on specificity.

## 9. Cross-references

- Directly extends `fundamentals_de` [[ch01_data_engineering_described|Ch.1]] and [[ch02_data_engineering_lifecycle|Ch.2]] (both synthesized) — no
  contradiction found on cross-check; [[ch02_data_engineering_lifecycle|Ch.2]]'s "data architecture" undercurrent
  pointer is exactly the material developed here.
- Explicitly defers to [[ch04_choosing_technologies|Ch.4]] (technology choice, monolith-vs-distributed detail),
  [[ch05_data_generation_source_systems|Ch.5]] (event-driven streaming/messaging), [[ch06_storage|Ch.6]] (storage, IoT storage detail), [[ch08_queries_modeling_transformation|Ch.8]]
  (transformations, data marts, data models), [[ch11_future_of_data_engineering|Ch.11]] (modern data stack's future,
  "live data stack") — none synthesized yet. Flagged for `check_deferred_refs.py`.
- Explicitly defers to `ddia_kleppmann` (not yet synthesized in this vault) for
  distributed-systems depth (§3) — this is the first note in this project to defer
  to a *different source*, not just a later chapter of the same book; worth
  tracking once DDIA synthesis begins.
- The data lakehouse definition here (p128) is consistent with `databricks_big_book_4e`'s
  vendor framing in the Lakebase note, though that note is about a different
  Databricks product (Lakebase, not the lakehouse architecture itself) — no direct
  contradiction, but worth noting both sources discuss the same vendor's platform
  from different angles. `[D]`

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 3-1 through 3-18 (18 figures: enterprise architecture subset diagram, operational/technical split, domain-sharing diagram, distributed system diagram, tier diagrams, monolith/microservices diagrams, event-driven diagrams, warehouse/lake/lakehouse workflow diagrams, Lambda/Kappa diagrams, IoT diagrams, data mesh diagram) | All flagged pages in this range are `reading_order_risk` dispositioned `deferred` per the project-wide sampled finding (header/image-ordering artifact, not corrupted body text). Captions were fully extracted and are described narratively above where load-bearing (§1, §4); diagrams were not individually rendered to image for this chapter. |
| "Additional Resources" list (p136–139, ~65 external links) | Bibliography, not chapter content — by far the largest such list in the book so far; not synthesized. |
| IoT architecture subsection detail (p131–134: gateways, edge computing specifics) | Covered at summary level in §1/§4 where it overlaps core architecture concepts (the reverse-ETL-shaped IoT serving pattern); the chapter's own framing calls this "scratching the surface," and this note matches that scope rather than expanding it. |
| Footnoted external definitions (TOGAF, Gartner, EABOK, DAMA DMBOK data-architecture definitions, p97–100) | Quoted directly where load-bearing to this note's own definition-building (§1); the source documents themselves were not independently retrieved. |
