---
title: About Me
hidemeta: true
---

Hi! I'm Joseph Liu, a first-year computer science student at the University of Waterloo.

I love to program in my free time, and have built and contributed to various projects over the
years—more on those below. Aside from programming, I also enjoy [reading](/reading-log), writing,
math puzzles, and the occasional anime.

## Programming experience and projects

Nowadays, I primarily work with Rust and Go on backend projects; however, I am comfortable working across the entire stack and have experience in
Python, TypeScript, Swift, Java, and C++ among other technologies.

### Contributions to YAGPDB

Most of my open-source work centers around the [YAGPDB project](https://yagpdb.xyz), a large-scale
distributed Discord bot for which I am an administrator and code contributor. I have written [120+
patches](https://github.com/botlabs-gg/yagpdb/commits?author=jo3-l) for YAGPDB over the years. Highlights include

- implementing multiple language features and security hardening for YAGPDB's custom scripting
  engine;
- collaborating with other contributors to move the documentation off GitBook to Hugo, cutting load
  time for tens of thousands of viewers;
- and migrating multiple legacy plugins away from GORM to SQLBoiler, impacting a couple hundred
million database rows.

The latter change, to the great dismay of myself and the YAGPDB engineering team, unintentionally
took down production for several hours. Ask me about it!

Other than the main YAGPDB project, I have also built a [language server and VS Code extension](https://github.com/jo3-l/yag-template-lsp) for YAGPDB's custom scripting language. As part of this work, I implemented an [error-tolerant and lossless parser](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-syntax) generating a CST with rowan and [scope resolution](https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-analysis/src/scope).

### Other open-source projects

- [obscenity](https://github.com/jo3-l/obscenity): A popular profanity detection library for Node.js
  written in TypeScript. I designed and implemented its extensible transformer-based architecture, and wrote extensive tests with Vitest and fast-check.
  
  Obscenity is used by hundreds of open-source projects and in various corporate applications, and is downloaded 30k+ times weekly on npm.
- [markpdf](https://github.com/jo3-l/markpdf): A command-line utility to edit PDF bookmarks using a
  convenient indentation-based format, built in Go.
- [liftoff](https://github.com/jo3-l/liftoff): An interpreter for a toy programming language, built
  with Python. Though basic, the language is sufficiently complete to build some [interesting programs](https://github.com/jo3-l/liftoff/blob/main/examples/ccc21j5.rk).
- [yagpdb-cc](https://github.com/yagpdb-cc/yagpdb-cc): A community collection of custom commands for
  YAGPDB. I created and continue to maintain this project, having reviewed submissions from 30+
  contributors over the years. I've also built some
  [supporting](https://github.com/jo3-l/yagfuncdata)
  [automation](https://github.com/jo3-l/action-check-yag-tmpl-syntax) which has seen use in other
  YAGPDB-related projects.
- [vsHacks](https://vshacks.github.io/): A now-annual hackathon I founded in high school, organized by my programming club in collaboration with other high schools across Greater
  Vancouver. I led work on the hackathon website and helped run workshops during the event, which
  saw 50+ participants from the district and beyond.

### Professional experience

In Summer 2025, I interned at TD Bank Group as a software developer on the Enterprise Innovation team. I'm casually looking for work for Summer 2026; my resume is available on request.

## Contact

I'm happy to chat! You can reach me through `jliu1602 [at] gmail.com` or via Discord (username `jo3_l`.)
