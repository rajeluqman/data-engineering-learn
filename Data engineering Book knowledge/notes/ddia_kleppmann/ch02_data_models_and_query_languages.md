# Ch.2 — Data Models and Query Languages

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 47–88 (42 pages, including endnotes) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[N]` new example · `[U]` unresolved

---

## 1. Concepts and definitions

**Data models as layered abstractions, the chapter's own four-layer stack [S]** (p47): (1) application developers model the real world as objects/data structures; (2) those structures are expressed in a general-purpose data model (JSON/XML/relational/graph); (3) database engineers represent that model as bytes on disk/memory/network; (4) hardware engineers represent bytes as electrical/optical/magnetic phenomena.

"each layer hides the complexity of the layers below it by providing a clean data model" (p48).

**Relational model origin and endurance [S]** (p47): proposed by Codd in 1970.

By the mid-1980s RDBMS/SQL "had become the tool of" choice for regular, structured data (p48). "The dominance of relational databases has lasted around 25–30 years — an eternity in computing history" (p48).

Its roots lie in mundane business use cases: "typically transaction processing" (entering sales or bank transactions, airline reservations, stock-keeping) "and batch processing" (customer invoicing, payroll, reporting) (p48).

**NoSQL's name is explicitly arbitrary, not descriptive [S]** (p49): "The term NoSQL is unfortunate, since it doesn't actually refer to any particular technology" — "it was intended simply as a catchy Twitter hashtag for a meetup on open source, distributed, non-relational databases in 2009."

The name has since been reinterpreted (p49): "it has been retroactively re-interpreted as Not Only" SQL.

**Four named driving forces behind NoSQL adoption [S]** (p49): need for greater scalability than relational databases easily achieve; preference for free/open-source software; specialized query operations poorly supported by the relational model; frustration with relational schema restrictiveness and desire for a more dynamic model. Predicted resolution: "polyglot persistence" — relational databases continuing alongside a variety of non-relational stores.

**Impedance mismatch, defined [S]** (p50): "if data is stored in relational tables, an awkward translation layer is required between the objects in the application code and the database model of tables, rows and columns. The disconnect between the models is sometimes called an impedance mismatch." ORMs "reduce the amount of boilerplate code... but they can't completely hide the differences between the two models."

**JSON documents have better locality than the normalized multi-table relational schema for self-contained tree data, the chapter's worked résumé example [S]** (p51): "If you want to fetch a profile in the relational example, you need to either perform multiple queries... or perform a messy multi-way join... In the JSON representation, all the relevant information is in one place, and one query is sufficient."

**Normalization's core rationale, precisely stated [S]** (p54): "The advantage of using an ID is that because it has no meaning to humans, it never needs to change... Anything that is meaningful to humans may need to change sometime in future — and if that information is duplicated, all the redundant copies need to be updated. That incurs overhead on writes, and risks inconsistencies... Removing such duplication is the key idea behind normalization."

**Many-to-one relationships don't fit document databases well, an explicit structural limitation [S]** (p54): "normalizing this data requires many-to-one relationships... which don't fit nicely into the document model. In relational databases, it's normal to refer to rows in other tables by ID, because joins are easy. In document databases, joins are not needed for one-to-many tree structures, and support for joins is often weak."

**Data tends toward interconnection over time, an explicit named growth pattern [S]** (p54): "even if the initial version of an application fits well in a join-free document model, data has a tendency of becoming more interconnected as features are" added — illustrated with the résumé example gaining organization/school entity references and many-to-many recommendation relationships.

**Historical parallel: IMS's hierarchical model prefigures document databases, with the same limitations [S]** (p56–57): IBM's IMS (1968, Apollo program origin) "represented all data as a tree of records nested within records, much like the JSON structure... it made many-to-many relationships difficult and it didn't support joins. Developers had to decide whether to duplicate (denormalize) data, or to manually resolve references... These problems of the 1960s were very much like the problems that developers are running into with document databases today."

**CODASYL/network model, an explicit generalization of the hierarchical model with a costly navigational burden [S]** (p57–58): "a record can have multiple parents," enabling many-to-many relationships, but accessed only via named "access paths" — chains of pointer-like links traversed by moving a cursor. "Even CODASYL committee members admitted that this was like navigating around an n-dimensional data space." Named structural cost: "if you didn't have a path to the data you wanted, you were in a difficult situation... It was difficult to make changes to an application's data model."

**The relational model's key insight — query optimizer built once, reused by all [S]** (p58): "you only need to build a query optimizer once, and then all applications that use the database can benefit from it. If you don't have a query optimizer, it's easier to hand-code the access paths for a particular query than to write a general-purpose optimizer — but the general-purpose solution wins in the long run."

Adding new indexes requires no query rewriting (p59): "you can just declare a new index, and queries will automatically use whichever indexes are most appropriate."

**Document databases and relational databases are not fundamentally different for many-to-many relationships, only for one-to-many nesting [S]** (p60): both resolve related items "by using a unique identifier, which is called a foreign key in the relational model, and a document reference in the document" model. "That identifier is resolved at read time, by using a join or follow-up queries. To date, document databases have not followed the path of CODASYL" (i.e., no navigational access-path querying) (p60).

**Which data model simplifies application code, an explicit decision rule [S]** (p60–61): document-like tree data (loaded whole) favors the document model, since "the relational technique of shredding... can lead to cumbersome schemas and unnecessarily complicated application code." Highly interconnected data reverses the preference: "the document model is very awkward, the relational model is acceptable, and graph models... are the most natural." A named document-model limitation: "you cannot refer directly to a nested item within a document" — you must navigate via something like "the second item in the list of positions for user 251," "much like an access path in the hierarchical model."

**Schema-on-read vs. schema-on-write, precisely defined and compared to type checking [S]** (p61): "schema-on-read (the structure of the data is implicit, and only interpreted when the data is read), in contrast with schema-on-write (the traditional approach... where the schema is explicit and the database ensures all data conforms to it)." Direct analogy: "Schema-on-read is similar to dynamic (run-time) type-checking... schema-on-write is similar to static (compile-time) type-checking." Document databases are named as misleadingly called "schemaless": "there is an implicit schema, but it is not enforced by the database."

**Schema change cost, an explicit myth correction with one named exception [S]** (p62): "Schema changes have a bad reputation of being slow and requiring downtime. This reputation is not entirely deserved: most relational database systems execute the ALTER TABLE statement in a few milliseconds — with the exception of MySQL, which copies the entire table on ALTER TABLE, which can mean minutes or even hours of downtime."

Bulk `UPDATE` on an existing large table is different (p62): "likely to be slow on any database, since every row needs to be re-written" — mitigated by defaulting new columns to NULL and filling them in lazily at read time, just as a document database would.

**Schema-on-read explicitly favored for heterogeneous data, two named conditions [S]** (p62): "there are many different types of objects, and it is not practical to put each type of object in its own table," or "the structure of the data is determined by external systems, over which you have no control, and which may change at any time."

**Document locality's real performance boundary, an explicit two-sided cost [S]** (p62): storage locality helps "if your application often needs to access the entire" document.

But (p62): "the database typically needs to load the entire document, even if you access only a small portion of it, which can be wasteful on large documents. On updates to a document, the entire document usually needs to be" rewritten.

Recommendation (p62): "keep documents fairly small, and avoid writes that increase the size of a" document.

**Locality is not unique to the document model, three named relational/columnar analogues [S]** (p63): Google Spanner's interleaved parent-table rows, Oracle's multi-table index cluster tables, and Bigtable's column-family concept (used in Cassandra/HBase) — "It's worth pointing out that the idea of grouping related data together for locality is not limited to the document model."

**Convergence of document and relational databases, an explicit forecast [S]** (p63–64): relational databases have added XML/JSON support (PostgreSQL 9.3+, IBM DB2 10.5+), and document databases like RethinkDB support relational-style joins. "It seems that relational and document databases are becoming more similar over time, and that is a good thing: the data models complement each other... A hybrid of the relational and document models is a good route for databases to take in future."

**Declarative vs. imperative query languages, precisely distinguished with worked parallel examples [S]** (p64–65): imperative code "tells the computer to perform certain operations in a certain order"; a declarative language "you just specify the pattern of the data you want... but not how to achieve that goal. It is up to the database system's query optimizer to decide." Concrete parallel worked examples given across three domains: a JS filtering loop vs. relational algebra `σ` selection vs. SQL `SELECT`; and CSS/XSL selectors vs. imperative DOM manipulation for web page styling.

**Declarative languages hide implementation details, enabling safe internal changes [S]** (p65): "If the database wants to reclaim unused disk space behind the scenes, it might need to move records around, changing the order in which the animals appear... The SQL example doesn't guarantee any particular ordering, and so it doesn't mind if the order changes... The fact that SQL is more limited in functionality gives the database much more room for automatic optimizations."

**Declarative languages parallelize better, tied to the multicore hardware trend [S]** (p65): "Today, CPUs are getting faster by adding more cores, not by running at significantly higher clock speeds than before. Imperative code is very hard to parallelize... Declarative languages have a better chance of getting faster in parallel execution, because they specify only the pattern of the results, but not the algorithm."

**CSS as a real-world declarative example outside databases, a fully worked side-by-side comparison [S]**: the task of visually highlighting the currently selected navigation item is expressed in 4 lines of CSS, an equivalent 4-line XSL template, versus roughly a dozen lines of imperative DOM JavaScript that the chapter calls "awful" (p65).

Two named concrete correctness problems afflict the imperative version: it fails to un-highlight when the selection changes without a page reload, and any future API improvement requires rewriting application code, whereas (p67) "browser vendors can improve the performance of CSS and XPath without breaking" compatibility.

**MapReduce querying, positioned as neither declarative nor imperative [S]** (p67): "MapReduce is neither a declarative query language, nor a fully imperative query API, but somewhere in between: the logic of the query is expressed with snippets of code, which are called repeatedly by the processing framework." It is based on the functional `map` and `reduce` primitives found in many functional programming languages.

**MapReduce's purity constraint, precisely defined [S]** (p69): map/reduce functions "must be pure functions, which means: they only use the data that is passed to them as input, they cannot perform additional database queries and they must not have any side-effects. These restrictions allow the database to run the functions anywhere, in any order, and re-run them on failure."

**MapReduce's usability problem, an explicit named driver for MongoDB's later declarative aggregation pipeline [S]** (p69–70): "you have to write two carefully coordinated JavaScript functions, which is often harder than writing a single query. Moreover, a declarative query language offers more opportunities for a query optimizer to improve the performance." The chapter's closing observation on this arc: "a NoSQL system may find itself accidentally reinventing SQL, albeit in disguise."

**Graph model definition and two element types [S]** (p70): a graph consists of "vertices (also known as nodes or entities) and edges (also known as relationships or arcs)." Named canonical use cases: social graphs, the web graph, road/rail networks — plus a named heterogeneous case, Facebook's single graph mixing people, locations, events, checkins, and comments as vertex types with many distinct edge label types.

**Property graph model, precisely defined by its two element schemas [S]** (p71–72): each vertex has a unique identifier, a set of outgoing edges, a set of incoming edges, and a properties key-value collection; each edge additionally has a tail vertex, a head vertex, and a relationship label. Three named structural advantages: unrestricted vertex-to-vertex connectivity (no schema constraint on what can relate to what); efficient bidirectional traversal via indexed tail/head vertex lookups; and multiple relationship types coexisting cleanly in one graph via edge labels.

**Graphs handle heterogeneous regional/administrative structure that relational schemas struggle with, the chapter's own worked example [S]** (p72–73): "different kinds of regional structures in different countries (France has départements and régions whereas the US has counties and states)," a country nested within a country, and "varying granularity of data (Lucy's current residence is specified as a city, whereas her place of birth is specified only at the level of a state)."

**Graphs support evolvability directly, an explicit named benefit [S]** (p73): "Graphs are good for evolvability: as you add features to your application, a graph can easily be extended to accommodate changes in your application's data structures" — illustrated with a hypothetical food-allergy extension to the résumé example.

**Cypher's declarative pattern-matching, defined by worked example [S]** (p73–75): a `MATCH` clause like `(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name:'United States'})` expresses "follow a WITHIN edge, zero or more times," analogous to a regex `*` operator, letting the query optimizer choose execution strategy (forward scan from people, or backward from the two named locations) "automatically... you can get on with writing the rest of your application."

**Variable-length graph traversal is awkward but possible in SQL, an explicit named comparison of verbosity [S]** (p74–76): the same emigration query takes 4 lines in Cypher versus a 29-line `WITH RECURSIVE` common table expression in SQL. "If the same query can be written in four lines in one query language, but requires 29 lines in another, that just shows that different data models are designed to satisfy different use cases."

**Graph databases are explicitly not the second coming of CODASYL, four named structural differences [S]** (p76–77): no schema restricting which vertex types can connect to which (vs. CODASYL's typed nesting schema); direct ID- or index-based vertex access (vs. CODASYL's access-path-only traversal); no defined ordering of vertices/edges to maintain (vs. CODASYL's ordered child sets); and native support for high-level declarative query languages (vs. CODASYL's imperative-only queries). `[D]`

**Triple-store model, defined and mapped onto the property graph model [S]** (p77): information as `(subject, predicate, object)` statements. A primitive-valued object is "equivalent to the key and value of a property on the subject vertex"; a vertex-valued object makes "the predicate... an edge in the graph, the subject is the tail vertex and the object is the head vertex."

**The semantic web is explicitly decoupled from the triple-store data model as a technique [S]** (p78–79): "The triple-store data model is completely independent of the semantic web — for example, Datomic is a triple-store that does not claim to have anything to do with the semantic web." The semantic web itself is candidly assessed: "over-hyped in the early 2000s, but so far hasn't shown any sign of being realized in practice," yet "there is also a lot of good work that has come out of the semantic web project. Triples can be a good internal data model for applications."

**RDF's URI-based predicates exist specifically to prevent naming collisions across combined datasets [S]** (p80): "you should be able to combine your data with someone else's data, and if they attach a different meaning to the word within or lives_in, you won't get a conflict because their predicates are actually" different URIs.

**SPARQL, positioned as Cypher's direct ancestor [S]** (p80): "It predates Cypher, and since Cypher's pattern-matching is borrowed from SPARQL, they look quite" similar.

The same emigration query is (p80) "even more concise in SPARQL than it is in" Cypher.

**Datalog, the oldest of the three graph query languages, framed as a foundation for future parallel programming [S]** (p81): "having been studied extensively by academics in the" 1980s.

Separately (p81): "it has been suggested that declarative languages based on Datalog may be the future for parallel programming, which has rekindled interest in Datalog" recently. Used in production by Datomic (native query language) and Cascalog (Hadoop-based Datalog implementation).

**Datalog's incremental rule-composition style, worked in full [S]** (p82–83): triples are written as `predicate(subject, object)`; derived predicates are defined via rules (`within_recursive`, `migrated`) that can reference other rules, applied repeatedly until no new facts are generated (the chapter's own worked fixpoint trace across Figure 2-6, deriving that Idaho is transitively within North America).

Trade-off named directly (p83): "it's a very powerful approach, because rules can" be combined and reused in different queries (p84). "It's less convenient for simple one-off queries, but it can cope better if your data is complex" (p84).

## 2. WHAT / WHY / WHEN

**WHAT:** A systematic comparison of three families of general-purpose data models — relational, document, and graph (property graph, triple-store, and their query languages Cypher/SPARQL/Datalog) — plus a parallel treatment of declarative vs. imperative query languages (SQL, CSS/XSL, MapReduce, MongoDB's aggregation pipeline), framed historically via the hierarchical/CODASYL/relational "great debate" of the 1970s. `[D]`

**WHY it matters:** the chapter's explicit thesis is that no data model is universally superior — each embodies assumptions that fit certain relationship shapes (one-to-many tree data → document; many-to-many highly interconnected data → graph; general-purpose with strong many-to-one/many-to-many support → relational) — and that history repeats: today's document-vs-relational debate directly mirrors the 1970s hierarchical-vs-network-vs-relational debate, with the relational model's core innovation (a reusable, general-purpose query optimizer replacing hand-coded access paths) being the reason it ultimately dominated both then and, likely, in the document-database convergence happening now. `[D]`

**WHEN to choose document over relational (p60–61):** when data is naturally tree-shaped (one-to-many, whole-document access patterns) and many-to-many relationships are rare or absent. **WHEN to choose graph over both (p70, p76):** when many-to-many, highly interconnected relationships are the norm rather than the exception, especially with heterogeneous vertex/edge types or variable-depth traversal needs. **WHEN schema-on-read beats schema-on-write (p62):** heterogeneous record types impractical to table-per-type, or externally-controlled, unpredictably-changing data structure.

## 3. Assumptions and prerequisites

- Forward-references storage engine internals to Ch.3 (p47, p63) and schema evolution/encoding formats to Ch.4 (p51, p62) — both not yet synthesized in this vault.
- Forward-references fault-tolerance and concurrency comparisons between relational/document databases to Ch.5 and Ch.7 (p59), and MapReduce's full distributed-execution treatment to Ch.10 (p68) — all not yet synthesized.
- Assumes Ch.1's reliability/scalability/maintainability framework only implicitly (e.g., evolvability is invoked directly for graphs, p73) without formal restatement.

## 4. Mechanism / key steps

**The chapter's own worked query-language comparison across three graph languages, identical semantics per query, the "who emigrated from the US to Europe" case (p73–83):** Cypher's `MATCH` pattern with a `*0..` variable-length traversal operator (4 lines) → SPARQL's near-identical triple-pattern syntax (even more concise) → SQL's `WITH RECURSIVE` common table expression achieving the same result via explicit iterative UNION-based set-building (29 lines) → Datalog's incremental rule definition and fixpoint application (`within_recursive`, `migrated`), which "takes a small step at a time" but composes across queries better than the other three.

**MapReduce's map/reduce mechanics, the chapter's own shark-sighting worked example (p68–69):** a `map` function is called once per matching document, emitting a `(key, value)` pair; all emitted pairs sharing a key are grouped; a `reduce` function is called once per group to fold the values into a single result — contrasted directly against the equivalent single-statement SQL `GROUP BY` query and MongoDB's later declarative aggregation-pipeline syntax for the same computation.

## 5. Trade-offs and limitations

- **Normalization vs. denormalization is an old, still-unresolved-by-fiat trade-off (§1, p54):** the chapter explicitly declines to take a side ("we will suspend judgement for now"), deferring the systematic treatment of caching/denormalization/derived data to Part III — a clear signal that this is a genuine engineering trade-off, not a settled question.
- **Document locality is a real but bounded win (§1, p62–63):** the same feature that makes whole-document reads fast makes partial reads wasteful and any size-increasing update expensive, since the whole document typically must be rewritten.
- **Datalog trades one-off query convenience for compositional power (§1, p83):** an explicit, named two-sided trade — Datalog's rule-based incrementalism is worse for simple ad hoc queries but scales better as query complexity and reuse needs grow.
- **Schema-on-read vs. schema-on-write is explicitly framed as contentious with no universal answer (§1, p61):** directly paralleled to the static-vs-dynamic-typing debate in programming languages, which the chapter treats as similarly unresolved.

## 6. Failure modes and edge cases

- **CODASYL's mandatory access-path navigation as a named historical failure mode (§1, p58):** any query lacking a pre-existing path to the needed data required rewriting substantial hand-written query code — a direct structural cause of CODASYL's eventual obsolescence.
- **MySQL's full-table-copy `ALTER TABLE` behavior, a named concrete exception to the "schema changes are fast" rule (§1, p62):** can mean "minutes or even hours of downtime" on large tables, unlike most other RDBMSs' millisecond-scale schema changes.
- **Naive imperative DOM manipulation losing correctness under state changes (§1, p66):** the chapter's own worked example shows a manually-applied highlight style persisting incorrectly after the underlying selection changes, specifically because the imperative code has no mechanism analogous to CSS's automatic re-evaluation.
- **Forcing highly interconnected data into a join-free document model (§1, p61, p54–55):** named directly as leading to "significantly more complex application code and worse performance" once many-to-many relationships become common, even if an application started out fitting the document model well.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the document-vs-relational-vs-graph decision framework (§1/§2, driven by relationship shape: tree/one-to-many vs. general-purpose vs. highly interconnected many-to-many) is directly reusable as a first-pass data-model selection heuristic for any new application in this vault's projects. `[D]`
- **Build:** the schema-on-read heterogeneous-data justification (§1, p62) is a directly reusable decision criterion for choosing document-style storage specifically when record types are numerous/externally-controlled, rather than as a general default.
- **Maintain:** the "data tends toward interconnection over time" pattern (§1, p54–55) is a directly reusable planning heuristic — expect a document-model application's relationship needs to grow more relational/graph-like as features accumulate, and plan schema evolution accordingly.
- **RCA:** unexpectedly slow or hours-long schema migrations are directly diagnosable against the named MySQL full-table-copy `ALTER TABLE` behavior (§6, p62) before assuming a general RDBMS limitation.
- **Optimization:** the locality-boundary rule for documents (§1, p62–63, "keep documents fairly small, avoid size-increasing writes") is a directly reusable, concrete document-database schema design guideline.

## 8. How to test / verify these claims

- The Cypher-vs-SQL-vs-Datalog verbosity comparison (§1, p74–83) is directly reproducible: implement the same variable-length-traversal query in all three languages against equivalent data and compare line counts and readability.
- The MySQL `ALTER TABLE` full-table-copy claim (§6, p62) is directly testable: run an `ALTER TABLE ADD COLUMN` on a large table in MySQL versus PostgreSQL and compare execution time.
- The MapReduce purity-and-parallelizability claim (§1, p69) is directly testable: confirm identical results when re-running the same map/reduce job with different node counts or execution order.
- The declarative-query-language reordering-safety claim (§1, p65) is testable by construction: modify physical row storage order in a relational table and confirm that unordered `SELECT` queries remain correct while comparing against what would happen to equivalent ordering-dependent imperative code.

## 9. Cross-references

- Directly extends Ch.1's evolvability concept (invoked explicitly for graph databases, p73) without contradiction.
- Forward-references (not yet synthesized in this vault): Ch.3 (storage engine internals, referenced for locality discussion), Ch.4 (schema evolution and encoding formats, referenced for JSON/XML encoding trade-offs), Ch.5 and Ch.7 (fault-tolerance and concurrency comparisons between relational and document databases), Ch.10 (MapReduce's full distributed-execution treatment and SQL-as-MapReduce-pipeline implementations), and Part III generally (denormalization, caching, derived data).
- No contradiction found with any other already-synthesized source in this vault; this chapter's data-model comparisons are complementary to (and do not overlap with) the dimensional-modeling-focused `kimball_dwtoolkit_3e` material, which operates one layer up (analytical schema design) from this chapter's concern (general-purpose storage/query data models).

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 2-1 through 2-6 (LinkedIn relational schema, JSON tree diagram, company-entity linking diagram, many-to-many résumé diagram, example graph-structured data diagram, Datalog fixpoint derivation diagram) | Structure and content described narratively above where load-bearing (§1, §4); full diagrams not reproduced verbatim. |
| Full worked code listings (Examples 2-1 through 2-11: JSON résumé document, property graph relational schema DDL, Cypher CREATE/MATCH queries, SQL recursive CTE, Turtle/RDF-XML triple representations, SPARQL query, Datalog facts/rules) | Representative excerpts and their semantics captured narratively in §1/§4; the complete verbatim code listings are not reproduced in full given their length, though every query's logic and comparative verbosity point is captured. |
| Closing "further data models" survey (genome sequence-similarity search, particle physics big-data, full-text search) (p84–85) | Named briefly as acknowledged scope boundaries of the chapter; not separately expanded since the chapter itself treats them as out of scope. |
| Full numbered reference list (47 references, p63–66 of chapter / p85–88 of PDF) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. Codd's original nonsimple domains proposal, footnote v) are captured inline in §1 with attribution context. |
