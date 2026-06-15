---
type: source
title: Context Engineering for Engineers
created: 2026-05-26
updated: 2026-05-26
video_id: 3jN77Aw7Utk
url: https://www.youtube.com/watch?v=3jN77Aw7Utk
channel: YC Root Access
published: 2025-08-25T16:05:44Z
tags:
  - ai-engineering
  - context-engineering
  - rag
  - llm-performance
  - chroma
  - agentic-ai
---

# Context Engineering for Engineers

## Metadata

- Video ID: `3jN77Aw7Utk`
- Channel: YC Root Access
- Published: 2025-08-25T16:05:44Z
- URL: https://www.youtube.com/watch?v=3jN77Aw7Utk

## Summary

Jeff, founder of Chroma, argues that 'context engineering' is a more accurate and practical framework than 'prompt engineering' or 'RAG' for building reliable AI software. He emphasizes that AI systems are essentially software programs requiring careful management of the context window through a 'gather and glean' methodology—maximizing recall first, then refining for precision—to improve performance and reliability.

## Key Ideas

- AI systems should be treated as software programs rather than 'techno-machine gods'.
- Context engineering involves intentionally deciding what enters the model's context window.
- Long context windows are currently unreliable for complex reasoning tasks; performance degrades as token length increases.
- The 'needle in a haystack' test is insufficient for evaluating real-world AI performance because it requires minimal reasoning.
- The 'gather and glean' framework: gather broad information (maximize recall) and then distill it (maximize precision).
- For agents, providing past failure cases is more beneficial for performance than providing past success cases, which can lead to lazy pattern matching.
- Compaction of context is critical for agentic loops, but current automated summarization techniques are often ineffective.

## Entities

- [[entities/jeff|Jeff]] (person): Founder of Chroma and speaker at YC Root Access.
- [[entities/chroma|Chroma]] (company): A company that builds search and retrieval databases for AI.
- [[entities/anthropic|Anthropic]] (company): AI research lab known for large context window models.
- [[entities/kelly|Kelly]] (person): Researcher at Chroma.

## Topics

- [[topics/context-engineering|Context Engineering]]: The practice of curating and optimizing the information provided to an LLM to ensure reliable, fast, and cheap outputs.
- [[topics/gather-and-glean|Gather and Glean]]: A two-stage pipeline for context: gathering a wide pool of data (recall) followed by filtering and ranking to retain only relevant information (precision).
- [[topics/agentic-loops|Agentic Loops]]: Systems where agents perform iterative tasks, requiring careful management of conversation history and context compaction.

## Notable Claims

- Model performance drops precipitously as token length increases for tasks requiring reasoning. Evidence: Chroma's technical report showing performance degradation on tasks beyond simple needle-in-a-haystack retrieval.
- Providing past success cases to an agent can hinder performance. Evidence: Observation that agents may become lazy and pattern-match to the provided success example rather than reasoning through the current problem.

## Quotes

> Context engineering is a much better term than prompt engineering or rag.
> We believe AI can be useful if you give it the right context and you know these systems ideally are reliable, fast and cheap.
> Needle in a haystack is a very easy task... the reasoning power is basically zero.
> You don't have to use state-of-the-art models all the time. You can use small fast cheap models and use a lot of them.
