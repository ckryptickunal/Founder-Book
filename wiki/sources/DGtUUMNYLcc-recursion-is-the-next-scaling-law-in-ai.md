---
type: source
title: Recursion Is The Next Scaling Law In AI
created: 2026-05-26
updated: 2026-05-26
video_id: DGtUUMNYLcc
url: https://www.youtube.com/watch?v=DGtUUMNYLcc
channel: Y Combinator
published: 2026-05-01T14:00:32Z
tags:
  - ai-research
  - recursion
  - llms
  - neural-networks
  - reasoning
  - machine-learning
  - y-combinator
---

# Recursion Is The Next Scaling Law In AI

## Metadata

- Video ID: `DGtUUMNYLcc`
- Channel: Y Combinator
- Published: 2026-05-01T14:00:32Z
- URL: https://www.youtube.com/watch?v=DGtUUMNYLcc

## Summary

This video explores the emerging trend of using recursion at inference time to improve AI reasoning performance, contrasting it with the traditional approach of simply scaling model size. The discussion focuses on two specific research papers—Hierarchical Reasoning Models (HRM) and Tiny Recursive Models (TRM)—which demonstrate that small, recursive models can outperform massive LLMs on complex, incompressible tasks like Sudoku and the ARC Prize by utilizing latent memory states and iterative refinement.

## Key Ideas

- Recursion at inference time allows models to perform complex reasoning without needing massive parameter counts.
- LLMs are limited by their feedforward nature and lack of an internal, writable memory tape, making them struggle with incompressible problems.
- HRM and TRM use latent variables (hidden states) as a 'memory cache' to perform iterative computation, similar to a Turing machine.
- Truncated Backpropagation Through Time (TBTT) with a depth of one is surprisingly sufficient for training these recursive models.
- The 'outer refinement loop' is a critical architectural component that enables models to iteratively improve their latent representations.
- Combining the semantic representation power of large-scale LLMs with the recursive reasoning capabilities of TRMs is the likely future of AI architecture.

## Entities

- [[entities/francois-chopard|Francois Chopard]] (person): Visiting partner at Y Combinator and expert in AI research.
- [[entities/alex-graves|Alex Graves]] (person): Researcher known for work on RNNs and adaptive compute time.
- [[entities/constantine|Constantine]] (person): Researcher at Francois's company.
- [[entities/alexia|Alexia]] (person): Researcher behind the Tiny Recursive Models (TRM) paper.
- [[entities/melanie-mitchell|Melanie Mitchell]] (person): Author and researcher.
- [[entities/y-combinator|Y Combinator]] (organization): Startup accelerator and media producer.
- [[entities/hrm-hierarchical-reasoning-models|HRM (Hierarchical Reasoning Models)]] (project): A recursive model architecture using hierarchical frequency levels.
- [[entities/trm-tiny-recursive-models|TRM (Tiny Recursive Models)]] (project): A simplified, highly efficient recursive model architecture.

## Topics

- [[topics/recursion-in-ai|Recursion in AI]]: Using iterative weight application to perform multi-step reasoning within a single forward pass.
- [[topics/incompressible-problems|Incompressible Problems]]: Tasks like Sudoku or maze solving that cannot be solved in a single feedforward step and require iterative computation.
- [[topics/latent-space-reasoning|Latent Space Reasoning]]: Performing computation within continuous hidden states rather than discrete token space.
- [[topics/backpropagation-through-time-bptt|Backpropagation Through Time (BPTT)]]: The traditional training method for RNNs that faces vanishing/exploding gradient issues as sequence length increases.

## Notable Claims

- Recursive models can outperform massive LLMs on specific reasoning tasks while using significantly fewer parameters. Evidence: TRM (7 million parameters) achieved 87% on ARC Prize, outperforming larger models.
- Truncated Backpropagation Through Time (T=1) is sufficient for training effective recursive models. Evidence: Empirical results from HRM and TRM papers show that deeper backprop does not significantly improve performance.
- LLMs are inherently limited by their feedforward architecture when solving problems that require external memory or iterative logic. Evidence: Theoretical lower bounds on sorting algorithms (n log n) cannot be bypassed by feedforward transformers without external memory or chain-of-thought hacks.

## Quotes

> Recursion is the next scaling law in AI.
> It is sufficient and not necessary to go bigger and get better performance, and it is sufficient and not necessary to add more recursion.
> The right answer is to take the amazingness here and take the amazingness here... and when you slam them together, I think that it's just going to take off.
