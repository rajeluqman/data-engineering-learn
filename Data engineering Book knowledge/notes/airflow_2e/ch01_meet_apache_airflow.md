# Ch.1 — Meet Apache Airflow

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 33–50 (18 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Data pipeline, defined via a worked three-step weather-dashboard example [S]** (p34): "data pipelines generally consist of several tasks or actions that must be executed to achieve the desired result" — the chapter's own running example fetches weather data, cleans/transforms it, then pushes it to a dashboard.

Explicit ordering constraint (p34): these tasks need to be executed in a specific order, since "it doesn't make sense to try transforming the data before fetching it, for example."

**Directed acyclic graph (DAG), defined as the explicit representation of task dependencies [S]** (p35): tasks are nodes, dependencies are directed edges, with an edge from task 1 to task 2 meaning "task 1 needs to be completed before task 2 can start."

The acyclic property is explicitly named critical (p35): a cycle (task A depends on B, B depends on A) creates "this logical inconsistency leads to a deadlock in which neither task 2 nor 3 can run, preventing us from executing the graph."

**The DAG execution algorithm, the chapter's own three-step conceptual loop [S]** (p36): for every open task, check whether all upstream tasks (tasks on the other end of incoming edges) are complete; if so, queue the task for execution; execute queued tasks and mark them complete; repeat until the whole graph is done. Worked via the weather-dashboard example across three loop iterations (p36–37, Figure 1.4): fetch has no upstream dependency and runs first; clean becomes eligible only after fetch completes; push becomes eligible only after clean completes. `[D]`

**Graph-based pipelines vs. monolithic scripts, two named explicit advantages [S]** (p38): independent branches of a DAG (e.g. fetching/cleaning weather data vs. sales data in the umbrella-demand example) can be executed in parallel "if we apply our graph execution algorithm, making better use of available resources and potentially decreasing the running time of a pipeline compared with executing the tasks sequentially."

Separately (p39), a DAG's incremental-task decomposition means "we need to rerun only tasks that failed" and any downstream dependencies, rather than the whole pipeline as a single monolithic script would require. `[D]`

**Workflow managers, defined as the general category Airflow belongs to, with a comparison table of twelve named alternatives [S]** (p39): "the challenge of running graphs of dependent tasks is hardly a new problem" — the chapter's own comparison table (Airflow, Argo, Azkaban, Conductor, Dagster, Luigi, Make, Metaflow, Nifi, Oozie, Prefect, Temporal, Control-M) differentiates tools by workflow-definition format (XML/YAML/JSON/code), scheduling support, backfilling support, UI presence, and horizontal scalability.

Named key trade-off (p40): static-file-defined workflows (Oozie's XML) "provide legible workflows but limited flexibility."

Code-defined workflows (Luigi, Airflow), by contrast, "provides greater flexibility but can be more challenging to read and test" (p40).

**Airflow's five core components, the chapter's own architecture breakdown [S]** (p41–42): the **DAG processor** parses DAG files and serializes them into the Airflow metastore via the API server; the **scheduler** checks each DAG's schedule and queues tasks whose upstream dependencies are satisfied once their interval has passed; **workers** pick up queued tasks and execute them; the **triggerer** checks completion status for tasks supporting asynchronous/deferred processing, freeing workers while waiting on external conditions; the **API server** is (p42) "the main interface where users can visualize DAGs and monitor DAG runs," and functions as the mandatory gateway for all other components' metastore reads/writes — "all database interaction should be done via the Airflow API server."

**The scheduler's operating loop, the chapter's own five-step description, explicitly identified as the same algorithm as §1's generic DAG-execution loop [S]** (p43–44): DAG processor extracts tasks/dependencies/schedule into the metastore; for each DAG, the scheduler checks whether the schedule interval has elapsed and if so schedules its tasks; for each scheduled task, checks whether upstream dependencies are satisfied and if so queues it; tasks depending on external resources may be deferred to the triggerer, freeing workers; loop back to the interval check.

Explicit note (p44): "the steps followed by the scheduler are similar to the algorithm introduced in section 1.1. This similarity is no accident."

**Airflow's DAG-as-Python-code model, defined with an explicit flexibility rationale [S]** (p40): each DAG file is "essentially Python scripts that describe the structure of the corresponding DAG." Airflow parses these files to extract task/dependency/schedule structure.

Named advantage (p40): "this programmatic approach gives you a lot of flexibility for building DAGs." This includes dynamically generating optional tasks or entire DAGs from external metadata or config files. `[D]`

Airflow 3 additionally introduces an experimental non-Python (Go) SDK option, though Python remains Airflow's primary language (p40). `[D]`

**Incremental loading and backfilling, defined as a named powerful consequence of schedule-interval semantics [S]** (p47): Airflow's schedule provides "details about the last and next (expected) schedule intervals." This lets a DAG run process only the data delta for its own interval instead of reprocessing the entire dataset each run — a significant time/cost benefit at scale. Backfilling extends this by letting a DAG be executed retroactively for past schedule intervals, enabling both historical-dataset creation and full reprocessing after a code change, by clearing and rerunning past task results. `[D]`

**Airflow's named fit criteria, five explicit reasons to choose and three explicit reasons not to choose [S]** (p48): good fits — regular time-based scheduled workflows, irregular event-triggered workflows, workflows needing discrete time-interval bucketing of data, integration with a wide variety of external systems (via Airflow's provider ecosystem), and workflows benefiting from software-engineering practices applied to pipeline code, plus easy backfilling.

Poor fits (p49): streaming pipelines — Airflow is "designed primarily to run recurring or batch-oriented tasks rather than streaming workloads"; teams with little/no programming experience, for whom a GUI-based or static-definition tool may fit better; and very large use cases where DAG code complexity requires deliberate engineering discipline (DRY, Single Responsibility Principle) and where Airflow's lack of built-in data-lineage/versioning features may require pairing with specialized tools (mitigated somewhat by recent OpenLineage support).

## 2. WHAT / WHY / WHEN

**WHAT:** an introduction to representing data pipelines as directed acyclic graphs of dependent tasks, the generic algorithm for executing such graphs, and Airflow's specific realization of this model — Python-code-defined DAGs, a five-component architecture (DAG processor, scheduler, workers, triggerer, API server), and the operational features (scheduling, backfilling, monitoring UI, automatic retry) that follow from it. `[D]`

**WHY it matters:** the chapter's implicit argument is that the DAG abstraction is not Airflow-specific but a general solution to dependency-ordered task execution, and Airflow's specific value proposition is combining that general abstraction with Python-native flexibility, a broad systems-integration ecosystem, and schedule-interval semantics that make incremental (rather than full-reprocessing) batch pipelines the default, cheap option. `[D]`

**WHEN to choose Airflow vs. an alternative workflow manager, synthesized from the chapter's own fit criteria (p48–49):** choose Airflow for batch-oriented, schedule-driven or event-triggered pipelines integrating many external systems, built by teams comfortable writing pipeline structure as Python code; choose a different tool (streaming framework, GUI-based workflow tool, or a data-lineage-specialized platform) when the workload is fundamentally streaming, the team lacks programming experience, or strict built-in lineage/versioning is a hard requirement Airflow does not natively provide. `[D]`

## 3. Assumptions and prerequisites

- Assumes roughly one year of Python experience (string formatting, comprehensions, args/kwargs), basic Linux terminal familiarity, and basic SQL/database and data-format knowledge, per the chapter's own stated reader expectations for the rest of Part 1. `[S]` (p49)
- Forward-references dynamic DAG generation and custom operators to Ch.12 and later parts of the book — not yet synthesized in this vault. `[S]` (p49)
- Forward-references detailed scheduling mechanics to Ch.3 and Ch.4 — not yet synthesized in this vault. `[S]` (p44)

## 4. Mechanism / key steps

**Airflow's scheduling-to-execution pipeline, the chapter's own five-step worked description (p43–44)** `[D]`: a user writes a workflow as a DAG file → the DAG processor reads the file, extracts tasks/dependencies/schedule interval, and stores the result in the Airflow metastore → the scheduler periodically checks whether each DAG's schedule interval has elapsed; if so, it schedules that DAG's tasks → for each scheduled task, the scheduler checks whether its upstream dependencies are satisfied, queuing it for execution if so → tasks awaiting external conditions may be deferred to the triggerer instead of occupying a worker → workers pick up queued tasks, execute them, and report results back through the API server to the metastore, where they become visible in the web UI.

## 5. Trade-offs and limitations

- **Code-defined DAGs (Airflow, Luigi) trade legibility for flexibility, compared to static-file-defined workflows (Oozie's XML), which are more legible but far less flexible (§1, p42–43):** an explicit, named trade-off the chapter uses to differentiate workflow managers, with no universally correct choice.
- **Graph-based, incrementally-composable pipelines cost more upfront design effort than a single monolithic script but pay that cost back via cheaper partial reruns and parallel execution of independent branches (§1, p41–43):** the chapter frames this as a durable advantage for any pipeline expected to fail partially or scale in complexity, not a free win for trivial one-off scripts.
- **Airflow's batch/schedule-interval design is a poor fit for genuinely streaming or highly dynamic (structurally day-to-day-changing) workloads (§1, p49):** the chapter is explicit that this is a deliberate design trade-off, not a current limitation expected to be fixed — Airflow is "designed primarily" for batch-oriented recurring tasks.

## 6. Failure modes and edge cases

- **Circular task dependencies producing an unresolvable deadlock (§1, p37–38):** the chapter's own explicit worked case — if task 2 depends on task 3 and task 3 depends on task 2, "neither task 2 nor 3 can run," and the acyclic constraint on DAGs exists specifically to rule this scenario out structurally.
- **Monolithic-script pipelines requiring a full rerun on any task failure (§1, p41):** named directly as an inefficiency graph-based decomposition avoids — "we'd have to rerun the entire script" in the monolithic case, versus only the failed task and its downstream dependents in a DAG.
- **Default automatic retry masking only intermittent failures, not systematic ones (§1, p49–50):** Airflow's configurable retry-with-backoff "can help tasks recover from any intermittent failures," but the chapter implies (via the subsequent discussion of the grid view for debugging genuinely failed tasks) that retries are not a substitute for diagnosing a systematically broken task.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the DAG-vs-monolithic-script decision framing (§1, §5, p41–43) is directly reusable as a first-pass justification for structuring any new data pipeline in this vault's projects as an explicit task graph rather than a single script, specifically once partial-failure recovery or parallelizable independent branches are relevant. `[D]`
- **Build:** the incremental-loading/backfilling pattern (§1, p47) is a directly reusable default for any new Airflow pipeline processing time-partitioned data — process only the current interval's delta by default, and rely on backfilling rather than full-dataset reprocessing scripts when historical data or a code fix needs to be applied retroactively.
- **Maintain:** the "all database interaction should be done via the Airflow API server" architectural rule (§1, p45) is a directly reusable constraint when reasoning about or debugging any custom Airflow component or plugin that might be tempted to talk to the metastore directly.
- **RCA:** an Airflow task observed silently retrying without ever succeeding is directly diagnosable via the grid view's per-task-instance log drill-down (§1, p49–50) before assuming a scheduler or infrastructure problem — the chapter frames this as the standard first debugging step.
- **Optimization:** the fit-criteria checklist (§2, p48–49) is directly reusable for evaluating, at a project's outset, whether Airflow is the right orchestration tool at all — avoiding the cost of building on top of a batch-oriented orchestrator for a workload that is actually better served by a streaming framework or a GUI-based tool for a low-code team.

## 8. How to test / verify these claims

- The DAG execution algorithm's dependency-respecting ordering (§1, §4, p39–40) is directly reproducible: implement the chapter's own three-task weather-dashboard DAG in Airflow, observe via the graph/grid view that `clean` never starts before `fetch` completes and `push` never starts before `clean` completes.
- The parallel-execution claim for independent branches (§1, p42–43) is directly testable: run the umbrella-demand DAG's two independent fetch/clean branches (weather and sales) and confirm via the grid/graph view that both branches' tasks can run concurrently rather than strictly sequentially.
- The incremental-loading/backfilling claim (§1, p47) is directly testable: configure a DAG with a daily schedule, run it forward normally, then trigger a backfill for a past date range and confirm each backfilled run processes only that date's data slice rather than the entire historical dataset.
- The automatic-retry claim (§1, p49–50) is directly testable: configure a task with a transient, intermittent failure condition and a nonzero retry count, and confirm Airflow retries it the configured number of times before marking it failed if retries are exhausted.

## 9. Cross-references

- Forward-references dynamic DAG generation and custom operators/sensors to [[ch09_extending_airflow_with_custom_operators_and_sensors|Ch.9]] and [[ch12_best_practices|Ch.12]] — not yet synthesized in this vault.
- Forward-references detailed scheduling semantics to [[ch03_time_based_scheduling|Ch.3]] (Time-based scheduling) and [[ch04_asset_aware_scheduling|Ch.4]] (Asset-aware scheduling) — not yet synthesized in this vault.
- No cross-reference yet possible to other sources in this vault, since this is the first `airflow_2e` chapter synthesized.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 1.1–1.14 (weather-dashboard and umbrella-demand DAG diagrams, workflow-manager comparison table, Airflow architecture and scheduler-loop diagrams, and web-UI screenshots: login, main page, Dags tab, graph view, grid view) | Structure and content described narratively above where load-bearing (§1, §4); full diagram/table layouts and screenshot content not reproduced verbatim. |
| The full workflow-manager comparison table's per-tool column detail (Table 1.1: origin company, language, scheduling/backfilling/UI/installation-platform/horizontal-scalability flags for all 12 listed tools) | Chapter itself presents this as reference material; this note captures the comparative dimensions and the two named illustrative examples (Oozie vs. Luigi/Airflow) rather than reproducing the full table. |
| Detailed screenshot-level walkthrough of the Airflow web UI (login page, main page, Dags tab, graph view, grid view) | Described at the level of what each view is for and shows, per the chapter's own framing; exact visual layout and screenshot content not reproduced, since it is illustrative UI documentation rather than conceptual content. |
