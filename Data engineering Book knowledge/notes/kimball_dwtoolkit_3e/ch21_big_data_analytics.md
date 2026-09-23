# Ch.21 — Big Data Analytics

**Source:** `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd ed., Kimball & Ross, Wiley)
**PDF page range:** 563–578 (16 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session) — final chapter of `kimball_dwtoolkit_3e`
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Big data defined by variety and paradigm shift, not size [S]** (p563): "Its bigness is actually not the most interesting characteristic. Big data is structured, semistructured, unstructured, and raw data in many different formats... But most important, big data is a paradigm shift in how you think about data assets, where you collect them, how you analyze them, and how you monetize the insights from the analysis."

**Nineteen named capabilities a candidate big data system must support [S]** (p564–565): including scaling to petabytes across thousands of distributed, possibly heterogeneous processors; storing data in original captured formats without conversion; embedding and executing arbitrarily complex UDFs across large libraries as relation scans over petabyte-sized data in minutes; loading at gigabytes/second before structure is declared or discovered; executing streaming analytic queries on incoming load data; updating in place at full load speed; joining a billion-row dimension to a trillion-row fact table without preclustering; scheduling multi-hundred-node workflows with no single point of failure and graceful failover; and supporting extreme mixed workloads spanning ad hoc queries, strategic analysis, and simultaneous batch/streaming loads.

**Two architectural responses named directly [S]** (p565): "In response to these challenges, two architectures have emerged: extended RDBMSs and MapReduce/Hadoop."

**Extended RDBMS's core requirement, not merely wider type support [S]** (p566): "it is not sufficient for RDBMSs to merely host the new data types as blobs to be delivered at some later time to a BI application that can interpret the data... To really own big data, RDBMSs must allow the new data types to be processed within the DBMS inner loop by means of specially crafted user-defined functions (UDFs) written by business user analysts."

**A two-pass RDBMS use case named directly [S]** (p566): "process the data twice through the RDBMS, where in the first pass the RDBMS is used as a fact extractor on the original data, and then in the second pass, these results are automatically fed back to the RDBMS input as conventional relational rows, columns, and data types."

**MapReduce/Hadoop, defined and scoped [S]** (p566): "MapReduce is a processing framework originally developed by Google in the early 2000s for performing web page searches across thousands of physically separated machines." "MapReduce is actually a UDF execution framework, where the" F "can be extraordinarily complex. The most significant implementation of MapReduce is Apache Hadoop."

The chapter explicitly declines to go deeper (p566): "A full discussion of the MapReduce/Hadoop architecture is beyond the scope of this book."

**Extended RDBMS vs. MapReduce/Hadoop comparison, an explicit non-competitive framing [S]** (p566): "The two big data architecture approaches have separate long-term advantages and are likely to coexist far into the future." Named trade-offs (Figure 21-2): RDBMS is proprietary/expensive, requires structured data, excels at speedy indexed lookups and relational semantics, but has indirect support for complex data structures and iteration; Hadoop is less expensive, structure-free, excels at massive full scans and complex/iterative processing, but has indirect relational-semantics support (e.g. via Hive) and little/no transaction processing support.

**Six inherited best practices from 30 years of conventional DW/BI, restated as directly applicable to big data [S]** (p567): drive source selection from business needs; focus incessantly on UI simplicity and performance; think dimensionally; integrate separate sources with conformed dimensions; track time variance with SCDs; anchor all dimensions with durable surrogate keys.

**Legacy-avoidance as an explicit management best practice [S]** (p568): "It's not a good idea to attempt building a legacy big data environment at this time. The big data environment is changing too rapidly to consider building a long-lasting legacy foundation... Assume you will reprogram and rehost all your big data applications within two years."

**Sandbox-to-production discipline, explicitly requiring IT tolerance of chaotic experimentation [S]** (p568–569): "IT must be uncharacteristically tolerant of the range of technologies the data scientists use and be prepared in many cases to re-implement the data scientists' work in a standard set of technologies that can be supported over the long haul."

**Hadoop as a low-risk entry point, an explicit named starting use case [S]** (p569): "consider using Hadoop as a low-cost, flexible backup and archiving technology."

The chapter also names a second benefit (p569): "This approach may also enable you address the sunsetting challenge where original applications may not be available in the distant future (perhaps because of licensing restrictions)"; you can dump the data into a documented format instead.

**The data highway, five named caches of increasing latency [S]** (p569–570): Raw Source (immediate) → Real Time Cache (seconds) → Business Activity Cache (minutes) → Top Line Cache (24 hours) → DW and Long Time Series (daily/periodic/annual).

Each cache is "physical and distinct from the other caches" (p570), and data can take multiple parallel paths from raw source to intermediate caches, not just one linear pipeline.

**Big data as a fact extractor, a concrete named example [S]** (p570): unstructured text tweet analysis "can produce a whole set of numerical, trendable sentiment measures including share of voice, audience engagement, conversation reach, active advocates, advocate influence, advocacy impact, resolution rate, resolution time, satisfaction score, topic trends, sentiment ratio, and idea impact."

**Latency/quality trade-off along the data highway, an explicit acceptance rule [S]** (p571): "very low latency (that is, immediate) data is unavoidably dirty because there are limits to how much cleansing and diagnosing can be done in very short time intervals." Column-level tests survive at any speed; structural and business-rule tests are "necessarily slower," and slower caches like the top line cache are typically "built on fundamentally more complete data."

**Add-value-early principle, with an explicit acknowledged counter-position [S]** (p571): "apply filtering, cleansing, pruning, conforming, matching, joining, and diagnosing at the earliest touch points possible." The chapter names a genuine dissenting view: "there is a school of thought that applies cleansing logic only at analysis run time because cleansing might delete 'interesting outliers.'"

**Backflow to earlier caches, an explicit durable-key mechanism [S]** (p571–572): "Job One in each ETL step from one cache to the next is to replace idiosyncratic proprietary keys with the unique durable keys so that analysis in each cache can take advantage of the rich upstream content with a simple join on the unique durable key." The chapter poses its own open question about feasibility: "Can this ETL step be performed even when transferring raw source data into the real time cache in less than a second? Maybe…."

**Streaming analytics can terminate early on threshold events [S]** (p572): "when the results of a streaming query surpass a threshold, the analysis can be halted without running the job to the bitter end."

The chapter attributes foundational work here to continuous query language (CQL) research on dynamically moving time windows (p572).

**Boundary crashes, an explicit historical parallel [S]** (p572): "In the early days of computer programming, when machines had pathetically small hard drives and real memories, boundary crashes were common... Boundary crashes for normal database applications have more or less been eliminated, but big data raises this issue again." Hadoop's mitigation is named directly: "you can, for the most part, indefinitely add commodity hardware," though provisioning and networking are still real constraints.

**Public-to-private cloud prototyping, with an explicit named risk and an explicit named limitation [S]** (p572–573): "Just remember not to leave a huge data set online with the public cloud provider over the weekend when the programmers have gone home!" Separately: "in some cases in which you are trying to exploit data locality with rack-aware MapReduce processes, you may not use a public cloud service because it may not provide the data storage control needed."

**10x–100x performance gains named as a recurring, expected pattern, not an occasional bonus [S]** (p573): "Search for and expect tenfold to hundredfold performance improvements over time... When free from being controlled by a big vendor's RDBMS optimizer and inner loop, smart developers can implement spot solutions that are truly 100 times as fast as standard techniques." Named cost: "these individual spot solutions may not be part of a unified single architecture."

**Two named cutting-edge performance-demanding applications [S]** (p573): visualization of full big datasets ("'Flying around' a petabyte of data requires spectacular performance!") and "semantic zooming without pre-aggregations," described as descending from aggregated to progressively detailed levels in unstructured/semistructured data, "analogous to zooming in on a map."

**Resource isolation warning, an explicit named risk [S]** (p573): "be cautious if your big data analytics run on the data warehouse machine because big data requirements change rapidly and inevitably in the direction of requiring more compute resources" — a direct threat to the conventional warehouse's SLA if resources are shared.

**Dimensionalization as a big-data-analytics use case in its own right, with a worked micro-example [S]** (p574): a single Twitter tweet reading "Wow! That is awesome!" may not seem to contain anything worth dimensionalizing, but with some analysis you often can get customer, location, product, marketplace condition, provider, weather, cohort group, session, triggering prior event, and final outcome, "and the list goes on."

Explicit urgency follows (p574): "incoming data should be fully dimensionalized at the earliest extraction step in as close to real time as possible."

**Conformed dimensions explicitly inherited as the top big-data integration technique [S]** (p574): "Conformed dimensions are perhaps the most powerful best practice from the conventional DW/BI world that should be inherited by big data."

The same incremental, nondisruptive rollout method already synthesized from Ch.8 and Ch.19 is explicitly cross-referenced (p575).

**Durable surrogate keys, restated with an explicit "snare and delusion" warning against natural keys [S]** (p575): "These natural keys turn out to be a snare and a delusion in the real world. They are incompatible across applications and are poorly administered, and they are administered by someone else who may not have the interests of the data warehouse at heart." Durability is defined precisely: "there is no business rule that can change the key. The durable key belongs to the DW/BI system, not to the data source."

**Deferred structure declaration, an explicit trade-off with a named ETL reframing [S]** (p575–576): "putting off declaring data structures at the time of loading into Hadoop or a data grid" avoids a resource-intensive premature-structuring step and accommodates legitimately different analyst perspectives on the same data, at the cost that "data without a declared structure may be difficult or impossible to index for rapid access." The eventual RDBMS-bound structuring step "can be thought of as a valuable ETL step," not a conflict with big data's philosophy.

**Name-value pair loading as a concrete escape hatch for unexpected content [S]** (p576): "In many cases, you open the fire hose and discover unexpected or undocumented data content, which you must nevertheless load at gigabytes per second. The escape from this problem is to load this data as simple name-value pairs" — the chapter's own worked example: an applicant declaring "rare postage stamp = $10,000" as a financial asset never seen before, loaded gracefully as a name-value pair despite being completely undocumented.

**Data virtualization's explicit cost/benefit framing [S]** (p576–577): "data virtualization trades off the cost of computing at run time with the cost of ETL to build physical tables before run time." Recommended lifecycle: "expect to materialize the virtual schemas when they have been tested and vetted and the analysts want the performance improvements of actual physical tables."

**There is no such thing as big data governance, an explicit unifying governance principle [S]** (p577): "data governance must be a comprehensive approach for the entire data ecosystem, not a spot solution for big data in isolation."

Named component areas follow (p577): "privacy, security, compliance, data quality, metadata management, master data management, and the business glossary" that exposes definitions and context to the business community.

**Dimensionalize before governing, an explicit sequencing rule extending the earlier dimensionalization best practice [S]** (p577): "The best chance at classifying data in ways that are important to your data governance responsibilities is to dimensionalize it as fully as possible at the earliest stage in the data pipeline. Parse it, match it, and apply identity resolution on-the-fly."

**Privacy named as the single most important governance perspective under specific conditions [S]** (p577): "If you analyze data sets that include identifying information about individuals or organizations, privacy is the most important governance perspective."

"Egregious episodes of compromising the privacy of individuals or groups can damage your reputation, diminish marketplace trust, expose you to civil lawsuits, and get you in trouble with the" law (p577).

A concrete Hadoop-specific caveat follows (p578): "after data is written to Hadoop, Hadoop doesn't manage updates very well. Data should either be masked or encrypted on write (persistent data masking) or data should be masked on read (dynamic data masking)."

## 2. WHAT / WHY / WHEN

**WHAT:** The book's closing chapter, covering big data's defining characteristics and eighteen named use cases, the nineteen technical capabilities a big data system must support, a comparison of the two dominant architectural responses (extended RDBMS vs. MapReduce/Hadoop), and an extensive, explicitly categorized set of best practices across management, architecture, data modeling, and governance — deliberately without prescribing specific dimensional designs for any individual big data use case. `[D]`

**WHY it matters:** the chapter's thesis is continuity, not rupture — it repeatedly argues that the book's core dimensional modeling disciplines (conformed dimensions, durable surrogate keys, SCDs, dimensional thinking itself) remain the most powerful available tools for making big data usable and governable, rather than treating big data as requiring an entirely new discipline. `[D]`

**WHEN to use the extended-RDBMS architecture vs. MapReduce/Hadoop (p566–567):** favor extended RDBMS when data can be structured and relational semantics, transaction processing, and fast indexed lookups matter; favor Hadoop when data volume/variety defeats upfront structuring, full-scan and iterative/complex processing dominate, and transaction processing is not required — the chapter frames these as durably coexisting, not a transitional either/or.

**WHEN to defer data structure declaration vs. structure at load time (p575–576):** defer when structure is genuinely unknown or would force premature, information-destroying normalization, or when legitimately different analyst perspectives must coexist on the same raw data; structure at (or before) load time when rapid indexed access is the priority and the data's shape is already well understood.

## 3. Assumptions and prerequisites

- Assumes conformed dimensions and their incremental, nondisruptive rollout mechanics from Ch.8 (Customer Relationship Management) and Ch.19 (ETL Subsystems and Techniques), directly cross-referenced (p575). `[S]`
- Assumes SCD techniques from Ch.5 (Procurement), directly cross-referenced and reaffirmed as equally important for big data (p576). `[S]`
- Assumes durable surrogate key vocabulary and rationale established across the whole book, directly restated and extended with big-data-specific stakes (p575).
- Assumes multivalued/name-value-pair bridge table treatment from Ch.8 (Figures 8-7/8-8, the loan application example), directly cross-referenced for the name-value pair loading best practice (p576). `[S]`
- Assumes factless fact table and always-1 count fact vocabulary from earlier chapters, implicitly underlying the dimensionalization worked example, though not explicitly re-cited here.

## 4. Mechanism / key steps

**Data highway flow, the chapter's own worked structure (p569–572, Figure 21-3):** raw data enters at the Raw Source cache → moves through ETL processes toward increasingly latent, increasingly clean caches (Real Time → Business Activity → Top Line → DW/Long Time Series), potentially via multiple parallel paths rather than one strict pipeline (e.g. simultaneously feeding a real-time UI and a daily top-line ODS that in turn feeds the DW) → at each ETL step, natural/proprietary keys are replaced with durable surrogate keys ("Job One") so any cache can join back to richer upstream dimensional content → derived summary data can also flow backward down the highway toward earlier, lower-latency caches.

**Sandbox-to-production big data workflow (p568–569, the chapter's own worked example):** data scientists prototype freely in their preferred languages/tools (e.g. custom R code directly accessing Hadoop) → after proof of concept, an IT turnover team reprograms the logic into standardized, supportable technology (e.g. redeployed under a metadata-driven ETL tool running in a scalable, secure grid computing environment) — explicitly requiring IT to tolerate technological diversity during the experimental phase.

## 5. Trade-offs and limitations

- **Extended RDBMS vs. Hadoop, an explicit multi-axis trade-off with no universal winner (§1, p566–567):** cost, structure requirements, lookup speed, relational semantics depth, and transaction processing support all point in opposite directions between the two architectures.
- **Spot-solution performance gains (10x–100x) come at the cost of architectural unity (§1, p573):** the chapter names this tension directly — the same freedom from vendor optimizer constraints that enables dramatic speedups also fragments the overall technology stack.
- **Deferred structure declaration trades indexability for flexibility (§1, p575–576):** an explicit, acknowledged two-sided trade rather than a costless technique.
- **Data virtualization trades runtime computation cost for avoided upfront ETL cost (§1, p576–577):** a genuine engineering trade-off with a recommended resolution (materialize once vetted), not a permanent either/or.
- **Early cleansing vs. preserving interesting outliers, an explicit acknowledged disagreement in the field (§1, p571):** the chapter names the counter-argument rather than presenting its own recommendation as uncontested.

## 6. Failure modes and edge cases

- **Treating new big data types as opaque blobs delivered whole to a downstream BI tool (§1, p566):** explicitly named as insufficient — real integration requires in-database UDF processing, not blob storage alone.
- **Building a long-lasting legacy big data architecture today (§1, p568):** named directly as a mistake given the pace of change in the space — a two-year rehost/reprogram horizon should be assumed instead.
- **Running big data analytics on the same machine as the conventional data warehouse without isolation (§1, p573):** named directly as a threat to warehouse SLAs given big data's inevitably escalating resource demands.
- **Leaving prototype data live on a public cloud unattended (§1, p572–573):** a concrete, named operational risk (cost and exposure) during exploratory cloud prototyping.
- **Storing sensitive data in Hadoop without masking, given Hadoop's weak update support (§1, p578):** named directly as a specific technology-driven privacy risk requiring either write-time or read-time masking as a mitigation.
- **Treating big data governance as a separate, isolated governance track (§1, p578):** explicitly named as a conceptual error — "There is No Such Thing as Big Data Governance" as a standalone heading makes this the chapter's most emphatic warning.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the five-cache data highway model (§1/§4, p569–570) is a directly reusable architectural planning framework for any future low-latency-to-batch data delivery spectrum in this vault's projects, replacing an unconstrained "make it real-time" requirement with named, cost-differentiated tiers. `[D]`
- **Build:** the durable-surrogate-key-first ETL step ("Job One") at every cache transition (§1/§4, p571–572) is a directly reusable build discipline ensuring any future big data pipeline preserves joinability back to richer dimensional content.
- **Maintain:** the sandbox-to-production reimplementation workflow (§4, p568–569) is a directly reusable governance pattern for managing the tension between data-scientist experimentation freedom and long-term supportability.
- **RCA:** unexpectedly poor data completeness or accuracy in a low-latency data feed (§1, p571) is directly diagnosable against the explicit latency/quality trade-off curve — check whether the feed's cache tier inherently limits achievable data quality before assuming a pipeline defect.
- **Optimization:** the explicit expectation of 10x–100x performance gains via spot solutions (§1, p573) is a directly reusable optimization mindset — periodically re-evaluate whether purpose-built, non-RDBMS-optimizer-constrained solutions could dramatically outperform standard techniques for specific big data workloads, while tracking the resulting architectural fragmentation cost.

## 8. How to test / verify these claims

- The name-value pair loading technique's flexibility claim (§1, p576) is directly testable: attempt to load a genuinely novel, previously undocumented attribute (e.g. the chapter's own "rare postage stamp" example) into a name-value pair structure and confirm it loads without schema modification.
- The durable-surrogate-key backflow mechanism (§1, p571–572) is directly testable: confirm that a dimension member's durable key is present and joinable across multiple cache tiers on the data highway.
- The latency/quality trade-off curve (§1, p571) is empirically testable by comparing data completeness/error rates across a real system's real-time, intra-day, and daily-batch feeds of the same underlying data.
- The privacy masking requirement for Hadoop-stored sensitive data (§1, p578) is directly auditable: verify whether persistent (write-time) or dynamic (read-time) masking is actually applied to any Hadoop-resident PII.

## 9. Cross-references

- Directly extends and is fully consistent with conformed dimensions and their incremental rollout from [[ch08_customer_relationship_management|Ch.8]] (Customer Relationship Management) and [[ch19_etl_subsystems_and_techniques|Ch.19]] (ETL Subsystems and Techniques), SCD techniques from [[ch05_procurement|Ch.5]] (Procurement), name-value pair bridge tables from [[ch08_customer_relationship_management|Ch.8]], and durable surrogate key vocabulary established throughout the book — no contradiction found; this chapter explicitly and repeatedly frames itself as inheriting rather than replacing these techniques.
- This is the final chapter of `kimball_dwtoolkit_3e` — the chapter's own closing summary makes no forward chapter reference, consistent with its position as the book's last chapter.
- No unresolved forward-references to not-yet-synthesized chapters were found in this chapter's body; all cross-references point backward to already-synthesized chapters.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figure 21-1 (extended RDBMS architecture diagram), 21-2 (RDBMS vs. Hadoop comparison table), 21-3 (data highway cache diagram) | Structure and content described narratively above where load-bearing (§1, §4); full diagrams not reproduced verbatim. |
| Full 18-item big data use case list (p563–564) | Representative items captured in §1's framing; the complete verbatim list is not separately reproduced since the chapter itself declines to design schemas for each. |
| Full five-cache example application lists (p569–570, ~15 named example applications across the five caches) | Representative examples captured in §1; the complete per-cache lists are not separately reproduced. |
| Chapter summary closing remarks (p578) | Restates points already captured in §1/§2; not separately reproduced. |
