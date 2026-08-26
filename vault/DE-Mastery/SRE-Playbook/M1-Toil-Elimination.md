# M1: Core SRE Philosophy — Toil Elimination & Blast Radius
Source: Staff DE SRE Playbook — Modul 1
Status dalam repo kau: ✅ mostly covered
---
## Mindset Shift: Script Writer ke Staff Platform Engineer
| Dimensi | Junior DE | Staff DE |
|---|---|---|
| Fokus | Tulis code transform data lulus UAT | Sistem resilient, self-healing, observable |
| Pandangan kegagalan | "Restart balik esok" | "Kenapa timeout? Impact error budget?" |
| Security | Static credentials | Zero-Trust, OIDC, Unity Catalog |
| Data Quality | Ad-hoc SQL bila user komplen | Schema-drift gating automatik, GE |
---
## Toil — apa dia
Analogi: Cuci pinggan guna tangan dari perigi = Toil.
Bina mesin basuh pinggan automatik = Engineering Work.
Dalam DE, Toil adalah:
- Manual restart Airflow DAG bila fail
- Masuk IP manual dalam Security Group
- Tambah column baru manual dalam 20 file dbt
Staff action: Hapus via Terraform, DAB, CI/CD GitHub Actions, Automated Recovery.
---
## Evidence dalam repo kau
| Teknik | Repo | File | Status |
|---|---|---|---|
| Terraform IaC | banking | snowflake_serving.tf (warehouse + resource monitor) | ✅ |
| Databricks Asset Bundle | banking | databricks.yml 22-task job graph | ✅ |
| CI/CD change gating | banking, EZCOM | lint + compile + DQ checks | ✅ |
| Control vs data plane | banking + airflow-dag | ADR-011 | ✅ |
| Local pre-flight test | home-credit, migration_fiber | tests/local/* + COST_LOG.md | ✅ |
| $0 dev loop | pharma, creative_lab SAHAJA | dbt/profiles.yml DuckDB :memory: | ✅ |
---
## Gap M1
OIDC Role Federation belum ada — static credentials masih digunakan.
Fix: Implement AWS OIDC dalam GitHub Actions CI/CD.
---
## Blast Radius Control
Sebarang perubahan kena diuji: sejauh mana kegagalan satu komponen
boleh rosakkan komponen lain?
Banking answer: decoupled architecture via S3 EventBridge + Delta Lake +
dbt star schema + Airflow Datasets. ADR-011 explains the why.
