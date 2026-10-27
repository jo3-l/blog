---
title: About Me
hidemeta: true
---

Hi! I'm Joseph Liu, a third-year undergraduate student at the University of Waterloo double majoring
in computer science and pure mathematics.

I love to program in my free time, and have built and contributed to various open-source projects over the
years. Aside from programming, I also enjoy blogging, math puzzles, and the occasional anime. On occasion
I play tennis and hike. [Here's some places I've been.](/travel)

## Open-source work

My main open-source projects are YAGPDB, a large-scale Discord bot which I made significant contributions to (130+ merged PRs over the years); and Obscenity, a popular profanity detection library for Node.js, which I designed and built at 14.

### YAGPDB: distributed Discord bot

[YAGPDB](https://yagpdb.xyz) is a large-scale bot for the Discord chat platform, written in Go. It's used in ~3.5 million Discord communities and is distributed over ~30 different nodes. I was a very active code contributor in high school and remain an administrator for the bot.

My main interest is the bot's dynamic scripting runtime: YAGPDB allows users to write custom programs in a funky DSL, and have them run in the bot's environment. I implemented various new language features, such as `break/continue` in loops, returning from procedures, and exception handling via `try/catch`, which are now widely used.

Some other work includes

- contributing dozens of new features and bug fixes, working full-stack,
- collaborating with other contributors to migrate the documentation webiste from GitBook to Hugo, cutting load time for thousands of viewers and enabling support for custom syntax highlighting,
- migrating database access code handling hundreds of millions of records in legacy plugins from GORM to SQLBoiler, improving performance and type safety.

---

Other than the main YAGPDB project, I also developed a [**language server and VS Code extension**](https://github.com/jo3-l/yag-template-lsp) for YAGPDB's scripting language, which provides key IDE features such as autocompletion, syntax highlighting, error diagnostics, refactoring tools, etc. From a technical standpoint the project comprises a Rust server component and a TypeScript VS Code extension communicating over LSP. As part of the server component, I implemented an [error-tolerant and lossless parser](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-syntax) generating a CST with rowan, a [symbol resolution algorithm](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-analysis/src/scope), and a [Wadler-style pretty printer](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-format).

### Obscenity: profanity detection library

One day in 2021 I decided to build a robust profanity detection library, as one does. These days it is the most widely used library for this purpose in the JavaScript backend ecosystem, with [300k+ downloads weekly](https://www.npmjs.com/package/obscenity). It's used in 600+ open-source projects, including UK government websites, Minecraft developer tools, forum software, streaming websites, and a whole lot of online multiplayer games.

The problem is surprisingly tricker that it seems: there are many ways for a user to obsfucate a phrase to bypass a naive keyword searching algorithm. For instance, if we wish to block the word `apple`, a clever user can instead write `аpple`, where the `a` has been replaced by the Cryllic lookalike character `а`. (Try this in your browser console: `"a" === "а"`). My profanity detection library runs a highly configurable normalization step prior to matching to catch such cases and has various other intriguing bells and whistles.

### Other open-source projects

- [**markpdf**](https://github.com/jo3-l/markpdf), a command-line utility to edit PDF bookmarks using a
  convenient indentation-based format, written in Go. Some academics seem to enjoy using it.
- [**vsHacks**](https://vshacks.github.io/), a hackathon in Vancouver that I co-founded in high school.
- [**turnstile**](https://github.com/jo3-l/turnstile), a Typst package for typesetting Fitch-style [natural deduction](https://en.wikipedia.org/wiki/Natural_deduction) proofs with a really nice syntax (ab)using Typst term-lists.
- [**liftoff**](https://github.com/jo3-l/liftoff), an interpreter for a toy programming language in Python.
- [**wwlocal**](https://github.com/jo3-l/wwlocal), a fast local viewer for the WaterlooWorks job board. Totally vibecoded, but very convenient to use and in my opinion the interface is very intuitive.
- **assorted solutions to programming puzzles**, see for instance [my Advent of Code solutions](https://github.com/jo3-l/wwlocal) (I consistently ranked in the top ~150 fastest participants each year, back when the global leaderboard still existed) and [my solutions to various programming olympiad problems](https://github.com/jo3-l/cp-practice).

## Professional experience

I've had the pleasure of working a variety of different internships as a co-op student at Waterloo.

- In Winter 2027, I'll be interning at
- In Summer 2026, I interned at Bloomberg L.P. in the compliance engineering team, where I built a distributed concurrency limiter for a high-volume Airflow data pipeline.
- In Summer 2025, I interned at TD Bank in the enterprise innovation team, where I prototyped an open banking integration using Plaid.

## Contact

I'm happy to chat! You can reach me at jliu1602 [at] gmail.com or via Discord (username jo3_l).
