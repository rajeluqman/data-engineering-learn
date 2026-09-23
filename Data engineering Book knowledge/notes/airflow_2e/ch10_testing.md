# Ch.10 — Testing

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 256–286 (31 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**DAG integrity test** [S]: "the first step in testing generally is a DAG integrity test... This test verifies all your DAGs for their integrity (i.e., validating the correctness of the DAG, confirming that the DAG doesn't cycle, the task IDs in the DAG are unique, and so on)."
(p257)

**Unit test vs. integration test** [S]: "Small individual units of work (i.e., single functions) can be tested with unit tests. Although unit tests may validate correct behavior, they don't validate the behavior of a system composed of multiple units. For this purpose, we write integration tests, which validate the behavior of multiple components together."
(p257)

**Mocking** [S]: "Mocking is faking certain operations or objects. We could mock the call to a database that's expected to exist in a production setting but not during testing by tell"
(p267) [D] (source continues "-ing Python to return a certain value instead of making the actual call to the database" across a hyphenated line wrap).

**pytest fixture** [S]: "In pytest, these kinds"
(p272) [D] (source continues "of functions are called fixtures" immediately before a cited URL parenthetical).

**`dag.test()`** [S]: "One way to test entire DAGs is to use the dag.test() method, introduced in Airflow 2.5.0; it allows you to do a DAG test run programmatically."
(p282)

**DTAP environments** [D]: Development/Test/Acceptance/Production — isolated environments used when a local Docker-based emulation of production isn't feasible (e.g. due to security restrictions).

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter covers a layered testing strategy for Airflow — DAG integrity tests, CI/CD wiring, unit tests for individual operators (with and without mocking, with local files, with real Docker-backed external systems), and finally whole-DAG integration tests via `dag.test()` or environment emulation (Whirl, DTAP).

**WHY** [S]: "how do you ensure that the code you've written is valid before deploying it into a production"
(p256) — the source continues "system? As in any software development process, testing your DAGs is a crucial step toward ensuring that they function correctly in both normal situations... and edge cases." [D] (paraphrase of the continuation, avoiding the source's nested scare-quoted "happy").

**WHEN** [D]: run DAG integrity tests on every DAG, every CI run, as the cheapest and broadest safety net (§10.1.1); use mocking when a unit test must isolate an operator from external systems it cannot reach in CI (§10.1.4-10.1.5); use a real Docker-backed dependency (e.g. PostgreSQL container) when the test needs to validate actual interaction logic, not just that a call was made (§10.2); use `dag.test()` or full environment emulation when validating cross-task interactions within a DAG, not just single operators (§10.4).

## 3. Assumptions and prerequisites

- Prerequisite: custom hooks/operators from chapter 9, reused as the subject under test throughout this chapter (p264, "Looking at the custom components demonstrated in chapter 9").
- Assumes `pytest` as the testing framework, explicitly chosen over the standard-library `unittest`: "pytest is one of the most popular third-party frameworks for testing features such as fixtures, which we'll be using in this chapter."
(p257)
- Assumes Docker is installed and its socket is accessible for container-based tests: "make sure that your container environment allows other programs to use the Docker socket. In Docker Desktop, for example, this setting isn't enabled by default."
(p275)
- Assumes mocking targets the *call site* import, not the definition site: "The correct way to mock in Python is to mock the location where the method is being called, not where it's defined."
(p270)

## 4. Mechanism / key steps

1. Write a DAG integrity test that instantiates every DAG file via `DagBag(dag_folder=dag_file, include_examples=False)`, parameterized over all discovered files with `@pytest.mark.parametrize("dag_file", DAG_FILES)`, then inspects `caplog.records` for `ERROR`-level entries and re-raises them (p259-260, Listing 10.3).

2. Structure tests in a `tests/` directory mirroring the project layout, with test files prefixed `test_`, since "pytest scans given directories and searches for files with test_ prefixes or suffixes."
(p258)

3. Wire a CI/CD pipeline (demonstrated with GitHub Actions) that runs static checks (Flake8, Pylint, Black) followed by `pytest tests/`, triggered `on: [push]` (p262-264, Listing 10.9).

4. Unit-test an operator directly by instantiating it and calling `execute()` with an explicit context dict, bypassing the full Airflow runtime: `task = BashOperator(...); result = task.execute(context={})` (p265-266, Listing 10.11).

5. Mock a metastore-backed call with `pytest-mock`'s `mocker.patch.object`, passing the target class, the method name, and a `return_value`, e.g. patching `MovielensHook.get_connection` to return a fixed `Connection` object instead of querying the real metastore (p268, Listing 10.15).

6. Capture the mock object in a variable (e.g. `mock_get = mocker.patch.object(...)`) to assert on call behavior afterward: `mock_get.call_count == 1` and `mock_get.assert_called_with("testconn")` (p269, Listing 10.17).

7. Test filesystem-touching operators using pytest's `tmp_path` fixture to get an auto-cleaned temporary directory, avoiding leftover files after the test: "After the test, the tmp_path and its contents are removed."
(p272)

8. Test operators against a real external system by spinning up a Docker container within the test using `pytest-docker-tools`'s `fetch()` (pulls an image) and `container()` (starts a container) fixtures, mapping a container port to a random free host port by setting its value to `None` in the `ports` dict argument (p274-276, Listings 10.22-10.25).

9. Seed a test database's schema/data by mounting an init script into the container via the `volumes` argument, pointing at `/docker-entrypoint-initdb.d/` for Postgres images (p276-277, Listing 10.25-10.26).

10. Combine container fixtures with mocked upstream calls in a single test: mock the MovieLens API response while running real queries against the Dockerized PostgreSQL, asserting row counts before and after `task.execute()` (p278-279, Listing 10.27).

11. Use IDE breakpoints (or `import pdb; pdb.set_trace()` for command-line debugging) while running a test in debug mode to inspect intermediate state inside an operator's `execute()` method (p279-281, Listings 10.28-10.29).

12. Debug a task running via CLI without registering metastore records: `airflow tasks test [dagid] [taskid] [execution date]` (p281, "airflow tasks test runs the task without registering any records in the metastore").

13. Test an entire DAG (not just one operator) with `dag.test()`, called either from `if __name__ == "__main__":` at the bottom of the DAG file, or from a pytest test importing the DAG object defined in variable style (not context-manager style) and calling `dagtestdag.test(logical_date=...)` (p282-284, Listings 10.29-10.31).

14. When full environment emulation is needed, consider Whirl (Docker-Compose-based simulation of production components) or dedicated DTAP branches/environments when local Docker emulation isn't feasible (e.g. IP-allowlisted external systems) (p285-286).

## 5. Trade-offs and limitations

- `dag.test()` is documented as broken as of the source's writing: "this example doesn't work in Airflow 3.1 as of this writing because the DAG is no longer automatically serialized when .test() is called."
(p283)
- Calling `dag.test()` directly at the bottom of a DAG file "mixes actual logic (i.e., the DAG) with testing logic. If you want to use mocks or assertions to verify the behavior, things could get messy quite quickly."
(p283)
- Mocking all external systems in a DAG-level test avoids external dependencies but requires maintaining "a clear idea and definition of what each of these external systems is expected to return."
(p285) The mock set grows with each additional integration.
- Emulating a full production environment (e.g. with Whirl) "could lead to some complexity in your setup because coordinating multiple dependencies can be tricky" (p285), and "not everything is available as a Docker image" (e.g. Google Cloud Storage) (p285).
- Full DTAP environments "can be cumbersome to set up and manage," leading smaller projects to run with fewer than four (p286).
- Docker-container-based tests add measurable startup latency: "This process takes a couple of seconds, so there will be a small delay in the test suite."
(p279)

## 6. Failure modes and edge cases

- **DAG cycle**: `AirflowDagCycleException: Cycle detected in DAG: 01_dag_cycle. Faulty task: t3` (p262) is raised (and caught by the integrity test) when tasks form a circular dependency, e.g. `t1 >> t2 >> t3 >> t1` (p258, Listing 10.1).
- **Missing required operator argument**: `airflow.exceptions.AirflowException: missing keyword argument 'bash_command'` (p262) when a `BashOperator` is instantiated without its required argument — caught by the same DAG integrity test.
- **Mocking the wrong location**: mocking `BaseHook.get_connection()` where it's *defined* rather than `MovielensHook.get_connection()` where it's *called* silently fails to intercept the call — "intuitively, therefore, we'd probably mock BaseHook.get_connection(). This would be incorrect, however."
(p270)
- **Duplicate/fixed task IDs from a loop**: "A common mistake while generating tasks in a for loop, for example, is using a fixed task ID instead of a dynamically set task ID, which results in each generated task having the same ID."
(p257) Caught by DAG integrity checks.
- **Files-with-no-DAG-objects flagged**: the integrity test's `elif "assumed to contain no DAGs" in record.message` branch fails any `/dags` Python file that doesn't instantiate a DAG object, which may be a false positive for legitimate utility modules stored in the same folder (p260).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: keep a directory with only DAG files (no utility scripts) if adopting a strict DAG integrity test, since files with no DAG objects are treated as failures by the pattern shown (p260).
- **Build** [D]: layer tests from cheap/broad (DAG integrity) to expensive/narrow (Docker-backed integration tests, whole-DAG tests) so CI catches the most common mistakes fastest, consistent with the chapter's own ordering (§10.1 → §10.2 → §10.4).
- **Maintain** [D]: when mocking a hook method, always patch the import path used at the call site, not the base-class definition, to avoid silently non-functional mocks (p270).
- **RCA** [D]: if a unit test with a mocked hook passes but production fails, check whether the mock targeted the correct import location, and whether `mock_get.call_count`/`assert_called_with` assertions were actually checked rather than only the return value (p269-270).
- **Optimization** [D]: prefer mocking over full container emulation for tests that only need to verify call arguments/counts; reserve Docker-backed tests for verifying actual data-transformation correctness against a real system (p273-274, motivating "Testing with Docker containers allows us to use the real methods of hooks without having to mock calls").

## 8. How to test/verify these claims

- Reproduce the DAG cycle failure by running `pytest tests/` against Listing 10.1's cyclic DAG (p258) and confirming the exact `AirflowDagCycleException` text (p262).
- Reproduce the missing-argument failure by instantiating a `BashOperator` without `bash_command` inside a DAG file and running the integrity test (p262, Listing 10.7-10.8).
- Verify the mocking-location claim by attempting to patch `BaseHook.get_connection` instead of `MovielensHook.get_connection` and confirming the test still hits the real (unmocked) code path (p270).
- Verify the Docker-container test flow by running Listing 10.27 (p277-279) end-to-end and confirming `row_count` is `0` before `task.execute()` and `>0` after.
- Verify `dag.test()` behavior against the currently installed Airflow version, given the source's own caveat that it's broken in Airflow 3.1 as of writing (p283) — check the cited GitHub issue for current status before relying on it [U].
- Verify `tmp_path` cleanup by inspecting the filesystem immediately after a test using it completes, confirming the temporary directory no longer exists (p272).

## 9. Cross-references

- [[ch09_extending_airflow_with_custom_operators_and_sensors|Chapter 9]] (custom operators and sensors): `MovielensHook`, `MovielensFetchRatingsOperator`, and related components are the direct subject under test throughout this chapter (p264).
- GitHub issue tracking the `dag.test()` regression in Airflow 3.1, cited at https://github.com/apache/airflow/issues/56657 (p283).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 10.1–10.13 (UI screenshots, debugger screenshots, diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full GitHub Actions YAML (Listing 10.9) | Representative structure and key lines cited; full YAML reproducible from the source PDF directly rather than duplicated verbatim here. |
| Whirl's internal architecture and DTAP branch-strategy specifics (§10.4.2-10.4.3) | The source itself states DTAP implementation "may be very specific to the project and infrastructure, so it's beyond the scope of this book" (p286); only the high-level approach is captured here. |
| PyCharm-specific debugger UI walkthrough (§10.3) | Tool-specific screenshots; the underlying breakpoint/debug-mode concept is captured in prose instead. |
