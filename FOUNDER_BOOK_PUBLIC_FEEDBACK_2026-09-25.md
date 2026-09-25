# Founder-Book: public problem and user-feedback corpus

**Researched:** 2026-09-25. **Project:** [ckryptickunal/Founder-Book](https://github.com/ckryptickunal/Founder-Book). **Scope:** Founder-thought retrieval, contradiction handling and update quality.

**Reading note:** These are third-party discussions in the problem space, **not feedback from users of this repo**. User posts are experiences or questions, not proof of prevalence. Relevance statements are hypotheses to test, not features claimed to exist. Each record uses stable fields for agents: date, audience, type, evidence, source, and project relevance.

## What emerges

- **Problem cluster:** Ingestion volume is not knowledge quality; retrieval needs precise citations, abstention and contradiction handling.
- Maintain source-level provenance and distinguish user-reported failure from speculation, feature request, promotional claim or counterpoint.

## Source records

### FOUNDER-BOOK-01
- date: 2026-02-15
- audience: Self-hosted knowledge-base builder
- type: firsthand need
- evidence: The builder consumes many channels and says insights get buried; they want attribution by episode/timestamp and to notice when speakers contradict one another.
- source: https://www.reddit.com/r/LocalLLaMA/comments/1r5jrti/building_a_selfhosted_ai_knowledge_system_with/
- Founder-Book relevance: Link each founder claim to exact source and time, and expose disagreements rather than merging them into a false consensus.

### FOUNDER-BOOK-02
- date: 2025-01-11
- audience: RAG practitioner
- type: discussion
- evidence: A knowledge base with conflicting tax-rate documents creates disambiguation and conflict-resolution problems; the question asks how relevance and integrity can be preserved.
- source: https://www.reddit.com/r/Rag/comments/1hysaqw/optimizing_rag_systems_how_to_handle_ambiguous/
- Founder-Book relevance: Keep source, date and claim-level disagreement visible in the founder wiki. This is analogous RAG feedback, not founder-specific demand.

### FOUNDER-BOOK-03
- date: 2025-06-20
- audience: Long-video summarization experimenter
- type: firsthand
- evidence: The author says Gemini produced key-point citations to timestamps outside the source chunk while summarizing lectures.
- source: https://www.reddit.com/r/LocalLLaMA/comments/1lg27hk/gemini_models_yes_even_the_recent_25_ones/
- Founder-Book relevance: Require verifiable timestamp evidence for founder positions before adding them to a durable profile.

### FOUNDER-BOOK-04
- date: 2025-01-19
- audience: Obsidian user
- type: firsthand
- evidence: The author watched long interviews and tutorials but "used to lose track of the best quotes and ideas" before establishing a searchable capture workflow.
- source: https://www.reddit.com/r/ObsidianMD/comments/1i4vh5u/my_5step_workflow_for_summarizing_youtube_videos/
- Founder-Book relevance: Reduce rediscovery work while retaining original speech and quotation context.

### FOUNDER-BOOK-05
- date: 2026-01-05
- audience: Claude user of long-form audio
- type: firsthand
- evidence: Manual transcript extraction, timestamp cleanup and context-window pasting was "driving me crazy."
- source: https://www.reddit.com/r/ClaudeAI/comments/1q4ii1r/i_got_tired_of_copypasting_transcripts_so_i_built/
- Founder-Book relevance: Make ingestion repeatable without losing who said what or when.

### FOUNDER-BOOK-06
- date: 2025-10-01
- audience: PKM user
- type: decision need
- evidence: The poster values NotebookLM sticking to uploaded sources, wants strict abstention outside the corpus, and seeks a resilient alternative.
- source: https://www.reddit.com/r/PKMS/comments/1nv1wjh/alternatives_to_notebooklm_for_closedcorpus_pkm/
- Founder-Book relevance: Make source-only mode and export/recovery part of the trust model.

### FOUNDER-BOOK-07
- date: 2025-12-31
- audience: Knowledge-base builder
- type: firsthand
- evidence: Dumping more notes into an AI KB made answers sound right but miss the point, the author reports.
- source: https://www.reddit.com/r/PKMS/comments/1q04r73/the_three_things_that_actually_matter_when/
- Founder-Book relevance: Curate founder concepts and contradictions; more scraped content alone is not quality.

### FOUNDER-BOOK-08
- date: 2026-04-06
- audience: Video-first PKM learner
- type: firsthand
- evidence: Video notes end up disconnected from the precise point in the talk, unlike article highlights.
- source: https://www.reddit.com/r/PKMS/comments/1se2md3/how_do_you_capture_knowledge_from_videos_into/
- Founder-Book relevance: Make every founder quote navigable to the moment it came from.

### FOUNDER-BOOK-09
- date: 2025-10-24
- audience: Obsidian AI video summarizer user
- type: firsthand
- evidence: The plugin began returning errors after months of use despite new keys and credits.
- source: https://www.reddit.com/r/ObsidianMD/comments/1of6to0/youtube_summary_worked_for_months_now_i_have_open/
- Founder-Book relevance: A scheduled sync needs visible failure and source freshness status.

### FOUNDER-BOOK-10
- date: 2025-11-19
- audience: Obsidian clipper maintainer
- type: reported user feedback
- evidence: The maintainer reports a YouTube change broke transcript retrieval for months and users contacted them about it.
- source: https://www.reddit.com/r/ObsidianMD/comments/1p0u3l9/obsidian_easy_clipper_update_youtube_transcripts/
- Founder-Book relevance: Alert on failed founder-source sync instead of silently leaving a stale profile.

### FOUNDER-BOOK-11
- date: 2026-04-29
- audience: Builder planning a video-to-KB pipeline
- type: project inquiry
- evidence: A poster asks for help creating structured knowledge extraction from YouTube rather than keeping raw videos alone.
- source: https://www.reddit.com/r/ArtificialInteligence/comments/1szda37/looking_for_help_and_advice_to_build_a_knowledge/
- Founder-Book relevance: This is weak demand evidence; evaluate exact extraction requirements before treating it as feature validation.

## Candidate checks (not an instruction to implement)

- Reproduce the cited problem with a small example before treating it as a priority.
- Compare a baseline workflow against the proposed improvement; keep failure states and confidence visible.
- Ask actual users of this repository before claiming product-market fit.

## Method and limits

Searched relevant public discussions and opened each linked page. The selected posts are independent problem-space signals; samples are small and selection-biased. Some are questions, feature requests, or interested commentary rather than reproducible bug reports. This is a dated snapshot, not an exhaustive or live feed. No private repository sources were used.
