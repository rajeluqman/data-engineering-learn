# P2: Burn-Rate Alerting — Gap Closing Guide
Priority: 2
Prerequisite: P1 SLO/Error Budget mesti ada dulu
Status: ❌ Belum implement
---
## Kenapa bukan basic Slack alert
Basic alert: fire on ANY failure ke alert fatigue ke orang ignore ke real incident missed.
Burn-rate: fire hanya bila error budget dihakis CEPAT — setiap alert meaningful.
---
## Step 1: Hitung burn rate threshold
  Contoh: SLO Freshness = 99% (error budget = 7.3 jam/bulan)
  Burn rate 14x = habis dalam 2 hari = KRITIKAL
  MONTHLY_BUDGET_MINUTES = 7.3 * 60  # 438 minit
  BURN_RATE_THRESHOLD = 14  # 14x normal = trigger PagerDuty
---
## Step 2: Implement dalam Airflow callback (banking-airflow-dag context)
  def send_burnrate_alert(context):
      """
      Trigger HANYA bila critical pipeline fail yang akan
      menghakis error budget dengan cepat.
      """
      dag_id = context.get('task_instance').dag_id
      execution_date = context.get('execution_date')
      estimated_delay_minutes = 45  # ikut execution_timeout
      budget_consumed_pct = (estimated_delay_minutes / MONTHLY_BUDGET_MINUTES) * 100
      payload = {
          "routing_key": "PAGERDUTY_INTEGRATION_KEY",
          "event_action": "trigger",
          "payload": {
              "summary": f"CRITICAL SLO BREACH: {dag_id}",
              "severity": "critical",
              "custom_details": {
                  "error_budget_consumed": f"{budget_consumed_pct:.1f}%",
                  "burn_rate": f"{BURN_RATE_THRESHOLD}x",
                  "action": "Immediate On-Call Response Required"
              }
          }
      }
      # requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)
  default_args = {
      'on_failure_callback': send_burnrate_alert,
      'execution_timeout': timedelta(minutes=45)
  }
---
## Step 3: Differentiate alert level
  Burn Rate 1x      No alert (normal operation)
  Burn Rate 2-5x    Slack warning (team awareness)
  Burn Rate 6-13x   Slack urgent (senior DE attention)
  Burn Rate 14x+    PagerDuty critical (on-call response)
---
## Note GE API
Playbook blueprint guna GE 0.x API. GE 1.x (2025+) tukar sepenuhnya.
Bila implement GE component dalam burn-rate logic, search GE 1.x docs dulu.
