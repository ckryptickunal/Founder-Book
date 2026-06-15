---
type: source
title: Context Engineering: Lessons Learned from Scaling CoCounsel
created: 2026-05-26
updated: 2026-05-26
video_id: sLFv3RSj_d8
url: https://www.youtube.com/watch?v=sLFv3RSj_d8
channel: YC Root Access
published: 2025-08-25T16:03:14Z
tags:
  - ai-development
  - prompt-engineering
  - llm
  - legaltech
  - software-architecture
  - evaluation
---

# Context Engineering: Lessons Learned from Scaling CoCounsel

## Metadata

- Video ID: `sLFv3RSj_d8`
- Channel: YC Root Access
- Published: 2025-08-25T16:03:14Z
- URL: https://www.youtube.com/watch?v=sLFv3RSj_d8

## Summary

Jake, founder of CoCounsel, outlines a rigorous methodology for 'context engineering'—the process of refining prompts and system architecture to build reliable AI applications. He emphasizes that success relies on treating prompts as a combination of instructions and context, utilizing systematic evaluation (evals) to reach high accuracy, and breaking complex tasks into manageable, testable micro-steps.

## Key Ideas

- Most prompts are a combination of instructions and context; success depends on optimizing both.
- Model application architecture should mirror how the world's best human expert performs the task.
- Rigorous evaluation is the primary differentiator; developers must iterate until they pass 100% of test cases.
- If an AI fails, it is often a retrieval or data quality issue (e.g., poor OCR) rather than a prompt issue.
- Use 'stop words' or token limits to force the model to think before outputting, while keeping responses fast.
- Reinforcement fine-tuning with 50-100 high-quality examples can significantly boost performance for specific micro-tasks.
- Different prompts within a workflow may benefit from different models to optimize for both cost and accuracy.

## Entities

- [[entities/jake|Jake]] (person): Founder of Kstax and CoCounsel.
- [[entities/cocounsel|CoCounsel]] (product): AI assistant for lawyers.
- [[entities/openai|OpenAI]] (company): AI research and deployment company.
- [[entities/thomson-reuters|Thomson Reuters]] (company): Global information services company.
- [[entities/prompt-fu|Prompt Fu]] (product): Open-source command-line tool for prompt testing.
- [[entities/vellum|Vellum]] (product): Cloud-based platform for prompt management.
- [[entities/chroma|Chroma]] (product): Vector database.

## Topics

- [[topics/prompt-engineering|Prompt Engineering]]: The practice of crafting instructions and context to guide LLM behavior.
- [[topics/evaluation-evals|Evaluation (Evals)]]: The process of testing prompts against a set of objective criteria to ensure reliability.
- [[topics/retrieval-augmented-generation-rag|Retrieval Augmented Generation (RAG)]]: The importance of providing high-quality, clean data to the model for accurate reasoning.
- [[topics/agentic-workflows|Agentic Workflows]]: Designing systems that perform multi-step tasks, sometimes autonomously, to mimic human expertise.

## Notable Claims

- GPT-4 significantly outperformed GPT-3.5 on the bar exam, moving from the 10th to the 90th percentile. Evidence: Cited as a benchmark study that validated the viability of AI for legal tasks.
- If an AI is failing, it is often due to poor input data (like bad OCR) rather than the prompt itself. Evidence: Observation from legal document processing where garbled text prevented accurate reasoning.
- Reinforcement fine-tuning requires only 50-100 examples to be effective. Evidence: Practical experience from scaling CoCounsel's micro-step models.

## Quotes

> The definition of a good prompt engineer is somebody who can write pretty well and also like concisely directly understandably write great instructions and also somebody who is willing to not sleep for two weeks straight until they get it right.
> If it's hard for you to read, it'll be hard for the AI to read is the general rule.
> If the thing says the sky is purple, the sky is damn purple.
