---
title: Property-Based Testing is Magical
date: '2024-08-11'
summary: 'An exploration of property-based testing—a powerful technique for building robust test suites with minimal tedium.'
description: 'An exploration of property-based testing—a powerful technique for building robust test suites with minimal tedium.'
tags: [programming, testing]
---

When I began programming, writing tests felt like a chore, a checklist item to cross off on the
elusive path to High Quality Code. However, in the years since---having spent some time contributing
to (read: occasionally breaking) a legacy codebase and building more complex projects---I've come to
appreciate testing for what it can be when done well: a tool that enables refactoring with
confidence.

That said, writing good tests requires some skill and experience. There are various techniques that I find to
generally elevate test quality: I'm a big fan of both [table-driven
testing](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests), which reduces the friction
of adding new cases; and snapshot testing, which makes updating expected outputs easy.

But neither table-driven testing nor snapshot testing is the focus of this blog post. Rather, I want
to explore another technique, _property-based testing_, that felt almost like magic the first time I
encountered it. Here's the pitch for property-based testing:

> **The pitch.** With some setup, property-based testing can automatically hunt for edge cases for
> you; a good property-based testing framework will even reduce (or _shrink_) failing test cases so
> that they are easy to debug.

That sounds too good to be true, and in some sense it is. Property-based tests are not always
applicable, can be difficult to write, and are not a replacement for normal example-based tests. But
when they are appropriate, they're _awesome_.

In this post, then, I'll attempt to explain what property-based testing is both in abstract and in
concrete, using a real example I wrote recently.

## What is property-based testing?

At its core, a property-based test continually generates random inputs and checks for certain
properties in the output. For instance, if we are optimizing an algorithm, we might want to ensure
that the previous and new implementation agree, in which case the relevant property is
`old(input) == new(input)`. If we are writing a parser for untrusted input, we might instead verify
that no inputs crash the process, yielding the property `doesNotCrash(parse(input))`.[^1]

Good property-based testing frameworks will abstract away the loop and provide helpers for
intelligently generating many types of input data, in addition to automatically shrinking failing
test cases.

[^1]:
    Those familiar with the concept of fuzz tests may see a similarity to property-based tests.
    The line separating the two is murky at best (and one could make a good argument for the two being
    one and the same); see [this post by
    Kaminski](https://www.tedinski.com/2018/12/11/fuzzing-and-property-testing.html) for more.

### The cliché sorting example

A classic application of property-based testing is sorting algorithms. Suppose we have implemented
the procedure `sort(nums: number[]): number[]`. An obvious property to check is that the output
should be in order by comparing consecutive elements: that is, for all `nums: number[]`, the
property `isSorted(sort(nums))` should hold.

The following example does just this with the aid of the [`fast-check`](https://fast-check.dev/)
property testing framework for TypeScript. We specify the input as any `number[]` via
`fc.array(fc.integer())`, and then `fast-check` does all the hard work of generating interesting
inputs, running the test, and shrinking failures.

(A complete test suite would no doubt need to test various other properties: the sorted array should
contain the same elements as the input array disregarding order, have the same length, and so on.
Testing for any mismatch with a simpler sort algorithm or a library implementation would also be
useful: `expect(ourSort(nums)).toStrictEqual(builtinSort(nums))` or similar.)

```ts
import { test, fc } from '@fast-check/vitest';
import { expect } from 'vitest';

declare function sort(nums: number[]): number[];

function isSorted(nums: number[]) {
	return nums.every((x, i) => i === 0 || nums[i - 1] <= x);
}

test.prop([fc.array(fc.integer())], (nums) => {
	expect(isSorted(sort(nums))).toBe(true);
});
```

In contrast, consider what an example-based test suite for a sorting procedure would entail: we
would need to manually select input arrays, making sure to vary the order and number of elements for
good coverage, and then also write out the correct output arrays. An example-based test verifies
that the system behaves correctly given some input, whereas a property-based test asserts something
about a _whole class_ of inputs. The property-based test above doesn't obviate the need for
example-based tests, but the main point is that the property-based test is easy and useful.

Of course, not all property-based tests are so straightforward to design; in fact, sorting
algorithms are near-optimal candidates for property-based tests, given their simple input and range
of interesting properties. Most scenarios suffer on both counts: inputs are more complex and useful
properties more difficult to coax out.

In the next section, therefore, we will discuss a real property-based test I wrote as part of the
[Obscenity project](https;//github.com/jo3-l/obscenity), a profanity detection library for Node.js.

## Testing a parser for a DSL

Obscenity provides a pattern DSL for specifying profane words---think regular expressions but much
less powerful. Other than literal text, patterns support optional expressions (enclosed in `[]`, so
`b[a]` matches `b` or `ba`), wildcards (`?`), and word boundary assertions at the start or end of
the pattern (`|`). A BNF-style grammar for Obscenity patterns is:

```bnf
Pattern ::= WordBoundary? Atom* WordBoundary?

Atom         ::= Literal | Wildcard | Optional
Literal      ::= (basic_char | '\' escape_char)+
Wildcard     ::= '?'
Optional     ::= '[' (Literal | Wildcard)+ ']'
WordBoundary ::= '|'

basic_char  ::= character excluding '\', '?', '[', ']', and '|'
esacpe_char ::= any of '\', '?', '[', ']', '|'
```

At first glance, a parser for this grammar, `parse(pattern) -> ParsedPattern`, does not seem to
admit any obvious properties. While we could test that the parser never deadlocks on any
input---which would actually be a useful property test to write, given that the parser accepts
untrusted input---with some thought we can devise a more useful property.

Specifically, by writing a function `stringify(ParsedPattern)` that takes the parser's output and
reconstructs the corresponding pattern and composing this with the `parse` function, we get the
property `stringify(parse(pattern)) == pattern`: that is, the parser should roundtrip. This
property, while more complicated to check, is far more interesting---in some sense, it checks
whether the parser's _interpretation_ of a pattern (as reported by `stringify(parse(pattern))`) is
correct (matches the original `pattern`.) For instance, if we somehow forget to implement parsing
for wildcards and treat `?` characters literally, `stringify(parse('?'))` would yield `\?`, which does not
agree with the original input `?`.

To write this property test, we need to be able to generate arbitrary strings that are valid
patterns.[^2] [^3] It's straightforward to do so by following the grammar: first, we create generators
(`fast-check` calls these _arbitraries_) for each component of a pattern: literals, wildcards, and
optionals.

[^2]:
    While we could in theory just feed random strings into the parser, this would be rather
    ineffective; very few random strings are interesting patterns. An optional expression, for
    instance, needs to start with a `[` and end with a `]`, and such structure is unlikely to
    manifest in a random string.

[^3]:
    This general technique---using a grammar to generate valid and complex inputs---is aptly
    known as _grammar testing_, and there is a fair bit of literature on this topic.

```ts
const literalArb = fc.stringOf(
	fc.oneof(fc.char(), fc.char16bits()).map(escapeIfNeeded),
	{
		minLength: 1,
	},
);
const wildcardArb = fc.constant('?');
const optionalArb = fc
	.array(fc.oneof(literalArb, wildcardArb), { minLength: 1 })
	.map((children) => '[' + children.join('') + ']');
```

Combining these arbitraries yields a complete pattern.

```ts
const patternArb = fc
	.tuple(
		fc.boolean(),
		fc.stringOf(fc.oneof(literalArb, wildcardArb, optionalArb)),
		fc.boolean(),
	)
	.map(([hasStartWB, inner, hasEndWB]) => {
		return (hasStartWB ? '|' : '') + inner + (hasEndWB ? '|' : '');
	});
```

...and finally we can write the property test.

```ts
test.prop([patternArb])('parser roundtrips valid patterns', (pattern) => {
	const parsed = new Parser().parse(pattern);
	expect(stringify(parsed)).toBe(pattern);
});
```

Running this test immediately found two bugs, both valid. Let's talk about them one by one.

### Bug 1: Parser misinterprets `[\?]`

```txt {hl_lines=[3,5]}
Error: Property failed after 4 tests
{ seed: -391669338, path: "3:0:1:0:1:1", endOnFailure: true }
Counterexample: ["[\\?]"]
Shrunk 5 time(s)
Got AssertionError: expected '[\??]' to be '[\?]' // Object.is equality
    ...stack trace elided...
Encountered failures were:
- ["|[v?㶨X㾺0O⍙ᓰ]?[\\|좲樿ꎻ秸\\?]"]
- ["[v?㶨X㾺0O⍙ᓰ]?[\\|좲樿ꎻ秸\\?]"]
- ["?[\\|좲樿ꎻ秸\\?]"]
- ["[\\|좲樿ꎻ秸\\?]"]
- ["[樿ꎻ秸\\?]"]
- ["[\\?]"]
```

The pattern `[\?]` is valid according to the grammar: it should parse as an optional literal
question mark `?`. But the error is saying that the parser interpreted this pattern as an optional
literal question mark `?` followed by a wildcard---there should not be a wildcard!

The rather silly mistake was that the parser was not consuming the character after the escape
character `\`.

```ts {hl_lines=2}
if (c === '\\') {
	const escaped = this.peek(); // should be `this.eat()`
	if (!escaped) this.error("expected character after '\\'");
	// ...
}
```

Although this error would certainly be caught by a normal example-based test, the property-based
test _found the edge case for us instantly_ with a nice, near-minimal reproduction. Note that the
fast-check framework shrunk the failing input from `|[v?㶨X㾺0O⍙ᓰ]?[\|좲樿ꎻ秸\?]` all the way to
`[\?]`---a great example of what I mean when I say property testing feels almost like magic.

The second bug is more insidious.

### Bug 2: Parser errors on `\|`

```txt {hl_lines=[3,5]}
Error: Property failed after 724 tests
{ seed: 589454055, path: "723:0:1:0:1", endOnFailure: true }
Counterexample: ["\\|"]
Shrunk 4 time(s)
Got PatternSyntaxError: Invalid pattern '\|': expected character after '\'
    ...stack trace elided...
Encountered failures were:
- ["|?[??)떲tE회tૼ1뮉傗e&⨀I띿=@u??*6\"\\]O௯>!l畭]t还E_瞗픏\\|"]
- ["?[??)떲tE회tૼ1뮉傗e&⨀I띿=@u??*6\"\\]O௯>!l畭]t还E_瞗픏\\|"]
- ["[??)떲tE회tૼ1뮉傗e&⨀I띿=@u??*6\"\\]O௯>!l畭]t还E_瞗픏\\|"]
- ["t还E_瞗픏\\|"]
- ["\\|"]
```

The error is (extremely!) confusing and I didn't know what to make of it at first: there is clearly
a character after the `\`. To add to the confusion, this error only occurs when `\|` is at the end
of the pattern; a `\|` in the middle parses correctly.

However, I soon realized the issue: originally, I implemented boundary assertions by unconditionally
removing any leading or trailing `|` before parsing occurs, given that boundary assertions are only
legal at the start or end of patterns. Yet this implementation is broken: not all `|` at the ends of
patterns are boundary assertions; they can be escaped, as is the case here. The fix is to parse `|`
normally and issue an error when the `|` is not positioned at the start or end of the pattern.

To me, this second example epitomizes the power of property-based testing: **while example-based
testing only covers cases we can think of, property-based testing uncovers scenarios that we may
never have considered.** While I'm still planning to write an example-based test suite for the
parser---again, property tests complement, not replace other testing strategies---with this property
test I have much more confidence in the parser's correctness and in future changes.

## Concluding thoughts

Property-based tests are extremely powerful, yet criminally underused. Yes, they aren't always
applicable, and yes, it can take some effort to find useful properties---but in my experience they are
well worth the time spent. Give them a try in your next project and let me know what you think! :)
