---
type: source
title: Boris Cherny: We Cut 80% of Claude Code\u2019s Prompt
created: 2026-08-06
updated: 2026-08-06
video_id: qyPCVqFUyDo
url: https://www.youtube.com/watch?v=qyPCVqFUyDo
channel: Y Combinator
published: 2026-07-27T17:00:30Z
tags:
  - llm
  - claude
  - opus-5
  - anthropic
  - ai-agents
  - prompt-engineering
  - system-prompt
  - model-capabilities
  - code-generation
  - code-refactoring
  - software-development
  - ai-development
---

# Boris Cherny: We Cut 80% of Claude Code’s Prompt

## Metadata

- Video ID: `qyPCVqFUyDo`
- Channel: Y Combinator
- Published: 2026-07-27T17:00:30Z
- URL: https://www.youtube.com/watch?v=qyPCVqFUyDo

## Summary

Boris Cherny, creator of Claude Code, discusses the groundbreaking capabilities of Opus 5, including its ability to run tasks for extended periods and its robust resistance to prompt injection. He advocates for a radical 'delete and rebuild' approach to AI product development, where system prompts and tools are frequently re-evaluated and simplified as models become more intelligent. Cherny introduces concepts like 'unhobbling' models to unlock their full, often unrealized, potential, citing examples such as Claude rewriting the Bun JavaScript runtime from Zig to Rust in 11 days and using OpenCV for drawing. He emphasizes that successful interaction with modern LLMs requires an empirical mindset, giving models challenging tasks, and crucially, providing mechanisms for self-verification. He also details how dynamic workflows, loops, and routines enable Claude to orchestrate thousands of agents for complex tasks, including self-maintenance of its own codebases, suggesting that for many areas, coding is becoming automated.

## Key Ideas

- Opus 5 demonstrates significant advancements in long-duration task execution and prompt injection resistance, setting a new frontier for LLM capabilities.
- The rapid evolution of LLMs necessitates a 'delete and rebuild' strategy for system prompts and tools in agentic products, as models quickly outgrow previous instructions.
- The concept of 'unhobbling' models involves removing product-imposed limitations ('product overhang') to fully unleash their inherent, often unrealized, capabilities.
- Effective AI product development requires an empirical, scientific mindset: give models challenging tasks, provide mechanisms for self-verification, and iterate based on observed performance.
- Advanced orchestration features like dynamic workflows, loops, and routines enable models to manage thousands of agents, automating complex engineering tasks such as codebase rewrites and self-maintenance.
- The role of 'prompt engineering' is shifting from specific tricks to defining high-level tasks, guardrails, and crucial verification criteria, treating the model more like an intelligent coworker.
- Coding is becoming increasingly automated for many types of tasks, freeing human engineers to focus on product innovation and user interaction.
- Learning computer science practically, by solving real-world problems, is crucial for success in the AI era.

## Entities

- [[entities/boris-cherny|Boris Cherny]] (person): Creator of Claude Code and speaker in the interview.
- [[entities/claude-code|Claude Code]] (product): An agentic product/harness built on Anthropic's Claude models, designed for coding tasks.
- [[entities/opus-5|Opus 5]] (product): Anthropic's latest and most advanced large language model, part of the Claude series, noted for its new capabilities.
- [[entities/anthropic|Anthropic]] (company): The AI research and development company behind the Claude models.
- [[entities/arc-agi-3|Arc AGI 3]] (project): A benchmark or task on which Opus 5 achieved a 30% score, a significant improvement.
- [[entities/opus-4-7|Opus 4.7]] (product): A previous version of Anthropic's Claude model, noted for early prompt injection resistance.
- [[entities/opus-4-8|Opus 4.8]] (product): A previous version of Anthropic's Claude model, noted for early prompt injection resistance.
- [[entities/sonnet-5|Sonnet 5]] (product): A version of Anthropic's Claude model, noted for good prompt injection resistance.
- [[entities/people|People]] (other): Likely referring to a specific Claude model version or internal project, noted for good prompt injection resistance.
- [[entities/crystal|Crystal]] (person): Researcher whose mechanistic interpretability work on neuron activation is used for prompt injection classification.
- [[entities/bun|Bun]] (product): An open-source JavaScript runtime, alternative to Node.js, originally written in Zig and rewritten to Rust by Claude.
- [[entities/node-js|Node.js]] (product): A popular JavaScript runtime environment, which Bun is an alternative to.
- [[entities/zig|Zig]] (other): A systems programming language, similar to C, in which the Bun runtime was originally written.
- [[entities/rust|Rust]] (other): A systems programming language, known for memory safety, to which the Bun codebase was rewritten by Claude.
- [[entities/jared|Jared]] (person): A member of the Bun team who initiated the experiment of having Claude rewrite the Bun codebase.
- [[entities/fable|Fable]] (product): A previous Claude model generation that first demonstrated the capability to rewrite codebases.
- [[entities/opencv|OpenCV]] (product): An open-source computer vision library that Opus 5 was found to be able to use for drawing.
- [[entities/electron|Electron]] (product): A framework for building desktop applications using web technologies, used for Claude's desktop app.
- [[entities/swift|Swift]] (other): Apple's programming language for building apps across Apple platforms, to which the Electron app is being rewritten by Claude.
- [[entities/github|GitHub]] (company): A platform for version control and collaboration, used for Mac OS runners and codebases.
- [[entities/slack|Slack]] (product): A communication platform where Claude Tag sessions and routines can run.
- [[entities/claude-tag|Claude Tag]] (product): A new Anthropic product where Claude runs in Slack.
- [[entities/ti-83-calculators|TI-83 calculators]] (product): A graphing calculator on which Boris Cherny first learned to code in BASIC.

## Topics

- [[topics/large-language-model-capabilities|Large Language Model Capabilities]]: Discussion of Opus 5's new abilities, including extended task execution, prompt injection resistance, and advanced reasoning for complex problems, highlighting its rapid performance acceleration.
- [[topics/ai-product-development-methodology|AI Product Development Methodology]]: Emphasis on an empirical, 'delete and rebuild' approach for harnesses and prompts, adapting to rapidly changing model capabilities rather than rigid system design, and the importance of 'ablations'.
- [[topics/prompt-engineering-evolution|Prompt Engineering Evolution]]: The shift from specific prompt tricks to defining high-level tasks, guardrails, and crucial self-verification mechanisms for models, treating them more like intelligent coworkers.
- [[topics/agentic-ai-systems|Agentic AI Systems]]: Exploration of how models can orchestrate multiple agents, perform long-running, complex tasks, and even self-maintain codebases using dynamic workflows, loops, and routines.
- [[topics/unhobbling-models-and-product-overhang|Unhobbling Models and Product Overhang]]: The concept of removing artificial constraints ('hobbling') and addressing 'product overhang' to allow models to express their full, often unrealized, potential and capabilities.
- [[topics/future-of-coding-and-engineering|Future of Coding and Engineering]]: The increasing automation of coding tasks, suggesting that for many areas, coding is 'solved,' allowing human engineers to focus on higher-level product innovation and user interaction.
- [[topics/practical-learning-in-computer-science|Practical Learning in Computer Science]]: Advice for students to learn computer science by applying it to solve real-world problems, combining technical skills with business and design acumen, rather than purely theoretical study.

## Notable Claims

- Opus 5 achieved a 30% score on Arc AGI 3, a significant increase from previous low single digits or teens. Evidence: Stated by the interviewer and confirmed by Boris Cherny.
- Opus 5 can run for days, weeks, or months at a time, especially with auto mode, without needing scaffolding. Evidence: Boris Cherny's direct statement and examples of long-running tasks like the Electron to Swift rewrite.
- Opus 5 (and earlier versions like 4.7, 4.8, Sonnet 5, People) is resistant to prompt injection. Evidence: Boris Cherny's direct statement, attributing it to a combination of well-aligned models, a prompt injection classifier (based on Crystal's mechanistic interpretability), and an auto mode classifier.
- Anthropic deleted over 80% of Claude Code's system prompt for Opus 5. Evidence: Boris Cherny's direct statement, explaining it's because Opus 5 is more intelligent and doesn't need as many explicit instructions.
- The model is sometimes more intelligent without system prompts. Evidence: Anthropic's internal ablation experiments using 'simple mode' for Claude Code.
- Opus 5 can rewrite essentially any codebase from one language to another. Evidence: Example of the Bun runtime (Zig) being rewritten to Rust by Claude, running for 11 days, now in production.
- Opus 5 can use OpenCV to draw images like portraits, animals, and landscapes, despite not being explicitly trained for it. Evidence: Internal discovery at Anthropic through accidental experimentation, described as a 'solicitation gap'.
- Claude can rewrite the Electron desktop app in Swift, comparing pixel by pixel, and has been running for over 2 weeks. Evidence: Boris Cherny's personal experiment using Claude Tag and a Mac virtual machine, which is still ongoing.
- Claude can maintain its own codebases (CLI, iOS, Android, desktop apps) using routines like cleaning up dead code, shipping experiments, writing/deleting tests, and unifying abstractions. Evidence: Boris Cherny's description of internal practices at Anthropic, running hundreds/thousands of agents daily.
- Coding is 'solved' for many types of tasks, particularly those Boris Cherny works on. Evidence: Boris Cherny's statement, with a caveat for highly specialized or complex systems like deep systems code or distributed systems.

## Quotes

> It can go for days, weeks, months at a time. It just won't stop.
> The model does not seem to be prompt injectable anymore.
> We're literally looking at neurons in the model's brain that light up when prompt injection happens.
> We deleted 80% of the system prompt.
> The model is actually a little bit more intelligent without these prompts.
> Every 6 months delete your Claude MD. Delete your skills. Delete your hooks. See what the model does and it might surprise you.
> The way to think about it is almost like a like a living creature, like it's something more organic.
> Hobbling is this idea in a research that the model is doing something and you're just getting in the way.
> The model is able to do all sorts of things with today's models, not a future model, but today's model, that we have not yet realized.
> You should give the model slightly harder tasks than what you think it can do.
> The model can now rewrite essentially any code base from one language to a different language. It's just sort of crazy.
> It ran for 11 days, and it rewrote the entire code base.
> The verification I think is probably the single most important thing that people do not get right or actually.
> Don't listen to the LinkedIn influencers.
> The way the model works is you have to approach it empirically. You have to give it a task that's too hard. You have to give it the tools to verify the work like you would yourself.
> It's not a theoretical science, it's become an empirical science.
> Learn not just the computer science... but learn how to apply it.
