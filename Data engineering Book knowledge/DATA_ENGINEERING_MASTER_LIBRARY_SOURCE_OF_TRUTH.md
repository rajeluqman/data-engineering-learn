# DATA ENGINEERING MASTER LIBRARY - SOURCE OF TRUTH

> **Purpose:** Canonical catalog for the attached data engineering books and the complementary free references supplied by the user.
>
> **Scope:** This file inventories every attached PDF, records its verified metadata and chapter-level contents, and preserves the supplied free-reference mapping. It is an index and routing document; the attached PDFs and linked references remain the authoritative sources for detailed content.
>
> **Last verified:** 2026-09-19

---

## 1. Completeness Ledger

| Source group | Expected | Recorded | Status |
|---|---:|---:|---|
| Attached PDF books | 7 | 7 | COMPLETE |
| Supplied free-reference rows | 10 | 10 | COMPLETE |
| Attached PDF pages | 2,868 | 2,868 | COMPLETE |

---

## 2. Attached PDF Inventory

| # | Exact attached filename | Canonical title | Author(s) / publisher | Pages | Library ID |
|---:|---|---|---|---:|---|
| 1 | `Data Pipelines with Apache Airflow, 2nd Edition.pdf` | *Data Pipelines with Apache Airflow, Second Edition* | Julian de Ruiter, Ismael Cabral, Kris Geusebroek, Daniel van der Ende, Bas Harenslak | 514 | `libfile_f27683b600d081919bd8df1379677f44` |
| 2 | `Database Internals alex petrov.pdf` | *Database Internals* | Alex Petrov | 238 | `libfile_2c171617cf708191908a3946b5536283` |
| 3 | `Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf` | *Fundamentals of Data Engineering* | Joe Reis and Matt Housley | 445 | `libfile_dc9b5ae647188191a40b8787455fcab2` |
| 4 | `Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf` | *Designing Data-Intensive Applications* | Martin Kleppmann; O'Reilly Media (2017) | 491 | `libfile_006bd4bf1cbc819197d5592452d2b033` |
| 5 | `Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf` | *The Data Warehouse Toolkit, 3rd Edition* | Ralph Kimball and Margy Ross; Wiley | 601 | `libfile_cfce93aeb79c8191ad005d41e78fa7fd` |
| 6 | `streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf` | *Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing* | Tyler Akidau, Slava Chernyak, and Reuven Lax | 456 | `libfile_b42b300da0b48191b31524fcd480bbd5` |
| 7 | `Big-Book-of-Data-Engineering-4th-Edition.pdf` | *Big Book of Data Engineering, 4th Edition* | Databricks | 123 | `libfile_feff66bac1148191b4d63edb1e2ac8f2` |

---

## 3. Verified Chapter-Level Index of Attached PDFs

### 3.1 Data Pipelines with Apache Airflow, Second Edition

#### Part 1 - Getting started

1. Meet Apache Airflow
2. Anatomy of an Airflow DAG
3. Time-based scheduling
4. Asset-aware scheduling
5. Templating tasks using the Airflow context
6. Defining dependencies between tasks

#### Part 2 - Beyond the basics

7. Triggering workflows with external input
8. Communicating with external systems
9. Extending Airflow with custom operators and sensors
10. Testing
11. Running tasks in containers

#### Part 3 - Airflow in practice

12. Best practices
13. Project: Finding the fastest way to get around NYC
14. Project: Keeping family traditions alive with Airflow and generative AI

#### Part 4 - Airflow in production

15. Operating Airflow in production
16. Securing Airflow
17. Airflow deployment options

#### Appendices

- Appendix A: Running code samples
- Appendix B: Prometheus metric mapping

### 3.2 Database Internals

#### Part I - Storage Engines

1. Introduction and Overview
2. B-Tree Basics
3. File Formats
4. Implementing B-Trees
5. Transaction Processing and Recovery
6. B-Tree Variants
7. Log-Structured Storage
- Part I Conclusion

#### Part II - Distributed Systems

8. Introduction and Overview
9. Failure Detection
10. Leader Election
11. Replication and Consistency
12. Anti-Entropy and Dissemination
13. Distributed Transactions
14. Consensus
- Part II Conclusion
- Bibliography

### 3.3 Fundamentals of Data Engineering

#### Part I - Foundation and Building Blocks

1. Data Engineering Described
2. The Data Engineering Lifecycle
3. Designing Good Data Architecture
4. Choosing Technologies Across the Data Engineering Lifecycle

#### Part II - The Data Engineering Lifecycle in Depth

5. Data Generation in Source Systems
6. Storage
7. Ingestion
8. Queries, Modeling, and Transformation
9. Serving Data for Analytics, Machine Learning, and Reverse ETL

#### Part III - Security, Privacy, and the Future of Data Engineering

10. Security and Privacy
11. The Future of Data Engineering

#### Appendices

- Appendix A: Serialization and Compression Technical Details
- Appendix B: Cloud Networking

### 3.4 Designing Data-Intensive Applications

#### Part I - Foundations of Data Systems

1. Reliable, Scalable and Maintainable Applications
2. Data Models and Query Languages
3. Storage and Retrieval
4. Encoding and Evolution

#### Part II - Distributed Data

5. Replication
6. Partitioning
7. Transactions
8. The Trouble with Distributed Systems
9. Consistency and Consensus

#### Part III - Derived Data

10. Batch Processing
11. Stream Processing
12. The Future of Data Systems

### 3.5 The Data Warehouse Toolkit, 3rd Edition

1. Data Warehousing, Business Intelligence, and Dimensional Modeling Primer
2. Kimball Dimensional Modeling Techniques Overview
3. Retail Sales
4. Inventory
5. Procurement
6. Order Management
7. Accounting
8. Customer Relationship Management
9. Human Resources Management
10. Financial Services
11. Telecommunications
12. Transportation
13. Education
14. Healthcare
15. Electronic Commerce
16. Insurance
17. Kimball DW/BI Lifecycle Overview
18. Dimensional Modeling Process and Tasks
19. ETL Subsystems and Techniques
20. ETL System Design and Development Process and Tasks
21. Big Data Analytics

### 3.6 Streaming Systems

#### Part I - The Beam Model

1. Streaming 101
2. The What, Where, When, and How of Data Processing
3. Watermarks
4. Advanced Windowing
5. Exactly-Once and Side Effects

#### Part II - Streams and Tables

6. Streams and Tables
7. The Practicalities of Persistent State
8. Streaming SQL
9. Streaming Joins
10. The Evolution of Large-Scale Data Processing

### 3.7 Big Book of Data Engineering, 4th Edition

#### Introduction

- Introduction to Data Engineering on Databricks

#### Guidance and Best Practices

1. Migrating Apache Spark ETL Workloads to Databricks
2. How Observability in Lakeflow Helps You Build Reliable Data Pipelines
3. A Cost Maturity Journey With Databricks
4. Lakeflow Connect: Efficient and Easy Data Ingestion Using the Microsoft SQL Server Connector
5. Implement CDC Data Load and SCD Type 2 With Lakeflow
6. Optimizing Materialized Views Recomputation
7. Reverse ETL With Lakebase: Activate Your Lakehouse Data for Operational Analytics
8. Production-Grade Data Quality Using Spark Declarative Pipelines
9. Collaborative Data Engineering Made Simple With Databricks Asset Bundles
10. A Practical Guide to Serverless Migrations

#### Case Studies

1. iFood: Transforming Data to Elevate Food Deliveries and Experiences
2. NFCU: Using Real-Time Data to Trailblaze Member Personalization
3. Cincinnati Reds: Winning On and Off the Field With Cutting-Edge Baseball Analytics
4. Porsche Holding: Unifying Customer Data to Drive a New Automotive Experience
5. Hinge Health: Developing Personalized Care Plans to Improve Patient Outcomes

---

## 4. Supplied Free Alternatives and Complementary References

The following table preserves the user's supplied mapping and wording. Tracking parameters have been retained because the instruction was to preserve it word by word.

| Buku asal | Alternatif percuma + link | Coverage dan batas |
|---|---|---|
| **1. Fundamentals of Data Engineering** | [Google Cloud Well-Architected Framework](https://cloud.google.com/architecture/framework?utm_source=chatgpt.com) + [Data Engineering Wiki](https://dataengineering.wiki/?utm_source=chatgpt.com) | Architecture, lifecycle concepts, operations, security dan cost. **Perlu susun sendiri learning sequence; Google framework berorientasikan GCP.** |
| **2. DDIA** | [**Distributed Systems, 4th Edition — Maarten van Steen & Andrew Tanenbaum**](https://www.distributed-systems.net/index.php/books/ds4/?utm_source=chatgpt.com) + Google SRE | Buku digital percuma daripada penulis untuk distributed-systems foundation. **Tak menggantikan keseluruhan penerangan data systems dan trade-offs DDIA.** |
| **3. The Data Warehouse Toolkit** | [**Kimball Dimensional Modeling Techniques**](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/?utm_source=chatgpt.com) | Rujukan terus daripada Kimball untuk dimensional modeling. **Kurang naratif dan worked case studies berbanding buku penuh.** |
| **4. Database Internals** | [**CMU Intro to Database Systems**](https://15445.courses.cs.cmu.edu/fall2024/?utm_source=chatgpt.com) | Bahan kursus meliputi storage, indexes, transactions, concurrency, recovery dan query execution. **Bahan kursus, bukan ebook; tambah Distributed Systems untuk sisi distributed.** |
| **5. Data Pipelines with Apache Airflow** | [**Apache Airflow Documentation**](https://airflow.apache.org/docs/apache-airflow/stable/?utm_source=chatgpt.com) | Concepts, tutorials dan implementation reference. **Pilih version yang sama dengan projek.** |
| **6. Learning Spark** | [**Apache Spark Documentation**](https://spark.apache.org/docs/latest/?utm_source=chatgpt.com) | SQL, DataFrames, Structured Streaming dan configuration. **Lebih sesuai sebagai reference; perlu latihan bertahap.** |
| **7. Streaming Systems** | [**Apache Beam Programming Guide**](https://beam.apache.org/documentation/programming-guide/?utm_source=chatgpt.com) + [Google Dataflow Model paper](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/?utm_source=chatgpt.com) | Windowing, event time, late data dan correctness/latency/cost trade-offs. **Tak seluas keseluruhan buku.** |
| **8. Data Quality Fundamentals** | [**Great Expectations — GX Core**](https://docs.greatexpectations.io/docs/core/introduction/?utm_source=chatgpt.com) + Google SRE Workbook | Validation workflows dan operational monitoring. **Masih perlu tambah data ownership, business quality rules dan reconciliation.** |
| **9. The Site Reliability Workbook** | [**Buku asal, percuma daripada Google**](https://sre.google/workbook/table-of-contents/?utm_source=chatgpt.com) | Tak perlu pengganti—buku penuh boleh dibaca. |
| **10. SQL Performance Explained** | [**Use The Index, Luke!**](https://use-the-index-luke.com/?utm_source=chatgpt.com) | Penulis menyediakan web edition percuma untuk indexing dan SQL tuning. **PDF buku berbayar berasingan.**<br><br><br> |

---

## 5. Consolidated Source Register

This register prevents a source from being silently mistaken for an attached book.

| # | Source | Type | Present as attached PDF? | Primary domain |
|---:|---|---|---|---|
| 1 | Fundamentals of Data Engineering | Book | Yes | DE lifecycle and architecture |
| 2 | Designing Data-Intensive Applications | Book | Yes | Distributed data systems |
| 3 | The Data Warehouse Toolkit, 3rd Edition | Book | Yes | Dimensional modeling and ETL |
| 4 | Database Internals | Book | Yes | Storage engines and distributed internals |
| 5 | Data Pipelines with Apache Airflow, Second Edition | Book | Yes | Orchestration and pipeline operations |
| 6 | Streaming Systems | Book | Yes | Stream processing semantics |
| 7 | Big Book of Data Engineering, 4th Edition | Vendor compilation | Yes | Databricks and Lakeflow implementation patterns |
| 8 | Google Cloud Well-Architected Framework | Web framework | No | GCP architecture and operations |
| 9 | Data Engineering Wiki | Community wiki | No | Broad DE concepts and guides |
| 10 | Distributed Systems, 4th Edition | Free digital book | No | Distributed systems foundation |
| 11 | Google SRE | Free online books/resources | No | Reliability and operations |
| 12 | Kimball Dimensional Modeling Techniques | Web reference | No | Dimensional modeling patterns |
| 13 | CMU Intro to Database Systems | Course materials | No | Database systems internals |
| 14 | Apache Airflow Documentation | Official documentation | No | Current Airflow behavior and APIs |
| 15 | Apache Spark Documentation | Official documentation | No | Current Spark behavior and APIs |
| 16 | Apache Beam Programming Guide | Official documentation | No | Beam model and streaming APIs |
| 17 | Google Dataflow Model paper | Research paper | No | Streaming correctness, latency, and cost |
| 18 | Great Expectations - GX Core | Official documentation | No | Data validation workflows |
| 19 | The Site Reliability Workbook | Free online book | No | Practical reliability operations |
| 20 | Use The Index, Luke! | Free web edition | No | SQL indexing and tuning |

---

## 6. Source Selection Rules

1. Use an attached book for stable principles, established terminology, and chapter-level theory.
2. Use official documentation for exact product behavior, syntax, compatibility, and version-specific features.
3. Use research papers for formal models and the assumptions behind algorithms.
4. Use vendor material as an implementation reference and label vendor-specific recommendations.
5. Use community references to discover practical issues; verify important claims against official documentation, code, tests, or measured evidence.
6. Record business meaning, grain, keys, ownership, SLA, retention, security, and failure policy separately because books cannot determine project-specific business rules.
7. Treat this Markdown file as the canonical catalog. Treat each linked or attached source as authoritative for its own detailed content.

---

## 7. Coverage Map

| Knowledge area | Primary attached source | Complementary source |
|---|---|---|
| End-to-end DE lifecycle | Fundamentals of Data Engineering | Google Cloud Well-Architected Framework; Data Engineering Wiki |
| Distributed systems and correctness | Designing Data-Intensive Applications | Distributed Systems, 4th Edition; Google SRE |
| Dimensional modeling and SCD | The Data Warehouse Toolkit | Kimball Dimensional Modeling Techniques |
| Storage engines and database mechanics | Database Internals | CMU Intro to Database Systems |
| Orchestration, DAGs, testing, deployment | Data Pipelines with Apache Airflow | Apache Airflow Documentation |
| Batch and Spark processing | Big Book of Data Engineering | Apache Spark Documentation |
| Streaming semantics | Streaming Systems | Apache Beam Programming Guide; Google Dataflow Model paper |
| Data quality and validation | Fundamentals of Data Engineering; Big Book of Data Engineering | Great Expectations - GX Core; Google SRE Workbook |
| Reliability and incident operations | Data Pipelines with Apache Airflow | The Site Reliability Workbook; Google SRE |
| SQL performance | Database Internals | Use The Index, Luke! |

---

## 8. Known Gaps Requiring Additional Sources or Project Evidence

- Business rules, stakeholder decisions, business glossary, and metric definitions
- Source-system contracts, data ownership, and change-management agreements
- Engine- and version-specific details for Snowflake, Delta Lake, dbt, Kafka, Debezium, cloud IAM, and networking
- Data privacy, regulatory requirements, retention schedules, and audit evidence for the operating jurisdiction
- Cost baselines, workload measurements, query plans, performance benchmarks, and capacity limits
- Recovery drills, replay tests, concurrency tests, failure injection, and incident postmortems
- CI/CD implementation, infrastructure as code, secrets management, and environment promotion strategy
- Data product ownership, SLOs, escalation routes, on-call practices, and operational runbooks

---

## 9. Integrity Note

- All seven attached filenames are recorded exactly once in the inventory.
- All ten supplied free-reference rows are recorded exactly once.
- Chapter-level indexes were extracted from the attached PDFs and normalized only for encoding artifacts and heading structure.
- Detailed book prose is intentionally not duplicated in this catalog. Retrieve the relevant chapter from the corresponding source when deeper context is required.
