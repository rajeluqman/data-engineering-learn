# Dimensional Modeling & Grain

> **One line:** organizing a warehouse around facts (measurable events) and dimensions (the context that describes them), with "grain" as the non-negotiable first decision — what does one row in this fact table actually represent?

**Spread:** 3/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Kimball | [[ch03_retail_sales\|Ch.3 Retail Sales]], [[ch01_dw_bi_dimensional_modeling_primer\|Ch.1 DW/BI Primer]], [[ch15_electronic_commerce\|Ch.15 Electronic Commerce]], [[ch06_order_management\|Ch.6 Order Management]], [[ch02_dimensional_modeling_techniques_overview\|Ch.2 Dimensional Modeling Techniques]] | The entire book's organizing discipline — by far the vault's heaviest single-concept coverage (72+61+58+48+45 hits just in the top 5 chapters) |
| DDIA | [[ch03_storage_and_retrieval\|Ch.3 Storage & Retrieval]] | The storage-engine perspective on why star-schema-shaped queries are fast (column-oriented storage, index design) |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]], [[ch11_future_of_data_engineering\|Ch.11 Future of DE]] | Dimensional modeling as one modeling paradigm among several (contrasted with normalized/Data Vault approaches) |

### Your own track notes

- SQL track — [[master_sql_data_with_baraa\|Baraa]] (56 hits) — your SQL fundamentals already build toward this without naming it explicitly

---

## The thread

Kimball is *the* source for this — nothing else attempts its depth, and nothing else should try to compete with it. DDIA Ch.3 is worth reading immediately after any Kimball chapter: it explains *mechanically* why a star schema (few large fact tables, many small dimension tables) performs well on columnar storage — Kimball tells you the modeling rule, DDIA tells you why the rule pays off physically. "Grain" — the single most important sentence you write when designing a fact table — is the concept every other Kimball chapter (transaction/periodic-snapshot/accumulating-snapshot fact types, all SCD handling) assumes you got right first.

## Related

[[keys-surrogate-natural]] · [[slowly-changing-dimensions]] · [[medallion-layering]] · [[joins]]
