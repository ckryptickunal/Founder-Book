---
type: source
title: Programming Bottom-Up
created: 2026-05-26
updated: 2026-05-26
video_id: pg-programming-bottom-up
url: https://www.youtube.com/watch?v=pg-programming-bottom-up
channel: Paul Graham Essays
published: September 1993
tags:
  - lisp
  - programming-philosophy
  - software-architecture
  - productivity
  - abstraction
---

# Programming Bottom-Up

## Metadata

- Video ID: `pg-programming-bottom-up`
- Channel: Paul Graham Essays
- Published: September 1993
- URL: https://www.youtube.com/watch?v=pg-programming-bottom-up

## Summary

This essay, an introduction to the book 'On Lisp', contrasts traditional top-down programming design with the bottom-up approach favored by Lisp programmers, where the language is extended to fit the specific problem, resulting in more concise, reusable, and maintainable code.

## Key Ideas

- Top-down design involves breaking a program into subroutines based on its functional requirements.
- Bottom-up design involves building the language up toward the program by creating new operators as needed.
- Language and program should evolve together until the language appears custom-designed for the task.
- Bottom-up design reduces complexity by creating a larger, more abstract language and a smaller, more agile program.
- Small teams using Lisp can achieve higher individual productivity and outperform larger groups.

## Entities

- [[entities/paul-graham|Paul Graham]] (person): Author of the essay and the book On Lisp.
- [[entities/lisp|Lisp]] (product): A family of programming languages known for its flexibility and support for bottom-up design.
- [[entities/frederick-brooks|Frederick Brooks]] (person): Author of The Mythical Man-Month.

## Topics

- [[topics/software-design-methodology|Software Design Methodology]]: The comparison between top-down decomposition and bottom-up language extension.
- [[topics/code-reusability|Code Reusability]]: How building a substrate of utilities facilitates faster development of future programs.
- [[topics/team-productivity|Team Productivity]]: The observation that smaller teams can be more productive than larger ones, especially when using powerful abstraction tools.

## Notable Claims

- Bottom-up design leads to smaller, more agile programs. Evidence: By abstracting bookkeeping into language features, the remaining program logic is shorter and has fewer components.
- Small teams are more productive than large teams. Evidence: References Frederick Brooks' law on group productivity and suggests that Lisp techniques amplify the efficiency of small groups.

## Quotes

> In Lisp, you don't just write your program down toward the language, you also build the language up toward your program.
> Like the border between two warring states, the boundary between language and program is drawn and redrawn, until eventually it comes to rest along the mountains and rivers, the natural frontiers of your problem.
> As industrial designers strive to reduce the number of moving parts in a machine, experienced Lisp programmers use bottom-up design to reduce the size and complexity of their programs.
