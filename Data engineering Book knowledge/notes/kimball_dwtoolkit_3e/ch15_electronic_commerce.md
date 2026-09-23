# Ch.15 — Electronic Commerce

**Source:** `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd ed., Kimball & Ross, Wiley)
**PDF page range:** 389–410 (22 pages, last page blank) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Clickstream framed as a moving target, not a static source [S]** (p389): "The clickstream is not just another data source that is extracted, cleaned, and dumped into the DW/BI environment. The clickstream is an evolving collection of data sources."

**Clock synchronization across distributed web servers, a named concrete problem [S]** (p390): "a very interesting problem arises in synchronizing the log files after the fact. Remember that a busy web server may be processing hundreds of page events per second. It is unlikely the clocks on separate servers will be in synchrony to one-hundredth of a second."

**Basic clickstream data is stateless and anonymous, two named foundational limitations [S]** (p390): "The most basic form of clickstream data from a normal website is stateless. That is, the log shows an isolated page retrieval event but does not provide a clear tie to other page events elsewhere in the log." Separately: "Unless visitors agree to reveal their identity in some way, you often cannot be sure who they are, or if you have ever seen them before."

**Five named session-identification methods, ranked by reliability [S]** (p391–393): (1) host/IP time-contiguity collation — "requires no cookies or special web server features" but "breaks down for websites with large numbers of visitors because dynamically assigned IP addresses may be reused immediately"; (2) session-level browser cookie — but "you can't tell when the visitor returns to the site at a later time in a new session"; (3) SSL-based tracking — requires "high-overhead SSL" and "each host must have its own unique security certificate"; (4) hidden-field session ID in dynamically generated pages — "requires a great deal of control over the website's page generation methods"; (5) persistent cookie — "there is no absolute guarantee that even a persistent cookie will survive" removal. Explicit ranking: "the most reliable method of session tracking from web server log records is obtained by setting a persistent cookie in the visitor's browser."

**Visitor identity, four named concrete obstacles [S]** (p392–393): visitors want anonymity and may not trust the site with personal information; self-reported identity may be inaccurate; "you can't be sure which family member is visiting your site" even with a persistent cookie, since cookies identify a computer, not a person; and "you can't assume an individual is always at the same computer," since different devices carry different cookies for the same person.

**Page dimension grain, an explicit anti-explosion rule [S]** (p394): "We will not create a page row for every instance of a dynamic page because that would yield a dimension with an astronomical number of rows. These rows also would not differ in interesting ways. You want a row in this dimension for each interesting distinguishable type of page."

**Granular element-level tracking as a named extreme-volume case [S]** (p395): "some internet companies track the more granular individual elements on each page of their web sites... A single complex web page can generate hundreds of rows each time the page is served to a visitor... often exceeding 10 terabytes per day!" Gaming is named as a comparable case: "gaming companies may generate a row for every gesture made by every online game player, which again can result in hundreds of millions of rows per day."

**Session dimension's customer-status attribute, an explicit anti-pattern warning [S]** (p395): "Do not put these labels in the customer dimension" — these statuses "may change over very short periods of time" (p396).

The chapter's own fix (p396): "If there are a large number of these statuses, consider creating a separate customer status mini-dimension rather than embedding this information in the session dimension" — directly reapplying the type 4 mini-dimension decision criterion (volatility + size) established in earlier chapters to a new context.

**Session-grain clickstream fact table, an explicit deliberate deviation from the lowest-granularity design principle [S]** (p397): "While we typically encourage designers to start with the most granular data available in the source system, this is a purposeful deviation from our standard practices," justified by scale: "100 million page fetches boil down to 20 million complete visitor sessions."

**Dual date/time roles for universal vs. local wall-clock time, with an explicit rejection of an alternative design [S]** (p398): "you must record all session dates and times, uniformly, in a single time zone such as Greenwich Mean Time (GMT) or Coordinated Universal Time (UTC)," and separately "record the date and time of the session relative to the visitor's wall clock." A customer-dimension time-zone attribute alternative is explicitly rejected: "constraints to determine the correct wall clock time would be horrendously complicated... This is not the business of the BI reporting application to work out. It is the business of the database to store this information."

**Full date/time stamp preferred over a time-of-day dimension for exact instants, an explicit reasoning [S]** (p398–399): "Unlike the calendar date dimension, a time-of-day dimension would contain few if any meaningful attributes... Also, the use of an explicit date/time stamp allows direct arithmetic between different date/time stamps to calculate precise time gaps between sessions, even those crossing days. Calculating time gaps using a time-of-day dimension would be awkward."

**Causal dimension explicitly rejected at session grain, with a precise diagnostic for why [S]** (p399): "if the causal dimension focuses on individual products, it would be inappropriate to add it to this design. The symptom that the causal dimension does not mesh with this design is the multivalued nature of the causal factors for a given complete session." A broader market-conditions causal dimension (not product-specific) is named as compatible with session grain instead.

**Nominal session-end time assignment, an explicit ETL handling rule for unknowable session endings [S]** (p399): "your extract software needs to assign a small and nominal number of seconds to this last session step, so the analysis is not unrealistically distorted" — for cases like a visitor typing a new URL, walking away, or closing the browser, none of which are directly observable from conventional web logs.

**Conformed fact naming discipline, a concrete example [S]** (p401): "If you call both of these measures simply 'seconds,' you risk having these seconds inappropriately added or combined. Because these seconds are not precisely equivalent, you should name them differently as a warning" — distinguishing `Session Seconds` (session-grain fact table) from `Page Seconds` (page-event-grain fact table), with an explicit consistency check: "you would expect the page seconds for a session in this second fact table to add up to the session seconds in the first fact table."

**Null facts as an efficiency non-issue in most systems [S]** (p401): order-related facts "will be zero or null for many rows in this fact table if the specific page event is not the event that places the order."

This is not a real efficiency concern: "In many database management systems, these null facts are handled efficiently and may take up literally zero space in the fact table" (p402).

**Aggregate clickstream fact table, a concrete worked performance estimate [S]** (p403): building a shrunken-rollup aggregate table (grouped by month, demographic type, entry page, session outcome) "results in a drastically smaller fact table, almost certainly less than 1% of the original session-grained fact table... you can expect queries directed to this aggregate table to run at least 100 times as fast."

**Google Analytics framed structurally as an external data warehouse [S]** (p403–404): "Google Analytics (GA) is a service provided by Google that is best described as an external data warehouse that provides many insights about how your website is used." A notable structural convergence is pointed out directly: "GA's detailed technical explanation of the data elements that can be collected through the service are described correctly as either dimensions or measures. Someone at Google has been reading our books…"

**Web profitability built on the sales transaction process, not the clickstream, with the reasoning made explicit [S]** (p406): "You could, as an alternative, try to build web profitability on top of the clickstream, but this would involve an even more controversial allocation process in which you allocate costs down to each session. It would be hard to assign activity and infrastructure costs to a session that has no obvious product involvement and leads to no immediate sale."

A named benefit of the chosen approach follows: "you get a view of profitability across all your sales channels, not just the web" (p406).

**Physical storage decision for derived P&L columns, governed by access pattern [S]** (p407): "If you provide all access through views, you can easily provide the computed columns without physically storing them. But if your users are allowed to access the underlying physical table, you should include net revenue, gross profit, and net profit as physical columns" — the same view-vs-physical-storage reasoning already established for derived facts, now applied to a multi-tier P&L calculation.

**Cost allocation quality varies by cost type, an explicit named spectrum [S]** (p407–408): "Sometimes a cost is only available as a national average, computed for an entire year. Any allocation scheme is going to assign a kind of pro forma value that has no real texture to it. Other costs will be broken down a little more granularly... Finally, some costs may be truly activity-based and vary in a highly dynamic, responsive, and realistic way over time."

**DW/BI team's role scoped explicitly against full activity-based costing [S]** (p408): "The DW/BI team cannot be responsible for implementing activity-based costing (ABC) in a large organization. When the team is building a profitability dimensional model, the team gets the best cost data available at the moment and publishes the P&L... Over time, as the sources of cost improve, the DW/BI team incorporates these new sources and notifies the users that the business rules have improved."

## 2. WHAT / WHY / WHEN

**WHAT:** A web retailer case study covering raw clickstream data challenges (session/visitor identification), four new clickstream-specific dimensions (page, event, session, referral), two clickstream fact tables at different grains (session and individual page event, the latter using the step dimension from Ch.8), an aggregate clickstream fact table, Google Analytics as an external data source, clickstream integration into a full retailer bus matrix, and a cross-channel web profitability P&L schema. `[D]`

**WHY it matters:** the chapter treats the clickstream not as an isolated novelty but as a domain that must be deliberately conformed into the existing enterprise bus architecture — the entire back half of the chapter (bus matrix integration, profitability) exists specifically to argue that "the profitability of the web sales channel can be measured if you allocate the right costs back to the individual sales," i.e., that clickstream analysis is only valuable once integrated with the rest of the business, not in isolation. `[D]`

**WHEN to deviate from lowest-granularity-first design (p397):** deliberately choose a coarser grain (session, not page event, not micro-element) when source volumes are so extreme (100M+ page fetches/day) that starting at the truly atomic grain would be operationally unmanageable for a first iteration — with the explicit caveat that this coarser table alone cannot answer page- or event-level behavioral questions, requiring the finer-grained companion table described next in the chapter.

**WHEN to add a causal dimension to a clickstream fact table (p399):** only at a grain where the causal factor is genuinely single-valued for the fact row — a product-specific promotion causal dimension fits the page-event grain (one product context per page) but not the session grain (multiple products' causal factors could apply within one session); a broader, non-product-specific market-conditions dimension can fit at session grain.

**WHEN to build an aggregate clickstream table (p403):** when frequent business questions require summarizing millions of rows from either atomic-grain table and a DBA-observed performance problem justifies the ~100x query speedup available from a shrunken-rollup aggregate — consistent with the general aggregate-table cost/benefit gating principle already established in Ch.12.

## 3. Assumptions and prerequisites

- Assumes the step dimension technique from Ch.8 (Customer Relationship Management), directly and explicitly reused: "you can add the powerful step dimension described in Chapter 8... The step dimension, originally shown in Figure 8-11, provides the position of the specific page event within the overall session" (p402). `[S]`
- Assumes type 4 mini-dimension volatility/size criteria from Ch.5 (Procurement), directly reapplied to the session dimension's customer-status attribute (p395–396). `[S]`
- Assumes degenerate dimension vocabulary, directly reapplied to the session ID in the page-event fact table: "a degenerate dimension that does not have a join to a dimension table... a unique identifier, with no semantic content" (p401). `[S]`
- Assumes shrunken rollup conformed dimension mechanics from Ch.4 (Inventory), directly reapplied to the month and demographic dimensions in the aggregate clickstream table (p403). `[S]`
- Assumes the P&L fact table structure introduced in Ch.6 (Order Management), directly cross-referenced: "It is organized as a simple profit and loss (P&L) statement (refer to Figure 6-14)" (p406). `[S]`
- Assumes sales transaction fact table grain and dimensionality from earlier retail-focused chapters, directly extended for the cross-channel profitability schema (p406).
- Assumes role-playing date dimension mechanics established across multiple earlier chapters, directly reapplied for universal-vs-local time (p398).

## 4. Mechanism / key steps

**Two-fact-table clickstream design, the chapter's own worked progression (p397–402):**
1. Build a session-grain fact table first (date/time ×2 roles, customer, entry page, session, referrer; facts: session seconds, pages visited, orders placed, order quantity, order dollars) — deliberately coarser than the source data to keep initial row counts manageable.
2. Build a page-event-grain fact table second (adds page, event, session ID degenerate dimension, three step-dimension roles, product, promotion; facts: page seconds, order quantity, order dollars) — the true lowest-practical-granularity table, enabling page- and behavior-level analysis the session table cannot support.
3. Name conformed facts distinctly across the two tables (`Session Seconds` vs. `Page Seconds`) specifically to prevent accidental cross-table addition, while ensuring their values reconcile (page seconds should sum to session seconds).

**Aggregate table construction from the session-grain fact table (p403, the chapter's own worked example):** group the atomic session-grain fact table by month, demographic type, entry page, and session outcome → count sessions and sum all additive facts → result in a table "almost certainly less than 1%" the size of the source table, connected to shrunken conformed rollup dimensions (month as a conformed subset of the date dimension, demographic as a conformed subset of the customer dimension).

**Web profitability P&L construction (p406–408, the chapter's own worked cascade):** start from gross revenue (units × list price) → subtract manufacturer's allowance, marketing promotion, and markdown to get net revenue → subtract manufacturing/acquisition cost and storage cost to get gross profit → continue subtracting freight cost, special deal cost, and other overhead (including allocated website infrastructure costs) to get net profit → store or view-compute the intermediate derived columns depending on whether users access the fact table directly or only through views.

## 5. Trade-offs and limitations

- **Every session-identification method carries a named specific weakness (§1, p391–393):** no method is presented as strictly superior in all conditions — IP-collation fails under high traffic and shared/dynamic IPs, transient cookies lose cross-session continuity, SSL tracking imposes overhead and certificate requirements, hidden-field IDs require tight control over page generation, and persistent cookies can still be cleared or refused.
- **The session-grain fact table cannot answer page- or event-level behavioral questions (§1, p400):** an explicit, named limitation of the deliberately coarser first design — "analysts cannot ask questions about visitor behavior or individual pages" from it alone, requiring the companion page-event table.
- **Website infrastructure cost allocation is inherently approximate (§1, p407–408):** classic infrastructure costs "are therefore difficult to allocate directly to the product and customer activity," and multiple allocation schemes (by page count, by pages visited, by actual purchases) are all named as plausible but imperfect options, with cost data quality itself varying from "pro forma" national averages to genuinely activity-based figures.

## 6. Failure modes and edge cases

- **Clock drift across distributed web servers corrupting session reconstruction (§1, p390):** a concrete, named synchronization failure mode specific to clickstream data that has no equivalent in most other business processes covered in this book.
- **IP-based session collation breaking down under dynamic IP reuse and shared sessions across multiple IPs (§1, p391):** a named concrete failure mode for the least reliable of the five session-identification methods.
- **Assuming a persistent cookie reliably identifies an individual rather than a device (§1, p392–393):** named directly as a false assumption — multiple people can share one cookie-bearing device, and one person's identity fragments across multiple cookie-bearing devices.
- **Embedding volatile, short-lived customer-status labels directly in the customer dimension (§1, p395–396):** an explicitly named anti-pattern given the churn rate of such labels — reinforces the same volatility-based mini-dimension criterion documented in Ch.5 and Ch.10.
- **Naming two non-equivalent additive facts identically across related fact tables (§1, p401):** a concrete, named data-quality risk (`Session Seconds` vs. `Page Seconds` collision) that could cause incorrect cross-table aggregation if not deliberately avoided through distinct naming.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the deliberate coarser-grain-first exception (§1/§2, p397) is a directly reusable design precedent for any future extremely-high-volume event stream in this vault's projects, provided a finer-grain companion table is explicitly planned rather than treated as optional. `[D]`
- **Build:** the two-tier session/page-event clickstream design (§4) is a directly reusable reference architecture for any web analytics pipeline needing both aggregate behavioral summaries and granular page-level analysis.
- **Maintain:** the conformed-fact-naming discipline (§1/§5, p401) is a directly reusable maintenance guardrail whenever two related fact tables at different grains carry facts that are related but not numerically interchangeable.
- **RCA:** unexplained discrepancies between session-level and page-level time totals (§4) are a direct diagnostic check against the documented reconciliation expectation ("page seconds... should add up to the session seconds") — a mismatch signals an ETL or session-boundary-detection bug rather than a data-quality inevitability.
- **Optimization:** the aggregate table's ~100x speedup estimate (§1, p403) is a directly reusable optimization benchmark and cost/benefit reference point when evaluating whether a similar aggregate is worth building for another high-volume atomic fact table.

## 8. How to test / verify these claims

- The page-seconds-to-session-seconds reconciliation expectation (§1, p401) is directly testable: sum `Page Seconds` for all page events within a session and compare against that session's `Session Seconds` value in the companion fact table.
- The aggregate table size and performance claims (§1, p403, "<1% size," "100x faster") are directly reproducible by building the described aggregate from a real session-grain dataset and measuring both row count reduction and query latency.
- The null-fact storage efficiency claim (§1, p401–402) is directly testable against a specific target database engine by comparing physical storage size for a fact table with a high proportion of null numeric columns versus fully populated rows.
- The five session-identification methods' relative reliability ranking (§1, p391–393) is testable via a controlled multi-session browsing experiment comparing each method's ability to correctly attribute page events to true sessions.

## 9. Cross-references

- Directly reuses and is fully consistent with the step dimension from [[ch08_customer_relationship_management|Ch.8]] (Customer Relationship Management), mini-dimension volatility criteria from [[ch05_procurement|Ch.5]] (Procurement), degenerate dimension vocabulary established across multiple chapters, shrunken rollup conformed dimensions from [[ch04_inventory|Ch.4]] (Inventory), and the P&L fact table structure from [[ch06_order_management|Ch.6]] (Order Management) — no contradiction found; this chapter is a direct, explicit continuation and integration exercise built on these prior techniques.
- The chapter's own text explicitly signals the next chapter is a recap chapter: "In the next chapter, we'll turn our attention to the primary business processes in an insurance company as we recap many of the dimensional modeling patterns presented throughout this book" (p409) — [[ch16_insurance|Ch.16]] is expected to be a consolidation chapter, consistent with [[ch11_telecommunications|Ch.11]]'s and [[ch13_education|Ch.13]]'s similar consolidation roles.
- No unresolved forward-references to not-yet-synthesized chapters beyond the explicit [[ch16_insurance|Ch.16]] pointer were found in this chapter's body.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 15-1 through 15-9 (page/event/session/referral dimension attribute tables, both clickstream fact table schemas, aggregate fact table schema, bus matrix, P&L fact table schema) | Structure and content described narratively above where load-bearing (§1, §4); full attribute tables, sample data values, and the bus-matrix X-grid not reproduced verbatim. |
| Full list of candidate web retailer dimensions (p392–393, 16 items) | Representative items (the four clickstream-unique ones: page, event, session, referral) captured in §1; the full 16-item list is not separately reproduced since most are already-covered dimension types from earlier chapters. |
| Full bus matrix business process list for the web retailer (p404–405, ~20 rows) | Overall structure and key integration point (clickstream sharing conformed dimensions with adjacent processes) captured in §1; the complete row list is not reproduced verbatim. |
| Full P&L worked query list (p408, 7 example questions) | Representative questions captured in §1; complete list not separately reproduced. |
| Chapter summary closing remarks (p409) | Restates points already captured in §1/§2; not separately reproduced. |
