---
title: About Me
hidemeta: true
---

Hi! I'm Joseph Liu, a first-year computer science student at the University of Waterloo. Before
Waterloo, I graduated from the IB Diploma program in the May 2024 session with 45/45 points.

I love to program in my free time, and have built and contributed to various projects over the
years---more on those below. Besides programming, I also enjoy [reading](/reading-log), writing,
playing tennis, and the occasional anime/manga; my favorite anime this year was Frieren.

## Programming experience and projects

Nowadays, I primarily work with Rust and Go on backend projects; however, I also have experience in
Python, TypeScript, Java, and C++ among other technologies.

I am a [longtime contributor][yag-contributions] to the open-source YAGPDB Discord bot in Go,
focusing on improving its custom templating engine. Notably, I implemented multiple language
features such as loop control flow actions (`break`, `continue`) and error-handling constructs, and
am currently working on a [language server in Rust](https://github.com/jo3-l/yag-template-lsp) using
tower-lsp. Some highlights from the latter project include an [error-tolerant and lossless
parser][yag-template-syntax] outputting a CST with rowan and [scope resolution][scope].

[yag-contributions]: https://github.com/botlabs-gg/yagpdb/commits?author=jo3-l
[yag-template-syntax]: https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-syntax
[scope]: https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-analysis/src/scope

Some of my other projects include:

- [obscenity](https://github.com/jo3-l/obscenity): A robust profanity detection library for Node.js
  written in TypeScript. It implements an extensible transformer-based design and is thoroughly
  tested with Vitest and fast-check. Obscenity is used by hundreds of open-source projects, and has
  been downloaded 700k+ times total on npm.
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
- [vsHacks](https://vshacks.github.io/): In high school, I co-founded vsHacks, a now-annual
  hackathon organized by my programming club in collaboration with other high schools across Greater
  Vancouver. I led work on the hackathon website and helped run workshops during the event, which
  saw 50+ participants from the district and beyond.

For a complete list, see [my GitHub repositories](https://github.com/jo3-l/?tab=repositories).[^1]

## Contact

I'm always happy to chat! Please email me at `jliu1602 [at] gmail.com` or send me a direct message
on Discord (username `jo3_l`.)

[^1]: If you came to this page from GitHub, you're welcome for the quick lesson in recursion :)
