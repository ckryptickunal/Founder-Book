# Contributing to Founder Book

Thanks for your interest! Founder Book is a small, hackable codebase — contributions of all
sizes are welcome.

## Ways to help

- **Add a content source.** The easiest contribution: add a channel or essay site to
  [`sources.json`](sources.json). For a new kind of essay site, add a parser in
  `fetch_new_essays.py` (`INDEX_PARSERS`) and a matching `"kind"`.
- **Improve ingestion.** Better prompts, schema fields, or entity/topic de-duplication in
  `ingest.py`.
- **Improve retrieval.** The Q&A retriever in `query_wiki.py` is a simple token-overlap scorer;
  embeddings / BM25 would be a great upgrade.
- **Docs & examples.** Clarify setup, add recipes.

## Ground rules

1. **Never commit secrets or personal data.** `.env`, `wiki/ideas/`, `wiki/synthesis/`,
   `wiki/log.md`, and `Local Files/` are git-ignored for a reason — keep it that way.
2. **Keep scripts resilient.** Per-item failures must be caught and logged, never crash a batch.
   Always save progress incrementally (manifests, state files).
3. **Be conservative with cost.** Default to the cheap Gemini models; only escalate where quality
   demonstrably requires it.
4. **Respect content owners.** Only add publicly available sources, and honor takedown requests.

## Dev setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your keys
python3 auto_sync.py --dry-run   # safe: discovers, fetches nothing
```

## Submitting changes

1. Fork and branch from `main`.
2. Keep changes focused; match the surrounding style.
3. Open a PR describing the change and how you tested it.
