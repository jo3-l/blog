---
title: Favorites
weight: 1
date: '2024-08-09'
summary: 'A collection of my favorite technical content—pieces that influence the way I think about programming.'
description: 'A collection of my favorite technical content—pieces that influence the way I think about programming.'
hidemeta: true
---

In no particular order. Unfortunately, since I started collecting these several years after I started programming,
the list is rather incomplete.

## Design and Code Style

[The Wrong Abstraction][wrong-abstraction] and [Goodbye, Clean Code][goodbye-clean-code]

- At some point I was obsessed with GOF-style design patterns and elaborate abstractions in general.
  These two posts finally pushed me to understand that design patterns are _tools_, not rules to
  follow, and that sometimes the best abstraction is no abstraction (or a minimal one.)

[Notes on Programming in C][pikestyle]

- Among other interesting notes about data-oriented design, there's the observation that simple
  algorithms and data structures---Pike lists arrays, linked lists, hash tables, and binary trees---
  composed appropriately are sufficient (and lead to the clearest code) for the vast majority of
  programs.

[Names][names]

- Names need not---indeed, should not---be maximally verbose all the time; a short name whose
  meaning can be inferred from context is preferable to a long-winded name since it aids skimming
  and increases information density. Long, descriptive names are occasionally appropriate, but don't
  be dogmatic about it.

  A great analogy from [Isaac Schlueter via HN][issacs-hn]:

  > The first time you meet someone, you learn their full name. When discussing them with someone
  > else who knows them, you use just a single name. If they're standing right there, you don't
  > bother using their name, but just make eye contact, and maybe a "Hey". Should be the same way
  > with variables.

[When to comment that code][ddevault-comments]

[wrong-abstraction]: https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
[goodbye-clean-code]: https://overreacted.io/goodbye-clean-code/
[pikestyle]: http://doc.cat-v.org/bell_labs/pikestyle
[names]: https://research.swtch.com/names
[ddevault-comments]: https://drewdevault.com/2023/03/09/2023-03-09-Comment-or-no-comment.html
[issacs-hn]: https://news.ycombinator.com/item?id=840331

## Performance

[Matt Godbolt "What Has My Compiler Done for Me Lately?"][cppcon-godbolt]

- I used to do competitive programming, and picked up the bad habit of writing things like
  `v >> 1` instead of `v / 2` and `memset(dp, 0x3f, sizeof(dp))` instead of
  `std::fill(std::begin(dp), std::end(dp), 0x3f3f3f3f)` in the belief that the former was more performant.
  This talk convinced me that this belief was totally unfounded and shows just how smart modern compilers
  can be---the two optimizations above are, in fact, relatively simple for compilers to do!

  Of course, compilers are not magic: programmers must still take care to choose appropriate data
  structures and algorithms. Finer optimizations are sometimes necessary, but warrant more careful
  profiling and benchmarking.

[Why is processing a sorted array faster than processing an unsorted array?][so-branch-predictor] and
[Bjarne Stroustrup: Why you should avoid Linked Lists][stroustrup-linked-lists]

- Processor-level performance considerations---branch prediction and memory locality respectively.

[Undefined Behavior can result in time travel][ub-time-travel]

- How undefined behavior enables optimizations, which can sometimes manifest as undesirable and
  bizarre changes.

[cppcon-godbolt]: https://www.youtube.com/watch?v=bSkpMdDe4g4
[so-branch-predictor]: https://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-processing-an-unsorted-array
[stroustrup-linked-lists]: https://www.youtube.com/watch?v=YQs6IC-vgmo
[ub-time-travel]: https://devblogs.microsoft.com/oldnewthing/20140627-00/?p=633

## Other

[My Kind of REPL][inline-snapshot-tests]

- Inline snapshot tests---one of my favorite testing strategies.

[Go Testing By Example][go-tests] and [How to Test][how-to-test]

[Strings, bytes, runes and characters in Go][go-strings]

- Bytes ≠ code points ≠ characters.

[Parse, don't validate][parse-dont-validate]

- Judiciously encoding constraints on data using the type system.

[Using unwrap() in Rust is Okay][unwrap]

- Most languages that promote "errors as values" also provide a way to raise fatal errors (called
  panics in Rust and Go); this post addresses the question of when, if ever, is it OK to panic over
  returning an error.

[Accurate mental model for Rust's reference types][rust-references]

- A `&mut T` is most accurately described as an exclusive reference and likewise `&T` is a shared
  reference. Crucially, `&T` is _not necessarily_ an immutable `T`, as demonstrated by interior
  mutability and atomic values.

[inline-snapshot-tests]: https://ianthehenry.com/posts/my-kind-of-repl/
[go-tests]: https://research.swtch.com/testing
[how-to-test]: https://matklad.github.io/2021/05/31/how-to-test.html
[go-strings]: https://go.dev/blog/strings
[parse-dont-validate]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[unwrap]: https://blog.burntsushi.net/unwrap/
[rust-references]: https://docs.rs/dtolnay/0.0.9/dtolnay/macro._02__reference_types.html
