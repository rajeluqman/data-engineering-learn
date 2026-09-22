# Ch.14 — Cincinnati Reds: Winning On and Off the Field With Cutting-Edge Baseball Analytics

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; customer case study featuring Bryce Dugar, Data Engineering Manager, Cincinnati Reds)
**PDF page range:** 114–116 (3 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Cincinnati Reds' reported migration results** [S]: "3–5x [improvement in latency with serverless Databricks Lakeflow Jobs] / 1,000s [of hours of compute time saved daily] / 83% [decrease in pipeline runtime]."

(p114)

**Data volume growth driver** [S]: "Over the past decade, data stream volume and complexity grew by up to 100x, driven by the rise of Internet of Things (IoT) devices and sensors that track player performance, in-stadium activity and fan engagement."

(p115)

**Cost outcome of serverless transition** [S]: "the team saw a 65–80% reduction in VM costs by transitioning to serverless Databricks Lakeflow Jobs... With the Reds running 15,000–20,000 workflow steps daily, this efficiency saved hundreds of thousands of compute minutes each day."

(p116)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this is a vendor customer case study describing how the Cincinnati Reds migrated from Azure Data Factory and on-premises legacy infrastructure to Databricks Lakeflow Jobs on serverless compute, to cut ETL/analytics latency for player-performance and game-day decision-making.

**WHY** [S]: "Processing billions of rows and queries often took hours or even days, making real-time applications impractical... A lot of the stuff we were doing before was just troubleshooting issues like missing rows or unprocessed data. We'd spend hours just fixing those problems instead of actually driving insights."

(p115)

**WHEN** [D]: relevant as a reference case for teams facing rapidly growing IoT/sensor-driven data volume (the chapter cites "up to 100x" growth over a decade) on legacy on-premises infrastructure, where manual troubleshooting and job-startup latency are blocking near-real-time analytics delivery to non-technical stakeholders (coaches, players).

## 3. Assumptions and prerequisites

- [U] This is a vendor-published customer success story built around a single named data engineering manager's account; all quantitative claims (3-5x latency improvement, 65-80% VM cost reduction, 83% pipeline-runtime decrease, "1,000s of hours" compute time saved daily) are self-reported by the Cincinnati Reds/Databricks, not independently audited in this chapter.
- Some of the chapter's own headline figures appear inconsistently stated across the text — e.g., the summary banner states "3-5x" latency improvement (10 min → 2-3 min) while the body text separately states "reduced latency by up to 83%" and "an hour...done in 10 minutes" — readers should treat these as different measurements taken at different points/pipelines rather than a single unified metric (p114, p116).
- Assumes an Azure-based prior stack (migrating specifically from Azure Data Factory) to Databricks Lakeflow Jobs on serverless compute (p116).

## 4. Mechanism / key steps

1. Diagnose the pre-migration problem: on-premises legacy systems processing "billions of rows and queries" taking "hours or even days," with data volume/complexity having grown "up to 100x" over a decade due to IoT/sensor proliferation (player performance, in-stadium activity, fan engagement tracking), and heavy manual troubleshooting consuming engineering time (p115).

2. Adopt Databricks Lakeflow Jobs as the unified orchestration layer to "define, manage and monitor jobs with multiple tasks for ETL," reduce manual intervention, and deliver more timely insights, replacing the prior Azure Data Factory orchestration (p115-116).

3. Integrate orchestration via APIs to trigger jobs with parameters, giving analysts independence to develop/execute notebooks with improved traceability and iterative processing capability (p115).

4. Migrate from job compute (with pools) to a fully serverless architecture, eliminating the job-startup delay previously incurred under pooled job compute, which the chapter credits with the reported 3-5x latency improvement (10 minutes → 2-3 minutes) (p115).

5. Realize downstream cost and scale benefits: a reported 65-80% reduction in VM costs, applied across "15,000-20,000 workflow steps daily," saving "hundreds of thousands of compute minutes each day" and freeing capacity for new workloads and faster report delivery (p116).

6. Remove memory/compute-core constraints via the serverless environment, enabling more efficient handling of large, complex data queries and improving end-to-end workflow traceability from ingestion to final output (p116).

## 5. Trade-offs and limitations

- [U] As vendor-published case-study content, this chapter presents no trade-offs, limitations, or challenges encountered during or after the serverless migration — every outcome is framed positively, with system instability, session crashes, and lengthy processing times described only as pre-migration problems now eliminated (p116).
- The chapter's own quantitative figures are not fully internally consistent (see §3 note on differing latency-improvement figures cited in different places), which is itself worth flagging when using these numbers as a benchmark rather than treating them as a single precise measurement (p114, p116).

## 6. Failure modes and edge cases

- **Manual troubleshooting consuming engineering time instead of driving insights**: "we'd spend hours just fixing those problems instead of actually driving insights or improving performance" — a pre-migration failure mode specific to missing rows and unprocessed data on the legacy on-premises system (p115).
- **Job-startup latency under classic (job/pool) compute**: "using job compute, even with pools, often led to delays while waiting for jobs to spin up" — the specific latency source that migrating to serverless compute addressed (p115).
- **System instability and session crashes under the legacy/pre-serverless setup**: described as eliminated post-migration ("Data scientists and engineers no longer face system instability, session crashes or lengthy processing times"), implying these were real operational failure modes prior to the transition (p116).
- Not otherwise discussed [U]: the chapter does not describe any failure modes or edge cases encountered in the current (post-migration) architecture.

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when data volume is growing rapidly due to IoT/sensor proliferation, budget explicitly for scaling data infrastructure ahead of a 100x-scale volume increase rather than assuming incremental legacy-system tuning will keep pace, per the specific growth trajectory the Reds report (p115).
- **Build** [D]: prefer serverless compute over job compute with pools specifically to eliminate job-startup latency as a bottleneck in time-sensitive (near-real-time) analytics pipelines, per the Reds' own before/after comparison (p115).
- **Maintain** [D]: use API-based job triggering with parameters to give downstream analysts independence in running/iterating on notebooks, reducing dependency on a central data engineering team for routine job execution (p115).
- **RCA** [D]: if a data team is spending disproportionate time on manual troubleshooting (missing rows, unprocessed data) rather than analysis, treat this as a signal that the underlying orchestration/compute platform may be undersized or poorly suited to current data volume, rather than a purely process-level problem (p115).
- **Optimization** [D]: track workflow-step-level cost and time savings (as the Reds did across 15,000-20,000 daily workflow steps) to quantify the cumulative impact of infrastructure changes at scale, rather than only measuring per-job improvements in isolation (p116).

## 8. How to test/verify these claims

- [U] This chapter's headline figures (3-5x latency improvement, 65-80% VM cost reduction, 83% pipeline-runtime decrease) are self-reported without a stated measurement methodology, and are not fully internally consistent across the chapter's own text; readers should not assume these figures generalize without their own comparable before/after benchmarking.
- Verify the job-compute-vs-serverless latency claim by running an equivalent ETL pipeline on both job compute (with pools) and serverless compute, measuring end-to-end duration including startup time, per the Reds' own before/after comparison methodology (p115).
- Verify the VM cost-reduction claim by comparing actual cloud billing for an equivalent workload volume before and after the serverless transition, since the chapter's 65-80% figure is presented as a range without a stated calculation method (p116).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces Lakeflow Jobs at a conceptual level, directly applied here.
- Ch.11 (A Practical Guide to Serverless Migrations): provides the general serverless migration playbook (cost governance, job-switching mechanics, dependency management) that this case study's transition implicitly follows.
- Ch.4 (A Cost Maturity Journey With Databricks): the VM cost-reduction outcome reported here would be measurable via that chapter's system-tables-based cost-reporting mechanisms, though this chapter does not describe its own measurement approach.

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Direct customer quotes beyond those already reproduced (Bryce Dugar) | Key quotes are reproduced in §1/§4 where they carry a specific technical or quantitative claim; remaining quotes restate the same sentiments already captured. |
| Discussion of data accessibility for different user roles (data scientists, business users, application developers) beyond what's captured in §4 | Mentioned narratively in the source but without technical implementation detail to synthesize beyond the role-differentiation point already noted (p115). |
