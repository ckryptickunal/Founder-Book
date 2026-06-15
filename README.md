# Founder Book

**A self-hostable, LLM-maintained knowledge base built from how founders actually think.**

Founder Book is a free, open-source tool that turns founder YouTube talks and essays into a
searchable, AI-queryable knowledge base — an **LLM wiki**. It points itself at YouTube channels
and essay sites (Garry Tan, Y Combinator, YC Root Access, Paul Graham, Sam Altman, …), pulls the
transcripts and articles, runs them through Gemini to extract people, companies, and topics, and
weaves it all into an interconnected Markdown wiki you can query in plain English from your
terminal — with cited, grounded answers (retrieval-augmented generation).

It then **keeps itself up to date on its own**: a background process watches those sources and
ingests new videos and essays automatically while you use the tool — never fetching the same
thing twice.

> **Inspired by [Andrej Karpathy](https://x.com/karpathy)'s idea of an _LLM Wiki_** — a personal
> knowledge base that a language model continuously reads, writes, and cross-links for you,
> instead of a static pile of notes you maintain by hand. Founder Book is one concrete take on
> that idea, specialized for startup/founder knowledge and made fully automatic.

---

## The problem

The best thinking from founders and investors is buried in **hundreds of hours of YouTube videos
and dozens of long essays**. When you have a specific question — *how do I price for enterprise?
what did they say about hiring the first engineer? how do I tell if I have product-market fit?* —
the answer is often a throwaway line 40 minutes into one talk and a single paragraph in someone
else's essay. Getting it means scrolling, scrubbing through video after video, and skimming article
after article.

**You shouldn't have to watch and read everything to get one answer.** You should be able to just
ask — and have an LLM respond using the *mental models, frameworks, and advice* that were actually
in those videos and essays, pull the relevant ones up for you, and, when you want to go deeper, hand
you the exact mentions and source links so you can use them directly.

That is what Founder Book does. Ask a question in plain English → it retrieves the relevant mental
models from across every source, synthesizes a grounded answer, and cites the specific videos/essays
(with the mentions behind each claim) so the originals are one click away. No scrolling required.

## What it does

```
YouTube channels / Essay sites / Local PDFs
        │
        ▼  discover new items (incremental, never re-fetches)
   extract transcripts (parallel Tor circuits)  +  scrape essays
        │
        ▼  Gemini analysis → entities, topics, summaries, claims, quotes
   Structured wiki (Markdown, Obsidian-compatible, fully wikilinked)
        │
        ▼
   Ask questions in natural language (RAG over the wiki + raw transcripts)
```

- **Build** a wiki of `sources/` (one page per video/essay), `entities/` (people, companies,
  products) and `topics/` (fundraising, PMF, hiring, …), all cross-linked.
- **Ask** questions conversationally; answers are grounded in retrieved pages + raw transcripts,
  with citations, and refuse to invent facts.
- **Stay current** automatically — see [Automatic updates](#automatic-updates-the-headline-feature).

---

## What's included in this repo

This repository ships both the **engine** and a large **starter corpus** so it works the moment
you clone it:

| Source | Type | Items |
|--------|------|-------|
| Garry Tan | YouTube | ~170 transcripts |
| Y Combinator | YouTube | ~800 transcripts |
| YC Root Access | YouTube | ~130 transcripts |
| Paul Graham | Essays | ~215 essays |
| Sam Altman | Essays | ~110 essays |
| **Generated wiki** | Markdown | ~1,500 sources · ~3,000 entities · ~3,000 topics |

All source content belongs to its original authors and is included for research/study. See
[Content & attribution](#content--attribution).

> **Privacy:** this repo intentionally contains **no API keys, no personal notes/ideas, and no
> query history.** Those live only on the maintainer's machine and are git-ignored. See
> [`.gitignore`](.gitignore).

---

## Who it's for

- **Founders, operators, and aspiring entrepreneurs** who want to search what
  top founders and investors actually said — startup advice, fundraising tactics,
  hiring, product-market fit, growth — instead of re-watching hours of video.
- **Anyone building an AI "second brain"** or personal knowledge management (PKM)
  system who wants a working, self-hostable example.
- **Developers** looking for a clean reference implementation of a
  **retrieval-augmented generation (RAG)** pipeline over YouTube transcripts and
  essays, with automatic, incremental ingestion.
- **Researchers and writers** studying startup, venture-capital, and AI discourse
  from primary sources.

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt

# Tor — used for block-free transcript extraction at scale
brew install tor      # macOS  (Linux: apt install tor)
```

### 2. Add your API keys

```bash
cp .env.example .env
# then edit .env and fill in:
#   YOUTUBE_API_KEY=...   (Google Cloud Console → YouTube Data API v3)
#   GEMINI_API_KEY=...    (Google AI Studio → API key)
```

### 3. Ask the existing corpus anything

```bash
python3 query_wiki.py "What does Paul Graham say about doing great work?"
```

The wiki is already built, so you can query immediately. To rebuild or extend it, read on.

---

## Automatic updates (the headline feature)

You should never have to remember to "go fetch the new videos." Founder Book does it for you.

### How it works

When you start the interactive CLI (`python3 query_wiki.py`), it launches **`auto_sync.py` as a
detached background process**. That process:

1. Reads the watch-list in [`sources.json`](sources.json).
2. For each **YouTube channel**, walks the uploads feed newest-first and **stops as soon as it
   reaches videos you already have** — so a routine check costs a couple of cheap metadata calls,
   not a full re-crawl. Only genuinely new videos are extracted (via Tor).
3. For each **essay site**, reads the live index and downloads only essays not already on disk.
4. Ingests everything new into the wiki with Gemini — in one pass.

It is **smart about not repeating work**: an item counts as "known" if it is on disk, recorded in a
channel's extract-state file, **or** already in the ingest manifest. State lives in
`wiki/automation_state.json`.

It is **safe and unobtrusive**:

- A **lockfile** ensures only one sync runs at a time, even with several CLI windows open.
- A **cooldown** (default 6 h/source) stops it re-crawling on every launch.
- It **degrades gracefully**: no Tor → it still discovers + queues videos and processes essays;
  no API key → it fetches but defers ingestion and tells you. One failure never aborts the rest.
- It runs in its **own process group** writing to `automation.log`, so the REPL is never blocked.

### Controlling it

Inside the Q&A CLI:

| Command | Action |
|---------|--------|
| `/sync` | Show last-sync status per source |
| `/sync now` | Force a background sync right now |

Standalone / scripted:

```bash
python3 auto_sync.py                # one pass (respects cooldown)
python3 auto_sync.py --force        # sync now, ignore cooldown
python3 auto_sync.py --dry-run      # show what WOULD be fetched; change nothing
python3 auto_sync.py --source "Garry Tan"   # one source only
python3 auto_sync.py --loop 360     # daemon: sync every 6 hours
python3 auto_sync.py --status       # print last-sync summary
```

Run it as a real daemon with `cron`/`launchd` — see [`docs/AUTOMATION.md`](docs/AUTOMATION.md).

### Watching a new source

Add an entry to [`sources.json`](sources.json) and you're done — the next sync picks it up:

```jsonc
{
  "youtube_channels": [
    { "name": "My Channel", "query": "https://www.youtube.com/@somehandle",
      "channel_id": null, "folder": "My Channel" }
  ],
  "essay_sources": [
    { "name": "Some Blog", "kind": "generic",
      "index_url": "https://example.com/essays", "base_url": "https://example.com",
      "folder": "Some Blog", "id_prefix": "sb" }
  ]
}
```

(`channel_id` is resolved from `query` once and cached back automatically.)

---

## The scripts

### Content acquisition

| Script | What it does |
|--------|--------------|
| `auto_sync.py` | **Background engine.** Discovers + fetches + ingests new videos/essays. |
| `fetch_new_essays.py` | Incrementally scrapes new essays from authors' websites. |
| `extract_channel.py` | Bulk transcript extraction via parallel Tor circuits. |
| `transcriptor.py` | Interactive single-video / full-channel extraction + channel resolution. |
| `fetch_transcript.py` | Fetch and print one transcript (quick caption check). |
| `retry_failed.py` | Retry videos in `failed_videos.json` through fresh Tor circuits. |
| `fetch_essays.py` | One-time essay import from public HuggingFace datasets. |

### Wiki management

| Script | What it does |
|--------|--------------|
| `ingest.py` | Analyze transcripts with Gemini → build/update wiki pages (parallel). |
| `ingest_file.py` | Ingest local PDFs / text / markdown / HTML. |
| `query_wiki.py` | Interactive Q&A CLI (RAG) — and launcher for the background sync. |
| `query_skills.py` | Task-specific answer skills (summary, comparison, …). |
| `lint_wiki.py` | Health check: broken links, orphans, stats. |
| `run_pipeline.py` | Full one-shot pipeline: retry → essays → ingest → verify. |
| `background.py` | Detaches `auto_sync.py` from the CLI; status/force helpers. |

A full walkthrough of each is in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## Asking questions

```bash
python3 query_wiki.py                       # interactive REPL
python3 query_wiki.py "..."                 # one-shot
```

Interactive commands: `/sync`, `/ingest <path>`, `/stats`, `/pages`, `/skills`, `/save`, `/quit`.
Answers are synthesized from retrieved wiki pages **and** the underlying raw transcripts, with
citations. If the wiki has no evidence, the answer says so rather than guessing.

---

## Project structure

```
.
├── sources.json              # watch-list for the auto-sync (channels + essay sites)
├── auto_sync.py              # background discovery → extract → ingest engine
├── fetch_new_essays.py       # incremental essay scraper
├── background.py             # detached launcher used by the CLI
├── extract_channel.py        # Tor-parallel transcript extraction
├── transcriptor.py           # channel resolution + metadata + transcript writer
├── ingest.py                 # Gemini wiki ingestion
├── ingest_file.py            # local file ingestion (PDF/txt/md/html)
├── query_wiki.py             # interactive Q&A CLI
├── query_skills.py           # answer skills
├── lint_wiki.py / run_pipeline.py / retry_failed.py / fetch_*.py
├── requirements.txt
├── .env.example
│
├── Garry Tan/  Y Combinator/  YC Root Access/   # raw YouTube transcripts (.txt)
├── Paul Graham/  Sam Altman/                     # essays as transcript files
│
└── wiki/                     # the generated knowledge base
    ├── sources/   entities/   topics/            # cross-linked Markdown pages
    ├── index.md                                  # catalog of all pages
    ├── ingested.json                             # ingest manifest (dedupe state)
    └── schema.md                                 # wiki format spec
```

---

## Environment variables

| Variable | Required | Used by |
|----------|----------|---------|
| `YOUTUBE_API_KEY` | yes (for new YouTube videos) | `transcriptor.py`, `extract_channel.py`, `auto_sync.py`, `retry_failed.py` |
| `GEMINI_API_KEY` | yes (for ingestion & Q&A) | `ingest.py`, `query_wiki.py`, `lint_wiki.py`, `ingest_file.py` |
| `GEMINI_MODEL` | no | Override ingestion model (default `gemini-3.1-flash-lite`) |
| `GEMINI_MODEL_QUERY` | no | Override Q&A model |
| `GEMINI_MODEL_LINT` | no | Override lint model |

---

## Troubleshooting

- **Tor not running / port 9050 refused** → `tor` (or `brew services start tor`). The background
  sync detects this and defers extraction until Tor is up.
- **YouTube rate-limit / IP block** → shouldn't happen (each request uses a unique Tor exit IP);
  if it does, re-run — extraction resumes from where it stopped.
- **Gemini errors during ingest** → check `GEMINI_API_KEY`; lower `ingest.py --workers`.
- **Missing video titles ("Unknown")** → invalid/rate-limited `YOUTUBE_API_KEY`; transcripts still
  download, only metadata is missing.

More in [`docs/AUTOMATION.md`](docs/AUTOMATION.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## FAQ

**What is Founder Book?**
Founder Book is a free, open-source, self-hostable knowledge base that turns
founder YouTube talks and essays into a searchable, cross-linked Markdown wiki you
can query in natural language. It's a concrete implementation of an
**LLM-maintained wiki** (an idea popularized by Andrej Karpathy) focused on startup
and founder knowledge.

**How is this different from searching YouTube or Google?**
Instead of returning links, Founder Book reads the full transcripts, extracts the
people, companies, and topics, and synthesizes a direct, cited answer from the
primary source material — grounded retrieval (RAG), not guesswork.

**Does it keep itself up to date?**
Yes. A background process (`auto_sync.py`) automatically discovers and ingests new
videos and essays from the channels and blogs you watch, while you use the tool,
without ever re-processing what it already has.

**Which founders and sources are included?**
A starter corpus from Garry Tan, Y Combinator, YC Root Access, Paul Graham, and
Sam Altman — and you can add any YouTube channel or essay site in `sources.json`.

**What AI model does it use?**
Google **Gemini** for ingestion and question-answering (model is configurable). You
bring your own API keys; nothing is sent anywhere else.

**Is my data private?**
Yes. Your API keys, personal notes/ideas, query history, and any locally-ingested
documents stay on your machine and are git-ignored — they are never published.

**Can I use it with Obsidian?**
Yes — the wiki is plain Markdown with YAML frontmatter and `[[wikilinks]]`, so it
opens as a graph in Obsidian out of the box.

**Do I need Tor?**
Only to extract *new* YouTube transcripts at scale (it avoids IP blocks). Querying
the existing wiki and reading essays works without it.

---

## Content & attribution

- **Concept:** inspired by Andrej Karpathy's idea of an LLM-maintained wiki.
- **Source content:** transcripts and essays are the work of their respective authors
  (Garry Tan, Y Combinator, Paul Graham, Sam Altman, and others) and are included here for
  research, study, and personal knowledge-management. All rights remain with the original
  creators. If you are a rights-holder and would like content removed, please open an issue.
- **Code:** released under the [MIT License](LICENSE).

Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

<sub>**Topics:** LLM wiki · AI second brain · RAG over YouTube transcripts · founder
knowledge base · searchable startup advice · Y Combinator / Paul Graham / Sam Altman
essays · Gemini RAG · personal knowledge management · Obsidian-compatible wiki ·
automatic YouTube transcript ingestion · open-source AI knowledge base.</sub>
