# Ch.11 — A Practical Guide to Serverless Migrations

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Diego Gomez)
**PDF page range:** 99–105 (7 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Classic vs. serverless compute billing model** [S]: "With classic compute, workloads run on clusters directly provisioned within the customer's own cloud account... Databricks charges DBUs for managing and orchestrating the workload, while the cloud provider bills separately for the underlying infrastructure... Serverless flips this paradigm. Compute resources run fully within Databricks-managed cloud accounts."

(p99)

**Serverless billing granularity** [S]: "You only pay for the time your workload is actually running... Billing starts when the workload starts processing and stops when it completes."

(p99)

**Serverless budget policy** [S]: "allow administrators to define one or more tag key-value pairs that get automatically applied to any serverless compute activity initiated by users or jobs assigned to the policy," surfacing in `system.billing.usage → custom_tags` for cost attribution.

(p101)

**Serverless environment version** [S]: "Serverless environments are versioned, with Databricks periodically rolling out updates to maintain compatibility, security and stability... Each version includes a set of pre-installed system libraries, drivers and configurations."

(p103)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter is a practical playbook for migrating workloads from classic to serverless compute on Databricks — covering the billing-model shift, cost-governance setup (budgets, serverless budget policies, monitoring), the actual job-migration steps, and dependency/environment-version management.

**WHY** [S]: "Many customers have been eager to adopt serverless compute on Databricks, attracted by the promise of eliminating infrastructure management, gaining elastic scalability and simplifying the user experience for their teams. Unlocking the full value of serverless involves rethinking environment configuration, cost governance and dependency management."

(p99)

**WHEN** [D]: apply this playbook when planning to move classic-compute jobs/notebooks to serverless compute, specifically establishing cost governance (budgets, tagging policies, monitoring) before migration, since serverless is "immediately available to all users by default" once enabled and existing classic-compute cluster policies don't automatically apply to it (p100).

## 3. Assumptions and prerequisites

- [U] This is vendor-authored guidance by a named Databricks employee describing Databricks' own serverless offering; specific claims about cost efficiency and startup-latency improvements reflect the vendor's own framing.
- Assumes serverless compute is being newly enabled in a workspace shared by multiple personas (the chapter's own example: data engineers, data scientists, analysts) with different workload patterns and cost profiles, motivating the emphasis on upfront governance (p100).
- Assumes access to Databricks system tables (`system.billing.usage`, `system.billing.list_prices`) for cost monitoring, and admin-level access to configure Budgets and Serverless Budget Policies (p100-102).
- Assumes familiarity with classic Databricks cluster policies as the baseline governance mechanism that serverless does not automatically inherit (p100).

## 4. Mechanism / key steps

1. Understand the billing-model shift before migrating: classic compute bills separately for Databricks DBUs and cloud-provider infrastructure, including startup and idle time; serverless bills a single, fully-inclusive $DBU rate only for actual processing time, with faster startup via Databricks-managed warm capacity pools (p99).

2. Establish cost governance before enabling serverless broadly: configure Budgets (spending thresholds and alerts) at workspace or account level, segmented by persona/team via tag-based scoping — e.g., a higher-threshold budget for GPU-serverless-using data scientists and a smaller, more predictable budget for data engineers/analysts (p100).

3. Enforce cost attribution via Serverless Budget Policies: define tag key-value pairs (e.g., `team=data-science`, `team=data-engineer`, `team=analyst`) that automatically attach to serverless compute activity for users/jobs assigned to each policy, surfacing in `system.billing.usage`'s `custom_tags` for accurate attribution (p101).

4. Monitor serverless spend continuously: query `system.billing.usage` joined to `system.billing.list_prices` (filtering `sku_name LIKE '%SERVERLESS%'` and relevant `billing_origin_product` values) to compute list-price cost by workspace over a rolling window, and schedule such queries as alerts to proactively notify administrators when spend approaches or exceeds budget (p101-102, worked SQL example on p102).

5. Migrate a job to serverless compute: switch the job's compute configuration from classic cluster to serverless via the job configuration UI or API (recommending a duplicate job for testing to avoid impacting production), noting that serverless environments start minimal by default and require explicit library configuration (p102).

6. Select an appropriate serverless environment version: since Databricks manages the underlying runtime image, choose from versioned serverless environments (each with a fixed set of pre-installed system libraries/drivers/configurations), generally defaulting to the latest available version for the newest fixes and performance improvements (p103).

7. Configure library dependencies at the appropriate scope: workspace-level default dependencies (for packages common across teams), job task-level dependencies (recommended for production — finer control, reduces package-conflict risk), or notebook-scoped dependencies via the in-notebook Environment panel (useful for development, also configures memory settings, budget policies, and environment version) (p103).

8. Validate migration performance using a provided dashboard (built on system tables) comparing classic versus serverless runs of the same job (by `job_id`) on duration and cost per run, to decide which jobs are worth fully migrating (p103-104).

## 5. Trade-offs and limitations

- Serverless's fully-inclusive $DBU rate "may appear higher than classic compute" on a per-unit basis, but the chapter frames the net cost comparison as favorable once idle/startup time elimination is accounted for — implying per-unit-rate comparisons alone can be misleading without considering utilization pattern (p99).
- Serverless being "immediately available to all users by default" once enabled is presented as a flexibility benefit but explicitly creates a governance gap, since "any existing compute policies that govern classic compute — such as cluster policies — don't automatically apply to serverless workloads," requiring deliberate new governance setup rather than reuse of existing controls (p100).
- Serverless environments keep "things light by default," meaning migrated jobs are not automatically compatible without explicit library configuration — a direct trade-off of the minimal-by-default design versus classic clusters' more inherited/persistent environment state (p102-103).
- GPU serverless workloads specifically are flagged as carrying materially higher unmonitored cost risk than other serverless workload types, implying governance (e.g., budget thresholds) may need to be workload-type-aware rather than uniform (p100).

## 6. Failure modes and edge cases

- **Unbounded cost growth without upfront governance**: "without proper guardrails, it would be easy for serverless consumption to scale unpredictably — particularly as GPU serverless workloads can generate larger costs if left unchecked" — the chapter frames this as the central risk motivating governance-before-migration ordering (p100).
- **Migrated job failing due to missing libraries**: since "serverless keeps things light by default," a job migrated without first configuring its required library dependencies will lack necessary packages at runtime (p102-103).
- **Testing directly against production jobs**: migrating a production job's compute configuration in place (rather than duplicating it first) risks "unintended impact on production workloads" during validation, per the chapter's own explicit tip (p102).
- **Stale serverless environment version causing missed fixes**: not selecting the latest available serverless environment version means missing "the most recent fixes, performance improvements and package updates" that Databricks periodically rolls into newer versions (p103).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: sequence serverless adoption as governance-first (budgets, tagged budget policies, monitoring) before broad workload migration, since serverless's default-open availability and lack of automatic policy inheritance from classic compute make this ordering load-bearing for cost control, not merely best practice (p100-102).
- **Build** [D]: define library dependencies at the job task level (rather than workspace-level defaults) for production workloads specifically, per the chapter's own recommendation, to minimize package-conflict risk across teams sharing a workspace (p103).
- **Maintain** [D]: default to the latest serverless environment version when configuring new or migrated jobs, and periodically review environment version currency, since Databricks manages runtime updates on its own release cadence rather than the customer's (p103).
- **RCA** [D]: if serverless spend for a specific team/workload type spikes unexpectedly, first check whether serverless budget policy tags are correctly applied and whether that workload type (e.g., GPU serverless) has an appropriately scaled budget threshold, rather than assuming a platform-level billing anomaly (p100-102).
- **Optimization** [D]: use the classic-vs-serverless comparison dashboard (duration and cost per run by `job_id`) to make per-job migration decisions empirically, rather than migrating all workloads uniformly, since not every job may show equivalent cost/performance benefit from serverless (p103-104).

## 8. How to test/verify these claims

- Reproduce the chapter's own cost-monitoring query against a real Databricks account's `system.billing.usage`/`system.billing.list_prices` tables, filtered to serverless SKUs, and confirm it correctly surfaces per-workspace 30-day serverless cost (p102).
- Verify the serverless budget policy tag-propagation claim by assigning a budget policy to a test user/job, running serverless compute under that assignment, and confirming the expected tags appear in `system.billing.usage.custom_tags` (p101).
- Verify the classic-vs-serverless cost/latency claim directly by running the same workload on both classic and serverless compute and comparing actual billed duration/cost via the chapter's own provided comparison dashboard (p103-104).
- Verify the "light by default" library claim by migrating a job with third-party dependencies to serverless without first configuring those dependencies, and confirming the run fails or behaves differently until dependencies are explicitly configured (p102-103).

## 9. Cross-references

- Ch.1 (Introduction to Data Engineering on Databricks): introduces serverless compute options within Lakeflow Jobs/Declarative Pipelines at a conceptual level.
- Ch.4 (A Cost Maturity Journey With Databricks): the Budgets, Serverless Budget Policies, and `system.billing.usage`/`system.billing.list_prices`-based monitoring mechanisms here directly reuse that chapter's general FinOps framework, applied specifically to the serverless migration use case.
- Ch.2 (Migrating Apache Spark ETL Workloads to Databricks): that chapter's "Use Serverless for quicker startup, termination, and better total cost of ownership" recommendation is the general claim this chapter operationalizes into a concrete migration playbook.
- External resources referenced but not reproduced: the official Databricks pricing page, serverless release notes (for the full list of environment versions), documentation on workspace-level default dependencies, and a Git repository containing the classic-vs-serverless comparison dashboard code (p99, p103-104).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Full SQL query for computing serverless cost by workspace over 30 days | Reproduced only as a named mechanism step in §4/§8; the exact query is illustrative and schema-version-specific, fully captured in prose. |
| Embedded UI screenshots (job configuration UI, notebook Environment panel, comparison dashboard) | Visual content; described narratively where relevant, not reproduced. |
