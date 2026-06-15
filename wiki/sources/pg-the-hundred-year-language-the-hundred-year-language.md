---
type: source
title: The Hundred-Year Language
created: 2026-05-26
updated: 2026-05-26
video_id: pg-the-hundred-year-language
url: https://www.youtube.com/watch?v=pg-the-hundred-year-language
channel: Paul Graham Essays
published: April 2003
tags:
  - programming-languages
  - software-engineering
  - language-design
  - computer-science
  - evolution
  - optimization
  - lisp
---

# The Hundred-Year Language

## Metadata

- Video ID: `pg-the-hundred-year-language`
- Channel: Paul Graham Essays
- Published: April 2003
- URL: https://www.youtube.com/watch?v=pg-the-hundred-year-language

## Summary

In this 2003 keynote, Paul Graham explores the evolution of programming languages by projecting their trajectory over the next century. He argues that languages evolve like species, with some becoming 'evolutionary dead-ends' (like Cobol or Java) and others forming main branches. Graham posits that the most successful future languages will have small, clean cores (axioms) and prioritize programmer convenience over machine efficiency, as hardware will continue to grow faster, making cycle-wasting acceptable for the sake of simplicity and flexibility.

## Key Ideas

- Programming languages evolve along trees; staying on the main branches is a heuristic for choosing good languages.
- A language's long-term survival depends on having a small, clean set of fundamental axioms.
- As hardware becomes faster, the 'cost' of machine cycles decreases, making programmer time the primary bottleneck.
- Future languages should separate program semantics from implementation details, allowing for 'good waste' of cycles to gain simplicity.
- The best way to design a language is to aim for the 'hundred-year language'—a language so well-designed it would be useful even today.
- Language design is increasingly driven by application programmers and open-source communities rather than academic research.

## Entities

- [[entities/paul-graham|Paul Graham]] (person): Programmer, venture capitalist, and essayist.
- [[entities/java|Java]] (language): A popular object-oriented programming language.
- [[entities/cobol|Cobol]] (language): An early high-level programming language.
- [[entities/lisp|Lisp]] (language): A family of programming languages with a long history.
- [[entities/arc|Arc]] (language): A Lisp dialect developed by Paul Graham.
- [[entities/john-mccarthy|John McCarthy]] (person): Computer scientist and inventor of Lisp.
- [[entities/pycon|PyCon]] (organization): The annual Python programming language conference.

## Topics

- [[topics/language-evolution|Language Evolution]]: The concept that programming languages follow evolutionary paths similar to biological species.
- [[topics/premature-optimization|Premature Optimization]]: The practice of sacrificing code clarity and flexibility for performance gains that may not be necessary.
- [[topics/bottom-up-programming|Bottom-up Programming]]: Building software in layers, where each layer acts as a language for the one above it.
- [[topics/moore-s-law|Moore's Law]]: The observation that computing power increases exponentially, which Graham argues will make machine efficiency less critical over time.

## Notable Claims

- Java will eventually be an evolutionary dead-end. Evidence: Comparison to Cobol and the assertion that it lacks intellectual descendants.
- The most important factor in a language's survival is the size and cleanliness of its core axioms. Evidence: Analogy to real estate where location is the only unchangeable factor.
- Wasting programmer time is the true inefficiency, not wasting machine time. Evidence: The trend of increasing hardware speed versus the constant cost of human labor.
- Object-oriented programming is a way to write 'spaghetti code' in large organizations. Evidence: Observation of how large teams use it to accrete patches.

## Quotes

> I've found in my long career as a slob that cruft breeds cruft, and I've seen this happen in software as well as under beds and in the corners of rooms.
> Wasting programmer time is the true inefficiency, not wasting machine time.
> The word 'essay' comes from the French verb 'essayer', which means 'to try'. An essay, in the original sense, is something you write to try to figure something out.
> I'm not proposing that all numerical calculations would actually be carried out using lists. I'm proposing that the core language... be defined this way.
