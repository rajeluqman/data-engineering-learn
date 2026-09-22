# Concept Spread Index (GENERATED — do not hand-edit)

> Regenerate with `python vault/state/build_concept_index.py`.
> Mapping is measured by regex scan, not recalled. Term lists are a hypothesis;
> the concept->chapter mapping below is evidence.

- Files scanned: **138**
- Cross-cutting threshold: appears in **>= 3** distinct book sources
- Cross-cutting concepts found: **32**
- Narrow (single/dual-source) concepts: **2**

## Cross-cutting concepts (hub candidates)

| Concept | Book sources | Chapters | Hits |
|---|---|---|---|
| Data Quality & Expectations | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 58 | 311 |
| Partitioning & Clustering | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 54 | 815 |
| Checkpointing & Fault Recovery | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 54 | 470 |
| Transactions & Consistency | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 52 | 512 |
| Deduplication | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 50 | 399 |
| Orchestration & Task Dependencies | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 50 | 590 |
| Surrogate, Natural & Business Keys | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 38 | 446 |
| Lineage & Governance | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 36 | 164 |
| Backfill & Reprocessing | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 32 | 134 |
| Testing & Pipeline Validation | 6 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 16 | 57 |
| File Layout & Compaction | 5 (databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 28 | 251 |
| Idempotency & Exactly-Once | 5 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, streaming_systems) | 27 | 159 |
| Security & Access Control | 5 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e) | 26 | 193 |
| Replication & Distributed Coordination | 5 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e) | 24 | 441 |
| Ingestion Patterns & Connectors | 5 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, streaming_systems) | 24 | 123 |
| Change Data Capture & Change Tracking | 5 (databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 22 | 155 |
| Batch vs Streaming | 5 (databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 17 | 58 |
| Event Time vs Processing Time | 5 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, streaming_systems) | 16 | 204 |
| Schema Evolution & Compatibility | 5 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e) | 16 | 52 |
| Aggregation & Combiners | 4 (ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 32 | 260 |
| Incremental vs Full Recompute | 4 (airflow_2e, databricks_big_book_4e, kimball_dwtoolkit_3e, streaming_systems) | 18 | 82 |
| SQL Window Functions | 4 (airflow_2e, databricks_big_book_4e, ddia_kleppmann, fundamentals_de) | 15 | 242 |
| Materialized Views | 4 (databricks_big_book_4e, ddia_kleppmann, fundamentals_de, streaming_systems) | 14 | 45 |
| Slowly Changing Dimensions | 3 (databricks_big_book_4e, fundamentals_de, kimball_dwtoolkit_3e) | 30 | 142 |
| Dimensional Modeling & Grain | 3 (ddia_kleppmann, fundamentals_de, kimball_dwtoolkit_3e) | 29 | 873 |
| Watermarks | 3 (ddia_kleppmann, fundamentals_de, streaming_systems) | 17 | 208 |
| Joins | 3 (databricks_big_book_4e, kimball_dwtoolkit_3e, streaming_systems) | 17 | 154 |
| Windowing (event-time buckets) | 3 (ddia_kleppmann, fundamentals_de, streaming_systems) | 14 | 155 |
| Serverless & Compute Sizing | 3 (databricks_big_book_4e, fundamentals_de, streaming_systems) | 14 | 146 |
| Late Data & Allowed Lateness | 3 (fundamentals_de, kimball_dwtoolkit_3e, streaming_systems) | 12 | 45 |
| Cost Management & FinOps | 3 (airflow_2e, databricks_big_book_4e, fundamentals_de) | 12 | 76 |
| Persistent State Management | 3 (airflow_2e, ddia_kleppmann, streaming_systems) | 7 | 27 |

## Narrow concepts (demote or fold into a hub)

| Concept | Book sources | Chapters | Hits |
|---|---|---|---|
| Medallion / Layered Architecture | 1 (databricks_big_book_4e) | 13 | 579 |
| Streams & Tables Duality | 1 (streaming_systems) | 9 | 36 |

## Per-concept chapter evidence

### Data Quality & Expectations

- **airflow_2e** (6 files): `ch10_testing.md`(6), `ch01_meet_apache_airflow.md`(4), `ch02_anatomy_of_an_airflow_dag.md`(1), `ch03_time_based_scheduling.md`(1), `ch05_templating_tasks_using_the_airflow_context.md`(1), `ch16_securing_airflow.md`(1)
- **databricks_big_book_4e** (12 files): `ch09_production_grade_data_quality_using_sdp.md`(40), `ch12_ifood_case_study.md`(9), `ch01_introduction_to_data_engineering_on_databricks.md`(6), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(4), `ch13_nfcu_case_study.md`(4), `ch05_lakeflow_connect_sql_server_connector.md`(3), `ch10_collaborative_data_engineering_with_dabs.md`(3), `ch03_observability_in_lakeflow.md`(2), `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(2), `ch11_practical_guide_to_serverless_migrations.md`(2), `ch07_optimizing_materialized_views_recomputes.md`(1), `ch14_cincinnati_reds_case_study.md`(1)
- **ddia_kleppmann** (7 files): `ch09_consistency_and_consensus.md`(8), `ch11_stream_processing.md`(4), `ch01_reliable_scalable_maintainable_applications.md`(2), `ch02_data_models_and_query_languages.md`(2), `ch07_transactions.md`(2), `ch10_batch_processing.md`(2), `ch04_encoding_and_evolution.md`(1)
- **fundamentals_de** (4 files): `ch08_queries_modeling_transformation.md`(3), `ch01_data_engineering_described.md`(2), `ch02_data_engineering_lifecycle.md`(1), `ch04_choosing_technologies.md`(1)
- **kimball_dwtoolkit_3e** (15 files): `ch20_etl_system_design_and_development_process_and_tasks.md`(13), `ch19_etl_subsystems_and_techniques.md`(11), `ch07_accounting.md`(6), `ch08_customer_relationship_management.md`(6), `ch21_big_data_analytics.md`(5), `ch15_electronic_commerce.md`(4), `ch01_dw_bi_dimensional_modeling_primer.md`(3), `ch10_financial_services.md`(3), `ch02_dimensional_modeling_techniques_overview.md`(2), `ch06_order_management.md`(2), `ch16_insurance.md`(2), `ch09_human_resources_management.md`(1)
- **streaming_systems** (5 files): `ch01_streaming_101.md`(2), `ch03_watermarks.md`(2), `ch07_practicalities_of_persistent_state.md`(2), `ch08_streaming_sql.md`(2), `ch09_streaming_joins.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(2)
- **track_sql** (8 files): `master_sql_data_with_baraa.md`(89), `M11-cp1-3-drill-2-quiz.md`(15), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(5), `ansh-lamba-chatgpt-quiz-handoff.md`(4), `ansh-lamba-raw-notes.md`(4), `M10-de-project.md`(1), `M2-ddl-dml-keys.md`(1), `M7-de-scenarios.md`(1)

### Partitioning & Clustering

- **airflow_2e** (7 files): `ch03_time_based_scheduling.md`(22), `ch08_communicating_with_external_systems.md`(9), `ch12_best_practices.md`(4), `ch01_meet_apache_airflow.md`(2), `ch04_asset_aware_scheduling.md`(1), `ch14_project_keeping_family_traditions_alive_with_airflow_and_generative_ai.md`(1), `ch15_operating_airflow_in_production.md`(1)
- **databricks_big_book_4e** (4 files): `ch12_ifood_case_study.md`(11), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(5), `ch09_production_grade_data_quality_using_sdp.md`(3), `ch16_hinge_health_case_study.md`(1)
- **ddia_kleppmann** (8 files): `ch06_partitioning.md`(135), `ch10_batch_processing.md`(30), `ch11_stream_processing.md`(23), `ch07_transactions.md`(18), `ch09_consistency_and_consensus.md`(16), `ch08_trouble_with_distributed_systems.md`(10), `ch05_replication.md`(6), `ch01_reliable_scalable_maintainable_applications.md`(2)
- **fundamentals_de** (6 files): `ch06_storage.md`(23), `ch05_data_generation_source_systems.md`(12), `ch08_queries_modeling_transformation.md`(9), `ch03_designing_good_data_architecture.md`(3), `ch10_security_and_privacy.md`(3), `ch07_ingestion.md`(1)
- **kimball_dwtoolkit_3e** (9 files): `ch20_etl_system_design_and_development_process_and_tasks.md`(17), `ch14_healthcare.md`(8), `ch17_kimball_dwbi_lifecycle_overview.md`(6), `ch03_retail_sales.md`(2), `ch11_telecommunications.md`(2), `ch16_insurance.md`(2), `ch05_procurement.md`(1), `ch19_etl_subsystems_and_techniques.md`(1), `ch21_big_data_analytics.md`(1)
- **streaming_systems** (6 files): `ch05_exactly_once_and_side_effects.md`(9), `ch03_watermarks.md`(4), `ch06_streams_and_tables.md`(3), `ch09_streaming_joins.md`(3), `ch10_evolution_of_large_scale_data_processing.md`(2), `ch02_what_where_when_how.md`(1)
- **track_python** (2 files): `pyspark-evidence-map.md`(18), `master-doc.md`(1)
- **track_shared** (3 files): `lakehouse-map.md`(4), `errors-gotchas.md`(2), `gym-and-troubleshooting-doctrine.md`(1)
- **track_sql** (9 files): `master_sql_data_with_baraa.md`(343), `ansh-lamba-raw-notes.md`(13), `ansh-lamba-chatgpt-quiz-handoff.md`(12), `M11-de-platform.md`(2), `M9-performance.md`(2), `M1-dql-core.md`(1), `M5-window-functions.md`(1), `M11-cp1-3-drill-2-quiz.md`(1), `INDEX.md`(1)

### Checkpointing & Fault Recovery

- **airflow_2e** (2 files): `ch02_anatomy_of_an_airflow_dag.md`(8), `ch01_meet_apache_airflow.md`(2)
- **databricks_big_book_4e** (5 files): `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(9), `ch13_nfcu_case_study.md`(3), `ch05_lakeflow_connect_sql_server_connector.md`(1), `ch07_optimizing_materialized_views_recomputes.md`(1), `ch12_ifood_case_study.md`(1)
- **ddia_kleppmann** (9 files): `ch11_stream_processing.md`(31), `ch07_transactions.md`(26), `ch10_batch_processing.md`(16), `ch08_trouble_with_distributed_systems.md`(13), `ch09_consistency_and_consensus.md`(12), `ch01_reliable_scalable_maintainable_applications.md`(8), `ch05_replication.md`(8), `ch03_storage_and_retrieval.md`(7), `ch02_data_models_and_query_languages.md`(2)
- **fundamentals_de** (5 files): `ch06_storage.md`(6), `ch07_ingestion.md`(3), `ch03_designing_good_data_architecture.md`(2), `ch05_data_generation_source_systems.md`(2), `ch10_security_and_privacy.md`(1)
- **kimball_dwtoolkit_3e** (16 files): `ch16_insurance.md`(33), `ch04_inventory.md`(30), `ch14_healthcare.md`(22), `ch13_education.md`(16), `ch07_accounting.md`(12), `ch06_order_management.md`(11), `ch20_etl_system_design_and_development_process_and_tasks.md`(11), `ch19_etl_subsystems_and_techniques.md`(8), `ch01_dw_bi_dimensional_modeling_primer.md`(6), `ch05_procurement.md`(5), `ch02_dimensional_modeling_techniques_overview.md`(2), `ch08_customer_relationship_management.md`(2)
- **streaming_systems** (8 files): `ch05_exactly_once_and_side_effects.md`(30), `ch10_evolution_of_large_scale_data_processing.md`(14), `ch09_streaming_joins.md`(3), `ch01_streaming_101.md`(2), `ch07_practicalities_of_persistent_state.md`(2), `ch08_streaming_sql.md`(2), `ch04_advanced_windowing.md`(1), `ch06_streams_and_tables.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(8)
- **track_shared** (1 files): `gym-and-troubleshooting-doctrine.md`(6)
- **track_sql** (7 files): `ansh-lamba-raw-notes.md`(35), `ansh-lamba-chatgpt-quiz-handoff.md`(17), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(8), `M11-cp1-3-drill-2-quiz.md`(5), `master_sql_data_with_baraa.md`(5), `README.md`(4), `M1-dql-core.md`(1)

### Transactions & Consistency

- **airflow_2e** (4 files): `ch03_time_based_scheduling.md`(2), `ch16_securing_airflow.md`(2), `ch06_defining_dependencies_between_tasks.md`(1), `ch13_project_finding_the_fastest_way_to_get_around_nyc.md`(1)
- **databricks_big_book_4e** (4 files): `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(3), `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(2), `ch_reverse_etl_lakebase.md`(2), `ch10_collaborative_data_engineering_with_dabs.md`(1)
- **ddia_kleppmann** (9 files): `ch07_transactions.md`(119), `ch09_consistency_and_consensus.md`(112), `ch05_replication.md`(12), `ch03_storage_and_retrieval.md`(11), `ch08_trouble_with_distributed_systems.md`(9), `ch06_partitioning.md`(6), `ch04_encoding_and_evolution.md`(4), `ch11_stream_processing.md`(4), `ch02_data_models_and_query_languages.md`(2)
- **fundamentals_de** (5 files): `ch06_storage.md`(11), `ch05_data_generation_source_systems.md`(7), `ch08_queries_modeling_transformation.md`(6), `appA_serialization_and_compression.md`(5), `ch07_ingestion.md`(2)
- **kimball_dwtoolkit_3e** (20 files): `ch16_insurance.md`(29), `ch04_inventory.md`(17), `ch08_customer_relationship_management.md`(13), `ch03_retail_sales.md`(9), `ch09_human_resources_management.md`(9), `ch14_healthcare.md`(8), `ch20_etl_system_design_and_development_process_and_tasks.md`(8), `ch05_procurement.md`(7), `ch01_dw_bi_dimensional_modeling_primer.md`(6), `ch19_etl_subsystems_and_techniques.md`(6), `ch06_order_management.md`(5), `ch13_education.md`(4)
- **streaming_systems** (4 files): `ch01_streaming_101.md`(3), `ch06_streams_and_tables.md`(3), `ch09_streaming_joins.md`(2), `ch10_evolution_of_large_scale_data_processing.md`(2)
- **track_python** (1 files): `pyspark-evidence-map.md`(6)
- **track_shared** (1 files): `errors-gotchas.md`(2)
- **track_sql** (4 files): `master_sql_data_with_baraa.md`(26), `M11-cp1-3-drill-2-quiz.md`(6), `M1-dql-core.md`(2), `M8-programmable.md`(2)

### Deduplication

- **airflow_2e** (15 files): `ch05_templating_tasks_using_the_airflow_context.md`(7), `ch03_time_based_scheduling.md`(6), `ch13_project_finding_the_fastest_way_to_get_around_nyc.md`(6), `ch09_extending_airflow_with_custom_operators_and_sensors.md`(4), `ch10_testing.md`(2), `ch15_operating_airflow_in_production.md`(2), `appA_running_code_samples.md`(1), `ch04_asset_aware_scheduling.md`(1), `ch06_defining_dependencies_between_tasks.md`(1), `ch07_triggering_workflows_with_external_input.md`(1), `ch08_communicating_with_external_systems.md`(1), `ch11_running_tasks_in_containers.md`(1)
- **databricks_big_book_4e** (5 files): `ch13_nfcu_case_study.md`(13), `ch01_introduction_to_data_engineering_on_databricks.md`(1), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch03_observability_in_lakeflow.md`(1), `ch11_practical_guide_to_serverless_migrations.md`(1)
- **ddia_kleppmann** (7 files): `ch11_stream_processing.md`(5), `ch04_encoding_and_evolution.md`(4), `ch07_transactions.md`(3), `ch02_data_models_and_query_languages.md`(2), `ch03_storage_and_retrieval.md`(2), `ch08_trouble_with_distributed_systems.md`(1), `ch09_consistency_and_consensus.md`(1)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(1)
- **kimball_dwtoolkit_3e** (8 files): `ch07_accounting.md`(3), `ch19_etl_subsystems_and_techniques.md`(3), `ch20_etl_system_design_and_development_process_and_tasks.md`(3), `ch08_customer_relationship_management.md`(2), `ch12_transportation.md`(2), `ch02_dimensional_modeling_techniques_overview.md`(1), `ch10_financial_services.md`(1), `ch13_education.md`(1)
- **streaming_systems** (3 files): `ch05_exactly_once_and_side_effects.md`(29), `ch07_practicalities_of_persistent_state.md`(5), `ch09_streaming_joins.md`(4)
- **track_python** (1 files): `pyspark-evidence-map.md`(24)
- **track_shared** (2 files): `errors-gotchas.md`(3), `lakehouse-map.md`(2)
- **track_sql** (8 files): `master_sql_data_with_baraa.md`(177), `ansh-lamba-raw-notes.md`(22), `ansh-lamba-chatgpt-quiz-handoff.md`(19), `M11-cp1-3-drill-2-quiz.md`(15), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(7), `M1-dql-core.md`(2), `M10-de-project.md`(1), `M7-de-scenarios.md`(1)

### Orchestration & Task Dependencies

- **airflow_2e** (19 files): `ch02_anatomy_of_an_airflow_dag.md`(75), `ch06_defining_dependencies_between_tasks.md`(59), `ch01_meet_apache_airflow.md`(47), `ch10_testing.md`(47), `ch03_time_based_scheduling.md`(41), `ch12_best_practices.md`(38), `ch04_asset_aware_scheduling.md`(33), `ch17_airflow_deployment_options.md`(29), `ch07_triggering_workflows_with_external_input.md`(22), `ch11_running_tasks_in_containers.md`(20), `ch05_templating_tasks_using_the_airflow_context.md`(16), `ch15_operating_airflow_in_production.md`(16)
- **databricks_big_book_4e** (9 files): `ch11_practical_guide_to_serverless_migrations.md`(13), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(10), `ch14_cincinnati_reds_case_study.md`(8), `ch01_introduction_to_data_engineering_on_databricks.md`(7), `ch03_observability_in_lakeflow.md`(5), `ch05_lakeflow_connect_sql_server_connector.md`(2), `ch10_collaborative_data_engineering_with_dabs.md`(1), `ch13_nfcu_case_study.md`(1), `ch15_porsche_holding_case_study.md`(1)
- **ddia_kleppmann** (5 files): `ch11_stream_processing.md`(3), `ch05_replication.md`(2), `ch09_consistency_and_consensus.md`(2), `ch06_partitioning.md`(1), `ch10_batch_processing.md`(1)
- **fundamentals_de** (9 files): `ch02_data_engineering_lifecycle.md`(11), `ch11_future_of_data_engineering.md`(7), `ch04_choosing_technologies.md`(6), `ch07_ingestion.md`(3), `ch08_queries_modeling_transformation.md`(3), `ch05_data_generation_source_systems.md`(2), `ch09_serving_data.md`(2), `ch01_data_engineering_described.md`(1), `ch06_storage.md`(1)
- **kimball_dwtoolkit_3e** (4 files): `ch19_etl_subsystems_and_techniques.md`(3), `ch02_dimensional_modeling_techniques_overview.md`(1), `ch07_accounting.md`(1), `ch08_customer_relationship_management.md`(1)
- **streaming_systems** (2 files): `ch07_practicalities_of_persistent_state.md`(2), `ch01_streaming_101.md`(1)
- **track_shared** (1 files): `lakehouse-map.md`(1)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(3)

### Surrogate, Natural & Business Keys

- **airflow_2e** (1 files): `ch05_templating_tasks_using_the_airflow_context.md`(1)
- **databricks_big_book_4e** (2 files): `ch05_lakeflow_connect_sql_server_connector.md`(4), `ch_reverse_etl_lakebase.md`(2)
- **ddia_kleppmann** (4 files): `ch03_storage_and_retrieval.md`(5), `ch06_partitioning.md`(5), `ch02_data_models_and_query_languages.md`(1), `ch05_replication.md`(1)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(8)
- **kimball_dwtoolkit_3e** (20 files): `ch19_etl_subsystems_and_techniques.md`(32), `ch02_dimensional_modeling_techniques_overview.md`(25), `ch03_retail_sales.md`(19), `ch05_procurement.md`(16), `ch20_etl_system_design_and_development_process_and_tasks.md`(14), `ch21_big_data_analytics.md`(12), `ch11_telecommunications.md`(10), `ch13_education.md`(9), `ch14_healthcare.md`(9), `ch01_dw_bi_dimensional_modeling_primer.md`(8), `ch07_accounting.md`(8), `ch06_order_management.md`(7)
- **streaming_systems** (1 files): `ch06_streams_and_tables.md`(3)
- **track_python** (1 files): `pyspark-evidence-map.md`(3)
- **track_shared** (1 files): `lakehouse-map.md`(5)
- **track_sql** (7 files): `master_sql_data_with_baraa.md`(159), `M11-cp1-3-drill-2-quiz.md`(24), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(8), `ansh-lamba-chatgpt-quiz-handoff.md`(7), `ansh-lamba-raw-notes.md`(7), `M2-ddl-dml-keys.md`(3), `M1-dql-core.md`(1)

### Lineage & Governance

- **airflow_2e** (1 files): `ch01_meet_apache_airflow.md`(4)
- **databricks_big_book_4e** (12 files): `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(15), `ch01_introduction_to_data_engineering_on_databricks.md`(12), `ch11_practical_guide_to_serverless_migrations.md`(12), `ch03_observability_in_lakeflow.md`(11), `ch05_lakeflow_connect_sql_server_connector.md`(6), `ch12_ifood_case_study.md`(6), `ch15_porsche_holding_case_study.md`(6), `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(2), `ch07_optimizing_materialized_views_recomputes.md`(2), `ch04_cost_maturity_journey_with_databricks.md`(1), `ch14_cincinnati_reds_case_study.md`(1), `ch_reverse_etl_lakebase.md`(1)
- **ddia_kleppmann** (3 files): `ch10_batch_processing.md`(5), `ch03_storage_and_retrieval.md`(1), `ch05_replication.md`(1)
- **fundamentals_de** (7 files): `ch02_data_engineering_lifecycle.md`(6), `ch09_serving_data.md`(5), `ch03_designing_good_data_architecture.md`(4), `ch11_future_of_data_engineering.md`(4), `ch08_queries_modeling_transformation.md`(2), `ch01_data_engineering_described.md`(1), `ch05_data_generation_source_systems.md`(1)
- **kimball_dwtoolkit_3e** (9 files): `ch21_big_data_analytics.md`(11), `ch04_inventory.md`(6), `ch19_etl_subsystems_and_techniques.md`(4), `ch01_dw_bi_dimensional_modeling_primer.md`(3), `ch05_procurement.md`(3), `ch17_kimball_dwbi_lifecycle_overview.md`(2), `ch03_retail_sales.md`(1), `ch07_accounting.md`(1), `ch18_dimensional_modeling_process_and_tasks.md`(1)
- **streaming_systems** (2 files): `ch05_exactly_once_and_side_effects.md`(1), `ch10_evolution_of_large_scale_data_processing.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(6)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(15)

### Backfill & Reprocessing

- **airflow_2e** (9 files): `ch03_time_based_scheduling.md`(37), `ch01_meet_apache_airflow.md`(15), `ch13_project_finding_the_fastest_way_to_get_around_nyc.md`(4), `ch02_anatomy_of_an_airflow_dag.md`(3), `ch06_defining_dependencies_between_tasks.md`(3), `ch14_project_keeping_family_traditions_alive_with_airflow_and_generative_ai.md`(3), `ch12_best_practices.md`(2), `ch04_asset_aware_scheduling.md`(1), `ch08_communicating_with_external_systems.md`(1)
- **databricks_big_book_4e** (2 files): `ch07_optimizing_materialized_views_recomputes.md`(2), `ch09_production_grade_data_quality_using_sdp.md`(2)
- **ddia_kleppmann** (4 files): `ch11_stream_processing.md`(17), `ch10_batch_processing.md`(2), `ch03_storage_and_retrieval.md`(1), `ch05_replication.md`(1)
- **fundamentals_de** (3 files): `ch06_storage.md`(5), `ch05_data_generation_source_systems.md`(2), `ch07_ingestion.md`(1)
- **kimball_dwtoolkit_3e** (5 files): `ch04_inventory.md`(3), `ch11_telecommunications.md`(3), `ch05_procurement.md`(2), `ch01_dw_bi_dimensional_modeling_primer.md`(1), `ch19_etl_subsystems_and_techniques.md`(1)
- **streaming_systems** (6 files): `ch10_evolution_of_large_scale_data_processing.md`(7), `ch05_exactly_once_and_side_effects.md`(4), `ch07_practicalities_of_persistent_state.md`(3), `ch01_streaming_101.md`(1), `ch04_advanced_windowing.md`(1), `ch09_streaming_joins.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(2)
- **track_shared** (1 files): `gym-and-troubleshooting-doctrine.md`(1)
- **track_sql** (1 files): `M11-cp1-3-drill-2-quiz.md`(2)

### Testing & Pipeline Validation

- **airflow_2e** (1 files): `ch10_testing.md`(31)
- **databricks_big_book_4e** (2 files): `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(3), `ch10_collaborative_data_engineering_with_dabs.md`(3)
- **ddia_kleppmann** (4 files): `ch04_encoding_and_evolution.md`(1), `ch05_replication.md`(1), `ch10_batch_processing.md`(1), `ch11_stream_processing.md`(1)
- **fundamentals_de** (1 files): `ch03_designing_good_data_architecture.md`(1)
- **kimball_dwtoolkit_3e** (4 files): `ch20_etl_system_design_and_development_process_and_tasks.md`(5), `ch15_electronic_commerce.md`(3), `ch04_inventory.md`(1), `ch13_education.md`(1)
- **streaming_systems** (2 files): `ch02_what_where_when_how.md`(1), `ch07_practicalities_of_persistent_state.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(2)
- **track_shared** (1 files): `gym-and-troubleshooting-doctrine.md`(1)

### File Layout & Compaction

- **databricks_big_book_4e** (5 files): `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(28), `ch13_nfcu_case_study.md`(17), `ch04_cost_maturity_journey_with_databricks.md`(10), `ch12_ifood_case_study.md`(1), `ch15_porsche_holding_case_study.md`(1)
- **ddia_kleppmann** (8 files): `ch11_stream_processing.md`(31), `ch03_storage_and_retrieval.md`(23), `ch02_data_models_and_query_languages.md`(8), `ch04_encoding_and_evolution.md`(7), `ch05_replication.md`(4), `ch10_batch_processing.md`(2), `ch06_partitioning.md`(1), `ch08_trouble_with_distributed_systems.md`(1)
- **fundamentals_de** (3 files): `ch08_queries_modeling_transformation.md`(11), `ch01_data_engineering_described.md`(1), `ch04_choosing_technologies.md`(1)
- **kimball_dwtoolkit_3e** (7 files): `ch01_dw_bi_dimensional_modeling_primer.md`(6), `ch21_big_data_analytics.md`(3), `ch02_dimensional_modeling_techniques_overview.md`(1), `ch03_retail_sales.md`(1), `ch14_healthcare.md`(1), `ch17_kimball_dwbi_lifecycle_overview.md`(1), `ch19_etl_subsystems_and_techniques.md`(1)
- **streaming_systems** (2 files): `ch05_exactly_once_and_side_effects.md`(1), `ch10_evolution_of_large_scale_data_processing.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(18)
- **track_sql** (2 files): `master_sql_data_with_baraa.md`(69), `M11-cp1-3-drill-2-quiz.md`(1)

### Idempotency & Exactly-Once

- **airflow_2e** (7 files): `ch03_time_based_scheduling.md`(14), `ch13_project_finding_the_fastest_way_to_get_around_nyc.md`(9), `ch12_best_practices.md`(6), `ch08_communicating_with_external_systems.md`(5), `ch14_project_keeping_family_traditions_alive_with_airflow_and_generative_ai.md`(4), `ch05_templating_tasks_using_the_airflow_context.md`(1), `ch06_defining_dependencies_between_tasks.md`(1)
- **databricks_big_book_4e** (2 files): `ch01_introduction_to_data_engineering_on_databricks.md`(1), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1)
- **ddia_kleppmann** (6 files): `ch11_stream_processing.md`(29), `ch04_encoding_and_evolution.md`(2), `ch09_consistency_and_consensus.md`(2), `ch10_batch_processing.md`(2), `ch03_storage_and_retrieval.md`(1), `ch05_replication.md`(1)
- **fundamentals_de** (1 files): `ch05_data_generation_source_systems.md`(9)
- **streaming_systems** (8 files): `ch05_exactly_once_and_side_effects.md`(28), `ch10_evolution_of_large_scale_data_processing.md`(17), `ch01_streaming_101.md`(5), `ch08_streaming_sql.md`(5), `ch03_watermarks.md`(1), `ch04_advanced_windowing.md`(1), `ch07_practicalities_of_persistent_state.md`(1), `ch09_streaming_joins.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(7)
- **track_shared** (1 files): `gym-and-troubleshooting-doctrine.md`(2)
- **track_sql** (1 files): `M11-cp1-3-drill-2-quiz.md`(3)

### Security & Access Control

- **airflow_2e** (12 files): `ch16_securing_airflow.md`(84), `ch17_airflow_deployment_options.md`(16), `ch12_best_practices.md`(14), `ch08_communicating_with_external_systems.md`(9), `ch11_running_tasks_in_containers.md`(2), `ch13_project_finding_the_fastest_way_to_get_around_nyc.md`(2), `ch01_meet_apache_airflow.md`(1), `ch03_time_based_scheduling.md`(1), `ch05_templating_tasks_using_the_airflow_context.md`(1), `ch09_extending_airflow_with_custom_operators_and_sensors.md`(1), `ch14_project_keeping_family_traditions_alive_with_airflow_and_generative_ai.md`(1), `ch15_operating_airflow_in_production.md`(1)
- **databricks_big_book_4e** (4 files): `ch05_lakeflow_connect_sql_server_connector.md`(6), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(2), `ch09_production_grade_data_quality_using_sdp.md`(1), `ch12_ifood_case_study.md`(1)
- **ddia_kleppmann** (1 files): `ch04_encoding_and_evolution.md`(2)
- **fundamentals_de** (2 files): `ch10_security_and_privacy.md`(13), `ch09_serving_data.md`(6)
- **kimball_dwtoolkit_3e** (4 files): `ch21_big_data_analytics.md`(7), `ch19_etl_subsystems_and_techniques.md`(5), `ch13_education.md`(1), `ch16_insurance.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(8)
- **track_shared** (1 files): `gym-and-troubleshooting-doctrine.md`(2)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(5)

### Replication & Distributed Coordination

- **airflow_2e** (1 files): `ch15_operating_airflow_in_production.md`(1)
- **databricks_big_book_4e** (4 files): `ch03_observability_in_lakeflow.md`(2), `ch_reverse_etl_lakebase.md`(2), `ch05_lakeflow_connect_sql_server_connector.md`(1), `ch16_hinge_health_case_study.md`(1)
- **ddia_kleppmann** (9 files): `ch05_replication.md`(174), `ch09_consistency_and_consensus.md`(137), `ch11_stream_processing.md`(33), `ch08_trouble_with_distributed_systems.md`(26), `ch06_partitioning.md`(12), `ch07_transactions.md`(12), `ch10_batch_processing.md`(10), `ch01_reliable_scalable_maintainable_applications.md`(3), `ch03_storage_and_retrieval.md`(2)
- **fundamentals_de** (5 files): `ch06_storage.md`(11), `ch03_designing_good_data_architecture.md`(3), `ch05_data_generation_source_systems.md`(1), `ch07_ingestion.md`(1), `ch08_queries_modeling_transformation.md`(1)
- **kimball_dwtoolkit_3e** (4 files): `ch18_dimensional_modeling_process_and_tasks.md`(3), `ch17_kimball_dwbi_lifecycle_overview.md`(2), `ch05_procurement.md`(1), `ch06_order_management.md`(1)
- **track_sql** (1 files): `M1-dql-core.md`(1)

### Ingestion Patterns & Connectors

- **airflow_2e** (1 files): `ch07_triggering_workflows_with_external_input.md`(9)
- **databricks_big_book_4e** (10 files): `ch05_lakeflow_connect_sql_server_connector.md`(16), `ch15_porsche_holding_case_study.md`(16), `ch16_hinge_health_case_study.md`(11), `ch01_introduction_to_data_engineering_on_databricks.md`(6), `ch13_nfcu_case_study.md`(6), `ch12_ifood_case_study.md`(3), `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(2), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch10_collaborative_data_engineering_with_dabs.md`(1), `ch_reverse_etl_lakebase.md`(1)
- **ddia_kleppmann** (4 files): `ch11_stream_processing.md`(11), `ch01_reliable_scalable_maintainable_applications.md`(1), `ch04_encoding_and_evolution.md`(1), `ch06_partitioning.md`(1)
- **fundamentals_de** (4 files): `ch07_ingestion.md`(16), `ch06_storage.md`(2), `ch08_queries_modeling_transformation.md`(1), `ch11_future_of_data_engineering.md`(1)
- **streaming_systems** (3 files): `ch10_evolution_of_large_scale_data_processing.md`(10), `ch05_exactly_once_and_side_effects.md`(1), `ch06_streams_and_tables.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(4)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(1)

### Change Data Capture & Change Tracking

- **databricks_big_book_4e** (8 files): `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(33), `ch05_lakeflow_connect_sql_server_connector.md`(26), `ch16_hinge_health_case_study.md`(14), `ch13_nfcu_case_study.md`(6), `ch01_introduction_to_data_engineering_on_databricks.md`(2), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch07_optimizing_materialized_views_recomputes.md`(1), `ch_reverse_etl_lakebase.md`(1)
- **ddia_kleppmann** (3 files): `ch11_stream_processing.md`(24), `ch05_replication.md`(2), `ch03_storage_and_retrieval.md`(1)
- **fundamentals_de** (4 files): `ch07_ingestion.md`(18), `ch05_data_generation_source_systems.md`(8), `ch08_queries_modeling_transformation.md`(3), `appA_serialization_and_compression.md`(1)
- **kimball_dwtoolkit_3e** (4 files): `ch19_etl_subsystems_and_techniques.md`(2), `ch09_human_resources_management.md`(1), `ch10_financial_services.md`(1), `ch16_insurance.md`(1)
- **streaming_systems** (1 files): `ch06_streams_and_tables.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(6)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(2)

### Batch vs Streaming

- **databricks_big_book_4e** (2 files): `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(2), `ch15_porsche_holding_case_study.md`(2)
- **ddia_kleppmann** (1 files): `ch11_stream_processing.md`(7)
- **fundamentals_de** (3 files): `ch07_ingestion.md`(9), `ch08_queries_modeling_transformation.md`(1), `ch09_serving_data.md`(1)
- **kimball_dwtoolkit_3e** (2 files): `ch19_etl_subsystems_and_techniques.md`(2), `ch20_etl_system_design_and_development_process_and_tasks.md`(1)
- **streaming_systems** (9 files): `ch01_streaming_101.md`(12), `ch07_practicalities_of_persistent_state.md`(4), `ch09_streaming_joins.md`(4), `ch02_what_where_when_how.md`(3), `ch05_exactly_once_and_side_effects.md`(3), `ch03_watermarks.md`(2), `ch06_streams_and_tables.md`(2), `ch10_evolution_of_large_scale_data_processing.md`(2), `ch04_advanced_windowing.md`(1)

### Event Time vs Processing Time

- **airflow_2e** (1 files): `ch01_meet_apache_airflow.md`(1)
- **databricks_big_book_4e** (2 files): `ch14_cincinnati_reds_case_study.md`(2), `ch11_practical_guide_to_serverless_migrations.md`(1)
- **ddia_kleppmann** (1 files): `ch11_stream_processing.md`(18)
- **fundamentals_de** (2 files): `ch05_data_generation_source_systems.md`(1), `ch07_ingestion.md`(1)
- **streaming_systems** (9 files): `ch04_advanced_windowing.md`(46), `ch03_watermarks.md`(45), `ch01_streaming_101.md`(42), `ch02_what_where_when_how.md`(15), `ch10_evolution_of_large_scale_data_processing.md`(13), `ch07_practicalities_of_persistent_state.md`(9), `ch05_exactly_once_and_side_effects.md`(5), `ch06_streams_and_tables.md`(2), `ch09_streaming_joins.md`(2)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(1)

### Schema Evolution & Compatibility

- **airflow_2e** (2 files): `ch13_project_finding_the_fastest_way_to_get_around_nyc.md`(1), `ch14_project_keeping_family_traditions_alive_with_airflow_and_generative_ai.md`(1)
- **databricks_big_book_4e** (4 files): `ch16_hinge_health_case_study.md`(2), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch05_lakeflow_connect_sql_server_connector.md`(1), `ch09_production_grade_data_quality_using_sdp.md`(1)
- **ddia_kleppmann** (4 files): `ch04_encoding_and_evolution.md`(27), `ch02_data_models_and_query_languages.md`(7), `ch05_replication.md`(1), `ch11_stream_processing.md`(1)
- **fundamentals_de** (3 files): `ch08_queries_modeling_transformation.md`(3), `ch07_ingestion.md`(2), `ch05_data_generation_source_systems.md`(1)
- **kimball_dwtoolkit_3e** (1 files): `ch02_dimensional_modeling_techniques_overview.md`(1)
- **track_sql** (2 files): `M1-dql-core.md`(1), `master_sql_data_with_baraa.md`(1)

### Aggregation & Combiners

- **ddia_kleppmann** (2 files): `ch02_data_models_and_query_languages.md`(1), `ch10_batch_processing.md`(1)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(1)
- **kimball_dwtoolkit_3e** (15 files): `ch07_accounting.md`(5), `ch13_education.md`(5), `ch15_electronic_commerce.md`(5), `ch09_human_resources_management.md`(4), `ch16_insurance.md`(4), `ch04_inventory.md`(3), `ch11_telecommunications.md`(3), `ch05_procurement.md`(2), `ch01_dw_bi_dimensional_modeling_primer.md`(1), `ch03_retail_sales.md`(1), `ch06_order_management.md`(1), `ch10_financial_services.md`(1)
- **streaming_systems** (5 files): `ch07_practicalities_of_persistent_state.md`(14), `ch05_exactly_once_and_side_effects.md`(4), `ch10_evolution_of_large_scale_data_processing.md`(4), `ch08_streaming_sql.md`(3), `ch06_streams_and_tables.md`(1)
- **track_shared** (1 files): `errors-gotchas.md`(8)
- **track_sql** (8 files): `master_sql_data_with_baraa.md`(127), `M1-dql-core.md`(29), `M11-cp1-3-drill-2-quiz.md`(7), `drill-M1-business-decode.md`(7), `ansh-lamba-raw-notes.md`(6), `ansh-lamba-chatgpt-quiz-handoff.md`(5), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(3), `INDEX.md`(1)

### Incremental vs Full Recompute

- **airflow_2e** (3 files): `ch03_time_based_scheduling.md`(5), `ch12_best_practices.md`(3), `ch01_meet_apache_airflow.md`(1)
- **databricks_big_book_4e** (5 files): `ch07_optimizing_materialized_views_recomputes.md`(39), `ch09_production_grade_data_quality_using_sdp.md`(4), `ch05_lakeflow_connect_sql_server_connector.md`(3), `ch01_introduction_to_data_engineering_on_databricks.md`(2), `ch16_hinge_health_case_study.md`(1)
- **kimball_dwtoolkit_3e** (1 files): `ch20_etl_system_design_and_development_process_and_tasks.md`(6)
- **streaming_systems** (2 files): `ch07_practicalities_of_persistent_state.md`(3), `ch04_advanced_windowing.md`(2)
- **track_python** (1 files): `master-doc.md`(1)
- **track_shared** (1 files): `lakehouse-map.md`(1)
- **track_sql** (5 files): `master_sql_data_with_baraa.md`(7), `M1-dql-core.md`(1), `M10-de-project.md`(1), `M7-de-scenarios.md`(1), `M11-cp1-3-drill-2-quiz.md`(1)

### SQL Window Functions

- **airflow_2e** (1 files): `ch12_best_practices.md`(1)
- **databricks_big_book_4e** (1 files): `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1)
- **ddia_kleppmann** (2 files): `ch05_replication.md`(1), `ch11_stream_processing.md`(1)
- **fundamentals_de** (1 files): `ch06_storage.md`(1)
- **track_python** (2 files): `pyspark-evidence-map.md`(10), `master-doc.md`(1)
- **track_shared** (2 files): `errors-gotchas.md`(7), `lakehouse-map.md`(5)
- **track_sql** (6 files): `ansh-lamba-chatgpt-quiz-handoff.md`(76), `master_sql_data_with_baraa.md`(65), `ansh-lamba-raw-notes.md`(64), `M11-cp1-3-drill-2-quiz.md`(4), `M5-window-functions.md`(3), `M1-dql-core.md`(2)

### Materialized Views

- **databricks_big_book_4e** (8 files): `ch09_production_grade_data_quality_using_sdp.md`(9), `ch07_optimizing_materialized_views_recomputes.md`(6), `ch16_hinge_health_case_study.md`(6), `ch01_introduction_to_data_engineering_on_databricks.md`(2), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(1), `ch12_ifood_case_study.md`(1), `ch13_nfcu_case_study.md`(1)
- **ddia_kleppmann** (2 files): `ch03_storage_and_retrieval.md`(5), `ch11_stream_processing.md`(3)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(4)
- **streaming_systems** (3 files): `ch06_streams_and_tables.md`(3), `ch08_streaming_sql.md`(2), `ch10_evolution_of_large_scale_data_processing.md`(1)

### Slowly Changing Dimensions

- **databricks_big_book_4e** (7 files): `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(22), `ch05_lakeflow_connect_sql_server_connector.md`(3), `ch01_introduction_to_data_engineering_on_databricks.md`(2), `ch13_nfcu_case_study.md`(2), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch07_optimizing_materialized_views_recomputes.md`(1), `ch16_hinge_health_case_study.md`(1)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(3)
- **kimball_dwtoolkit_3e** (17 files): `ch05_procurement.md`(19), `ch02_dimensional_modeling_techniques_overview.md`(12), `ch19_etl_subsystems_and_techniques.md`(12), `ch07_accounting.md`(7), `ch09_human_resources_management.md`(7), `ch20_etl_system_design_and_development_process_and_tasks.md`(7), `ch01_dw_bi_dimensional_modeling_primer.md`(6), `ch16_insurance.md`(5), `ch08_customer_relationship_management.md`(4), `ch18_dimensional_modeling_process_and_tasks.md`(4), `ch03_retail_sales.md`(3), `ch06_order_management.md`(2)
- **track_python** (1 files): `pyspark-evidence-map.md`(7)
- **track_shared** (1 files): `lakehouse-map.md`(1)
- **track_sql** (3 files): `M10-de-project.md`(1), `M7-de-scenarios.md`(1), `master_sql_data_with_baraa.md`(1)

### Dimensional Modeling & Grain

- **ddia_kleppmann** (1 files): `ch03_storage_and_retrieval.md`(20)
- **fundamentals_de** (4 files): `ch08_queries_modeling_transformation.md`(10), `ch11_future_of_data_engineering.md`(2), `appB_cloud_networking.md`(1), `ch01_data_engineering_described.md`(1)
- **kimball_dwtoolkit_3e** (21 files): `ch03_retail_sales.md`(72), `ch01_dw_bi_dimensional_modeling_primer.md`(61), `ch15_electronic_commerce.md`(58), `ch06_order_management.md`(48), `ch02_dimensional_modeling_techniques_overview.md`(45), `ch13_education.md`(45), `ch16_insurance.md`(45), `ch18_dimensional_modeling_process_and_tasks.md`(43), `ch04_inventory.md`(40), `ch07_accounting.md`(39), `ch11_telecommunications.md`(39), `ch12_transportation.md`(38)
- **track_python** (1 files): `pyspark-evidence-map.md`(2)
- **track_sql** (2 files): `master_sql_data_with_baraa.md`(56), `M11-cp1-3-drill-2-quiz.md`(1)

### Watermarks

- **ddia_kleppmann** (1 files): `ch11_stream_processing.md`(2)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(1)
- **streaming_systems** (10 files): `ch03_watermarks.md`(96), `ch02_what_where_when_how.md`(32), `ch10_evolution_of_large_scale_data_processing.md`(20), `ch08_streaming_sql.md`(10), `ch09_streaming_joins.md`(10), `ch06_streams_and_tables.md`(9), `ch04_advanced_windowing.md`(6), `ch05_exactly_once_and_side_effects.md`(4), `ch07_practicalities_of_persistent_state.md`(4), `ch01_streaming_101.md`(2)
- **track_python** (1 files): `pyspark-evidence-map.md`(8)
- **track_shared** (1 files): `lakehouse-map.md`(1)
- **track_sql** (3 files): `M1-dql-core.md`(1), `M10-de-project.md`(1), `M7-de-scenarios.md`(1)

### Joins

- **databricks_big_book_4e** (1 files): `ch07_optimizing_materialized_views_recomputes.md`(2)
- **kimball_dwtoolkit_3e** (4 files): `ch08_customer_relationship_management.md`(9), `ch02_dimensional_modeling_techniques_overview.md`(4), `ch03_retail_sales.md`(1), `ch10_financial_services.md`(1)
- **streaming_systems** (4 files): `ch09_streaming_joins.md`(28), `ch01_streaming_101.md`(5), `ch02_what_where_when_how.md`(1), `ch08_streaming_sql.md`(1)
- **track_shared** (2 files): `dialect-map.md`(1), `errors-gotchas.md`(1)
- **track_sql** (6 files): `master_sql_data_with_baraa.md`(82), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(5), `ansh-lamba-chatgpt-quiz-handoff.md`(4), `ansh-lamba-raw-notes.md`(4), `M3-joins-set-ops.md`(3), `M11-cp1-3-drill-2-quiz.md`(2)

### Windowing (event-time buckets)

- **ddia_kleppmann** (1 files): `ch11_stream_processing.md`(12)
- **fundamentals_de** (1 files): `ch08_queries_modeling_transformation.md`(3)
- **streaming_systems** (10 files): `ch04_advanced_windowing.md`(57), `ch09_streaming_joins.md`(27), `ch01_streaming_101.md`(22), `ch02_what_where_when_how.md`(7), `ch08_streaming_sql.md`(5), `ch06_streams_and_tables.md`(4), `ch07_practicalities_of_persistent_state.md`(3), `ch10_evolution_of_large_scale_data_processing.md`(3), `ch03_watermarks.md`(2), `ch05_exactly_once_and_side_effects.md`(2)
- **track_python** (1 files): `pyspark-evidence-map.md`(1)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(7)

### Serverless & Compute Sizing

- **databricks_big_book_4e** (11 files): `ch11_practical_guide_to_serverless_migrations.md`(67), `ch04_cost_maturity_journey_with_databricks.md`(21), `ch14_cincinnati_reds_case_study.md`(21), `ch05_lakeflow_connect_sql_server_connector.md`(9), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(6), `ch13_nfcu_case_study.md`(6), `ch12_ifood_case_study.md`(3), `ch01_introduction_to_data_engineering_on_databricks.md`(2), `ch07_optimizing_materialized_views_recomputes.md`(1), `ch10_collaborative_data_engineering_with_dabs.md`(1), `ch15_porsche_holding_case_study.md`(1)
- **fundamentals_de** (2 files): `ch04_choosing_technologies.md`(6), `ch05_data_generation_source_systems.md`(1)
- **streaming_systems** (1 files): `ch10_evolution_of_large_scale_data_processing.md`(1)

### Late Data & Allowed Lateness

- **fundamentals_de** (2 files): `ch02_data_engineering_lifecycle.md`(2), `ch07_ingestion.md`(2)
- **kimball_dwtoolkit_3e** (4 files): `ch14_healthcare.md`(7), `ch19_etl_subsystems_and_techniques.md`(7), `ch02_dimensional_modeling_techniques_overview.md`(3), `ch20_etl_system_design_and_development_process_and_tasks.md`(1)
- **streaming_systems** (6 files): `ch02_what_where_when_how.md`(9), `ch03_watermarks.md`(5), `ch08_streaming_sql.md`(4), `ch01_streaming_101.md`(2), `ch10_evolution_of_large_scale_data_processing.md`(2), `ch09_streaming_joins.md`(1)

### Cost Management & FinOps

- **airflow_2e** (1 files): `ch17_airflow_deployment_options.md`(1)
- **databricks_big_book_4e** (7 files): `ch04_cost_maturity_journey_with_databricks.md`(33), `ch11_practical_guide_to_serverless_migrations.md`(15), `ch05_lakeflow_connect_sql_server_connector.md`(5), `ch16_hinge_health_case_study.md`(3), `ch14_cincinnati_reds_case_study.md`(2), `ch02_migrating_apache_spark_etl_workloads_to_databricks.md`(1), `ch12_ifood_case_study.md`(1)
- **fundamentals_de** (3 files): `ch04_choosing_technologies.md`(6), `ch03_designing_good_data_architecture.md`(5), `appB_cloud_networking.md`(1)
- **track_sql** (1 files): `master_sql_data_with_baraa.md`(3)

### Persistent State Management

- **airflow_2e** (1 files): `ch17_airflow_deployment_options.md`(1)
- **ddia_kleppmann** (1 files): `ch01_reliable_scalable_maintainable_applications.md`(2)
- **streaming_systems** (4 files): `ch07_practicalities_of_persistent_state.md`(11), `ch10_evolution_of_large_scale_data_processing.md`(7), `ch01_streaming_101.md`(3), `ch02_what_where_when_how.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(2)

### Medallion / Layered Architecture

- **databricks_big_book_4e** (5 files): `ch06_implement_cdc_and_scd_type_2_with_lakeflow.md`(26), `ch12_ifood_case_study.md`(26), `ch16_hinge_health_case_study.md`(3), `ch_reverse_etl_lakebase.md`(2), `ch09_production_grade_data_quality_using_sdp.md`(1)
- **track_python** (1 files): `pyspark-evidence-map.md`(158)
- **track_shared** (1 files): `lakehouse-map.md`(14)
- **track_sql** (6 files): `master_sql_data_with_baraa.md`(328), `M10-de-project.md`(10), `M1-dql-core.md`(5), `M11-cp1-3-drill-2-quiz.md`(3), `M7-de-scenarios.md`(2), `M11-cp1-3-ddl-dql-joins-dml-quiz.md`(1)

### Streams & Tables Duality

- **streaming_systems** (9 files): `ch08_streaming_sql.md`(17), `ch06_streams_and_tables.md`(9), `ch09_streaming_joins.md`(4), `ch01_streaming_101.md`(1), `ch02_what_where_when_how.md`(1), `ch03_watermarks.md`(1), `ch04_advanced_windowing.md`(1), `ch05_exactly_once_and_side_effects.md`(1), `ch07_practicalities_of_persistent_state.md`(1)

