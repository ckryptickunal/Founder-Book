---
type: source
title: The ML Technique Every Founder Should Know
created: 2026-05-26
updated: 2026-05-26
video_id: dC_3ys349bU
url: https://www.youtube.com/watch?v=dC_3ys349bU
channel: Y Combinator
published: 2026-01-22T15:01:12Z
tags:
  - ai
  - machine-learning
  - diffusion
  - robotics
  - deep-learning
  - research
  - y-combinator
---

# The ML Technique Every Founder Should Know

## Metadata

- Video ID: `dC_3ys349bU`
- Channel: Y Combinator
- Published: 2026-01-22T15:01:12Z
- URL: https://www.youtube.com/watch?v=dC_3ys349bU

## Summary

Y Combinator's 'Decoded' series features visiting partner Francois Chahbar discussing the fundamental role of diffusion models in modern AI. The conversation covers the evolution of diffusion from its 2015 origins to current applications in robotics, biology, and weather forecasting, highlighting the shift toward simpler, more efficient training methods like flow matching.

## Key Ideas

- Diffusion models learn data distributions by iteratively adding noise and then training a model to reverse that process.
- Diffusion is highly effective for mapping high-dimensional data in low-data regimes.
- Flow matching simplifies the diffusion process by learning a direct, straight-line velocity between noise and data, rather than a circuitous path.
- The core diffusion math is surprisingly simple (often ~10 lines of code), making it a powerful, domain-agnostic framework for images, proteins, robotics, and text.
- Diffusion models offer a potential path toward more 'brain-like' intelligence by incorporating randomness and recursive, non-autoregressive processing.
- While autoregressive LLMs and MCTS (for games) remain dominant in their niches, diffusion is rapidly expanding into almost every other AI domain.

## Entities

- [[entities/francois-chahbar|Francois Chahbar]] (person): YC visiting partner and PhD student at Stanford focusing on diffusion-based world models for AGI.
- [[entities/joshua-sohl-dickinson|Joshua Sohl-Dickinson]] (person): Researcher who authored the foundational 2015 paper on non-equilibrium thermodynamics for diffusion.
- [[entities/deepmind|DeepMind]] (organization): AI research lab known for AlphaFold and protein folding breakthroughs.
- [[entities/stable-diffusion|Stable Diffusion]] (product): Popular open-source image generation model.
- [[entities/yarin-lipman|Yarin Lipman]] (person): Researcher at Meta who contributed to flow matching.

## Topics

- [[topics/diffusion-models|Diffusion Models]]: A machine learning framework that learns to reverse noise to reconstruct data distributions.
- [[topics/flow-matching|Flow Matching]]: A simplified training objective for diffusion that learns a direct velocity vector between noise and data.
- [[topics/general-intelligence-agi|General Intelligence (AGI)]]: The long-term goal of creating systems that can reason and learn recursively, potentially using diffusion-based architectures.

## Notable Claims

- Diffusion models are currently the most versatile AI technique, applicable to almost any high-dimensional data mapping. Evidence: Successful deployment in image generation, protein folding (AlphaFold), robotics (diffusion policy), and weather forecasting (GenCast).
- The mathematical implementation of diffusion has become significantly simpler over time. Evidence: Transition from complex KL-divergence-based loss functions to simple velocity-prediction loops in flow matching.
- Autoregressive LLMs are bottlenecked by their one-token-at-a-time generation process. Evidence: Contrast with human cognitive processes that involve recursive improvement and conceptual thinking rather than linear character-by-character output.

## Quotes

> It's honestly surprising how applicable this process is.
> There's really no limit to the things that this can do.
> I think we often assume as models have gotten more sophisticated that they become less accessible for people to understand but this is quite literally 10 lines of code.
> If you're in the business of training models, I would seriously look at diffusion.
