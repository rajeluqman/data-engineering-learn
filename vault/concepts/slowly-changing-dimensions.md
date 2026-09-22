# Slowly Changing Dimensions

> **One line:** deciding what happens when an attribute of a dimension (a customer's address, a product's category) changes — overwrite it, keep history, or something in between.

**Spread:** 3/6 book sources · SQL + Python tracks · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Kimball | [[ch05_procurement\|Ch.5 Procurement]] | Heaviest coverage — worked SCD examples in a procurement domain |
| Kimball | [[ch02_dimensional_modeling_techniques_overview\|Ch.2 Dimensional Modeling Techniques]] | The canonical reference — Types 0 through 7, not just the famous 1/2/3 |
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | SCD as a named ETL subsystem (the mechanics of *implementing* the change, not just the taxonomy) |
| Kimball | [[ch07_accounting\|Ch.7 Accounting]], [[ch09_human_resources_management\|Ch.9 HR]] | Domain-specific SCD scenarios |
| Databricks | [[ch06_implement_cdc_and_scd_type_2_with_lakeflow\|Ch.6 CDC + SCD2]] | The production implementation — SCD Type 2 built via `apply_changes_from_snapshot`, `__START_AT`/`__END_AT` columns |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]], [[ch13_nfcu_case_study\|Ch.13 NFCU]] | SCD as a downstream consumer of CDC feeds |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]] | SCD as one modeling decision among several |

### Your own track notes

- SQL track — `M10-de-project`, `M7-de-scenarios` frame SCD as a scenario-based interview question

---

## The thread

Kimball's Types 0–7 is the full taxonomy; Databricks Ch.6 shows you the *only two* that matter in almost every real pipeline (Type 1 overwrite, Type 2 new-row-with-history) implemented end to end, from a [[change-data-capture|CDC]] feed straight into a queryable history table. The `__START_AT`/`__END_AT` columns Databricks generates are the physical implementation of what Kimball describes abstractly as "row effective date... row expiration date." This concept doesn't work without [[keys-surrogate-natural|surrogate keys]] — a natural key alone can't represent two versions of the same entity as two distinct rows.

## Related

[[keys-surrogate-natural]] · [[change-data-capture]] · [[dimensional-modeling]] · [[medallion-layering]]
