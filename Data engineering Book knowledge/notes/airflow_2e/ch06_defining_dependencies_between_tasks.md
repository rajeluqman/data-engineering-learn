# Ch.6 — Defining dependencies between tasks

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 141–174 (34 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Linear dependency** [D]: a chain of tasks executed strictly one after another, expressed with the bitwise right-shift operator: "Airflow allows us to indicate this type of relationship between two tasks by creating a dependency between them, using the bitwise right shift operator (>>)."
(p142)

**Fan-out / fan-in** [S]: "This type of structure, in which one task has a dependency on multiple upstream tasks, is often referred to as a fan-in structure because it consists of multiple upstream tasks that fan into a single downstream task."
(p144)

**Trigger rule** [S]: "Trigger rules are essentially the conditions that Airflow applies to tasks to determine whether they're ready to execute, based on the execution status of their"
(p158)

**`all_success` (default trigger rule)** [S]: "Airflow's default trigger rule is all_success, which states that all a task's dependencies must complete successfully before the task itself can execute."
(p158)

**Propagation** [S]: "This type of behavior, in which the result of upstream tasks affects downstream tasks, is referred to as propagation."
(p159)

**XCom** [S]: "Airflow also allows you to share small pieces of data between tasks using XComs. (XCom is an abbreviation of cross-communication.) XComs essentially enable you to exchange messages between tasks, enabling some level of shared state."
(p162)

**Taskflow API** [S]: "Airflow has a decorator-based API for defining Python tasks and their dependencies: the Taskflow API."
(p166)

**BranchPythonOperator** [S]: "callables passed to the BranchPythonOperator are expected to return the ID of a downstream task as a result of their computation."
(p148-149)

**LatestOnlyOperator** [S]: "Airflow provides the built-in LatestOnlyOperator class, which effectively performs the same job as our custom-built implementation based on the PythonOperator."
(p157)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter covers the full mechanism for controlling task execution order and conditional flow in Airflow — dependency operators (`>>`), branching, conditional (skip-based) tasks, trigger rules, and two ways of passing data between tasks (XCom, Taskflow API).

**WHY** [S]: explicit dependency declaration "clearly defines the implicit ordering of our tasks. This enables Airflow to schedule tasks only when their dependencies have been met, which is more robust than, say, scheduling individual tasks one after another using cron and hoping that preceding tasks will be complete by the time the next task starts."
(p142)

**WHEN** [D]: use fan-out/fan-in for parallel independent branches that must later converge (§6.1.2); use branching (§6.2) when a DAG must choose between mutually exclusive downstream paths at run time; use conditional tasks / `LatestOnlyOperator` (§6.3) when a task should run only under a specific run-time condition (e.g. most-recent run only); adjust trigger rules (§6.4) whenever branching or conditional skipping would otherwise incorrectly propagate a skip/failure downstream; use XCom (§6.5) for small values passed between tasks, and the Taskflow API (§6.6) to simplify Python-task chains that would otherwise require manual XCom push/pull.

## 3. Assumptions and prerequisites

- Prerequisite: basic DAG construction and the rocket-launch example from chapter 2, reused here as the linear-dependency example (p142, "Our rocket-launch picture-fetching DAG from chapter 2").
- Prerequisite: the umbrella ML use case from chapter 1, reused throughout §6.1–6.5 (p143).
- Prerequisite: atomicity concepts from chapter 3, referenced when discussing XCom anti-patterns (p165, "Chapter 3 discusses atomicity in detail").
- Assumes the default trigger rule (`all_success`) unless explicitly overridden — branching and conditional-skip patterns rely on this default behavior to explain why naive branching breaks downstream tasks (p151).
- Assumes XCom values are serializable: "This means that some Python types, such as lambdas and many multiprocessing-related classes, generally can't be stored in an XCom (though you probably shouldn't do that anyway)."
(p165)

## 4. Mechanism / key steps

1. Define linear dependencies with the right-shift operator: `download_launches >> get_pictures >> notify` (p143, Listing 6.2).

2. Define fan-out dependencies (one task to many): `start >> [fetch_weather, fetch_sales]` (p144, Listing 6.4).

3. Define fan-in dependencies (many tasks to one): `[clean_weather, clean_sales] >> join_datasets` (p144, Listing 6.5).

4. Implement branching within a single task by checking a run-time condition inside the callable, e.g. `if context["data_interval_start"] < ERP_CHANGE_DATE: _clean_sales_old(**context) else: _clean_sales_new(**context)` (p146, Listing 6.7) — noted as harder to observe from the UI (§6.2.1, p147).

5. Implement branching within the DAG structure using `BranchPythonOperator`, whose callable returns the task ID (or list of IDs) to execute next: `pick_erp_system >> [fetch_sales_old, fetch_sales_new]` (p149, Listing 6.11).

6. When branching skips tasks, fix downstream skip-propagation by changing the join task's trigger rule to `none_failed`: `EmptyOperator(task_id="join_datasets", trigger_rule="none_failed")` (p151-152, Listing 6.14) — or, more cleanly, insert a dedicated empty join task carrying that trigger rule so unrelated tasks don't need their rule changed (p152-153, Listing 6.15).

7. Implement a run-time condition within a task by raising `AirflowSkipException` to skip the task and its downstream dependents, e.g. a `_latest_only` function using `dag.timetable.next_dagrun_info(...)` to determine whether the current run is the most recent (p153-156, Listing 6.16-6.18).

8. Prefer the built-in `LatestOnlyOperator` over a hand-rolled latest-only check, since "running tasks for only the most recent DAG run is a common use case" (p157): `train_model >> latest_only >> deploy_model` (p157, Listing 6.19).

9. Set an explicit `trigger_rule` argument on any operator to control exactly when it executes relative to its parents' states, per Table 6.1's full enumeration (`all_success`, `all_failed`, `all_done`, `all_done_setup_success`, `all_skipped`, `one_failed`, `one_success`, `one_done`, `none_failed`, `none_failed_min_one_success`, `none_skipped`, `always`) (p160-161).

10. Push data explicitly between tasks using `xcom_push` on the task instance (p161, Listing 6.20).

Retrieve it with `xcom_pull` on the task instance (p162, Listing 6.21).

11. Push XCom values implicitly by returning a value from a `PythonOperator` callable, registered under the default key `return_value` (p164, Listing 6.23) — many operators do this automatically via `do_xcom_push`, which "by default is True in the BaseOperator" (p164).

12. Reference XCom values inside Jinja templates via the `templates_dict` argument (p164, Listing 6.22).

13. Define a custom XCom backend by subclassing `BaseXCom` and implementing `serialize_value`/`deserialize_value` static methods, then configuring Airflow with the `xcom_backend` parameter (p166, Listing 6.24) — useful for storing larger values in external object storage rather than the metastore (p166).

14. Clean up stale XCom values with the `airflow db clean` command; for custom backends, "you have to implement monitoring and cleaning yourself" (p166).

15. Define Python tasks with the Taskflow API using the `@task` decorator instead of `PythonOperator` + manual XCom calls: `@task def train_model(): ... return model_id` and `@task def deploy_model(model_id): ...`, connected via `model_id = train_model(); deploy_model(model_id)` (p167-169, Listings 6.26-6.28).

16. Define an entire DAG with the Taskflow API using the `@dag` decorator on a Python function that internally defines `@task`-decorated functions, then explicitly calling the decorated function at module level so Airflow registers the DAG: `taskflow_api_decorator()` (p170, Listing 6.29) — "it's important to call the decorated function at the end of the script to allow Airflow to pick it up as a new DAG."
(p170)

17. Mix Taskflow-style tasks with regular operator-based tasks in the same DAG when needed, e.g. connecting an `EmptyOperator`-based `join_datasets` to a Taskflow-returned `model_id` via `join_datasets >> model_id` (p171-172, Listing 6.30).

## 5. Trade-offs and limitations

- Branching within a task (rather than within the DAG) is "difficult to see which code branch Airflow is using during a specific DAG run" from the UI alone (p147).
- Branching-within-task approaches "prevents you from using function" (p147) [D] (source continues "-ality provided by more specialized Airflow operators" across a hyphenated line wrap) — since only general operators like `PythonOperator` can express the internal condition.
- Naive fan-in after a branch causes unintended skips because "by default, Airflow requires all tasks upstream of a given task to complete successfully before that task itself can be executed" (p149-150) — the default `all_success` trigger rule propagates skips.
- Adding an explicit join task after a branch (rather than adjusting `join_datasets`'s own trigger rule) avoids "three edges" convergence complexity and keeps unrelated tasks' trigger rules unchanged (p152).
- XComs introduce hidden/implicit dependencies: "they add a hidden dependency between tasks because the pulling task has an implicit dependency on the task pushing the required value."
(p165)

"this dependency isn't visible in the DAG, and Airflow won't take it into account when scheduling the tasks"
(p165)
- XComs can break operator atomicity, illustrated by an API-token example where "the token expired after a couple of hours, so any rerun of the second task failed" (p165).
- XCom values are size-limited by backend: SQLite 2 GB, PostgreSQL 1 GB, MySQL 64 KB (p165).
- The Taskflow API "it's available to a limited number of opera" (p171) [D] (source continues "-tors" across a hyphenated line wrap), so DAGs mixing Taskflow and non-Taskflow operators can become confusing due to differing dependency syntax.
- Sharing XCom values across different DAGs or execution dates is explicitly discouraged: "we strongly rec"
(p163) — the source continues "ommend against doing this unless you have an extremely good reason." [D] (paraphrase of the continuation, not quoted verbatim due to a hyphenated line wrap).

## 6. Failure modes and edge cases

- **Unwanted downstream skip after branching**: connecting both branches of a `BranchPythonOperator` directly to a fan-in task with the default `all_success` rule causes Airflow to skip the fan-in task and everything downstream of it, because only one branch actually executes (p149-150, Figure 6.8, "These tasks are wrongly skipped").
- **Upstream failure propagation**: "the downstream clean_sales task can no longer be executed because it requires fetch_sales to be successful... assigned the state upstream_failed" (p159) — a single upstream failure halts the entire downstream chain under the default trigger rule.
- **`none_failed` still propagates real failures**: "the rule doesn't propagate skips, but it still propagates"
(p160) — the source continues on p161: "failures, meaning that any failures in the fetch/clean tasks will still halt the execution of downstream tasks." [D] (paraphrase of the continuation, not quoted verbatim due to a page break).
- **Backfilling side effects with conditional deployment logic**: without a latest-only guard, backfilling triggers `train_model`/`deploy_model` for every historical interval, "deploying many nonrelevant instances of our model" (p153).
- **Serialization failure for unsupported XCom types**: lambdas and multiprocessing-related classes generally can't be stored as XCom values (p163).
- **XCom database overflow**: "be careful not to overflow the database storage by storing huge values or a lot of Xcom values" — mitigated with `airflow db clean` (p166).
- **Forgetting to call a `@dag`-decorated function**: a Taskflow-style DAG definition function must be explicitly invoked at the end of the script, or Airflow will not register the DAG (p172, "Don't forget to call the decorated function").

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: prefer branching-within-the-DAG (`BranchPythonOperator`) over branching-within-a-task whenever the two code paths diverge significantly, since it keeps the executed path visible in the UI (p147, Figure 6.5-6.6 contrast).
- **Build** [D]: when adding a fan-in join after a branch, add a dedicated empty join task with the corrected trigger rule rather than changing the trigger rule of the "real" downstream task, to keep responsibilities separated (p152-153).
- **Maintain** [D]: document any XCom-based data dependency explicitly in code comments or design docs, since Airflow's scheduler has no visibility into it and won't enforce correct task ordering on its own (p163).
- **RCA** [D]: when a task unexpectedly shows `upstream_failed` or is skipped, check (a) whether an upstream task failed or was skipped, and (b) whether the task's trigger rule is the default `all_success`, which propagates both conditions (p158-159).
- **Optimization** [D]: use the Taskflow API for Python-heavy DAGs to eliminate manual XCom push/pull boilerplate (p170, "reducing boilerplate code").

Fall back to the regular operator API for any operator not covered by table 6.2's Taskflow decorators (p171).

## 8. How to test/verify these claims

- Reproduce the wrongly-skipped fan-in behavior by building the branch-then-join DAG from Listing 6.9-6.13 (p148-150) and confirming in the UI that `join_datasets` and its downstream tasks show a skipped state (p150, Figure 6.8).
- Confirm the `none_failed` fix by applying Listing 6.14/6.15 (p151-153) and rerunning the same DAG, verifying `join_datasets` now executes (p151, Figure 6.9).
- Reproduce the latest-only conditional behavior by running Listing 6.16-6.18 (p153-156) across several backfilled dates and confirming only the most recent run's `deploy_model` task executes, per Figure 6.13 (p157).
- Verify XCom push/pull directly via the Airflow UI's Browse > XComs page after running Listing 6.20-6.21 (p161-162, Figure 6.16).
- Verify the Taskflow API's implicit dependency wiring by running Listing 6.26-6.28 (p167-169) and confirming the resulting graph view shows a `train_model >> deploy_model` edge (p169, Figure 6.18).
- Verify trigger-rule semantics directly against Table 6.1 (p160-161) by constructing minimal DAGs for each rule and injecting forced failures/skips to observe execution outcomes.

## 9. Cross-references

- Chapter 1 (umbrella ML use case) and Chapter 2 (rocket-launch DAG): source examples reused throughout this chapter (p142-143).
- Chapter 3 (atomicity and idempotency): referenced for the XCom-breaking-atomicity discussion (p165).
- Later chapters (unspecified in the extracted range): Table 6.2 notes several Taskflow decorators are covered via "delve into most of them in subsequent chapters" (p168).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 6.1–6.19 (DAG diagrams, UI screenshots, graph/tree views) | Visual content; described narratively where relevant, not reproduced. |
| Full Table 6.1 (trigger rules) and Table 6.2 (Taskflow decorators) | Representative entries quoted/cited; complete tables (p160-161, p167) reproducible from the source PDF directly rather than duplicated verbatim here. |
| `@task.pyspark`, `@task.kubernetes`, and other advanced Taskflow decorators | Named in Table 6.2 but explicitly deferred by the source itself to later chapters (p167, "We'll delve into most of them in subsequent chapters"); not elaborated here. |
