# LLM Wiki Schema

This wiki is generated and maintained by scripts that call Gemini 2.5 Flash. Raw transcript files are the source of truth; generated wiki pages can be updated whenever sources change.

## Directory Roles

- `sources/`: one page per transcript/video, named by video ID.
- `entities/`: people, companies, products, organizations, and named projects.
- `topics/`: reusable concepts such as fundraising, AI agents, hiring, product-market fit, sales, and growth.
- `synthesis/`: cross-source analyses, comparisons, answers, and evolving theses.
- `index.md`: catalog of generated wiki pages.
- `log.md`: append-only chronological record of ingests, queries, and lint passes.

## Page Format

Every generated page should use YAML frontmatter:

```yaml
---
type: source | entity | topic | synthesis
title: Page title
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - video_id_or_page
tags:
  - tag
---
```

## Linking

- Use Obsidian-style wikilinks: `[[Page Name]]`.
- When referencing a source video, link to the source page when it exists.
- Prefer stable, human-readable page titles for entities/topics.

## Source Pages

Source pages should include:

- Video metadata: title, channel, URL, published date, duration/views/likes if known.
- Concise summary.
- Key ideas.
- Entities mentioned.
- Topics.
- Notable quotes or claims.
- Suggested wiki pages to update later.

## Entity and Topic Pages

Entity/topic pages should include:

- Definition or identity.
- Why it matters in this corpus.
- Key claims and recurring themes.
- Source references.
- Open questions or contradictions.

## Maintenance Rules

- Do not modify raw transcript files.
- Keep `log.md` append-only.
- Update `index.md` after every ingest or generated synthesis.
- Prefer conservative updates over speculative claims.
- Flag contradictions instead of silently resolving them.
