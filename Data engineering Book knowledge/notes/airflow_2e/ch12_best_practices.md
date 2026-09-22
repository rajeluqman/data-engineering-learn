# Ch.12 — Best practices

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 321–351 (31 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Factory function** [S]: "This type of function takes any required configuration for the steps and generates the corresponding DAG or set of tasks, thus producing it (like a factory)."
(p332)

**Task group** [S]: "Task groups allow you to visually group sets of tasks into smaller groups, making your DAG structure easier to oversee and comprehend."
(p335)

**Dynamic Task Mapping** [S]: "Dynamic Task Mapping allows you to change the structure of your DAG dynamically to reflect the data you're processing in a DAG run."
(p338)

**`expand()` / `partial()`** [S]: "expand()—This function is the one into which we pass the values we want to map"
(p339) [D] (source continues "over. For each element of the input, a separate task is created and rendered in the Airflow UI" across a line wrap).

"partial()—Any parameters that should remain constant for all mapped values"
(p339) [D] (source continues "passed into expand should be passed into partial, including the base operator parameters such as task_id").

**Idempotency (restated)** [S]: "idempotency, which means that rerunning the same task multiple times produces the same overall result (assuming that the task itself hasn't changed)."
(p344)

**Determinism** [S]: "a task should always"
(p344) [D] (source continues "return the same output for a given input. By contrast, nondeterministic tasks prevent you from building reproducible DAGs" across a line wrap).

**Resource pool** [S]: "Airflow allows you to control how many tasks have access to a given resource by using resource pools. Each pool contains a fixed number of slots, which grant access to the corresponding resource."
(p349)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter is a collection of cross-cutting practices for production-quality DAGs — code style, credential/configuration management, avoiding computation in DAG parsing, factory functions, task groups, Dynamic Task Mapping, idempotency/determinism, efficient data handling, and resource pools.

**WHY** [S]: "we'll dive a bit deeper into some best practices that can help you write well-architected DAGs that are both easy to understand and efficient in terms of how they handle your data and resources."
(p321)

**WHEN** [D]: adopt style guides/linters/formatters always (§12.1.1); centralize credentials via the metastore or a secrets backend whenever a DAG touches external systems (§12.1.2); use factory functions when the DAG structure is fixed but repeated across similar inputs known at parse time (§12.1.5); use Dynamic Task Mapping instead when the number of tasks depends on run-time data (§12.1.8); use resource pools whenever multiple tasks could overwhelm a shared downstream resource (§12.4).

## 3. Assumptions and prerequisites

- Prerequisite: atomicity and incremental processing concepts from chapter 3, explicitly reused: "As briefly discussed in chapter 3, one of the key requirements for a good Airflow task"
(p344) [D] (source continues "is idempotency, which means that rerunning the same task multiple times produces the same overall result").

"The main idea behind incremental processing (which we touched on in chapter 3)"
(p347).
- Prerequisite: the umbrella DAG from chapter 6, reused as a task-groups example: "In our DAG for training"
(p336) [D] (source continues "machine learning models in chapter 6, for example, we created a considerable number of tasks for fetching and cleaning weather and sales data" across a hyphenated line wrap).
- Prerequisite: scheduling mechanisms from chapters 3-4, referenced when discussing explicit timetable classes: "As discussed at length in chapters 3 and 4, you have multiple ways to define your DAG's schedule in Airflow."
(p336)
- Dynamic Task Mapping's traditional (non-Taskflow) syntax assumes familiarity with XCom, since mapped values are wrapped in lists specifically because of XCom's mechanics (p339).

## 4. Mechanism / key steps

1. Adopt a style guide (PEP 8, Google Python Style Guide) and static checkers (Flake8, Pylint) or an all-in-one tool (Ruff) to catch style and correctness issues; run e.g. `python -m flake8 dags/*.py` (p322-325, Listings 12.1-12.9) — note Airflow-specific Ruff rules exist for migration linting: `ruff check dags/ --select AIR3 --preview --show-fixes` (p325).

2. Apply a code formatter (Black or YAPF) consistently across the team to remove formatting bikeshedding, e.g. `python -m black dags/` (p324-325, Listings 12.5-12.8).

3. Pick one consistent DAG-definition style (context manager, plain variable, or Taskflow `@dag`) and one consistent task-dependency notation (`>>`, `<<`, `.set_downstream()`, etc.) per team, since Airflow supports several equivalent syntaxes (p325-326, Listings 12.10-12.13).

4. Store all credentials — including those used by custom `PythonOperator` functions — in the Airflow connections store (metastore) rather than hardcoding them, fetched via `BaseHook.get_connection(conn_id)` (p326-327, Listing 12.14); for external secret managers, use Airflow's secrets-backend integrations (p327).

5. Pick one consistent configuration mechanism (YAML files, Airflow Variables, environment variables, etc.) across DAGs, following DRY for configuration shared across multiple DAGs (p327-329).

6. Load configuration/credentials inside task functions (worker-scope) rather than in the DAG's top-level definition (scheduler/parsing-scope), to avoid stale-environment mismatches and unnecessary parse-time cost, e.g. moving a `yaml.load(...)` call from module level into a `_fetch_data(config_path, **context)` function body (p329-330, Listings 12.18-12.19).

7. Avoid any long-running or repeatedly-executed computation in the DAG's top-level definition, since Airflow re-parses DAG files at regular intervals; move such computation into a task's callable instead (p330-331, Listings 12.20-12.23).

8. Write factory functions that take configuration and generate a set of tasks or an entire DAG, e.g. `generate_tasks(dataset_name, raw_dir, processed_dir, preprocess_script, output_dir, dag)` returning the first/last task in the chain, called once per data set inside a loop (p332-333, Listings 12.24-12.25); similarly, `generate_dag(...)` can return a full `DAG` object, with multiple generated DAGs assigned unique names via `globals()[...]` (p333-334, Listings 12.26-12.28).

9. Group related generated tasks visually with `TaskGroup(group_name, tooltip=...)` as a context manager wrapping the factory call, collapsing complex substructures in the UI (p335-336, Listing 12.29).

10. Use `PythonOperator.partial(task_id=..., python_callable=..., op_kwargs={...}).expand(op_args=[[v1], [v2], ...])` to dynamically generate one task instance per element of a run-time-determined list, with `partial()` holding constant arguments and `expand()` holding the value(s) to map over (p338-340, Listing 12.31).

11. Chain Dynamic Task Mapping across two tasks by passing an upstream task's `.output` into a downstream task's `.expand(...)`, e.g. `print_rating.expand(op_args=fetch_ratings.output)` (p340, Listing 12.32) — simplified further using the Taskflow API: `print_rating.expand(rating=fetch_ratings())` (p342, Listing 12.33).

12. Apply Dynamic Task Mapping to an entire `@task_group`-decorated group rather than a single task when multiple downstream tasks must be generated per mapped element (p342-343, Listing 12.34).

13. Push data-volume reduction as early as possible in a pipeline (filter/aggregate before joining large data sets) rather than joining first and filtering later, to reduce intermediate data-set size (p345-346, Figure 12.9).

14. Use incremental (time-partitioned) processing for large or growing data sets so each run only processes its own partition, and failures only require rerunning that partition, not the whole data set (p346-347).

15. Cache/persist intermediate task outputs (e.g. to cloud storage) so individual tasks can be rerun without re-executing their upstream dependencies; always retain the rawest ingested copy of data for reprocessing (p347-348).

16. Avoid writing intermediate data to the local filesystem of an Airflow worker, since downstream tasks may run on a different worker with no access to that filesystem; use shared storage (cloud buckets, shared databases) instead (p348-349).

17. Offload heavy computation/filtering to the source or destination system itself (e.g. push filtering into the database query, or run large jobs on a Spark cluster) rather than performing it on the Airflow worker (p349).

18. Create a resource pool (Admin > Pools in the UI, or programmatically) with a fixed number of slots, then assign tasks to it via the `pool` argument, e.g. `PythonOperator(task_id="my_task", pool="my_resource_pool")` (p350, Listing 12.35), to bound concurrent access to a shared resource.

## 5. Trade-offs and limitations

- Generating multiple DAGs from a single file "can be confusing."
(p335)

"this pattern is best used sparingly and only when it provides significant benefits."
(p335) The source recommends one file per DAG as the general pattern.
- Dynamic Task Mapping's traditional (non-Taskflow) syntax "feels a bit clunky, mostly because of the use of XCom" (p342) — mitigated by the Taskflow API for the same functionality.
- Caching intermediate data "may require excessive storage if you have several intermediate versions of large data sets," creating a retention-period trade-off, and adding existence checks for rewritable intermediate data "adds complexity" (p347-348).
- Writing intermediate files to a local worker filesystem breaks downstream task access when tasks run on different workers, a limitation of Airflow's distributed worker model (p348).
- Loading configuration/computation in the global DAG scope adds parsing cost on every scheduler cycle, but the source notes not all cases are equally bad ("You may not mind loading a configuration file from a local filesystem repeatedly, but repeated loading from cloud storage or a database may be less desirable") (p330).
- Writing a custom hook/operator to fetch credentials lazily "may require a bit more work" compared to simply moving the fetch call into the task callable (p331).

## 6. Failure modes and edge cases

- **Repeated expensive parse-time computation**: placing a long-running computation at DAG top level causes Airflow to "execute do_some_long_computation every time the DAG file is loaded, blocking the entire DAG-parsing process until the computation finishes."
(p330)
- **Repeated metastore hits from global-scope credential fetches**: fetching credentials in the DAG's global scope causes "queries repeated every 30 seconds or so (depending on the Airflow config) against your database simply to retrieve these credentials."
(p331)
- **DAG name collisions in factory loops**: generating multiple DAGs in a loop without assigning each a unique global variable name causes "Airflow will see only a single DAG instance: the last one generated by the loop"
(p334) — fixed via the `globals()[...]` assignment pattern.
- **Cross-worker filesystem inaccessibility**: two dependent tasks running on different workers "don't have access to each other's filesystems and therefore can't access each other's files" if intermediate data is written locally rather than to shared storage (p348).
- **Nondeterministic task output**: relying on unordered dict/data-structure iteration, external mutable state, unsynchronized parallel processing, race conditions, or improper exception handling can all silently make a task's output vary between runs of identical input (p344).
- **Schedule-expression ambiguity across instances**: shorthand/cron `schedule` expressions can resolve differently depending on instance-level settings (`AIRFLOW__SCHEDULER__CREATE_CRON_DATA_INTERVALS`, `AIRFLOW__SCHEDULER__CREATE_DELTA_DATA_INTERVALS`) and even differ in default behavior between Airflow 2 and 3 (p336) — mitigated by always using an explicit timetable class.

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: choose factory functions for statically-known repeated DAG/task structures, and Dynamic Task Mapping for structures that depend on run-time data volume, rather than trying to force one mechanism to cover both cases (p337-338).
- **Build** [D]: always fetch credentials and load configuration inside task callables, never at DAG module scope, to avoid both parse-time cost and environment mismatches between the scheduler and worker (p329-331).
- **Maintain** [D]: enforce one consistent DAG-definition style, dependency-notation style, and configuration-storage mechanism per team/codebase to reduce cognitive overhead when reading unfamiliar DAGs (p325-326, p329).
- **RCA** [D]: if reruns of a DAG produce duplicate data or side effects, check for missing idempotency (overwrite-on-rerun) guarantees in the task's output-writing logic, and check for nondeterministic behavior sources (unordered iteration, external state, race conditions) if reruns of identical input produce different results (p344).
- **Optimization** [D]: push filtering/aggregation as early as possible in a data pipeline, prefer incremental over monolithic processing for time-series data, and offload heavy computation to the source/destination system or a dedicated compute cluster rather than the Airflow worker (p345-349).

## 8. How to test/verify these claims

- Reproduce the repeated-metastore-hit failure mode by placing `BaseHook.get_connection(...)` at DAG module scope (Listing 12.22, p331) and monitoring database query logs across scheduler parse cycles, then confirming the query frequency drops after moving the call into a task callable (Listing 12.23, p331-332).
- Reproduce the DAG-name-collision failure mode by generating multiple DAGs in a loop without unique `globals()` keys and confirming only the last-generated DAG appears in the Airflow UI, then confirming all DAGs appear once the `globals()[f"..."]` pattern is applied (p334).
- Verify Dynamic Task Mapping's variable task count by running the `05_dynamic_task_mapping` DAG (p340, Listing 12.32) against API responses with different numbers of reviews and confirming the grid/graph view shows a matching number of mapped task instances (p341, Figures 12.6-12.7).
- Verify resource-pool concurrency limits by assigning several tasks to a pool with N slots and confirming no more than N run concurrently, with additional tasks queued until a slot frees up (p350, Listing 12.35).
- Verify the style/format tooling claims by running Flake8, Black, and Ruff against the exact before/after code in Listings 12.1-12.9 (p322-325) and confirming the reported violations/reformatting match.

## 9. Cross-references

- Chapter 3 (idempotency, atomicity, incremental processing): directly restated and extended in §12.2 and §12.3.2 (p344, p346).
- Chapter 6 (the umbrella ML DAG): reused as the task-groups worked example (p335).
- Chapters 3-4 (scheduling mechanisms): referenced for the explicit-timetable-class recommendation (p336).
- Blog post on functional data engineering by Maxime Beauchemin, cited for further reading on the functional-programming approach to task design (p345).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 12.1–12.12 (UI screenshots, diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full PEP 8 / Google Python Style Guide / Ruff rule reference | The source itself defers to external documentation for these ("we refer you to https://www.pylint.org and https://flake8.pycqa.org," p323); only representative examples are captured here. |
| Full Kubernetes-secrets-backend and Airflow-secrets-backend integration list | The source references Airflow's documentation link for the full list (p327); only the general mechanism is captured. |
