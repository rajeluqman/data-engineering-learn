# Ch.10 — Security and Privacy

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 394–403 (10 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 3,611
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**The chapter's people/process/technology ordering [S]** (p395): "we lay out some things data engineers should consider around security, particularly in people, processes, and technology (in that order)" — an explicit, deliberate sequencing, not an arbitrary list.

**The power of negative thinking [S]** (p395, citing Atul Gawande's 2007 NYT op-ed): "positive thinking can blind us to the possibility of terrorist attacks or medical emergencies and deter preparation. Negative thinking allows us to consider disastrous scenarios and act to prevent them."

**Security theater vs. security habit [S]** (p396): "a pervasive focus on compliance... but not enough attention to potentially bad scenarios... this creates an illusion of security but often leaves gaping holes" — contrasted with genuine, habitual security: "Security needs to be simple and effective enough to become habitual throughout an organization."

**The principle of least privilege, restated as this chapter's own definition [S]** (p397): "a person or system should be given only the privileges and data they need to complete the task at hand and nothing more."

**Broken glass process [S]** (p397): data "must be retained but should be accessed only in an emergency. Put this data behind a broken glass process: users can access it only after going through an emergency approval process... Access is revoked immediately once the work is done."

**Shared responsibility model in the cloud [S]** (p397): "The cloud vendor is responsible for ensuring the physical security of its data center and hardware" and "Most cloud security breaches continue to be caused by end users, not the cloud."

**Encryption at rest vs. over the wire [S]** (p400): at rest — "full-disk encryption" and "server-side encryption for all data stored in servers, filesystems, databases, and object storage," plus encrypted backups; over the wire — "HTTPS is generally required for modern cloud APIs," with an explicit named limitation: "HTTPS does nothing to protect data if bucket permissions are left open to the public."

**Hardened perimeter vs. zero-trust security, revisited from Ch.3 [S]** (p402): "The cloud is generally closer to zero-trust security—every action requires authentication," contrasted with air-gapped hardened-perimeter systems, whose named worked example is "nuclear missile silos are air gapped (not connected to any networks)."

## 2. WHAT / WHY / WHEN

**WHAT:** A short, practice-oriented chapter revisiting the security undercurrent in depth, organized strictly by people → processes → technology, closing with a worked example security policy and a note on low-level/systems security. `[D]`

**WHY it matters:** stated as directly as any claim in the book: "We believe that security is the first thing a data engineer needs to think about in every aspect of their job and every stage of the data engineering lifecycle" (p394). `[S]`

**WHEN to apply the broken-glass process (p397):** specifically for sensitive data that "must be retained but should be accessed only in an emergency" — not a default access pattern, but reserved for retained-but-rarely-needed sensitive data where normal role-based access would be excessive.

**WHEN cloud vs. on-premises/air-gapped security makes sense (p402):** the chapter's default recommendation is cloud/zero-trust "because it imposes zero-trust practices and allows companies to leverage the army of security engineers employed by the public clouds," but concedes "sometimes hardened perimeter security still makes sense" for the highest-sensitivity, network-isolable cases (its own analogy: nuclear missile silos).

## 3. Assumptions and prerequisites

- Assumes the security-as-undercurrent framing already established across earlier chapters: "security being an undercurrent" (p395) is referenced as prior knowledge, not redefined here. `[S]`
- Assumes the hardened-perimeter-vs-zero-trust distinction from Ch.3: "Recall that in Chapter 3, we discussed the difference between a hardened perimeter and zero-trust security" (p402). `[S]`
- Assumes the reader already understands IAM roles/service accounts at a basic level; the chapter applies rather than introduces this vocabulary (p397). `[D]`

## 4. Mechanism / key steps

**Excess-permission monitoring and automatic revocation, the chapter's own worked example (p400–401):** a vendor tool tracks per-user/service-account permission usage over time → if an analyst "hasn't accessed Redshift for six months," the unused permission is flagged → the tool can be configured to "automatically alert an administrator or remove permissions after a specified elapsed time" → if access is later needed again, "they can put in a ticket to restore permissions." This is presented as a concrete implementation of least privilege that doesn't rely on manual periodic review alone.

## 5. Trade-offs and limitations

- **Encryption's explicit limits, stated directly (p400):** "Encryption is not a magic bullet. It will do little to protect you in the event of a human security breach that grants access to credentials" — framed as a "baseline requirement," not a sufficient control on its own.
- **FTP's named vulnerability, stated directly (p400):** "FTP is simply not secure on a public network... FTP is vulnerable to man-in-the-middle attacks, whereby an attacker intercepts downloaded data and changes it before it arrives at the client. It is best to simply avoid FTP."
- **Self-hosted/on-premises security's residual human risk, stated directly even for the most hardened case (p402):** "Just keep in mind that even on premises, air-gapped servers are vulnerable to human security failings" — the chapter does not present physical isolation as eliminating risk, only shifting its locus back to people (§1's opening claim, "The weakest link in security and privacy is you," p395).

## 6. Failure modes and edge cases

- **Public S3 buckets and open inbound access, named as observed real-world failures (p401–402):** "we've seen publicly available Amazon S3 buckets housing lots of sensitive data. We've also witnessed Amazon EC2 instances with inbound SSH access open to the whole world for 0.0.0.0/0 (all IPs) or databases with open access to all inbound requests over the public internet."
- **Ransomware with reduced insurance payouts as a compounding failure (p397–398):** "Ransomware attacks are widespread these days. Some insurance companies are reducing payouts in the event of an attack, leaving you on the hook both to recover your data and pay the bad actor" — motivating the chapter's explicit backup-and-restore-testing requirement, not backups alone.
- **Delayed breach discovery as the default case, stated directly (p400):** "Most companies don't find out about security incidents until well after the fact" — the chapter's stated reason for treating logging/monitoring/alerting as non-optional DataOps work rather than a nice-to-have.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the people→processes→technology ordering (§1) is a directly reusable sequencing principle for any security review or audit conducted for this vault's projects — start with human/social-engineering exposure before auditing tooling. `[D]`
- **Build:** the example security policy's credential rules (p398–399: SSO-first, MFA, no credentials in code, use a secrets manager, disable/delete old credentials) are directly reusable, concrete build requirements for any project's credential-handling practices. `[D]` (this note's own summary of the chapter's bullet list.)
- **Maintain:** the excess-permission automatic-revocation mechanism (§4) is a concrete, source-backed maintenance practice — periodic automated permission audits, not just onboarding-time provisioning, should be a standing operational control.
- **RCA:** the "most breaches are caused by end users, not the cloud" claim (§1, shared responsibility model) reframes any cloud security incident postmortem — the default hypothesis should be misconfiguration or human error on the customer side, not a cloud-provider failure. `[D]`
- **Optimization/monitoring:** the four named monitoring categories (access, resources, billing, excess permissions, p400–401) form a directly reusable cross-sectional monitoring checklist for any data platform's security dashboard.

## 8. How to test / verify these claims

- The excess-permission revocation mechanism (§4) is directly testable: provision a role, leave it unused for the configured threshold period, and confirm automated flagging/removal fires as configured.
- The FTP man-in-the-middle vulnerability claim (§5) is a well-established, independently verifiable protocol-level fact, checkable against any general networking-security reference — not unique to this book's claim.
- The "most cloud security breaches are caused by end users, not the cloud" claim (§1) is presented by the authors as their own field observation without a cited statistic — `[S]` as the book's own claim, but `[U]` as an externally verified rate.
- The billing-spike-as-compromise-indicator claim (§4/§7) is directly testable by simulating unauthorized resource usage in a test cloud account and confirming a configured budget alert fires.

## 9. Cross-references

- Directly extends `fundamentals_de` [[ch03_designing_good_data_architecture|Ch.3]] (hardened perimeter vs. zero-trust security, p402) and the security-undercurrent material threaded through every previously synthesized chapter ([[ch02_data_engineering_lifecycle|Ch.2]]–[[ch09_serving_data|Ch.9]]) — this chapter is explicitly framed as a deeper, dedicated return to that recurring undercurrent rather than new territory. No contradiction found.
- Directly echoes the least-privilege and broken-glass-process language already introduced in [[ch06_storage|Ch.6]] (storage undercurrents) and [[ch09_serving_data|Ch.9]] (serving undercurrents) — this chapter gives the fullest definition of both terms in the source; the earlier chapters' briefer mentions are consistent with, not contradicted by, this chapter's treatment. `[D]`
- No forward-references to not-yet-synthesized chapters were found in this chapter (it is largely self-contained and retrospective). Nothing flagged for `check_deferred_refs.py`.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Full "Example Security Policy" bullet lists (p398–399: Protect Your Credentials, Protect Your Devices, Software Update Policy — ~20 total bullets) | Representative items captured in §7; the complete enumerated policy text is not reproduced verbatim to avoid unnecessary duplication of source content. |
| "Security for Low-Level Data Engineering" subsection (p402–403, CPU/microcode/logging-library vulnerability discussion) | The chapter itself explicitly scopes this as out of its own depth ("this book is principally about high-level data engineering... we'll leave it to you to dig into the gory technical details," p403) — summarized at definitional level only in §1, not expanded further here. |
| "Additional Resources" list (p403, 3 external book/publication references) | Bibliography, not chapter content — not synthesized. |
| Footnoted external source (Atul Gawande's NYT op-ed) | Quoted where load-bearing (§1); the source document itself was not independently retrieved beyond what this chapter quotes. |
