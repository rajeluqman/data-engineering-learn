# Ch.4 — A Cost Maturity Journey With Databricks

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Zach King and Rajneesh Arora)
**PDF page range:** 27–45 (19 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Crawl-walk-run cost maturity journey** [S]: "Think of this as the 'crawl, walk, run' journey to go from chaos to control," consisting of four steps: "Cost Attribution," "Cost Reporting," "Cost Control," "Cost Optimization."

(p27-28)

**Budget Policy vs. Budgets** [S]: "A Budget Policy is very different from Budgets... A Budget Policy only applies to serverless workloads."

(p32)

**Compute Policy `dbus_per_hour`** [S]: "can be used with a range policy type to set lower and upper bounds on DBU cost of clusters that users can create. However, this only enforces max DBU per cluster that uses the policy."

(p37)

**Photon's DBU multiplier** [S]: "Photon increases the amount of DBUs the cluster costs by a multiple of 2.9x for job clusters, and approximately 2x for All-Purpose clusters."

(p43)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter is a structured, four-step FinOps playbook for Databricks (cost attribution via tagging/budget policies, cost reporting via system tables and dashboards, cost control via compute policies, and cost optimization via resource-selection best practices).

**WHY** [S]: "higher velocity for data practitioners can lead to chaos unless balanced with careful cost management"

(p27), motivating a structured, incremental approach to cost maturity rather than ad hoc cost control.

**WHEN** [D]: apply this playbook when an organization's Databricks usage has grown past the point where informal cost tracking is sufficient — specifically when multiple teams/business units self-serve compute resources and centralized visibility/control is needed to avoid unmanaged spend.

## 3. Assumptions and prerequisites

- [U] This is vendor-authored guidance from named Databricks employees describing Databricks' own platform features; specific tool recommendations and claimed savings figures (e.g., "2-3x cheaper," "up to 3x better price-to-performance") are vendor claims, not independently benchmarked in this chapter.
- Assumes a Unity-Catalog-governed Databricks account with access to system tables (`system.billing.usage`, `system.compute.clusters`, `system.lakeflow.jobs`, etc.) as the mechanism underlying all cost reporting content (p33-43).
- Assumes administrative-level access (workspace/account admin) for configuring Budget Policies, Compute Policies, and Statement Timeouts, since these are explicitly admin-scoped features (p31, p37, p40).
- Assumes familiarity with basic Databricks compute concepts (classic vs. serverless compute, job vs. all-purpose clusters) introduced in earlier chapters of this source.

## 4. Mechanism / key steps

1. **Cost attribution (Step 1)**: tag compute resources (SQL Warehouse, jobs, instance pools) and, separately, Unity Catalog securables; classic compute inherits tags from the cluster definition, while serverless compute is tagged via a three-step Budget Policy process (create policy → assign to users/groups/service principals → user selects/auto-selects policy at serverless compute creation time) (p28-32).

2. **Cost reporting (Step 2)**: use `system.billing.usage` and related system tables as the foundation for cost visibility; import the pre-built Account Usage AI/BI dashboard (usage trends, Top-N usage by billable object, tag-based usage analysis, AI spending forecasts) and the Jobs System Tables dashboard (top jobs by potential savings, lowest CPU/highest memory utilization, outdated DBR versions); configure Budgets (distinct from Budget Policies) to notify recipients when account-wide or filtered spend exceeds a USD threshold (p33-36).

3. **Cost controls (Step 3)**: use Compute Policies to enforce guardrails — `dbus_per_hour` (range type) to bound per-cluster DBU cost, `max_clusters_by_user` (top-level policy setting) to cap concurrent clusters per user, `cluster_type` (fixed type) to restrict a policy to all-purpose/job/dlt use, `node_type_id`/`driver_node_type_id` (allowlist/regex) to constrain instance types, `spark_version` (allowlist, e.g. `auto:latest-lts`) to enforce runtime currency, spot-instance attributes with `first_on_demand` set to at least 1, and `custom_tags.*` attributes (fixed/allowlist) to enforce tagging compliance; separately, configure SQL warehouse Statement Timeout to bound long-running queries, and AI Gateway rate limits to bound model-serving cost exposure (p37-40).

4. **Cost optimization (Step 4)**: prefer job compute over all-purpose compute for automated workloads (typically 2-3x cheaper, per the chapter), use SQL warehouses for SQL-only workloads, keep runtimes current, prefer serverless for faster startup/termination and better TCO, use autoscaling (except for continuous streaming or `AvailableNow`-triggered jobs, where Spark Declarative Pipelines' Enhanced Autoscaling instead applies), choose VM instance type by workload shape (memory-optimized for ML, compute-optimized for streaming, storage-optimized for disk-caching-heavy ad hoc/interactive workloads, GPU only for GPU-accelerated libraries, general-purpose otherwise), and use spot/spot-fleet instances in lower (dev/stage) environments (p41-42).

5. Use provided system-table SQL queries to operationalize optimization: one query identifies jobs still running on interactive all-purpose clusters (candidates to migrate to job compute) (p42), and another identifies interactive clusters configured with Photon that may be paying its DBU multiplier without benefit (p43).

## 5. Trade-offs and limitations

- Photon increases DBU cost ("2.9x for job clusters, ~2x for All-Purpose") but "can yield a lower overall TCO for jobs by reducing the runtime duration" — its net cost-effectiveness depends on whether the runtime reduction offsets the multiplier, and the chapter explicitly warns it "isn't always beneficial for continuous streaming jobs that are up 24/7" (p43).
- `dbus_per_hour` alone caps per-cluster DBU cost, but as the chapter notes, "a single user with permission to this policy could still create many clusters"

(p37), each capped individually — full cost control requires pairing it with `max_clusters_by_user`.
- Budget Policy tag propagation to system tables depends on which tasks within a job actually run on serverless compute: it fully propagates only when all tasks are serverless, partially propagates when mixed, and does not propagate at all when no tasks are serverless — a subtlety that affects the completeness of cost-attribution data (p32).
- Interactive (all-purpose) clusters with Photon "may have significant amounts of idle time," which "may result in higher costs with Photon" if auto-termination is not configured — the chapter frames Photon's benefit as conditional on utilization pattern, not a strict win (p43).

## 6. Failure modes and edge cases

- **Unbounded per-user cluster proliferation**: setting only `dbus_per_hour` without `max_clusters_by_user` leaves a loophole where a user creates many capped clusters, defeating the intended cost ceiling (p37).
- **Incomplete cost attribution from mixed serverless/non-serverless job tasks**: in a job with some serverless and some classic-compute tasks, Budget Policy tags propagate only for the serverless portion, so naive cost reporting based solely on Budget Policy tags will undercount or misattribute the classic-compute portion's cost (p32).
- **Long-running, unoptimized SQL queries disrupting other queries**: without a configured Statement Timeout, "unoptimized queries (poor filters or even no filters) or unoptimized tables" can run indefinitely and "even disrupt other queries if too many begin to queue up" (p40).
- **Model-serving endpoint abuse**: without AI Gateway rate limits, "ML models and LLMs can also be abused with too many requests, incurring unexpected costs" (p40).
- **Idle interactive clusters running Photon without auto-termination**: this combination can produce higher costs than expected, since Photon's per-hour cost multiplier applies during idle time as well as active compute time if the cluster isn't terminated (p43).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: implement the four-step order (attribution → reporting → controls → optimization) rather than jumping straight to optimization, since accurate attribution/reporting is the chapter's own stated foundation for meaningful cost control and optimization decisions (p27-28, p45).
- **Build** [D]: pair `dbus_per_hour` with `max_clusters_by_user` when building any self-service compute policy, and use `cluster_type: fixed` to keep job/all-purpose/dlt policies cleanly separated, per the chapter's own recommended pattern (p37).
- **Maintain** [D]: enforce tag compliance systematically (via Compute Policy `custom_tags.*` attributes and/or a scheduled compliance-checking job) rather than relying on voluntary tagging discipline, since the chapter explicitly recommends this as the mechanism for "initial tagging compliance" (p33).
- **RCA** [D]: when investigating unexpected Databricks spend, first check whether jobs are running on all-purpose rather than job compute (the chapter's own provided query identifies this directly) and whether Photon is enabled on idle-prone interactive clusters or 24/7 streaming jobs without a corresponding runtime-duration benefit (p42-43).
- **Optimization** [D]: apply the VM-instance-type-by-workload-shape mapping (memory-optimized for ML, compute-optimized for streaming, storage-optimized for disk-caching-heavy interactive work, GPU only for GPU-accelerated libraries) as a first-pass sizing heuristic before deeper workload-specific tuning (p41-42).

## 8. How to test/verify these claims

- Verify the job-vs-all-purpose-compute cost claim by running the same workload on both cluster types under otherwise identical configuration and comparing actual DBU cost, since the chapter's "2-3x cheaper" figure is stated as typical but dependent on "promotions and active discounts" (p42).
- Verify the Photon DBU multiplier and net-TCO claims by running matched job-cluster and all-purpose-cluster workloads with and without Photon enabled, comparing both DBU rate and total runtime duration, per the chapter's own framing of Photon's cost-effectiveness as duration-dependent (p43).
- Run the chapter's own provided SQL queries (all-purpose-cluster job finder, Photon-usage finder) against a real Databricks account's system tables and confirm they surface the expected candidate jobs/clusters for optimization (p42-43).
- Verify the Budget Policy tag-propagation behavior described for mixed serverless/classic jobs by constructing a job with one serverless and one classic task, then inspecting `system.billing.usage` for tag presence on each task's billing record (p32).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces Lakeflow Jobs and serverless compute concepts referenced throughout this chapter.
- Ch.2 (Migrating Apache Spark ETL Workloads to Databricks): covers cluster-type selection and System-Tables-based monitoring at a general level; this chapter provides the FinOps-specific deep dive.
- Ch.3 (How Observability in Lakeflow Helps You Build Reliable Data Pipelines): the Jobs System Tables AI/BI Dashboard and System Tables mechanism referenced here overlap directly with that chapter's observability content.
- The FinOps Foundation™, credited as the origin of the formal cost-control/oversight practice this chapter builds on (p27).
- "Comprehensive Guide to Optimize Databricks, Spark and Delta Lake Workloads," referenced for deeper data/storage/Spark optimization strategies beyond this chapter's scope (p44).
- External per-cloud documentation (AWS/Azure/GCP variants) referenced throughout for tagging, Budget Policies, Budgets, and Compute Policies, not reproduced here (p28-40).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Full Python/SDK code listings (warehouse/cluster/job tag-update functions), Terraform HCL blocks, and JavaScript/JSON compute-policy attribute snippets | Reproduced only as named mechanism steps in §4; the specific code is illustrative API usage, not independently verifiable conceptual claims, and is version/API-surface-specific. |
| Full SQL queries for finding all-purpose-cluster jobs and Photon-enabled interactive clusters | Referenced and described in §4/§8 as verification methods rather than reproduced verbatim; the underlying system-table schema is Databricks-version-specific. |
| Embedded product screenshots (tagging UI, Account Usage dashboard, Jobs Monitoring dashboard, DBSQL/Model Serving monitoring dashboards) | Visual content; described narratively where relevant, not reproduced. |
| Organizational-structure discussion (Centralized/Hub-and-spoke, Hybrid/distributed FinOps models) beyond what's captured in §7 | Organizational/process guidance rather than a technical claim requiring citation-level fidelity; captured at summary level only. |
