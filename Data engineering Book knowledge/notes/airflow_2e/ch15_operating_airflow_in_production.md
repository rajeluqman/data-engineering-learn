# Ch.15 — Operating Airflow in production

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 413–453 (41 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Executor** [S]: "In Airflow, an executor configures the execution modes."
(p416)

**Metastore** [S]: "Everything that happens in Airflow is registered in a database, referred to as the metastore."
(p426)

**API server (Airflow 3)** [S]: "Airflow 3 introduced the API server as the intermediary between components."
(p415)

**DAG processor** [S]: "The DAG processor parses DAG files (i.e., reads DAG files, extracts bits and pieces, and stores these bits in the metastore) and makes them available to Airflow in general."
(p415)

**Task scheduler vs. task executor (scheduler's two responsibilities)** [S]: "Determining which tasks are ready to execute and placing them in the queued state, also known as the task scheduler" and "Fetching and executing tasks in the queued state, also known as the task executor."
(p429)

**StatsD instrumentation** [S]: "In the context of StatsD and Airflow, being instrumented means that certain events in Airflow result in sending information about the event so that it can be collected, aggregated, and visualized or reported."
(p439)

**Alert fatigue** [S]: "too many alerts can lead to alert fatigue, a situation in which people ignore alerts when they're too common."
(p445)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter covers operating Airflow itself as a production system — the full component architecture, choosing and configuring an executor, metastore setup, scheduler tuning, DAG-processor tuning, logging, metrics/monitoring (Prometheus/Grafana), failure alerting, and scaling to multiple Airflow instances.

**WHY** [D]: "we'll switch gears and discuss what it takes to run and deploy Airflow from an operations perspective" (p413) — the book's earlier chapters focused on building pipelines as a user; this chapter addresses running Airflow itself reliably at scale.

**WHEN** [D]: choose `LocalExecutor` for a single machine that's sufficient (§15.2.2); choose `CeleryExecutor` when scaling across multiple machines without needing full container isolation; choose `KubernetesExecutor` when container isolation per task and existing Kubernetes familiarity matter; choose `EdgeExecutor` when a task must run in an environment physically separate from the rest of Airflow (§15.2.2); split into multiple Airflow instances only once organizational/team scale makes a shared instance's single-point-of-failure and resource-contention risk unacceptable (§15.9).

## 3. Assumptions and prerequisites

- Prerequisite: the high-level Airflow architecture introduced in chapter 1, revisited and expanded here (p413, "Back in chapter 1, we showed the Airflow architecture displayed in figure 15.1").
- Prerequisite: deferrable operators/triggerer concept from earlier chapters, referenced when describing the triggerer component (p414).
- Assumes a general understanding of distributed software architecture, logging, monitoring, and alerting concepts, but "no specific technology knowledge is required" (p413).
- Assumes the target-state Airflow 3 architecture (API server as gateway to the metastore for all components) even though, as the source notes, "At the time of writing, this gateway wasn't yet fully implemented for all components" (p414-415) — actual behavior may differ depending on the Airflow version in use [U].

## 4. Mechanism / key steps

1. Identify the six executor types Airflow supports at time of writing — `LocalExecutor`, `CeleryExecutor`, `BatchExecutor` (AWS, experimental), `KubernetesExecutor`, `EcsExecutor` (AWS), `EdgeExecutor` (experimental) — and set the active one via `AIRFLOW__CORE__EXECUTOR` (p416).

2. Configure a hybrid multi-executor setup by listing multiple executors in `airflow.cfg`'s `[core] executor` value (e.g. `'LocalExecutor,CeleryExecutor'`), then select per-task via the `executor` argument on an operator (p417, Listing 15.1) — avoid the statically-coded `CeleryKubernetesExecutor`/`LocalKubernetesExecutor` hybrids, which the source explicitly recommends against (p417).

3. Set up `LocalExecutor` by setting `AIRFLOW__CORE__EXECUTOR=LocalExecutor`, tuning subprocess parallelism via `AIRFLOW__CORE__PARALLELISM` (default 32), and installing Airflow with a MySQL or PostgreSQL extra (p419-420).

4. Set up `CeleryExecutor` by installing the `celery` extra, setting `AIRFLOW__CORE__EXECUTOR=CeleryExecutor`, configuring a broker URL (`AIRFLOW__CELERY__BROKER_URL`, e.g. Redis or RabbitMQ) and a result backend (`AIRFLOW__CELERY__RESULT_BACKEND`), ensuring the DAGs folder is identically accessible to all worker machines, then starting the API server, scheduler, and `airflow celery worker` (p420-422).

5. Monitor Celery-based deployments with Flower (`airflow celery flower`, default port 5555) for worker/task status (p422).

6. Set up `KubernetesExecutor` by setting `AIRFLOW__CORE__EXECUTOR=KubernetesExecutor`; each task runs in its own pod, created via a pod-creation request to the Kubernetes API running `airflow tasks run ...` (p422-423) — distribute DAG files to pods via a shared `PersistentVolume`, a Git-sync init container, or building DAGs into the image (p424).

7. Set up `EdgeExecutor` by installing `apache-airflow-providers-edge3`, setting the full executor path, `AIRFLOW__CORE__INTERNAL_API_SECRET_KEY`, `AIRFLOW__EDGE__API_ENABLED=True`, and `AIRFLOW__EDGE__API_URL`; manage workers via `airflow edge list-workers` and maintenance-mode CLI commands (p425).

8. Initialize/migrate the metastore with `airflow db migrate`, pointing Airflow at a production database via `AIRFLOW__CORE__SQL_ALCHEMY_CONN` in URI form (p426-427); disable example DAGs/connections with `AIRFLOW__CORE__LOAD_EXAMPLES=False` and `AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False` before the first `db migrate` (p427-428).

9. Tune scheduler behavior via `AIRFLOW__SCHEDULER__SCHEDULER_HEARTBEAT_SEC`, `AIRFLOW__SCHEDULER__SCHEDULER_HEALTH_CHECK_THRESHOLD`, `AIRFLOW__SCHEDULER__MAX_DAGRUNS_TO_CREATE_PER_LOOP`, `AIRFLOW__SCHEDULER__MAX_DAGRUNS_PER_LOOP_TO_SCHEDULE`, and `AIRFLOW__SCHEDULER__IDLE_SLEEP_TIME` to trade CPU/database load against scheduling latency (p431-432).

10. Run multiple scheduler instances for scalability/redundancy — Airflow uses row-level database locking (`SELECT ... FOR UPDATE`) instead of a consensus algorithm, requiring PostgreSQL 9.6+ or MySQL 8+ (p431).

11. Control maximum parallel task counts via `AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG` (default 16), `AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG` (default 16), `AIRFLOW__CORE__PARALLELISM` (default 32, global), and `AIRFLOW__CELERY__WORKER_CONCURRENCY` (default 16, Celery-specific), plus the `default_pool`'s 128-slot ceiling and per-task `pool` assignment (p432-433).

12. Tune the DAG processor manager via `AIRFLOW__DAG_PROCESSOR__MIN_FILE_PROCESS_INTERVAL`, `AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL` (default 300s), and `AIRFLOW__DAG_PROCESSOR__PARSING_PROCESSES` (default 2, fixed to 1 on SQLite), trading CPU use against DAG-change pickup latency (p433-435).

13. Configure remote logging (S3, GCS, Azure Blob, Elasticsearch, OpenSearch, Redis, Alibaba OSS) by installing the corresponding provider extra and setting `AIRFLOW__LOGGING__REMOTE_LOGGING=True` plus `AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID` (p437-438).

14. Instrument metrics with StatsD (push model): install the `statsd` extra, set `AIRFLOW__METRICS__STATSD_ON=True`, `STATSD_HOST`, `STATSD_PORT`, `STATSD_PREFIX` (p440).

15. Build a Prometheus/Grafana monitoring stack: run the Prometheus StatsD exporter to translate StatsD metrics to Prometheus format, configure Prometheus to scrape that exporter, then add Prometheus as a Grafana data source and build dashboards (p441-444, Listings 15.9-15.13).

16. Configure failure alerting via `on_failure_callback` (DAG- or task-level, propagated through `default_args`), `on_success_callback`, `on_retry_callback`, or the built-in `email_on_failure` argument with SMTP configuration (`AIRFLOW__SMTP__*`) and an `email` address per task (p447-449).

## 5. Trade-offs and limitations

- The `LocalExecutor` is "easy to set up and gives you decent performance," but "is limited by the resources of the scheduler's machine" (p420) — no horizontal scaling.
- `CeleryExecutor` is "easier to set up from scratch because you don't need to set up infrastructure in the form of Kubernetes" compared to `KubernetesExecutor` (p422), but sharing the DAGs folder across all worker machines "can be challenging to set up" (p420).
- `KubernetesExecutor` provides strong per-task isolation but "it helps to have existing knowledge of Kubernetes, which can be large and complex."
(p423)

Helm-based DAG distribution options each carry their own trade-off (shared volume vs. sync delay vs. redeploy-on-DAG-change) (p424).
- `EdgeExecutor` is explicitly experimental: "There are some limitations on the EdgeExecutor at the time of writing (particularly with respect to logging), and its performance is untested" (p419).
- Lowering `AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL` gets DAG changes picked up faster but "can also lead to a significant increase in CPU use because the DAGs are being parsed constantly" (p434).
- A single shared Airflow instance across teams is cost-efficient but creates a single point of failure and DAG-ownership/permission challenges; per-team instances give isolation but duplicate infrastructure cost and lose cross-instance dataset-event triggering by default (p449-452).
- Prometheus/Grafana metrics are "close to real time but not millisecond real time" (up to roughly a minute of delay) and Prometheus itself "isn't a reporting system and doesn't store individual events" (p445) — InfluxDB is suggested for event-level reporting instead.
- Alerting is a "double-edged sword": too many alerts cause alert fatigue, where people start ignoring them (p445).

## 6. Failure modes and edge cases

- **Disabled example DAGs remain in the metastore**: setting `AIRFLOW__CORE__LOAD_EXAMPLES=False` after DAGs have already been loaded "tells Airflow not to load example DAGs" (p428) — "DAGs that are already loaded remain in the database and are not deleted" (p428) — cleanup requires explicit removal.
- **Row-level-locking prerequisite for multi-scheduler**: "Airflow allows you to disable row-level locking. If you do this, however, you can't run multiple schedulers because of the risk that multiple schedulers would interact with the same rows in the database" (p431).
- **Metric-model mismatch between StatsD and Prometheus**: "a StatsD metric results in a unique metric name in Prometheus" when hierarchical dot-separated names aren't automatically converted to Prometheus labels, requiring explicit exporter configuration (p443).
- **SMTP misconfiguration silently prevents alert emails**: `email_on_failure` defaults to `True` on `BaseOperator`, but "Without the proper SMTP configuration, however, Airflow won't email" — a silent no-op rather than an error (p449).
- **Cross-instance dataset triggering not supported by default**: in a multi-instance-per-team setup, "by default, data set events are available only within a single Airflow instance"
(p452), so triggering team 2's DAGs from team 1's dataset updates requires custom tooling (e.g. Airbridge).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: pick the executor based on actual scaling and isolation needs, not novelty — the source explicitly notes "even on Kubernetes sometimes, the CeleryExecutor can still be a great choice" due to KubernetesExecutor's per-pod overhead (p452, Summary).
- **Build** [D]: always disable example DAGs/connections and use a production database (PostgreSQL/MySQL) before the first `airflow db migrate` in a real deployment, since retroactive cleanup is manual (p427-428).
- **Maintain** [D]: raise `AIRFLOW__SCHEDULER__SCHEDULER_HEARTBEAT_SEC` (e.g. to 60s) to reduce metastore query load at scale, and tune `MAX_DAGRUNS_TO_CREATE_PER_LOOP` when running multiple schedulers with many/large DAGs to avoid skew between schedulers (p431-432).
- **RCA** [D]: to diagnose scheduler health, check `dag_processing.import_errors` (should be 0), `dag_processing.total_parse_time` (spikes indicate DAG-processing problems), and `executor.queued_tasks`/`executor.running_tasks`/`executor.open_slots` before assuming an application-level bug (p446-447).
- **Optimization** [D]: instrument Airflow with StatsD/OpenTelemetry and route through Prometheus + Grafana (preferred over StatsD's native format for its label-based flexibility) to track latency, load, errors, and saturation across DAG, task, and component levels (p437-447).

## 8. How to test/verify these claims

- Verify executor installation by running any DAG and confirming a task reaches the running state, since "If any task makes it to running state, it went through the cycle of being scheduled, queued, and running" (p419).
- Verify multi-scheduler safety by starting a second `airflow scheduler` process against a PostgreSQL 9.6+/MySQL 8+ metastore and confirming both process tasks without duplication (p431).
- Verify remote logging by configuring `AIRFLOW__LOGGING__REMOTE_LOGGING=True` with a test bucket/connection, running a task, and confirming its log appears in the remote system rather than only the local filesystem (p437-438).
- Verify the Prometheus/Grafana pipeline end-to-end by following Listings 15.9-15.13 (p442-444) exactly, confirming the Airflow target shows "UP" on Prometheus's targets page and a metric (e.g. `airflow_dag_processing_total_parse_time`) renders in a Grafana panel.
- Verify failure alerting by deliberately failing a task (`bash_command="exit 1"`) with `on_failure_callback` and `email_on_failure` configured, and confirming both the callback executes and (with valid SMTP config) an email is sent, per the task log line `Sent an alert email to [...]` (p449, Listing 15.15 context).

## 9. Cross-references

- Chapter 1 (Airflow architecture overview): the component diagram (Figure 15.1) revisits and extends this chapter's baseline (p413).
- Chapter 17 (Airflow deployment options, referenced as a future chapter): Helm-based Kubernetes deployment details are deferred there — "Chapter 17 describes the process of installing, configuring, and managing Airflow with Helm."
(p423)

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 15.1–15.18 (architecture diagrams, UI/dashboard screenshots) | Visual content; described narratively where relevant, not reproduced. |
| Full example log output (Listings 15.3, 15.5, 15.7-15.8, 15.10) | Representative lines cited; full raw log dumps reproducible from the source PDF directly rather than duplicated verbatim here. |
| Full list of Prometheus exporters and metrics catalog | The source itself defers to the Airflow documentation for the complete metrics list (p447); only representative diagnostic metrics are captured here. |
| Vendor-specific multi-instance guidance (Astronomer, Google, AWS links) | External vendor documentation cited by the source (p452) rather than content synthesized in the chapter itself. |
