# Ch.10 — Collaborative Data Engineering Made Simple With Databricks Asset Bundles

**Source:** `databricks_big_book_4e` (Big Book of Data Engineering, 4th Edition, Databricks; chapter by Daniel Taylor and Axel Richier)
**PDF page range:** 94–98 (5 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Databricks Asset Bundles (DABs)** [S]: "Databricks Asset Bundles are a tool to facilitate the adoption of software engineering best practices, including source control, code review, testing and continuous integration and delivery, for your data and AI projects."

(p94)

**DABs as a Terraform wrapper** [S]: "Behind the scenes, Asset Bundles acts as a Databricks-supported wrapper around the Databricks Terraform provider for all resources relating to application code."

(p95)

**Top-level configuration (`databricks.yaml`)** [S]: "a YAML file in a project's root...that is used to define all of your deployment targets as well as reusable complex and static variables."

(p96)

**`mode` key** [S]: "can take one of two possible default values, `development` or `production`. For lower environments, we want to specify our targets' deployment mode to `development`. In turn, this will deploy all resources under our bundle and isolate all those resources to the user issuing the deployment."

(p96)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter explains what Databricks Asset Bundles are, why they solve a specific Terraform-based collaboration bottleneck (simultaneous developers overwriting shared state), and walks through a concrete two-engineer scenario demonstrating isolated development-environment deployment through to production merge.

**WHY** [S]: "In lower, noncontrolled environments, and if we were to use Terraform as the DevX tool of choice, each individual's deployment would overwrite existing configurations (assuming a single, remote state file was used). This is extremely problematic."

(p95)

**WHEN** [D]: applicable when multiple data engineers need to develop and integration-test changes to the same or related Databricks jobs/pipelines/ML assets simultaneously, in a shared lower (dev) environment, without their deployments overwriting each other.

## 3. Assumptions and prerequisites

- [U] This is vendor-authored content by named Databricks employees describing Databricks' own DABs tooling; framing of DABs as solving problems "Terraform... wasn't really designed for" (p95) is the vendor's own comparative framing.
- Assumes familiarity with core Terraform concepts (state files, providers) as the baseline DABs is contrasted against and built upon (p95).
- Assumes a version-controlled mono-repository workflow (git branches, pull requests) as the collaboration model DABs is demonstrated within (p96-98).
- The chapter's own worked example specifies Databricks CLI version 0.277.0 as the version used; exact CLI behavior may differ across versions (p96).

## 4. Mechanism / key steps

1. Structure a data project's source control repository so application code (Lakeflow Jobs, Spark Declarative Pipelines, Databricks Apps, ML training/inference) lives alongside its orchestration pipeline definitions, declared via YAML (or JSON, or more recently Python) (p94).

2. Define a root `databricks.yaml` configuration specifying deployment targets and reusable variables, with a `mode` key set to `development` for lower environments (isolating resources to the deploying user) or `production` for UAT/production environments (intended for use with a service principal); custom modes are also supported (p96).

3. Deploy from an isolated feature branch: each engineer branches off the shared repository (`git checkout -b feature/alice`), makes local changes to their assigned pipeline, and deploys to the shared lower environment via `databricks bundle validate -t dev --profile <profile>` followed by `databricks bundle deploy -t dev --profile <profile>` (p96-97).

4. Rely on DABs' automatic state-file isolation and resource-name prefixing: each user's deployment is isolated to their own state file (stored in the workspace file system under their user) and each deployed resource is prefixed with a unique identifier, so simultaneous deployments from different engineers/branches do not overwrite one another (p95-96).

5. Promote to production via standard code-review workflow: each engineer opens a pull request from their feature branch to main once their isolated dev-environment changes are tested; upon PR approval, changes merge into main, and production deployment uses `databricks bundle deploy -t prod --profile <profile>` (typically under a service principal, per `mode: production`) (p97-98).

## 5. Trade-offs and limitations

- DABs simplifies bundle authoring compared to raw Terraform ("lowers the barrier to entry for engineers unfamiliar with Terraform's concepts and syntax") but this simplification implies a narrower surface area than full Terraform — the chapter recommends Terraform for "static, core infrastructure assets" and DABs specifically for "application code, data projects and ephemeral resources," implying the two are complementary rather than DABs being a full Terraform replacement (p94-95).
- The chapter explicitly frames raw Terraform's weakness as being about "fluidity and ability to quickly iterate when it comes to things like unit and integration testing as well as state management — especially across different, simultaneous development tasks on the same subset of resources" — this is a collaboration/iteration-speed limitation specific to multi-developer lower-environment workflows, not a claim that Terraform is unsuitable for infrastructure management generally (p95).
- `development` mode's per-user isolation is explicitly a lower-environment pattern; `production` mode (recommended with a service principal) does not use this per-user isolation model, implying the isolation mechanism is deliberately scoped to dev/test workflows, not how production deployments are intended to work (p96).

## 6. Failure modes and edge cases

- **Shared remote Terraform state file overwritten by simultaneous deployments**: without DABs' isolation, individual deployments against a single shared remote state file overwrite each other's configurations, a failure mode affecting both engineers working on the same resource and engineers working on different resources within the same state file (p95).
- **Resource naming collisions without prefixing**: without DABs' automatic unique-prefixing of deployed resources under `development` mode, simultaneous deployments of similarly named jobs/pipelines from different branches could collide in the shared workspace (p96).
- **Using `production` mode without a service principal**: the chapter notes production mode "should be used with a service principal for all other environments, such as UAT and production" — implying that deploying to these environments under a personal user identity (rather than a service principal) deviates from the recommended pattern, though the chapter doesn't elaborate on the specific consequences (p96).

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: adopt a two-tool split — Terraform for static/core infrastructure, DABs for application code/data projects/ephemeral job compute — rather than choosing one tool exclusively, per the chapter's own recommended division of responsibility (p94).
- **Build** [D]: structure each engineer's workflow around feature-branch isolation plus `mode: development` bundle deployment, so integration testing in a shared lower environment doesn't require coordinating deployment timing across team members (p96-97).
- **Maintain** [D]: reserve `production` (or custom) mode with service-principal-based deployment for UAT/production environments, keeping the per-user isolation model exclusive to development/lower environments (p96).
- **RCA** [D]: if two engineers report unexpected overwrites or missing resources in a shared lower environment, check whether deployments are going through DABs with `development` mode (which isolates and prefixes resources) versus raw Terraform against a single shared state file, which the chapter identifies as the root mechanism behind this exact failure mode (p95-96).
- **Optimization** [D]: use DABs' isolated-state-plus-prefixing mechanism to enable true parallel development on the same repository/environment, rather than serializing engineers' integration testing to avoid state collisions, directly targeting the "time-to-production" improvement the chapter claims (p98).

## 8. How to test/verify these claims

- Reproduce the chapter's own two-engineer scenario: have two developers branch from the same repository, modify different (or the same) Spark Declarative Pipelines, and deploy simultaneously to the same lower environment via `databricks bundle deploy -t dev`, confirming both deployments coexist without overwriting each other (p96-97).
- Verify the state-file isolation claim by inspecting the workspace file system after each engineer's deployment and confirming separate, per-user state files rather than a single shared state file (p95-96).
- Verify the resource-prefixing claim by inspecting the names of deployed jobs/pipelines in the shared development workspace and confirming each carries a unique prefix tied to the deploying user/branch (p96).
- Cross-check the CLI command syntax (`databricks bundle validate`, `databricks bundle deploy`) against current Databricks CLI documentation, since the chapter pins its example to CLI version 0.277.0 and syntax may have evolved since (p96).

## 9. Cross-references

- [[ch01_introduction_to_data_engineering_on_databricks|Ch.1]] (Introduction to Data Engineering on Databricks): introduces Lakeflow Jobs and Spark Declarative Pipelines at a conceptual level, both used as the example resource types deployed via DABs here.
- [[ch05_lakeflow_connect_sql_server_connector|Ch.5]] (Lakeflow Connect: SQL Server Connector): the chapter's appendix referenced DABs as a way to manage Lakeflow Connect pipelines as code — this chapter provides the general DABs collaboration model underlying that usage.
- [[ch02_migrating_apache_spark_etl_workloads_to_databricks|Ch.2]] (Migrating Apache Spark ETL Workloads to Databricks): recommended "managing these artifacts with Terraform and VCS for strong consistency, versioning" for Compute Policies — this chapter's Terraform-plus-DABs split directly extends that recommendation to application code specifically.
- External Databricks documentation referenced but not reproduced: DABs root mapping configuration, resource-specific mappings, and CLI commands, explicitly deferred by the chapter itself ("we recommend starting with the documentation. We won't be exploring these concepts too deeply in this chapter") (p95).
- External source code repository referenced but not reproduced, for readers wanting to follow the chapter's worked example directly (p96).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Detailed DABs root-mapping configuration syntax and CLI command reference beyond the `mode`/`bundle validate`/`bundle deploy` commands shown in the worked example | The chapter itself explicitly defers this to external documentation rather than covering it in depth; not fabricated or expanded beyond what's in the source text (p95). |
| Screenshots/UI elements implied by the workspace file-system state-file description | No embedded screenshots are present in the extracted chapter text; description is narrative only, consistent with the source. |
