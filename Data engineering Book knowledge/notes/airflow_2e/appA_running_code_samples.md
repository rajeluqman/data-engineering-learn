# Appendix A — Running code samples

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 500–503 (4 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: appendix`

## 1. Concepts and definitions

**Chapter-directory code structure** [S]: "The code is organized by chapter, and each chapter is structured the same way. The top level of the repository consists of several chapter directories (numbered 01–17), which contain self-contained code examples for the corresponding chapters."
(p500)

**`compose.override.yaml`** [S]: "compose.override.yaml—File with chapter-specific overrides and extra"
(p500).

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this appendix documents the accompanying GitHub code repository's per-chapter directory layout and the Docker Compose commands used to start, inspect, and tear down each chapter's runnable example environment.

**WHY** [S]: "The repository holds the code used in this book, along with easy-to-execute Docker environments that enable you to run all the examples yourself."
(p500)

**WHEN** [D]: consult this appendix whenever setting up, debugging, or cleaning up any chapter's example environment throughout the book.

## 3. Assumptions and prerequisites

- Assumes Docker and Docker Compose are installed and available on the reader's machine (implicit throughout, e.g. `docker compose up --build`, p501).
- Assumes sufficient local resources for more complex chapters: "In our case, 4 CPUs, 16 GB of memory, and 80 GB of disk space worked for all examples. The examples in early chapters, which are less complex, require fewer resources."
(p502)

## 4. Mechanism / key steps

1. Each chapter directory contains a standard set of files: `dags/` (DAG files), `compose.yaml` (standard Airflow setup), `compose.override.yaml` (chapter-specific overrides/extra services), `.env` (chapter-specific environment variables), and `README.md` (chapter-specific run instructions) (p500).

2. Start a chapter's environment from within its directory with `docker compose up --build`, which starts the API server, scheduler, DAG processor, triggerer, workers, a PostgreSQL metastore, and a Redis queue (p501) — run in the background with `docker compose up --build -d` (p501).

3. Some chapters add extra services (e.g. chapter 15 adds Grafana, Prometheus, Flower, and Redis for monitoring examples) via `compose.override.yaml`, which "takes care of the details for you" (p501).

4. Inspect running containers with `docker ps` (container names are prefixed by the containing folder name, making chapter ownership identifiable) and view logs with `docker logs -f <container_name>` (p502).

5. Tear down an environment with `docker compose down -v` from the chapter directory, which stops containers and removes associated networks/volumes (p502) — verify complete removal with `docker ps -a` (p502-503).

6. Remove any leftover unrelated containers individually with `docker rm <container_id>`, or all at once with `docker rm $(docker ps -aq)` (p503).

7. Remove unused Docker volumes with `docker volume prune`, with an explicit caution: "We urge you to use caution with this command, however. It may result in inadvertent data loss if you end up discarding the wrong Docker volumes."
(p503)

## 5. Trade-offs and limitations

- Later, more complex chapters require substantially more local compute resources than earlier ones, since "some chapters spin up additional services that require a lot of memory and CPUs" (p502).
- `docker volume prune` is a blunt, environment-wide operation and risks deleting volumes unrelated to the chapter being torn down if run carelessly (p503).

## 6. Failure modes and edge cases

- **Accidental data loss from over-broad volume pruning**: running `docker volume prune` without checking which volumes are in use can discard volumes still needed by other running Docker environments (p503).
- **Leftover unrelated containers after teardown**: `docker ps -a` after `docker compose down -v` "may show a list of unrelated containers that you'll want to remove" separately, since compose teardown only affects that project's own containers (p503).

## 7. Implications for design/build/maintain/RCA/optimization

- **Build** [D]: always run example environments from within the specific chapter's directory, since `compose.yaml`/`compose.override.yaml`/`.env` are chapter-scoped and not designed to be run from the repository root.
- **RCA** [D]: when an example fails to start or behaves unexpectedly, check `docker logs -f <container_name>` for the specific service first, since the appendix explicitly frames logs as the primary diagnostic tool ("We hope that these logs will provide valuable feedback if things go awry," p502).
- **Optimization** [D]: allocate Docker Desktop (or equivalent) resources proportional to the chapter being run — later chapters need more CPU/memory/disk than earlier ones (p502).

## 8. How to test/verify these claims

- Reproduce the standard startup flow: run `docker compose up --build` in a chapter directory and confirm the container set matches the documented list (API server, scheduler, DAG processor, triggerer, workers, PostgreSQL, Redis) via `docker ps` (p501-502).
- Verify teardown completeness by running `docker compose down -v` followed by `docker ps -a` and confirming no containers from that chapter remain (p502-503).

## 9. Cross-references

- Chapter 15 (operating Airflow in production): cited as the chapter whose examples require the extra Grafana/Prometheus/Flower/Redis monitoring services configured via `compose.override.yaml` (p501).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Full example log output (p502) | Representative log lines cited; full raw output reproducible from running the environment directly rather than duplicated verbatim here. |
