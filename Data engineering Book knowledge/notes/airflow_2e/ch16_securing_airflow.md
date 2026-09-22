# Ch.16 — Securing Airflow

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 454–473 (20 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**RBAC (role-based access control)** [S]: "The RBAC model consists of users, each of which is assigned to a single role."
(p455)

"Permissions (certain operations) are assigned to those roles, which apply to certain components of the UI"
(p455).

**Fernet key / symmetric encryption** [S]: "Airflow can encrypt and decrypt secrets using a Fernet key."
(p459)

"Using one key for both encryption and decryption is called symmetric encryption"
(p459).

**Directory service / LDAP** [S]: "A popular way to manage users is via a service that supports the Lightweight Directory Access Protocol (LDAP), such as Microsoft Entra ID or OpenLDAP. Services of this kind are called directory services."
(p460)

**Distinguished name (DN) / directory information tree (DIT)** [S]: "entities (e.g., users, printers, and network shares) are stored in a hierarchical structure named a directory information tree (DIT). Each entity is called an entry... each entry is uniquely identified by a distinguished name (DN)."
(p461)

**HTTPS / asymmetric encryption (TLS)** [S]: "The encryption used in HTTPS is Transport Layer Security (TLS), which uses both asymmetric encryption and symmetric encryption... asymmetric encryption consists of two keys: public and private."
(p465)

**Secrets backend** [S]: "Airflow has a feature, the secrets backend, which provides a mechanism to fetch secrets from external secret storage systems while still using the existing variable and connection classes."
(p470)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter covers Airflow's security layers end to end — RBAC-based UI access control, encryption of secrets at rest (Fernet key), centralized user management via LDAP directory services, encryption of traffic in transit (HTTPS/TLS), and centralized secret retrieval via a secrets backend.

**WHY** [S]: "As an orchestrator with access to many other systems, Airflow is a desirable target for hackers. To keep unwanted intruders at bay, Airflow offers several layers of security to help prevent unauthorized access."
(p454)

**WHEN** [D]: configure RBAC roles before creating any real users, to control which UI actions/pages each person can reach (§16.1); enable Fernet encryption before creating any users/connections, since it protects data already at rest, and set it up first ("Before creating any users and passwords, ensure that you've enabled encryption in Airflow") (§16.2); connect to an LDAP directory service instead of managing Airflow-local users whenever a central user-management system already exists (§16.3); enable HTTPS whenever the Airflow UI/API is reachable beyond a fully trusted local network (§16.4); use a secrets backend when secrets should live in one centrally-managed system rather than scattered across environment variables/connections (§16.5).

## 3. Assumptions and prerequisites

- Assumes "some knowledge of basic security principles."
(p455) The chapter is also written to be accessible to readers with little security background.
- Assumes Airflow's RBAC interface is built on Flask-AppBuilder (FAB), and that `webserver_config.py` in `$AIRFLOW_HOME` is the configuration entry point for it (p457-458).
- Assumes FAB-based LDAP authentication requires `AIRFLOW__CORE__AUTH_MANAGER` to be set to the FAB auth manager class before LDAP settings in `webserver_config.py` take effect (p463).
- Assumes a certificate authority or self-signed certificate is available for HTTPS configuration, with the explicit caveat that "No official certificate can be issued for localhost; therefore, it must be self-signed" (p467).

## 4. Mechanism / key steps

1. Create an RBAC user with a specific role via the CLI: `airflow users create --role Admin --username bobsmith --password topsecret --email ... --firstname ... --lastname ...` (p455-456, Listing 16.1).

2. Understand the five default RBAC roles and their scopes — `Admin` (all permissions), `Public` (none, unauthenticated), `Viewer` (read-only DAG access), `User` (Viewer plus DAG edit actions, no secrets access), `Op` (User plus connections/pools/variables/XComs/config access) (p456).

3. Customize the RBAC interface (including non-security settings like themes) by placing a `webserver_config.py` file in `$AIRFLOW_HOME`; Airflow generates a default one if none exists (p457-458).

4. Generate a Fernet key and configure Airflow to use it: `Fernet.generate_key()` then set `AIRFLOW__CORE__FERNET_KEY=<key>` (p459-460, Listing 16.2) — alternatively, avoid storing the raw key in an environment variable by using `AIRFLOW__CORE__FERNET_KEY_CMD` to read it from a command (e.g. `cat /path/to/secret`) (p460).

5. Connect Airflow's authentication to an LDAP directory service by setting `AIRFLOW__CORE__AUTH_MANAGER` to the FAB auth manager, then configuring `webserver_config.py` with `AUTH_TYPE = AUTH_LDAP`, `AUTH_LDAP_SERVER`, `AUTH_LDAP_SEARCH`, `AUTH_LDAP_BIND_USER`/`AUTH_LDAP_BIND_PASSWORD`, `AUTH_LDAP_UID_FIELD`, and `AUTH_USER_REGISTRATION_ROLE` for the default role assigned on first login (p463, Listing 16.4).

6. Manually reassign a user's RBAC role after LDAP-based first login by editing the `ab_user_role` table directly in the metastore, since "At the time of writing, no feature exists for mapping LDAP groups to Airflow RBAC roles"
(p463).

7. Generate a self-signed TLS certificate/private-key pair with `openssl req -x509 -newkey rsa:4096 ... -keyout privatekey.pem -out certificate.pem ...`, including a SAN extension for `localhost`/`127.0.0.1` since most browsers require it (p466-467, Listing 16.5).

8. Enable HTTPS on the API server by setting `AIRFLOW__API__SSL_CERT` and `AIRFLOW__API__SSL_KEY` to the certificate/key file paths (p467).

9. Add a self-signed certificate to the local trust store (e.g. via macOS Keychain Access, adding it to the System keychain and explicitly trusting SSL) so browsers stop warning about it (p468-469) — for publicly reachable deployments, obtain a certificate from a trusted authority (e.g. Let's Encrypt) instead (p470).

10. Configure a secrets backend by setting `AIRFLOW__SECRETS__BACKEND` to the relevant provider class (e.g. `airflow.providers.hashicorp.secrets.vault.VaultBackend`) and `AIRFLOW__SECRETS__BACKEND_KWARGS` with connection details specific to that backend (p471-472).

11. Store a connection in the secrets backend under a key `conn_uri` (URI-formatted) and a variable under a key `value`, using a hierarchical secret path such as `secret/connections/secure_api` (p470-472).

12. Rely on Airflow's fixed secret-resolution order: secrets backend first, then environment variables (`AIRFLOW_CONN_*`/`AIRFLOW_VAR_*`), then the Airflow metastore (p472).

## 5. Trade-offs and limitations

- RBAC permission granularity is very fine: "access to every menu and menu item is con"
(p457) [D] (source continues "-trolled by a permission" across a hyphenated line wrap), which is powerful but makes finding the correct permissions cumbersome — the source's own workaround is inspecting other roles' existing permission sets (p457).
- Losing a Fernet key permanently loses access to all previously-encrypted secrets: "If this key is lost, encrypted messages can no longer be decrypted."
(p459)
- LDAP directory services trade transactional flexibility for read-heavy, structured lookups: "relational databases are designed for transactional use of any data you want to store, whereas directory services are designed for high volumes of read operations" — LDAP is not a substitute for a general-purpose database (p461).
- No built-in LDAP-group-to-RBAC-role mapping exists at time of writing: "At the time of writing, no feature exists for mapping LDAP groups to Airflow RBAC roles"
(p463), forcing a manual metastore edit as the only way to assign non-default roles to LDAP-authenticated users.
- Self-signed certificates work for local/dev use but require every client to manually trust them; this doesn't scale to publicly reachable deployments, which need an authority-issued certificate instead (p470).
- A secrets backend is additive, not a replacement: "The secrets backend doesn't replace secrets stored in environment variables or the Airflow metastore; it's an alternative location to store secrets" (p472), adding a third location to reason about during troubleshooting.

## 6. Failure modes and edge cases

- **Unencrypted secrets readable by anyone with database access**: "Without encryption, passwords and other secrets, such as connections, are stored unencrypted in the database. Then anybody who has access to the database can read the passwords."
(p459)
- **Untrusted self-signed certificate warnings**: browsers display security warnings for self-signed certificates by default, since "their validity can't be checked" (p468) — requiring explicit manual trust configuration per client machine (p468-469).
- **Publicly exposed Airflow services**: "In any cloud, it's easy to expose a service to the internet"
(p459), and every Airflow component (API server/UI, DAG processor, database) is a potential attack entrance point if not access-restricted.
- **Man-in-the-middle traffic interception over plain HTTP**: "All HTTP traffic is transferred in plain text; an attacker reading the traffic could intercept and read passwords as they're transmitted."
(p466)

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: narrow the attack surface first — restrict network exposure (no external IP, IP allowlisting) — before layering on RBAC, encryption, and secrets-backend controls, since the source frames this as the foundational step (p459, "lowering the number of exposed entrance points... is always a good idea").
- **Build** [D]: enable Fernet encryption before creating any real users or connections, since retroactively encrypting already-stored plaintext secrets is not addressed by simply adding the key afterward (p459).
- **Maintain** [D]: store the Fernet key and TLS private key in files with restricted permissions (or fetched via `FERNET_KEY_CMD`) rather than plaintext environment variables, and never share the private key (p460, p468).
- **RCA** [D]: if a user can't log in via LDAP with the expected role, check whether `AUTH_USER_REGISTRATION_ROLE` matches expectations and whether a manual `ab_user_role` table edit is needed, since automatic LDAP-group-to-role mapping doesn't exist (p463).
- **Optimization** [D]: centralize secrets in a dedicated secrets-management system (Vault, AWS SSM, Azure Key Vault, Google Secrets Manager) to gain rotation/versioning features Airflow itself doesn't provide, and to shrink the attack surface by storing each secret in exactly one place (p470, p473).

## 8. How to test/verify these claims

- Reproduce RBAC role restrictions by logging in as a `Viewer`-role user and confirming DAG-editing actions (clear, trigger, pause) are unavailable, then confirming they become available under the `User` role (p456, Table 16.1).
- Verify Fernet encryption by inspecting a connection's password field directly in the metastore database before and after setting `AIRFLOW__CORE__FERNET_KEY`, confirming it changes from plaintext to an encrypted string (p459-460).
- Verify LDAP authentication by configuring `webserver_config.py` per Listing 16.4 (p463) against a running LDAP service and confirming login succeeds with LDAP-stored credentials, landing the user in the configured default role.
- Verify HTTPS setup by generating a self-signed certificate (Listing 16.5, p467), configuring `AIRFLOW__API__SSL_CERT`/`SSL_KEY`, and confirming the UI is served on `https://` instead of `http://` (p467-468).
- Verify secrets-backend resolution order by defining the same secret name in the secrets backend, an environment variable, and the metastore simultaneously, and confirming the secrets-backend value takes precedence (p472).

## 9. Cross-references

- No explicit forward/backward chapter cross-references were found in this chapter's extracted text; it functions as a self-contained security reference layered on top of earlier chapters' operational content (chapter 15).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 16.1–16.21 (UI screenshots, RBAC diagrams, LDAP/DIT diagrams, HTTPS handshake diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Table 16.2 (LDAP operations: Abandon, Add, Bind, Compare, Delete, Extended, Modify DN, Modify, Search, Unbind) | Representative operations (bind, search, unbind) used in Airflow's actual LDAP flow are cited; the complete operation reference is reproducible from the source PDF directly. |
| Full list of FAB configuration options / themes | The source defers to FAB's own documentation for the complete option/theme list (p458); only the configuration mechanism itself is captured here. |
| Full secrets-backend class paths for every provider (Vault, AWS SSM, GCP Secrets Manager, Azure Key Vault) beyond the Vault worked example | Representative class paths cited; the source itself defers full details to Airflow's documentation (p472). |
