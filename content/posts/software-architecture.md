---
title: Low coupling and high cohesion
date: '2026-09-10'
summary: In this era of software engineering with LLMs, I argue that these principles are doubly important
tags: [programming, llms]
draft: true
---

recently, I've been spending a lot of time trying to determine which principles of software architecture I care
about most

- low coupling
  - different subsystems should be as independent as possible
  - think about dependency graph of your subsystems. nodes that are at the center of the graph (lots of dependencies)
    ought to have extra human attention, review, and care put into them. a poor design or interface infects other code
  - enable one to reason about one subsystem at a time without worrying about its implications for others
- high cohesion
  - keep related functionality and components together. locality of behavior
  - vertical slice architecture/feature-based design
  - when a change needs to be made, ensure that it's easy to reason about the locations in the code that need to be changed
  - vibecoded projects: find myself hesistant to make changes myself because files are spread all over the place;
    to execute a single conceptual change requires finding and touching many files

to attempt to summarize these two as one, together they minimize the amount of context that one needs to make changes confidently.
minimize the blast radius of a mistake
