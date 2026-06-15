---
type: source
title: OpenAI vs. Deepseek vs. Qwen: Comparing Open Source LLM Architectures
created: 2026-05-26
updated: 2026-05-26
video_id: raTbhtKZTZA
url: https://www.youtube.com/watch?v=raTbhtKZTZA
channel: Y Combinator
published: 2025-08-29T14:01:34Z
tags:
  - llm
  - open-source-ai
  - deep-learning
  - architecture
  - openai
  - deepseek
  - qwen
  - machine-learning
---

# OpenAI vs. Deepseek vs. Qwen: Comparing Open Source LLM Architectures

## Metadata

- Video ID: `raTbhtKZTZA`
- Channel: Y Combinator
- Published: 2025-08-29T14:01:34Z
- URL: https://www.youtube.com/watch?v=raTbhtKZTZA

## Summary

This video provides a technical comparative analysis of three major open-source LLM architectures: OpenAI's GPT OSS, Alibaba's Qwen 3, and DeepSeek's V3/V3.1. It explores how these models utilize different strategies for mixture-of-experts (MoE) scaling, context window extension, and post-training alignment to achieve state-of-the-art performance.

## Key Ideas

- Modern LLMs share a common architectural foundation (GQA, SwiGLU, RoPE, RMS Norm) but diverge significantly in implementation details.
- Context window extension strategies vary: GPT OSS uses native pre-training with YaRN, DeepSeek uses staged fine-tuning, and Qwen 3 uses inference-time scaling.
- The 'moat' for AI labs is increasingly shifting from model architecture to proprietary data engineering and synthetic data generation pipelines.
- Reinforcement learning (RL) is becoming a standard, highly efficient component of post-training, with some models achieving significant reasoning gains from as few as 4,000 data pairs.
- There is a lack of first-principles justification in current AI research; most advancements are presented as empirical findings rather than derived theoretical improvements.

## Entities

- [[entities/openai|OpenAI]] (company): Developer of GPT OSS and GPT-4o.
- [[entities/deepseek|DeepSeek]] (company): Chinese AI research lab known for V3 and R1 models.
- [[entities/alibaba-cloud|Alibaba Cloud]] (company): Developer of the Qwen model family.
- [[entities/gpt-oss|GPT OSS]] (product): Open-weights mixture-of-experts model by OpenAI.
- [[entities/qwen-3|Qwen 3]] (product): Family of dense and MoE models by Alibaba.
- [[entities/deepseek-v3|DeepSeek V3]] (product): Large-scale mixture-of-experts model.

## Topics

- [[topics/mixture-of-experts-moe|Mixture of Experts (MoE)]]: An architecture where only a subset of model parameters are activated per token, allowing for large model capacity with efficient inference.
- [[topics/context-window-scaling|Context Window Scaling]]: Techniques like YaRN and RoPE modifications used to extend the number of tokens a model can process.
- [[topics/multi-head-latent-attention-mla|Multi-Head Latent Attention (MLA)]]: A memory-efficient attention mechanism used by DeepSeek to compress key-value caches.
- [[topics/post-training-alignment|Post-Training Alignment]]: The use of reinforcement learning and chain-of-thought data to refine model behavior and reasoning capabilities.

## Notable Claims

- DeepSeek's MLA provides better memory savings and performance than Grouped Query Attention (GQA). Evidence: Cited from the DeepSeek V2 research paper.
- Qwen 3's mixture-of-experts models match dense model performance with only 20% of active parameters. Evidence: Reported performance benchmarks from the Qwen 3 release.
- Reinforcement learning can significantly improve reasoning with very small datasets. Evidence: Qwen 3 achieved strong results using only 4,000 query-verifier pairs.

## Quotes

> Deepseek is such a fundamental change to the economics of what's going on.
> Each lab describes the combination of tools that works well for them, but almost no one gives a first principles justification of why one tool is better than the other.
> The big takeaway when reading these papers is you shouldn't focus too much on just the benchmark performance or topline stats like context size. Instead, look at the specific methods that these labs are using.
