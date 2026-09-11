# Part B — Break It (Applied Reasoning)

## 1. Retrieval returns 5 chunks, but 2 are irrelevant

- Lower `number_of_results` and apply the existing `SIMILARITY_DISTANCE_THRESHOLD` to drop weak matches before generation.
- Use smaller, more topically focused chunks so surface-level matches don't pull in unrelated content.
- Instruct the prompt to ignore irrelevant context instead of blending everything.
- Longer-term: add a re-ranking step to score and filter top-k chunks before they reach the LLM.

## 2. Document set grows from 5 to 5,000 files

- Indexing breaks first — files are embedded and upserted one at a time with no batching, which won't scale.
- ChromaDB (local) may need to move to a managed/distributed vector DB for latency at this scale.
- More files means more plausible near-matches, so retrieval precision drops — needs metadata filtering and/or re-ranking.
- No incremental indexing currently — every run risks re-processing unchanged files.

## 3. Question needs facts from two different documents

- **No, not reliably.** Retrieval is a single similarity search against the whole question, so if the two needed facts don't each match the question's phrasing well, one may be missed.
- Fix (not implemented): query decomposition — split the question into sub-questions, retrieve for each separately, then combine context before answering.