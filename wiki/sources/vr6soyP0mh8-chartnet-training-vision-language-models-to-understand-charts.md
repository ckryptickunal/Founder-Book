---
type: source
title: ChartNet: Training Vision-Language Models to Understand Charts
created: 2026-09-24
updated: 2026-09-24
video_id: vr6soyP0mh8
url: https://www.youtube.com/watch?v=vr6soyP0mh8
channel: YC Root Access
published: 2026-08-06T17:35:32Z
tags:
  - ai
  - machine-learning
  - computer-vision
  - synthetic-data
  - data-science
  - chartnet
  - ibm-research
---

# ChartNet: Training Vision-Language Models to Understand Charts

## Metadata

- Video ID: `vr6soyP0mh8`
- Channel: YC Root Access
- Published: 2026-08-06T17:35:32Z
- URL: https://www.youtube.com/watch?v=vr6soyP0mh8

## Summary

ChartNet is a large-scale, open-source synthetic dataset and pipeline designed to improve vision-language models (VLMs) in chart understanding. By leveraging a two-stage pipeline that translates charts into programmatic plotting code and performs iterative code augmentation, the project provides multimodal data including images, code, data tables, and natural language summaries to enhance numerical reasoning in AI models.

## Key Ideas

- Charts are best understood by models when provided with both visual data and the underlying programmatic code used to generate them.
- Synthetic data generation can be scaled by using LLMs to perform iterative augmentations in 'code space' rather than just image space.
- Small, specialized models trained on high-quality, multimodal synthetic datasets can outperform massive frontier models on specific tasks like chart and table extraction.
- ChartNet provides a comprehensive, diverse dataset that includes metadata like data tables and question-answer reasoning traces.

## Entities

- [[entities/yovana|Yovana]] (person): PhD candidate at MIT and lead researcher on ChartNet.
- [[entities/mit|MIT]] (organization): Massachusetts Institute of Technology.
- [[entities/ibm-research|IBM Research]] (organization): The research division of IBM.
- [[entities/mit-ibm-watson-ai-labs|MIT-IBM Watson AI Labs]] (organization): A joint research lab between MIT and IBM.
- [[entities/chartnet|ChartNet]] (project): A foundation model data generation pipeline and dataset for chart understanding.
- [[entities/gpt-4|GPT-4]] (product): A large multimodal model developed by OpenAI.

## Topics

- [[topics/vision-language-models-vlms|Vision-Language Models (VLMs)]]: AI models capable of processing and understanding both visual and textual information.
- [[topics/synthetic-data-generation|Synthetic Data Generation]]: The process of creating training data programmatically to overcome limitations in real-world data availability.
- [[topics/chart-understanding|Chart Understanding]]: The ability of AI to interpret visual charts, extract data, and perform numerical reasoning.

## Notable Claims

- A 2 billion parameter model trained on ChartNet can outperform significantly larger models like GPT-4 on chart understanding tasks. Evidence: Performance benchmarks conducted by the researchers across various open-source and public datasets.
- Training on carefully curated, multimodal synthetic data can replicate capabilities typically associated with massive frontier models. Evidence: Results showing that models trained on ChartNet outperformed leading peer models and Claude Opus on specific extraction tasks.

## Quotes

> The key gain... is that these capabilities that we commonly associate with these massive frontier models, we could instead gain by training on a carefully curated data sets that has this multimodal coverage.
> Unlike natural images, the models have to understand the text and they also have to engage in some kind of numerical reasoning.
