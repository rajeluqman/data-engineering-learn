# Ch.4 — Encoding and Evolution

**Source:** `ddia_kleppmann` (Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly, 2017)
**PDF page range:** 129–162 (34 pages, including endnotes) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`
**Synthesis status:** `synthesized` (this session)
**Provenance key:** `[S]` source-supported · `[D]` derived interpretation · `[U]` unresolved

---

## 1. Concepts and definitions

**Backward vs. forward compatibility, precisely defined [S]** (p130): "Backward compatibility: Newer code can read data that was written by older code. Forward compatibility: Older code can read data that was written by newer code." Backward compatibility is named as the easier of the two: "as author of the newer code, you know the format of data written by older code." Forward compatibility is harder "because it requires older code to ignore additions made by a newer version of the code."

**Rolling upgrade, defined and its evolvability payoff named directly [S]** (p130): "deploying the new version to a few nodes at a time, checking whether the new version is running smoothly, and gradually working your way through all the nodes. This allows new versions to be deployed without service downtime, and thus encourages more frequent releases and better evolvability."

**Encoding/decoding, defined and distinguished from encryption [S]** (p131): "The translation from the in-memory representation to a byte sequence is called encoding (also known as serialization or marshalling), and the reverse is called decoding." A footnote makes an explicit distinction: "encoding has nothing to do with encryption."

**Language-specific serialization, four named deep problems [S]** (p131–132): language lock-in (hard to read the data from another language); a named security risk — "if an attacker can get your application to decode an arbitrary byte sequence, they can instantiate arbitrary classes, which in turn often allows them to do terrible things such as remotely executing arbitrary code"; forward/backward compatibility treated as an afterthought; and efficiency treated as an afterthought — "Java's built-in serialization is notorious for its bad performance and bloated encoding." Verdict: "it's generally a bad idea to use your language's built-in encoding for anything other than very transient purposes."

**JSON/XML/CSV, three named subtle problems beyond syntax debates [S]** (p132–133): number ambiguity — "In XML and CSV, you cannot distinguish between a number and a string that happens to consist of digits... JSON distinguishes strings and numbers, but it doesn't distinguish integers and floating-point," with a concrete named consequence: Twitter's 64-bit tweet IDs "cannot be exactly represented" in IEEE 754 doubles, so Twitter's API "includes tweet IDs twice, once as a JSON number and once as a decimal string"; no native binary string support (worked around via Base64, "somewhat hacky"); optional-but-complicated schema languages that many JSON tools skip entirely.

**Despite flaws, textual formats persist because of organizational, not technical, reasons [S]** (p133): "as long as people agree on what the format is, it often doesn't matter how pretty or efficient the format is. The difficulty of getting different organizations to agree on anything outweighs most other concerns."

**MessagePack worked case study, a concrete measured result [S]** (p134): encoding a 3-field JSON record in MessagePack yields "66 bytes long, which is only a little less than the 81 bytes taken by the textual JSON encoding." Explicit skepticism follows: "It's not clear whether such a small space reduction (and perhaps a speedup in parsing) is worth the loss of human-readability."

**Thrift and Protocol Buffers, defined by their schema requirement and field-tag mechanism [S]** (p135, p138): both "require a schema for any data that is encoded," and generate per-language classes from that schema via a code-generation tool. "Field tags are like aliases for fields — they are a compact way of saying what field we're talking about, without having to spell out the field name" — replacing field names entirely in the wire encoding.

**Field tags are the load-bearing compatibility mechanism, an explicit hard rule [S]** (p138): "You can change the name of a field in the schema, since the encoded data never refers to field names, but you cannot change a field's tag, since that would make all existing encoded data invalid."

**Adding/removing fields, precise compatibility rules stated directly [S]** (p139–140): new fields must get new tag numbers, and old code encountering an unrecognized tag "can simply ignore that field" using the type annotation to know how many bytes to skip (forward compatibility). New fields must not be `required` — "every field you add after the initial deployment of the schema must be optional or have a default value" (backward compatibility). Removing a field mirrors this with the constraints reversed: "you can only remove a field that is optional... and you can never use the same tag number again."

**Changing a field's datatype, a named concrete risk [S]** (p139): "there is a risk that values lose precision or get truncated" — worked example: widening a 32-bit int to 64-bit lets new code read old data safely (zero-fill), but old code reading new data risks silent truncation if the decoded value overflows 32 bits.

**Protocol Buffers' repeated marker vs. Thrift's list type, an explicit named trade-off [S]** (p139): Protocol Buffers "does not have a list or array datatype, but instead has a repeated marker for fields"

This has (p139) "the nice effect that it's ok to change an optional (single-valued) field into a repeated (multi-valued) field" — new code reading old data sees a 0-or-1-element list; old code reading new data sees only the last element.

Thrift's dedicated, parameterized list type (p139) "does not allow the same evolution from single-valued to multi-valued as Protocol Buffers does, but it has the advantage of supporting nested lists."

**Avro, defined by its absence of tag numbers, the chapter's own comparative framing [S]** (p140): "there are no tag numbers in the schema."

The same example record encodes in (p140) "just 32 bytes long — the most compact of all the encodings we have seen."

Decoding requires the exact schema used at encode time (p141): a decoded value carries no self-describing type tag, so the reader must walk fields in schema-declared order to know each one's datatype. `[D]`

**Writer's schema vs. reader's schema, Avro's defining mechanism [S]** (p142): "The key idea with Avro is that the writer's schema and the reader's schema don't have to be the same — they only need to be compatible." Resolution matches fields by name: unmatched writer fields are ignored; unmatched reader fields are filled from a declared default.

**Avro's compatibility rule, precisely and narrowly stated [S]** (p142): "you may only add or remove a field that has a default value." Adding a field with no default breaks backward compatibility (new readers can't fill it in from old data); removing a field with no default breaks forward compatibility (old readers expect it, new writers don't provide it).

**Avro's explicit null handling, a deliberate anti-implicit-null design choice [S]** (p143): "if you want to allow a field to be null, you have to use a union type." "This is a little more verbose than having everything nullable by default, but it helps prevent bugs by being explicit about what can and cannot be null" (p143).

Consequently Avro has no `required`/`optional` markers like Thrift/Protocol Buffers (p143) — "it has union types and default values instead."

**Three named contexts for tracking the writer's schema without duplicating it per record [S]** (p144): large multi-record files (Avro's object container format embeds the schema once at the file's start); databases with individually written records (embed a version number per record, keep a schema-version table, e.g. LinkedIn's Espresso); network connections (negotiate schema version once at connection setup, as Avro RPC does). `[D]`

**Avro's dynamic-schema-generation advantage over Thrift/Protocol Buffers, a concrete worked contrast [S]** (p144): dumping a relational database to Avro requires no manual tag-number bookkeeping — "The data export process does not need to pay any attention to the schema change — it can simply do the schema conversion every time it runs."

By contrast (p145), Thrift/Protocol Buffers field tags "would likely have to be assigned by hand" on every database schema change, the schema generator having "to be very careful to not assign previously used field tags."

"This kind of dynamically generated schema simply wasn't a design goal of Thrift or Protocol Buffers, whereas it was for Avro" (p145).

**Code generation's value is language-paradigm-dependent, an explicit named contrast [S]** (p145): useful in statically typed languages (Java, C++, C#) for compile-time type-checking and IDE autocompletion; "often frowned upon" in dynamically typed languages, and actively counterproductive for dynamically generated schemas, since it adds "an unnecessarily obstacle to getting to the data."

**Schema-driven binary encodings' four named nice properties [S]** (p146): more compact than "binary JSON" variants (field names omitted entirely); the schema is always-up-to-date documentation, "because the schema is required for decoding"; a schema database enables pre-deployment compatibility checking; and code generation aids static-language type-checking.

**Schema evolution's closing synthesis, an explicit reconciliation of two philosophies [S]** (p146): "schema evolution allows the same kind of flexibility as schemaless/schema-on-read JSON databases provide... while also providing better guarantees about your data and better tooling."

**"Data outlives code," a named aphorism with a direct database-specific consequence [S]** (p148): "within a single database you may have some values that were written five milliseconds ago, and some values that were written five years ago," while application code deployments replace themselves "within a few minutes."

"Rewriting (migrating) data into a new schema is certainly possible, but it's an expensive thing to do on a large dataset, so most databases avoid it if possible" (p148).

**The unknown-field-loss failure mode in application-mediated database round-trips, a concrete worked example [S]** (p148): if application code "decode[s] a database value into model objects... and later re-encode[s] those model objects, the unknown field might be lost in that translation process" — e.g. old code reading a record with a new `photoURL` field it doesn't model, then writing it back without that field, silently destroying it. "Solving this is not a hard problem, you just need to be aware of it."

**Archival storage dumps deliberately re-encode to a single, current schema, an explicit rationale [S]** (p149): even if the source database mixes schema eras, "the data dump will typically be encoded using the latest schema... Since you're copying the data anyway, you might as well encode the copy of the data consistently." Named good fit: immutable, write-once Avro object container files, and a segue into columnar analytic formats like Parquet.

**REST vs. RPC's fundamental philosophical split, an explicit named opposition [S]** (p151): REST "is not a protocol, but rather a design philosophy that builds upon the principles of HTTP"

RPC, by contrast, tries to make (p152) "a request to a remote network service look the same as calling a function or method in your programming language" — a goal the chapter calls "fundamentally flawed."

**Six named concrete differences between a local function call and a network request [S]** (p161–163): unpredictable failure vs. predictable outcomes; a genuinely new failure mode (an unknown-outcome timeout, distinct from a normal return, exception, or infinite loop); the need for explicit idempotence/deduplication when retrying, since retries can duplicate an already-successful action; wildly variable latency vs. roughly constant local call cost; the need to encode all parameters (no passing local pointers/references); and cross-language datatype translation friction (explicitly reconnecting to the earlier JSON-number-precision problem, e.g. numbers above 2^53).

**REST's explicit self-awareness advantage over hidden-RPC libraries [S]** (p153): "Part of the appeal of REST is that it doesn't try to hide the fact that it's a network protocol (although this doesn't seem to stop people from building RPC libraries on top of REST)."

**Modern RPC frameworks are more explicit about network semantics than classic RPC, three named concrete mechanisms [S]** (p153): Finagle and Rest.li use "futures (promises) to encapsulate asynchronous actions that may fail" — simplifying fan-out/fan-in across parallel service calls.

gRPC (p153) "supports streams, where a call consists of not just one request and one response, but a series of requests and responses over time"

**REST vs. custom binary RPC, an explicit named trade-off with REST favored for public APIs [S]** (p153): "Custom RPC protocols with a binary encoding format can achieve better performance than something generic like JSON over REST. However, a RESTful API has other significant advantages: it is good for experimentation and debugging... it is supported by all mainstream programming languages and platforms, and there is a vast ecosystem of tools."

Conclusion (p153): "REST seems to be the predominant style for public APIs." The main focus of RPC frameworks instead is on requests between services owned by the same organization, typically within the same datacenter. `[D]`

**RPC's simplifying compatibility assumption, an explicit named contrast with databases [S]** (p154): "it is reasonable to assume that all the servers will be updated first, and all the clients second. Thus, you only need backward compatibility on requests, and forward compatibility on responses."

**Cross-organizational RPC compatibility burden, an explicit named consequence [S]** (p154): "the provider of a service often has no control over its clients and cannot force them to upgrade. Thus, compatibility needs to be maintained for a long time, perhaps indefinitely. If a compatibility-breaking change is required, the service provider often ends up maintaining multiple versions of a service API side-by-side."

The chapter's own direct statement (p154): "There is no agreement on how API versioning should work, i.e. how a client can indicate which version of the API it wants to use"

**Message broker, defined by five named advantages over direct RPC [S]** (p155): buffering against an unavailable/overloaded recipient; automatic redelivery to a crashed consumer, preventing message loss; no need for the sender to know the recipient's network address; fan-out to multiple recipients from one message; and logical decoupling — "it logically decouples the sender from the recipient (the sender just publishes messages and doesn't care who consumes them)."

The key structural difference from RPC (p155): "message-passing communication is usually one-way: a sender normally doesn't expect to receive a reply to its messages."

**Message brokers are data-model-agnostic, an explicit named consequence for evolvability [S]** (p168): "message brokers typically don't enforce any particular data model — a message is just a sequence of bytes, with some metadata, so you can use any encoding format. If the encoding is backward and forward compatible, you have the greatest flexibility to change publishers and consumers independently, and deploy them in any order."

**Distributed actor frameworks, defined and their location-transparency advantage over classic RPC explicitly justified [S]** (p156): "The actor model is a programming model for concurrency in a single process... Each actor communicates with other actors by sending and receiving asynchronous messages. Message delivery is not guaranteed: in certain error scenarios, messages will be lost."

"Location transparency works better in the actor model than in RPC, because the actor model already assumes that messages may be lost, even within a single process" (p156).

**Three named distributed actor frameworks' compatibility postures, contrasted directly [S]** (p156): Akka defaults to Java's built-in (non-compatible) serialization but can swap in Protocol Buffers for rolling-upgrade support; Orleans' default custom encoding "does not support rolling upgrade deployments" at all, requiring a full parallel-cluster cutover instead.

In Erlang OTP (p157) "it is surprisingly hard to make changes to record schemas (despite the system having many features designed for high availability); rolling upgrades are possible but need to be planned carefully"

## 2. WHAT / WHY / WHEN

**WHAT:** A systematic tour of data encoding formats (language-specific serializers, JSON/XML/CSV and their binary variants, schema-driven binary formats Thrift/Protocol Buffers/Avro) and the three modes of data flow between processes (databases, services via REST/RPC, asynchronous message-passing via brokers or actors) — organized entirely around the chapter's two central concerns, backward and forward compatibility, both required to support rolling upgrades and long-lived stored data. `[D]`

**WHY it matters:** the chapter's unifying thesis is that evolvability (introduced in Ch.1) is not just an application-code property but is fundamentally gated by the data encoding format chosen, since "data outlives code" and different nodes running different code versions must coexist during any realistic deployment — meaning the encoding format's compatibility guarantees directly determine how safely and quickly an organization can ship changes. `[D]`

**WHEN to prefer Avro over Thrift/Protocol Buffers (p147–148):** specifically when schemas are dynamically generated from an external, independently-evolving source (e.g. a relational database schema), since Avro's name-based field matching requires no manual tag-number bookkeeping on every schema change, unlike Thrift/Protocol Buffers' hand-assigned tags.

**WHEN to use RPC vs. message brokers vs. plain database access (p164–170):** use synchronous RPC/REST when a low-latency, immediate request-response is genuinely needed and organizational boundaries favor debuggability (REST) or same-organization performance (binary RPC); use asynchronous message brokers when buffering, fan-out, sender/recipient decoupling, or resilience to a temporarily unavailable consumer matters more than immediate response; use direct database access when the "message" is really just state that a future reader (possibly the same process) will need to reconstruct at an arbitrary later time.

## 3. Assumptions and prerequisites

- Directly extends Ch.1's evolvability concept, cross-referenced by this vault's own note (`ch01_reliable_scalable_maintainable_applications.md`), not a page citation into Ch.4 itself. `[D]`
- Directly extends Ch.2's schema-on-read/schema-on-write discussion, cross-referenced by this vault's own note (`ch02_data_models_and_query_languages.md`). `[D]`
- Directly extends Ch.3's column-oriented storage discussion (Parquet) and data-warehousing material, cross-referenced by this vault's own note (`ch03_storage_and_retrieval.md`). `[D]`
- Forward-references transaction serializability terminology conflict to Ch.7 (p131), network unreliability/timeout semantics to Ch.8 (p162), Hadoop/large-file batch processing context to Ch.10 (p149), message broker comparisons (RabbitMQ, Kafka, etc.) to Ch.11 (p155), and request routing/service discovery to a later chapter section (p153) — all not yet synthesized in this vault.

## 4. Mechanism / key steps

**Thrift/Protocol Buffers schema evolution decision procedure, synthesized from the chapter's own rules (p139–141):** adding a field → assign a new, never-before-used tag number → mark it optional or give it a default (never `required`) → old code encountering the new tag simply skips it using the type annotation to determine byte length (forward compatible) → new code reading old data without that field either uses the default or treats it as absent (backward compatible). Removing a field → confirm it is currently optional (never remove a `required` field) → retire its tag number permanently, never reusing it, since old data may still reference it.

**Avro schema resolution mechanism, the chapter's own worked description (p144–145, Figure 4-6):** at decode time, the Avro library holds both the writer's schema (used to encode) and the reader's schema (what the application expects) side by side → match fields between the two schemas by name (order and position don't matter) → for a writer field with no matching reader field, discard it → for a reader field with no matching writer field, fill it from the reader schema's declared default value.

**Choosing how to track the writer's schema per context, the chapter's own three-branch decision (p144)** `[D]`: large immutable multi-record file → embed the writer's schema once at the file header (Avro object container format). Individually-updatable database records → prepend a schema version number to each record, maintain a schema-version lookup table, fetch the matching writer's schema per record at read time. Bidirectional network connection → negotiate the schema version once at connection setup, reuse it for the connection's lifetime (Avro RPC's approach).

## 5. Trade-offs and limitations

- **Backward compatibility is easy, forward compatibility is hard, an explicit asymmetry (§1, p130):** the newer code author controls and can special-case the old format, but old code cannot anticipate future additions it has never seen.
- **Protocol Buffers' repeated-field trick vs. Thrift's typed list, a genuine two-sided trade (§1, p141):** Protocol Buffers gains free single-to-multi-valued schema evolution at the cost of no nested-list support; Thrift gains nested lists at the cost of that specific evolution path.
- **Code generation helps static languages, actively hinders dynamic ones and dynamically-generated schemas (§1, p148):** not a universal best practice — its value is entirely contingent on the target language's type-checking model and the schema's own generation process.
- **Custom binary RPC outperforms REST but sacrifices REST's tooling ecosystem and debuggability (§1, p164):** an explicit, named performance-vs-operability trade-off, with the chapter noting REST nonetheless dominates for public APIs specifically because of the latter.
- **Distributed actor frameworks' default serialization choices trade rolling-upgrade support for simplicity out of the box (§1, p169–170):** Akka and Orleans both ship non-compatible defaults, requiring deliberate opt-in to compatible encodings (or a full cluster cutover in Orleans' case) to support rolling upgrades at all.

## 6. Failure modes and edge cases

- **Deserializing arbitrary, attacker-controlled byte sequences via language-native serializers (§1, p131–132):** an explicit, named remote-code-execution risk class — "if an attacker can get your application to decode an arbitrary byte sequence, they can instantiate arbitrary classes... allowing them to do terrible things such as remotely executing arbitrary code."
- **Large integers silently losing precision in JSON (§1, p132–133):** the chapter's own named concrete case — Twitter tweet IDs above 2^53 becoming inaccurate when parsed as JavaScript floating-point numbers, forcing Twitter's API to duplicate the field as both a JSON number and a string.
- **Unknown-field loss during application-mediated database read-modify-write cycles (§1, p156):** a concrete, named data-loss pattern distinct from the encoding format's own compatibility guarantees — the format may preserve unknown fields perfectly, but naive application-level decode-into-model-object-then-re-encode logic can still silently drop them.
- **Retrying a network request whose response (not request) was lost (§1, p162):** named directly as causing the underlying action to execute multiple times unless idempotence/deduplication is deliberately engineered — a failure mode with no local-function-call analogue.
- **Changing a field's datatype in a way that causes truncation for old code reading new data (§1, p140):** the chapter's own named 32-bit-to-64-bit-widening example demonstrates asymmetric safety — safe in one read direction, unsafe in the other.

## 7. Implications for design / build / maintain / RCA / optimization

- **Design:** the field-tag-vs-name-based schema evolution comparison (§1, p139, p144–145) is directly reusable as a decision input when choosing an encoding format for any new data pipeline in this vault's projects, particularly favoring Avro when schemas are derived from an independently-changing source like a database. `[D]`
- **Build:** the three-branch "how does the reader know the writer's schema" decision procedure (§4, p146–147) is a directly reusable architectural pattern for any system needing schema-aware binary encoding across files, databases, or network connections.
- **Maintain:** the "data outlives code" principle (§1, p154–155) is a directly reusable operating discipline for any long-lived data store — plan for encoding formats and migration strategies assuming stored data will substantially outlive the application code version that wrote it.
- **RCA:** an application observed to silently lose newly added fields on old-code read-modify-write cycles (§6, p156) is directly diagnosable against the documented unknown-field-loss pattern — check for naive model-object round-tripping before assuming an encoding-format bug.
- **Optimization:** the REST-vs-custom-binary-RPC performance/tooling trade-off (§1, p164) is a directly reusable framework for choosing an inter-service communication protocol — binary RPC for same-organization, performance-sensitive internal calls; REST for public or debugging-heavy interfaces.

## 8. How to test / verify these claims

- The MessagePack size-reduction claim (§1, p134, "66 bytes vs. 81 bytes") is directly reproducible: encode the chapter's own example record in both formats and compare byte counts.
- The Avro compactness claim (§1, p144, "32 bytes... the most compact") is directly reproducible: encode the same example record with Avro, Thrift BinaryProtocol/CompactProtocol, and Protocol Buffers, and compare resulting byte counts.
- The Twitter tweet-ID JSON-precision-loss claim (§1, p132–133) is directly testable: parse a tweet ID above 2^53 as a JSON number in a JavaScript environment and confirm precision is lost, then confirm the string-encoded copy remains accurate.
- The forward/backward compatibility rules for Thrift/Protocol Buffers (§1, p139–140) and Avro (§1, p145–146) are each directly testable by construction: encode data with an old schema, decode with a new schema (and vice versa), and confirm the documented pass/fail behavior for each named field-change type (add, remove, retype, rename).

## 9. Cross-references

- Directly extends [[ch01_reliable_scalable_maintainable_applications|Ch.1]]'s evolvability concept and [[ch02_data_models_and_query_languages|Ch.2]]'s schema-on-read/schema-on-write discussion — no contradiction found; this chapter treats encoding-format compatibility as the concrete mechanism underlying the more abstract evolvability and schema-flexibility ideas introduced earlier. `[D]`
- Directly extends [[ch03_storage_and_retrieval|Ch.3]]'s column-oriented storage and data-warehousing material (Parquet, archival storage) — fully consistent. `[D]`
- Forward-references (not yet synthesized in this vault): [[ch07_transactions|Ch.7]] (transaction serializability, a terminology clash with "serialization" explicitly flagged), [[ch08_trouble_with_distributed_systems|Ch.8]] (network unreliability and timeout semantics), [[ch10_batch_processing|Ch.10]] (Hadoop/batch processing context for large Avro files), [[ch11_stream_processing|Ch.11]] (detailed message broker comparison), and a later chapter section on request routing/service discovery.
- No contradiction found with any already-synthesized source in this vault.

---

## Exclusions (declared, not silently dropped)

| Item | Reason |
|---|---|
| Figures 4-1 through 4-7 (MessagePack, Thrift BinaryProtocol/CompactProtocol, Protocol Buffers, and Avro byte-sequence breakdown diagrams; Avro schema resolution diagram; unknown-field-loss data-flow diagram) | Structure and content described narratively above where load-bearing (§1, §4); full byte-level diagrams not reproduced verbatim. |
| Full worked schema definitions in Thrift IDL, Protocol Buffers, and Avro IDL/JSON for Example 4-1 (p135–142) | Representative excerpts and their semantics captured in §1; the complete verbatim schema listings across all three formats are not reproduced in full given their length and mutual redundancy. |
| Full three-category web-service-context enumeration (p150–151, client-to-service, service-to-service, cross-organization) | Representative structure captured in §1/§2 framing; the complete verbatim enumeration is not separately reproduced. |
| Full numbered reference list (53 references, p133–139 of chapter / p158–161 of PDF) | Citation metadata only; not treated as substantive content requiring synthesis, though individually notable attributed claims (e.g. the Twitter tweet-ID precision issue, CWE-502 deserialization risk) are captured inline in §1 with attribution context. |
