---
type: source
title: Why Arc Isn't Especially Object-Oriented
created: 2026-05-26
updated: 2026-05-26
video_id: pg-why-arc-isn-t-especially-object-oriented
url: https://www.youtube.com/watch?v=pg-why-arc-isn-t-especially-object-oriented
channel: Paul Graham Essays
published: Unknown
tags:
  - programming
  - software-engineering
  - lisp
  - oop
  - language-design
---

# Why Arc Isn't Especially Object-Oriented

## Metadata

- Video ID: `pg-why-arc-isn-t-especially-object-oriented`
- Channel: Paul Graham Essays
- Published: Unknown
- URL: https://www.youtube.com/watch?v=pg-why-arc-isn-t-especially-object-oriented

## Summary

Paul Graham argues that object-oriented programming (OOP) is often overvalued and unnecessary, suggesting it is frequently used as a crutch for language limitations or as a way to manage large, mediocre programming teams rather than as a superior architectural paradigm.

## Key Ideas

- OOP is a useful technique in specific domains but should not be the default paradigm for all programming.
- OOP is often used to compensate for the lack of powerful language features like lexical closures and macros.
- Large companies favor OOP because it imposes a restrictive discipline on large, changing teams of mediocre developers.
- OOP can create unnecessary 'scaffolding' that makes simple tasks appear more complex and labor-intensive than they are.
- Powerful languages like Lisp allow developers to achieve the benefits of OOP (like state management) through simpler mechanisms like hash tables and closures.

## Entities

- [[entities/paul-graham|Paul Graham]] (person): Programmer, venture capitalist, and essayist.
- [[entities/common-lisp|Common Lisp]] (project): A dialect of the Lisp programming language.
- [[entities/clos|CLOS]] (project): Common Lisp Object System.

## Topics

- [[topics/object-oriented-programming|Object-Oriented Programming]]: A programming paradigm based on the concept of objects, which Graham critiques for its tendency toward bloat and unnecessary complexity.
- [[topics/language-design|Language Design]]: The philosophy of including features in a programming language based on actual necessity versus perceived industry trends.

## Notable Claims

- OOP is popular in big companies because it prevents mediocre programmers from doing damage. Evidence: Graham notes that OOP imposes a discipline that forces code into protocols, which limits individual developer impact at the cost of code bloat.
- OOP is often used to simulate features missing in statically-typed languages. Evidence: Graham points to the lack of lexical closures and macros as a primary driver for the adoption of OOP in certain languages.

## Quotes

> You should be able to define new types, but you shouldn't have to express every program as the definition of new types.
> Object-oriented programming is like crack for these people: it lets you incorporate all this scaffolding right into your source code.
> It seems more dangerous to put stuff in that you've never needed because it's thought to be a good idea.
