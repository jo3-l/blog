---
title: Optimizations in Go's strings.Repeat implementation
date: "2025-08-01"
summary: In the strings package of Go's standard library lies an innocuous-looking function, strings.Repeat(s, count). The standard library implementation winds up being more complicated than one might anticipate!
description: In the strings package of Go's standard library lies an innocuous-looking function, strings.Repeat(s, count). The standard library implementation winds up being more complicated than one might anticipate!
tags: [go, performance]
katex: true
draft: true
---

The `strings` package of Go's standard library provides a procedure `strings.Repeat(s string, count int) string` that repeats the input
string a given number of times. It behaves as expected; for example, `strings.Repeat("a", 3) == "aaa"`.

At first glance, one might expect the implementation to be totally straightforward. Yet, as of Go 1.25, the real implementation of `strings.Repeat` clocks in at a hefty [93 lines](https://github.com/golang/go/blob/e73dadc758d30a11146e32cc1d0baafa255641a6/src/strings/strings.go#L591-L684)[^1]! **Where does the unexpected complexity come from?**

The answer: several interesting optimizations and edge cases befitting of a standard library implementation.

---

In this post, we'll build up to the current implementation of `strings.Repeat` piece-by-piece, adding optimization after optimization to the naive implementation until we converge on the real one. In particular, my goal is to not only _present_ the optimizations added to `strings.Repeat` but also attempt to motivate them as best as possible---how would one discover these issues in practice? Of course, I have the benefit of hindsight and am far from a performance expert myself, but hopefully you'll still enjoy the post regardless :)

**Table of Contents**

- [A horrendously naive implementation (1)](#1-a-horrendously-naive-implementation)
- [A less naive implementation: preallocating a buffer (2)](#2-a-less-naive-implementation-preallocating-a-buffer)
- [An acceptably naive, idiomatic implementation (3)](#3-an-acceptably-naive-idiomatic-implementation)
- [Interlude](#interlude) <-- jump here to start from the more interesting additions
- [Going faster by doing less (4)](#4-going-faster-by-doing-less)
- [Going faster by understanding CPU caches (5)](#5-going-faster-by-understanding-cpu-cache)
- [Going even faster by doing nothing (6)](#6-going-even-faster-by-doing-nothing)
- [The promised land](#the-promised-land)
- [Conclusion](#conclusion)

<!-- intentionally omitted --->
<!-- - [Whoops the binary search bug bit us (7)](#7-whoops-the-binary-search-bug-bit-us) -->

## 1. A horrendously naive implementation

Here's what a Go novice might write for `strings.Repeat`.

```go
func Repeat(s string, count int) string {
	out := ""
	for range count {
		out += s
	}
	return out
}
```

Although this code works, it has a glaring performance issue.
A benchmark reporting the time and memory used by `Repeat("abc", count)` for `count = 1, 2, 4, ..., 32` immediately reveals the issue. (Benchmarking gurus, fret not; the call to `Repeat` is, perhaps surprisingly, not optimized out or hoisted out the loop.)

```go
func BenchmarkRepeat(b *testing.B) {
	s := "abc"
	for count := 1; count <= 64; count *= 2 {
		b.Run(fmt.Sprintf("repeat_%d", count), func(b *testing.B) {
			for b.Loop() {
				Repeat(s, count)
			}

			b.ReportAllocs()
		})
	}
}
```

Here are the results on my machine:

| count | time/op (ns) | allocs/op |
|-----------|------------------|---------------|
| 1 | 5.695 | 0 |
| 2 | 27.38 | 1 |
| 4 | 70.52 | 3 |
| 8 | 173.5 | 7 |
| 16 | 432.5 | 15 |
| 32 | 1,079 | 31 |

The time/op is noisy and will vary if you run the same experiment locally, but the key is the allocations: `Repeat(s, count)` makes `count - 1` (why -1?)[^2] separate heap allocations. The cause is that Go strings are immutable, and `out += s` will allocate a new string in each iteration. In fact, since the original contents of `out` must be copied to the new string along with `s`, this code is not only inefficient memory-wise but also time-wise: the asymptotic runtime is quadratic in `count`.

Let's take a stab at allocating less.

## 2. A less naive implementation: preallocating a buffer

Since we know that the output string will have length $m \times n$ where `m = len(s)` and `n = count`, we can preallocate a `[]byte` buffer of the proper size at the start and append to it:

```go
func Repeat(s string, count int) string {
	buf := make([]byte, 0, len(s) * count)
	for range count {
		buf = append(buf, s...)
	}
	return string(buf)
}
```

Running the benchmark again, we get

| count | time/op (ns) | allocs/op |
|-----------|------------------|---------------|
| 1 | 22.60 | 2 |
| 2 | 29.58 | 2 |
| 4 | 34.75 | 2 |
| 8 | 44.51 | 2 |
| 16 | 71.94 | 2 |
| 32 | 112.2 | 2 |

Nice! Now, `Repeat(s, count)` only makes a constant number of heap allocations (2) instead of `count - 1`. The runtime has also improved for larger `count`. (As an interesting historical note, our implementation here now resembles a modern variant of the original implementation of `strings.Repeat`, [contributed way back in November 2009](https://github.com/golang/go/commit/37f71e8ad644c0e91bb4449882f60b95c7d4644a).)

However, there are two obvious questions to be resolved:

1. There are 2 heap allocations---why? Can we make just 1? 
2. Our new implementation regresses in the `count = 1` case. Can we make it faster?

## 3. An acceptably naive, idiomatic implementation

For the first issue, the first allocation comes from `make([]byte, 0, len(s) * count)` and is unavoidable in the general case. The second, unwanted allocation comes from the `[]byte -> string` conversion when we return `string(buf)`. Since a Go string is just a fat pointer to bytes in memory and `buf` does not escape the function, this additional allocation is entirely avoidable. A sufficiently smart compiler would simply reuse `buf` as the backing memory of the string, as requested in [Go issue #6714](https://github.com/golang/go/issues/6714).

In the meantime, what can we do? One option is to resort to unsafe trickery to manufacture a string backed by the memory of `buf` using [`unsafe.StringData`](https://pkg.go.dev/unsafe#StringData). Yuck. Lucky for us, there is a nicer solution. The Go standard library provides [`strings.Builder`](https://pkg.go.dev/strings#Builder), which allows building strings incrementally while minimizing allocations. Under the hood, it resorts to the same unsafe trickery mentioned above, but encapsulates it in a safe API. Here's the refactored code:

```go
func Repeat(s string, count int) string {
	var b strings.Builder
	b.Grow(len(s) * count)
	for range count {
		b.WriteString(s)
	}
	return b.String()
}
```

As in our previous code, `strings.Builder` allocates a byte buffer up front, but the final call to `b.String()` will reuse the backing memory of the buffer instead of copying.

Benchmark results:
| count | time/op (ns) | allocs/op |
|-----------|------------------|---------------|
| 1 | 15.51 | 1 |
| 2 | 17.46 | 1 |
| 4 | 24.74 | 1 |
| 8 | 43.32 | 1 |
| 16 | 58.20 | 1 |
| 32 | 94.54 | 1 |
| 64 | 166.7 | 1 |

Cool---just one allocation, and a runtime win to boot! Beyond eliminating the extra conversion, one additional benefit of using `strings.Builder` is that it doesn't [zero-initialize its internal buffer](https://github.com/golang/go/commit/132fae93b789ce512068ff4300c665b40635b74e), whereas `make` always zeros.

However, compared to the original naive solution using string concatenation, we are still regressing in the `count = 1` case. We can handle this case specially at the top of the function, and also special-case `count = 0` while at it:

```go
func Repeat(s string, count int) string {
	switch count {
	case 0:
		return ""
	case 1:
		return s
	}

	var b strings.Builder
	b.Grow(len(s) * count)
	for range count {
		b.WriteString(s)
	}
	return b.String()
}
```

Of course, one might question whether `count = 0` and `count = 1` are hit enough in real code to justify the branch. The CL that [added special handling for `count = 1` to the real implementation of `strings.Repeat` in 2022](https://go-review.googlesource.com/c/go/+/411477) argues that although the forms `strings.Repeat(s, 0)` and `strings.Repeat(s, 1)` are uncommon, when the count is computed dynamically, it's reasonable for the resulting value to be `0` or `1`. Moreover, the CL presents benchmarks that show the branch has negligible cost in the case where `count > 1`. So we'll leave them in.

## Interlude

The above implementation is idiomatic Go and vaguely performant. It is where I might stop if I were reimplementing `strings.Repeat` from scratch in my own codebase.

Yet, we are barely over 10 lines, and as mentioned at the start of this blog, the real standard library implementation is near 100. Let's start digging into the interesting stuff.

## 4. Going faster by doing less

The first few optimizations we made were fairly obvious. But now that the low-hanging fruit are gone, it's time to do a little profiling to guide our investigation. Running `go test -test=^$ -bench=. -cpuprofile=cpu.out` with

```go
func BenchmarkRepeat(b *testing.B) {
	for b.Loop() {
		Repeat("a", 1024)
	}
}
```

instruments the benchmark and generates a CPU profile at `cpu.out`. We can then use `go tool pprof -http=:8081 cpu.out` to open a web view of the profile. Most of the time is spent between the following procedures:

{{< figure src="/profile1.png" alt="graph of cpu profile" width="500" class="center" >}}

What's going on here? Recall that our code looks like this currently:

```go
func Repeat(s string, count int) string {
	switch count {
	case 0:
		return ""
	case 1:
		return s
	}

	var b strings.Builder
	b.Grow(len(s) * count)
	for range count {
		b.WriteString(s)
	}
	return b.String()
}
```

The majority of the work is being done in the (inlined) call to `b.WriteString` on line 12 in the loop body. (The other runtime is accounted for by the initial buffer allocation, shuffling data around, and testing the loop end condition.) With this in mind, let's start looking at `WriteString` and see what we can discover.

### copyCheck

The body of `WriteString` looks like this:

```go
func (b *Builder) WriteString(s string) (int, error) {
	b.copyCheck()
	b.buf = append(b.buf, s...)
	return len(s), nil
}
```

Besides appending to the internal buffer, as expected, there's an additional call to `copyCheck`. In the profile graph, we see that `copyCheck` accounts for 150 ms / 880 ms. What is this procedure doing? Going into the implementation, we see

```go
func (b *Builder) copyCheck() {
	if b.addr == nil {
		// This hack works around a failing of Go's escape analysis
		// that was causing b to escape and be heap allocated.
		// See issue 23382.
		// TODO: once issue 7921 is fixed, this should be reverted to
		// just "b.addr = b".
		b.addr = (*Builder)(abi.NoEscape(unsafe.Pointer(b)))
	} else if b.addr != b {
		panic("strings: illegal use of non-zero Builder copied by value")
	}
}
```

Ah! As the name might have suggested, `copyCheck` is a safety check that ensures `strings.Builder`'s are never copied. This restriction is necessary since `strings.Builder` requires exclusive ownership of its underlying buffer so that the final string conversion can reuse the same buffer. If the builder is copied, the underlying buffer will be aliased and that assumption no longer holds.

However, in our case, and more generally in any correct use of `strings.Builder`, `copyCheck` ends up being an entirely redundant check. Ideally the compiler would be intelligent enough to elide the check, but it is not. Nevertheless, if we want to continue using `strings.Builder`, we must live with the call to `copyCheck`. Let's continue for now, but note the observation:

> **Observation 1.** We're calling `copyCheck` on every iteration of the loop, but it's totally redundant.

### memmove

Moving past `copyCheck`, 270 ms of 880 ms is spent in `runtime.memmove`. There's no `runtime.memmove` to be seen in our original code, so where is it coming from?

If we stop and ponder a little about what `b.buf = append(b.buf, s...)` must do under the hood, the answer reveals itself. When we append a string (interpreted as a slice of bytes) to a slice of bytes in Go, two things must happen under the hood:

1. Check whether the slice has enough capacity to accommodate the new bytes at the end;
	- if not, reallocate the buffer to make space, then
2. Copy the new bytes to the end of the slice.

The second step uses `memmove`. Indeed, if we look at [the function responsible for `append` codegen](https://github.com/golang/go/blob/e73dadc758d30a11146e32cc1d0baafa255641a6/src/cmd/compile/internal/walk/assign.go#L476), we see the following comment:

```text {hl_lines=12, linenos=false}
// expand append(l1, l2...) to
//
//	init {
//	  s := l1
//	  newLen := s.len + l2.len
//	  // Compare as uint so growslice can panic on overflow.
//	  if uint(newLen) <= uint(s.cap) {
//	    s = s[:newLen]
//	  } else {
//	    s = growslice(s.ptr, s.len, s.cap, l2.len, T)
//	  }
//	  memmove(&s[s.len-l2.len], &l2[0], l2.len*sizeof(T))
//	}
//	s
```

`memmove` ends up calling out to optimized assembly, but let's peek at the source anyway in case there is anything interesting. The implementation for amd64 is in [`runtime/memmove_amd64.s`](https://github.com/golang/go/blob/go1.25rc2/src/runtime/memmove_amd64.s). The exact algorithm used is dependent on input size, and an oversimplified overview is:

- for small inputs, straightline code that copies source bytes into registers and then to the destination is used;
- for larger inputs, either AVX (vectorized) instructions or [REP MOVSB](https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz) is used.

What one is used in our case? Let's look at the disassembly view in pprof:

```
    163            .          .           move_1or2: 
    164            .          .           	MOVB	(SI), AX 
    165            .          .           	MOVB	-1(SI)(BX*1), CX 
    166         10ms       10ms           	MOVB	AX, (DI) 
    167        170ms      170ms           	MOVB	CX, -1(DI)(BX*1) 
    168            .          .           	RET 
```

Oh.

Given `Repeat("a", 1024)`, our code boils down to

```go
for range 1024 {
	buf = append(buf, 'a')
}
```

which is memmove'ing `a` to the end of `buf` one character at a time. Our writes aren't big enough to use the vectorized copy loop or `REP MOVSB` at all!

That also explains why `memmove`, which feels like it should be the bottleneck in our code, isn't taking up as much time as one would expect relative to `WriteString` and `copyCheck`. Since we're writing one character at a time instead of batching, each single `memmove` is cheap but we're paying for shuffling data around registers, the capacity check in `append`, the redundant `copyCheck`, and so on in every iteration as well.

> **Observation 2.** We're not taking full advantage of `memmove` since we're only writing one copy of the string to the output buffer per iteration. On the other hand, per-iteration overhead ends up costing us heavily.

### Calling `WriteString` less by writing more at a time

The natural solution, then, is to try to write bigger chunks at a time---informally, instead of writing one copy of the string per iteration, write a whole bunch of copies. The _total_ number of bytes we write will not change, but the hope is that we'll utilize `memmove` more effectively by virtue of copying more bytes at a time.

Now... how do we actually do this? Where do the "bigger chunks" come from?

This step requires a bit of imagination but should be familiar to anyone familiar with divide-and-conquer algorithms. For simplicity, let's first focus on `Repeat(s, count)` where `count` is a power of `2`. We first write one copy of `s` to the output buffer:

```
iteration 1:
------------
buf = s // buf += s
      ^ new
```

and another:

```
iteration 2:
------------
buf = ss // buf += s
       ^ new
```

Here's the key. On the third iteration, instead of writing another copy of `s`, notice that the buffer already contains _two_ copies of `s`. So we can just append the contents of the buffer to the end of itself!

```
iteration 3:
------------
buf = ssss // buf += buf
        ^^ new
```

Likewise, on the fourth iteration, we have

```
iteration 4:
------------
buf = ssssssss // buf += buf
          ^^^^ new
```

and we repeat all the way until we reach `count`.

In the case where `count` is a power of `2`, the above idea works perfectly:

```go
n := len(s) * count // final length

b.WriteString(s)
for b.Len() < n {
	b.WriteString(b.String())
}
```

To account for the case where `count` is not a power of `2`, we need to take care to not write too many copies on the last iteration:

```go
n := len(s) * count // final length

b.WriteString(s)
for b.Len() < n {
	chunk := min(b.Len(), n-b.Len())
	// chunk==b.Len() except in the last iteration,
	// in which case `b` might hold more copies than needed,
	// so just write enough to get to `n`.
	b.WriteString(b.String()[:chunk]) 
}
```

The complete code now looks like so:

```go
func Repeat(s string, count int) string {
	switch count {
	case 0:
		return ""
	case 1:
		return s
	}

	n := len(s) * count

	var b strings.Builder
	b.Grow(n)
	b.WriteString(s)
	for b.Len() < n {
		chunk := min(b.Len(), n-b.Len())
		b.WriteString(b.String()[:chunk])
	}
	return b.String()
}
```

Compared to the previous implementation, the main loop now only runs $\lceil \log_2(\texttt{count}) \rceil$ times, and writes increasingly longer strings containing more and more copies of `s` at a time. We therefore expect `memmove` to dominate the runtime, and for overhead in `WriteString` such as `copyCheck` and `append` capacity checks to become negligible. Since `memmove` is able to use more sophisticated algorithms with reduced cycles per copied byte, we also expect the overall runtime to drop.

Let's see if these expectations hold. Using the [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat) tool, we can compare the old/new benchmark results:

```
          │   old.txt    │               new.txt               │
          │    sec/op    │   sec/op     vs base                │
Repeat-16   2210.0n ± 7%   250.3n ± 5%  -88.67% (p=0.000 n=10)
```

Not bad---around 10x faster for `Repeat("a", 1024)`!

Viewing the updated CPU profile, we see the following:

{{< figure src="/profile2.png" alt="graph of cpu profile after log optimization" width="500" class="center" >}}

That's quite different compared to our previous profile! Garbage collection is now responsible for much more of the runtime. (You'll notice that only around 50% of the time is spent in `Repeat`. The graph above doesn't show GC procedures running in background workers, which accounts for the other half.) My best guess is that since our `Repeat` function is significantly faster, the benchmark is able to generate lots more output which then needs to be garbage collected.

In any case, our expected outcomes above do hold: the vast majority of actual `Repeat` call time is now spent in `memmove`, and the overhead due to `WriteString` and `copyCheck` is negligible. The new implementation is substantially faster as well.

## 5. Going faster by understanding CPU caches

## 6. Going even faster by doing nothing*

## 7. Whoops, the binary search bug bit us

## The promised land

## Conclusion

[^1]: This line count admittedly includes some comments, constants, and whitespace, but even excluding those leaves us with around ~50 lines of code.
[^2]: It's natural to wonder why there are `count - 1` allocations instead of exactly `count`. The off-by-one is due to a Go compiler optimization where `string1 + string2` will return `string2` without an additional allocation if `string1` is empty (see [the implementation of `runtime.concatstrings`](https://github.com/golang/go/blob/e73dadc758d30a11146e32cc1d0baafa255641a6/src/runtime/string.go#L48-L53)), so the first iteration does not incur an allocation.
