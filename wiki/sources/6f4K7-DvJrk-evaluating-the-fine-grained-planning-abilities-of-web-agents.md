---
type: source
title: Evaluating the Fine-Grained Planning Abilities of Web Agents
created: 2026-09-24
updated: 2026-09-24
video_id: 6f4K7-DvJrk
url: https://www.youtube.com/watch?v=6f4K7-DvJrk
channel: YC Root Access
published: 2026-08-06T17:35:38Z
tags:
  - ai
  - llm
  - vlm
  - web-agents
  - model-evaluation
  - planning
  - research
---

# Evaluating the Fine-Grained Planning Abilities of Web Agents

## Metadata

- Video ID: `6f4K7-DvJrk`
- Channel: YC Root Access
- Published: 2026-08-06T17:35:38Z
- URL: https://www.youtube.com/watch?v=6f4K7-DvJrk

## Summary

Surgan, a CMU master's student, discusses his EMNLP-presented research on evaluating the fine-grained planning abilities of Vision-Language Model (VLM) web agents. Instead of only evaluating final task outcomes, he proposes a method to decompose planning into specific, measurable skills—such as temporal ordering, future state prediction, and action selection—using low-cost, synthetic tests to identify where models fail.

## Key Ideas

- Evaluating web agents solely on final task success is insufficient for understanding planning failures.
- Planning can be broken down into discrete, fine-grained skills like temporal ordering and future state prediction.
- A semi-automatic approach can discover these skills and create synthetic, low-cost tests to evaluate them.
- Performance on these fine-grained skill tests is highly correlated with overall task performance.
- Fine-grained evaluation serves as a complementary, cost-effective diagnostic tool to filter models before running expensive, full-trace evaluations.

## Entities

- [[entities/surgan|Surgan]] (person): Master's student at CMU and researcher in VLM web agents.
- [[entities/cmu|CMU]] (organization): Carnegie Mellon University.
- [[entities/emnlp|EMNLP]] (organization): Conference on Empirical Methods in Natural Language Processing.

## Topics

- [[topics/web-agents|Web Agents]]: AI models designed to interact with web interfaces to complete user tasks.
- [[topics/fine-grained-planning|Fine-Grained Planning]]: The process of breaking down complex agent reasoning into smaller, measurable cognitive steps.
- [[topics/model-evaluation|Model Evaluation]]: Methodologies for assessing the performance and capabilities of LLMs and VLMs.

## Notable Claims

- Most current VLM web agents perform poorly (below 50%) on simple, fine-grained planning tests. Evidence: Results from the researcher's synthetic test suite applied to open-source models.
- Performance on fine-grained planning skills is a strong predictor of overall end-task success. Evidence: Correlation analysis between the synthetic test scores and final task execution performance.

## Quotes

> I'm thinking how do I break down planning, which is the ability to come up with thoughts to solve this action, into these fine-grained skills, and put a number to the capability of the model for each of these skills.
> It's not replacement, it's like complementary to the existing evaluation that we do.
