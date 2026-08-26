# M6: Security-by-Design, Zero Trust & IaC Governance
Source: Staff DE SRE Playbook — Modul 6
Status dalam repo kau: 🟡 Terraform ada, OIDC belum
---
## Prinsip Zero Trust
Staff DE tak simpan static credentials dalam script atau Airflow Connections.
Guna AWS OIDC Role Federation + GitHub Actions + Azure Entra ID RBAC.
---
## Evidence dalam repo kau
| Evidence | Repo | File | Status |
|---|---|---|---|
| Terraform IaC S3 + Snowflake | banking | snowflake_serving.tf | ✅ |
| Unity Catalog access control | banking | databricks.yml | ✅ |
| PII masking hash-once-at-Silver | banking, olist, home-credit, migration_fiber | _sha256 | ✅ |
| Zero public access S3 | banking | aws_s3_bucket_public_access_block | ✅ |
| dbt least-privilege env segregation | semua repo | profiles.yml per env | ✅ |
| OIDC Role Federation | — | — | ❌ GAP |
---
## Terraform Blueprint (dari playbook)
  resource "aws_s3_bucket" "bronze_bucket" {
    bucket = "banking-platform-bronze-prod-s3"
    tags   = { Environment = "Production", Governance = "Strict" }
  }
  resource "aws_s3_bucket_public_access_block" "bronze_privacy" {
    bucket                  = aws_s3_bucket.bronze_bucket.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }
  resource "databricks_grants" "bronze_grants" {
    table = "banking_catalog.bronze.transactions_raw"
    grant {
      principal  = "data_engineers_group"
      privileges = ["SELECT", "MODIFY"]
    }
    grant {
      principal  = "bi_analysts_group"
      privileges = []  # ZERO ACCESS TO RAW BRONZE
    }
  }
---
## Gap M6
OIDC federation belum implement. Ini yang elak static credentials dalam CI/CD.
Lower priority dari M2/M3/M4 — IaC foundation dah ada.
