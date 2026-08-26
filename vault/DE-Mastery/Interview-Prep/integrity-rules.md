# Integrity Rules — Wajib Enforce Setiap Interview
Satu angka yang tak boleh dipertahankan lebih mahal dari lima bullet kosong.
Semua rule ni berdasarkan evidence sebenar dalam repo kau.
---
## Rule 1 — Banking MDM crosswalk = manufactured overlap
  SAY:
  "I engineered controlled overlap into public datasets that don't naturally
  share customers, to prove the identity-resolution logic works."
  DON'T SAY:
  "I resolved real customer identities"
---
## Rule 2 — SLA Gym = training drill, BUKAN production
  pharma/gym_l*_trap.py = deliberately sabotaged DAGs kau tulis sendiri
  SAY:
  "Training drills I built to practise identifying anti-patterns"
  DON'T SAY:
  "Production incidents I handled"
---
## Rule 3 — Banking MERGE = belum run live
  silver_fraud.py docstring sendiri kata:
  "Not executed against live Bronze data this session, written and
  py_compile-checked; live-run verification pending"
  SAY:
  "The pattern is implemented; live-run verification is pending"
  DON'T CLAIM:
  Dah run dalam production
---
## Rule 4 — $0 dev loop = pharma + creative_lab SAHAJA
  4 repo lain (banking, home-credit, paysim, olist):
  Snowflake semua target = env-segregation, BUKAN $0
  DONT CLAIM $0 untuk 4 repo tu
---
## Rule 5 — Volve = cost decision, bukan Spark tuning
  ADR-002: "classic clusters burn $0.15-0.40/DBU"
  = dokumentasi keputusan cost, bukan hands-on shuffle tuning
  SAY:
  "The instinct to know when NOT to use Spark"
  BUKAN:
  Shuffle tuning atau performance optimization claim
---
## Rule 6 — Shuffle tuning = gap tulen
  Ada Spark dalam stack tapi takde evidence broadcast join
  atau shuffle tuning eksplisit dalam mana-mana repo.
  SAY:
  "I understand the concept; haven't explicitly optimised shuffle
  in production"
  DON'T CLAIM:
  Hands-on shuffle tuning
---
## Rule 7 — Streaming = gap tulen
  Semua pipeline kau adalah batch atau incremental.
  Takde Kafka, takde watermark handling, takde late data logic.
  Kalau JD sebut streaming expertise:
  "My experience is batch and incremental — I understand streaming
  concepts but haven't implemented production streaming pipelines."
---
## Semak diri sebelum interview
Baca list ni 10 minit sebelum masuk interview.
Kalau rasa nak claim sesuatu yang tak ada dalam ✅ list — jangan.
Better cakap jujur gap tu dan explain cara kau akan tutup dia.
