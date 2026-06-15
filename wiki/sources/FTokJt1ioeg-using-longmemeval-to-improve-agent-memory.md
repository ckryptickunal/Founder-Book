---
type: source
title: Using LongMemEval to Improve Agent Memory
created: 2026-05-26
updated: 2026-05-26
video_id: FTokJt1ioeg
url: https://www.youtube.com/watch?v=FTokJt1ioeg
channel: YC Root Access
published: 2025-08-25T16:08:57Z
tags:
  - ai-agents
  - llm
  - benchmarking
  - mastra
  - memory-optimization
  - typescript
  - software-engineering
---

# Using LongMemEval to Improve Agent Memory

## Metadata

- Video ID: `FTokJt1ioeg`
- Channel: YC Root Access
- Published: 2025-08-25T16:08:57Z
- URL: https://www.youtube.com/watch?v=FTokJt1ioeg

## Summary

Sam, CEO of Mastra, discusses using the LongMemEval benchmark to optimize the memory layer of the Mastra TypeScript agent framework. He details how iterative testing against this benchmark led to improvements in semantic recall and working memory through better data structuring, template tailoring, and temporal reasoning fixes.

## Key Ideas

- Memory in AI agents is the compression and retrieval of chat history to provide relevant context for LLMs.
- LongMemEval evaluates five core memory subtasks: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and negative constraints.
- Framework-level optimizations, such as grouping messages by time and using tailored templates, significantly improve agent performance.
- Configuration parameters like 'top K' (retrieval count) have a measurable impact on performance and must be tuned appropriately.
- Iterative evaluation is essential for identifying subtle bugs in how data is presented to the LLM.
- Data structure matters: presenting messages as a flat list is less effective than structured, timestamped groupings for temporal reasoning.

## Entities

- [[entities/mastra|Mastra]] (company): A TypeScript agent framework for building AI applications.
- [[entities/longmemeval|LongMemEval]] (project): A benchmark specifically designed to evaluate the memory capabilities of AI agents.
- [[entities/gatsby|Gatsby]] (company): A web framework company where the Mastra team previously worked.

## Topics

- [[topics/agent-memory|Agent Memory]]: The process of storing, compressing, and retrieving chat history to maintain context in LLM interactions.
- [[topics/benchmarking|Benchmarking]]: The practice of using standardized tests to measure and iteratively improve the performance of AI systems.
- [[topics/temporal-reasoning|Temporal Reasoning]]: The ability of an AI to understand and reason about time-based events within a conversation history.

## Notable Claims

- Tailored templates for specific questions improve working memory accuracy. Evidence: Mastra observed increased accuracy in their working memory module after implementing script-generated, question-specific templates.
- Data structure and presentation significantly impact LLM reasoning capabilities. Evidence: Grouping messages by day and hour, rather than using a flat list, improved the agent's ability to perform temporal reasoning.
- Overwriting specific parts of working memory is more effective than full rewrites. Evidence: Targeted updates to working memory reduced errors compared to asking the LLM to rewrite the entire memory store.

## Quotes

> Memory is the compression of a queue of chat messages.
> The loop that leads to improvement is: write an eval scaffold and then just iterate a lot.
> Configuration matters.
