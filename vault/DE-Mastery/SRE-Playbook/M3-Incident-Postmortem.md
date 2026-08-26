# M3: Production Incident Management & Blameless Post-Mortem
Source: Staff DE SRE Playbook — Modul 3
Status dalam repo kau: 🟡 RCA ada, template formal belum
---
## Analogi Black Box Pesawat
Juruterbang dan penyiasat tak salahkan sesama sendiri.
Analisis kotak hitam untuk cari punca fizikal/sistem supaya tak berulang.
---
## Incident Response Steps
1. Triage dan lantik Incident Commander
2. Mitigate dulu, root-cause kemudian (restore service first)
3. Communication sync — update stakeholder tiap jam: Issue, Impact, Mitigation, ETA
4. Apply safe interim fix
5. RCA selepas fire out
6. Tulis post-mortem
---
## Evidence RCA dalam repo kau
| RCA | Repo | Status |
|---|---|---|
| Silent schema down-casting | banking | ✅ |
| Arithmetic error at full volume | banking | ✅ |
| Oversized compute pool ke throttling | Credit Risk | ✅ |
| Slack failure alerting | Credit Risk | ✅ |
| Serial fallback aborting parallel fan-out | Credit Risk | ✅ |
| SQL dialect fallback MERGE ke 2-step | migration_fiber ADR-008 | ✅ |
| Parity validation before/after migration | migration_fiber/parity_check.py | ✅ |
| On-call SLA ownership real production | Banking | ✅ |
---
## Template Blameless Post-Mortem (7 bahagian wajib)
  BLAMELESS POST-MORTEM REPORT
  Incident Title: [nama]
  Date: [tarikh]
  Incident Commander: [nama]
  Severity: P1/P2/P3
  1. SUMMARY
     [1-2 ayat: apa jadi, berapa lama, apa impact]
  2. IMPACT
     - Data Freshness SLO: breached by X minutes / not breached
     - Error Budget Burn: consumed X% of monthly budget
     - Business impact: [siapa affected]
  3. ROOT CAUSES
     - Structural Cause: [apa dalam sistem yang bagi peluang ni jadi]
     - Testing Defect: [apa test yang sepatutnya catch ni]
     - Governance Defect: [apa process yang missing]
  4. TRIGGER
     [Event spesifik yang trigger incident]
  5. RESOLUTION / MITIGATION
     - [Langkah 1]
     - [Langkah 2]
  6. LESSONS LEARNED
     What went well:
     - [benda yang kerja dengan baik]
     What went wrong:
     - [benda yang boleh lebih baik]
  7. ACTION ITEMS (PREVENTATIVE ENGINEERING)
     [Item 1] [Description] (Owner: [nama], Due: [tarikh])
     [Item 2] [Description] (Owner: [nama], Due: [tarikh])
---
## Gap M3
Ada RCA discipline ✅ tapi BELUM amalkan 7-bahagian format di atas secara berstruktur.
Next incident yang berlaku — tulis post-mortem ikut template ni.
---
## Next action
Refer: Gap-Closing\P3-Postmortem-Template.md
