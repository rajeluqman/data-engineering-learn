# Ch.14 — Project: Keeping family traditions alive with Airflow and generative AI

**Source:** `airflow_2e` (Data Pipelines with Apache Airflow, 2nd Edition, Manning)
**PDF page range:** 373–410 (38 pages) — per `audit/CHAPTER_MAP.csv`
**Chapter map status:** `located`, `entry_type: chapter`

## 1. Concepts and definitions

**Retrieval-augmented generation (RAG)** [S]: "Retrieval-augmented generation (RAG) solves many of the challenges of fine-tuning because it gives LLMs the power to read efficiently from an external library. This way, we don't have to retrain the LLM every time we add a recipe collection."
(p375)

**Embedding model** [S]: "A model that translates text into a vector representation is called an embedding model."
(p376)

**Chunk** [S]: "In a RAG system, text needs to be broken into smaller pieces to make retrieval more efficient. We call these pieces chunks."
(p384)

**Weaviate collection** [S]: "A collection is similar to a table in a traditional database"
(p387) [D] (source continues "in which each table contains fields associated with entities of our business logic... Weaviate uses a collection to put together objects that fit with one another" across a line wrap).

**UUID-based content identity** [S]: "These UUIDs are generated based on the content of each recipe, meaning that exactly the same text (including punctuation and spacing) always produces the same UUID."
(p385)

**Cosine similarity** [S]: "Two vectors that point in the same direction have a cosine similarity of 1. This concept is particularly useful in text analysis, in which the specific words in a recipe can vary widely, but the overall direction, which reflects the context or meaning, is what truly matters."
(p402)

**Prompt template** [S]: "A prompt template assists us in guiding the model's response, helping it better understand the context and produce consistent output."
(p404)

## 2. WHAT / WHY / WHEN

**WHAT** [D]: this chapter builds an end-to-end RAG (retrieval-augmented generation) pipeline orchestrated by Airflow — ingesting recipes, chunking and UUID-tagging them, storing embeddings in the Weaviate vector database with create/update/delete logic, and using an LLM with a prompt template to answer recipe questions grounded in that stored content.

**WHY** [S]: "Having high-quality data is paramount to building a good GenAI system or prod"
(p373) [D] (source continues "-uct because poor input data inevitably leads to poor results" across a hyphenated line wrap, then "Airflow can play an important role in ensuring high-quality input data by automating the processes involved in data preparation" on p374).

**WHEN** [D]: use RAG instead of fine-tuning when new content must be added continuously without expensive retraining, when full auditability of "where did this answer come from" matters, and when hosting/retraining costs for a fine-tuned model are prohibitive (§14.2-14.3); use RAG's create/update/delete logic (via content-derived UUIDs) whenever a knowledge base changes incrementally rather than being rebuilt from scratch each run (§14.7-14.8).

## 3. Assumptions and prerequisites

- Prerequisite: `DockerOperator` usage from chapter 11, directly reused for every task in this project's DAG: "In chapter 11, we used the DockerOperator to fetch data from an API. We can use this same pattern to develop GenAI applications."
(p381)
- Prerequisite: the Docker-Compose-based reproducible project setup pattern from chapter 13, reused: "As we did in chapter 13, we'll build our project using a Docker Compose file"
(p378).
- Assumes an available embedding-model provider (OpenAI's `text-embedding-3-large`, or an Azure OpenAI deployment) and corresponding credentials configured via environment variables (p389-391).
- Assumes recipes are already split into ingredients/instructions fields at upload time via the Recipe Vault UI's JSON structure, which the chunking logic depends on (p384-385).

## 4. Mechanism / key steps

1. Collect raw recipe input via a Streamlit-based upload UI (or a preload DAG for starter data), storing each recipe as JSON in MinIO object storage under a `raw` folder partitioned by date (p379-380).

2. Share common `DockerOperator` configuration (`image`, `environment`, `docker_url`, `network_mode`, `auto_remove`, `tty`) across every task in the DAG via a single `docker_kwargs` dict unpacked with `**docker_kwargs`, avoiding repetition (p382-383, Listing 14.1).

3. Preprocess each day's recipes: list JSON files for the templated `data_interval_start` path, split each recipe into exactly two chunks (ingredients, instructions) via `create_chunks`, and consolidate into one pandas DataFrame with `recipe_name` and `chunk` columns (p383-385, Listings 14.2-14.3).

4. Assign content-derived UUIDs to both `recipe_name` and `chunk` via Weaviate's `generate_uuid5`, so identical text always produces the same UUID and near-identical text produces a completely different one (p385-387, Listing 14.4, Figure 14.8) — save the result as `preprocessed.parquet` back to MinIO.

5. Create the Weaviate collection (idempotently) by first checking whether a collection with the given name already exists, and returning early (logging a message) if so — creation only ever happens once (p388, p391-393, Listings 14.5, 14.10).

6. Configure the collection's `vectorizer_config` via a dedicated `get_vectorizer_config` function that branches on an `OPENAI_CONN_TYPE` environment variable to build either an Azure OpenAI or OpenAI-API embedding configuration (p390-391, Listing 14.8) — passed as a list, since Weaviate supports multiple simultaneous embedding configurations (p391).

7. Define the collection schema via `Property` objects with explicit `data_type` (`DataType.UUID` for identifier fields with `skip_vectorization=True`, `DataType.TEXT` for vectorized content fields) (p391-392, Listing 14.9).

8. Compare newly preprocessed recipes against what's already stored: for each `recipe_name`, query Weaviate by that property, and classify each recipe's chunk set into one of three regimes — `create` (no existing objects), `update` (chunk UUID sets differ from what's stored), or drop (identical chunk UUID sets, already present) (p393-396, Listing 14.11, Figures 14.10-14.12).

9. Delete stale objects before re-inserting updated ones: filter Weaviate objects by `recipe_name` for all recipes marked `update`, and delete them in bulk via `collection.data.delete_many(where=filter)`, skipping the step entirely if there is nothing to delete (p397-398, Listing 14.12).

10. Upload new/updated recipes to Weaviate in dynamically-sized batches using `collection.batch.dynamic()`, checking `collection.batch.failed_objects` after each add and raising a `ValueError` if any objects failed (p398-400, Listing 14.13).

11. At query time, embed the user's question with the same embedding model used to store recipes, run a cosine-similarity search against the vector database to retrieve the most relevant chunks, and feed both the question and retrieved context into an LLM via a `PromptTemplate` that fixes the expected input variables (`context`, `input`, `chat_history`) and output format (a JSON object with `answer` and `provided_recipe` fields) (p401-405, Listing 14.15).

12. Wire retrieval and generation together using LangChain's `create_retrieval_chain` combined with `create_stuff_documents_chain`, invoking the chain with the user's question and any chat history (p407-408, Listing 14.16).

## 5. Trade-offs and limitations

- Fine-tuning an LLM on new content is costly (adjusting billions of parameters requires significant compute), requires an ongoing retraining pipeline for new content, requires hosting the resulting custom model, and blurs source clarity — "it's challenging to determine which recipes the LLM knew before we retrained it and which ones are our recipes" (p374-375). RAG avoids all four costs by keeping the LLM frozen and retrieving from an external, auditable store.
- Chunk-size selection is a direct trade-off: chunks too large make source attribution difficult ("like asking for a recipe and getting a big stack of cookbooks in return"), while chunks too small (e.g. per-sentence) produce "many chunks from the same recipe as the source for a single query," which is also inefficient (p384-385).
- The idempotent collection-creation check ("may seem inefficient... but it guarantees that we'll always verify whether the collection exists") trades a small per-run overhead for safety against accidental schema loss (p393).
- The three-way create/update/delete comparison strategy is use-case-specific: "In many other applications... the update strategy could vary greatly. If we introduced tenancy into the pipeline, for example, we'd have to consider whether a specific user uploaded the recipe."
(p396)

## 6. Failure modes and edge cases

- **Duplicate content mis-detection avoided via UUIDs**: without content-based UUIDs, checking whether a recipe already exists would require we'd have to "compare the new recipe with every existing one"
(p385) [D] (source continues "word by word, which is slow and inefficient") — the UUID scheme makes this an O(1) key lookup instead.
- **Empty delete/upload sets handled explicitly**: both the delete task and the save task check for zero records (`len(df) == 0` / `len(source_objects) == 0`) and skip/log rather than attempting a no-op or erroring, which matters on the very first run against an empty vector database (p398-399, p400).
- **Partial batch upload failures**: `save_in_vectordb` checks `collection.batch.failed_objects` after each batch add and raises `ValueError("Failed to save {len(failed_objects)} objects.")` if any objects failed, flagging the Airflow task as failed so it can be fixed (connection or data issue) and rerun (p399-400, p401).
- **LLM refuses ungrounded answers by design**: the prompt template explicitly instructs the LLM to say it doesn't know the recipe if it's not present in the retrieved context, rather than hallucinating from its own pretraining knowledge: "If the context doesn't contain the answer, reply saying that you don't know how to do that recipe."
(p404)

## 7. Implications for design/build/maintain/RCA/optimization

- **Design** [D]: prefer RAG over fine-tuning whenever content changes incrementally and provenance/auditability of generated answers matters, since RAG keeps retrieval and generation separately inspectable (p374-376).
- **Build** [D]: factor shared operator configuration (image, environment, network, cleanup policy) into a single kwargs dict reused across all tasks in a DAG built entirely on one container image, following DRY (p382-383).
- **Maintain** [D]: treat the vector-database schema (collection properties, vectorizer config) as append-only in production; changing it requires deleting and recreating the collection, so the idempotent create-collection task doubles as a safety guard against accidental schema drift (p393).
- **RCA** [D]: if the `save_recipes_to_weaviate` task fails, check the raised `ValueError`'s failed-object count first — the failure could be a connectivity issue or a data-shape issue, both of which are safely retriable since the task is designed to be rerun (p401).
- **Optimization** [D]: split chunking exactly along the same content shape the pipeline needs for later attribution and update comparisons (ingredients vs. instructions here) rather than choosing purely by size, since attribution granularity is itself a scaling concern (p384-385).

## 8. How to test/verify these claims

- Reproduce the UUID-determinism claim directly: call `generate_uuid5` on two near-identical strings differing by one word (as in Listing 14.4's cheesecake example, p386) and confirm the resulting UUIDs are completely different despite the minimal text change.
- Verify the create/update/delete classification by running the `compare_objects` task (Listing 14.11, p394-396) against a vector database containing zero, stale, and up-to-date versions of a given recipe, confirming each case lands in the expected regime.
- Verify the idempotent collection-creation behavior by running the `create_collection` task twice and confirming the second run logs that the collection already exists and takes no schema action (p393).
- Verify end-to-end RAG grounding by asking the chat interface for a recipe not present in the vector database and confirming the LLM responds that it doesn't know the recipe rather than fabricating one, per the prompt template's explicit instruction (p404, p408).
- Verify cosine-similarity retrieval behavior by embedding two semantically similar recipes (e.g. two dessert recipes) and two dissimilar ones, confirming the similar pair's cosine similarity is closer to 1 than the dissimilar pair's (p402-403, Figure 14.16).

## 9. Cross-references

- [[ch11_running_tasks_in_containers|Chapter 11]] (running tasks in containers): `DockerOperator` pattern reused for every task in this project (p381).
- [[ch13_project_finding_the_fastest_way_to_get_around_nyc|Chapter 13]] (NYC transportation project): Docker-Compose-based reproducible project structure reused (p378).

## Exclusions (declared, not silently dropped)

| Item | Reason for exclusion |
|---|---|
| Figures 14.1–14.20 (vector-space diagrams, UI screenshots, architecture diagrams) | Visual content; described narratively where relevant, not reproduced. |
| Full Streamlit Recipe Vault UI implementation | Frontend/UI scaffolding tangential to the Airflow-orchestrated RAG pipeline that is this chapter's subject. |
| Full LangChain retrieval-chain internals beyond the shown composition | The source itself keeps this at usage level; internal LangChain mechanics are out of scope for this chapter and this note. |
| Full embedding-model landscape comparison (Word2vec, Ada-002, Embed v3, Llama 3) | Named only as a survey of alternatives (p389); not elaborated since the project uses only `text-embedding-3-large`. |
