# Defend or Drop — Interview Claim Guide
Setiap teknik dalam inventory kau: ayat boleh cakap vs ayat kena elak.
Berdasarkan status evidence sebenar dalam repo kau.
---
## BOLEH DEFEND PENUH (✅)
### Partition pruning + ZORDER (banking)
DEFEND:
"I implemented Delta compaction with OPTIMIZE and ZORDER on 8 fact and
bridge tables in my banking lakehouse — specifically ZORDERed by customer_id,
which turns a full-partition scan into reading 1-2 files per customer lookup."
NOTE: Cheatsheet docs kata 🟡 tapi code dah landed. Trust the code, not the docs.
---
### Checkpoint-resume idempotency (paysim)
DEFEND:
"I built checkpoint-resume into the cumulative pipeline — after each day's
MERGE, state is written to S3. On retry, it resumes from the last completed
day instead of restarting from day 1. An unreadable checkpoint raises loudly
rather than silently restarting and double-counting."
---
### Serverless vs cluster decision (Volve)
DEFEND:
"For Volve sensor analytics, I deliberately chose SQL Warehouse over classic
Spark clusters because classic clusters burn $0.15-0.40/DBU of trial credit.
The whole pipeline is SQL DDL/DML against Serverless SQL Warehouse — zero
PySpark. The instinct to know WHEN NOT to use Spark is the senior move."
---
### Atomic publish pointer-swap (pharma)
DEFEND:
"Object storage has no atomic rename, so I built a verified publish pattern:
build into gold/<run_id>/, verify completeness, then copy to gold/_current/
that consumers read. Rollback means re-publishing an older run_id — instant,
zero data loss."
---
### Control-plane vs data-plane split (banking ADR-011)
DEFEND:
"Airflow fires one DatabricksRunNowOperator that triggers the entire 22-task
Databricks Asset Bundle job graph. Airflow only handles extraction to Landing —
nothing past that runs on the Airflow worker. This prevents two systems owning
the same dependency graph and drifting apart."
---
### Layered GE quality gates (5 repos)
DEFEND:
"Bronze gates are WARN — pipeline continues because Bronze is expected to be
messy, that's what Bronze is for. Silver gates are strict — PK uniqueness
failures halt the pipeline. Different consequence per layer, not one config
for everything."
---
### $0 dev loop (pharma + creative_lab ONLY)
DEFEND:
"In pharma and creative_lab, dbt dev target uses DuckDB in-memory — every
model iteration costs $0. Cloud warehouse is only touched by a promoted,
validated build."
CAVEAT WAJIB:
"The other four repos — banking, home-credit, paysim, olist — use Snowflake
for all targets. That's environment segregation, not a $0 dev loop."
---
### Multi-pattern extraction (banking)
DEFEND:
"Four heterogeneous sources, each needing a different extraction strategy —
watermark-incremental for PostgreSQL and MS SQL, simulated CDC via trigger
table for Teradata, change-tracking API for Salesforce, paginated REST for
the core-banking API. All four write state through one shared watermark
abstraction stored in the lake, not in code."
---
## DEFEND DENGAN CAVEAT (🟡)
### Delta MERGE upsert (banking silver_fraud.py)
DEFEND:
"The pattern is implemented and compile-checked in banking — I can walk
through the logic. Live-run verification against Bronze data is still pending."
DON'T SAY: "I've run this in production"
---
### MDM customer crosswalk (banking)
DEFEND:
"I engineered controlled overlap into three public Kaggle datasets that don't
naturally share customers — to exercise the identity-resolution logic. The
crosswalk assigns canonical customer IDs and applies source-priority
survivorship rules where the anchor population is Home Credit."
DON'T SAY: "I resolved real customer identities across production systems"
---
### Delta Time Travel recovery
DEFEND:
"The pattern is in the playbook and I understand it — restoreToVersion gives
you instant zero-copy rollback to any previous Delta table state. I haven't
run this against a live production incident yet."
---
## JANGAN CLAIM (❌)
### SLA Gym traps (pharma)
DON'T SAY: "I handled these production incidents"
SAY: "I built training drills — deliberately sabotaged DAGs — to practise
identifying anti-patterns like sequential-when-parallelizable and no
partition pruning."
### Shuffle tuning
DON'T SAY: "I've optimised Spark shuffle in production"
SAY: "I understand broadcast joins vs sort-merge joins and when to apply each.
I haven't explicitly profiled shuffle in a production job yet — my next step
is to check the Spark UI Exchange nodes for banking fact_txn."
### Burn-rate alerting
DON'T SAY: "I have burn-rate alerting implemented"
SAY: "I have basic Slack failure alerts. Burn-rate alerting with PagerDuty
is my next implementation — the architecture is: on_failure_callback with
error budget calculation before triggering, differentiated by burn rate level."
### SLO/Error Budget formal
DON'T SAY: "I have formal SLOs defined"
SAY: "I have quality gates at every medallion layer that implement the spirit
of SLOs — but I haven't yet formalized them with explicit SLO targets, error
budgets, and a tracking dashboard. That's my current P1 gap."
### Streaming / Kafka
DON'T SAY: "I have streaming pipeline experience"
SAY: "My experience is batch and incremental — watermark-based, checkpoint-
resume, Delta MERGE upsert. I understand streaming concepts including
watermarks and late data handling, but I haven't implemented production
streaming pipelines."
