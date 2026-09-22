# Ch.12 — iFood: Transforming Data to Elevate Food Deliveries and Experiences

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; customer case study, no individual author byline)
**PDF page range:** 106–109 (4 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**iFood's reported migration results** [S]: "67% [reduction in processing and storage costs] / 70% [reduction in maintenance efforts] / 30% [less coding time]."

(p106)

**Legacy-to-current event-volume growth** [S]: "a legacy architecture capable of handling 100 million events per day was now overwhelmed by a surge of 8 billion–10 billion events daily."

(p107)

**Medallion architecture at iFood** [S]: "The Bronze layer consolidates data from various platforms into a single table per product, using a predefined schema partitioned by processing date... In the Silver layer, iFood applies Spark Declarative Pipelines expectations and quality rules to validate the data... By replacing traditional partitioning with Liquid Clustering, all events for a product are consolidated into a single table."

(p108-109)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this is a vendor customer case study describing how iFood (a Brazilian food-delivery platform) migrated its data pipelines from a fragmented, legacy architecture to Spark Declarative Pipelines on a medallion (Bronze/Silver/Gold) architecture, reporting specific cost, maintenance, and coding-time reductions.

**WHY** [S]: iFood "needed a more reliable, scalable and efficient data platform to meet the growing demand for real-time insights and innovation"

(p106), driven by data volume growth described elsewhere in the chapter (p107).

**WHEN** [D]: relevant as a reference case when evaluating Spark Declarative Pipelines for a high-volume (billions-of-events-per-day), multi-source streaming ingestion use case, or when considering consolidating a large number of fragmented tables/pipelines under a medallion architecture.

## 3. Assumptions and prerequisites

- [U] This is a vendor-published customer success story (marketing content co-produced with the customer), not an independent case study; all quantitative claims (67%/70%/30% figures, 210TB/800-billion-record table, cost reduction "from tens of thousands to just thousands of dollars per month") are self-reported by iFood/Databricks and not independently audited in this chapter.
- Assumes the reader has context on Spark Declarative Pipelines and the medallion (Bronze/Silver/Gold) architecture pattern from earlier chapters in this source; neither is re-derived here.
- The specific scale figures (300,000 drivers, 55 million users, 350,000 restaurant partners, 10 billion daily events) are iFood's reported figures at time of publication and should be treated as a point-in-time snapshot, not necessarily current (p106-107).

## 4. Mechanism / key steps

1. Diagnose the pre-migration problem: a fragmented architecture with data spread across "multiple systems" (order management system, consumer app, driver app) lacking proper governance, requiring "significant engineering effort to manually code, optimize and maintain complex workflows," with frequent out-of-memory errors during high-volume ingestion causing "frequent driver shutdowns and operational disruptions" (p107).

2. Migrate to a declarative pipeline model: adopt Spark Declarative Pipelines so engineers "describe their desired transformations in simple code," letting the platform "automatically handle the operational complexity behind these pipelines, including execution, scaling and monitoring" (p107).

3. Consolidate the data model: reduce "the number of tables from nearly 4,000 to just 100" as part of the pipeline consolidation, simplifying governance and improving the foundation for data quality (p107).

4. Ingest at scale via Amazon Kinesis into Spark Declarative Pipelines: real-time events from the consumer app, delivery driver app, and partner portal flow through Kinesis queues at "approximately 10 billion records" ingested daily, with the declarative ingestion pipeline reducing "ingestion latency from hours to seconds" (p108).

5. Structure the medallion layers for scale: Bronze consolidates data into one table per product (predefined schema, partitioned by processing date, acting as an extended-retention staging zone beyond the message queues); Silver applies SDP expectations/quality rules and uses Liquid Clustering (replacing traditional partitioning) to consolidate all of a product's events into a single table, supporting tables as large as "210TB and 800 billion records" (p108-109).

6. Enable self-service analytics: business analysts in growth/product teams access Silver-layer data directly to build Gold-layer analytical tables for user-journey analysis, A/B testing, and driver-app usability insights, without needing data engineering intervention for each new analysis (p109).

## 5. Trade-offs and limitations

- [U] As vendor-published case-study content, this chapter presents no trade-offs, limitations, or challenges encountered during or after the Spark Declarative Pipelines migration — every outcome is framed positively, with no discussion of migration cost, risk, or any residual pain points beyond what's explicitly named as "upcoming initiatives" (p109).
- The chapter reports planned future work (DABs adoption, serverless computing, column masking for sensitive data, variant-type handling for complex structures) as still upcoming at time of publication, implying the described architecture was not yet fully mature in these specific dimensions (p109).

## 6. Failure modes and edge cases

- **Pre-migration out-of-memory failures under high-volume ingestion**: "iFood's pipelines were hindered by out-of-memory errors during high-volume event ingestions, leading to frequent driver shutdowns and operational disruptions" — this is presented as the specific pre-migration failure mode that Spark Declarative Pipelines resolved (p107).
- **Fragmented governance obscuring data accuracy issues**: "With the data spread across numerous systems and lacking proper governance, troubleshooting and ensuring data accuracy became a time-consuming and error-prone process" — a governance/observability failure mode specific to the pre-migration, multi-system architecture (p107).
- Not otherwise discussed [U]: the chapter does not describe any failure modes or edge cases encountered in the current (post-migration) architecture.

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when consolidating a fragmented multi-system data architecture, consider table-count reduction (via unified per-product Bronze tables) as an explicit design goal alongside pipeline-tooling migration, since iFood's own reported table-count reduction (nearly 4,000 → 100) was presented as a direct governance and data-quality enabler, not just a side effect (p107).
- **Build** [D]: use Liquid Clustering rather than traditional partitioning when consolidating high-cardinality, high-volume event data into single per-product Silver tables at very large scale (hundreds of TB, hundreds of billions of records), per iFood's own reported approach (p109).
- **Maintain** [D]: apply SDP expectations/quality rules at the Silver layer as the point where data becomes validated and analyst-consumable, keeping Bronze as a lightly structured staging zone with extended retention (p108-109).
- **RCA** [D]: if a high-volume streaming ingestion pipeline is experiencing out-of-memory errors or worker shutdowns, consider whether a declarative pipeline framework (handling execution/scaling/monitoring automatically) would address root causes better than manual tuning of a custom-coded pipeline, per the specific failure mode iFood reports resolving this way (p107).
- **Optimization** [D]: treat self-service Gold-table creation by business analysts (rather than data engineering as a bottleneck) as a target outcome of a well-governed Silver layer, since iFood credits this pattern with enabling faster business-critical insight generation (p109).

## 8. How to test/verify these claims

- [U] This chapter's quantitative claims (67%/70%/30% reductions, specific table sizes, cost figures) are self-reported and not accompanied by independently reproducible benchmarks or methodology in-chapter; readers seeking to validate similar results should run their own before/after measurements on a comparable migration rather than assuming these percentages generalize.
- Verify the ingestion-latency claim ("hours to seconds") by benchmarking a comparable Kinesis-to-Spark-Declarative-Pipelines ingestion setup against a legacy custom-coded equivalent under similar event volume (p108).
- Verify the Liquid Clustering claim by comparing query/write performance on a large, high-cardinality table under traditional partitioning versus Liquid Clustering at meaningfully large scale, since iFood's reported benefit is specific to their 210TB/800-billion-record table context (p109).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces Spark Declarative Pipelines and Lakeflow Connect at a conceptual level, directly applied in this case study.
- Ch.7 (Optimizing Materialized Views Recomputes): covers Spark Declarative Pipelines' Enzyme engine and incremental-refresh mechanics that likely underlie iFood's described pipeline efficiency gains, though not explicitly named in this chapter.
- Ch.9 (Production-Grade Data Quality Using Spark Declarative Pipelines): the SDP "expectations and quality rules" referenced at iFood's Silver layer are the same mechanism detailed in that chapter.
- Ch.10 (Collaborative Data Engineering Made Simple With Databricks Asset Bundles): iFood's stated plan to "leverage DABs for streamlined development" directly anticipates that chapter's content.
- Ch.11 (A Practical Guide to Serverless Migrations): iFood's stated plan to adopt "serverless computing for greater flexibility" directly anticipates that chapter's content.

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Direct customer quotes beyond those already reproduced (Thiago Julião, Maristela Albuquerque, Gabriel Campos) | Key quotes are reproduced in §1/§4 where they carry a specific technical or quantitative claim; remaining quotes are restatements of the same sentiments already captured. |
| Embedded architecture diagram | Visual content; described narratively in §4 based on the accompanying prose, not reproduced as an image. |
