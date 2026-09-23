# Ch.3 — Storage and Retrieval

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 89–128 (40 pages, including endnotes) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[U]` unresolved

---

## 1. Concepts and definitions

**Chapter framing, a database's most fundamental job [S]** (p89): "a database needs to do two things: when you give it some data, it should store the data — and when you ask it again later, it should give the data back to you." This chapter examines that same relationship from Ch.2 "from the database's point of view."

**Log, defined generally, distinct from application logs [S]** (p91, footnote i): "log is used in the more general sense: an append-only sequence of records. It doesn't have to be human-readable, it might be binary and intended only for other programs to read."

**Worked minimal key-value store, the chapter's own two-Bash-function example [S]**: `db_set` appends the key and value to a file; `db_get` greps for the key and returns the last match (p90).

This demonstrates two asymmetric performance facts directly: appending is fast — "appending to a file is generally very efficient" (p91).

Lookup is O(n) (p91): "if you double the number of records n in your database, a lookup takes twice as long."

**Index defined as a derived, overhead-carrying structure [S]** (p91): "An index is an additional structure that is derived from the primary data... Maintaining additional structures is overhead, especially on writes... Any kind of index usually slows down writes, because the index also needs to be updated every time data is written." This produces the chapter's central storage trade-off: "well-chosen indexes speed up read queries, but every index slows down writes," which is why databases require indexes to be chosen deliberately, not applied universally by default.

**Hash index mechanics [S]** (p92): "keep an in-memory hash map where every key is mapped to a byte offset in the data file — the location at which the value can be found." Lookups become: consult the hash map for the offset, seek, read.

**Bitcask, the worked concrete implementation [S]** (p92–93): "Bitcask offers high-performance reads and writes, subject to the requirement that all the keys fit in the available RAM." Values can exceed available memory since "they can be loaded from disk with just one disk seek." Named ideal workload: "the value for each key is updated frequently" with "not too many distinct keys" (e.g. a cat-video play-count counter).

**Compaction and segment merging, defined and justified [S]** (p93): "Compaction means throwing away duplicate keys in the log, and keeping only the most recent update for each key." Merging happens concurrently with serving requests: "The merging and compaction can be done in a background thread, and while it is going on, we can still continue to serve read and write requests as normal, using the old segment files."

**Five named practical issues in a real log-structured hash-index implementation [S]** (p94–95): file format (binary length-prefixed strings beat CSV); deleting records via a tombstone marker; crash recovery (Bitcask snapshots each segment's hash map to disk for fast reload); partially written records (checksums detect and discard corrupted tail writes); concurrency control (one writer thread; append-only segments are safely read by many threads concurrently).

**Append-only design's three named advantages over in-place updates [S]** (p95): sequential writes are faster than random writes on both spinning disks and SSDs; concurrency/crash-recovery are simpler since there's no risk of "a file containing part of the old and part of the new value spliced together"; merging avoids data-file fragmentation over time.

**Hash index's two named limitations [S]** (p95–96): the hash table must fit entirely in memory ("unfortunately it is difficult to make an on-disk hash map perform well"); and "range queries are not efficient... you'd have to look up each key individually."

**SSTable, defined by its sort-order requirement [S]** (p96): a log segment format requiring "the sequence of key-value pairs is sorted by key," with each key appearing at most once per merged segment. Three named advantages over hash-indexed segments: (1) merging becomes a simple, memory-independent mergesort-style pass; (2) the in-memory index needed can be sparse — "one key for every few kilobytes of segment file is sufficient" since scanning a small span is fast; (3) records scanned together can be grouped into a compressible block, since "disk bandwidth is usually a worse bottleneck than CPU."

**Memtable and the full LSM-tree write path, worked step by step [S]** (p99): incoming writes go to an in-memory sorted tree (the memtable, e.g. a red-black tree); once it exceeds a size threshold (typically a few megabytes) it is flushed to disk as a new SSTable segment; reads check the memtable, then progressively older on-disk segments; a background process periodically merges and compacts segments. A separate append-only write-ahead log protects against losing unflushed memtable contents on crash, discarded once its memtable is safely flushed.

**LSM-Tree, its name and lineage, and Bloom filter optimization [S]** (p99–100): the technique underlies LevelDB, RocksDB, Cassandra, HBase (inspired by Google's Bigtable paper, which coined "SSTable" and "memtable"), and was formally named Log-Structured Merge-Tree by Patrick O'Neil et al. A named performance gap and its fix: "the LSM-tree algorithm can be slow when looking up keys that do not exist in the database" (must check every segment back to the oldest) — mitigated by LevelDB's Bloom filters, "a memory-efficient data structure for approximating the contents of a set" that "can tell you if a key does not appear in the database."

**B-tree, defined by its page-based, fixed-size-block design philosophy [S]** (p100–101): "B-trees break the database down into fixed-size blocks or pages, traditionally 4 kB in size, and read or write one page at a time. This corresponds more closely to the underlying hardware." Introduced in 1970, called "ubiquitous" within a decade, and remains "the standard index implementation in almost all relational databases." Guarantees logarithmic height: "a B-tree with n keys always has a height of O(log n)."

**B-tree page-splitting mechanism, worked in full [S]** (p101): "If there isn't enough free space in the page to accommodate the new key, it is split into two half-full pages, and the parent page is updated to account for the new subdivision of key" ranges.

**Write-ahead log (WAL), defined by its crash-safety role [S]** (p102): "an append-only file to which every B-tree modification must be written before it can be applied to the pages of the tree itself. When the database comes back up after a crash, this log is used to restore the B-tree back to a consistent state." Consequence: "A B-tree index must therefore write every piece of data at least twice: once to the log, and once to the tree page itself (and perhaps again as pages are split)."

**Concurrency control on B-trees requires explicit locking, unlike log-structured segments [S]** (p102–103): "careful concurrency control is required if multiple threads are going to access the B-tree at the same time... typically done by protecting the tree's data structures with latches (lightweight locks). Log-structured approaches are simpler in this regard, because they do all the merging in the background without interfering with incoming queries."

**Four named B-tree optimizations [S]** (p103): copy-on-write pages (LMDB) instead of WAL-based in-place overwrite, doubling as a concurrency-control mechanism; abbreviated interior-page keys to increase branching factor and reduce tree height; deliberate sequential-on-disk leaf-page layout for range-scan efficiency (harder to maintain than in LSM-trees, which naturally rewrite large contiguous segments during merging); sibling pointers on leaf pages for order-preserving scans without backtracking to parent pages; fractal-tree B-tree variants borrowing log-structured ideas to reduce seeks.

**B-trees vs. LSM-trees, a fully worked comparison with no declared universal winner [S]** (p103–104): "As a rule of thumb, LSM-trees are typically faster for writes, whereas B-trees are thought to be faster for reads. Actual benchmarks are often inconclusive and sensitive to the details of the workload." Named LSM-tree downside: background compaction can interfere with concurrent request latency, "especially" visible "at higher percentiles," where "B-trees can be more predictable." Named B-tree advantage: "each key exists in exactly one place in the index," which makes B-trees attractive for implementing range-lock-based transaction isolation directly on the index structure. Closing verdict: "There is no quick and easy rule for determining which type of storage engine is better for your use case, so it is worth testing empirically."

**Secondary indexes, defined and distinguished from primary key indexes [S]** (p104–105): unlike a primary key index, "keys are not unique" — resolved either by storing a list of matching row identifiers per key (like a postings list) or by appending a row identifier to make each key unique. Both B-trees and log-structured indexes can serve as secondary indexes.

**Heap file vs. clustered index, precisely distinguished with a named trade-off [S]** (p105): a heap file stores the actual row data "in no particular order" (it may be append-only, or it may keep track of deleted rows in order to overwrite them with new data later), with all indexes pointing to a shared location — avoiding duplication across multiple secondary indexes, at the cost of an extra hop per read. A clustered index (e.g. MySQL InnoDB's primary key) stores the row directly within the index, eliminating that hop.

A covering index is named as an explicit middle ground (p105): it "stores some of a table's columns within the" index, letting some queries be answered from the index alone. All duplication-based approaches trade write overhead and transactional-consistency complexity for read speed.

**Concatenated (multi-column) index, defined by worked analogy [S]** (p106): "combines several fields into one key by appending one column to another... like an old-fashioned paper phone book, which provides an index from (lastname, firstname) to phone number" — usable for last-name-only or last-name-plus-first-name lookups, but "useless if you want to find all the people with a particular first name."

**Multi-dimensional index need, a concrete named geospatial failure case for standard B-tree/LSM indexes [S]** (p106): a standard index "can give you either all the restaurants in a range of latitudes... or all the restaurants in a range of longitudes... but not both simultaneously." Named solutions: space-filling curves mapping 2D into a single B-tree-indexable dimension, or specialized structures like R-trees (used by PostGIS via PostgreSQL's Generalized Search Tree facility). A named generalization beyond geography: multidimensional indexes on arbitrary attribute tuples, e.g. `(date, temperature)` for efficient weather-data range queries (used by HyperDex).

**Fuzzy indexing, defined by contrast with exact-match indexing [S]** (p107): standard indexes support exact or sorted-range lookups but not "similar keys, such as misspelled words." Lucene supports edit-distance search via an in-memory finite-state-automaton term index (rather than LevelDB's sparse offset list), which "can be transformed into a Levenshtein automaton" for efficient bounded-edit-distance search.

**In-memory databases, motivated by RAM cost decline, with a corrected explanation of their speed advantage [S]** (p107–108): "Counter-intuitively, the performance advantage of in-memory databases is not due to the fact that they don't need to read from disk. Even a disk-based storage engine may never need to read from disk if you have enough memory, because the operating system caches recently used disk blocks in memory anyway. Rather, they can be faster because they can avoid the overheads of encoding in-memory data structures in a form that can be written to disk."

**In-memory database durability techniques, four named mechanisms [S]** (p107–108): special battery-powered RAM (rare), a change log written to disk, periodic snapshots to disk, or replication to other machines — "Despite writing to disk it's still an in-memory database, because the disk is merely used as an append-only log for durability, and reads are served entirely from memory."

**Anti-caching, a named research direction extending in-memory architectures beyond RAM size [S]** (p108): evicts least-recently-used data to disk when memory is full, reloading on access — "similar to what operating systems do with virtual memory and swap files, but the database can manage memory more efficiently than the OS, as it can work at the granularity of individual records rather than entire memory pages." Still requires "indexes to fit entirely in memory."

**Transaction, defined broadly, decoupled from ACID [S]** (p109, boxed note): "A transaction needn't necessarily have ACID... properties. Transaction processing just means allowing clients to make low-latency reads and writes — as opposed to batch processing jobs, which only run" periodically, for example once per day.

**OLTP vs. OLAP, defined by access pattern, with a full comparison table [S]** (p109–110): OLTP fetches "a small number of records per query... by key," writes are "random-access, low-latency" from user input, representing "latest state of data," at gigabyte-to-terabyte scale. OLAP "scan[s] over a huge number of records" computing aggregates, writes arrive via "bulk import (ETL) or event stream," representing "history of events that happened over time," at terabyte-to-petabyte scale.

**Data warehouse's core purpose, an explicit isolation rationale [S]** (p110–111): OLTP databases are "closely guarded" and DBAs are "usually reluctant to let business analysts run ad-hoc analytic queries on an OLTP database, since those queries are often expensive... which can harm the performance of concurrently executing transactions." A data warehouse is "a separate database that analysts can query to their heart's content, without affecting OLTP operations," populated via ETL (Extract-Transform-Load).

**Star schema, defined and directly cross-referenced to Kimball [S]** (p111–112): "a so-called fact table... Each row of the fact table represents an event that occurred at a particular time," with "dimension tables" representing "the who, what, where, when, how and why of the event," referenced by foreign key. "The name star schema comes from the fact that when the table relationships are visualized, the fact table is in the middle, surrounded by its foreign keys to dimension tables like rays of a star." Snowflake schema is named as the further-normalized variant, "more normalized than star schemas, but... star schemas are often preferred because they are simpler for analysts to work with." Fact tables at large enterprises can reach "tens of petabytes" (Apple, Walmart, eBay named directly).

**Column-oriented storage, motivated by real analytic query access patterns [S]** (p115): "a typical data warehouse query only accesses 4 or 5" columns "at one time" — SELECT-star queries are rarely needed for analytics — even though fact tables commonly exceed 100 columns.

"The idea behind column-oriented storage is simple: don't store all the values from one row together, but store all the values from each column together instead. If each column is stored in a separate file, a query only needs to read and parse those columns" that are used in that query (p115).

**Column compression via bitmap encoding, worked mechanism [S]** (p114–116): for a column with n distinct values, build n bitmaps (one bit per row, 1 if the row has that value). Small-n bitmaps (e.g. ~200 country codes) can be stored densely; larger-n bitmaps are typically sparse and further compressed via run-length encoding. Named query benefit: `WHERE product_sk IN (...)` becomes a bitwise OR across the relevant bitmaps; a multi-column `AND` predicate becomes a bitwise AND across two columns' bitmaps, valid precisely (p118) because the columns contain the rows in the same order.

**Vectorized processing, defined by its CPU-cache-locality rationale [S]** (p116): "the query engine can take a chunk of compressed column data that fits comfortably in the CPU's L1 cache, and iterate through it in a tight loop... Column compression allows more rows from a column to fit in the same amount of L1 cache. Operators... can be designed to operate on such chunks of compressed column data directly."

**Sort order in column storage, defined by whole-row (not per-column) sorting and its compression side effect [S]** (p118): "it wouldn't make sense to sort each column independently, because then we would no longer know which items in the columns belong to the same row."

A named compression consequence follows (p119): "That compression effect is strongest on the first sort key. The second and third sort key will be more jumbled up, and thus not have such long runs of repeated values."

But (p119) having the first few columns sorted is still a win overall.

**Multiple sort orders, a named C-Store/Vertica innovation exploiting mandatory replication [S]** (p118–119): "Data needs to be replicated to multiple machines anyway, so that you don't lose data if one machine fails. You might as well store that redundant data sorted in different ways, so that when you're processing a query, you can use the version that best fits the query pattern."

**Writing to column-oriented storage, the LSM-tree reuse pattern [S]** (p119–120): "An update-in-place approach, like B-trees use, is not possible with compressed columns... Fortunately, we have already seen a good solution earlier in this chapter: LSM-trees. All writes first go to an in-memory store... When enough writes have accumulated, they are merged with the column files on disk." Vertica implements exactly this pattern.

**Materialized view, precisely distinguished from a virtual view [S]** (p120): "a materialized view is an actual copy of the query results, written to disk, whereas a virtual view is just a shortcut for writing queries." Named cost: "such updates make writes more expensive, which is why materialized views are not often used in OLTP databases. In read-heavy data warehouses they can make more sense."

**Data cube (OLAP cube), defined and its central trade-off named explicitly [S]** (p121): "It is a grid of aggregates grouped by different dimensions."

Pre-summing along each dimension makes certain queries fast (p121): "because they have effectively been pre-computed." A query for totals along the right dimension needs "no need to scan millions of rows" (p122).

Named disadvantage (p122): "it doesn't have the same flexibility as querying the raw data" — a query needing a dimension not baked into the cube (e.g. filtering by exact price threshold) cannot be answered from it.

"Most data warehouses therefore try to keep as much raw data as possible, and use aggregates such as data cubes only as a performance boost for certain queries" (p122).

## 2. WHAT / WHY / WHEN

**WHAT:** A systematic tour of storage engine internals across two axes — indexing structures for OLTP (hash indexes/Bitcask, SSTables/LSM-trees, B-trees, and specialized indexes: secondary, multi-column, fuzzy) and column-oriented storage for OLAP (star schemas, columnar layout, bitmap compression, sort orders, materialized views/data cubes) — explicitly framed as the database-internals counterpart to Ch.2's application-facing data model discussion. `[D]`

**WHY it matters:** the chapter's explicit goal is to equip application developers (not storage-engine implementers) with enough internal-mechanics vocabulary to choose and tune the right storage engine for a given workload, grounded in the recurring observation that OLTP and OLAP have fundamentally different bottlenecks (disk seek time for OLTP's small-key lookups vs. disk bandwidth for OLAP's massive sequential scans), which drives essentially every design choice discussed. `[D]`

**WHEN to choose LSM-trees over B-trees (p103–104):** favor LSM-trees for high, sustained write throughput (turning random writes into sequential ones) and range-scan-friendly sorted storage; favor B-trees when read predictability (avoiding compaction-induced tail latency) and single-location-per-key transactional locking semantics matter more. **WHEN to build a data cube (p121):** only as a targeted performance boost for known, stable aggregate queries, never as a replacement for retaining raw fact data, since any dimension not baked into the cube becomes permanently unanswerable from it.

## 3. Assumptions and prerequisites

- Directly extends Ch.2's relational schema example (Figure 2-1, the LinkedIn résumé schema), reused to motivate secondary indexes on `user_id` (p104). `[S]`
- Directly cross-references `kimball_dwtoolkit_3e` by name and edition for the star schema / dimensional modeling technique, cited in-text on p112 and listed in the reference list (p126): "Ralph Kimball and Margy Ross: The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling, 3rd edition" — confirming this vault's two synthesized sources directly cite each other's subject matter. `[S]`
- Forward-references transaction isolation and range locks to Ch.7 (p104), snapshot isolation and copy-on-write concurrency control to a later chapter section (p103), and batch processing (Hadoop/MapReduce) to Ch.10 (p109) — all not yet synthesized in this vault.
- Assumes Ch.1's percentile-based performance vocabulary (p50 percentiles), directly reused when discussing LSM-tree compaction's tail-latency impact (p104). `[S]`

## 4. Mechanism / key steps

**Full LSM-tree read/write path, the chapter's own worked design (p92–99):** write → append to on-disk write-ahead log (crash safety) → insert into in-memory sorted memtable → once memtable exceeds threshold, flush to disk as a new sorted, compressed SSTable segment (discard the corresponding WAL) → background process merges and compacts segments mergesort-style, discarding superseded/deleted (tombstoned) values, using a sparse in-memory offset index (one entry per few KB) since data is sorted → optionally maintain Bloom filters to short-circuit lookups for genuinely absent keys → read → check memtable, then progressively older on-disk segments in turn, using per-segment sparse indexes to jump near the target key and scan forward.

**Full B-tree read/write path (p100–103):** read → start at the root page, use its k keys and k+1 child-page references to descend into the correct key-range subtree, repeat until reaching a leaf page containing the value or a reference to it → write (update) → locate leaf page, modify value, write page back to disk → write (insert causing overflow) → split the overfull page into two half-full pages, update the parent page's range boundaries and references (recursively splitting ancestors if needed) → crash safety → every modification is first written to an append-only write-ahead log before being applied to the tree pages themselves, enabling post-crash tree reconstruction.

**Bitmap-encoded bitwise query execution, the chapter's own worked example (p115–116):** `WHERE product_sk IN (30, 68, 69)` → load the three per-value bitmaps → compute bitwise OR. `WHERE product_sk = 31 AND store_sk = 3` → load the two relevant bitmaps → compute bitwise AND, valid because both columns' bitmaps share the same row ordering, so the kth bit always refers to the same underlying row across all columns.

## 5. Trade-offs and limitations

- **Hash indexes trade range-query capability and unbounded key-set scaling for simplicity and raw speed (§1, p95–96):** an explicit, named two-sided limitation — the entire key set must fit in memory, and no efficient range scan is possible.
- **B-trees vs. LSM-trees is explicitly declared workload-dependent with no universal winner (§1, p103–104):** the chapter's own closing verdict ("no quick and easy rule... worth testing empirically") is a rare, direct refusal to prescribe a default choice.
- **Column-oriented storage optimizes reads at a real, named write cost (§1, p119–120):** "An update-in-place approach, like B-trees use, is not possible with compressed columns," requiring the same LSM-tree-style buffered-write reuse pattern to make writes tractable at all.
- **Materialized views and data cubes trade write cost and query flexibility for read speed on known query shapes (§1, p120–121):** both require additional update work on every underlying data change, and data cubes specifically become useless for queries touching a dimension not built into the cube.
- **Clustered/covering indexes trade storage and write overhead for read speed via duplication (§1, p105):** an explicit generalization of the store-once-vs-duplicate trade-off already seen in denormalization discussions.

## 6. Failure modes and edge cases

- **Naive O(n) linear-scan lookup at large record counts (§1, p90):** the chapter's own worked db_get example demonstrates this directly — "terrible performance if you have a large number of records."
- **On-disk hash maps performing poorly in practice (§1, p95–96):** named directly as requiring "a lot of random access I/O," being "expensive to grow when it becomes full," and needing "fiddly logic" for hash collisions — a structural reason hash indexes stay in-memory-only in practice.
- **Crashes mid-write corrupting B-tree structure across multiple pages (§1, p102):** named directly — "if the database crashes after writing only some of the pages, you end up with a corrupted index (e.g. there may be an orphan page which is not a child of any parent)" — the direct motivation for the write-ahead log.
- **LSM-tree compaction causing high-percentile latency spikes (§1, p104):** an explicit, named operational failure mode distinct from average-case performance — "it can easily happen that a request needs to wait while the disk finishes an expensive compaction operation."
- **Sorting each column independently in a column store (§1, p117):** named directly as a conceptual error that would destroy the ability to reconstruct rows, since row identity in columnar storage depends entirely on shared positional ordering across all column files.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the OLTP-vs-OLAP access-pattern comparison table (§1, p109–110) is directly reusable as a first-pass storage-engine-family selection framework for any new data system in this vault's projects. `[D]`
- **Build:** the full LSM-tree and B-tree read/write mechanics (§4) are directly reusable reference implementations when evaluating or tuning a specific database's storage engine choice (e.g. RocksDB vs. InnoDB) for a given workload.
- **Maintain:** the "no universal winner, benchmark empirically" principle for B-trees vs. LSM-trees (§1, p104) is a directly reusable operating discipline — avoid defaulting to a storage engine choice based on reputation alone when workload-specific benchmarking is feasible.
- **RCA:** unexplained high-percentile latency spikes on an LSM-tree-backed database (§6, p104) are directly diagnosable against the documented background-compaction interference pattern before assuming an application-level cause.
- **Optimization:** the bitmap-encoding/vectorized-processing techniques (§1, p114–116) are directly reusable optimization patterns for any analytic workload with low-cardinality filter columns, and the star-schema-to-column-store pairing (§1, p111–116) is a directly reusable architectural pattern already consistent with this vault's `kimball_dwtoolkit_3e` dimensional modeling material.

## 8. How to test / verify these claims

- The O(n) linear scan claim (§1, p90) is directly reproducible: time `db_get` against progressively larger synthetic databases and confirm roughly linear lookup-time growth.
- The bitmap bitwise-AND/OR query technique (§1, p115–116) is directly testable by construction: build the described per-value bitmaps for a small dataset and confirm the AND/OR results match a naive row-scan filter.
- The B-tree write-ahead-log crash-recovery claim (§1, p102) is testable via fault injection: simulate a crash mid-page-write and confirm the WAL-based replay restores a consistent tree state.
- The LSM-tree vs. B-tree write/read throughput rule of thumb (§1, p103–104) is directly benchmarkable: run identical write-heavy and read-heavy workloads against a representative LSM-tree engine (e.g. RocksDB) and B-tree engine (e.g. a standard RDBMS) and compare throughput and tail latency.

## 9. Cross-references

- Directly extends [[ch02_data_models_and_query_languages|Ch.2]]'s relational schema example for the secondary-index discussion (p104), and explicitly cites `kimball_dwtoolkit_3e` (The Data Warehouse Toolkit, 3rd edition) by name for the star schema / dimensional modeling technique (p112) — a direct, source-confirmed link between this vault's two major synthesized sources on the exact same technique (star schema / conformed fact-and-dimension modeling), with full consistency: this chapter's fact/dimension table definitions match the terminology already synthesized from `kimball_dwtoolkit_3e` [[ch01_reliable_scalable_maintainable_applications|Ch.1]]–[[ch03_storage_and_retrieval|Ch.3]].
- Forward-references (not yet synthesized in this vault): [[ch07_transactions|Ch.7]] (transaction isolation, range locks, snapshot isolation/copy-on-write), and [[ch10_batch_processing|Ch.10]] (batch processing, Hadoop, MapReduce as a SQL-on-Hadoop foundation).
- No contradiction found with any already-synthesized source.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 3-1 through 3-12 (hash-indexed log diagram, compaction/merging diagrams, SSTable merge and sparse-index diagrams, B-tree lookup/split diagrams, star schema ERD, column-oriented storage layout, bitmap encoding diagram, data cube diagram) | Structure and content described narratively above where load-bearing (§1, §4); full diagrams and complete sample data tables not reproduced verbatim. |
| Full worked star-schema example's complete dimension table contents (Figure 3-9, p91–92) | Representative structure (fact_sales plus dim_product/store/promotion/date/customer) captured in §1; full sample row data not reproduced verbatim. |
| Full SQL-on-Hadoop and commercial data warehouse vendor lists (p111, ~12 named products) | Representative names captured in §1 framing; the complete list is not separately reproduced since it is enumerative vendor context, not a technical claim requiring synthesis. |
| Full numbered reference list (57 references, p101–105 of chapter / p123–127 of PDF) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. Bigtable's coining of "SSTable"/"memtable," the original LSM-Tree paper, the star schema's Kimball attribution) are captured inline in §1 with attribution context. |
