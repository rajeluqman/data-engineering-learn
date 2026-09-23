# Ch.19 — ETL Subsystems and Techniques

**Source:** `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd ed., Kimball & Ross, Wiley)
**PDF page range:** 479–532 (54 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**"It depends" named as a dangerous excuse [S]** (p479): "the 'it depends' response is dangerous because it becomes an excuse to take an unstructured approach to developing an ETL system, which in the worse-case scenario results in an undifferentiated spaghetti-mess of tables, modules, processes, scripts, triggers, alerts, and job schedules. This 'creative' design approach should not be tolerated."

**34 subsystems, four functional groups [S]** (p486): **Extracting** (subsystems 1–3, "Gathering raw data from the source systems"); **Cleaning and conforming** (4–8, "improve the quality of the data received from the source, and merging data from two or more sources to create and enforce conformed dimensions and conformed metrics"); **Delivering** (9–21, "Physically structuring and loading the data into the presentation server's target dimensional models"); **Managing** (22–34, "Managing the related systems and processes of the ETL environment in a coherent manner").

**Ten requirements areas to round up before designing, each a real gating constraint [S]** (p479–485): business needs (KPIs and drill paths from requirements), compliance (chain-of-custody documentation, named directly: "list those data inputs and data transformation steps for which you must maintain the 'chain of custody'"), data quality (three converging named forces: cultural demand for data-driven management, distributed/disparate sources, tightened compliance), security (an explicit tension: "the data warehouse seeks to publish data widely to decision makers, whereas the security interests assume data should be restricted to those with a need to know"), data integration (conforming dimensions and facts), data latency (a named architectural discontinuity: "if the data latency requirement is sufficiently urgent, the ETL system's architecture must convert from batch to microbatch or streaming-oriented. This switch isn't a gradual or evolutionary change; it's a major paradigm shift"), archiving and lineage (a named default rule: "All staged data should be archived unless a conscious decision is made that specific data sets will never be recovered in the future"), BI delivery interfaces (an explicit named anti-pattern: "The most elementary and serious error is to hand across a full-blown, normalized physical model and walk away from the job"), available skills, and legacy licenses.

**Data quality reframed as a business-process symptom, not a data-entry failing [S]** (p491): paraphrasing Michael Hammer's *Reengineering the Corporation*: "Seemingly small data quality issues are, in reality, important indications of broken business processes." A worked counterexample shows why input-format constraints alone fail: forcing a valid-looking Social Security number format just causes clerks to "type in an artificial number that passes the roadblock" when the real number is unknown.

**Nine-step data quality culture template [S]** (p492): declare high-level commitment; drive process reengineering at the executive level; spend money on the data entry environment, application integration, and process change; promote end-to-end team awareness and interdepartmental cooperation; publicly celebrate data quality excellence; continuously measure and improve.

**Three quality screen categories, Jack Olson's taxonomy [S]** (p493): column screens "test the data within a single column" (e.g. unexpected nulls, out-of-range values, format violations).

Structure screens "test the relationship of data across columns" (p493), e.g. hierarchy many-to-one validity, foreign-key/primary-key relationships, address block validity.

Business rule screens implement "more complex tests that do not fit the simpler column or structure screen categories" (p494), including time-dependent rules and aggregate threshold checks.

**Three quality-screen error responses, explicitly ranked [S]** (p494): halt the process, suspend to a file, or tag and pass through — "The third choice is by far the best choice, whenever possible."

Suspending to a file is named directly as "often a poor solution because it is not clear when or if these records will be fixed and re-introduced" (p494).

**Error event schema, fact table grain [S]** (p495): "the grain of a fact table is the physical description of why a fact table row exists. Thus every quality screen error produces exactly one row in this table, and every row in the table corresponds to an observed error." A second, lower-grain error event detail fact table exists so "a complex structure or business rule error that triggers a single error event row in the higher level error event fact table may generate many rows in this error event detail fact table."

**Deduplication and survivorship, defined [S]** (p497): "Survivorship is the process of combining a set of matched records into a unified image that combines the highest quality columns from the matched records into a conformed row."

This requires "clear business rules that define the priority sequence for column values from all possible source systems" (p497).

**Conforming dimensions, an explicitly agile-compatible process [S]** (p497): "For two dimensions to be conformed, they must share at least one common attribute with the same name and same contents. You can start with a single conformed attribute such as Customer Category and systematically add this column in a nondisruptive way to customer dimensions in each of the customer-facing processes."

**Slowly changing dimension manager, three-plus-four techniques with distinct ETL mechanics [S]** (p500–505): type 1 overwrite (with an explicit performance warning: "Some ETL tools contain UPDATE else INSERT functionality... can be a performance killer. For maximum performance, existing row UPDATEs should be segregated from new row INSERTs"); type 2 add new row (requiring five housekeeping columns: change date, row effective date/time, row end date/time, reason for change, current flag; an explicit correction: "Always use the system or as-of date to derive the type 2 effective time stamps," never a possibly-unreliable last-modified field); type 3 add new attribute; type 4 mini-dimension; type 5 (type 4 plus a type 1 outrigger key embedded in the base dimension); type 6 (a type 1 attribute embedded directly in a type 2 dimension); type 7 (dual type 1/type 2 keys in the fact table itself, using a foreign durable key alongside the normal surrogate key).

**Surrogate key generation, an explicit named anti-pattern [S]** (p505–506): "Avoid the temptation of concatenating the operational key of the source system and a date/time stamp. Although this approach seems simple, it is fraught with problems and ultimately will not scale."

**Hierarchy manager, fixed vs. ragged, with a staging-area exception to the no-snowflake rule [S]** (p506): "Snowflakes or normalized data structures are not recommended for the presentation level. However, the use of a normalized design may be appropriate in the ETL staging area to assist in the maintenance of the ETL data flow for populating and maintaining the hierarchy attributes."

**User-maintained dimensions, an explicit named ownership failure and its fix [S]** (p509): "The ETL team often ends up with stewardship responsibility for these dimensions, but this is typically not successful because the ETL team is not aware of changes that occur to these custom groupings, so the dimensions fall into disrepair and become ineffective."

The fix pairs business-department ownership with a maintenance UI, plus a specific default-value convention (p509): the ETL process should create a unique default description concatenating the phrase Not Yet Assigned with the surrogate key value, so that "multiple unassigned values do not inadvertently get lumped together in reports and aggregate tables."

**Three fact table loader types, each with distinct ETL mechanics [S]** (p509–511): transaction (largest/most detailed; simple time stamp; partitioned by time; late-arriving and update handling via insert-then-delete using a sequential surrogate key); periodic snapshot (single period-representing date column; can be loaded en masse at period end or as a "hot rolling periodic snapshot" continuously updated through the period, "difficult to implement if the business rules for calculating the balances at the period end are complex"); accumulating snapshot (destructively modified as the pipeline progresses; a named physical-storage caveat: "Repeated updates to accumulating snapshot fact rows may cause the rows to grow due to these variable row lengths, affecting the residency of disk blocks. It may be worthwhile to occasionally drop and reload rows").

**Surrogate key pipeline mechanics [S]** (p512): dimension tables must be updated before the fact table lookup: "In that way, the dimension tables are always the legitimate source of primary keys you must replace in the fact table (refer to Figure 19-11)."

A named late-arriving-data caveat follows for historical reloads or late-arriving facts (p513): "you need to create logic to find the surrogate key that applied at the time the fact record was generated. This means finding the surrogate key where the fact transaction date is between the key's effective start date and end date." This is not simply the current key.

**Late arriving fact vs. late arriving dimension, two distinct problems [S]** (p514): late facts require "search back in history to decide which dimension keys were in effect when the activity occurred" and possibly adjusting semi-additive balances in subsequent rows; late dimensions require choosing between waiting (acceptable in batch-latency environments) or assigning a placeholder dimension row with dummy attributes later corrected via type 1 overwrite — explicitly preferred over pointing to a shared default row, since the latter "has the same unpleasant side effect... of requiring destructive updates to the fact rows' foreign keys."

**Dimension manager / fact provider split, an explicit division of authority [S]** (p515–517): the dimension manager is "a centralized authority who prepares and publishes conformed dimensions," responsible for implementing agreed labels, adding new/type-2 rows, modifying type-1/type-3 rows in place, versioning, and replicating to all fact providers simultaneously; the fact provider "must be using conformed dimensions provided by the dimension manager" and is responsible for receiving/updating local copies, loading fact rows with correct surrogate keys, invalidating and recalculating aggregates, quality-assuring the result, and notifying users of what changed.

**OLAP cube loading order and SCD compatibility, an explicit warning repeated for emphasis [S]** (p518): "the relational schemas are the best and preferred source for OLAP cubes" loaded after conventional ETL completes. "Type 2 SCDs fit an OLAP system well because a new surrogate key is just treated as a new member. Type 1 SCDs that restate history do not fit OLAP well. Overwrites to an attribute value can cause all the cubes using that dimension to be reprocessed in the background, become corrupted, or be dropped. Read this last sentence again."

**Three ETL management goals [S]** (p519): reliability ("must run to completion to provide data on a timely basis that is trustworthy"), availability (meeting SLAs), manageability ("A successful data warehouse is never done. It constantly grows and changes along with the business").

**Job scheduler's five named service capabilities [S]** (p520): job definition (dependency sequencing), job scheduling (time- and event-based), metadata capture, logging (preferably to a database, "because the structure makes it easier to create graphs and reports"), and notification (interfacing to problem escalation).

**Backup, archive, and recovery, several concrete named practices [S]** (p521–524): backup must provide high performance, simple administration, and automated lights-out operation; archiving is framed as "a cost-benefit issue" and its own "security blanket," with a named compliance-driven retention horizon of "five, 10, or perhaps even 50 years"; fact table surrogate keys enable clean insert-then-delete corrections and fast crash-recovery restart by range-constraining on key sequence.

**Version control and migration, an explicit dev-test-production discipline [S]** (p524): "Ideally, the test system is identically configured to its corresponding production system. Everything done to the production system should have been designed in development and the deployment script tested on the test environment."

**Workflow monitor's ordered bottleneck checklist, directly cross-referenced to Ch.20 [S]** (p525): the list is "ordered starting with the most important bottlenecks:"

The named bottlenecks include poorly indexed source queries, wrong optimizer choice from SQL syntax, insufficient RAM causing thrashing, RDBMS-side sorting, slow transformation steps, excessive I/O, unnecessary write-then-read cycles, non-incremental aggregate rebuilds, change data capture filtering applied too late in the pipeline, untapped parallelization opportunities, unnecessary transaction logging, and network/file-transfer overhead (p525–526).

**Lineage vs. dependency analysis, precisely distinguished [S]** (p526): lineage traces backward "identify the source of that data element... and all transformations... undergone"; dependency traces forward "identify all downstream intermediate tables and final BI reports containing that data element or its derivations."

**Problem escalation, a four-tier support structure [S]** (p527–528): help desk → systems administrator/DBA → ETL manager → ETL developer, in ascending order of last resort.

**Security, an explicit insider-threat framing [S]** (p528): "A serious security breach is much more likely to come from within the organization than from someone hacking in from the outside... the folks on the ETL team present as much a potential threat as any group inside the organization."

**Compliance manager, the type 1/type 3 death sentence [S]** (p529): "The compliance requirements may mean you cannot actually change any data, for any reason... The big impact of these compliance requirements on the data warehouse can be expressed in simple dimensional modeling terms. Type 1 and type 3 changes are dead. In other words, all changes become inserts. No more deletes or overwrites." The mechanism: augment the fact table with a surrogate key, begin/end version date-time, a change reference, and a source reference, converting any would-be overwrite into a fact-table-level type 2 change.

**Metadata repository manager, a balance principle [S]** (p531): "Develop a balanced strategy between doing nothing and doing too much."

## 2. WHAT / WHY / WHEN

**WHAT:** The book's most comprehensive single-chapter architecture reference — ten ETL requirements-gathering areas, then all 34 named ETL subsystems grouped into extracting (1–3), cleaning/conforming (4–8), delivering (9–21, including the full SCD type 1–7 taxonomy and the three fact table loader types), and managing (22–34, covering scheduling, backup, recovery, versioning, monitoring, security, compliance, and metadata). `[D]`

**WHY it matters:** the chapter's own framing is explicit — ETL is not a vague, situational "it depends" activity but a structured discipline with 34 recurring, nameable components present "in almost every dimensional data warehouse back room," which the authors offer specifically to prevent the "spaghetti-mess" outcome of ad hoc ETL design. `[D]`

**WHEN to convert from batch to streaming/microbatch architecture (p483):** only when data latency requirements are genuinely urgent enough to demand it — explicitly not a gradual tuning change but "a major paradigm shift in which almost every step of the data delivery pipeline must be re-implemented." This decision should not be made incrementally or lightly.

**WHEN to use each SCD variant, restated from Ch.5 with ETL-specific mechanics added here:** type 1 for corrections with no history need; type 2 as "the main workhorse technique" for accurate tracked change; type 3 for soft, dual-reference changes; type 4 for rapidly-changing attribute clusters split into a mini-dimension; types 5–7 for combining current-value convenience with full type-2 history in various structural forms.

## 3. Assumptions and prerequisites

- Assumes the three basic SCD techniques from Ch.5 (Procurement), directly cross-referenced and extended with full ETL mechanics for all seven types (p500). `[S]`
- Assumes surrogate key rationale from Ch.3 (Retail Sales), directly cross-referenced (p505). `[S]`
- Assumes conformed dimensions and facts from Ch.4 (Inventory), directly cross-referenced for the conforming subsystem (p499). `[S]`
- Assumes the audit dimension concept from Ch.6 (Order Management), directly cross-referenced (p497). `[S]`
- Assumes multivalued dimension bridge tables from Ch.8 (Customer Relationship Management) and weighting factors from Ch.10 (Financial Services), directly cross-referenced for the bridge table builder subsystem (p513–514). `[S]`
- Assumes ragged hierarchy bridge tables from earlier chapters, directly cross-referenced for the hierarchy manager (p505).
- Forward-references data quality/low-latency trade-offs and ETL performance tuning specifics to Ch.20 (ETL System Design and Development Process and Tasks) (p482, p525).

## 4. Mechanism / key steps

**Type 2 SCD surrogate key management flow, the chapter's own worked diagram (Figure 19-4, p500–502):** source extract → CRC compare against the master dimension cross-reference to detect changes → if CRCs match, ignore → if CRCs differ, find the specific changed field(s) → if the field is type 1 or type 3, update the dimension attribute in place → if the field is type 2, insert a new row, assign a new surrogate key, set the housekeeping dates/current-flag, and update the prior most-recent row's end-effective date and current flag → update the most-recent surrogate key map table used by the surrogate key pipeline.

**Surrogate key pipeline flow, the chapter's own worked diagram (Figure 19-11, p512–513):** ensure all dimension tables are fully updated first → for each incoming fact row, replace every natural key (date, product, store, promotion, etc.) with its current surrogate key by looking up the dimension table (ideally pinned in memory) → route any referential integrity failures or key collisions to a data quality screen for halt/suspend/tag resolution → discard the natural keys entirely from the fact row → load the fully surrogate-keyed row.

**Compliance-enabled fact table conversion, the chapter's own worked mechanism (Figure 19-12, p529–530):** add five columns to an existing fact table (fact table surrogate key, begin version date/time, end version date/time, change reference key, source reference key) → on initial load, set begin version to creation time, end version to a far-future sentinel, change reference to "original" → on any would-be overwrite, insert a new row sharing the same fact table surrogate key with updated columns and a new begin version time, then close out the prior row's end version time to match → any historical query constrains to a point in time and/or a specific fact table surrogate key sorted by begin version date/time to reconstruct the full change history.

## 5. Trade-offs and limitations

- **Suspense files for error handling are explicitly discouraged as a default (p494):** "We recommend not using the suspense file for minor data transgressions" — tagging and passing through is preferred except when data is genuinely unusable downstream.
- **Type 1 overwrites require rebuilding all affected aggregates; type 2 additions made in the present, not backdated, do not (p502):** a concrete, named asymmetry in downstream aggregate maintenance cost between SCD techniques.
- **Extract-to-stream vs. extract-to-file, a genuine trade-off (p490):** streaming is "more appealing" but file-based extraction is easier to restart, easier to encrypt/compress before transfer, and easier to verify via row-count comparison — the chapter names file-based extraction's advantages explicitly rather than treating streaming as strictly superior.
- **Compression before encryption, not after, an explicit ordering constraint (p491):** "Remember to compress before encrypting because encrypted files do not compress very well" — a concrete operational sequencing rule, not a stylistic preference.
- **The compliance-enabled fact table format is a significant structural addition that need not be the primary operational table (p530–531):** it can exist purely in the background alongside a normal, unindexed-for-compliance version used for regular BI queries, avoiding unnecessary overhead when compliance demonstration is only occasionally needed.

## 6. Failure modes and edge cases

- **Loading records based purely on a timed extract, an explicitly named unreliable technique (p488):** "This process is horribly unreliable. Time-based data selection loads duplicate rows when it is restarted from mid-process failures... if the nightly load process fails to run and skips a day, there's a risk that the missed data will never make it into the data warehouse."
- **DBA emptying a full transaction log during log-scraping-based CDC (p489):** named directly as destroying all unprocessed transactions within it — "when a log is emptied, all transactions within them are lost."
- **Assigning a fact row to a shared default dimension row for an unknown late-arriving entity (p514):** named directly as requiring the same costly destructive fact-key updates later as leaving the row unresolved — a placeholder dimension row with its own surrogate key is the preferred alternative.
- **Everyone or no one having production warehouse admin access (p528–529):** the chapter names both extremes as observed real failure patterns: "We've seen situations where no one on the team had security privileges; in other cases, everyone had access to everything."
- **ETL team members treated as a low insider-threat group (§1, p528):** explicitly corrected — internal breaches, including from the ETL team itself, are named as more likely than external hacking.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the ten ETL requirements-gathering areas (§1, p479–485) are directly reusable as a pre-design checklist for any new ETL system in this vault's projects, each representing a potential "showstopper" if skipped. `[D]`
- **Build:** the full SCD type 1–7 ETL mechanics (§1/§4, p500–505) and the surrogate key pipeline flow (§4, p512–513) are directly reusable implementation blueprints for any dimensional ETL build.
- **Maintain:** the dimension manager / fact provider authority split (§1, p515–517) is a directly reusable governance model for maintaining conformed dimensions across multiple fact tables or systems over time.
- **RCA:** the ordered ETL bottleneck checklist (§1, p525–526) is a directly reusable diagnostic sequence for investigating slow-running ETL jobs, prioritized by the chapter's own experience-based ranking rather than guesswork.
- **Optimization:** the explicit compress-before-encrypt ordering rule (§5, p491) and the incremental-vs-full aggregate rebuild distinction tied to dimension version numbers (§1, p516) are both directly reusable, concrete optimization rules.

## 8. How to test / verify these claims

- The type 2 SCD five-housekeeping-column pattern (§1, p502) is directly testable: apply a type 2 change to a test dimension and confirm the prior row's end-effective date and current flag update correctly while a new row is created with a new surrogate key.
- The surrogate-key-pipeline historical-lookup rule (§1, p513) is directly testable: reload a historical or late-arriving fact record and confirm the correct period-appropriate surrogate key is selected via the effective-date range, not the current key.
- The compliance-enabled fact table mechanism (§4, p529–530) is directly testable by construction: apply a simulated overwrite to a compliance-enabled table and confirm the full before/after state is reconstructable by querying a specific point in time.
- The timed-extract unreliability claim (§6, p488) is directly reproducible: simulate a mid-process failure and restart under a SYSDATE-1-style extract and confirm duplicate rows are loaded.

## 9. Cross-references

- Directly extends and is fully consistent with SCD techniques from [[ch05_procurement|Ch.5]] (Procurement), surrogate keys from [[ch03_retail_sales|Ch.3]] (Retail Sales), conformed dimensions/facts from [[ch04_inventory|Ch.4]] (Inventory), the audit dimension from [[ch06_order_management|Ch.6]] (Order Management), and multivalued bridge tables with weighting factors from [[ch08_customer_relationship_management|Ch.8]] (Customer Relationship Management) and [[ch10_financial_services|Ch.10]] (Financial Services) — no contradiction found; this chapter is the detailed ETL-mechanics counterpart to dimensional modeling techniques already synthesized.
- The chapter's own text signals the very next chapter is a direct continuation: "In the next chapter we will describe the processes and tasks for building the ETL system" (p532), confirming [[ch20_etl_system_design_and_development_process_and_tasks|Ch.20]] covers the practical ETL system design and development process, consistent with the CHAPTER_MAP's remaining table of contents.
- No unresolved forward-references beyond the explicitly noted [[ch20_etl_system_design_and_development_process_and_tasks|Ch.20]] pointer were found in this chapter's body.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 19-1 through 19-12 (error event schema, audit dimension sample, conforming process flow, SCD types 2–7 diagrams, junk dimension architecture, surrogate key pipeline diagram, compliance-enabled fact table diagram) | Structure and content described narratively above where load-bearing (§1, §4); full diagrams not reproduced verbatim. |
| Full ten-requirements-area NOTE checklists (p480–485, verbatim checklist text for each area) | Representative content and the core rule for each area captured in §1; the complete verbatim checklist wording is not reproduced. |
| Special dimensions manager's full catalogue of dimension types (date/time, junk, mini, shrunken subset, small static, user-maintained) (p505–509) | Representative named types and their ETL handling captured in §1; not every sub-type's full detail is separately expanded given most mechanics directly parallel already-synthesized dimensional modeling techniques. |
| Chapter summary closing remarks (p532) | Restates points already captured in §1/§2; the forward-pointer to Ch.20 is captured in §9. |
