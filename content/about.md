---
title: About Me
hidemeta: true
---

Hi! I'm Joseph Liu, a third-year undergraduate student at the University of Waterloo double majoring
in computer science and pure mathematics.

I love to program in my free time, and have built and contributed to various open-source projects over the
years. Aside from programming, I also enjoy blogging, math puzzles, and anime. On occasion
I play tennis and hike. [Here's some places I've visited.](/travel)

## Professional experience

My [resume](/resume.pdf) is available.

- In Winter 2027, I'll be interning at River Markets, a startup developing trading infrastructure for prediction markets.
- In Summer 2026, I interned at Bloomberg L.P. on the compliance engineering team, where I designed and built a distributed concurrency limiter for a high-volume Airflow data pipeline.
- In Summer 2025, I interned at TD Bank on the enterprise innovation team, where I prototyped open banking integrations using Plaid.

## Open-source work

My most popular open-source projects are YAGPDB, a Discord bot written in Go which I made significant contributions to; and Obscenity, a profanity detection library for Node.js which I originally designed and built in 2021. I also maintain a bunch of less noteworthy projects.

### YAGPDB: a distributed Discord bot

[YAGPDB](https://yagpdb.xyz) is a large-scale bot for the Discord messaging platform. It's used in ~3.5 million Discord communities and is a surprisingly complex piece of software. I am the top external code contributor with ~130 merged PRs to date---though I'm less active these days---and remain a community administrator.

My main interest is the bot's dynamic scripting runtime: YAGPDB allows users to write custom programs in a funky DSL which run on the bot's environment. I implemented various new language features, such as `break/continue` in loops, returning from procedures, and exception handling via `try/catch`, which are now widely used.

Some other noteworthy contributions include

- collaborating with other contributors to migrate the documentation webiste from GitBook to Hugo, cutting load time for thousands of viewers and enabling support for custom syntax highlighting,
- migrating database access code handling hundreds of millions of records in legacy plugins from GORM to SQLBoiler, improving performance and type safety.

Besides the main YAGPDB project, I am also the primary developer of a [**language server and VS Code extension**](https://github.com/jo3-l/yag-template-lsp) for YAGPDB's scripting language, which provides key IDE features such as autocompletion, error diagnostics, refactoring tools, etc. From a technical standpoint the project comprises a Rust server component and a TypeScript VS Code extension communicating over LSP. As part of the server component, I implemented an [error-tolerant and lossless parser](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-syntax) generating a concrete syntax tree, a [symbol resolution algorithm](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-analysis/src/scope), and a [Wadler-style pretty printer](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-format).

### Obscenity: a profanity detection library

[Obscenity](https://www.npmjs.com/package/obscenity) is a robust, extensible profanity detection library, written in TypeScript. These days it is the most widely used library for this purpose in the JavaScript backend ecosystem, with 300k+ downloads weekly. It's used in 600+ open-source projects, including UK government websites, Minecraft developer tools, forum software, streaming websites, and a whole lot of online multiplayer games.

The problem is surprisingly tricker than it seems: there are many ways for a user to obsfucate a phrase to bypass a naive keyword searching algorithm. For instance, if we wish to block the word `apple`, a clever user can instead write `аpple`, where the `a` has been replaced by the Cryllic lookalike character `а`. (Try this in your browser console: `"a" === "а"`). My profanity detection library runs a highly configurable normalization step prior to matching to catch such cases and has various other intriguing bells and whistles.

### Other projects

- [**markpdf**](https://github.com/jo3-l/markpdf), a command-line utility to edit PDF bookmarks using a
  convenient indentation-based format, written in Go. Some academics seem to enjoy using it.
- [**vsHacks**](https://vshacks.github.io/), a hackathon in Vancouver that I co-founded in high school.
- [**turnstile**](https://github.com/jo3-l/turnstile), a Typst package for typesetting Fitch-style [natural deduction](https://en.wikipedia.org/wiki/Natural_deduction) proofs with a really nice syntax (ab)using Typst term-lists.
- [**liftoff**](https://github.com/jo3-l/liftoff), an interpreter for a toy programming language in Python.
- [**wwlocal**](https://github.com/jo3-l/wwlocal), a fast local viewer for the WaterlooWorks job board. Totally vibecoded, but very convenient to use and in my opinion the interface is very intuitive.
- **assorted solutions to programming puzzles**, for instance [Advent of Code solutions](https://github.com/jo3-l/wwlocal) (I ranked in the top ~150 fastest participants each year, back when the global leaderboard still existed) and [solutions to various programming olympiad problems](https://github.com/jo3-l/cp-practice).

## Contact

I'm happy to chat! You can reach me at jliu1602 [at] gmail.com or via Discord (username jo3_l).
