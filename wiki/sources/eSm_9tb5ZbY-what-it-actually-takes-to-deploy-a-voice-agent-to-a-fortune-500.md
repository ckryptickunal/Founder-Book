---
type: source
title: What It Actually Takes to Deploy a Voice Agent to a Fortune 500
created: 2026-08-06
updated: 2026-08-06
video_id: eSm_9tb5ZbY
url: https://www.youtube.com/watch?v=eSm_9tb5ZbY
channel: YC Root Access
published: 2026-06-24T17:00:32Z
tags:
  - voice-ai
  - autonomous-agents
  - llm
  - simulation
  - evaluation
  - observability
  - enterprise-software
  - startup
  - founder-journey
  - waymo
  - customer-support-automation
  - ai-infrastructure
---

# What It Actually Takes to Deploy a Voice Agent to a Fortune 500

## Metadata

- Video ID: `eSm_9tb5ZbY`
- Channel: YC Root Access
- Published: 2026-06-24T17:00:32Z
- URL: https://www.youtube.com/watch?v=eSm_9tb5ZbY

## Summary

Brooke Hopkins, CEO of Koval, discusses her company's simulation and evaluation platform for voice agents, which recently raised a $28.2 million Series A. She explains how Koval helps enterprises scale voice AI by testing agents before production and monitoring them in the wild, drawing parallels to her experience at Waymo. The conversation covers the rapid enterprise adoption of voice agents, their unique failure modes, the evolution from simple customer support to novel AI-native experiences, and the importance of robust evaluation strategies. Hopkins also shares insights into her founder journey, the decision to focus on enterprise, and the future of voice AI, emphasizing the need for agent-native infrastructure and continuous validation.

## Key Ideas

- Koval provides a simulation and observability platform for voice agents, enabling enterprises to scale their use without testing on live customers.
- Voice is emerging as the 'killer UI' for AI, being the first productionized use case for autonomous agents and a natural interface for headless AI.
- Enterprises are rapidly adopting voice agents due to existing infrastructure (like IVR trees) and are expanding beyond customer support to new AI-native experiences.
- Voice agents fail differently than human agents, exhibiting 'vocal hallucinations' or completely incorrect responses, necessitating new QA and compliance measures.
- Effective evaluation of voice agents prioritizes understanding user intent and goal completion over raw metrics like word error rate.
- The future of voice AI lies in controllability for real-time models and bridging cascading architectures (speech-to-text, LLM, text-to-speech) through shared embeddings and specialized models, similar to advancements in self-driving cars.
- The founder's journey for Koval involved refining a broader 'evals' idea into a focused voice agent solution, driven by strong customer pull and a 'founder-market fit' with Brooke's Waymo background.
- Focusing on enterprise customers, despite initial challenges, allowed Koval to build a scalable solution for complex, high-volume use cases and align with longer-term roadmaps.
- Modern software development, especially with AI agents, shifts focus from building to planning, validation, and continuous operation at scale, requiring an 'agent-native' approach to APIs and product design.

## Entities

- [[entities/brooke-hopkins|Brooke Hopkins]] (person): Founder and CEO of Koval, previously led evaluation infrastructure at Waymo.
- [[entities/koval|Koval]] (company): A simulation and evaluation platform for voice agents, helping scale and monitor them. Recently announced a $28.2 million Series A round.
- [[entities/perplexity|Perplexity]] (company): Customer of Koval, mentioned as monitoring millions of calls.
- [[entities/deepgram|Deepgram]] (company): Customer of Koval, mentioned as monitoring millions of calls.
- [[entities/norwest|Norwest]] (company): Led Koval's $28.2 million Series A funding round.
- [[entities/base-10|Base 10]] (company): Participated in Koval's Series A funding round.
- [[entities/mac-ventures|Mac Ventures]] (company): Participated in Koval's Series A funding round.
- [[entities/yc|YC]] (organization): Y Combinator, a startup accelerator that funded Koval and where Harsh (the interviewer) is a partner.
- [[entities/waymo|Waymo]] (company): Autonomous driving technology company where Brooke Hopkins previously led evaluation infrastructure, providing foundational experience for Koval.
- [[entities/harsh|Harsh]] (person): Interviewer from YC Root Access, discussing Koval with Brooke Hopkins.
- [[entities/fonly|Fonly]] (company): A YC company and Koval's first customer, also recently raised Series A.
- [[entities/datadog|DataDog]] (company): Mentioned as an analogy for Koval's market position (observability).
- [[entities/applied-intuition|Applied Intuition]] (company): Mentioned as an analogy for Koval's market position (simulation).
- [[entities/linear|Linear]] (company): Used as an example of a product that scales expertise and provides opinionated workflows for engineering teams.
- [[entities/open-claw-agents|Open Claw Agents]] (other): A concept referring to AI agents with broad access to systems, raising security and management challenges.

## Topics

- [[topics/voice-agents-and-ai|Voice Agents and AI]]: Discussion on the rise of voice as a primary interface for AI, its applications in various industries like logistics and healthcare, and its potential to automate complex interactions.
- [[topics/koval-s-platform-and-technology|Koval's Platform and Technology]]: Explanation of Koval's role in simulating and evaluating voice agents, ensuring scalability, reliability, and compliance for enterprises, drawing parallels to self-driving car evaluation.
- [[topics/enterprise-adoption-of-voice-ai|Enterprise Adoption of Voice AI]]: Insights into why enterprises are quickly deploying voice agents, starting with customer support and expanding to novel AI-native experiences, and the existing infrastructure that facilitates this adoption.
- [[topics/challenges-and-evolution-of-voice-ai|Challenges and Evolution of Voice AI]]: Exploration of the unique failure modes of voice agents (e.g., vocal hallucinations), the shift in evaluation priorities from word error rate to intent, and future advancements like real-time model controllability.
- [[topics/founder-journey-and-startup-advice|Founder Journey and Startup Advice]]: Brooke Hopkins' personal story of founding Koval, including her transition from Waymo, the process of finding product-market fit, the decision to focus on enterprise, and general advice for aspiring founders.
- [[topics/simulation-and-evaluation|Simulation and Evaluation]]: The critical importance of robust simulation and evaluation infrastructure for AI systems, particularly voice agents, to ensure performance, compliance, and continuous improvement at scale, contrasting with traditional software testing.

## Notable Claims

- Voice is the first productionized use case for autonomous agents. Evidence: Brooke Hopkins states, 'I think what's so exciting about voice is A, it's the first productionized use case for autonomous agents.'
- Enterprises deploy voice agents at massive scale and more rapidly than any other type of agent because there's a lot more infrastructure already in place for voice. Evidence: Brooke Hopkins explains, 'We're seeing enterprises deploy voice agents at massive scale and more rapidly than any other type of agent because there's a lot more infrastructure already in place for voice. So, for example, standard operating procedures for customer service, you have IVR trees or call flows that already exist.'
- Voice agents fail in totally different ways than a customer support agent might fail, including vocal hallucinations or saying the completely wrong thing. Evidence: Brooke Hopkins notes, 'voice agents fail in totally different ways than a customer support agent might fail... it might say just the completely wrong thing. Or it might uh have a vocal hallucination. Famously, voice agents will accidentally scream, or they'll start to whisper or they'll change voices halfway through.'
- Word error rate or transcription is less important than understanding the intent of the conversation and reaching the final goal for voice agents. Evidence: Brooke Hopkins states, 'I think that people think word error rate or transcription is more important than it actually is because really you can have a full conversation and miss lots of words and still understand what that person is saying... But, really it's about how like did you understand the intent of the conversation and did you get to the final step?'
- Controllability for real-time models is the next big unlock for voice AI. Evidence: Brooke Hopkins identifies, 'I think controllability for real-time models' as the next big unlock, explaining the current cascading architecture and the need to bridge these models.
- Software engineering is the integral of programming over time. Evidence: Harsh (interviewer) quotes this analogy, and Brooke Hopkins agrees, 'So, it's pretty easy to make something work once, but then to make it work over time is the challenging part, and I think that's still true even with agents...'

## Quotes

> "Koval is a simulation and observability platform for voice agents. So, we help you to scale your voice agent over millions of conversations so that you don't have to test your voice agents with real customers in production."
> "I think what's so exciting about voice is A, it's the first productionized use case for autonomous agents."
> "We're going to see something very similar to what happened with the web and mobile, will happen with voice, where people start with things that are already happening on the phone, like customer support, or, um, logistics, and they're going to branch into all of these novel voice experiences that are much more AI native."
> "The things that agents are struggle more with is that they might trip up in more egregious ways that an human agent might not. So, for example, it might say just the completely wrong thing. Or it might uh have a vocal hallucination."
> "I think that people think word error rate or transcription is more important than it actually is because really you can have a full conversation and miss lots of words and still understand what that person is saying."
> "Controllability for real-time models. So, today the way most voice AI applications work is with cascading architectures."
> "When people are willing to knock down barriers for you, that is definitely a really great sign."
> "You definitely don't want only enterprise customers because then you're not learning from the fastest moving AI companies. And at the same time, moving up to enterprise allows you to have a lot more focus and consistency."
> "I think I thought that there was a way to become ready to be a startup founder, but really you just have to jump into it and be really curious and work as hard as you possibly can."
