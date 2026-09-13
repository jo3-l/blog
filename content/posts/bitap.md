---
title: 'Bitap: my favorite string matching algorithm'
date: '2026-09-07'
tags: [programming, algorithms]
summary: An exposition of the bitap or shift-and exact string matching algorithm
---

A classic problem is to find the first occurrence of a pattern $P$ in a string $T$. There are various classic algorithms to solve this problem efficiently, such as [Boyer-Moore](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm), [Knuth-Morris-Pratt](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm), and [Two-Way](https://en.wikipedia.org/wiki/Two-way_string-matching_algorithm). In this post I want to provide an exposition of a less well-known algorithm, the _bitap_ or _shift-and_ algorithm[^1], that runs efficiently when the pattern $P$ is relatively short (of length less than the width of a machine word). Despite its constraints, I like it a lot because it is simple both to understand and to implement, relatively efficient for short strings, and uses bit operations in a particularly elegant fashion.

[^1]: I should note that I'm referring to the _exact_ string-matching algorithm here. "bitap algorithm" can also mean a variant that supports fuzzy matching in terms of Levenshtein distance, which is cool but not the subject of this post.

To show that the algorithm is as simple conceptually as claimed, let me try to derive it incrementally starting from the most naive string matching algorithm.

## Deriving bitap

### The naive algorithm

The simplest brute-force algorithm to solve the string matching problem just tries to match the pattern $P$ starting from each possible position in the string $T$.

```go
// Returns the first index i such that T[i:] starts with the pattern P,
// or -1 if no such index occurs.
//
// The pattern P is required to be nonempty.
func match(T, P string) int {
outer:
	// starting from each position i = 0, ... in the string T...
	for i := range len(T) - len(P) + 1 {
		// try to match the pattern P, one character at a time...
		for j := range len(P) {
			// moving onto the next start position if a mismatch occurs.
			if T[i+j] != P[j] {
				continue outer
			}
		}
		return i
	}
	return -1
}
```

### The naive algorithm, but make it streaming

Let's now impose an additional constraint to motivate us to change the algorithm a little: instead of being given all the characters of the text $T$ at once, suppose that they are now provided in the form of a _stream_, one character at a time. (Perhaps $T$ is very long and we do not wish to load all its contents into memory at once.)

The simple algorithm presented above is not streaming: it needs to read up to $m = \texttt{len}(P)$ characters ahead starting from the current position in $T$ to detect a match of the pattern. How can we adapt it so that it only performs one pass through the data?

After a bit of thought, one comes up with the following variant of the brute-force algorithm. Instead of immediately trying to detect an occurrence of $P$ by reading ahead in the text $T$ starting from each start position $i = 0, \dots$, we can instead maintain a set of _in-progress matches_ as we scan through the text $T$. Conceptually, an in-progress match consists of the prefix of the pattern $P$ that has already been matched just before the current position, along with the remaining suffix that has not been matched yet. When we read a new character $c$ in $T$, we advance the in-progress matches that are expecting the character $c$, and kill the rest. If any of the active matches progress to the end of the pattern $P$, we are done.

```go
func matchOnepass(T, P string) int {
	type state struct {
		remaining string // suffix of P yet to be matched
	}
	var active []state
	for i := range len(T) {
		c := T[i]

		// Always attempt to start a new match.
		active = append(active, state{remaining: P})
		var next []state
		for _, m := range active {
			if c == m.remaining[0] {
				// Advance this in-progress match by one position.
				remaining := m.remaining[1:]
				if remaining == "" {
					// Matched all of P, with the final character appearing at position i.
					// The first character appears |P| - 1 units to the left.
					return i - len(P) + 1
				}
				next = append(next, state{remaining})
			}
		}
		active = next
	}
	return -1
}
```

We can optimize `matchOnepass` a little by representing an in-progress match state by the index $j$ of the next character to match in the pattern $P$. (The suffix of $P$ yet to be matched then corresponds to `P[j:]`.) This simplifcation yields

```go
func matchOnepassInt(T, P string) int {
	var active []int // state is now an int
	for i := range len(T) {
		c := T[i]

		active = append(active, 0) // attempt to start a new match
		var next []int
		for _, j := range active {
			if c == P[j] {
				// advance
				j++
				if j == len(P) {
					// matched all of P
					return i - len(P) + 1
				}
				next = append(next, j)
			}
		}
		active = next
	}
	return -1
}
```

How can we improve this algorithm further? One observation we can make is that the in-progress states in `active` are now always integers between `0` and `len(P)`, the length of the pattern. If $P$ is not too long, there may be a more efficient way to represent the `active` set instead of a list of integers. This idea is what leads us to our next modification, using _bitsets_ and bit manipulation, from which the bitap algorithm arises.

### Bit manipulation

Indeed, if $P$ is relatively short, say `len(P) < 64`, then we can pack the set of active states into a single integer (understood as a 64-bit bitset). So, for instance, if `active = {1, 2, 7}`, then

```
active_bitset = 0b1000_0110
```

Let's try this!

```go
func matchOnepassBitset(T, P string) int {
	var active uint64 // bitset
	for i := range len(T) {
		c := T[i]

		active |= 1 << 0 // add 0 to the bitset (attempt to start a new match)
		var next uint64
		for j := range 64 {
			if active&(1<<j) == 0 {
				continue
			}
			// for each state j in the active set...

			if c == P[j] {
				// advance
				j++
				if j == len(P) {
					// matched all of P
					return i - len(P) + 1
				}
				next |= 1 << j
			}
		}
		active = next
	}
	return -1
}
```

Hm. That doesn't seem like a major improvement. Although it is nice that `active` has a more compact encoding, there are still two nested loops, begging the question to whether we can eliminate the inner loop somehow...

It turns out that we indeed can, using some clever bit manipulation and a small change in perspective. Observe that, in the above algorithm, we look at each match state, checking if it can continue (by comparing `c` with `P[j]`), and then advance by one position if so. On the other hand, an alternative approach is to unconditionally advance _all_ match states by one position, and then kill any states that arose from an invalid transition. The key is that, unlike the previous approach, both of these steps can be implemented in a single bit operation operating on the entire bitset at once.

Indeed, to advance all match states by one position, it suffices to shift left by one: `active << 1`. The only challenge that remains is to kill off states arising from an invalid transition: in other words, given `next = active << 1`, we want to only keep the states that should really have advanced after observing the character `c`. The second and final insight is that we can accomplish this by precomputing a bitset of valid states that can arise after observing the character `c` for each character that appears in the pattern, and then intersecting with the appropriate bitset.

```go
func matchBitap(T, P string) int {
	var validMask [256]uint64 // table of bitmasks, indexed by byte
	for j := range len(P) {
		// If we see c, then we are permitted to advance to state j+1
		// (assuming we were at state j before).
		c := P[j]
		validMask[c] |= 1 << (j + 1)
	}

	var active uint64
	for i := range len(T) {
		c := T[i]

		active |= 1 << 0 // attempt to start a new match
		next := (active << 1) & validMask[c] // advance states and mask off invalid transitions
		if next&(1<<len(P)) != 0 {
			// Matched all of P!
			return i - len(P) + 1
		}
		active = next
	}
	return -1
}
```

At last, we have arrived at the the _shift-and_ or _bitap_ algorithm (named since it shifts `<< 1`, then ands `& validMask[c]`)!

I remark that the typical presentation has a slightly different index convention shifted by one, which is more appropriate in practice, but the spirit is the same and my convention allows for this blog to flow a bit more naturally. There is also a more efficient variant _shift-or_ that inverts all the bit masks and uses bit-OR instead of bit-AND, which performs one less bit operation per input character.

## So what?

As mentioned at the start, the bitap algorithm only really shines when the pattern is relatively short: though it can theoretically be generalized to longer patterns (by using multi-word bitsets), the performance gains start diminishing. Moreover, asymptotically, when the length of the pattern is bounded by a constant, the runtime of bitap is identical to that of the naive brute-force algorithm (both are linear in the length of the text $T$). And practically, it may even perform worse than the naive algorithm in a one-off test due to the precomputation required.

In view of these limitations, why do I like bitap at all? I think that it is conceptually very elegant and simple to derive from the naive algorithm--as described above, it simply maintains a set of active states as it steps through the input string, using bit operations to go fast. Though I've also studied Boyer-Moore and KMP in detail, it takes me quite some time to derive them from scratch[^2], whereas bitap is very easily derived, since to me it is just the naive algorithm dressed up differently. It is my hope that you feel the same way after this blog post.

[^2]: and I can only wish that I could derive Two-Way from scratch. I don't even understand how it works.
