# Ch.11 — Running tasks in containers

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 287–318 (32 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Container-based virtualization** [S]: "container-based virtualization... is a much more lightweight approach than VMs... container-based virtualization uses kernel-level functionality in the host OS to virtualize applications."
(p290)

**Container engine** [S]: "Interaction between containers and the host OS is often managed by a service called the container engine, which provides an API for managing and running the application containers and their images."
(p290)

**Dockerfile** [S]: "we can start building a Docker image by creating a Dockerfile, which is essentially a text-based file that tells Docker how to build the image."
(p292)

**`DockerOperator`** [S]: "The easiest way to run a task in a container with Airflow is to use the DockerOperator, which is available in the apache-airflow-providers-docker provider package."
(p298)

**Kubernetes** [S]: "Kubernetes is an open source container orchestration platform that focuses on the deployment, scaling, and management of containerized applications."
(p307)

**Pod** [S]: "In Kubernetes, these applications are called pods, which can contain one or multiple containers that must run together on a single machine."

"a pod is the smallest unit of work inside Kubernetes."
(p307-308)

**`KubernetesPodOperator`** [S]: "we replace our DockerOperators with instances of the KubernetesPodOperator, which are available in the apache-airflow-providers-cncf-kubernetes providers package."

"As the name implies, the KubernetesPodOperator runs tasks within pods on a Kubernetes cluster."
(p311)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter motivates and demonstrates running Airflow tasks as containers, first with plain Docker (`DockerOperator`) and then with Kubernetes (`KubernetesPodOperator`), as an alternative to Airflow's built-in operator ecosystem.

**WHY** [S]: motivated by the operational cost of using many different operators: "creating and managing DAGs with many operators can be quite challenging due to the complexity involved," specifically around "operator interfaces and implementations" (§11.1.1) and "complex and conflicting dependencies" (§11.1.2) (p288-289).

**WHEN** [D]: use `DockerOperator` when tasks need isolated, independently-versioned dependencies and a single Docker host/worker is sufficient (§11.4); use `KubernetesPodOperator` when tasks need to scale across multiple machines or require specific per-task resource allocation (CPU/memory/GPU) (§11.5); prefer the generic-operator (containerized) approach over building/maintaining many specialized Airflow operators when dependency conflicts or operator-maintenance burden become significant (§11.1.3).

## 3. Assumptions and prerequisites

- Prerequisite: the movie-recommender DAG and MovieLens ratings-fetching code from chapter 9, reused and re-implemented as containerized tasks throughout this chapter (p288, "based on our recommender use case from chapter 9"; p300, "convert the code we wrote for fetching ratings (chapter 9) to a script").
- Assumes Docker is installed and running for the Docker-based sections (p291).
- Assumes access to a running Kubernetes cluster and a locally installed `kubectl` client for the Kubernetes-based sections: "make sure that you have access to a Kubernetes cluster and have the kubectl client installed locally."
(p308)
- Assumes familiarity with basic container concepts is optional, since the chapter provides its own introduction: "If you're familiar with Docker and the concepts behind containers, feel free to skip ahead to section 11.3."
(p290)

## 4. Mechanism / key steps

1. Run an existing image with `docker run <image> <command>`, e.g. `docker run debian:buster-slim echo Hello, world!` (p291, Listing 11.1) — Docker pulls the image if not cached, creates a container, executes the command, and streams output back (p291-292).

2. Build a custom image with a Dockerfile: a `FROM` base-image instruction, `COPY`/`RUN` instructions to add dependencies and application files, and `ENTRYPOINT`/`CMD` to define the default executed command (p292-293, Listing 11.3), then build with `docker build --tag <name> .` (p293, Listing 11.4).

3. Mount host storage into a container with `--volume <host_path>:<container_path>` on `docker run`, since "your container environment is isolated from your host OS, meaning that it... has an isolated filesystem separated from the host filesystem."
(p295)

4. Replace task-specific operators with `DockerOperator` instances, each specifying `image`, `command`, and `volumes` arguments, e.g. `DockerOperator(task_id="rank_movies", image="manning-airflow/movielens-rank", command=[...], volumes=["/tmp/airflow/data:/data"])` (p298, Listing 11.9).

5. Convert existing Python task logic into a standalone CLI script (using `click` or `argparse`) so it can run inside a container independent of Airflow's own Python environment (p300-302, Listings 11.10-11.11).

6. Package the CLI script and its dependencies into a Dockerfile, install dependencies via `pip install` (inline or via `requirements.txt`), copy the script, and put it on `PATH` so it's runnable by name (p302, Listings 11.12-11.13).

7. Build a Docker-based DAG by replacing each task-specific operator with a `DockerOperator` referencing the corresponding built image, using `mounts=[Mount(source=..., target="/data", type="volume")]` for shared storage and `network_mode=...` to reach other containers such as the API (p303-305, Listings 11.14-11.15).

8. Set up Kubernetes resources before running tasks: create a namespace (`kubectl create namespace airflow`), a `PersistentVolume`/`PersistentVolumeClaim` YAML for storage, and a `Deployment`/`Service` YAML for any backing services (e.g. the MovieLens API), then apply them with `kubectl apply -f` (p299-310, Listings 11.18-11.22).

9. Replace `DockerOperator` instances with `KubernetesPodOperator` instances, specifying `image`, `cmds`, `arguments`, `namespace`, `name`, `volumes`, `volume_mounts`, `image_pull_policy`, and `is_delete_operator_pod` (p311-312, Listing 11.23).

10. Construct Kubernetes volume/volume-mount configuration objects using the Kubernetes Python SDK's `k8s.V1PersistentVolumeClaimVolumeSource`, `k8s.V1Volume`, and `k8s.V1VolumeMount` classes, referencing the previously created `PersistentVolumeClaim` by name (p312-313, Listing 11.24).

11. Diagnose a stuck/pending Kubernetes task by first checking Airflow task logs for "Pod not yet started" warnings, then running `kubectl --namespace airflow get pods` to list pods and `kubectl describe pod [NAME]` to inspect scheduling events (p315-316, Listings 11.28-11.29) — e.g. a missing `PersistentVolumeClaim` surfaces as `FailedScheduling ... persistentvolumeclaim "data-volume" not found` (p316).

## 5. Trade-offs and limitations

- Using many specialized operators requires "spend[ing] valuable time and resources tracking down and fixing the underlying issues" for "more esoteric, less frequently used Airflow operators" (p288).
- All operator dependencies "must be installed in the environment that runs the Airflow scheduler, as well as the Airflow workers themselves."
(p289) Python "doesn't provide a mechanism for installing multiple versions of the same package in the same environment" (p289), creating conflict risk across DAGs.
- The containerized approach "requires building an image for each task"
(p297), trading operator-proliferation complexity for image-build/maintenance overhead.
- Container-based tasks improve testability because images "can be developed and main"
(p298) [D] (source continues "-tained separately from the Airflow DAG in which they run" across a hyphenated line wrap), unlike `PythonOperator` tasks that are "tightly coupled to the DAG itself" (p298).
- Docker alone "doesn't help you orchestrate and distribute the work over multiple machines, thus limiting the scalability of the approach" — the specific limitation Kubernetes addresses (p307).
- Setting up and maintaining a Kubernetes cluster "which is not necessarily trivial"
(p317), and storage must be made available specifically to the Kubernetes pod rather than the Airflow worker.
- Kubernetes pods are explicitly ephemeral: "it's essential to remember that Kubernetes pods are assumed to be ephemeral resources. There can be many reasons why task pods fail to complete."
(p317)

## 6. Failure modes and edge cases

- **Missing volume mount silently loses output**: running a container without mounting a host volume produces no output file on the host filesystem, since the container filesystem is isolated: `ls amsterdam.out: No such file or directory` (p295).
- **Orphaned running containers**: `docker ps` must be checked for containers "still secretly running" after use; stopped containers persist in the background until explicitly removed with `docker rm` (p296).
- **Kubernetes pod stuck pending due to missing resource**: a task pod stuck in the pending state is often caused by Kubernetes being unable to schedule it, e.g. `FailedScheduling ... persistentvolumeclaim "data-volume" not found` (p316) when the required `PersistentVolumeClaim` was never applied — fixed by (re)applying the resource YAML (p316).
- **Wrong diagnostic tool for Kubernetes issues**: the source explicitly directs troubleshooting order — check Airflow logs first, then use `kubectl` for cluster/scheduling-specific issues: "If you see anything that looks like a scheduling issue, kubectl is your best hope for identifying issues with your Kubernetes cluster or configuration."
(p317)

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: decouple task logic from the DAG by wrapping it in a standalone CLI script and container image, enabling independent versioning/testing of the task's implementation from the orchestration logic (p300, p297).
- **Build** [D]: put dependencies for each task in its own Docker image rather than the shared Airflow worker environment, eliminating cross-task dependency-version conflicts (p296, Figure 11.6).
- **Maintain** [D]: since containerized tasks share one operator interface (`DockerOperator` or `KubernetesPodOperator`), only that single operator's behavior needs to be understood/debugged across a fleet of DAGs, rather than every operator type in use (p296-297).
- **RCA** [D]: when a `KubernetesPodOperator` task is stuck, check the task's Airflow log first for pod-status warnings, then run `kubectl describe pod` to find the specific scheduling failure reason before assuming an application-level bug (p315-317).
- **Optimization** [D]: move to Kubernetes (over plain Docker) specifically when workloads need to scale across multiple machines or require differentiated per-task resources (CPU/memory/GPU), since "Kubernetes provides considerable advantages over Docker, especially with"
(p317) [D] (source continues "regard to scalability, flexibility... and managing other resources, such as storage and secrets").

## 8. How to test/verify these claims

- Reproduce the isolated-filesystem behavior by running the `wttr-example` container without a `--volume` mount and confirming no output file appears on the host (p295), then rerunning with `--volume` and confirming the file exists at the mounted path (p295-296, Listings 11.7-11.8).
- Reproduce the full Docker-based DAG by running Listing 11.14-11.15 (p303-305) and confirming the `fetch_ratings`/`rank_movies` task logs and output CSV match the shapes shown in Listings 11.16-11.17 (p305-306).
- Reproduce the Kubernetes pending-pod failure by deliberately omitting the `PersistentVolumeClaim` resource, running the `02_kubernetes` DAG, and confirming the exact `FailedScheduling` event text via `kubectl describe pod` (p316), then confirming it resolves after applying the missing resource (p316-317).
- Verify volume/volume-mount wiring by inspecting `k8s.V1Volume`/`k8s.V1VolumeMount` object construction against Listing 11.24 (p312-313) and confirming the pod actually reads/writes to the mounted `/data` path.

## 9. Cross-references

- [[ch09_extending_airflow_with_custom_operators_and_sensors|Chapter 9]] (custom operators and sensors): the MovieLens ratings-fetching logic and recommender DAG reused and re-implemented as containerized CLI scripts throughout this chapter (p288, p300).
- *Kubernetes in Action* by Marko Lukša (Manning, 2017), cited as a recommended full reference for Kubernetes beyond this chapter's high-level treatment (p297).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 11.1–11.12 (architecture diagrams, UI screenshots, workflow diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full `click`-based CLI scaffold and complete option definitions (Listing 11.10-11.11) | Representative structure cited; full CLI argument definitions were themselves omitted by the source "for brevity" (p301) and are available only in the accompanying code repository. |
| Full Kubernetes YAML specifications for the MovieLens API deployment/service (Listing 11.21) | Representative fields cited; complete YAML reproducible from the source PDF directly rather than duplicated verbatim here. |
| Full introduction to Kubernetes architecture and concepts beyond what's used in this chapter's example | The source itself defers full depth to a dedicated Kubernetes book (p297, "Kubernetes is a topic that could fill an entire book"). |
