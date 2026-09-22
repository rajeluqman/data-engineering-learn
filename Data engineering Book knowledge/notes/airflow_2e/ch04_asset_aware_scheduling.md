# Ch.4 — Asset-aware scheduling

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 98–115 (18 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Asset** [S]: "An asset is a virtual reference and can be anything depending on your use case: a data set, a data table, a machine learning model, and so on."
(p100)

An asset "is identified by its Uniform Resource Identifier (URI), which generally reflects the unique location of the asset."
(p100)

**Valid URI/ID forms** [S]: "Although we strongly recommend using a valid URI, the URI is treated as a string ID, and Airflow makes no assumptions about the location or content of the URI itself."
(p100)

Example valid identifiers listed in the source: `s3://example_bucket/example.csv`, `file://tmp/data.csv`, `/my_data.csv`, `my_dataset` (p100).

**Producer DAG / consumer DAG** [S]: "For the producer DAG, the asset is an output of the DAG, meaning that it will generate an asset event whenever it updates the data set."
(p100)

"For the consumer DAG, the asset is an input, which means that Airflow will trigger the DAG automatically"
(p100) — the source continues onto p101 with "whenever the asset is updated" [D] (paraphrase of the continuation, not quoted verbatim due to a page break).

**Asset event** [D]: the record Airflow creates each time a task with an `outlets` reference to an asset finishes successfully; consumer DAGs scheduled on that asset are triggered by this event.

**Metadata** [S]: "Airflow allows you to add metadata to an asset event. This metadata is reflected in the extra field of an event, which is essentially a dictionary of arbitrary values depending on your needs."
(p106)

**`triggering_asset_events`** [S]: "Airflow allows us to access this information using the triggering_asset_events variable in the Airflow context, which provides the collection of the events that triggered our DAG."
(p105)

**`AssetOrTimeSchedule`** [S]: "You can implement this kind of hybrid schedule using the AssetOrTimeSchedule class, which accepts both a time-based timetable and an asset expression."
(p114)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: Asset-aware scheduling is Airflow's event-driven scheduling mode, where a DAG's trigger condition is expressed as a dependency on one or more named assets rather than (or in addition to) a time-based interval.

**WHY** [S]: The chapter motivates this against the alternative of duplicating ingestion logic per team: "The load increases when multiple DAGs request the same data from an API, which can lead to performance issues or extra costs," "If the API endpoints change, the logic would have to be updated in multiple places," and "If teams implement the data retrieval logic differently, they could create data inconsistencies and conflicting business insights."
(p99)

Directly triggering downstream DAGs from the producer is also rejected: "this would create tight coupling between the workflows."

"The producer DAG needs to know about all its consumers, which doesn't scale well because the DAG would have to keep a manually curated list of all the downstream consumers as more teams start using the data set (an error-prone process)."
(p100)

**WHEN** [S]: "Asset-aware scheduling doesn't provide any notion of time; therefore, it's less suitable for DAGs that need to run on a fixed schedule."
(p101)

[D] Use it when downstream consumers should react to data availability rather than wall-clock time; combine it with time-based scheduling (`AssetOrTimeSchedule`, §4.8) when a DAG needs both responsiveness to data and a regular execution cadence (p114).

## 3. Assumptions and prerequisites

- Prerequisite: understanding of time-based scheduling and the `schedule`/`start_date`/`catchup` parameters from chapter 3 [S] (p99, "In chapter 3, we scheduled a DAG to ingest user events from an API at regular time intervals").
- Assumes the producer DAG's task uses `outlets=[...]` on the relevant operator to attach the asset (p102-103).
- Assumes the URI string is used consistently (exact string match) between producer and consumer DAG definitions — the chapter constructs both `Asset(...)` references with the identical URI string in each example (p98-104).
- The `triggering_asset_events.values() | first | first` idiom assumes exactly one asset and one event triggered the run; multi-asset consumption requires selecting per-asset events explicitly (§4.7).

## 4. Mechanism / key steps

1. Define an `Asset` object with a URI string: `events_dataset = Asset("file:///data/events_01")` (p102, Listing 4.1; the URI recurs verbatim on p102-104).

2. Attach the asset as an output of a producer task via the operator's `outlets` argument: `outlets=[events_dataset]` (p102-103, Listing 4.2).

3. Running the producer task successfully causes Airflow to emit an asset event, visible in the Assets tab of the UI (p103).

4. Define a consumer DAG whose `schedule` parameter references the asset directly: `schedule=[events_dataset]` (p104, Listing 4.4) — this replaces a time-based `schedule` entirely, so the consumer DAG has no `logical_date`/`data_interval` by default (p104-105).

5. Because asset-triggered runs have no logical date, retrieve information about the triggering run via `triggering_asset_events` in Jinja templates, e.g. `(triggering_asset_events.values() | first | first).source_dag_run.logical_date` (p105, Listing 4.5).

**Known defect** [S]: "this example doesn't work in Airflow 3 as of this writing because the source_dag_run attribute seems to have been removed accidentally in the switch from Airflow 2 to 3 (see https://github.com/apache/airflow/issues/52932 for details) ... In the meantime, you can use the metadata approach discussed in section 4.5 as a workaround."
(p105)

6. Alternative to relying on `source_dag_run`: attach explicit metadata to the asset event by yielding a `Metadata` object from the producer task: `yield Metadata(events_dataset, extra={"date": logical_date.strftime("%Y-%m-%d")})` (p107, Listing 4.6).

Read the metadata back in the consumer via `.extra.date` (p108, Listing 4.7).

7. Skip emitting an asset event (and thus avoid triggering consumers) by raising `AirflowSkipException()` from the producer task, e.g. when the underlying data path already exists (p108-109, Listing 4.8).

8. Consume multiple assets in one DAG by listing them all in `schedule=[events_dataset_1, events_dataset_2]` (p110, Listing 4.10).

Select each asset's event explicitly with a user-defined macro: `def _get_event(triggering_asset_events, uri): return triggering_asset_events[Asset(uri)][0]`, registered via `user_defined_macros={"get_event": _get_event}` (p111, Listing 4.12).

9. By default, a multi-asset consumer triggers "whenever all input assets had an event since the last time the DAG was run" (p113) — i.e. an implicit AND.

10. Express explicit boolean trigger logic between assets with `&` (AND) and `|` (OR) operators in the `schedule` expression, e.g. `schedule=(asset_1 | (asset_2 & asset_3))` (p114, Listing 4.13).

11. Combine time-based and asset-based triggers with `AssetOrTimeSchedule(timetable=CronTriggerTimetable(...), assets=[...])` (p114, Listing 4.14).

## 5. Trade-offs and limitations

- Asset-aware scheduling removes the tight coupling and duplicated-ingestion problems of time-based multi-team pipelines (p99-100) [D], but loses all built-in time semantics — see the WHEN quote in §2 above (p101).
- The `source_dag_run.logical_date` approach for date propagation is broken on Airflow 3 due to an upstream regression (p105) — the metadata (`extra` field) approach is the more portable pattern going forward [D].
- Metadata fields become an implicit data contract: "It's tempting to see these fields as extra information you provide, but they're an important part of the data contract with your consumers because changes to these fields will potentially break their pipelines."
(p108)
- Multi-asset scheduling does not correlate execution dates across producers: "Airflow doesn't take any scheduling dates from upstream DAGs and the like into account. Airflow triggers your DAG for any combination of events, regardless of the execution dates that they represent. If you want to make sure that your inputs are from the same execution date, you must add this check yourself."
(p113-114)
- The `logical_date` available to a consumer via `source_dag_run` only exists because the specific producer in the example happens to have a time-based schedule: "The logical_date you use to generate the file paths is available only because the producer has a time-based schedule. If this DAG were also triggered on an event or had a manual trigger, it would not contain this information."
(p106)

## 6. Failure modes and edge cases

- **Undefined `logical_date` in event-driven consumer**: attempting to use `{{ logical_date | ds }}` in a schedule-by-asset DAG raises `UndefinedError: 'logical_date' is undefined`, because "event-driven DAGs don't define any date- or interval-related parameters" (p104-105).
- **Chained producer schedule dependency**: per the WARNING on p106, changing the producer's schedule type (e.g., from time-based to event-based) silently breaks any consumer relying on `source_dag_run.logical_date`, since that attribute only exists when the producer itself has a time-based schedule.
- **Airflow-3 regression**: `source_dag_run` attribute missing on `triggering_asset_events` entries as of the book's writing (p105), tracked at the cited GitHub issue — a documented but unresolved defect, not a documentation error.
- **Skipped producer task suppresses downstream triggering**: raising `AirflowSkipException` in the producer intentionally prevents an asset event and therefore prevents triggering consumers — "any downstream DAGs will not be triggered in this case" (p109). If this skip condition is miscalibrated, consumers silently stop receiving new runs.
- **Partial multi-asset trigger sets**: "multiple events coming from one asset won't trigger the consumer until the second asset also has an event" (p113) — if one producer stalls, dependent multi-asset consumers never fire, with no timeout described in the source (p112-113).
- **Over-complex conditional asset expressions**: the source cautions, "You can also combine the operators to form more complex expressions but be careful not to make things too complex."
(p114)

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: model shared data products (event feeds, tables) as named assets with stable URIs so that any number of downstream consumer teams can subscribe without producer-side knowledge of them, directly addressing the manually-curated-consumer-list anti-pattern described in §2 above (p100).
- **Build** [D]: treat metadata `extra` fields as a versioned interface, per the explicit data-contract warning (p108) — changing a field name or semantics is a breaking API change for every consumer DAG.
- **Maintain** [D]: before changing a producer's schedule type, audit consumer DAGs for reliance on `source_dag_run.logical_date`, since this dependency is not visible from the producer DAG's code alone (p106).
- **RCA** [D]: if a consumer DAG unexpectedly stops running, check (a) whether the producer's task is silently skipping via `AirflowSkipException` (p108-109), and (b) for multi-asset consumers, whether all required upstream assets have actually produced an event since the last consumer run (p112-113).
- **Optimization** [D]: for pipelines needing both periodic freshness checks and rapid reaction to upstream changes, `AssetOrTimeSchedule` (p113) avoids running two separate DAGs or building custom trigger logic.

## 8. How to test/verify these claims

- Verify asset-triggering behavior directly in the Airflow UI's Assets tab, which the chapter uses throughout: "This view (figure 4.4) shows our producing DAG together with the data set it creates (left) as well as the list of asset events that was generated (right)."
(p103)
- Reproduce the `UndefinedError: 'logical_date' is undefined` failure by defining a consumer DAG with `schedule=[asset]` and a Jinja template referencing `logical_date`, as shown on p104-105.
- Confirm the skip-based suppression behavior by running a producer DAG twice against the same output path and observing in the UI that the second run is marked skipped and does not trigger the consumer (p109, Figure 4.7).
- Confirm multi-asset AND semantics by enabling only one of two producer DAGs feeding a shared consumer and verifying the consumer does not run until both producers have emitted at least one event since the last consumer run (p112-113, Figures 4.9–4.11).
- Check current upstream status of the `source_dag_run` regression at the GitHub issue cited in the source (p105) before relying on that attribute in an Airflow 3 deployment [U] — not independently verified in this session, only the citation is confirmed present in the source text.

## 9. Cross-references

- Chapter 3 (time-based scheduling): baseline DAG (`06_interval_delta.py`) that this chapter converts into producer/consumer form (p103-104).
- Chapter 5 (templating): referenced for more detail on the `user_defined_macros` / templating mechanism used for `get_event` (p111).
- Chapter 6 (task execution and dependencies): referenced for the mechanics of task skipping via `AirflowSkipException` (p108).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 4.1–4.11 (UI screenshots and diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full DAG file listings (`dags/01a_basic_producer.py`, etc.) | Only the code excerpts explicitly quoted in the chapter's listings are captured; full file contents not printed in source text extracted. |
| GitHub issue #52932 resolution status | Referenced by the source as of its writing; current status not verified in this session [U]. |
