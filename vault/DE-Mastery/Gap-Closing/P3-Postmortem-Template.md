# P3: Blameless Post-Mortem Template — Gap Closing Guide
Priority: 3
Status: 🟡 RCA ada, format formal belum
---
## Cara guna
Copy template ni bila berlaku incident.
Isi semua 7 bahagian. Ringkas dan jelas lebih baik dari panjang.
Simpan dalam folder: Interview-Prep\Incidents\YYYY-MM-DD-[nama-incident].md
---
## TEMPLATE (copy dari sini)
  BLAMELESS POST-MORTEM REPORT
  ==============================
  Incident Title:
  Date of Incident:
  Incident Commander:
  Severity: [P1 Business Critical / P2 High / P3 Medium]
  Duration: [dari detect sampai resolve]
  1. SUMMARY
     [1-2 ayat: apa jadi, berapa lama, apa impact]
  2. IMPACT
     - Data Freshness SLO: [breached by X minutes / not breached]
     - Error Budget Burn: [consumed X% of monthly budget]
     - Teams affected: [BI team / stakeholders / end users]
     - Business impact: [konkrit]
  3. ROOT CAUSES
     - Structural Cause: [apa dalam sistem yang bagi peluang ni jadi]
     - Testing Defect: [apa test yang sepatutnya catch ni tapi tak ada]
     - Governance Defect: [apa process / agreement yang missing]
  4. TRIGGER
     [Event spesifik yang trigger incident]
  5. RESOLUTION / MITIGATION
     - [Langkah 1 yang diambil]
     - [Langkah 2]
     - Time to resolve: [X jam Y minit]
  6. LESSONS LEARNED
     What went well:
     - [benda yang kerja]
     What went wrong:
     - [benda yang boleh lebih baik]
  7. ACTION ITEMS (PREVENTATIVE ENGINEERING)
     [Item 1] [Description konkrit] (Owner: [nama], Due: [tarikh])
     [Item 2] [Description konkrit] (Owner: [nama], Due: [tarikh])
  ==============================
---
## Contoh lengkap (dari SRE Playbook)
  BLAMELESS POST-MORTEM REPORT
  ==============================
  Incident Title: P1 Gold Layer Reporting Outage & Data Corruption
  Date: 2026-08-25
  Incident Commander: Staff Data Engineer
  Severity: P1 Business Critical
  Duration: 3 hours 45 minutes
  1. SUMMARY
     Schema drift dalam upstream core-banking REST API introduced STRING type
     dalam field 'amount'. Silver-to-Gold PySpark job fail TypeCastException.
     Executive dashboards stale 225 minit.
  2. IMPACT
     - Freshness SLO: breached by 225 minutes (target <60 mins)
     - Error Budget: consumed 18% of monthly budget
     - Executive BI dashboards stale sepanjang morning operations
  3. ROOT CAUSES
     - Structural: Upstream team modified API payload tanpa schema registry notification
     - Testing: Schema validation gate tak enforce strict check pada API payloads
     - Governance: CI/CD takde contract validation test (dbt source freshness)
  4. TRIGGER
     Upstream release v2.4.1 deployed at 04:00 AM UTC
  5. RESOLUTION
     - Routed ingestion ke fallback JSON parser dengan explicit schema casting
     - Delta Lake time travel restore Gold table ke timestamp pre-corruption
     - Re-run dbt models untuk refresh Power BI Direct Lake caches
     Time to resolve: 3 jam 45 minit
  6. LESSONS LEARNED
     What went well:
     - Airflow failure callback triggered Slack alert immediately
     - Delta Lake time travel = instant zero-copy rollback
     What went wrong:
     - Alert fatigue delayed acknowledgment 20 minit (noisy Slack channel)
  7. ACTION ITEMS
     [1] Implement Schema-Drift Gating dalam PySpark Bronze (Owner: DE Team, Due: 2026-09-01)
     [2] Migrate Alerting ke PagerDuty Burn-Rate trigger (Owner: DE Lead, Due: 2026-09-05)
     [3] Establish Data Contract dengan Upstream Software Eng (Owner: Staff DE, Due: 2026-09-10)
  ==============================
