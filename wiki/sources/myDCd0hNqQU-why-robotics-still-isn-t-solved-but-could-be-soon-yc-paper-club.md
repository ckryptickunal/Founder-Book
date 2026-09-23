---
type: source
title: Why Robotics Still Isn't Solved - But Could Be Soon | YC Paper Club
created: 2026-09-24
updated: 2026-09-24
video_id: myDCd0hNqQU
url: https://www.youtube.com/watch?v=myDCd0hNqQU
channel: Y Combinator
published: 2026-08-08T14:00:16Z
tags:
  - robotics
  - ai
  - vla
  - sim-to-real
  - embodied-ai
  - machine-learning
  - yc-paper-club
---

# Why Robotics Still Isn't Solved - But Could Be Soon | YC Paper Club

## Metadata

- Video ID: `myDCd0hNqQU`
- Channel: Y Combinator
- Published: 2026-08-08T14:00:16Z
- URL: https://www.youtube.com/watch?v=myDCd0hNqQU

## Summary

This YC Paper Club session explores the current state of robotics, focusing on why 'solving' robotics remains elusive despite advancements in Vision-Language-Action (VLA) models. The discussion covers the challenges of the sim-to-real gap, the necessity of memory in long-horizon tasks, the role of embodied reasoning, and the practicalities of building robotics application companies.

## Key Ideas

- Robotics is currently in a 'year of demos' rather than a year of widespread deployment.
- Key hurdles include the sim-to-real gap, lack of sensory-motor feedback (epidermis), and embodiment drift.
- Adding memory to VLA policies is essential for long-horizon tasks to prevent repetitive failures and enable in-context adaptation.
- Embodied reasoning (chain-of-thought for robots) should be selective and resource-budgeted rather than exhaustive.
- Robotics application companies should focus on end-to-end business problems, starting with teleoperation and off-the-shelf hardware.
- World Action Models (WAMs) offer a path toward better physics-based reasoning but face significant latency and compute challenges.

## Entities

- [[entities/y-combinator|Y Combinator]] (organization): Startup accelerator hosting the Paper Club.
- [[entities/physical-intelligence|Physical Intelligence]] (company): Research lab focused on embodied AI.
- [[entities/rerun|Rerun]] (company): Provides infrastructure and data tools for physical AI.
- [[entities/general-instinct|General Instinct]] (company): Building infrastructure for real-time physical AI models.
- [[entities/waymo|Waymo]] (company): Autonomous vehicle company.
- [[entities/chelsea-finn|Chelsea Finn]] (person): Stanford professor and researcher in robotics.
- [[entities/marcel|Marcel]] (person): PhD student at Stanford/Physical Intelligence.
- [[entities/tyler-lum|Tyler Lum]] (person): PhD student presenting Sim-to-Real work.
- [[entities/nico|Nico]] (person): CEO of Rerun.
- [[entities/bill|Bill]] (person): Founder of General Instinct.

## Topics

- [[topics/sim-to-real-gap|Sim-to-Real Gap]]: The difficulty of transferring policies trained in simulation to the physical world due to physics discrepancies.
- [[topics/embodied-memory|Embodied Memory]]: Integrating short-term and long-term memory into robot policies to handle long-horizon tasks.
- [[topics/embodied-reasoning|Embodied Reasoning]]: Using chain-of-thought techniques to improve action prediction in data-scarce robotics environments.
- [[topics/robotics-application-companies|Robotics Application Companies]]: A business model focusing on solving specific, high-value operational problems with robots rather than general-purpose models.
- [[topics/world-action-models|World Action Models]]: Models that predict future kinematics and frames to improve robot decision-making.

## Notable Claims

- Memory is necessary for long-horizon robotic tasks. Evidence: Policies without memory (like RT-2 or Groot) fail to track progress, leading to infinite loops or burnt food.
- Selective reasoning is superior to exhaustive reasoning. Evidence: Pruning non-critical perceptual reasoning improves success rates and reduces latency in embodied agents.
- Robotics application companies are the new SaaS. Evidence: Focusing on end-to-end business problems with off-the-shelf hardware allows for faster iteration and revenue generation.

## Quotes

> It's definitely the year of the demos.
> There's no way we have robots that can do that now 'cause we don't have an epidermis.
> Selective reasoning is way more important than exhaustive reasoning.
> The physical world is brutal; everything that you do is going to break.
