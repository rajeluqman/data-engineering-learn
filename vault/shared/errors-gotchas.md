# Errors & Gotchas

Append new entries as encountered. Format: # + title, then details.

---

## SQL-001 — Silent error: missing brace in multiple WHERE conditions

**Symptom:** Query runs, no syntax error, but wrong rows returned.
**Cause:** OR condition bleeds outside intended scope.
**Fix:** Always wrap each logical group in parentheses.

```sql
-- Wrong
WHERE gender = 'Female' AND country = 'France' OR join_date > '2022-01-01'

-- Correct
WHERE (gender = 'Female') AND (country = 'France' OR join_date > '2022-01-01')
```

---

## SQL-002 — FULL JOIN not supported in MySQL

**Symptom:** Syntax error on FULL JOIN keyword.
**Fix:** Use UNION of LEFT JOIN + RIGHT JOIN.
**Dialect note:** Supported in PostgreSQL, Snowflake, Teradata, Spark SQL.

---

## SQL-003 — MySQL alias readable in HAVING (dialect-specific)

**Symptom:** Works in MySQL, fails in other dialects.
**Cause:** MySQL executes HAVING after SELECT alias is defined.
**Fix for other dialects:** Repeat the full expression in HAVING.

```sql
-- MySQL only
SELECT category, AVG(price) AS avg_price FROM products
GROUP BY category HAVING avg_price > 500;

-- ANSI / other dialects
SELECT category, AVG(price) AS avg_price FROM products
GROUP BY category HAVING AVG(price) > 500;
```

---

## SQL-004 — Anti-join pattern (not a keyword)

**Note:** SQL has no ANTI JOIN keyword.
**Fix:** LEFT JOIN + IS NULL on the right-side key.

```sql
SELECT a.* FROM table_a a
LEFT JOIN table_b b ON a.id = b.id
WHERE b.id IS NULL;
```

---

## SQL-005 — Dedup: use ROW_NUMBER, not DELETE directly

**Reason:** DELETE on duplicates without identifying which to keep is destructive.
**Fix:** ROW_NUMBER() OVER (PARTITION BY key ORDER BY ...) → filter rn = 1.

---

## SQL-006 — QUALIFY (Snowflake only)

**Use:** Filter window function results inline, no subquery needed.

```sql
-- Snowflake
SELECT * FROM sales
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY date DESC) = 1;
```

---

## WIN-001 — Node.js PATH not inherited after install (Windows)

**Symptom:** Obsidian MCP plugin reports "Node not found" even after install.
**Cause:** PATH update only applies to processes started after install.
**Fix:** Full Windows restart after installing Node.js.

---

## SQL-007 — HAVING pada raw column (bukan aggregate)

**Symptom:** Query error atau salah logic.
**Cause:** HAVING digunakan untuk filter column biasa, bukan aggregate result.
**Fix:** Pindah ke WHERE.

```sql
-- Wrong
HAVING country > 3

-- Correct
HAVING total_customers > 3   -- filter aggregate alias
-- atau
WHERE country = 'Malaysia'   -- filter raw column
```

---

## SQL-008 — SUM(column) untuk kira bilangan rows

**Symptom:** Salah result — SUM akan tambah nilai dalam column, bukan count rows.
**Fix:** Guna COUNT(*) untuk kira bilangan rows.

```sql
-- Wrong
SUM(customer)   -- tambah nilai dalam column customer

-- Correct
COUNT(*)        -- kira bilangan rows
```

---

## SQL-009 — ORDER BY column salah untuk business intent

**Symptom:** Sort ikut label (category, country) tapi business nak sort ikut nilai.
**Fix:** ORDER BY aggregate alias, bukan group column.

```sql
-- Wrong (sort alphabetically by category name)
ORDER BY category DESC

-- Correct (sort by sales value)
ORDER BY total_sales DESC
```

---

## SQL-010 — Missing GROUP BY lepas guna aggregate

**Symptom:** SQL error — column in SELECT not in GROUP BY.
**Fix:** Setiap non-aggregate column dalam SELECT mesti ada dalam GROUP BY.

```sql
-- Wrong
SELECT category, SUM(unit_price) AS total_sales
FROM dim_product
-- GROUP BY missing ❌

-- Correct
SELECT category, SUM(unit_price) AS total_sales
FROM dim_product
GROUP BY category
```

---

## SQL-011 — Default ke fact_sales untuk semua query

**Symptom:** Query logic betul tapi join/column tak wujud.
**Cause:** fact_sales ada transaction data je, bukan customer atau product attributes.
**Fix:** Pilih table ikut jenis data yang diperlukan.

| Nak data pasal | Table |
|---|---|
| Customer info | dim_customer |
| Product info | dim_product |
| Sales transactions | fact_sales |

---

## SQL-012 — ORDER BY ASC untuk top-N query

**Symptom:** Query returns lowest values instead of highest.
**Fix:** Top-N (highest first) → ORDER BY DESC.

```sql
-- Wrong (returns lowest)
ORDER BY total_sales ASC

-- Correct (returns highest first)
ORDER BY total_sales DESC
```

---

## SQL-013 — Column duplicate dalam SELECT

**Symptom:** Redundant columns dalam output, confusing result.
**Fix:** Semak SELECT — setiap column sekali je, jangan repeat.

---

## SQL-014 — WHERE untuk filter aggregate result

**Symptom:** SQL error — aggregate functions not allowed in WHERE.
**Cause:** WHERE diproses sebelum GROUP BY, jadi aggregate tak wujud lagi.
**Fix:** Guna HAVING untuk filter aggregate.

```sql
-- Wrong
WHERE AVG(unit_price) > 500   -- ❌ error

-- Correct
HAVING AVG(unit_price) > 500  -- ✅
```
