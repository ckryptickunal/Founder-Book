---
type: source
title: Better Bayesian Filtering
created: 2026-05-26
updated: 2026-05-26
video_id: pg-better-bayesian-filtering
url: https://www.youtube.com/watch?v=pg-better-bayesian-filtering
channel: Paul Graham Essays
published: January 2003
tags:
  - spam
  - bayesian
  - machine-learning
  - email
  - algorithms
  - programming
  - optimization
---

# Better Bayesian Filtering

## Metadata

- Video ID: `pg-better-bayesian-filtering`
- Channel: Paul Graham Essays
- Published: January 2003
- URL: https://www.youtube.com/watch?v=pg-better-bayesian-filtering

## Summary

In this 2003 talk, Paul Graham discusses improvements to his Bayesian spam filtering algorithm, emphasizing the importance of using full email data (including headers), smarter tokenization, and handling false positives as bugs rather than just performance metrics. He argues that individual, user-specific filters are more effective than network-level solutions because they force spammers into a slow, inefficient optimization cycle.

## Key Ideas

- Spam filtering is not just text classification; it requires treating email structure and false positives with specific care.
- Ignoring email headers is a major mistake in filter design; they contain critical information for identifying spam.
- Tokenization should be sophisticated, preserving case, punctuation, and context (e.g., Subject vs. Body).
- False positives should be treated as bugs to be debugged, while filtering rate is an optimization problem.
- Individualized filters are superior to network-level filters because they make it impossible for spammers to optimize their messages against a single, static target.
- Degeneration (falling back to less specific tokens) is an effective strategy when exact matches are not found.

## Entities

- [[entities/paul-graham|Paul Graham]] (person): Author of the essay and developer of the Bayesian spam filtering approach.
- [[entities/crm114|CRM114]] (project): A highly effective statistical spam filter developed by Bill Yerazunis.
- [[entities/microsoft-research|Microsoft Research]] (organization): Research division that published early work on Bayesian spam filtering.
- [[entities/virtumundo|Virtumundo]] (company): An email marketing company mentioned in the context of false positives.

## Topics

- [[topics/bayesian-filtering|Bayesian Filtering]]: A statistical method for classifying email as spam or legitimate based on token probabilities.
- [[topics/tokenization|Tokenization]]: The process of breaking text into meaningful units for analysis, which Graham argues should be context-aware.
- [[topics/false-positives|False Positives]]: The accidental classification of legitimate mail as spam, which Graham argues is a more severe error than false negatives.

## Notable Claims

- Ignoring email headers significantly degrades the performance of a spam filter. Evidence: Graham notes that early filters ignoring headers performed poorly compared to his own, which included header data.
- Individualized filters are more effective than network-level filters. Evidence: Individual filters force spammers to test against millions of unique targets, breaking their optimization loop.

## Quotes

> There is a lesson here for filter writers: don't ignore data.
> Filtering is an optimization problem, and the key to optimization is profiling.
> I approach improving the filtering rate as optimization, and decreasing false positives as debugging.
> You can't dictate the problem to fit your solution.
