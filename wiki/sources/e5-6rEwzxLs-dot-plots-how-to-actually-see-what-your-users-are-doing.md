---
type: source
title: Dot Plots: How to Actually See What Your Users Are Doing
created: 2026-08-06
updated: 2026-08-06
video_id: e5-6rEwzxLs
url: https://www.youtube.com/watch?v=e5-6rEwzxLs
channel: Y Combinator
published: 2026-07-09T14:00:05Z
tags:
  - user-analytics
  - product-management
  - startup-metrics
  - data-visualization
  - user-behavior
  - retention
  - churn
  - b2b
  - product-market-fit
  - y-combinator
  - founders
  - dau
---

# Dot Plots: How to Actually See What Your Users Are Doing

## Metadata

- Video ID: `e5-6rEwzxLs`
- Channel: Y Combinator
- Published: 2026-07-09T14:00:05Z
- URL: https://www.youtube.com/watch?v=e5-6rEwzxLs

## Summary

The video introduces 'dot plots' as a powerful visualization tool for founders to understand individual user behavior, contrasting them with misleading aggregate metrics like DAUs/MAUs. A dot plot represents individual users as rows and time periods (typically days) as columns, with dots indicating value-generating user actions. This method helps identify usage patterns, retention issues, and the impact of specific features, providing insights not visible through traditional analytics. The speaker demonstrates how to construct and interpret dot plots, discusses advanced applications like tracking user state and sorting, and explains their scalability from early-stage startups to large companies like Google Photos. It also highlights their utility for B2B products in monitoring account health and preventing churn, while cautioning against common misuses like charting non-value-generating events or using overly broad time periods. The video concludes by emphasizing that dot plots complement cohort retention curves, offering a deeper understanding of 'how' users engage with a product.

## Key Ideas

- Aggregate user metrics (e.g., DAUs, MAUs) often obscure individual user behavior and can be misleading about product success.
- Dot plots visualize individual user activity over time, with each row representing a user and columns representing time periods (e.g., days), marked with dots for value-generating events.
- This visualization helps identify specific usage patterns (e.g., weekday vs. weekend users), diagnose retention problems, and understand the impact of features.
- Dot plots can be enhanced by tracking user states (e.g., device type, demographics) and sorting users based on attributes to reveal deeper insights.
- The tool scales from small startups to large enterprises (e.g., Google Photos with billions of users) by sampling user segments.
- Dot plots are valuable for B2B products to monitor customer engagement, identify inactive seats, and predict churn.
- Crucial for effective dot plots is choosing events that represent actual user value (e.g., 'listen to a song' instead of 'opened the app') and using appropriate time granularity (daily is often best).
- Dot plots are a simple logs visualization tool, easily implementable, and should be used in conjunction with cohort retention curves for a comprehensive understanding of user engagement.

## Entities

- [[entities/dave|Dave]] (person): The speaker and presenter of the video, sharing insights from his startup experience.
- [[entities/y-combinator|Y Combinator]] (organization): Startup accelerator and the channel hosting the video.
- [[entities/spotify|Spotify]] (company): Music streaming app used as an example to illustrate dot plot application.
- [[entities/bump|Bump]] (company): Speaker's previous startup where they used advanced dot plot techniques with different symbols.
- [[entities/github|GitHub]] (product): Code hosting platform whose contribution graph is cited as a familiar example of a dot plot.
- [[entities/max-levchin|Max Levchin]] (person): Co-founder of PayPal, whose approach to fraud detection through visual pattern recognition inspired the speaker's understanding of dot plots.
- [[entities/paypal|PayPal]] (company): Online payment system whose early fraud detection methods involved human visual analysis of transaction graphs.
- [[entities/google-photos|Google Photos]] (product): Photo storage and sharing service where dot plots were used to analyze user behavior at a massive scale (over a billion users).
- [[entities/reddit|Reddit]] (product): Social news aggregation, content rating, and discussion website, mentioned in the context of user demographics (e.g., 'college kid that you just got on Reddit').

## Topics

- [[topics/user-analytics|User Analytics]]: Methods and tools for understanding how users interact with a product, focusing on individual behavior rather than just aggregate numbers.
- [[topics/data-visualization|Data Visualization]]: The use of graphical representations to display and analyze data, specifically introducing and explaining 'dot plots' as a novel approach.
- [[topics/product-market-fit|Product-Market Fit]]: Identifying if a product satisfies a strong market demand, with dot plots serving as a signal for whether people truly want and use the product.
- [[topics/user-retention|User Retention]]: Strategies and metrics for keeping users engaged with a product over time, with dot plots providing granular insights into retention patterns and issues.
- [[topics/b2b-product-management|B2B Product Management]]: Applying user analytics techniques, like dot plots, to understand and manage engagement within business-to-business software contexts, particularly for monitoring account health and preventing churn.
- [[topics/startup-metrics|Startup Metrics]]: Key performance indicators and measurement tools essential for early-stage companies to track progress and make informed decisions about product development and user engagement.

## Notable Claims

- Relying on aggregate user metrics (like DAUs/MAUs) is one of the biggest mistakes founders make. Evidence: Aggregate graphs tend to go 'up and to the right' even if users aren't enjoying the product, masking individual user behavior. A DAU graph example is shown to illustrate its lack of detail compared to a dot plot.
- Dot plots allow you to understand what's going on with individual users while also giving a big picture view of product performance. Evidence: The construction of a dot plot (users as rows, time as columns, dots for events) visually represents individual journeys, and patterns emerge when viewing the plot in aggregate.
- Dot plots help identify patterns that would not be seen with aggregate charts or individual user logs. Evidence: The Spotify example reveals distinct patterns like 'weekday listeners' vs. 'weekend users' and immediate churn after onboarding, which are invisible in DAU graphs.
- Dot plots scale to thousands, millions, or even billions of users through sampling. Evidence: The speaker mentions using dot plots at Google Photos when it had over a billion users, by printing out plots for different sampled segments of the user base (e.g., 'iOS users in France').
- Dot plots can be very useful for B2B products to monitor account health and prevent churn. Evidence: An example is given of a B2B company that lost an $80,000/year contract because only 3 out of 10 seats activated and showed sporadic usage, a problem that could have been identified early with a dot plot.
- Choosing the wrong event (e.g., 'opened the app') or too wide a time period (e.g., weeks) are common misuses of dot plots. Evidence: These choices don't measure real user value or hide granular patterns, making it harder to understand actual engagement. The speaker advises picking value-generating events and daily granularity.
- Dot plots are a simple logs visualization tool that modern AI coding tools can create quickly. Evidence: They involve 'no fancy computations' and basically require parsing logs into a 2D grid, which can be 'whipped up in like 10 minutes' by AI coding tools.
- Dot plots are best used in conjunction with cohort retention curves. Evidence: Cohort retention curves show 'if' users stick over time, while dot plots show 'how' those users are actually using the product, providing complementary insights.

## Quotes

> One of the biggest mistakes I see founders make is relying on aggregate user metrics instead of understanding how any individual users use their product.
> But what you don't know is how are they using your product? How are they interacting? What features are they using? What's the frequency of use? What's the the pacing of how they use the product?
> What's really cool about this is it lets you figure out patterns that you probably would not have seen with your human brain just looking at aggregate charts or looking at individual user logs.
> Is your brain will start to notice these patterns in a way that you would never have figured out on your own.
> Dot plots give you a lot more granularity about what's going on with your users.
> Until you have hundreds of users, the dot plot could be your only dashboard.
> Cohort retention curves teach you in aggregate whether groups of users that you acquire stick with you over time... But the dot plot shows you how those users are actually using your product.
