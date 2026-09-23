# Ch.13 — NFCU: Using Real-Time Data to Trailblaze Member Personalization

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; customer case study featuring Jian (Miracle) Zhou, Senior Engineering Manager, Navy Federal Credit Union)
**PDF page range:** 110–113 (4 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**NFCU's reported migration results** [S]: "Billions of application events per month processed by Spark Declarative Pipelines / 9 billion events streamed continuously for 9 months, 24/7, with ~100% zero maintenance / 6-week time to market for a new real-time omnichannel application."

(p110)

**NFCU's four-step SDP pipeline** [S]: "three query functions and two CDC calls to complete all four steps... The first function they wrote connects to the event hubs, applies some transformation and returns a data frame. The second query function takes complex JSON documents and flattens them into individual application event records. They then used Spark Declarative Pipelines's APPLY CHANGES function to remove duplicates. In the third query function, they filtered the data down to just the login events."

(p111)

**Enhanced Autoscaling outcome** [S]: "The processing volume went up quickly, from just a few hundred users and a few thousand sessions every day to millions of users and billions of application events per month. This pipeline automatically scaled the resources depending on the data volume. Our production support engineers never had to intervene."

(p111)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this is a vendor customer case study describing how Navy Federal Credit Union (NFCU) built a near-real-time (≤10-minute-latency) member-activity dashboard on Spark Declarative Pipelines, Databricks SQL, and Power BI, within a six-week deadline tied to a phased online-banking-platform migration.

**WHY** [S]: "24 hours is a long turnaround time... As we were moving closer to the first wave of user migration, we decided to enhance our data solution to introduce new insights in near real time"

(p111), specifically needing to track "the number of unique members who were able to log into the new channel, and the number of unique sessions the channel served" (p111), filterable by migration wave.

**WHEN** [D]: relevant as a reference case for teams needing to stand up a new low-latency (minutes-scale), high-volume (billions-of-events) streaming analytics pipeline under a tight deadline (weeks, not months) with a small team new to the underlying cloud/streaming stack.

## 3. Assumptions and prerequisites

- [U] This is a vendor-published customer success story built around a single named engineering manager's account; all quantitative claims (9 billion events, ~100% zero maintenance, 6-week time to market) are self-reported by NFCU/Databricks, not independently audited in this chapter.
- NFCU's team was building its "first time... a real-time solution in Azure Cloud"

(p111), so the reported turnaround time reflects a team new to this specific architecture, not necessarily typical of an experienced team.

- Assumes an Azure-based stack: Azure Event Hubs (Kafka-protocol-compatible) for streaming ingestion from Azure Application Insights telemetry, Azure Data Lake Storage for storage, Databricks SQL for querying, and Power BI for visualization (p111).

## 4. Mechanism / key steps

1. Identify the data-access gap: NFCU "faced challenges using Azure Application Insights for dashboards due to the lack of access to member attribute data"

(p111), motivating streaming the telemetry out to a data lake instead of relying on Application Insights' own dashboarding.

2. Stream telemetry via Azure Event Hubs (Kafka-protocol support) into the data lake for "low-latency, high-reliability data consumption without requiring coding"

(p111) on the ingestion-transport side.

3. Build the SDP pipeline in four logical steps across three query functions and two CDC (`APPLY CHANGES`) calls: (a) connect to Event Hubs, transform, return a DataFrame; (b) flatten complex JSON documents into individual application-event records; (c) apply `APPLY CHANGES` to deduplicate; (d) filter to login events and select only relevant columns, then apply `APPLY CHANGES` again to deduplicate the login event table specifically (p111-112).

4. Configure pipeline persistence semantics: explicitly specify which intermediate data should be persisted versus kept in memory (not externally accessible) during pipeline execution (p112).

5. Apply the Expectations feature to set data-quality expectations and monitor data health on the resulting pipeline (p112).

6. Enable Enhanced Autoscaling before production deployment, anticipating unknown but growing compute demand as migration waves increased, allowing the pipeline to scale from "a few hundred users and a few thousand sessions"

(p112) to "millions of users and billions of application events per month"

(p112) without manual intervention.

7. Deliver the dashboard by connecting Power BI directly to the Databricks SQL endpoint, building Power BI semantic models over the lake data, with dashboard visuals querying Databricks directly to reflect near-real-time updates (p112).

8. Execute the full six-week build under a compressed timeline: one week for a proof of concept, three weeks to develop/test/establish a CI/CD process, deployment to production just before the first migration wave, and dashboard release "just a few days later" (p112).

## 5. Trade-offs and limitations

- [U] As vendor-published case-study content, this chapter presents no trade-offs or limitations of the SDP-based approach itself — occasional "hiccups that caused temporary interruptions" are mentioned but framed entirely positively, as evidence of automatic recovery rather than as a genuine limitation requiring mitigation (p112).
- The claimed "~100% zero maintenance" outcome is specific to this one pipeline's nine-month run under NFCU's particular workload and team context; it is not presented with a methodology for how "zero maintenance" was measured or defined (p110).

## 6. Failure modes and edge cases

- **Transient cloud-environment interruptions**: "On some days there were hiccups that caused temporary interruptions... Those hiccups were the natural result of being in the cloud environment," with the pipeline reported to have "automatically recovered from those transient errors" in every case described (p112).
- **Unpredictable compute demand across migration waves**: NFCU "were anticipating that would increase the demand for compute resource, but we were not sure exactly how much was needed for every wave"

(p112), addressed via Enhanced Autoscaling rather than manual capacity planning per wave.
- **Small-file accumulation degrading query performance**: implicitly addressed rather than experienced as a failure, since the chapter credits SDP's automatic "optimizes, compacts and vacuums" behavior with eliminating/reducing "the small file problem," implying this would otherwise have been a real risk at NFCU's event volume (p112).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when a team is new to a given cloud/streaming stack and under a hard deadline, consider a declarative pipeline framework (few functions/steps) specifically to compress build time, per NFCU's own framing of low-code complexity as directly enabling their six-week timeline (p111-112).
- **Build** [D]: use `APPLY CHANGES`-based deduplication at multiple stages of a streaming pipeline (both at raw ingestion and again at a filtered/derived table) rather than assuming deduplication only needs to happen once, per NFCU's own two-CDC-call pattern (p111-112).
- **Maintain** [D]: enable autoscaling proactively before a known but unpredictable demand ramp (e.g., a phased user migration), rather than attempting to pre-provision fixed capacity per phase, per NFCU's own stated rationale for turning on Enhanced Autoscaling ahead of deployment (p111).
- **RCA** [D]: if a long-running streaming pipeline experiences transient interruptions, first check whether they self-recovered automatically (a expected characteristic of a cloud-native streaming platform per NFCU's account) before treating each interruption as an incident requiring intervention (p112).
- **Optimization** [D]: rely on the pipeline framework's automatic table optimization/compaction/vacuuming for small-file management at high event volumes, rather than building custom file-compaction jobs, per NFCU's reported approach (p112).

## 8. How to test/verify these claims

- [U] This chapter's headline figures (9 billion events, "~100%" zero maintenance, 6-week time to market) are self-reported without an accompanying methodology; readers should not assume these figures generalize to other teams/workloads without their own comparable before/after measurement.
- Verify the `APPLY CHANGES`-based deduplication approach by replicating NFCU's described four-step pipeline pattern (connect → flatten → dedupe → filter/select → dedupe again) against a similarly structured streaming JSON event source and confirming duplicate records are correctly removed at both stages (p111-112).
- Verify the Enhanced Autoscaling claim by running a comparable pipeline under a step-function-like growth in event volume (mimicking NFCU's wave-based migration) and confirming compute scales automatically without manual reconfiguration (p111).
- Verify the small-file/compaction claim by measuring file count and query latency over time on a high-throughput streaming table with and without automatic optimize/compact/vacuum behavior enabled (p112).

## 9. Cross-references

- [[ch01_introduction_to_data_engineering_on_databricks|Ch.1]] (Introduction to Data Engineering on Databricks): introduces Spark Declarative Pipelines and its automatic orchestration/data-quality capabilities at a conceptual level, directly applied here.
- [[ch06_implement_cdc_and_scd_type_2_with_lakeflow|Ch.6]] (Implement CDC Data Load and SCD Type 2 With Lakeflow): the `APPLY CHANGES`/CDC deduplication mechanism used here parallels (though for a different purpose — deduplication rather than SCD Type 2 history) that chapter's CDC-handling content.
- [[ch07_optimizing_materialized_views_recomputes|Ch.7]] (Optimizing Materialized Views Recomputes): the automatic table optimize/compact/vacuum behavior credited here with eliminating the small-file problem is the same Enzyme-engine-adjacent mechanism discussed in that chapter's incremental-refresh context.
- [[ch09_production_grade_data_quality_using_sdp|Ch.9]] (Production-Grade Data Quality Using Spark Declarative Pipelines): the Expectations feature used here for data-quality monitoring is the same mechanism detailed in that chapter.

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Direct customer quotes beyond those already reproduced (Jian (Miracle) Zhou) | Key quotes are reproduced in §1/§4 where they carry a specific technical or quantitative claim; remaining quotes restate the same sentiments already captured. |
| Details of the "homegrown metadata-driven framework" NFCU built after initial production deployment | The chapter mentions this only in passing without technical detail on its design; nothing substantive to synthesize beyond noting it as a follow-on initiative (p113). |
