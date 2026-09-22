# Appendix B — Prometheus metric mapping

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 504–505 (2 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: appendix`

## 1. Concepts and definitions

**StatsD-to-Prometheus metric mapping** [S]: "This appendix contains a mapping for converting metrics from StatsD format to Prometheus format, as explained in chapter 15."
(p504)

**StatsD exporter role** [S]: "The StatsD exporter takes StatsD metrics provided by Airflow and exposes them in a format Prometheus can read."
(p504)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this appendix is the full YAML mapping configuration used by the Prometheus StatsD exporter to translate Airflow's native StatsD metric names into Prometheus-style metric names and labels.

**WHY** [S]: "Some conversions, however, aren't efficient or in line with Prometheus's naming conventions, so this mapping explicitly maps Airflow's StatsD metrics to Prometheus metrics."
(p504)

**WHEN** [D]: consult/apply this mapping when configuring the Prometheus StatsD exporter as part of the chapter 15 monitoring stack (§15.7).

## 3. Assumptions and prerequisites

- Prerequisite: the StatsD/Prometheus/Grafana monitoring setup from chapter 15, which this mapping directly supports (p504, "as explained in chapter 15").
- Assumes this mapping is current only as of the book's writing: "Because Airflow is an open source project, this mapping is subject to change."
(p504) [U] — verify against the current Airflow version's actual StatsD metric names before relying on it in production.

## 4. Mechanism / key steps

1. Match Airflow's dot-separated StatsD metric name patterns (e.g. `airflow.dag_processing.total_parse_time`, `airflow.dag.*.*.duration`) using the exporter's `match` field, with `*` wildcards capturing dynamic path segments (e.g. `dag_id`, `task_id`) (p504-505, Listing B.1).

2. Map each matched StatsD pattern to an explicit Prometheus metric `name` (e.g. `airflow_dag_processing_time`, `airflow_task_duration`) plus optional `help` text and `labels` built from captured wildcard groups (`$1`, `$2`) (p504-505).

3. Cover the specific metrics: DAG processing total parse time, per-DAG/task duration, DAG bag size (count), DAG processing import errors, per-file DAG loading duration, per-file last processing duration/seconds-ago/runtime, per-DAG dependency-check and success duration, per-DAG schedule delay, and executor open/queued/running task slot counts (p504-505, Listing B.1).

## 5. Trade-offs and limitations

- The mapping is explicitly a workaround for a mismatch between StatsD's hierarchical naming and Prometheus's label-based data model: "Some conversions... aren't efficient or in line with Prometheus's naming conventions" without this explicit mapping (p504).
- The mapping is not guaranteed to remain accurate across Airflow versions, since "Because Airflow is an open source project, this mapping is subject to change" (p504) [U].

## 6. Failure modes and edge cases

- **Stale mapping against a newer Airflow release**: if Airflow renames or adds StatsD metrics in a later version, this appendix's mapping (and the identically-named one in the book's GitHub repository) may no longer match, silently dropping or mis-labeling metrics in Prometheus — not independently verified in this session against any specific current Airflow version [U].

## 7. Implications for design/build/maintain/RCA/optimization

- **Build** [D]: apply this mapping file directly to the Prometheus StatsD exporter configuration when following chapter 15's monitoring setup, rather than relying on the exporter's generic default conversion rules, which chapter 15 itself noted don't always produce clean Prometheus labels.
- **Maintain** [D]: re-verify this mapping against the installed Airflow version's actual StatsD metric names periodically, given the source's own explicit warning that it's subject to change (p504).

## 8. How to test/verify these claims

- Apply Listing B.1's mapping to a running Prometheus StatsD exporter (as set up in chapter 15, §15.7.3) and confirm that querying `http://localhost:9102/metrics` shows the mapped Prometheus metric names (e.g. `airflow_dag_processing_time`, `airflow_task_duration{dag_id=...,task_id=...}`) rather than raw StatsD-style dot-separated names.
- Cross-check each `match` pattern in this appendix against the current Airflow version's actual emitted StatsD metric names (Airflow's own metrics documentation) to confirm the mapping is still current before relying on it [U] — not verified in this session.

## 9. Cross-references

- Chapter 15 (operating Airflow in production, §15.7, visualizing and monitoring Airflow metrics): this appendix is the direct reference material for that chapter's StatsD/Prometheus/Grafana monitoring setup (p504).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| None — the appendix is short and its full mapping content is captured in §4 above | Not applicable. |
