---
type: source
title: How Facebook could have built Threads 30X faster & cheaper
created: 2026-05-27
updated: 2026-05-27
video_id: O2dIsZsjaBA
url: https://www.youtube.com/watch?v=O2dIsZsjaBA
channel: Garry Tan
published: 2023-08-22T19:11:48Z
tags:
  - software-engineering
  - data-infrastructure
  - rama
  - scalability
  - back-end-development
  - database-architecture
---

# How Facebook could have built Threads 30X faster & cheaper

## Metadata

- Video ID: `O2dIsZsjaBA`
- Channel: Garry Tan
- Published: 2023-08-22T19:11:48Z
- URL: https://www.youtube.com/watch?v=O2dIsZsjaBA

## Summary

Garry Tan introduces Rama, a new data back-end platform by Red Planet Labs, arguing that it allows developers to build scalable, complex back-end systems with significantly less code and infrastructure than traditional stacks by replacing multiple specialized databases with a unified, data-structure-centric abstraction.

## Key Ideas

- Traditional data stacks rely on multiple, disconnected databases (MySQL, Redis, MongoDB, etc.), leading to redundant code, increased surface area for bugs, and scaling challenges.
- Rama generalizes back-end development by integrating distributed logs (Depots), ETL topologies, and partition states (P-States) into a single system.
- P-States allow developers to define custom data structures rather than being restricted to the fixed indexing models of traditional databases.
- Rama enables massive scalability and auto-scaling with significantly fewer lines of code compared to industry standards like Twitter or Mastodon.
- The platform is designed for modern data centers where scaling is achieved by adding more servers rather than larger ones.

## Entities

- [[entities/garry-tan|Garry Tan]] (person): Investor, CEO of Initialized Capital, and host of the channel.
- [[entities/nathan-marz|Nathan Marz]] (person): Creator of Rama and Apache Storm, author of Big Data books.
- [[entities/red-planet-labs|Red Planet Labs]] (company): The company behind the Rama data platform.
- [[entities/rama|Rama]] (product): A general-purpose data back-end platform that integrates storage, indexing, and processing.
- [[entities/apache-storm|Apache Storm]] (project): A distributed stream processing computation framework.
- [[entities/mastodon|Mastodon]] (project): An open-source decentralized social network.

## Topics

- [[topics/data-abstraction|Data Abstraction]]: Moving away from fixed database models toward flexible, user-defined data structures.
- [[topics/scalability|Scalability]]: The ability to handle massive throughput (e.g., 3,500 statuses per second) by distributing data across clusters.
- [[topics/developer-productivity|Developer Productivity]]: Reducing the 'DRY' (Don't Repeat Yourself) principle by eliminating the need to manage multiple disparate database technologies.

## Notable Claims

- Rama can build a Twitter-scale social network with 100x less code than traditional methods. Evidence: Comparison of a Rama-based Mastodon clone (10,000 lines of code) versus the original Twitter consumer product (1 million lines of code).
- Traditional database models are restrictive and force developers to deploy multiple systems. Evidence: The reliance on fixed models like key-value, document, or graph databases which lack the flexibility of Rama's P-States.

## Quotes

> If Rama had existed in 2008, my startup Posterous wouldn't have died.
> We're literally repeating ourselves over and over again in that data stack.
> The startup that you save might be your own.
