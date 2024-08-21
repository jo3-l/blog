---
title: Error-Resilient Parsing and CSTs with Rowan
date: '2024-08-21'
summary: 'Building parsers tolerant of syntax errors and representing lossless syntax trees with Rowan crate.'
description: 'Building parsers tolerant of syntax errors and representing lossless syntax trees with the Rowan crate.'
tags: [programming, parsing]
draft: true
---

Traditional compilers can get away with exiting immediately when faced with erroneous input---it
makes little sense to try to run programs with syntax errors. However, the situation is markedly
different for language servers, linters, and other static analysis tools intended to be used in the
editor.

Indeed, in the process of editing code, the program is more often syntactically invalid than not.
Consider the following incomplete Rust program, where we are adding a new function called `greet`.

```rust
fn main() {
	let name = "joe";
}

fn greet(user: | )
               ^ cursor here

struct User {
	name: String,
	age: usize,
}
```

This program is evidently syntactically invalid: the type of the parameter `name` is missing, as is
the whole body of the `greet` function. Yet we have largely come to expect language servers---the
things that power autocomplete and other features in editors---to gracefully handle these cases. For
instance, at the cursor, we would like to see completions for types such as `User`.

Stop and think for a moment about what this requires the language server to do under the hood. To
provide the completion for `User`, it must recover from the syntax errors in the incomplete
declaration `greet`, parse the `User` struct declaration as normal, and produce a partial syntax
tree for further analysis; we say that the parser in this case needs to be _error-resilient_ or _error-tolerant_.

But how are error-resilient parsers implemented, and what differentiates them from more typical
parsers that exit immediately upon encountering invalid input? How are partial syntax trees
represented? These fascinating questions are ones I first became acquainted with while writing a
[language sever of my own](https://github.com/jo3-l/yag-template-lsp) this summer, and in this post
I'll attempt to share what I've learnt about the topic. All the code examples in this post will be
in Rust and use the [Rowan](https://github.com/rust-analyzer/rowan) syntax tree crate[^1], but the
concepts discussed should generalize well to other implementations.

[^1]: Rowan powers `rust-analyzer` and most other LSPs written in Rust.
