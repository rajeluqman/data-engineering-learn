# Ch.7 — Triggering workflows with external input

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 177–193 (17 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Sensor** [S]: "One way to solve this problem in Airflow is to employ sensors, a special type (subclass) of operators. Sensors continuously poll for certain conditions to be True."
(p179)

**Poking** [S]: "Poking is Airflow's name for running the sensor and checking the sensor condition."
(p180)

**Sensor deadlock** [S]: "This behavior is often referred to as sensor deadlock."
(p185)

**Sensor `mode` (poke vs. reschedule)** [S]: "the sensor class takes a mode argument, which you can set to poke or reschedule. By default, it's set to poke, leading to the blocking behavior: the sensor task occupies a task slot as long as it's running."
(p185)

**Deferrable operator** [S]: "Another way to avoid the dreaded sensor deadlock is to use deferrable operators. These operators can free the workers when they're idling so that they can take care of other tasks."
(p186)

**Triggerer** [S]: "When an operator defers, it hands the job over to the triggerer, which starts handling any necessary polling or waits for the task to complete in an external system."
(p186)

**DAG run `conf`** [D]: a JSON payload passed when triggering a DAG run via CLI or REST API, made available to tasks through the `dag_run` context variable.

**`MessageQueueTrigger`** [D]: an Airflow trigger type that connects an `Asset` to a message-queue topic (e.g. Kafka), causing DAGs scheduled on that asset to run when qualifying messages are published.

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter covers four distinct mechanisms for starting a DAG run in response to something other than a fixed time schedule: sensors (polling), REST API/CLI triggering, dataset-update REST triggering, and message-queue-triggered assets.

**WHY** [S]: motivated by workflows needing to react to "events that occur outside Airflow, such as files being uploaded to a shared drive, developers pushing their code to a repository, and messages being published on a message bus."
(p177)

The specific sensor motivation: fixed-time scheduling of dependent data forces unnecessary waiting — "Supermarket 1 delivered its data at 16:30, and the workflow started processing it at 2:00 but did noth"
(p179) [D] (source continues "-ing for 9.5 hours" across a hyphenated line wrap).

**WHEN** [D]: use sensors when a workflow must wait for an external condition (e.g. file arrival) but no push-based signal exists (§7.1); use `mode="reschedule"` or deferrable operators when many long-running sensors would otherwise exhaust worker/task slots (§7.1.2); use REST API/CLI triggering when a DAG must be started from outside Airflow, e.g. from a CI/CD pipeline (§7.2); use message-queue-triggered assets when near-real-time, event-driven triggering across services or Airflow instances is needed (§7.3).

## 3. Assumptions and prerequisites

- Prerequisite: time-based scheduling (chapter 3) and asset-based scheduling (chapter 4), both referenced as the two prior triggering mechanisms this chapter extends (p177, "In previous chapters, we saw how to trigger pipelines based on time intervals (chapter 3) and asset updates (chapter 4)").
- Assumes an external signal for upload-complete exists or can be established (e.g. a `_SUCCESS` marker file, or a queue message) rather than inferring completion from partial file listings (p181-182).
- Deferrable operators assume a triggerer process is running alongside the scheduler: "make sure that your Airflow setup includes at least one triggerer process along with the sched"
(p186) [D] (source continues "-uler" across a hyphenated line wrap).
- `PythonOperator`/Taskflow Python tasks cannot use the deferral mechanism: "Python and Taskflow API Python operators can't be deferred."
(p186-187)
- The REST API examples assume basic authentication is acceptable only for demonstration; the source explicitly flags this isn't the recommended production approach (p189, "Sending a plain-text username/password is undesirable. Consult the Airflow API authentication documentation for information on other authentication methods").

## 4. Mechanism / key steps

1. Use `FileSensor` to poll for a file's existence: `FileSensor(task_id="wait_for_supermarket_1", filepath="/data/supermarket1/data.csv")` (p179-180, Listing 7.1) — the default poke interval is 60 seconds, configurable via `poke_interval` (p180).

2. Position the DAG's start time at the earliest possible boundary of expected data arrival rather than the latest possible arrival time, so sensors begin polling immediately and downstream processing starts as soon as data is available (p181).

3. For multi-file or partial-upload conditions that plain filename globbing can't safely express, use `PythonSensor` with a custom callable returning `True`/`False`, e.g. checking both `data-*.csv` files and a `_SUCCESS` marker file's existence (p182-183, Listing 7.2).

4. Configure a sensor's `timeout` argument to bound how long it polls before failing; default is seven days (p184, "By default, the sensor timeout is set to seven days").

5. Bound the number of concurrently running tasks per DAG with `max_active_tasks` to limit the blast radius of a sensor deadlock, e.g. `max_active_tasks=50` (p184, Listing 7.3).

6. Switch a sensor's `mode` argument from the default `poke` to `reschedule` so the task releases its slot between polls rather than holding it continuously (p185, Figure 7.9).

7. Use deferrable operator variants (commonly suffixed `Async`, e.g. `FileSensorAsync`) or set a `deferrable` boolean argument to True, which hands polling/waiting off to the triggerer's asyncio event loop instead of blocking a worker slot (p186).

8. Trigger a DAG manually from outside Airflow via the CLI: `airflow dags trigger dag1` (p187, Listing 7.4), optionally with configuration: `airflow dags trigger -c '{"supermarket_id": 1}' dag1` (p187, Listing 7.5).

9. Read the passed configuration inside a task via `context["dag_run"].conf` (p188, Listing 7.6) — note the source's own caution: "The DAG in listing 7.6, however, has no defined schedule; it runs only when triggered."
(p188)

10. Trigger a DAG via the REST API with a POST request to `/api/v1/dags/{dag_id}/dagRuns`, supplying a `conf` payload in the request body (p189, Listing 7.7).

11. Trigger DAGs indirectly by notifying Airflow of a dataset/asset update via a POST request to `datasets/events/` with a `dataset_uri` payload (p190, Listing 7.8).

12. Define a `MessageQueueTrigger` pointed at a message-queue topic (e.g. Kafka) with an `apply_function` used to filter which messages should cause a trigger: `MessageQueueTrigger(queue="kafka://kafka:9092/events", apply_function="custom.kafka_util.apply_function")` (p191, Listing 7.9-7.10).

13. Attach the trigger to an `Asset` via an `AssetWatcher`, then schedule a DAG on that asset: `asset = Asset("kafka_queue_asset", watchers=[AssetWatcher(name="kafka_watcher", trigger=trigger)])`, with `schedule=[asset]` on the DAG (p192, Listing 7.11-7.12).

## 5. Trade-offs and limitations

- A naive fixed-time schedule set late enough to guarantee all upstream data has arrived produces large unnecessary waiting time, e.g. "Supermarket 1 delivered its data at 16:30, and the workflow started processing it at 2:00 but did noth" (p179) [D] (source continues "-ing for 9.5 hours" across a hyphenated line wrap).
- Sensor polling introduces continuous load on both Airflow and the external system: "By polling some external system continuously, sensors introduce load on both Airflow and on the external system."
(p181)
- Default `mode=poke` sensors occupy a worker slot for their entire run, even between pokes, unlike `mode=reschedule` which "occupies a slot only while it's doing actual work"
(p185).
- Deferrable operators require an additional Airflow component: "make sure that your Airflow setup includes at least one triggerer process along with the sched"
(p186) [D] (source continues "-uler" across a hyphenated line wrap); the triggerer itself "is an optional component for Airflow in general but a requirement for using deferrable operators."
(p186)
- Triggering via REST API/CLI conflicts with time-based scheduling in the same DAG: a DAG relying on `dag_run.conf` "won't be possible to run on a schedule because a scheduled run doesn't provide any DAG run conf."
(p188)
- Message-queue-based triggering "requires additional infrastructure in the form of a message queue" (p192-193) compared to file-based sensors.
- Filename globbing for partial-upload detection is limited: "Although globbing (similar to"
(p181) — the source continues on p182: "regex but more limited in functionality) would be able to match multiple patterns with a complex pattern, a clearer, more understandable approach is to implement the two checks with the PythonSensor." [D] (paraphrase of the continuation, not quoted verbatim due to a page break).

## 6. Failure modes and edge cases

- **Premature trigger on partial upload**: an unqualified `FileSensor` wildcard match on `data-*.csv` "would return True, and the workflow would continue to the copy_to_raw task, which is undesirable because only part of the data for a given interval would have been processed" if the supermarket is still uploading (p181-182).
- **Sensor timeout failure**: an `AirflowSensorTimeout` exception is raised, e.g. "Sensor has timed out" with the run duration exceeding the configured timeout (p183, error log excerpt) when polled condition never becomes True within the configured window.
- **Sensor deadlock via snowball effect**: with a daily schedule and a seven-day default timeout, failed upstream deliveries accumulate polling sensors across days until "two new tasks can't run, and any other task trying to run is blocked" (p185) — bounded to the DAG if `max_active_tasks` is the limiting factor, or global if the Airflow-wide task limit is reached: "When the global Airflow limit of maximum tasks is reached, however, the entire system is stalled, which is obviously undesirable."
(p185)
- **`overload from too-aggressive poke_interval`**: "Be careful setting this interval to a low value, which may overload"
(p180)
- **Missing `conf` on scheduled runs**: a DAG designed around `dag_run.conf` will break if accidentally given a schedule, since scheduled (non-manually-triggered) runs provide no `conf` payload (p188).
- **Delayed message-triggered runs**: "There may be some delay in starting the DAG run because the Kafka consumer has a fixed (configurable) interval at which it fetches new messages."
(p192)

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: prefer a completion-marker file (or message) over inferring completion from partial file listings, since globbing alone cannot safely distinguish an in-progress upload from a finished one (p181-182).
- **Build** [D]: set DAG start times to the earliest plausible data-arrival boundary rather than the latest, so sensor-based DAGs process data as soon as it's available instead of waiting for a fixed late cutoff (p181).
- **Maintain** [D]: audit long-running sensor-heavy DAGs for `mode` and `timeout` settings; a default seven-day timeout combined with a daily schedule is the specific precondition for the documented snowball/deadlock failure (p184-185).
- **RCA** [D]: if many tasks across a DAG or Airflow instance are stuck in a running/polling state, check for sensor deadlock caused by unmet conditions accumulating across scheduled runs (p184-185) before suspecting infrastructure issues.
- **Optimization** [D]: convert high-volume, long-idle sensors to `mode="reschedule"` or deferrable operators to free worker slots during idle poll gaps, rather than increasing `max_active_tasks` as the first response to slot exhaustion (p185-186).

## 8. How to test/verify these claims

- Reproduce the sensor-timeout failure by setting a short `timeout` (e.g. `timedelta(minutes=5)` as in Listing 7.2, p183) against a file path that never appears, and confirm the `AirflowSensorTimeout` error text matches p183.
- Reproduce the sensor-deadlock snowball effect by scheduling a DAG daily with sensors that never succeed and observing task-slot occupancy grow day over day, as tabulated on p184-185.
- Verify `mode="reschedule"` frees the slot between pokes by comparing task-slot occupancy under `mode="poke"` vs. `mode="reschedule"` for the same sensor configuration (p185, Figure 7.9).
- Verify CLI/REST triggering by running `airflow dags trigger dag1` (p187, Listing 7.4) and confirming the resulting `dag_run_id` is prefixed `manual__`.
- Verify `dag_run.conf` propagation by running Listing 7.6 (p188) with the CLI's `-c` flag and confirming the printed `context["dag_run"].conf` matches the supplied JSON.
- Verify message-queue triggering by producing a Kafka message via the CLI command shown on p192 and confirming the corresponding DAG run starts (subject to the Kafka consumer's fetch interval).

## 9. Cross-references

- Chapter 3 (time-based scheduling) and Chapter 4 (asset-aware scheduling): the two prior triggering mechanisms this chapter builds on (p177).
- Chapter 9 (deferrable operators, referenced as a future chapter): "Chapter 9 discusses deferrable operators in depth and shows you how to create a custom deferrable operator."
(p186)
- Chapter 15 (Airflow production operation, referenced as a future chapter): "You can also control the number of concurrent tasks with several configuration options on the global Airflow level, as discussed in chapter 15."
(p185)

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 7.1–7.12 (timelines, UI screenshots, DAG diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full REST API JSON response bodies (Listings 7.7-7.8) | Representative fields cited; full raw JSON reproducible from the source PDF directly rather than duplicated verbatim here. |
| Kafka-specific CLI/produce mechanics beyond the trigger example | Kafka operational detail tangential to the Airflow-triggering mechanism that is this chapter's subject. |
