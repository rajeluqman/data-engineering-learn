# Drill — M1 Business Question Decode
Date: 2026-08-25

---

## Round 1 — Framework decode (no full query)

**Q: "Berapa ramai customer per country?"**
- GROUP BY: `country`
- Aggregate: `COUNT(*)`
- Table: `dim_customer`
- HAVING: —

**Q: "Average unit price per category, only avg > 300"**
- GROUP BY: `category`
- Aggregate: `AVG(unit_price)`
- HAVING: `avg_price > 300`
- Table: `dim_product`

**Q: "Total quantity per product, only > 50 unit, highest first"**
- GROUP BY: `product_key`
- Aggregate: `SUM(quantity)`
- HAVING: `total_sold > 50`
- ORDER BY: `total_sold DESC`
- Table: `fact_sales`

---

## Round 2 — Full query writing

### Q: "Total sales per category, only total > 500, highest first"

❌ Common mistakes:
- `WHERE total_sales > 500` → should be `HAVING`
- Missing `GROUP BY`
- Wrong table (fact_sales instead of dim_product)

✅ Correct:
```sql
SELECT category, SUM(unit_price) AS total_sales
FROM dim_product
GROUP BY category
HAVING total_sales > 500
ORDER BY total_sales DESC;
```

---

### Q: "Berapa ramai customer per country, only > 3"

❌ Common mistakes:
- `SUM(customer)` instead of `COUNT(*)`
- `HAVING country > 3` instead of `HAVING total_customers > 3`
- `ORDER BY country` instead of `ORDER BY total_customers`

✅ Correct:
```sql
SELECT country, COUNT(*) AS total_customer
FROM dim_customer
GROUP BY country
HAVING total_customer > 3
ORDER BY total_customer DESC;
```

---

## Weak spots — kena drill lagi

1. **GROUP BY** — selalu tertinggal masa tulis full query
2. **Table selection** — jangan default semua ke fact_sales
3. **WHERE vs HAVING** — dah faham concept, tapi kena build habit
