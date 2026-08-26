# M5: Idempotency, Delta Engine & Resilience Engineering
Source: Staff DE SRE Playbook — Modul 5
Status dalam repo kau: ✅ mostly covered
---
## Idempotency — apa dia
Analogi: Butang lif. Tekan 1 kali atau 100 kali — lif datang sekali je.
Pipeline idempotent: run 10 kali dengan input sama — hasil sama, tiada duplikasi.
---
## Evidence dalam repo kau
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
---
## Delta MERGE pattern (idempotent upsert)
  MERGE INTO banking_catalog.gold.dim_customer AS target
  USING (
      SELECT customer_id, name, email, current_timestamp() AS updated_at
      FROM banking_catalog.silver.stg_customers
  ) AS source
  ON target.customer_id = source.customer_id
  WHEN MATCHED AND (target.name <> source.name OR target.email <> source.email)
      THEN UPDATE SET
          target.name = source.name,
          target.email = source.email,
          target.updated_at = source.updated_at
  WHEN NOT MATCHED
      THEN INSERT (customer_id, name, email, updated_at)
           VALUES (source.customer_id, source.name, source.email, source.updated_at);
---
## Delta Time Travel Recovery
  from delta.tables import DeltaTable
  deltaTable = DeltaTable.forPath(spark, "s3://banking-lakehouse/gold/fact_transactions")
  deltaTable.restoreToVersion(142)
  Status: 🔵 pattern documented, belum run dalam repo sebenar kau.
  Claim sebagai "pattern yang boleh apply" bukan "yang aku dah run".
---
## Checkpoint-Resume pattern
  def _read_checkpoint(spark, checkpoint_path):
      """Return last completed day from checkpoint.
      Raises loudly if unreadable — manual investigation required.
      Better than silently restarting from zero and double-counting."""
---
## Atomic Publish / Pointer-Swap (pharma)
  Build ke  gold/<run_id>/     (verify completeness dulu)
  Copy ke   gold/_current/     (baru consumers boleh baca)
  Rollback = re-publish older run_id. Instant, zero data loss.
