---
type: source
title: Any-Horizon Reasoning for Video Agents
created: 2026-09-24
updated: 2026-09-24
video_id: istBNYB4Et4
url: https://www.youtube.com/watch?v=istBNYB4Et4
channel: YC Root Access
published: 2026-08-06T17:35:29Z
tags:
  - ai
  - computer-vision
  - video-agents
  - machine-learning
  - reinforcement-learning
  - synthetic-data
---

# Any-Horizon Reasoning for Video Agents

## Metadata

- Video ID: `istBNYB4Et4`
- Channel: YC Root Access
- Published: 2026-08-06T17:35:29Z
- URL: https://www.youtube.com/watch?v=istBNYB4Et4

## Summary

Jitesh discusses his CVPR research on 'Any-Horizon' reasoning for video agents, which addresses the inefficiency and inaccuracy of existing models when processing long-form video content. By mimicking human adaptive behavior—using world knowledge and external tools like web search rather than relying solely on imperfect temporal grounding—the team developed a more efficient, cost-effective system using synthetic data generation and multi-reward reinforcement learning.

## Key Ideas

- Humans naturally adapt their attention span and reasoning depth based on the length and context of a video.
- Existing video agents struggle with long-form content due to inaccurate temporal grounding models.
- Integrating external tools like web search and speech transcription mitigates the reliance on visual-only temporal grounding.
- Synthetic data generation using models like Gemini 2.5 Flash significantly reduces the cost of training compared to human annotation.
- A multi-reward reinforcement learning (RL) recipe, using an LLM as a judge, enables models to learn when to use specific tools versus visual grounding.

## Entities

- [[entities/jitesh|Jitesh]] (person): Researcher presenting work at YCML/Startup School.
- [[entities/georgia-tech|Georgia Tech]] (organization): Academic institution.
- [[entities/ai2|AI2]] (organization): Allen Institute for AI.
- [[entities/gemini-2-5-flash|Gemini 2.5 Flash]] (product): Large language model by Google.
- [[entities/cvpr|CVPR]] (other): Conference on Computer Vision and Pattern Recognition.

## Topics

- [[topics/video-reasoning|Video Reasoning]]: The ability of AI agents to understand, query, and extract information from video content.
- [[topics/temporal-grounding|Temporal Grounding]]: The process of identifying specific time segments in a video to answer questions.
- [[topics/reinforcement-learning-rl|Reinforcement Learning (RL)]]: A training method using rewards to teach models adaptive reasoning and tool usage.

## Notable Claims

- Existing video agents underperform on open-ended questions and are too slow for real-world deployment. Evidence: The researcher notes that current models struggle with long videos because they were not trained on them and rely on inaccurate temporal grounding.
- Using synthetic data generation is significantly cheaper than human annotation for long-form video training. Evidence: Human annotation via platforms like Prolific costs over $30 per hour, whereas model-generated synthetic data provides a one-time, lower-cost alternative.

## Quotes

> Humans are very good at adapting how much time do they spend on what based on the task at hand.
> When humans look at long videos, they just don't look at the visual information. They do a very knowledge-grounded approach.
