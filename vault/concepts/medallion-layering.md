# Medallion / Layered Architecture

> **One line:** organizing a data platform into progressively cleaner layers — raw as-landed data, validated/conformed data, business-ready data — so each layer has one clear job.

**Spread:** widened manually — the automated scanner found 579 hits but all in `databricks_big_book_4e` (Bronze/Silver/Gold is Databricks-specific vocabulary). The *concept* also appears under different names elsewhere. See methodology note in [[_BUILD-SPEC|the build spec]].

---

## ⚠️ Why the automated scan missed this

The scanner's patterns (`medallion`, `bronze`, `silver`, `gold`, `staging`) are Databricks' specific product vocabulary. Kimball and fundamentals_de teach the *same layering discipline* under older, more generic names: "staging area" and "presentation layer." A search for "bronze" will never find "staging area," even though they're doing the same architectural job.

---

## Where it appears

### Databricks' named layers (Bronze / Silver / Gold)

| Source | Chapter | Angle |
|---|---|---|
| Databricks | [[ch12_ifood_case_study\|Ch.12 iFood]] | The clearest worked example — Bronze consolidates per-product tables, Silver applies quality rules + Liquid Clustering, Gold serves analysts |
| Databricks | [[ch06_implement_cdc_and_scd_type_2_with_lakeflow\|Ch.6 CDC + SCD2]] | Bronze = raw replicated tables, Silver = SCD Type 2 history — the layering *is* the mechanism, not decoration |
| Databricks | [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]], [[ch01_introduction_to_data_engineering_on_databricks\|Ch.1 Introduction]] | Layering as the default Lakeflow project structure |

### The same discipline, older vocabulary

| Source | Chapter | Angle |
|---|---|---|
| Kimball | [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] (p506) | "Staging area" as an explicitly named exception zone — normalized structures are wrong for the presentation layer but "appropriate in the ETL staging area" — i.e. Bronze/Silver-equivalent has different rules than Gold-equivalent |
| Kimball | [[ch01_dw_bi_dimensional_modeling_primer\|Ch.1 DW/BI Primer]] | The presentation layer (star schemas, dimensional models) as the Gold-equivalent — the layer end users actually query |
| fundamentals_de | [[ch03_designing_good_data_architecture\|Ch.3 Designing Good Data Architecture]] | Layered architecture as a general design principle, not tied to any vendor's naming |

---

## The thread

Kimball's "staging area → presentation layer" split predates "Bronze → Gold" by decades and is architecturally identical: raw/normalized data lives in a zone with relaxed modeling rules, business-facing data lives in a zone with strict dimensional rules, and you never let end users query the staging zone directly. Databricks' Bronze/Silver/Gold just adds a named middle layer (Silver) for the SCD-history/quality-validated step that Kimball folds into "staging." Once you see this, "which layer does X belong in?" becomes the same question whether you're speaking Kimball or Databricks.

## Related

[[dimensional-modeling]] · [[data-quality]] · [[change-data-capture]] · [[slowly-changing-dimensions]]
