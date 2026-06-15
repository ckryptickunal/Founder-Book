---
type: source
title: Filters that Fight Back
created: 2026-05-26
updated: 2026-05-26
video_id: pg-filters-that-fight-back
url: https://www.youtube.com/watch?v=pg-filters-that-fight-back
channel: Paul Graham Essays
published: August 2003
tags:
  - spam
  - cybersecurity
  - email
  - bayesian-filtering
  - internet-infrastructure
---

# Filters that Fight Back

## Metadata

- Video ID: `pg-filters-that-fight-back`
- Channel: Paul Graham Essays
- Published: August 2003
- URL: https://www.youtube.com/watch?v=pg-filters-that-fight-back

## Summary

Paul Graham proposes a 'punish' mode for Bayesian spam filters that automatically spiders URLs found in suspected spam emails, effectively launching a distributed denial-of-service attack against spammers' servers to increase their costs and render their infrastructure ineffective.

## Key Ideas

- Spam filters can be improved by actively visiting URLs contained in suspicious emails.
- Widespread use of auto-retrieving filters would force spammers to bear the cost of their own high-volume traffic.
- This approach turns the spammer's volume against them, causing their servers to crash or become unavailable.
- The strategy could force spammers to adopt legitimate practices, such as providing working unsubscribe links.
- Implementation requires safeguards like blacklists to avoid attacking legitimate services like Yahoo Mail or Hotmail.

## Entities

- [[entities/paul-graham|Paul Graham]] (person): Computer scientist, essayist, and venture capitalist.
- [[entities/richard-jowsey|Richard Jowsey]] (person): Creator of death2spam.
- [[entities/death2spam|death2spam]] (project): An early spam filtering project.
- [[entities/yahoo-mail|Yahoo Mail]] (company): Email service provider.
- [[entities/hotmail|Hotmail]] (company): Email service provider.

## Topics

- [[topics/bayesian-spam-filtering|Bayesian Spam Filtering]]: A statistical technique for filtering email based on word frequency.
- [[topics/active-defense|Active Defense]]: The concept of using software to actively counter malicious actors rather than passively blocking them.
- [[topics/infrastructure-costs|Infrastructure Costs]]: The economic impact of bandwidth and server load on spam operations.

## Notable Claims

- Auto-retrieving spam filters would drive up spammer costs and decrease their sales. Evidence: By forcing spammer servers to handle millions of automated hits, the servers would crash, preventing legitimate victims from accessing the spam sites.
- This method would eventually force spammers to include working unsubscribe links. Evidence: If spammers want to keep their servers online, they would need to reduce the volume of traffic, making 'auto-unsubscribing' a necessity for survival.

## Quotes

> The huge volume of the spam, which has so far worked in the spammer's favor, would now work against him, like a branch snapping back in his face.
> If auto-retrieving filters became widespread, they'd become auto-unsubscribing filters.
