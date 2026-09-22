# Serverless & Compute Sizing

> **One line:** choosing (or not having to choose) how much infrastructure to provision — and paying only for actual processing time instead of idle wait.

**Spread:** 3/6 book sources · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch11_practical_guide_to_serverless_migrations\|Ch.11 Serverless Migrations]] | The dedicated playbook (67 hits) — billing model shift, cost governance before migration, compute selection |
| Databricks | [[ch04_cost_maturity_journey_with_databricks\|Ch.4 Cost Maturity]] | Compute-sizing decisions as a direct FinOps lever |
| Databricks | [[ch14_cincinnati_reds_case_study\|Ch.14 Cincinnati Reds]] | Real production payoff — 3–5x latency improvement from job-compute-with-pools → fully serverless |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]], [[ch02_migrating_apache_spark_etl_workloads_to_databricks\|Ch.2 Migration]] | Serverless as the default recommendation in a migration playbook |
| fundamentals_de | [[ch04_choosing_technologies\|Ch.4 Choosing Technologies]] | The general vendor-neutral framing — when to hand over infrastructure decisions vs. keep control |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | Light touch — compute-management evolution mentioned historically |

---

## The thread

Cincinnati Reds' case study is the clean before/after: job compute *with pools* still pays a startup-latency tax every run; going fully serverless removes it entirely. fundamentals_de Ch.4's vendor-neutral framing (when does handing over infrastructure control actually pay off?) is the question every Databricks serverless case study answers concretely — and Databricks Ch.11's explicit warning (governance-first, because serverless is "immediately available to all users by default" with no inherited cluster policies) is the trade-off fundamentals_de's abstract framing predicts but doesn't spell out.

## Related

[[cost-management]] · [[orchestration-and-dependencies]]
