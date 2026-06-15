---
type: source
title: The Engineering Unlocks Behind DeepSeek | YC Decoded
created: 2026-05-26
updated: 2026-05-26
video_id: 4Tmn-XP93m4
url: https://www.youtube.com/watch?v=4Tmn-XP93m4
channel: Y Combinator
published: 2025-02-05T15:00:04Z
tags:
  - ai
  - deepseek
  - llm
  - machine-learning
  - gpu
  - open-source
  - reinforcement-learning
---

# The Engineering Unlocks Behind DeepSeek | YC Decoded

## Metadata

- Video ID: `4Tmn-XP93m4`
- Channel: Y Combinator
- Published: 2025-02-05T15:00:04Z
- URL: https://www.youtube.com/watch?v=4Tmn-XP93m4

## Summary

The video analyzes the technical breakthroughs behind DeepSeek's R1 and V3 models, explaining how the company achieved state-of-the-art performance through algorithmic efficiency, mixture-of-experts architecture, and reinforcement learning, rather than just massive compute power.

## Key Ideas

- DeepSeek's performance is driven by architectural innovations like Multi-head Latent Attention (MLA) and Multi-token Prediction (MTP).
- The company optimized GPU utilization by training natively in 8-bit floating point (FP8) to overcome hardware constraints.
- DeepSeek R1 uses Group Relative Policy Optimization (GRPO) to enable reasoning through reinforcement learning without human-labeled examples.
- The $5.5 million training cost figure for V3 is misleading as it excludes R&D, hardware, and iterative training costs.
- DeepSeek's open-source approach and accessibility have democratized access to frontier-level reasoning models.

## Entities

- [[entities/deepseek|DeepSeek]] (company): A Chinese AI research lab known for the V3 and R1 models.
- [[entities/nvidia|Nvidia]] (company): Leading manufacturer of GPUs and AI infrastructure.
- [[entities/openai|OpenAI]] (company): Developer of GPT and o1/o3 reasoning models.
- [[entities/meta|Meta]] (company): Developer of the Llama model series.
- [[entities/deepseek-r1|DeepSeek R1]] (product): An open-source reasoning model optimized for complex tasks.
- [[entities/deepseek-v3|DeepSeek V3]] (product): A general-purpose base model using mixture-of-experts architecture.

## Topics

- [[topics/reinforcement-learning|Reinforcement Learning]]: The use of GRPO to train models to reason through complex problems via self-correction and reward signals.
- [[topics/hardware-efficiency|Hardware Efficiency]]: Techniques like FP8 training and mixture-of-experts to maximize GPU utilization under export constraints.
- [[topics/model-architecture|Model Architecture]]: The implementation of MLA for KV cache compression and MTP for better sequence planning.

## Notable Claims

- DeepSeek R1 achieves performance comparable to OpenAI's o1 at a fraction of the cost. Evidence: Performance on complex reasoning benchmarks like math and coding.
- DeepSeek V3 activates 11x fewer parameters per token than Llama 3 405B. Evidence: Mixture-of-experts architecture with 671B total parameters and 37B active parameters.
- The $5.5 million training cost for V3 is only for the final run. Evidence: The figure excludes R&D, hardware, and previous iterative training costs.

## Quotes

> What deep seek really proves is that there is still room for new players on the frontier.
> The deadline to apply for the first YC spring batch is February 11th.
