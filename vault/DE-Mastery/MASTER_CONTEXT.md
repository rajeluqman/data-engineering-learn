# MASTER_CONTEXT.md — Raja Luqman: DE Mastery Learning System
> Last updated: 2026-08-25
> Projek Python (Track A): Berasingan — jangan campur dalam projek ni.
---
## BAHAGIAN 0 — CARA SESSION KENA BERKELAKUAN
1. Baca MASTER_CONTEXT.md + SRE Playbook files + semua modul setiap sesi mula.
2. Kerangka teras = Staff DE SRE Playbook (6 modul). BUKAN Boyd.
   Boyd = mindset sahaja (murah vs mahal). Kekal sebagai analogi bila berguna.
3. Cost/compute optimization = Spark tuning guide (terpisah dari SRE playbook).
4. Ajar guna context repo sebenar — banking, pharma, Volve. Bukan contoh generic.
5. Enforce integrity tags (✅/🟡/🔵/❌) setiap kali sebut claim.
6. Pareto-first: 20% yang unlock 80% dulu.
7. Tiap sesi, tanya dulu: nak buat modul mana / tutup gap mana / interview prep.
8. Bahasa: BM casual default. English untuk code, ADR, nama teknik.
---
## BAHAGIAN 1 — KERANGKA TERAS: STAFF DE SRE PLAYBOOK
### Kenapa SRE Playbook, bukan Boyd
Boyd (convex optimization) = matematik akademik. Berguna sebagai analogi
"sesetengah cara nampak sama tapi satu murah satu mahal" — tapi takde SOP,
takde template, takde metrik konkrit.
SRE Playbook = proven industry framework. Ada nama, metrik boleh ukur,
code blueprint, template post-mortem. Ini yang orang sebenar guna.
### 6 Modul SRE Playbook
M1: Core SRE Philosophy (Toil elimination, blast radius, mindset shift)
M2: SLO/SLI + Circuit Breaker (4 metrik, error budget, DLQ)
M3: Incident Management + Blameless Post-Mortem (P1 handling, template)
M4: Burn-Rate Alerting (anti-alert-fatigue, PagerDuty blueprint)
M5: Idempotency + Delta Time Travel (MERGE, checkpoint, recovery)
M6: Zero-Trust + IaC Governance (OIDC, Terraform, Unity Catalog)
### Glossary SRE
| Term | Definisi |
|---|---|
| Toil | Kerja manual berulang yang tak bagi nilai jangka panjang |
| SLI | Metrik spesifik yang diukur (contoh: freshness latency) |
| SLO | Sasaran SLI dipersetujui dengan business |
| SLA | Perjanjian dengan penalti kalau SLO gagal |
| Error Budget | 100% minus SLO — baki kegagalan dibenarkan sebelum freeze |
| Burn Rate | Kadar error budget dihakis — trigger alert bila tinggi |
| Circuit Breaker | Stop ingestion automatik bila data quality rosak teruk |
| Blameless PM | Post-mortem fokus sistem, bukan blame orang |
### 4 Metrik Data SLI
1. Data Freshness    — masa event generation ke data available dalam Gold
2. Data Completeness — % record berjaya ingest vs anggaran volume
3. Data Correctness  — % data lulus GE test suite
4. Pipeline Availability — % DAG selesai tanpa manual intervention
---
## BAHAGIAN 2 — MAP 6 MODUL SRE → 10 REPO
### M1: Toil Elimination + Blast Radius ✅
| Evidence | Repo | File | Status |
|---|---|---|---|
| Terraform IaC | banking | snowflake_serving.tf | ✅ |
| Databricks Asset Bundle | banking | databricks.yml 22-task | ✅ |
| CI/CD change gating | banking, EZCOM | lint+compile+DQ | ✅ |
| Control vs data plane | banking+airflow-dag | ADR-011 | ✅ |
| Local pre-flight | home-credit, migration_fiber | tests/local/* + COST_LOG.md | ✅ |
| $0 dev loop | pharma, creative_lab SAHAJA | dbt/profiles.yml DuckDB | ✅ |
Gap M1: OIDC Role Federation belum ada.
### M2: SLO/SLI + Circuit Breaker 🟡
| Evidence | Repo | File | Status |
|---|---|---|---|
| Layered GE gates | home-credit, olist, paysim, pharma, Volve | gx/run_*_suite.py | ✅ |
| Quarantine/DLQ | banking | promotion_gate.py | ✅ |
| Schema-drift gating | banking | promotion_gate.py:75-84 | ✅ |
| Coverage-as-KPI | pharma | cheatsheets/08_dq.md | ✅ |
| Reconciliation on drift | EZCOM | row-count check | ✅ |
Gap M2 KRITIKAL:
- Ada quality gates tapi BELUM guna bahasa SLO/SLI/Error Budget formal.
- Takde dashboard track % freshness SLO dipenuhi.
- Error Budget policy bila freeze release belum defined.
### M3: Incident Management + Post-Mortem 🟡
| Evidence | Repo | Status |
|---|---|---|
| RCA silent schema down-casting | banking | ✅ |
| RCA arithmetic error at full volume | banking | ✅ |
| RCA oversized compute pool | Credit Risk | ✅ |
| Slack failure alerting | Credit Risk | ✅ |
| Serial fallback aborting parallel | Credit Risk | ✅ |
| SQL dialect fallback MERGE 2-step | migration_fiber ADR-008 | ✅ |
| Parity validation before/after | migration_fiber/parity_check.py | ✅ |
| On-call SLA ownership | Banking production | ✅ |
Gap M3: Ada RCA discipline tapi BELUM ada blameless post-mortem template formal.
### M4: Burn-Rate Alerting ❌ GAP TERBESAR
| Evidence | Repo | Status |
|---|---|---|
| Slack failure alert basic | Credit Risk | ✅ ada tapi = alert fatigue |
| Airflow SLA miss callback | paysim | ✅ |
| SLA Gym traps TRAINING SAHAJA | pharma | ✅ training artifact |
| Burn-rate model | — | ❌ BELUM ADA |
| PagerDuty integration | — | ❌ BELUM ADA |
Gap M4: Basic Slack alert fire on ANY failure = alert fatigue.
Burn-rate model dan PagerDuty belum ada.
Playbook blueprint guna GE API versi lama (0.x) — kena update ke 1.x.
### M5: Idempotency + Recovery ✅
| Evidence | Repo | File | Status |
|---|---|---|---|
| Checkpoint-resume S3 JSON | paysim | silver/cumulative_pipeline.py | ✅ |
| Delta MERGE upsert | olist | transform_silver.py:307-320 | ✅ |
| Delta MERGE upsert | paysim | cumulative balance MERGE | ✅ |
| Delta MERGE upsert | banking | silver/silver_fraud.py | 🟡 belum run live |
| Atomic publish pointer-swap | pharma | gold/<run_id>/ ke _current/ | ✅ |
| Exactly-once dedup | banking, paysim | promotion gate + checkpoint | ✅ |
| Watermark state dalam lake | banking | pipeline/common/watermark.py | ✅ |
| SCD2 preserve history | banking, olist, migration_fiber, pharma, home-credit | multiple | ✅ |
| Delta Time Travel recovery | playbook blueprint | restoreToVersion(142) | 🔵 |
### M6: Zero-Trust + IaC 🟡
| Evidence | Repo | File | Status |
|---|---|---|---|
| Terraform IaC S3 + Snowflake | banking | snowflake_serving.tf | ✅ |
| Unity Catalog access control | banking | databricks.yml | ✅ |
| PII masking hash-once-at-Silver | banking, olist, home-credit, migration_fiber | _sha256 | ✅ |
| Zero public access S3 | banking | aws_s3_bucket_public_access_block | ✅ |
| dbt least-privilege env segregation | semua repo | profiles.yml | ✅ |
| OIDC Role Federation | — | — | ❌ GAP |
---
## BAHAGIAN 3 — COST OPTIMIZATION (terpisah dari SRE)
Kerangka: Databricks/Spark tuning guide. SRE = ops. Spark guide = cost.
| # | Prinsip | Status |
|---|---|---|
| 1 | Proses kurang (pruning, ZORDER, window dedup) | ✅ banking/olist/migration_fiber/paysim |
| 2 | Elak shuffle (broadcast join, partition tune) | ❌ GAP KRITIKAL |
| 3 | Kira sekali (incremental, checkpoint, $0 dev) | ✅ paysim/pharma/creative_lab |
| 4 | Right-size (serverless, cost guardrail) | ✅ Volve ADR-002, banking Terraform |
| 5 | Parallelize independent (control vs data plane) | ✅ banking ADR-011 |
Evidence ringkas:
- Partition pruning     ✅ banking/olist/migration_fiber/paysim
- OPTIMIZE+ZORDER       ✅ banking/compaction.py 8 fact/bridge ZORDER customer_id
                           NOTE: docs cheatsheet kata 🟡 SALAH — code dah landed
- Window dedup          ✅ olist/paysim
- Incremental MERGE     ✅ paysim cumulative_pipeline.py
- Checkpoint-resume     ✅ paysim checkpoint.json ke S3
- $0 dev loop           ✅ pharma + creative_lab SAHAJA (4 repo lain = env-segregation)
- Serverless vs cluster ✅ Volve ADR-002 zero Spark SQL Warehouse (senior instinct)
- Cost guardrail TF     ✅ banking snowflake_serving.tf
- Pre-flight local test ✅ home-credit/migration_fiber COST_LOG.md
- Spark .cache()        ❌ gap kecil
- Streaming/Kafka       ❌ gap (semua batch)
- Broadcast/shuffle     ❌ gap KRITIKAL
---
## BAHAGIAN 4 — INTEGRITY RULES (WAJIB ENFORCE)
Rule 1: Banking MDM crosswalk = manufactured overlap
  SAY: "I engineered controlled overlap into public datasets to prove the resolution logic works"
  DONT SAY: "I resolved real customer identities"
Rule 2: SLA Gym traps = training drill BUKAN production
  pharma gym_l*_trap.py = deliberately sabotaged DAGs kau tulis sendiri
  SAY: "training drills I built to practise identifying anti-patterns"
  DONT SAY: "production incidents I handled"
Rule 3: Banking MERGE silver_fraud.py = belum run live
  SAY: "the pattern is implemented; live-run verification is pending"
  DONT CLAIM: dah run dalam production
Rule 4: $0 dev loop = pharma + creative_lab SAHAJA
  4 repo lain = env-segregation bukan $0
  DONT CLAIM $0 untuk banking/home-credit/paysim/olist
Rule 5: Volve ADR-002 = cost decision bukan Spark tuning
  SAY: "the instinct to know when NOT to use Spark"
  BUKAN: shuffle tuning claim
Rule 6: Shuffle tuning = gap tulen
  SAY: "I understand the concept; haven't explicitly optimised shuffle in production"
  DONT CLAIM: hands-on shuffle tuning
Rule 7: Streaming = gap tulen
  Semua pipeline batch atau incremental. Takde Kafka, takde late data logic.
---
## BAHAGIAN 5 — GAP PRIORITY
P1: SLO/Error Budget formal (M2/M4) — PALING KRITIKAL
    Ada quality gates tapi belum frame sebagai SLO/error budget.
P2: Burn-rate alerting (M4)
    Ada Slack alert tapi bukan burn-rate model.
    Note: update GE API lama dalam playbook ke versi 1.x dulu.
P3: Blameless post-mortem template (M3)
    Ada RCA discipline tapi bukan format berstruktur 7 bahagian.
P4: Shuffle tuning / broadcast join (Spark tuning guide — terpisah dari SRE)
    Gap cost optimization. Faham konsep, belum optimize dalam production.
P5: OIDC federation (M6)
    Lower priority — IaC foundation dah ada.
---
## BAHAGIAN 6 — REPO BUILD ORDER
Tier 0: home-credit → paysim (core Medallion, simplest)
Tier 1: olist (SCD2 + Delta MERGE compose)
Tier 2: migration_fiber (14 ADR deepest trail, study the DIFF)
Tier 3: pharma (10 ADR, MDM, atomic publish, interview cheatsheet)
Tier 4: creative_lab → migration_creative_lab (GenAI production)
Tier 5: Volve (0 tests GAP, SQL Warehouse only, MLflow)
Tier 6: banking + airflow-dag (capstone — LAST)
3 repo paling penting kalau masa terhad:
banking + migration_fiber + pharma (cover 14/17 pattern)
---
## BAHAGIAN 7 — PYTHON TRACK (BERASINGAN)
Track A — Projek Python berasingan. JANGAN campur di sini.
Video: YouTube ZvU7lupoXQE 5j 27m 12 chapter
Master doc Google Docs: 1tke_GvXJX9klF1o-kzom0yj60_p-dRhjeZ8g_t3VkCU
Status: Ch 2 & 3 selesai. Kuiz seterusnya = Ch 4 String Formatting.
---
## CARA UPDATE
1. Bila gap dah tutup: tukar tanda ke ✅
2. Update "Last updated" setiap sesi
3. Append je, jangan replace
4. Raja Luqman update sendiri — session tak boleh tulis ke file ni
