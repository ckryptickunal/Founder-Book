---
type: source
title: Interpretability and Safety for Robot Foundation Models
created: 2026-09-24
updated: 2026-09-24
video_id: 3WAHidozI9M
url: https://www.youtube.com/watch?v=3WAHidozI9M
channel: YC Root Access
published: 2026-08-06T17:35:24Z
tags:
  - ai-safety
  - robotics
  - interpretability
  - foundation-models
  - machine-learning
  - physical-ai
---

# Interpretability and Safety for Robot Foundation Models

## Metadata

- Video ID: `3WAHidozI9M`
- Channel: YC Root Access
- Published: 2026-08-06T17:35:24Z
- URL: https://www.youtube.com/watch?v=3WAHidozI9M

## Summary

Bear, founder of the Physical AI Safety Institute, discusses his pioneering research on interpretability for Robot Foundation Models (RFMs). The work focuses on applying AI safety techniques—specifically mapping feed-forward network (FFN) activations to semantic concepts—to gain direct control over robot behavior and mitigate risks associated with physical embodiment.

## Key Ideas

- Applying traditional AI safety and interpretability techniques to physical robot foundation models.
- Using FFN neuron clustering to identify and manipulate semantic concepts like 'speed' or 'caution' within a model.
- Physical embodiment introduces unique risks, such as the ability for a model to execute dangerous tasks in the real world that a digital-only model could only plan.
- The need to bridge the gap between AI safety, classical robotics (kinematics/dynamics), and robot learning communities.
- The 'Science of Physical AI Safety' workshop aims to formalize this interdisciplinary field.

## Entities

- [[entities/bear|Bear]] (person): Founder of the Physical AI Safety Institute and researcher at UC Berkeley.
- [[entities/physical-ai-safety-institute|Physical AI Safety Institute]] (organization): An organization dedicated to technical solutions for physical AI safety.
- [[entities/goodfire|Goodfire]] (company): A company involved in interpretability research.

## Topics

- [[topics/interpretability|Interpretability]]: The process of mapping internal model activations (FFNs) to human-understandable concepts to control robot behavior.
- [[topics/physical-ai-safety|Physical AI Safety]]: Addressing the unique risks posed by AI models that can physically interact with the world, such as humanoid robots.
- [[topics/robot-foundation-models-rfms|Robot Foundation Models (RFMs)]]: Large-scale models fine-tuned for robotic control and physical reasoning.

## Notable Claims

- RFMs introduce an amplified surface of risk compared to digital-only models because they can physically execute dangerous tasks. Evidence: The example of a humanoid robot potentially sourcing and assembling dangerous materials in the real world.
- FFN neuron clustering allows for direct control over robot action spaces. Evidence: Demonstrated by hyper-activating specific neuron clusters to change a robot's speed or caution level while executing the same command.

## Quotes

> Can we take those techniques and apply them to create concrete safety outcomes for systems that both think and physically act.
> An LLM might know how to make a bio weapon but an RFM embedded in a humanoid can know how to make it, it can go buy the parts... and actually go make it.
> The goal is to bring together the AI safety and robot learning communities to establish this shared field.
