---
type: source
title: How to Build an Internal AI Agent That Evolves Itself
created: 2026-05-26
updated: 2026-05-26
video_id: DGD9b8K42lk
url: https://www.youtube.com/watch?v=DGD9b8K42lk
channel: Unknown
published: Unknown
tags:
  - ai-agents
  - startup-productivity
  - automation
  - self-evolving-ai
  - ai-architecture
  - business-operations
  - customer-support-automation
  - tool-creation
  - llm-applications
  - answer-this
---

# How to Build an Internal AI Agent That Evolves Itself

## Metadata

- Video ID: `DGD9b8K42lk`
- Channel: Unknown
- Published: Unknown
- URL: https://www.youtube.com/watch?v=DGD9b8K42lk

## Summary

Ayush, founder of Answer This, explains how their company achieved $2 million in ARR with only two full-time employees by leveraging a self-extending AI agent. This internal AI ops agent automates over 100 emails daily, closes hundreds of support tickets, and handles CRM updates. Crucially, the agent is 'self-extending,' meaning it can autonomously code new tools for repeated tasks it encounters, making them permanently available. The architecture involves a Claude code CLI, read-only access to the company's database and codebase, and an editable 'instructions.md' file that allows the agent to self-evolve its behavior based on feedback, effectively giving it factual, behavioral, and procedural memories.

## Key Ideas

- Answer This achieved $2M ARR with only two full-time employees by extensively using an internal AI ops agent.
- The AI agent is 'self-extending,' capable of building its own permanent tools for new or repeated tasks it cannot yet perform.
- The agent's architecture includes a Claude code CLI, a task queue, read-only access to the database and codebase, and a general coding agent as a CLI.
- An editable 'instructions.md' file serves as the agent's 'personality' or memory, allowing it to update its own behavior based on direct feedback.
- Effective internal AI agents require three types of memory: factual (codebase, database), behavioral (instructions, feedback), and procedural (encoded into self-created tools).
- The setup can be replicated by using a coding-capable CLI as the main harness, providing read-only access to the codebase, basic CLIs, a coding agent CLI, and an editable instruction file.

## Entities

- [[entities/ayush|Ayush]] (person): Founder of Answer This, speaker in the video.
- [[entities/answer-this|Answer This]] (company): A company that builds AI agents for evidence-based scientific workflows, and the subject of the case study.
- [[entities/ryan|Ryan]] (person): Co-founder of Answer This, non-technical, who provided feedback directly to the AI agent.
- [[entities/claude-code-cli|Claude Code CLI]] (product): A coding-capable command-line interface used as the main harness for the AI agent.
- [[entities/intercom|Intercom]] (product): A startup tool mentioned as one of the CLIs given to the main AI agent.
- [[entities/fathom|Fathom]] (product): A startup tool mentioned as one of the CLIs given to the main AI agent.
- [[entities/stripe|Stripe]] (product): A payment processing tool mentioned as one of the CLIs given to the main AI agent.
- [[entities/slack|Slack]] (product): A communication platform used for task queues and direct interaction with the AI agent.
- [[entities/python|Python]] (other): Programming language used to wrap the Claude code CLI.

## Topics

- [[topics/ai-agents-in-business|AI Agents in Business]]: Discussion on how AI agents can be deployed to automate operational tasks, reduce manual labor, and significantly boost productivity and revenue in startups.
- [[topics/self-evolving-ai-systems|Self-Evolving AI Systems]]: Exploration of AI systems that can autonomously learn, adapt, and extend their capabilities by coding new tools and modifying their own behavior based on feedback.
- [[topics/startup-efficiency-and-scaling|Startup Efficiency and Scaling]]: Strategies for achieving high revenue and operational efficiency with minimal human resources through advanced automation and AI integration.
- [[topics/ai-architecture-and-implementation|AI Architecture and Implementation]]: Technical details and practical steps for setting up a self-extending AI agent, including memory types, tool integration, and feedback mechanisms.
- [[topics/automated-customer-support|Automated Customer Support]]: How AI agents can handle customer inquiries, update CRM, collect feedback, and self-correct mistakes in customer support workflows.

## Notable Claims

- Answer This achieved over $2 million in ARR with only two full-time employees. Evidence: Stated by Ayush, the founder of Answer This, who is one of the two full-time employees.
- The internal AI agent processes more than 100 emails a day and has closed over 400 customer support tickets. Evidence: Directly stated by Ayush as a performance metric of their AI agent.
- The AI agent is self-extending; it can build permanent tools for new tasks by asking a coding sub-agent. Evidence: Described as a core, unique feature of their AI agent's architecture by Ayush.
- The AI agent has grown from a skeleton to a full-blown tool with over 45 CLIs that it has made itself. Evidence: Stated by Ayush, illustrating the agent's self-authoring capabilities and growth.
- The AI agent can correct its own behavioral mistakes by updating its instruction set based on direct feedback. Evidence: An anecdote shared by Ayush where his co-founder Ryan messaged the agent in Slack to correct a class of support mistakes, which then ceased to occur.

## Quotes

> "We've been able to do over $2 million in ARR largely being two full-time employees, which is myself and my co-founder."
> "The most important part of this is not that the agent can do a fixed set of tasks, is that the agent is self-extending."
> "When it runs into a repeated task it cannot do yet, it asks a coding sub-agent to build a tool for it, and this tool becomes permanent and is available in future sessions."
> "To us it's magical because we only ask it to do things, but it's able to self-author tools and has gone from just being a skeleton to being this full-blown tool with over 45 CLIs that it has made itself."
> "The agent updated its own instruction set and tool link and then that entire class of mistakes stopped happening again."
> "An internal agent needs sort of three sorts of memories. It needs factual memories... It needs behavioral memories... And it needs procedural memory."
