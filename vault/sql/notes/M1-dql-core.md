# M1 — DQL Core

## SELECT & Projection

Pilih column yang nak dipaparkan. Non-aggregate column dalam SELECT **mesti** masuk GROUP BY.

## WHERE — Filtering

Filter row **sebelum** aggregation. Guna untuk raw column value (gender, country, date).

```sql
WHERE country = 'Malaysia'
WHERE join_date > '2022-01-01'
```

## GROUP BY — Aggregation

### Framework: Decode Business Question → SQL

Setiap business question, tanya 3 soalan ikut turutan:

**Soalan 1 — "PER apa?" → GROUP BY**
Cari keyword: "per", "each", "by", "setiap", "ikut"
- "sales per category" → `GROUP BY category`
- "customers by country" → `GROUP BY country`

**Soalan 2 — "Nak KIRA apa?" → Aggregate function**

| Business word | Function |
|---|---|
| how many, berapa ramai, count | COUNT(*) |
| total, sum, jumlah | SUM(column) |
| average, purata, avg | AVG(column) |
| highest, maximum | MAX(column) |
| lowest, minimum | MIN(column) |

**Soalan 3 — "Filter RAW atau AGGREGATE?" → WHERE vs HAVING**
- Filter raw column value → **WHERE**
- Filter hasil pengiraan (count > 5, avg > 200) → **HAVING**

### Rule wajib
- Ada COUNT/SUM/AVG dalam SELECT → **MESTI ada GROUP BY**
- Setiap non-aggregate column dalam SELECT → **MESTI masuk GROUP BY**

### Table selection

| Nak data pasal | Table |
|---|---|
| Customer info | dim_customer |
| Product info | dim_product |
| Sales transactions | fact_sales |
| Date/time | dim_date |

### Visualize output dulu sebelum tulis query

Lukis expected output dalam kepala dahulu:

```
category    | total_sales
------------|------------
Electronics | 1200
```

Bila dah visualize, kau dah tau column mana SELECT, mana aggregate.

## HAVING — Filter on Aggregates

Filter **selepas** GROUP BY. Guna untuk hasil pengiraan.

```sql
-- Betul
HAVING total_sales > 500
HAVING COUNT(*) > 3

-- Silap (guna WHERE untuk aggregate)
WHERE total_sales > 500  -- ❌
```

## ORDER BY & LIMIT / TOP

```sql
ORDER BY total_sales DESC   -- highest first (top-N)
ORDER BY total_sales ASC    -- lowest first
```

Default ORDER BY = ASC. Untuk top-N, **wajib DESC**.

## Execution Order

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

## DE/DA Application

Query template standard untuk business questions:

```sql
SELECT <group_column>, <aggregate_function> AS <alias>
FROM <table>
WHERE <raw_filter>          -- optional
GROUP BY <group_column>
HAVING <aggregate_filter>   -- optional
ORDER BY <alias> DESC
LIMIT <n>;                  -- optional
```
