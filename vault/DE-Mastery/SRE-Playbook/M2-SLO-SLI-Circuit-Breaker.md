# M2: SLO/SLI + Circuit Breaker + Error Budget
Source: Staff DE SRE Playbook — Modul 2
Status dalam repo kau: 🟡 Gates ada, bahasa formal belum
---
## Analogi Pizza Delivery
- SLI: % masa pizza sampai dalam 25 minit
- SLO: 95% pesanan sampai dalam 30 minit
- SLA: Lewat 45 minit = pizza percuma (penalti kewangan)
- Error Budget: 5% yang dibenarkan lambat
---
## 4 Metrik Data SLI
1. Data Freshness    — event generation ke available dalam Gold
2. Data Completeness — % record berjaya ingest vs anggaran
3. Data Correctness  — % lulus GE test suite
4. Pipeline Availability — % DAG selesai tanpa manual intervention
---
## Error Budget Policy
Bila error budget susut ke 0%:
- DILARANG deploy feature baru
- DILARANG dbt refactoring atau PySpark optimization baru
- 100% effort ke perbaiki stabiliti + testing coverage + technical debt
---
## Evidence dalam repo kau
| Evidence | Repo | File | Status |
|---|---|---|---|
| Layered GE gates Bronze WARN Silver strict | home-credit, olist, paysim, pharma, Volve | gx/run_*_suite.py | ✅ |
| Quarantine/DLQ bad record | banking | promotion_gate.py | ✅ |
| Schema-drift gating fail loud | banking | promotion_gate.py:75-84 | ✅ |
| Coverage-as-KPI-distribution | pharma | cheatsheets/08_dq.md | ✅ |
| Reconciliation on drift | EZCOM | row-count check | ✅ |
---
## Gap M2 KRITIKAL
1. Ada gates tapi BELUM frame sebagai SLO/SLI/Error Budget.
2. Takde dashboard track berapa % freshness SLO dipenuhi minggu ni.
3. Error Budget policy bila freeze release belum defined.
4. Circuit breaker + DLQ write belum integrate jadi satu unit.
---
## Blueprint Code (GE API kena update ke v1.x dulu)
Konsep circuit breaker:
  if not validation_results["success"]:
      # Write corrupted records to DLQ table
      corrupted_records.write.format("delta").mode("append")
          .saveAsTable("banking_catalog.bronze.transactions_dlq")
      raise ValueError("Pipeline halted. Check DLQ table.")
  else:
      # Write clean records to Silver
      clean_df.write.format("delta").mode("append")
          .saveAsTable("banking_catalog.silver.transactions_clean")
Note: Playbook blueprint guna GE 0.x API. GE 1.x (2025+) dah tukar API.
Kena update syntax bila implement sebenar.
---
## Next action
Refer: Gap-Closing\P1-SLO-Error-Budget.md
