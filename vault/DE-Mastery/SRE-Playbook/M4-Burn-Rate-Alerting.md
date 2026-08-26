# M4: Advanced SLO-Based Alerting — Anti-Alert Fatigue
Source: Staff DE SRE Playbook — Modul 4
Status dalam repo kau: ❌ GAP TERBESAR
---
## Analogi Penggera Asap vs Kebakaran
Kalau penggera berbunyi setiap kali orang hisap rokok (ANY failure alert)
orang akan matikan penggera. Bila rumah betul-betul terbakar, tiada siapa perasan.
Burn Rate Alerting = penggera hanya bunyi bila kebakaran besar yang
menghakis error budget dengan cepat.
---
## Konsep Burn Rate
  Error Budget = 100% - SLO
  Burn Rate    = Kadar error budget dihakis
  Contoh:
  SLO = 99% (1% error budget = 7.2 jam sebulan)
  Burn Rate 1x  = habis dalam 30 hari (normal)
  Burn Rate 14x = habis dalam 2 hari (KRITIKAL — trigger alert)
Alert patut trigger HANYA bila burn rate tinggi, bukan tiap failure.
---
## Evidence dalam repo kau
| Evidence | Status |
|---|---|
| Basic Slack alert fire on ANY failure | ✅ ada tapi = alert fatigue |
| Airflow SLA miss callback dalam paysim | ✅ |
| SLA Gym traps pharma TRAINING SAHAJA | ✅ training artifact |
| Burn-rate model | ❌ BELUM ADA |
| PagerDuty integration | ❌ BELUM ADA |
---
## Blueprint Code (konsep betul, implement dalam banking context)
  def send_burnrate_alert(context):
      dag_id = context.get('task_instance').dag_id
      execution_date = context.get('execution_date')
      payload = {
          "routing_key": "PAGERDUTY_INTEGRATION_KEY",
          "event_action": "trigger",
          "payload": {
              "summary": f"CRITICAL DATA SLO BREACH: {dag_id}",
              "severity": "critical",
              "custom_details": {
                  "error_budget_impact": "HIGH (Burn Rate > 14x)",
                  "action_required": "Immediate On-Call Action Required"
              }
          }
      }
  default_args = {
      'on_failure_callback': send_burnrate_alert,
      'execution_timeout': timedelta(minutes=45)
  }
Note penting: GE API dalam playbook guna versi lama (0.x).
GE versi 1.x (2025+) dah tukar API sepenuhnya. Kena update syntax bila implement.
---
## Gap M4 — cara tutup
Refer: Gap-Closing\P2-Burn-Rate-Alerting.md
Steps:
1. Define SLO formal dulu (P1 kena habis dulu)
2. Calculate error budget berdasarkan SLO
3. Implement burn-rate logic dalam Airflow callback
4. Replace Slack basic ke PagerDuty dengan threshold
