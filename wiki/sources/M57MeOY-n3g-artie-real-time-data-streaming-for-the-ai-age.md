---
type: source
title: Artie: Real Time Data Streaming For The AI Age
created: 2026-05-26
updated: 2026-05-26
video_id: M57MeOY-n3g
url: https://www.youtube.com/watch?v=M57MeOY-n3g
channel: Unknown
published: Unknown
tags:
  - data-streaming
  - real-time-data
  - change-data-capture
  - data-infrastructure
  - startup
  - series-a
  - y-combinator
  - founders
  - co-founders
  - enterprise-software
  - postgresql
  - snowflake
---

# Artie: Real Time Data Streaming For The AI Age

## Metadata

- Video ID: `M57MeOY-n3g`
- Channel: Unknown
- Published: Unknown
- URL: https://www.youtube.com/watch?v=M57MeOY-n3g

## Summary

Arty, a real-time data streaming platform founded by Robin and Jacqueline, recently announced a $12 million Series A funding round. The company addresses the critical and complex problem of moving production data between various systems (e.g., PostgreSQL to Snowflake) in real-time, a task many companies struggle to build and maintain in-house. Arty's solution, which took six months to build initially, has processed over 700 billion rows of data in the last year. The founders discuss their journey from identifying the problem at previous companies like OpenDoor and Zendesk, to acquiring their first major customer (Substack) via a cold email, and scaling the company with a remarkably lean team of just four people (two founders, two engineers) to cross $1 million ARR. They also share insights into the unique dynamics of being married co-founders, the significant technical challenges overcome, and their future plans to triple the team and expand their product roadmap to support emerging AI workloads with an Events API and more real-time destinations.

## Key Ideas

- Companies face significant challenges and resource drain when attempting to build and maintain in-house real-time data streaming infrastructure.
- Arty provides a reliable, production-ready, real-time data streaming platform as a service, abstracting away complex technical challenges.
- The product, being mission-critical infrastructure, requires high reliability from inception and targets larger companies with substantial data needs.
- A lean founding team, deeply involved in both sales and engineering, can lead to rapid product iteration and efficient growth.
- The unique relationship of married co-founders can foster unfiltered feedback and accelerate decision-making, despite initial concerns about work-life balance.
- Real-time data processing involves numerous complex technical 'battle scars,' including handling diverse data sources, massive scale, edge cases, and external library bugs.
- The increasing demand for real-time data to power AI workloads and agentic AI use cases is a key driver for Arty's future growth and product expansion.
- Founders are advised to prioritize action over overthinking, embracing experimentation and learning through doing.

## Entities

- [[entities/arty|Arty]] (company): A real-time data streaming platform that helps companies move data across their systems in real time.
- [[entities/robin|Robin]] (person): Co-founder of Arty, responsible for the technical vision and building the product, previously worked at OpenDoor and Zendesk.
- [[entities/jacqueline|Jacqueline]] (person): Co-founder of Arty, responsible for the business side and sales, initially skeptical of the idea but became convinced by the market need.
- [[entities/dalton-caldwell|Dalton Caldwell]] (person): Investor in Arty's $12 million Series A round.
- [[entities/paul-bai|Paul Bai]] (person): Investor in Arty's $12 million Series A round.
- [[entities/brian-berg|Brian Berg]] (person): Investor in Arty's $12 million Series A round, from Standard Capital.
- [[entities/standard-capital|Standard Capital]] (company): Investment firm that participated in Arty's Series A funding.
- [[entities/opendoor|OpenDoor]] (company): Robin's previous employer where he first encountered the need for faster, fresher data for experimentation and operationalization.
- [[entities/zendesk|Zendesk]] (company): Robin's previous employer where he experienced challenges with data warehousing and used the Maxwell CDC tool.
- [[entities/postgresql|PostgreSQL]] (product): A common production database that Arty streams data from, often to data warehouses like Snowflake.
- [[entities/snowflake|Snowflake]] (product): A cloud data warehouse that Arty streams data to, and a company that is launching its own streaming APIs.
- [[entities/substack|Substack]] (company): Arty's first major customer, a large platform with millions of users that deployed Arty's new product in production.
- [[entities/y-combinator-yc|Y Combinator (YC)]] (organization): A startup accelerator program that Arty participated in, providing advice on growth and hiring.
- [[entities/doordash|DoorDash]] (company): Mentioned as a company that built its own in-house real-time data infrastructure with massive teams.
- [[entities/netflix|Netflix]] (company): Mentioned as a company that built its own in-house real-time data infrastructure, specifically 'DB log' for online backfills.
- [[entities/instacart|Instacart]] (company): Mentioned as a company that built its own in-house real-time data infrastructure with massive teams.
- [[entities/kafka|Kafka]] (product): A distributed streaming platform used by Arty, where a bug in its SDK caused out-of-order data issues.
- [[entities/mongodb|MongoDB]] (product): A NoSQL database mentioned for its unusual data quirks (e.g., month greater than 12).
- [[entities/sql-server|SQL Server]] (product): Microsoft's relational database, noted for its challenging and undocumented 'right way' to implement Change Data Capture.
- [[entities/data-bricks|Data Bricks]] (product): A data and AI company, mentioned as a destination for Arty's event data and for launching its own streaming APIs.
- [[entities/redshift|Redshift]] (product): Amazon's cloud data warehouse, mentioned as a destination for Arty's event data.
- [[entities/elasticsearch|ElasticSearch]] (product): A search and analytics engine, mentioned as a potential future real-time destination for Arty's data.

## Topics

- [[topics/real-time-data-streaming|Real-time Data Streaming]]: The core problem Arty solves, enabling instant movement of data between disparate systems for various business needs.
- [[topics/change-data-capture-cdc|Change Data Capture (CDC)]]: The fundamental technology Arty employs to track and stream changes from production databases efficiently.
- [[topics/data-infrastructure-challenges|Data Infrastructure Challenges]]: The complexities, resource demands, and technical 'battle scars' involved in building and maintaining robust data pipelines at scale.
- [[topics/startup-founding-and-growth|Startup Founding and Growth]]: The journey of building a startup, from identifying a problem and securing initial funding to acquiring first customers and scaling a lean team.
- [[topics/co-founder-dynamics|Co-founder Dynamics]]: The unique aspects of a married co-founder relationship, including communication styles, feedback mechanisms, and work-life integration.
- [[topics/product-market-fit|Product-Market Fit]]: Identifying a critical, unmet need in the enterprise data space that resonates strongly with potential customers, leading to rapid adoption despite being a new product.
- [[topics/ai-workloads-and-data-requirements|AI Workloads and Data Requirements]]: The increasing importance of real-time, fresh data for powering modern AI and agentic AI applications.
- [[topics/lean-startup-methodology|Lean Startup Methodology]]: The strategy of building and growing a company with minimal resources, focusing on core constraints and founder-led sales and engineering.

## Notable Claims

- Arty is a real-time data streaming platform that helps companies move data across their systems in real time. Evidence: Direct statement by the founders at the beginning of the interview.
- Arty just raised a $12 million Series A from Dalton Caldwell, Paul Bai, and Brian Berg from Standard Capital. Evidence: Direct statement by the founders.
- Building a PostgreSQL to Snowflake connector in-house can take one to two years and is not a company's core competency. Evidence: Robin's personal experience at OpenDoor and Zendesk, where attempts to build such systems failed or were deemed too difficult.
- It took Arty about six months to build its core infrastructure initially, but with current tools (like AI), it could be done in two to three months now. Evidence: Robin's direct statement and reflection on the development timeline.
- Arty's first major customer was Substack, acquired through a cold email. Evidence: Jacqueline's direct statement and anecdote about the cold email and rapid response.
- Arty crossed $1 million ARR with only two founders and two engineers. Evidence: Direct statement by the founders, highlighting their lean operational model.
- Over the last 12 months, Arty has processed over 700 billion rows of data, a 12x increase from the previous year. Evidence: Jacqueline's direct statement about the company's operational scale and growth.
- A Kafka SDK library used by Arty had a bug that caused out-of-order data reads during rebalancing, requiring a vendor switch. Evidence: Robin's detailed explanation of a year-long debugging process to identify and resolve the issue.

## Quotes

> "Arti is a real time data streaming platform. Um what that means is we help companies move data across their systems in real time."
> "Unless it's a company P 0 don't don't don't bother."
> "Spending a year to two years building a Postgress to Snowflake connector just seems weird like just seems nonsensical. Yeah. It seems like not anyone's else's core competency."
> "If it doesn't exist, let me just build it myself."
> "Anything that needs to be real time is by definition like mission critical."
> "A bad employee is worse than no employee at all."
> "Because we are married um there is a layer of filter that is naturally removed... Every little thing every little thing an inkling of a thought gets discussed."
> "Data processing honestly is like a series of accumulated battle scars that you just learn and build resilience towards."
> "Your bug is your bug and so like you you end up having to like take responsibility for the whole thing."
> "Don't overthink something and you know either you take the YC advice, just try it. It may not always work, but at least you just do it."
