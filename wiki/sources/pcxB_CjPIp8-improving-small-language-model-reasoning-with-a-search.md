---
type: source
title: Improving Small Language Model Reasoning With A* Search
created: 2026-09-24
updated: 2026-09-24
video_id: pcxB_CjPIp8
url: https://www.youtube.com/watch?v=pcxB_CjPIp8
channel: YC Root Access
published: 2026-08-06T17:35:21Z
tags:
  - llm
  - reasoning
  - a-search
  - small-language-models
  - reinforcement-learning
  - causality
  - neurips
---

# Improving Small Language Model Reasoning With A* Search

## Metadata

- Video ID: `pcxB_CjPIp8`
- Channel: YC Root Access
- Published: 2026-08-06T17:35:21Z
- URL: https://www.youtube.com/watch?v=pcxB_CjPIp8

## Summary

Alex presents a research paper on improving reasoning in small language models (SLMs) using A* search at test time. By utilizing the model's own self-critique as a heuristic, the method enables efficient tree search for correct answers without the need for external reward models or costly distillation, outperforming existing methods on benchmarks like GSM8K.

## Key Ideas

- Small language models (SLMs) are preferred for their efficiency but lack the complex reasoning of larger models.
- Test-time A* search allows SLMs to perform complex reasoning by treating the process as a tree search.
- Self-critique acts as a heuristic for the A* cost function, eliminating the need for external reward models.
- The method effectively prunes hallucinated paths by evaluating the model's own confidence in its generated steps.
- A* search provides better accuracy-to-compute efficiency compared to traditional tree search methods.
- Future research is shifting toward causal reinforcement learning to solve the credit assignment problem in LLM agents.

## Entities

- [[entities/alex|Alex]] (person): Researcher and author of the paper on A* search for LLM reasoning.
- [[entities/neurips|NeurIPS]] (organization): Conference on Neural Information Processing Systems.
- [[entities/aistats|AISTATS]] (organization): International Conference on Artificial Intelligence and Statistics.
- [[entities/gsm8k|GSM8K]] (product): A dataset of high-school level mathematical word problems.
- [[entities/math-500|Math 500]] (product): A mathematical reasoning benchmark.

## Topics

- [[topics/test-time-scaling|Test-time Scaling]]: Techniques that increase compute during inference to improve model performance.
- [[topics/a-search|A* Search]]: A graph traversal and path search algorithm used here to navigate reasoning trees.
- [[topics/self-critique|Self-Critique]]: A prompting technique where the model evaluates its own output to provide a score or feedback.
- [[topics/causal-reinforcement-learning|Causal Reinforcement Learning]]: An approach to AI that focuses on cause-and-effect relationships rather than simple correlations.

## Notable Claims

- The A* search method improves reasoning accuracy in small language models without requiring external reward models. Evidence: Experimental results on GSM8K and Math 500 show higher accuracy compared to other test-time scaling methods.
- The proposed method is more efficient in terms of token and time usage than existing tree search methods. Evidence: Ablation studies demonstrate a 3-4% increase in accuracy for the same amount of tokens and time.

## Quotes

> Instead of using external reward model, we use the model's own self-critique as a heuristic.
> Correlation is not causation and to have true intelligence true reasoning agents you need like this causation.
