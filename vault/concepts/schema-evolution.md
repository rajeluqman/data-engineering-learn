# Schema Evolution & Compatibility

> **One line:** changing a data structure's shape over time without breaking every reader and writer that depends on it.

**Spread:** 5/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| DDIA | [[ch04_encoding_and_evolution\|Ch.4 Encoding & Evolution]] | The dedicated theoretical chapter — forward/backward compatibility, encoding formats (Avro, Protobuf, JSON) |
| DDIA | [[ch02_data_models_and_query_languages\|Ch.2 Data Models & Query Languages]] | Schema-on-read vs. schema-on-write as the upstream design decision |
| Databricks | [[ch16_hinge_health_case_study\|Ch.16 Hinge Health]] | Real-world consequence — schema propagation difficulty at 10x data growth |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]], [[ch09_production_grade_data_quality_using_sdp\|Ch.9 Data Quality]] | Managed schema evolution as a connector/pipeline feature |
| Airflow | [[ch13_project_finding_the_fastest_way_to_get_around_nyc\|Ch.13 NYC Project]], [[ch14_project_keeping_family_traditions_alive_with_airflow_and_generative_ai\|Ch.14 Family Traditions Project]] | Schema changes as a practical pipeline-maintenance event |
| fundamentals_de | [[ch08_queries_modeling_transformation\|Ch.8 Queries, Modeling & Transformation]], [[ch07_ingestion\|Ch.7 Ingestion]] | Where schema evolution decisions get made in the lifecycle |
| Kimball | [[ch02_dimensional_modeling_techniques_overview\|Ch.2 Dimensional Modeling Techniques]] | Schema change as *dimensional* change — this is where [[slowly-changing-dimensions|SCD]] enters |

---

## The thread

DDIA Ch.4 gives the vocabulary (forward-compatible: old code reads new data; backward-compatible: new code reads old data) that every other source assumes without restating. Kimball's SCD framework is a special case of this problem scoped to *dimension attribute values* specifically, not the full schema — a SCD Type 2 change is schema-stable but *data*-evolving, which is a subtler distinction than DDIA's chapter alone would suggest. Hinge Health's case study (Ch.16) is the cautionary tale: "difficult to propagate schema and data at the same time" at 10x growth is DDIA's abstract compatibility problem showing up as a real production headache.

## Related

[[slowly-changing-dimensions]] · [[data-quality]] · [[change-data-capture]]
