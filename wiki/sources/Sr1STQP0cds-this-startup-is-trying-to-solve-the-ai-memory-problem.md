---
type: source
title: This Startup Is Trying To Solve The AI Memory Problem
created: 2026-05-26
updated: 2026-05-26
video_id: Sr1STQP0cds
url: https://www.youtube.com/watch?v=Sr1STQP0cds
channel: Unknown
published: Unknown
tags:
  - ai
  - llm
  - memory-layer
  - ai-agents
  - open-source
  - mm0
  - mezero
  - stateless-llms
  - context-window
  - cost-optimization
  - latency-reduction
  - startup
---

# This Startup Is Trying To Solve The AI Memory Problem

## Metadata

- Video ID: `Sr1STQP0cds`
- Channel: Unknown
- Published: Unknown
- URL: https://www.youtube.com/watch?v=Sr1STQP0cds

## Summary

MM0 (Mezero) is building the memory layer for AI agents, addressing the fundamental issue of Large Language Models (LLMs) being stateless. Their solution enables AI agents to remember user preferences and past interactions, leading to improved performance, personalized experiences, and significant cost/latency savings for developers by optimizing prompt context. MM0 is an open-source solution with substantial market traction (14M+ Python package downloads, 41K+ GitHub stars) and recently secured $24 million in funding. The company emphasizes decoupling memory from specific LLM providers, making it neutral and portable across various agentic frameworks like AWS agents SDK, crewi, and flow wise. Founded by Taranjit and Desh, MM0's genesis came from a consumer app (Sudguru AI) that highlighted the critical need for AI memory. Their vision is to build the infrastructure for a future where all AI agents seamlessly remember and understand users, drastically reducing friction in human-AI interaction.

## Key Ideas

- LLMs are fundamentally stateless, causing AI agents to forget past interactions and start from scratch with each prompt.
- MM0 provides a 'memory layer' that allows AI agents to remember user preferences and past interactions, leading to continuous improvement over time.
- MM0's solution offers significant benefits to developers, including personalized AI experiences, cost savings through optimized prompt context, and reduced latency.
- The product utilizes a hybrid data store architecture (key-value, semantic chunk, graph memory) for efficient storage and real-time retrieval of relevant information.
- Memory for AI applications should be decoupled from specific LLM providers and remain neutral across different agentic frameworks to ensure developer ownership and flexibility.
- The initial idea for MM0 stemmed from a consumer app (Sudguru AI) built by the founders, which demonstrated the critical need for AI to remember user context.
- MM0 is an open-source project that has achieved widespread adoption and integration within the AI developer community.
- The long-term vision for MM0 is to enable a future where all AI agents deeply know and understand users, facilitating seamless and low-friction interactions across numerous AI applications.
- Founders' advice for entrepreneurs includes maintaining strong focus (DFS over BFS) and cultivating unwavering self-belief.

## Entities

- [[entities/taranjit|Taranjit]] (person): Co-founder of MM0, serial entrepreneur (7th attempt), originally from India.
- [[entities/desh|Desh]] (person): Co-founder and CTO of MM0, undergrad friend of Taranjit, previously led the AI platform team at Tesla Autopilot.
- [[entities/mm0-mezero|MM0 (Mezero)]] (company): Startup building the memory layer for AI agents, addressing the statelessness of LLMs. It is an open-source solution that recently raised $24M.
- [[entities/llm|LLM]] (other): Large Language Models, a core technology in AI agents, identified as fundamentally stateless.
- [[entities/aws|AWS]] (company): Amazon Web Services, a major cloud provider whose agent SDK (Strands) uses MM0 as an exclusive memory provider.
- [[entities/crewi|crewi]] (product): An agentic framework that MM0 powers memory for.
- [[entities/flow-wise|flow wise]] (product): An agentic framework that MM0 powers memory for.
- [[entities/tesla-autopilot|Tesla Autopilot]] (project): The AI platform team where Desh previously worked.
- [[entities/yc-y-combinator|YC (Y Combinator)]] (organization): Startup accelerator that MM0 joined in the Summer 2024 batch.
- [[entities/embed-chain|embed chain]] (project): The initial name of MM0's product when applying to YC, which focused on RAG before pivoting to a dedicated memory layer.
- [[entities/sudguru-ai|Sudguru AI]] (product): A consumer app built by Taranjit and Desh in December 2023 that went viral, highlighting the need for AI memory and leading to MM0's genesis.
- [[entities/sadguru|Sadguru]] (person): A famous Indian yogi who inspired the Sudguru AI app.
- [[entities/openai|OpenAI]] (company): A leading AI research and deployment company that recently launched its own memory layer, validating the market need for MM0's solution.
- [[entities/kindred|Kindred]] (company): Venture capital firm that led MM0's seed funding round.
- [[entities/basiset|Basiset]] (company): Venture capital firm that led MM0's Series A funding round and participated in their seed round.
- [[entities/lan|Lan]] (person): Individual associated with Basiset, known to the MM0 founders.
- [[entities/peak-15|Peak 15]] (company): Venture capital firm that invested in MM0.
- [[entities/strands|Strands]] (product): AWS agent SDK for which MM0 is the exclusive memory provider.

## Topics

- [[topics/ai-memory-layer|AI Memory Layer]]: Discussion of the fundamental problem of stateless LLMs and how MM0 provides a crucial memory layer for AI agents to remember past interactions and user preferences.
- [[topics/mm0-product-technology|MM0 Product & Technology]]: Explanation of MM0's core offering, its hybrid data store architecture (key-value, semantic, graph memory), and how it enables personalized, cost-effective, and low-latency AI applications.
- [[topics/open-source-strategy-adoption|Open Source Strategy & Adoption]]: MM0's success as an open-source project, evidenced by millions of Python package downloads and GitHub stars, and its integration with major agentic frameworks.
- [[topics/startup-journey-pivot|Startup Journey & Pivot]]: The founders' background, their experience with Y Combinator, and the pivotal moment when a consumer app (Sudguru AI) inspired the shift from RAG to building a dedicated memory layer for AI.
- [[topics/funding-growth|Funding & Growth]]: Details of MM0's recent $24 million seed plus Series A funding round, including key investors, and plans for using the funds to expand the team and product development.
- [[topics/market-positioning-decoupling|Market Positioning & Decoupling]]: MM0's strategy to remain relevant and essential even as major LLM providers like OpenAI introduce their own memory solutions, emphasizing the importance of decoupling memory from model providers for developer flexibility and ownership.
- [[topics/future-of-ai-agentic-interfaces|Future of AI & Agentic Interfaces]]: The founders' vision for a future where AI agents deeply understand and remember users, leading to seamless, low-friction interactions across numerous AI applications, and MM0's role in building that infrastructure.
- [[topics/founder-advice|Founder Advice]]: Insights and lessons learned from the founders' entrepreneurial journey, emphasizing the importance of focus (DFS over BFS) and unwavering self-belief.

## Notable Claims

- LLMs are fundamentally stateless. Evidence: LLMs are stateless. They don't remember things like human remembers.
- MM0 is the most adopted solution in the market for AI memory. Evidence: We are the most adopted solution in the market in terms of traction. We recently crossed 14 million Python package downloads, 41,000 GitHub stars.
- MM0 helps developers save cost and latency. Evidence: for developers we also help them save cost because you optimize the prompt and you also help them save latency.
- Memory should be decoupled from model providers. Evidence: you would not want to tie your memory to any you know model provider out there for model provider it memory is the next mode because models are becoming having a commodity but for a developer because they are using multiple LLMs it should be decoupled
- MM0 is the exclusive memory provider for the AWS agent SDK called Strands. Evidence: we are the exclusive memory provider in the a AWS agent SDK called strands

## Quotes

> Mezero is building memory layer for AI agents. Right now everybody is trying to create an AI agent and all of them are using LLM. But there's a fundamental issue. LLMs are stateless. They don't remember things like human remembers. So we are trying to fix that for every agent and every AI app that anybody is creating out there.
> The main benefit for anyone who is using a solution like me zero in their AI agent is like their agent improves uh over time.
> Instead of like talking everything that happened and then copy pasting that in the prompt, you can be more smart about what you share.
> The fact that it's good for us is because they're educating the market that you need memory as a default primitive in any AI application but for us it's good because developers are using multiple LLMs whenever they're building an AI application right and memory is not just read only memory is write only also so in that case as in you know best engineering practice and even like as a first principal thinking you would not want to tie your memory to any you know model provider out there
> We call it like make it work, make it neutral and make it portable.
> I think everything is possible. You just have to believe in it and you just have to make it work.
