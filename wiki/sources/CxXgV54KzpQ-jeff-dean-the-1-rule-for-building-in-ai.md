---
type: source
title: Jeff Dean: The 1% Rule for Building in AI
created: 2026-08-06
updated: 2026-08-06
video_id: CxXgV54KzpQ
url: https://www.youtube.com/watch?v=CxXgV54KzpQ
channel: Y Combinator
published: 2026-07-30T21:03:53Z
tags:
  - ai
  - machine-learning
  - jeff-dean
  - google
  - tpu
  - agent-systems
  - inference-hardware
  - context-engineering
  - startups
  - innovation
  - scientific-method
  - automation
---

# Jeff Dean: The 1% Rule for Building in AI

## Metadata

- Video ID: `CxXgV54KzpQ`
- Channel: Y Combinator
- Published: 2026-07-30T21:03:53Z
- URL: https://www.youtube.com/watch?v=CxXgV54KzpQ

## Summary

Jeff Dean discusses the rapid advancements in AI, particularly agent-based systems, and offers bold predictions for the future. He emphasizes the shift from general-purpose computing to specialized, energy-efficient inference hardware, drawing parallels to Google's early 'fits the memory' moment. Dean highlights the growing importance of 'context engineering' over just model size, making AI development more accessible to smaller teams. He advises founders to identify niche problems where general models fail (0-1% success rate) and to cultivate 'taste' in problem selection, even suggesting questioning fundamental assumptions like transistor reliability. Dean also foresees a future where AI automates the scientific method, leading to self-improving ML systems and accelerated discoveries across various fields, while sharing personal lessons on perseverance and team building.

## Key Ideas

- AI models are now capable of junior engineer-level tasks, with agent-based systems showing rapid growth in complexity and diverse applications.
- The future of AI will see significant automation of ML systems themselves, enabling self-improving capabilities through automated experimentation and problem decomposition.
- Specialized, high-performance, low-energy inference hardware is crucial for making agent-based AI systems widely available and reducing latency, mirroring Google's historical shift to in-RAM search.
- Agent-based systems can run for days or weeks on complex tasks, a capability not yet fully internalized by many, enabling sophisticated software development and optimization.
- Data movement is a major energy bottleneck in AI; founders often confuse 'model problems' with underlying 'energy or data I/O problems,' necessitating hardware specialization and efficient data handling.
- AI progress is increasingly driven by 'context engineering' (retrieval, tools, memory, agent orchestration) rather than solely model size, making it an accessible area for startups.
- Startups can win by focusing on niche domains where general models perform poorly (0-1% success rate), leveraging unique data access, or developing highly accurate specialized models.
- The scarce skill in an AI-driven future will be 'taste' – the wisdom to select impactful problems for agents to solve, cultivated through experience and questioning assumptions.
- AI will accelerate the scientific method by automating experimental loops and creating much faster validation models, leading to self-improving ML and breakthroughs in science and engineering.
- Perseverance is key; even impactful research (like distillation) can face initial rejection, but continued pursuit can lead to widespread adoption.

## Entities

- [[entities/jeff-dean|Jeff Dean]] (person): Distinguished Engineer at Google, known for contributions to MapReduce, BigTable, TensorFlow, TPU, and Gemini.
- [[entities/sanjay|Sanjay]] (person): Colleague of Jeff Dean, co-creator of MapReduce and co-author of 'Performance Hints'.
- [[entities/jeff-hinton|Jeff Hinton]] (person): Pioneer in deep learning, co-author of the distillation paper with Jeff Dean.
- [[entities/oral-fin|Oral Fin]] (person): Co-author of the distillation paper with Jeff Dean and Jeff Hinton.
- [[entities/google|Google]] (company): Technology company where Jeff Dean has made significant contributions, known for search, AI, and hardware development.
- [[entities/y-combinator|Y Combinator]] (organization): Startup accelerator, host of the interview.
- [[entities/mapreduce|MapReduce]] (product): Programming model and associated implementation for processing large data sets with a parallel, distributed algorithm on a cluster.
- [[entities/bigtable|BigTable]] (product): A compressed, high-performance, proprietary data storage system built on Google File System, Chubby, and other Google technologies.
- [[entities/tensorflow|TensorFlow]] (product): An open-source machine learning framework developed by Google.
- [[entities/tpu-tensor-processing-unit|TPU (Tensor Processing Unit)]] (product): Custom-built ASICs by Google for accelerating machine learning workloads, particularly for neural networks.
- [[entities/gemini|Gemini]] (product): A family of multimodal large language models developed by Google AI.
- [[entities/ai-ascent|AI Ascent]] (organization): Conference where Jeff Dean made a prediction about AI's capabilities.
- [[entities/alphafold|AlphaFold]] (product): An AI program developed by DeepMind (a Google subsidiary) which performs predictions of protein structure.
- [[entities/alphaevolve|AlphaEvolve]] (project): A system that proposes and evaluates solutions, keeping the ones that work, contributing to AI that builds AI.
- [[entities/alphachip|AlphaChip]] (project): A system that lays out chips, contributing to AI that builds AI.
- [[entities/neurips|NeurIPS]] (organization): A prominent conference in machine learning and computational neuroscience, which initially rejected the distillation paper.

## Topics

- [[topics/ai-capabilities-and-predictions|AI Capabilities and Predictions]]: Discussion on AI's current capabilities (junior engineer level), future predictions (automation of ML systems, agent longevity), and underestimated aspects of AI progress.
- [[topics/hardware-specialization-for-ai|Hardware Specialization for AI]]: The critical need for specialized, energy-efficient, low-latency inference hardware (like TPUs) to enable widespread AI adoption, drawing parallels to historical computing shifts.
- [[topics/energy-and-data-i-o-in-ml|Energy and Data I/O in ML]]: Analysis of the significant energy cost difference between computation and data movement, and how this shapes ML algorithm design (e.g., batching) and hardware decisions.
- [[topics/context-engineering-and-agent-systems|Context Engineering and Agent Systems]]: The evolving focus of AI development beyond model size to 'context engineering,' including tools, retrieval, memory, and orchestration for robust, long-running agent systems.
- [[topics/startup-opportunities-in-ai|Startup Opportunities in AI]]: Guidance for founders on identifying niche problems where general AI models fail, leveraging unique data, and building specialized solutions for specific domains.
- [[topics/ai-native-founder-skills|AI-Native Founder Skills]]: Emphasis on the importance of clear specifications for agents, cultivating 'taste' in problem selection, and questioning fundamental assumptions to drive innovation.
- [[topics/automated-scientific-discovery|Automated Scientific Discovery]]: The vision of AI systems automating the scientific method, leading to self-improving ML models and accelerated research in various scientific and engineering fields.
- [[topics/career-advice-and-team-building|Career Advice and Team Building]]: Reflections on career choices, the importance of working on impactful problems with enjoyable colleagues, and continuously acquiring new skills.

## Notable Claims

- AI is at the level of a junior engineer. Evidence: Models have been getting a lot better at agent-based, longer-running coding tasks and are now pretty capable.
- You will see a lot more automation of ML systems themselves by 2027. Evidence: ML systems will improve capabilities by running lots of experiments, breaking problems into subproblems, and using automated experimentation loops.
- Agent-based systems can run for days or weeks on really complicated tasks. Evidence: Some people are starting to see inklings of this, enabling tasks like implementing completely new versions of software in different programming languages with better properties.
- Calculation or math costs about one picojoule, but moving data costs a thousand times that. Evidence: Just bringing data in from HPM on an accelerator into the processor for computation.
- The distillation paper (teacher-student models) was rejected by NeurIPS for being 'unlikely to have significant impact'. Evidence: Jeff Dean explicitly states this, noting the reviewer's comment. The paper later became widely used in industry.
- Google's Flash models in Gemini are so capable relative to their size and speed partly due to distillation. Evidence: Jeff Dean states this directly, attributing their performance to the distillation technique.

## Quotes

> I feel like the models have been getting a lot better at sort of agent-based longer running coding tasks and it seems pretty clear that they are now actually pretty capable and depending on exactly your definition of of junior engineer it seems pretty spot-on I would say.
> I think you will see a lot more automation of ML systems themselves.
> I think everyone is now realizing that inference is the key to making you know these agent-based systems be available to more and more people and that latency is really important and that specialization of the hardware is a really key way you can make things that are more energy efficient and lower latency.
> Probably one thing is people don't quite realize how possible it is to have you know agent-based systems that can run not just for an hour or two hours on a problem you care about but for some problem domains and with highly capable models underlying them you can get them to run for days or weeks and do really really complicated tasks.
> If you build a specialized chip for low precision dense linear algebra and can't do anything else that turns out to be really useful for machine learning inference.
> The model is really only one piece of what you're trying to do which is build an overall system that can solve really interesting problems.
> The most important thing is to pick something you're super excited about and want to build and you think would be useful in the world.
> Look for something where the model succeeds 0% or 1% of the time not not 20%.
> It's really having incredibly good taste in what you ask your agents to work on.
> What would happen if you tried to build a system out of transistors that might have you know 20 errors per day rather than one every million years, right? That would be a very different design point.
> You want to optimize your discoveries per unit of compute input.
> If I work on this problem and the best possible outcome happens you know will the world be a lot better in some way or will the world go eh that's kind of cool but whatever.
