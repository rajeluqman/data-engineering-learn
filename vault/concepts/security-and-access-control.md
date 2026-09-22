# Security & Access Control

> **One line:** who can see or touch which data, and how that's enforced without engineers manually gatekeeping every request.

**Spread:** 5/6 book sources · SQL track · verified via `vault/state/build_concept_index.py`

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Airflow | [[ch16_securing_airflow\|Ch.16 Securing Airflow]] | The dedicated chapter — by far the heaviest coverage (84 hits): RBAC, Fernet encryption, LDAP, HTTPS/TLS, secrets backends |
| Airflow | [[ch17_airflow_deployment_options\|Ch.17 Deployment Options]] | Security implications of each deployment model |
| Airflow | [[ch12_best_practices\|Ch.12 Best Practices]] | Centralized credentials as a named best practice |
| fundamentals_de | [[ch10_security_and_privacy\|Ch.10 Security & Privacy]] | The general DE-lifecycle treatment of security |
| Databricks | [[ch05_lakeflow_connect_sql_server_connector\|Ch.5 Lakeflow Connect]] | Connector-level credential management via Unity Catalog service credentials |
| Kimball | [[ch21_big_data_analytics\|Ch.21 Big Data Analytics]], [[ch19_etl_subsystems_and_techniques\|Ch.19 ETL Subsystems]] | Security as an ETL subsystem concern |
| DDIA | [[ch04_encoding_and_evolution\|Ch.4 Encoding & Evolution]] | Light touch — encoding-format security implications |

---

## The thread

Airflow Ch.16 is the reference chapter for this concept — it's the only source that treats security as a full system (identity, encryption, network, secrets) rather than a scattered concern. Databricks Ch.5's "credentials never exposed in logs or hardcoded" property is the same discipline Airflow Ch.12 names as a best practice (centralized credentials), just enforced by the platform (Unity Catalog) instead of by convention.

## Related

[[lineage-and-governance]] · [[ingestion-patterns]]
