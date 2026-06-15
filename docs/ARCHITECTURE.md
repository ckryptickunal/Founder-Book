# Architecture

Founder Book is a pipeline of small, single-purpose Python scripts around two artifacts: a folder of
**raw transcript files** (the source of truth) and a generated **Markdown wiki**.

```
                          sources.json (watch-list)
                                  │
            ┌─────────────────────┴──────────────────────┐
            ▼                                             ▼
   YouTube discovery                              essay-site discovery
   (auto_sync.py +                                (fetch_new_essays.py)
    transcriptor.py)                                     │
            │                                            │
            ▼                                            ▼
   extract_channel.py  ──────────►  raw .txt transcripts  ◄────── ingest_file.py (PDF/MD/HTML)
   (parallel Tor circuits)         (Garry Tan/, Paul Graham/, …)
                                            │
                                            ▼
                                       ingest.py  ── Gemini ──►  analysis JSON
                                            │
                                            ▼
                              wiki/  sources/  entities/  topics/   (+ index.md, ingested.json)
                                            │
                                            ▼
                                       query_wiki.py  ── RAG + Gemini ──►  grounded answers
```

## 1. The raw transcript (source of truth)

Every piece of content — a YouTube video, an essay, a local PDF — becomes a `.txt` file with a
metadata header followed by `TRANSCRIPT` and the body. This uniform format is what makes the rest of
the pipeline source-agnostic. Raw files are **never modified** after creation; the wiki is always
regenerable from them.

Written by `transcriptor.write_transcript_file` (YouTube) and `fetch_essays` / `fetch_new_essays`
(essays). Files live in per-source folders named after the channel/author.

## 2. Acquisition

- **`transcriptor.py`** — resolves a channel name/URL/handle to a channel ID
  (`resolve_channel_id`), lists a channel's uploads (`get_all_video_ids`), and fetches per-video
  metadata. Also a standalone interactive extractor.
- **`extract_channel.py`** — the workhorse. Given a list of video URLs, it extracts transcripts
  using **parallel Tor circuits**: each worker gets a unique Tor exit IP via SOCKS auth isolation,
  so YouTube's per-IP rate limits never bite. State is saved per-video to
  `<folder>/_extract_state.json`, so it's safe to Ctrl-C and resume.
- **`retry_failed.py`** — re-attempts videos previously logged in `failed_videos.json` through fresh
  circuits.
- **`fetch_essays.py`** — one-time bulk import of essays from public HuggingFace datasets.
- **`fetch_new_essays.py`** — the incremental counterpart: reads an author's live index page and
  downloads only essays not already on disk. Pluggable per-site parsers live in `INDEX_PARSERS`.

## 3. Ingestion (`ingest.py`)

For each transcript not already in the manifest (`wiki/ingested.json`, keyed by video/essay ID and
mtime), `ingest.py`:

1. Parses the header + body (`parse_transcript_file`).
2. Sends the body to Gemini with a strict JSON schema asking for: summary, key ideas, entities
   (people/companies/products/orgs), topics, claims+evidence, quotes, tags
   (`analyze_transcript`). Robust JSON extraction + retries handle model quirks.
3. Writes a `sources/<id>-<slug>.md` page (`render_source_page`).
4. **Upserts** an `entities/<name>.md` and `topics/<name>.md` page per mention, appending a
   back-reference rather than overwriting (`upsert_reference_page`) — this is what builds the
   cross-linked graph.
5. Records the result in the manifest and appends to `wiki/log.md`.

It runs many transcripts in parallel (`--workers`, default 40) with locks around shared state, and
records per-item failures in `wiki/ingest_failures.json` so a single bad transcript never aborts the
batch.

## 4. The wiki (data model)

```
wiki/
├── sources/    one page per transcript: summary, key ideas, entities, topics, claims, quotes
├── entities/   one page per person/company/product, with "Source Mentions" back-links
├── topics/     one page per concept (fundraising, PMF, hiring, …), with back-links
├── index.md    regenerated catalog of every page (rebuild_index)
├── ingested.json   manifest: which source files have been ingested (dedupe key)
├── schema.md   the page-format spec
└── log.md      append-only activity log         ← personal; git-ignored
```

Pages use YAML frontmatter and Obsidian-style `[[wikilinks]]`, so the whole wiki opens cleanly in
Obsidian as a graph. See [`wiki/schema.md`](../wiki/schema.md).

## 5. Question answering (`query_wiki.py`)

A retrieval-augmented loop:

1. **Retrieve** — tokenize the question and score every wiki page by term overlap
   (`search_pages`); local-file/personal queries get pinned boosts.
2. **Assemble context** — include the top pages *and*, crucially, the **raw transcripts** behind the
   top source pages (`build_context` + `ingested.json`), so answers contain real detail, not just
   "go read page X".
3. **Route a skill** — pick an answer style (summary, comparison, document analysis, …) from
   `query_skills.py`.
4. **Answer with Gemini** under hard rules: synthesize a self-contained answer, cite pages, and if
   evidence is missing say what's missing instead of inventing it.

The interactive CLI also launches the [background auto-sync](AUTOMATION.md) and exposes `/ingest`,
`/stats`, `/pages`, `/skills`, `/save`, and `/sync`.

## 6. Maintenance

- **`lint_wiki.py`** — broken links, orphan pages, missing frontmatter, counts; `--suggest` adds
  Gemini-powered cleanup ideas.
- **`run_pipeline.py`** — a one-shot "catch everything up" pass: retry failures → fetch essays →
  ingest → self-verify. (For *discovering new* content, prefer `auto_sync.py`.)

## Design principles (from `.cursor` notes, distilled)

- Source of truth is the raw text; the wiki is derived and regenerable.
- Every batch script is crash-proof: per-item try/except, incremental checkpoints, always emit a
  status report.
- Prefer the cheapest model that does the job; make the model configurable per stage.
- Track state in JSON (manifests, extract-state, automation-state) so every step is resumable and
  idempotent.
