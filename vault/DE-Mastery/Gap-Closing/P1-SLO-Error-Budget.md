# P1: SLO/Error Budget Formal — Gap Closing Guide
Priority: 1 (paling kritikal)
Prerequisite untuk: P2 Burn-Rate Alerting
Status: ❌ Belum implement
---
## Kenapa ini priority 1
Kau ada quality gates (GE, promotion gate, reconciliation) ✅
Tapi kau belum frame ia sebagai SLO/SLI/Error Budget.
Bezanya:
- Quality gate = "pass or fail" boolean
- SLO = "99% data sedia sebelum 7AM, setiap hari" — boleh ukur trend
- Error Budget = "kau ada 7.2 jam sebulan untuk gagal — dah pakai berapa?"
Tanpa SLO formal, kau tak boleh implement burn-rate alerting (P2).
---
## Step 1: Define 4 SLI konkrit untuk banking pipeline
  SLI-1 Data Freshness:
    Ukur: masa Gold layer ready lepas scheduled run (7AM target)
    Contoh: gold_ready_time - scheduled_run_time (dalam minit)
  SLI-2 Data Completeness:
    Ukur: row count Gold vs row count Bronze per hari
    Formula: (gold_rows / bronze_rows) * 100
  SLI-3 Data Correctness:
    Ukur: % record lulus GE test suite dalam Silver layer
    Formula: (passed_expectations / total_expectations) * 100
  SLI-4 Pipeline Availability:
    Ukur: % DAG selesai tanpa manual intervention dalam 30 hari
    Formula: (successful_runs / total_runs) * 100
---
## Step 2: Set SLO target
  SLO-1 Freshness:    99.0% hari data ready sebelum 7:30AM
  SLO-2 Completeness: 99.5% record berjaya ingest
  SLO-3 Correctness:  99.0% lulus GE suite
  SLO-4 Availability: 95.0% DAG selesai tanpa intervention
---
## Step 3: Calculate Error Budget
  Error Budget = 100% - SLO
  SLO-1 (99%):   1%   = 7.3 jam sebulan boleh delay
  SLO-2 (99.5%): 0.5% = 3.6 jam sebulan boleh incomplete
  SLO-3 (99%):   1%   = 7.3 jam sebulan boleh ada quality issue
  SLO-4 (95%):   5%   = 36.5 jam sebulan boleh manual intervention
---
## Step 4: Track dalam Snowflake/Delta
  CREATE TABLE slo_tracking (
      date DATE,
      sli_name VARCHAR,
      measured_value FLOAT,
      slo_target FLOAT,
      is_breached BOOLEAN,
      error_budget_consumed_minutes FLOAT
  );
---
## Soundbite untuk interview
"I have quality gates at every medallion layer, but I haven't yet
formalized them as SLOs with explicit error budgets. My next step
is to define the 4 Data SLIs, set SLO targets with the business,
and build a tracking dashboard — which then enables burn-rate
alerting instead of basic Slack notifications."
