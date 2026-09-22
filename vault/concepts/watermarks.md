# Watermarks

> **One line:** a system's running bet about "how complete is my data so far, in event time?" — the mechanism that lets a streaming pipeline decide when it's safe to emit a final answer.

**Spread:** 3/6 book sources · SQL + Python + shared tracks · verified via `vault/state/build_concept_index.py`

---

## ⚠️ Same word, different meaning — read this first

Your own `lakehouse-map.md` uses "watermark" for something related but **simpler** than what Streaming Systems means by the same word.

| Sense | Meaning | Where taught |
|---|---|---|
| **Incremental-load bookmark** | `MAX(timestamp)` from the last successful load — "have I already loaded this row?" | Your [[lakehouse-map]] |
| **Input-completeness metric** | A moving estimate of event time such that "we believe no more data older than X will arrive" — drives when a window can safely trigger | Streaming Systems |

The lakehouse-map sense is a *simplified special case* that assumes data arrives roughly in order. The Streaming Systems sense is the general theory that explains *why* your simple bookmark can be wrong — late-arriving data violates exactly the assumption your bookmark depends on.

---

## Where it appears

| Source | Chapter | Angle |
|---|---|---|
| Streaming Systems | [[ch03_watermarks\|Ch.3 Watermarks]] | The dedicated, exhaustive theoretical chapter (96 hits) — perfect vs. heuristic watermarks, input/output watermark propagation |
| Streaming Systems | [[ch02_what_where_when_how\|Ch.2 What/Where/When/How]] | Watermarks as the answer to the "when" question in the four-question streaming model |
| Streaming Systems | [[ch10_evolution_of_large_scale_data_processing\|Ch.10 Evolution]] | High vs. low watermarks — and a named real bug pattern: high watermarks (tracking newest-seen event time) can incorrectly discard data under skew |
| Streaming Systems | [[ch08_streaming_sql\|Ch.8 Streaming SQL]], [[ch09_streaming_joins\|Ch.9 Streaming Joins]] | Watermarks applied to SQL semantics and join completeness |
| DDIA | [[ch11_stream_processing\|Ch.11 Stream Processing]] | Lighter theoretical touch — the same completeness problem, less formalized |

### Your own track notes

- [[lakehouse-map]] — `Watermark (MAX timestamp) → Bronze→Silver → "Incremental load — track last loaded timestamp per source table"` — this is the simplified sense above; worth revisiting after reading Streaming Systems Ch.3

---

## The thread

Read your own `lakehouse-map.md` entry *before* Streaming Systems Ch.3, then again *after*. The "before" reading treats a watermark as a simple bookmark. The "after" reading exposes the hidden assumption: `MAX(timestamp)` only works as a safe incremental-load cutoff if you're confident no row with an earlier timestamp will arrive later. Streaming Systems Ch.3's entire apparatus (perfect vs. heuristic watermarks) exists because that assumption is usually false in the real world — which is exactly why [[late-data|late data]] handling is a separate, necessary concept.

## Related

[[event-time-vs-processing-time]] · [[late-data]] · [[windowing-event-time]] · [[checkpointing-and-recovery]]
