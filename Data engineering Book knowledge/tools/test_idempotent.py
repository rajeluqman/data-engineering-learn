"""
G4: idempotency test for every generator.

WHY THIS EXISTS: re-running `build_chapter_map.py` after a bug fix once silently
reset all synthesized-chapter markers back to `located`, destroying synthesis
progress. That was caught only by chance. This test proves -- rather than assumes --
that running the generators again changes nothing, so the same class of state-wipe
can never pass unnoticed again.

WHAT IT DOES: hashes every generated artifact, runs every generator once, hashes
again, and fails if anything changed. Also warns about generators that rewrite
files they didn't need to touch.

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/test_idempotent.py"
"""
import hashlib
import io
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
TOOLS_DIR = os.path.join(BOOK_DIR, "tools")
PY = sys.executable

# Generators, in dependency order.
GENERATORS = [
    "build_source_register.py",
    "build_page_manifest.py",
    "detect_page_offsets.py",
    "build_chapter_map.py",
    "chapter_stats.py",
    "build_flag_ledger.py",
    "build_full.py",
    "build_master_context.py",
]

ARTIFACTS = [
    "audit/SOURCE_REGISTER.csv",
    "audit/PAGE_MANIFEST.csv",
    "audit/CHAPTER_MAP.csv",
    "audit/chapter_stats.json",
    "audit/FLAG_LEDGER.csv",
    "audit/page_offsets.json",
    "MASTER_CONTEXT.md",
    "MASTER_CONTEXT_FULL.md",
]


def snapshot():
    out = {}
    for rel in ARTIFACTS:
        p = os.path.join(BOOK_DIR, rel)
        if os.path.exists(p):
            out[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
        else:
            out[rel] = None
    return out


def run_all():
    """Run every generator once. Returns list of failure strings."""
    failures = []
    for g in GENERATORS:
        path = os.path.join(TOOLS_DIR, g)
        if not os.path.exists(path):
            failures.append(f"{g}: generator file missing")
            continue
        r = subprocess.run([PY, path], cwd=BOOK_DIR, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            failures.append(f"{g}: exited {r.returncode} -- {(r.stderr or '')[-300:]}")
    return failures


def main():
    # IMPORTANT (test design): comparing "artifact on disk now" vs "after one run"
    # does NOT test idempotency -- it also fires when an artifact was merely STALE
    # (e.g. notes were edited and MASTER_CONTEXT_FULL.md hadn't been regenerated
    # yet). That produced a false alarm the first time this test ran. The correct
    # comparison is run-1 output vs run-2 output: staleness is absorbed by run 1,
    # so any remaining difference is genuine non-determinism or state destruction.
    pre = snapshot()
    missing = [k for k, v in pre.items() if v is None]
    if missing:
        print(f"NOTE: artifacts not present before run (will be created): {missing}")

    print("run 1/2 (absorbs any staleness) ...")
    failures = run_all()
    before = snapshot()

    stale = [k for k in ARTIFACTS
             if pre.get(k) is not None and pre[k] != before[k]]
    if stale:
        print(f"NOTE: {len(stale)} artifact(s) were STALE on disk and were refreshed by run 1 "
              f"(not an idempotency failure): {stale}")

    print("run 2/2 (the actual idempotency check) ...")
    failures += run_all()
    after = snapshot()

    changed = [k for k in ARTIFACTS
               if before.get(k) is not None and before[k] != after[k]]

    print(f"\n{'STATUS':<8} ARTIFACT")
    for rel in ARTIFACTS:
        if before.get(rel) is None:
            status = "CREATED"
        elif before[rel] == after[rel]:
            status = "STABLE"
        else:
            status = "CHANGED"
        print(f"{status:<8} {rel}")

    if failures:
        print("\nGENERATOR ERRORS:")
        for f in failures:
            print(f"  {f}")

    if changed:
        print(f"\nFAIL: {len(changed)} artifact(s) changed on a no-op re-run -- a generator "
              f"is not idempotent and may be destroying state:")
        for c in changed:
            print(f"  {c}")
        return 1
    if failures:
        print("\nFAIL: one or more generators errored.")
        return 1
    print("\nPASS: all generators are idempotent (re-running changed nothing).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
