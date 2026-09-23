# Appendix B — Cloud Networking

**Source:** `fundamentals_de` (Fundamentals of Data Engineering, Reis & Housley, O'Reilly 2022)
**PDF page range:** 424–427 (4 pages) — per `audit/CHAPTER_MAP.csv` (v3; see
`GAPS_AND_VERIFICATION.md` §7b for the appendix-range bug this corrects)
**Chapter map status:** `located`, `entry_type: appendix`
**Synthesis status:** `synthesized` (this session)
**Word count (measured, `chapter_stats.json`):** 1,286
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Cloud network topology [S]** (p424): "describes how various components in the
cloud are arranged and connected" — the appendix states all three major clouds
(Azure, GCP, AWS) "use remarkably similar resource hierarchies of availability zones
and regions," with GCP adding one extra layer (the multiregion, see below).

**Availability zone [S]** (p425): "the smallest unit of network topology that public
clouds make visible to customers" — may internally span multiple data centers, but
customers cannot control placement at that finer grain. Highest bandwidth / lowest
latency is between systems within the same zone.

**Region [S]** (p425): "a collection of two or more availability zones," built with
independent resources (power, water, etc.) specifically so "a local power outage
doesn't take down multiple availability zones."

**Multiregion (GCP-specific) [S]** (p426): "a layer in the resource hierarchy;
a multiregion contains multiple regions." Named current multiregions: US, EU, ASIA.
The appendix is explicit this is a **GCP-specific** abstraction, not shared by
AWS/Azure in the same native form (those require manually duplicating data across
regions to achieve a similar effect).

## 2. WHAT / WHY / WHEN

**WHAT:** A reference appendix on cloud networking topology and its cost structure
(egress fees), explicitly aimed at data engineers who "frequently encounter
networking in their careers and often ignore it despite its importance" (p424). `[S]`

**WHY it matters for a DE project:** networking topology choices directly gate
pipeline cost and performance — the appendix's central practical thesis is that
*where* compute and storage are placed relative to zones/regions determines both
latency and egress cost, two of the "undercurrents" (cost/performance) this vault's
own architecture-review heuristics (see `[[fundamentals_de/ch01...]]` §7) should
check for any data pipeline design. `[D]`

**WHEN each topology layer matters (the appendix's own guidance):**
- Single-zone placement: "high throughput data workloads should run on clusters
  located in a single zone for performance and cost reasons" — explicit example
  given: "an ephemeral Amazon EMR cluster should generally sit in a single
  availability zone" (p425). `[S]`
- Multi-zone / multi-region: for resilience against correlated failure — "engineers
  can build highly resilient, separate infrastructure... by running servers in
  multiple zones" (p425); multiple regions additionally let engineers "put resources
  close to any of their users" for latency (p425). `[S]`
- Direct network connections (e.g., AWS Direct Connect): "these connection options
  often offer dramatic discounts on data egress charges" (p427), so they matter when
  egress cost or latency to on-premises/hybrid infrastructure justifies dedicated
  connectivity. `[S]`

## 3. Assumptions and prerequisites

- Assumes basic familiarity with VPCs (virtual private clouds) and public/private IP
  addressing — introduced briefly (p425) but not built up from first principles. `[D]`
- Cross-references Ch.4's cloud economics discussion for pricing context ("Chapter 4
  discusses cloud economics and how actual provider costs don't necessarily drive
  cloud pricing," p424) — this appendix does not re-derive that argument, just
  applies it to the specific case of network egress. `[S]`

## 4. Mechanism / key steps

No procedural mechanism; this is a conceptual/cost-structure reference. The closest
thing to a mechanism is the **cost-and-latency ordering implied by the topology
hierarchy**, stated across p425–426:
1. Within a zone: fastest, and traffic to private IPs within a zone is free.
2. Between zones (same region): "nominal data egress charges," somewhat higher
   latency than intra-zone.
3. Between regions: "even slower and may incur higher egress fees."
4. Object storage is treated as a regional resource — inter-zone movement to reach a
   VM is "mainly invisible to cloud customers" and not separately charged (object
   access costs still apply).

## 5. Trade-offs and limitations

- **Public internet egress vs. direct connect, with a concrete quoted figure
  (p427):** "AWS egress charges drop from 9 cents per gigabyte over the public
  internet to 2 cents per gigabyte over direct connect" (in a "typical scenario in
  the US") — a specific, source-cited number usable for a cost-justification
  argument, with the caveat that it's one illustrative scenario, not a universal
  rate. `[S]`
- **Regional resilience is not absolute (p426):** despite "regions' geo-redundant
  design, many major cloud service failures have affected entire regions" — the
  appendix attributes this explicitly to correlated failure from "code or
  configuration problems occurring at the regional level," not physical
  infrastructure failure. This is an important caveat against assuming
  multi-region deployment alone guarantees availability. `[S]`
- **GCP multiregion convenience is GCP-specific:** "cloud customers can set up
  multiregional infrastructure on AWS or Azure" but it "involves duplicating data
  between regions" manually (p426) — i.e., GCP's multiregion is a managed
  abstraction other clouds don't natively offer at the same layer. `[S]`
- **CDN limitations, explicitly flagged (p427):** "CDNs don't work everywhere, and
  certain countries may block internet traffic and CDN delivery" — a real
  operational caveat for any global data-serving design. `[S]`

## 6. Failure modes and edge cases

- Correlated regional failure from code/config deploys (§5) — the appendix's
  explicit example of a resilience assumption that doesn't hold in practice: "the
  regional failures we've observed have generally resulted from code or
  configuration problems occurring at the regional level" (p426), meaning
  multi-zone-within-a-region does not protect against a bad deploy pushed
  region-wide. `[S]`
- Public IP usage inside a VPC silently incurring egress charges — the appendix
  flags this as a "significant caveat": VM-to-VM traffic within a zone is free only
  "to private IP addresses"; using external/public IPs for the same traffic "can
  incur data egress charges" (p425) — an easy-to-miss cost trap. `[S]`

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** high-throughput compute clusters should default to single-zone
  placement unless there's a specific resilience or latency-to-users reason to
  spread them — directly actionable placement guidance for this vault's own cloud
  pipeline designs. `[D]`
- **Cost optimization:** checking whether inter-service traffic is routed via
  private IPs (free within a zone) versus public IPs (chargeable) is a concrete,
  low-effort cost-review checklist item derived from §6's failure mode. `[D]`
- **RCA:** if a "regionally resilient" architecture still goes down, the appendix's
  own framing (§5/§6, correlated code/config failure) suggests checking deployment
  pipelines and configuration management before assuming the outage was a physical
  infrastructure fault. `[D]`

## 8. How to test / verify these claims

- The private-vs-public-IP egress-charge behavior is directly testable: send traffic
  between two VMs in the same zone once via private IP and once via public IP, and
  compare the resulting egress line-item on the cloud bill. `[D]`
- The 9-cents-vs-2-cents AWS figure (§5) is stated as of the book's writing (2022)
  and for "a typical scenario in the US" — cloud pricing changes over time, so this
  specific number should be re-verified against current AWS pricing before citing it
  in a present-day cost argument, not assumed still accurate. `[S]` claim, `[D]` flag
  on currency of the figure.

## 9. Cross-references

- Builds directly on [[ch04_choosing_technologies|Ch.4]] (Choosing Technologies, cloud economics) — not yet
  synthesized in this vault.
- Same "verify current pricing before citing" caution applies to any cost figure
  pulled from this book across all appendices/chapters — book was published 2022,
  cloud pricing is dynamic.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figure B-1 (availability zones diagram, p425) | Structural content (zones nested within regions) is covered narratively in §1 above; the diagram itself was not re-drawn. |
| Named case study (Zoom's 2020 Oracle Cloud decision, p427, footnotes 2–3) | Covered at summary level in the source's own framing (an example of egress-fee competitive dynamics) — the two cited news-article footnotes themselves were not independently followed up or verified. |
