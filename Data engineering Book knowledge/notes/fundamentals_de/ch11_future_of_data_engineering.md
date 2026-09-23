# Ch.11 — The Future of Data Engineering

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 404–415 (12 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 4,759
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**The chapter's own framing of its epistemic status [S]** (p404): explicitly labeled "wild future speculation" alongside "observations of ongoing developments" — the book is careful to distinguish grounded observation from prediction, not present both with equal confidence.

**Cloud-scale data OS analogy [S]** (p406–407, citing Benn Stancil's "The Data OS"): drawing a direct parallel between single-device operating systems (which "orchestrate tasks and processes," provide standard APIs, and "maintain services by monitoring them and restarting them... in case of a failure") and cloud data services (BigQuery, Blob Storage, Snowflake, Lambda) which "resemble operating system services, but at a much larger scale."

**"Enterprisey" data engineering, the chapter's own redefinition of the term [S]** (p408): explicitly not "faceless committees... endless red tape" — instead "some of the good things that larger companies do with data—management, operations, governance, and other 'boring' stuff," now "trickling downstream" to smaller organizations.

**Live data stack, the chapter's own named successor to the MDS [S]** (p410): "will fuse real-time analytics and ML into applications by using streaming technologies, covering the full data lifecycle from application source systems to data processing to ML, and back."

**Stream, transform, and load (STL) [S]** (p411–412, "provisionally" named by the authors): a predicted shift "away from ELT—in database transformations—to something that looks more like ETL," where "extraction is an ongoing, continuous process" in a streaming context.

**Dark matter data [S]** (p413): "Spreadsheets are the dark matter of the data world" — the chapter's own estimate: "the user base of spreadsheets is between 700 million and 2 billion people," with "a good deal of data analytics" running in spreadsheets and "never mak[ing] its way into the sophisticated data systems" described elsewhere in the book.

## 2. WHAT / WHY / WHEN

**WHAT:** The book's closing, explicitly speculative chapter, covering: why the data engineering lifecycle itself is durable even as tools change; the trend toward tool simplification and managed services; a cloud-scale "data OS" analogy and its implications for interoperability standards; "enterprisey" data engineering; the blurring of engineering role boundaries; the predicted shift from the "modern data stack" to a "live data stack"; the fusion of applications with data and ML; and spreadsheets as an under-acknowledged, massive-scale data platform. `[D]`

**WHY it matters:** the chapter's own justification for existing at all, given the field's fast pace: "In this book, we focus on big ideas that we feel will be useful for the next several years... The order of operations and names of best practices and technologies might change, but the primary stages of the lifecycle will likely remain intact for many years to come" (p404). `[S]`

**WHEN the data-engineer role itself is at risk of disappearing (the chapter's own explicit rebuttal, p405):** "Some question whether increasingly simple tools and practices will lead to the disappearance of data engineers. This thinking is shallow, lazy, and shortsighted... If tooling becomes easier to use, data engineers will move up the value chain to focus on higher-level work." The chapter's own analogy: better mobile OS/frameworks "have not eliminated mobile app developers" (p408), only changed what they build.

## 3. Assumptions and prerequisites

- Assumes the full data engineering lifecycle framework from Ch.2 as the stable substrate against which all predictions in this chapter are made — the chapter explicitly reasserts, rather than revisits, that framework (p405). `[D]` (this note's own inference from the chapter's framing; not a direct quote.)
- Assumes streaming DAG and Kappa/Lambda architecture concepts from Ch.8: "building a streaming DAG was an extremely complex process with a high ongoing operational burden" (see Chapter 8) (p408). `[S]`
- Assumes semantic/metrics-layer and data-definition vocabulary from Ch.9: "we expect data modeling will involve some notion of an upstream definitions layer—including semantics, metrics, lineage, and data definitions (see Chapter 9)" (p412). `[S]`
- Assumes batch data-modeling techniques (Kimball/Inmon/Data Vault) from Ch.8 as the baseline the chapter argues is unsuited to streaming: "The traditional batch-oriented data modeling techniques you learned about in Chapter 8 aren't suited for streaming data" (p412). `[S]`

## 4. Mechanism / key steps

**Predicted next-generation orchestration platform capabilities, the chapter's own composite forecast (p407):** current orchestration (Airflow-class) → gains deeper data catalog/lineage awareness → gains IaC capabilities "similar to Terraform" → gains code-deployment features "like GitHub Actions and Jenkins" → engineers write infrastructure specifications directly into pipeline code → missing infrastructure (e.g. a Snowflake database, a Databricks cluster, a Kinesis stream) is provisioned automatically "the first time the pipeline runs." This is presented as a forecast, not a current capability. `[D]` (this note's own step-sequencing of the chapter's described trend.)

## 5. Trade-offs and limitations

- **The modern data stack's core limitation, stated directly (p410):** "the MDS is basically a repackaging of old data warehouse practices using modern cloud and SaaS technologies" and "it has some serious limitations when compared to the potential of next-generation real-time data applications," specifically because it "limits itself to batch techniques that treat data as bounded" (p411).
- **Batch transformation is not being fully replaced, an explicit hedge (p412):** "batch transformations won't entirely go away. Batch will still be very useful for model training, quarterly reporting, and more" — the chapter predicts streaming becoming "the norm," not batch's elimination.
- **BI tools' interactivity gap versus spreadsheets, stated directly (p413–414):** "BI tools have failed to bring comparable interactivity to databases. Users who interact with the UI are typically limited to slicing and dicing data within certain guardrails, not general-purpose programmable analytics" — an explicit, named shortcoming of the current BI-tool category relative to what spreadsheets already offer their power users.
- **The chapter's own explicit epistemic hedge on its predictions (p414):** "Some aspects of our prognostication sit on a relatively secure footing... Other predictions are much more speculative... Perhaps the trend toward real-time data will stall once again, with most companies continuing to focus on basic batch processing." This is a direct, source-stated confidence downgrade on the live-data-stack material specifically, distinguishing it from the lifecycle-durability claims made earlier in the chapter.

## 6. Failure modes and edge cases

- **The "throw it over the wall" anti-pattern between software and data engineering, named as the current failure state the chapter expects to be corrected (p409):** "We will move beyond the 'throw it over the wall' approach that is now pervasive" — describing today's disjointed handoff between application/software engineers and data engineers as an ongoing organizational failure mode, not a hypothetical one.
- **Siloed data-and-application architecture as a present, named problem (p412):** "applications sit in one area, and the MDS sits in another. To make matters worse, data is created with no regard for how it will be used for analytics. Consequently, lots of duct tape is needed to make systems talk with one another. This patchwork, siloed setup is awkward and ungainly."

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the "move up the value chain" framing (§1/§2) is a direct implication for how this vault's own DE-Mastery/portfolio-audit projects should be scoped — as tooling simplifies, the differentiating work shifts toward architecture, data modeling, and cross-system integration rather than low-level plumbing. `[D]`
- **Build:** the STL (stream, transform, load) prediction (§1) is a forward-looking design consideration for any new pipeline built in this vault's projects with streaming source systems — treating extraction as continuous rather than batch-triggered, where source systems support it. `[D]`
- **Maintain:** the chapter's own explicit warning to "keep an eye on vendor announcements... taking all claims with a healthy grain of salt" (p414) is a directly actionable due-diligence discipline consistent with this vault's own No-Guess Rule and the book's earlier benchmark-skepticism material (Ch.4). `[S]`
- **RCA:** N/A — this chapter is forward-looking/speculative rather than diagnostic; no RCA-relevant mechanism is claimed here beyond what earlier chapters already cover. `[D]`
- **Optimization:** the dark-matter-data observation (§1) is a concrete audit prompt for any organization assessing its true analytics footprint — spreadsheet-based analytics workflows should be counted as part of the data estate, not excluded because they sit outside "the sophisticated data systems" the rest of the book describes (p413).

## 8. How to test / verify these claims

- The spreadsheet user-base estimate ("between 700 million and 2 billion people," p413) is explicitly presented by the authors as a range from unspecified external estimates, not a single sourced figure — `[S]` as the book's own reported range, but `[U]` as to the actual current number or its original source.
- The live-data-stack and STL predictions (§1) are, by the chapter's own admission, speculative and not independently testable as of this book's writing (2022) — flagged `[U]` for any claim about their eventual accuracy; only the book's authorship of the prediction is `[S]`.
- The orchestration-platform forecast (§4) is checkable against the current state of Airflow, Dagster, and Prefect's actual feature sets as of any later date — a good candidate for a `check_deferred_refs.py`-style consistency check against more recent sources in this vault (e.g. the DE-Mastery track's real-world Airflow usage) if such a cross-check becomes relevant.

## 9. Cross-references

- Directly extends `fundamentals_de` [[ch02_data_engineering_lifecycle|Ch.2]] (lifecycle framework), [[ch03_designing_good_data_architecture|Ch.3]] (Kappa/Lambda architecture — implicit in the streaming-DAG discussion), [[ch04_choosing_technologies|Ch.4]] (benchmark skepticism, echoed in the "healthy grain of salt" vendor-claims warning), [[ch08_queries_modeling_transformation|Ch.8]] (streaming DAGs, batch data modeling, MapReduce/GFS lineage), [[ch09_serving_data|Ch.9]] (semantic/metrics layers, data definitions) — all previously synthesized, no contradiction found; this chapter functions as an explicit forward-looking synthesis of material established throughout the book rather than introducing new load-bearing technical claims.
- This is the last chapter of `fundamentals_de`'s main body (Chapters 1–11); no further forward references exist within this source. The two appendices (Serialization/Compression, Cloud Networking) were already synthesized earlier in this vault's work. This completes full-scope synthesis of `fundamentals_de`.
- The live-data-stack prediction here directly parallels the `databricks_big_book_4e` Reverse ETL/Lakebase note's operational-analytics framing (both describe closing the gap between analytical and operational systems) — consistent, no contradiction, though the two sources approach the same trend from different angles (this book speculatively, the Databricks source as a current vendor capability). Flagged for `check_deferred_refs.py` as a consistency check once more `databricks_big_book_4e` chapters are synthesized.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figure 11-1 (live data stack architecture diagram) | Described narratively above where load-bearing (§1); diagram not rendered to image for this chapter, consistent with the project-wide `reading_order_risk` finding. |
| "Titles and Responsibilities Will Morph" subsection detail (p408–409, the ML-engineer and software-engineer role-blurring discussion) | Summarized at concept level in §1/§2; the extended narrative discussion of role evolution is not reproduced in full, as it is organizational speculation rather than a falsifiable technical claim. |
| "The Tight Feedback Between Applications and ML" subsection (p412–413) | Summarized at concept level via the live-data-stack material in §1; this subsection's content is a direct extension of that same prediction without introducing distinct new claims requiring separate citation-level synthesis. |
| Footnoted external sources (Benn Stancil's "The Data OS," Ben Rogojan's "Three Data Engineering Experts" article) | Quoted or referenced where load-bearing (§1); source documents not independently retrieved beyond what this chapter quotes. |
| Full Conclusion section's closing remarks (p414–415, career/community-participation advice) | Motivational/career-advice content, not a technical or falsifiable claim requiring citation-level synthesis — summarized only at the level of the chapter's epistemic-hedge framing already captured in §5. |
