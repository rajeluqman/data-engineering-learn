# Ch.13 — Project: Finding the fastest way to get around NYC

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 352–372 (21 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Use case** [S]: "In this section, we try to answer this question:"
(p353) [D] (source poses, in scare quotes, the question of which transportation method is fastest from point A to point B in NYC right now).

**PandasOperator (custom operator pattern)** [D]: a single reusable `BaseOperator` subclass that composes three interchangeable callables — `input_callable`, `transform_callable`, `output_callable` — all communicating via the pandas DataFrame as a common interface, avoiding a separate operator per transformation.

**Raw/processed/export data staging** [S]: "Unedited data, for example, is stored in raw, derived and transformed data is stored in processed, and data sets ready for transfer are stored in export."
(p369)

**EAFP idiom** [S]: "we could apply Python's EAFP (easier to ask for forgiveness than permission) idiom, trying first and catching exceptions instead of checking every possible condition to skip when encountering a ValueError."
(p362)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter is a worked end-to-end Airflow project — extracting Citi Bike and Yellow Cab NYC transportation data from two differently-shaped APIs, staging it through raw/processed storage layers, generalizing pandas-based transformations into a single reusable operator, and writing idempotent results to PostgreSQL.

**WHY** [D]: to consolidate the book's individual techniques (custom operators, hooks, idempotency, data staging) into one realistic multi-source pipeline, since "It's time for you to make good use of all that knowledge and see how to apply your new skills to a real-life use case."
(p352)

**WHEN** [D]: apply the PandasOperator-style callable-composition pattern (§13.4) when multiple tasks share the same processing shape (read → transform → write) but differ only in the specific functions used; apply raw/processed staging (§13.5) whenever source data can't be re-fetched identically later (e.g. a REST API reflecting only current state); apply execution-date-tagged delete-then-insert (§13.6) when writing to a database table that doesn't naturally deduplicate on rerun.

## 3. Assumptions and prerequisites

- Prerequisite: hooks, custom operators, and connections from chapters 8-9, directly reused (`S3Hook`, `BaseHook.get_connection`, custom `BaseOperator` subclasses) throughout this chapter (p329-330, p335-336).
- Assumes a reproducible local environment via Docker Compose, exposing mock Citi Bike/Yellow Cab APIs, MinIO (S3-compatible storage), and PostgreSQL databases (p353-354, Listing 13.1).
- Assumes the reader accepts the simplifying assumption of mapping Citi Bike station coordinates to Yellow Cab taxi zones, at the cost of some accuracy: "To simplify our use case but sacrifice a little accuracy, we'll map the latitude and longitude of Citi Bike stations to taxi zones"
(p358).
- Assumes both data sources are queried at the same 15-minute interval to allow parallel processing within one DAG: "This configuration allows us to make two requests at the same interval, in the same DAG, and process all data in parallel."
(p359)

## 4. Mechanism / key steps

1. Schedule the DAG at a fixed short interval matching both data sources' granularity: `schedule="*/15 * * * *"` (p359, Listing 13.5).

2. Download from a REST API requiring custom HTTP+auth+S3-write logic (no built-in operator fits) using a `PythonOperator` wrapping `requests` and `S3Hook`: fetch via `BaseHook.get_connection("citibike")` for credentials, then `s3_hook.load_string(...)` to persist the JSON response to MinIO, with the object key templated using `data_interval_start` (p359-360, Listing 13.6).

3. Configure a custom S3-compatible endpoint (MinIO) via the connection's `extra` field rather than its host, since "we can provide the hostname via a key endpoint_url in the extras" — a hook-implementation detail not obvious from the connection form's visible fields (p360, Figure 13.4).

4. Download from a file-listing-based source (no fixed filenames known ahead of time) by first requesting the index/listing endpoint, then iterating and fetching each file individually before uploading each to MinIO (p361-362, Listing 13.9).

5. Make the upload idempotent by catching the storage backend's "already exists" failure with Python's EAFP idiom: wrap `s3_hook.load_string(...)` in `try/except ValueError` and treat an existing key as a no-op rather than a failure (p362-363, Listing 13.10).

6. Generalize repeated pandas-based transform tasks into a single `PandasOperator` accepting `input_callable`, `transform_callable` (optional), and `output_callable`, all communicating via a pandas DataFrame: `execute()` calls `input_callable(**input_kwargs)`, optionally `transform_callable(df, **transform_kwargs)`, then `output_callable(df, **output_kwargs)` (p365-366, Listing 13.11).

7. Register the callable-configuration kwargs dicts (`_input_callable_kwargs`, `_transform_callable_kwargs`, `_output_callable_kwargs`) as `template_fields` so their values (e.g. paths built from `data_interval_start`) can be Jinja-templated per task instance (p365, Listing 13.11).

8. Instantiate `PandasOperator` per data set by swapping only the callables/kwargs, e.g. `input_callable=get_minio_object` with `pandas_read_callable=pd.read_csv` for taxi data vs. a JSON-oriented equivalent for Citi Bike, and `pandas_write_callable=pd.DataFrame.to_parquet` for output (p366-367, Listing 13.12) — changing input format later requires only swapping the passed-in callable, not rewriting logic (p368).

9. Organize storage into lifecycle-based stages — `raw` (unedited ingested copies), `processed` (transformed data), and optionally `export` — since "we want to make our pipeline reproducible" and raw copies of non-replayable API responses must be preserved (p369, Figure 13.8).

10. Make the processed-data write step idempotent by enabling overwrite-on-rerun for destination files: "we should set a flag to overwrite destination files. This ensures that rerunning a task won't fail due to an existing output path."
(p370)

11. Make the database-write step idempotent by tagging each row with the Airflow execution date column and wrapping a delete-then-insert in a single transaction: `DELETE FROM ... WHERE airflow_execution_date = '{data_interval_start}'` followed by `df.to_sql(..., if_exists="append")`, both inside `engine.begin()` (p370-371, Listing 13.17) — ensuring reruns replace rather than duplicate that execution's rows.

## 5. Trade-offs and limitations

- Mapping Citi Bike coordinates onto Yellow Cab zones loses intra-zone distance variation: "Ride A is obviously shorter than ride B. By averaging all ride times from Greenwich Village South to the East Village, for example, we lose such information."
(p358)
- `SimpleHttpOperator` is unsuitable for this use case because "it turns out to be unsuitable for our use case: the SimpleHttpOperator simply makes an HTTP request but provides no functionality for storing the response anywhere." forcing a custom `PythonOperator` implementation (p359).
- Running pandas transformations via `PythonOperator` executes on the same machine as Airflow, unlike a Spark job dispatched to a separate cluster: "If a pandas job is hitting the limits of the machine's resources, it could theoretically take down the machine and Airflow with it."
(p364)
- Storing intermediate raw/processed data trades storage cost and pipeline complexity for reproducibility and shareability, versus a single in-memory extract-transform-load function that would be faster but not reproducible or reusable by other consumers (p368-369).
- More fine-grained data-stage separations (Raw > Preprocessed > Enriched > Processed > Export) exist in practice; "No one structure suits all; your project and the project's requirements determine the best way to structure the movement of data."
(p370)

## 6. Failure modes and edge cases

- **Non-idempotent object storage write**: `s3_hook.load_string()` "isn't an idempotent operation."
(p362)

"If a file with the same name already exists, the operation fails:"
(p362) Raises `ValueError: The key {key} already exists.` — fixed via the EAFP try/except pattern (p362-363).
- **Duplicate database rows on rerun**: without an execution-date tag and delete-before-insert, rerunning a task that appends to a database table "could result in duplicate rows that might pollute the results" (p370).
- **API result-size limits unaccounted for**: "APIs often limit compute power and"
(p358) [D] (source continues "data-transfer size; an API might limit the number of results to 1,000, for example" across a page break), requiring the caller to know approximate data volume and poll frequently enough to avoid exceeding the cap.
- **Non-obvious custom-endpoint configuration**: setting a non-default S3-compatible hostname (e.g. MinIO) is not available via the connection's visible host field; it must be set via the `extra` field's `endpoint_url` key, discoverable only by reading the hook's source (p360, "we have to read a hook's implementation to understand its inner workings").

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: when no built-in operator matches a specific integration shape (e.g. HTTP-to-S3 with authentication), implement it once as a `PythonOperator` callable, and generalize to a full custom operator (or a callable-composition operator like `PandasOperator`) if the pattern repeats across multiple tasks (p359, p365).
- **Build** [D]: template the callable-configuration kwargs (not just top-level operator arguments) via `template_fields` when building a generic multi-callable operator, so per-run values (paths, dates) still render correctly (p365).
- **Maintain** [D]: keep raw ingested copies of any data pulled from a non-replayable external system (APIs reflecting only current state), since reprocessing after a bug fix or schema change is otherwise impossible (p369).
- **RCA** [D]: if a rerun of a pipeline produces duplicate database rows, check whether the write step tags rows with a unique per-run identifier (e.g. execution date) and performs a delete-then-insert rather than a bare append (p370-371).
- **Optimization** [D]: keep pandas-based (single-machine) transformations only for data that fits comfortably on the Airflow worker; offload larger transformations to Spark (via `SparkSubmitOperator` or a `BashOperator` spark-submit call) or a containerized job (`KubernetesPodOperator`, AWS ECS `ECSOperator`) to avoid resource contention with Airflow itself (p363-365).

## 8. How to test/verify these claims

- Reproduce the non-idempotent-upload failure by running the taxi-download task twice against the same source file and confirming the exact `ValueError: The key ... already exists.` text (p362), then confirming the EAFP-wrapped version (Listing 13.10, p362-363) completes without error on rerun.
- Verify the `PandasOperator`'s callable-swapping claim by running it once with `pandas_read_callable=pd.read_csv` and once with `pd.read_parquet` against equivalent data, confirming only the operator's kwargs change, not its code (p368).
- Verify idempotent database writes by running the DAG twice for the same `data_interval_start` and confirming the row count in `citi_bike_rides` for that execution date does not double (p370-371, Listing 13.17).
- Verify the MinIO custom-endpoint configuration by connecting the `S3Hook` with `endpoint_url` set in `extra` and confirming successful uploads to the local MinIO instance rather than AWS S3 (p360).

## 9. Cross-references

- Chapters 8-9 (communicating with external systems; custom operators/hooks): `S3Hook`, `BaseHook.get_connection`, and custom-`BaseOperator` patterns are directly reused throughout (p359-360, p365-366).
- Blog post by Todd Schneider analyzing NYC transportation speed via Monte Carlo simulation, cited as the inspiration for this use case (p352).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 13.1–13.9 (architecture diagrams, screenshots, maps, web app UI) | Visual content; described narratively where relevant, not reproduced. |
| Full Docker Compose service list and port/credential table (§13.1) | Environment scaffolding for reproducing the exercise; representative services cited, full table reproducible from the source PDF directly. |
| Full `transform_taxi_data`/Citi Bike-equivalent transformation logic | Domain-specific pandas transformation detail tangential to the operator-generalization pattern that is this chapter's main teaching point; core `execute()` composition mechanism is fully captured instead. |
