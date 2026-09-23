# Ch.17 — Airflow deployment options

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 474–499 (26 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Managed Airflow service** [D]: a vendor-operated Airflow deployment (Astronomer Astro, Google Cloud Composer, AWS MWAA) that offloads infrastructure setup/maintenance/patching from the user.

**Helm** [S]: "Helm is a package manager for Kubernetes that helps you manage applications. Its charts help you define, install, and upgrade even complex Kubernetes applications."
(p479)

**Persistent volume (Kubernetes)** [S]: "Persistent volumes are Kubernetes's abstraction over storage, allowing you to mount shared volumes to containers without having to know the underlying storage technology."
(p487)

**Git-sync DAG deployment** [S]: "Airflow creates a sync container that pulls the code from the configured repository before starting a task"
(p489).

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter surveys production deployment options for Airflow — three vendor-managed services (Astronomer, Google Cloud Composer, AWS MWAA), then a hands-on Kubernetes/Helm-based self-managed deployment covering DAG delivery, dependency delivery, custom secrets, external metastore, and multi-executor configuration.

**WHY** [S]: "Up to now, all our examples have run on Airflow deployed on your local machine using Docker Compose. This setup, however, is hardly production ready for running your pipelines outside a development setting."
(p474)

**WHEN** [D]: use a managed service when minimizing operational burden matters more than deployment flexibility (§17.1); self-host on Kubernetes via Helm when fine-grained control, cost optimization at scale, or integration with existing on-prem/multi-cloud infrastructure is required (§17.2-17.3).

## 3. Assumptions and prerequisites

- Prerequisite: the Airflow component architecture and executor choices from chapter 15, directly reused: "The options are covered in chapter 15, so we won't repeat them here."
(p494)
- Prerequisite: Docker Compose-based local setup patterns from earlier chapters, extended here to bootstrap a local Kubernetes cluster via k3s (p477-478).
- Assumes access to a Kubernetes cluster (local via k3s/minikube/kind, or cloud-provided) and the `kubectl`/`helm` CLIs (p477-479).
- Assumes a reachable container registry to push custom Airflow images built for DAG/dependency delivery (p485-486).

## 4. Mechanism / key steps

1. Evaluate managed services by their integration surface: Astronomer's Astro (multi-cloud, DataOps-focused, deep Airflow project involvement) (p475-476), Google Cloud Composer (GKE-based, tight GCP service integration, pay-for-resources-used) (p476-477), and AWS MWAA (S3-based DAG upload, CeleryExecutor-based worker scaling, tight AWS service/IAM integration) (p477).

2. Bootstrap a local Kubernetes environment for experimentation using k3s inside Docker Compose, starting a cluster plus a PostgreSQL database and container registry via `docker compose up -d` (p478, Listing 17.1).

3. Connect tooling (`kubectl`, `helm`) to the cluster via a `KUBECONFIG`-pointed config file, verifying with `kubectl cluster-info` (p479, Listings 17.2-17.3).

4. Deploy default Airflow via the official Helm chart: `helm repo add apache-airflow https://airflow.apache.org` then `helm upgrade --install airflow apache-airflow/airflow --create-namespace --namespace airflow --set apiServer.service.type=LoadBalancer ...` (p479-480, Listing 17.4) — verify with `kubectl get pods --namespace airflow` (p480-481, Listing 17.5).

5. Override default Helm values via a values-override YAML file passed with `-f`, e.g. customizing the initial admin user under `webserver.defaultUser` (p481, Listing 17.6) — apply via `helm upgrade --install ... -f <values-file>` (p481-482, Listing 17.7); note that upgrading (not destroying) a release leaves prior state (e.g. the old user) intact (p482).

6. Fix the dynamically-generated-webserver-secret-key warning (p482) by creating a Kubernetes secret with a random hex token (`kubectl create secret generic my-apiserver-secret ...`) and referencing it via `apiSecretKeySecretName` in the values file (p482-483, Listings 17.8-17.10) — the source explicitly flags this specific method as insufficiently secure for production, recommending an external secrets store instead (p483).

7. Point Airflow at an external metastore by creating a Kubernetes secret holding the database connection URI and setting `postgresql.enabled: false` plus `data.metadataSecretName` in the values file (p483-484, Listings 17.11-17.12); clean up the now-unused in-cluster PostgreSQL StatefulSet afterward (p484, Listing 17.13).

8. Deploy DAGs via one of three mechanisms: (a) baking DAGs into the Airflow image with a `COPY` instruction and referencing the custom image via `images.airflow.repository`/`tag` (p485-486, Listings 17.14-17.17); (b) mounting a Kubernetes `PersistentVolume`/`PersistentVolumeClaim` and setting `dags.persistence.enabled: true` with `existingClaim` (p487-488, Listings 17.18-17.19); (c) Git-sync, configuring `dags.gitSync` with `repo`, `branch`, `subPath`, etc., which adds a sidecar `git-sync` container to the DAG processor pod (p489-490, Listings 17.20-17.21).

9. Deploy additional Python dependencies either via the non-production-suitable `_PIP_ADDITIONAL_REQUIREMENTS` environment variable, or (preferred for production) by baking them into the custom Airflow image alongside DAGs (p491-492, Listings 17.22-17.24).

10. Configure multiple executors simultaneously in Helm via `executor: "CeleryExecutor,KubernetesExecutor"`, with separate images configured for `images.airflow` (Celery default) and `images.pod_template` (KubernetesExecutor default), and per-task executor/image overrides settable from the DAG definition itself (p494-496, Listings 17.25-17.27).

## 5. Trade-offs and limitations

- "Rolling your own Airflow deployment can give you ultimate flexibility... Setting up and maintaining such a deployment can be a lot of work" (p475) — the central trade-off this chapter frames repeatedly between self-hosting and managed services.
- Google Cloud Composer integrates tightly with GCP services but "if you're looking to connect to on-site services or those in other clouds, running Airflow in GCP may make less sense" (p498).
- Baking dependencies into a single shared Airflow image means "all the Airflow workers use the same set of dependencies," which "soon becomes a bottleneck leading to conflicting dependencies for different use cases" once multiple teams share the deployment — mitigated by multiple Celery queues with per-queue images, or the multi-executor mechanism (p493).
- The `CeleryKubernetesExecutor` (Airflow 2 mechanism for per-task executor choice) "has been deprecated in Airflow 3 and superseded by the ability to configure multiple executors," which the source itself flags as "still marked experimental" as of writing (p493-494).
- Git-sync DAG delivery and Kubernetes persistent-volume DAG delivery both avoid rebuilding an image on every DAG change, but the persistent-volume approach's CI/CD wiring "typically doesn't provide out-of-the-box functionality for pushing directly to the shared volume."
(p487) Requires a custom push/pull mechanism depending on volume type.
- Kubernetes-based self-hosted deployments "can be expensive due to the costs of the underlying cluster"
(p499), compared to other compute or SaaS options like Astronomer.

## 6. Failure modes and edge cases

- **Unnecessary component restarts from a dynamically generated secret**: "The default Helm Chart generates a ran"
(p482) [D] (source continues "-dom key each time a deployment update is done, causing unnecessary restarts when updating the deployment" across a hyphenated line wrap), surfaced as an explicit console warning — fixed by pinning a static secret (p482-483).
- **Stale state after a database swap**: switching to an external metastore replaces the prior database entirely, so "we don't have the admin user anymore because we started using the new external metastore" unless the user-creation override is reapplied alongside the database change (p484).
- **Missing dependency causes task failure under multi-executor setup**: in the worked multi-executor example, "The version_celery task is expected to fail"
(p496) because the tensorflow dependency is missing in the default image, while the KubernetesExecutor tasks (using a different, dependency-complete image) succeed — illustrating per-executor image isolation working as intended, not a bug.
- **Reverting unrelated Helm values on upgrade**: each `helm upgrade` with a new values file must still include all previously-applied overrides (user, secret key, database), or "our previous changes" would be silently reverted — the source explicitly folds all prior changes into each subsequent values file for this reason (p484, p486, p493).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: choose DAG-delivery mechanism based on team topology — baked-in images for a single team wanting strict versioning/immutability, persistent volumes or Git-sync for multiple teams needing independent DAG delivery without full image rebuilds (p487, p489).
- **Build** [D]: always fold prior Helm value overrides into each new values file when iterating on a deployment, since `helm upgrade` does not preserve unspecified values from earlier releases automatically in this workflow (p484, p486).
- **Maintain** [D]: replace the default Helm Chart's auto-generated webserver/API-server secret key with a static one immediately in any long-lived deployment, to avoid unnecessary component restarts on every upgrade (p482-483).
- **RCA** [D]: if a task fails with a missing-dependency error in a multi-executor or multi-image setup, check which image (Celery default vs. Kubernetes pod template vs. per-task override) actually ran that task before assuming a code bug (p496-497).
- **Optimization** [D]: for multi-team deployments with conflicting dependency needs, use per-queue or per-executor custom images (multiple Celery queues, or the Airflow 3 multi-executor mechanism) rather than one shared image with every team's dependencies installed (p493-494).

## 8. How to test/verify these claims

- Reproduce the default Helm deployment (Listing 17.4, p480) and confirm all expected pods (`api-server`, `dag-processor`, `postgresql`, `redis`, `scheduler`, `statsd`, `triggerer`, `worker`) reach `Running` status via `kubectl get pods --namespace airflow` (p480-481).
- Verify the static-secret fix by applying Listings 17.9-17.10.

Confirm the "You should set a static" secret-key warning
(p482, Listing 17.8) no longer appears on subsequent `helm upgrade` runs.
- Verify each DAG-delivery mechanism by deploying the corresponding values file (baked-image, persistent-volume, Git-sync) and confirming the expected DAG(s) appear in the Airflow UI (p486, p488-489, p490-491).
- Verify multi-executor isolation by running the example DAG from Listing 17.26 (p494-496) and confirming `version_celery` fails on the missing dependency while `version_k8s`/`version_k8s_old` succeed on their respective images (p496-497).

## 9. Cross-references

- [[ch01_meet_apache_airflow|Chapter 1]] (Airflow architecture): the component diagram is reused to map Kubernetes pods to Airflow components (p480, Figure 17.3, "we link the list of running pods to the architecture described in chapter 1").
- [[ch15_operating_airflow_in_production|Chapter 15]] (operating Airflow in production): executor types and trade-offs are referenced rather than repeated: "The options are covered in chapter 15, so we won't repeat them here."
(p494)
- [[ch02_anatomy_of_an_airflow_dag|Chapter 2]] (DAG examples): the Git-sync example deploys `[[ch02_anatomy_of_an_airflow_dag|chapter02]]/dags` directly from the book's own repository (p490).
- Appendix A (referenced for the Docker Compose–based Kubernetes setup used throughout this chapter's examples) (p478).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 17.1–17.10 (Astronomer UI, Kubernetes architecture diagrams, Airflow UI screenshots) | Visual content; described narratively where relevant, not reproduced. |
| Full Helm values YAML files (Listings 17.6, 17.9-17.12, 17.17-17.20, 17.24, 17.26) | Representative/incremental fields cited per step; full YAML reproducible from the source PDF directly rather than duplicated verbatim here. |
| Full vendor pricing details (Astronomer, Cloud Composer, MWAA) | The source itself defers to each vendor's website for up-to-date pricing (p477, p478); not reproduced since pricing is time-sensitive and not a technical mechanism. |
| Astronomer-specific tooling details (Astro CLI, Astro IDE, Astronomer Cosmos, Astro Observe) beyond their named purpose | Vendor product features named for context (p476) but not elaborated, since they are outside core open-source Airflow mechanics. |
