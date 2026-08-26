# P4: Shuffle Tuning / Broadcast Join — Gap Closing Guide
Priority: 4
Kerangka: Spark tuning guide (BUKAN SRE playbook — ini cost optimization)
Status: ❌ Gap tulen — faham konsep, belum optimize dalam production
---
## Kenapa shuffle mahal
Shuffle = data bergerak antara node dalam Spark cluster.
Setiap shuffle = network I/O + disk write/read + rebalancing.
Dalam large dataset, shuffle boleh jadi 80% daripada total job time.
Analogi: Pindah barang antara 5 warehouse berbeza setiap kali nak sort.
Lagi baik: sort dalam satu warehouse, hantar sekali je.
---
## Dua jenis join dalam Spark
Sort-Merge Join (default untuk table besar):
  Kedua-dua table shuffle ikut join key
  Expensive bila kedua-dua besar
  O(n log n) sort untuk setiap partition
Broadcast Join (untuk table kecil):
  Table kecil dihantar ke SETIAP node (broadcast)
  Tiada shuffle untuk table besar
  O(1) lookup
  Sesuai bila table kecil < 10MB (default threshold)
---
## Bila guna mana
  Table kecil (<10MB) + Table besar  = Broadcast join
  Table besar + Table besar           = Sort-merge (default)
  Table medium + Table besar          = Tune broadcast threshold
---
## Implement dalam banking context
  from pyspark.sql.functions import broadcast
  # banking: join fact_txn (besar) dengan dim_customer (kecil)
  # CARA MAHAL — sort-merge join (shuffle fact_txn)
  result = fact_txn.join(dim_customer, "customer_id")
  # CARA MURAH — broadcast dim_customer (tiada shuffle untuk fact_txn)
  result = fact_txn.join(broadcast(dim_customer), "customer_id")
  # Tune threshold untuk semua join dalam session
  spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)  # 50MB
---
## Teknik lain reduce shuffle
  # Adaptive Query Execution (AQE) — Spark 3+
  spark.conf.set("spark.sql.adaptive.enabled", "true")
  spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
  # Tune partition count
  spark.conf.set("spark.sql.shuffle.partitions", "auto")  # Spark 3+ AQE
  # Elak repartition yang tak perlu
  # JANGAN: df.repartition(200).groupBy("key").agg(...)
  # BUAT:   df.groupBy("key").agg(...)  — biar AQE handle
---
## Claim selamat untuk interview
  SAY:
  "I understand shuffle is the primary cost driver in Spark — broadcast
  joins for small dimensions, AQE for adaptive partition tuning. I haven't
  explicitly profiled and optimised shuffle in production, but I know where
  to look: Spark UI Exchange nodes in the DAG."
  DON'T SAY:
  "I've tuned shuffle performance in production"
---
## Next step untuk tutup gap ni
1. Bukak Spark UI untuk banking fact_txn job
2. Tengok Exchange nodes dalam DAG — ini shuffle
3. Identify table mana candidate untuk broadcast
4. Implement broadcast hint
5. Compare before/after duration dalam Spark UI
6. Tulis ADR untuk document decision
