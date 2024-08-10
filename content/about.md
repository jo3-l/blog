---
title: About me
hidemeta: true
---

Hi! I'm Joseph Liu, a computer science student from Canada. Starting Fall 2024, I'll be studying at
the University of Waterloo; before that, I graduated from the IB Diploma program in high school with
45/45 points.

I love to program in my free time, and have built and contributed to various projects over the
years---more on those below. Besides programming, I also enjoy [reading](/reading-log), writing,
playing tennis, and the very occasional anime/manga; my favorite anime this year was Frieren.

## Programming experience and projects

Nowadays, I primarily work with Rust and Go on backend projects; however, I also have experience in
Python, TypeScript, Java, and C++ among other technologies.

I am a [longtime contributor][yag-contributions] to the open-source YAGPDB Discord bot in Go,
focusing on improving its custom templating engine. Notably, I implemented multiple language
features such as loop control flow actions (`break`, `continue`) and error-handling constructs, and
am currently working on improving editor integration via a [language server in
Rust](https://github.com/jo3-l/yag-template-lsp) with tower-lsp. As part of the latter project, I
implemented an [error-tolerant and lossless parser][yag-template-syntax] generating a CST with rowan.

[yag-contributions]: https://github.com/botlabs-gg/yagpdb/commits?author=jo3-l
[yag-template-syntax]: https://github.com/jo3-l/yag-template-lsp/tree/main/crates/yag-template-syntax

A selection of other interesting projects I am involved in:

- [obscenity](https://github.com/jo3-l/obscenity): A robust profanity detection library for Node.js
  written in TypeScript. It implements a extensible transformer-based design and is thoroughly
  unit-tested with Jest. Used by hundreds of open-source projects with 20k+ weekly downloads on npm
  and 500k+ downloads total.
- [vsHacks](https://vshacks.github.io/): In high school, I co-founded vsHacks—a now-annual hackathon
  organized by my programming club in collaboration with other schools across Greater Vancouver. I
  contributed extensively to the hackathon website and helped run workshops during the event, which
  saw 50+ participants from the district and beyond.
- [markpdf](https://github.com/jo3-l/markpdf): A command-line utility to edit PDF bookmarks using a
  convenient indentation-based format, built in Go. To test parts of markpdf, I experimented with a
  snapshot/golden testing strategy and quite liked the result; I hope to use snapshot testing more in
  future projects.
- [liftoff](https://github.com/jo3-l/liftoff): An interpreter for a toy programming language, built
  with Python. Though basic, the language is sufficiently complete to build some [interesting programs](https://github.com/jo3-l/liftoff/blob/main/examples/ccc21j5.rk).

For more, see [my GitHub profile](https://github.com/jo3-l/).[^1]

## Contact

I'd love to get in touch with you! Please email me at `jliu1602 [at] gmail.com` or shoot me a direct
message on Discord (username `jo3_l`.)

[^1]: if you came to this page from GitHub, you're welcome for the quick lesson in recursion :)
