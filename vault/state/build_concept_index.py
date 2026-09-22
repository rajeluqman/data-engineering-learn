#!/usr/bin/env python3
"""
Builds a MEASURED concept -> chapter index across the whole vault.

Why this exists: the 90 book-chapter notes only cross-reference within their own
book. This script extracts which cross-cutting concepts actually appear where, so
concept hub notes can be written from evidence instead of recall (No-Guess Rule).

Scans:
  - Data engineering Book knowledge/notes/<source_id>/*.md   (90 audited chapter notes)
  - vault/sql/, vault/python/, vault/shared/                 (learning-track notes)

Outputs (both regenerated in place, never hand-edited):
  - vault/concepts/_index.generated.md    human-readable spread report
  - vault/concepts/_index.generated.json  machine-readable mapping

Selection criterion for a "real" cross-cutting concept: it appears in >= MIN_SOURCES
distinct sources. Concepts concentrated in a single source are reported separately
as 'narrow' so they can be demoted rather than silently dropped.
"""

import io
import json
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BOOK_NOTES = os.path.join(VAULT_ROOT, "Data engineering Book knowledge", "notes")
OUT_DIR = os.path.join(VAULT_ROOT, "vault", "concepts")

TRACK_ROOTS = [
    os.path.join(VAULT_ROOT, "vault", "sql"),
    os.path.join(VAULT_ROOT, "vault", "python"),
    os.path.join(VAULT_ROOT, "vault", "shared"),
]

MIN_SOURCES = 3

# Each concept: display title + regex patterns (case-insensitive).
# Patterns are a HYPOTHESIS about vocabulary; the resulting mapping is MEASURED.
# Deliberately split terms that share a name but mean different things
# (sql-window-functions vs windowing-event-time; watermark variants).
CONCEPTS = {
    "idempotency-and-exactly-once": {
        "title": "Idempotency & Exactly-Once",
        "patterns": [r"idempoten", r"exactly[- ]once", r"at[- ]least[- ]once", r"at[- ]most[- ]once"],
    },
    "change-data-capture": {
        "title": "Change Data Capture & Change Tracking",
        "patterns": [r"change data capture", r"\bCDC\b", r"change tracking", r"change ?log"],
    },
    "incremental-vs-full-recompute": {
        "title": "Incremental vs Full Recompute",
        "patterns": [r"incremental refresh", r"full recompute", r"full refresh",
                     r"incrementaliz", r"incremental (load|ingestion|aggregation|processing)"],
    },
    "watermarks": {
        "title": "Watermarks",
        "patterns": [r"watermark"],
    },
    "late-data": {
        "title": "Late Data & Allowed Lateness",
        "patterns": [r"late data", r"allowed lateness", r"late[- ]arriving", r"late firing"],
    },
    "event-time-vs-processing-time": {
        "title": "Event Time vs Processing Time",
        "patterns": [r"event[- ]time", r"processing[- ]time", r"ingress time"],
    },
    "windowing-event-time": {
        "title": "Windowing (event-time buckets)",
        "patterns": [r"fixed window", r"sliding window", r"session window",
                     r"tumbl", r"windowing", r"validity window"],
    },
    "sql-window-functions": {
        "title": "SQL Window Functions",
        "patterns": [r"OVER\s*\(", r"PARTITION BY", r"ROW_NUMBER", r"DENSE_RANK",
                     r"\bRANK\(\)", r"\bLAG\(", r"\bLEAD\("],
    },
    "streams-and-tables": {
        "title": "Streams & Tables Duality",
        "patterns": [r"streams and tables", r"stream/table", r"stream and table",
                     r"data at rest", r"data in motion", r"time[- ]varying relation"],
    },
    "materialized-views": {
        "title": "Materialized Views",
        "patterns": [r"materialized view"],
    },
    "slowly-changing-dimensions": {
        "title": "Slowly Changing Dimensions",
        "patterns": [r"slowly changing", r"\bSCD\b", r"type 2 dimension"],
    },
    "keys-surrogate-natural": {
        "title": "Surrogate, Natural & Business Keys",
        "patterns": [r"surrogate key", r"natural key", r"business key", r"durable key",
                     r"primary key", r"foreign key", r"composite key"],
    },
    "dimensional-modeling": {
        "title": "Dimensional Modeling & Grain",
        "patterns": [r"\bgrain\b", r"fact table", r"dimension table", r"star schema",
                     r"snowflake schema", r"bus matrix"],
    },
    "deduplication": {
        "title": "Deduplication",
        "patterns": [r"dedup", r"duplicate"],
    },
    "partitioning-and-clustering": {
        "title": "Partitioning & Clustering",
        "patterns": [r"partition", r"clustering", r"z[- ]order", r"bucket"],
    },
    "file-layout-and-compaction": {
        "title": "File Layout & Compaction",
        "patterns": [r"small file", r"compaction", r"compact", r"OPTIMIZE", r"vacuum"],
    },
    "schema-evolution": {
        "title": "Schema Evolution & Compatibility",
        "patterns": [r"schema evolution", r"schema change", r"schema drift",
                     r"backward compatib", r"forward compatib"],
    },
    "data-quality": {
        "title": "Data Quality & Expectations",
        "patterns": [r"data quality", r"expectation", r"constraint", r"validat"],
    },
    "orchestration-and-dependencies": {
        "title": "Orchestration & Task Dependencies",
        "patterns": [r"orchestrat", r"\bDAG\b", r"dependenc", r"trigger rule"],
    },
    "backfill-and-reprocessing": {
        "title": "Backfill & Reprocessing",
        "patterns": [r"backfill", r"reprocess", r"\breplay", r"catchup", r"catch[- ]up"],
    },
    "checkpointing-and-recovery": {
        "title": "Checkpointing & Fault Recovery",
        "patterns": [r"checkpoint", r"fault[- ]toleran", r"snapshot", r"savepoint", r"recover"],
    },
    "state-management": {
        "title": "Persistent State Management",
        "patterns": [r"persistent state", r"stateful", r"state store", r"keyed state",
                     r"persistent timer"],
    },
    "medallion-layering": {
        "title": "Medallion / Layered Architecture",
        "patterns": [r"medallion", r"\bbronze\b", r"\bsilver\b", r"\bgold\b", r"staging (layer|table|zone)"],
    },
    "lineage-and-governance": {
        "title": "Lineage & Governance",
        "patterns": [r"lineage", r"governance", r"Unity Catalog", r"audit log", r"data mesh"],
    },
    "cost-management": {
        "title": "Cost Management & FinOps",
        "patterns": [r"\bFinOps\b", r"cost optimi", r"\bDBU\b", r"cost attribution",
                     r"budget polic", r"cost reduction"],
    },
    "batch-vs-streaming": {
        "title": "Batch vs Streaming",
        "patterns": [r"batch and streaming", r"batch vs", r"unbounded data", r"bounded data",
                     r"microbatch", r"micro[- ]batch"],
    },
    "joins": {
        "title": "Joins",
        "patterns": [r"inner join", r"outer join", r"semi join", r"anti join",
                     r"cross join", r"streaming join", r"fact[- ]to[- ]fact"],
    },
    "aggregation-and-combiners": {
        "title": "Aggregation & Combiners",
        "patterns": [r"combiner", r"GROUP BY", r"incremental combin", r"partial aggregat",
                     r"rollup", r"pre[- ]aggregat"],
    },
    "transactions-and-consistency": {
        "title": "Transactions & Consistency",
        "patterns": [r"\bACID\b", r"transaction", r"isolation level", r"serializab",
                     r"strong consistency", r"eventual consistency", r"linearizab"],
    },
    "replication-and-distribution": {
        "title": "Replication & Distributed Coordination",
        "patterns": [r"replication", r"\breplica\b", r"leader", r"follower", r"quorum", r"consensus"],
    },
    "testing-and-validation": {
        "title": "Testing & Pipeline Validation",
        "patterns": [r"unit test", r"integration test", r"\bpytest\b", r"DAG integrity",
                     r"reconcil", r"regression test"],
    },
    "security-and-access-control": {
        "title": "Security & Access Control",
        "patterns": [r"\bRBAC\b", r"encrypt", r"access control", r"masking",
                     r"credential", r"row[- ]level security", r"secret"],
    },
    "ingestion-patterns": {
        "title": "Ingestion Patterns & Connectors",
        "patterns": [r"Auto Loader", r"\bconnector\b", r"Fivetran", r"\bKafka\b",
                     r"Kinesis", r"Event Hubs", r"ingestion gateway"],
    },
    "serverless-and-compute": {
        "title": "Serverless & Compute Sizing",
        "patterns": [r"serverless", r"autoscal", r"auto[- ]scal", r"cluster polic",
                     r"job compute", r"all[- ]purpose compute"],
    },
}


def iter_markdown(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".obsidian", ".git")]
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def collect_files():
    """Returns list of (group, source_id, relpath, abspath)."""
    out = []
    if os.path.isdir(BOOK_NOTES):
        for src in sorted(os.listdir(BOOK_NOTES)):
            sdir = os.path.join(BOOK_NOTES, src)
            if not os.path.isdir(sdir):
                continue
            for p in iter_markdown(sdir):
                rel = os.path.relpath(p, VAULT_ROOT).replace("\\", "/")
                out.append(("book", src, rel, p))
    for troot in TRACK_ROOTS:
        if not os.path.isdir(troot):
            continue
        track = os.path.basename(troot)
        for p in iter_markdown(troot):
            rel = os.path.relpath(p, VAULT_ROOT).replace("\\", "/")
            out.append(("track", "track_" + track, rel, p))
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    files = collect_files()

    compiled = {
        cid: [re.compile(p, re.IGNORECASE) for p in meta["patterns"]]
        for cid, meta in CONCEPTS.items()
    }

    # concept -> source_id -> list of {relpath, hits}
    mapping = defaultdict(lambda: defaultdict(list))

    for group, source_id, rel, abspath in files:
        try:
            with io.open(abspath, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        for cid, regexes in compiled.items():
            hits = 0
            for rx in regexes:
                hits += len(rx.findall(text))
            if hits > 0:
                mapping[cid][source_id].append({"file": rel, "hits": hits})

    rows = []
    for cid, meta in CONCEPTS.items():
        by_source = mapping.get(cid, {})
        book_sources = sorted(s for s in by_source if not s.startswith("track_"))
        track_sources = sorted(s for s in by_source if s.startswith("track_"))
        n_chapters = sum(len(v) for v in by_source.values())
        total_hits = sum(e["hits"] for v in by_source.values() for e in v)
        rows.append({
            "id": cid,
            "title": meta["title"],
            "book_sources": book_sources,
            "track_sources": track_sources,
            "n_book_sources": len(book_sources),
            "n_chapters": n_chapters,
            "total_hits": total_hits,
            "by_source": {s: sorted(v, key=lambda e: -e["hits"]) for s, v in by_source.items()},
        })

    rows.sort(key=lambda r: (-r["n_book_sources"], -r["n_chapters"]))
    cross = [r for r in rows if r["n_book_sources"] >= MIN_SOURCES]
    narrow = [r for r in rows if r["n_book_sources"] < MIN_SOURCES]

    json_path = os.path.join(OUT_DIR, "_index.generated.json")
    with io.open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"min_sources": MIN_SOURCES, "files_scanned": len(files), "concepts": rows},
                  f, indent=2, ensure_ascii=False)

    md_path = os.path.join(OUT_DIR, "_index.generated.md")
    with io.open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Concept Spread Index (GENERATED — do not hand-edit)\n\n")
        f.write("> Regenerate with `python vault/state/build_concept_index.py`.\n")
        f.write("> Mapping is measured by regex scan, not recalled. Term lists are a hypothesis;\n")
        f.write("> the concept->chapter mapping below is evidence.\n\n")
        f.write("- Files scanned: **%d**\n" % len(files))
        f.write("- Cross-cutting threshold: appears in **>= %d** distinct book sources\n" % MIN_SOURCES)
        f.write("- Cross-cutting concepts found: **%d**\n" % len(cross))
        f.write("- Narrow (single/dual-source) concepts: **%d**\n\n" % len(narrow))

        f.write("## Cross-cutting concepts (hub candidates)\n\n")
        f.write("| Concept | Book sources | Chapters | Hits |\n|---|---|---|---|\n")
        for r in cross:
            f.write("| %s | %d (%s) | %d | %d |\n" % (
                r["title"], r["n_book_sources"], ", ".join(r["book_sources"]),
                r["n_chapters"], r["total_hits"]))

        f.write("\n## Narrow concepts (demote or fold into a hub)\n\n")
        f.write("| Concept | Book sources | Chapters | Hits |\n|---|---|---|---|\n")
        for r in narrow:
            f.write("| %s | %d (%s) | %d | %d |\n" % (
                r["title"], r["n_book_sources"], ", ".join(r["book_sources"]) or "none",
                r["n_chapters"], r["total_hits"]))

        f.write("\n## Per-concept chapter evidence\n\n")
        for r in rows:
            f.write("### %s\n\n" % r["title"])
            if not r["by_source"]:
                f.write("_No matches._\n\n")
                continue
            for s in sorted(r["by_source"]):
                files_s = r["by_source"][s]
                f.write("- **%s** (%d files): %s\n" % (
                    s, len(files_s),
                    ", ".join("`%s`(%d)" % (os.path.basename(e["file"]), e["hits"])
                              for e in files_s[:12])))
            f.write("\n")

    print("scanned %d files" % len(files))
    print("cross-cutting concepts (>=%d sources): %d" % (MIN_SOURCES, len(cross)))
    print("narrow concepts: %d" % len(narrow))
    print("wrote %s" % os.path.relpath(md_path, VAULT_ROOT).replace("\\", "/"))
    print("wrote %s" % os.path.relpath(json_path, VAULT_ROOT).replace("\\", "/"))


if __name__ == "__main__":
    main()
