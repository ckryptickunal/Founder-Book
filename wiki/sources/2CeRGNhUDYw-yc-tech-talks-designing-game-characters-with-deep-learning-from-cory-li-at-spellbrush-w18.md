---
type: source
title: YC Tech Talks: Designing Game Characters with Deep Learning, from Cory Li at Spellbrush (W18)
created: 2026-05-26
updated: 2026-05-26
video_id: 2CeRGNhUDYw
url: https://www.youtube.com/watch?v=2CeRGNhUDYw
channel: YC Root Access
published: 2022-08-12T00:28:21Z
tags:
  - ai
  - deep-learning
  - game-development
  - gans
  - computer-vision
  - startups
  - infrastructure
---

# YC Tech Talks: Designing Game Characters with Deep Learning, from Cory Li at Spellbrush (W18)

## Metadata

- Video ID: `2CeRGNhUDYw`
- Channel: YC Root Access
- Published: 2022-08-12T00:28:21Z
- URL: https://www.youtube.com/watch?v=2CeRGNhUDYw

## Summary

Cory Li, CEO of Spellbrush, discusses using Generative Adversarial Networks (GANs) to automate and scale character illustration for game development, significantly reducing production time and costs while addressing data bias in training sets.

## Key Ideas

- Art production is a major bottleneck and cost driver in AAA game development.
- GANs (Generative Adversarial Networks) allow for the rapid generation of high-quality character art in seconds rather than hours.
- AI can be used to overcome human illustrator biases, such as the underrepresentation of male characters or darker skin tones in anime datasets.
- Training large-scale AI models is cost-prohibitive in the cloud, leading the company to build a custom, cost-effective in-house GPU cluster.
- Spellbrush is developing the world's first AI-illustrated game using a custom internal architecture called NetGen.

## Entities

- [[entities/cory-li|Cory Li]] (person): CEO of Spellbrush
- [[entities/spellbrush|Spellbrush]] (company): A YC-backed startup building deep learning tools for art and artists
- [[entities/gans|GANs]] (project): Generative Adversarial Networks consisting of a generator and a discriminator
- [[entities/netgen|NetGen]] (product): Internal custom language for describing GAN architectures
- [[entities/aws|AWS]] (company): Cloud computing provider

## Topics

- [[topics/generative-ai|Generative AI]]: The use of neural networks to create new, original visual content based on learned datasets.
- [[topics/data-bias|Data Bias]]: The challenge of correcting skewed training data to ensure diverse representation in AI-generated art.
- [[topics/infrastructure-optimization|Infrastructure Optimization]]: The trade-off between cloud computing costs and building custom hardware for intensive machine learning workloads.

## Notable Claims

- AI can generate character art in under two seconds that would take a human illustrator 2 to 15 hours. Evidence: Comparison of AI-generated images against professional artist work and internal production metrics.
- In-house GPU clusters are significantly cheaper than cloud-based training for large models. Evidence: Comparison of $24/hour AWS costs versus $0.60/hour for their custom 20+ GPU cluster.

## Quotes

> Art is becoming increasingly more expensive and increasingly difficult to scale.
> The generator's job is to learn how to draw art and the discriminator's job is to learn how to tell good art from fake art.
> We actually spend a lot of effort in order to correct this because obviously like these percentages don't represent the real world and representation is important.
