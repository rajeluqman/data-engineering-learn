# Cost Management & FinOps

> **One line:** treating cloud/platform spend as something you deliberately attribute, monitor, and control — not a bill you just accept.

**Spread:** 3/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch04_cost_maturity_journey_with_databricks\|Ch.4 Cost Maturity Journey]] | The dedicated FinOps playbook (33 hits) — the "crawl, walk, run" maturity model: attribution → reporting → controls → optimization |
| Databricks | [[ch11_practical_guide_to_serverless_migrations\|Ch.11 Serverless Migrations]] | Cost governance as a *prerequisite* to migration, not an afterthought |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]], [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]], [[ch14_cincinnati_reds_case_study\|Ch.14 Cincinnati Reds]] | Cost as a measured, headline case-study outcome |
| fundamentals_de | [[ch04_choosing_technologies\|Ch.4 Choosing Technologies]], [[ch03_designing_good_data_architecture\|Ch.3 Designing Good Data Architecture]] | Cost as one architectural evaluation criterion among several — the vendor-neutral framing |
| Airflow | [[ch17_airflow_deployment_options\|Ch.17 Deployment Options]] | Light touch — cost implications of self-hosted vs. managed deployment |

---

## The thread

Databricks Ch.4's four-step maturity model (attribution → reporting → controls → optimization) is the concrete, ordered version of fundamentals_de's abstract "cost is an architectural trade-off" framing. The ordering matters: you can't meaningfully *control* cost (step 3) before you can *attribute* it (step 1) — a lesson every case study with a specific cost-reduction number (Hinge Health's 50%, Cincinnati Reds' latency-driven savings) implicitly followed, whether or not the chapter says so explicitly.

## Related

[[serverless-and-compute]] · [[file-layout-and-compaction]] · [[incremental-vs-full-recompute]]
