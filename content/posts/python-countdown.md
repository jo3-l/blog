---
title: A puzzling Python program
summary: Counting, seemingly without loops or recursion, in the language of the snakes
description: Counting, seemingly without loops or recursion, in the language of the snakes
date: '2025-08-08'
tags: [programming, python, puzzle]
---

Here's a quirky little Python program:

```python
class countdown:
	def __init__(self, n):
		self.n = n

	def __getitem__(self, k):
		if v := self.n - k:
			return print(v),

print("rocket launching 🚀") in countdown(10)
```

What does it output, and why?

<details>

<summary>Output</summary>

```text {linenos=false}
$ python3 countdown.py
rocket launching 🚀
10
9
8
7
6
5
4
3
2
1
```

</details>

<details>

<summary>Hint 1</summary>

`print` returns `None`, so after the initial log it remains to evaluate `None in countdown(10)`.

</details>

</details>

<details>

<summary>Hint 2</summary>

Suppose `X` is a list. What does `None in X` do internally? By analogy, what might `None in countdown(10)` do internally?

</details>

<details>

<summary>Explanation</summary>

Note first that `print("rocket launching 🚀")` evaluates to `None`, so we need to evaluate `None in countdown(10)`.

Since the `countdown` class doesn't define `__contains__()`, Python iterates over `countdown(10)` viewed as a sequence and tests if `elem == None` for each element. However, `countdown` doesn't define `__iter__()` either, so Python falls back to the so-called "old-style iteration protocol" in which

```
given C = countdown(10),
  iter(C)
corresponds to the sequence
  C.__getitem__(0),
  C.__getitem__(1),
  C.__getitem__(2),
  C.__getitem__(3),
  ...
```

To determine whether `None` is contained in this sequence, Python calls `__getitem__(k)` with indices `k = 0, 1, 2, ...` in order until it encounters `None` or an `IndexError`. Recall now that `countdown.__getitem__` is defined by

```python
def __getitem__(self, k):
	if v := self.n - k:
		return print(v),
	# implicit `return None`
```

For `k = 0, 1, ..., 9`, the number `v := self.n - k = 10 - k` takes on the values `10, 9, ..., 1`. Each of these values is nonzero, so the `if` succeeds and `v` is printed. Then, since `print` returns None, `__getitem__` returns the 1-tuple `(None,)` (note the trailing comma on line 3!) Since `(None,) != None`, Python continues iterating.

On the other hand, when `k = 10`, the number `v = self.n - k = 10 - 10 = 0` is zero and hence falsy, so `None` is implicitly returned. Now that `None` has been found in the sequence, Python stops iterating and the expression `None in countdown(10)` evaluates to `True`. (This value is then thrown away.)

Isn't that fun? :)

---

I learned this quirk from reading [issue #137473 in the CPython repository](https://github.com/python/cpython/issues/137473) on a particularly slow afternoon. The precise behavior here is specified by the second-last paragraph of [Section 6.10.2: Membership test operations](https://docs.python.org/3/reference/expressions.html#membership-test-operations) of the Python reference:

> Lastly, the old-style iteration protocol is tried: if a class defines `__getitem__()`, `x in y` is `True` if and only if there is a non-negative integer index _i_ such that `x is y[i]` or `x == y[i]`, and no lower integer index raises the `IndexError` exception. (If any other exception is raised, it is as if `in` raised that exception).

</details>

<details>

<summary>
How do LLMs do on this puzzle?
</summary>

I provided the first two models I thought of with the Python program here, and asked it to predict and explain the runtime behavior. (By no means do I believe this is a fair question; I just thought it'd be fun.)

The free version of GPT-5 one-shots my question and [correctly explains what's going on](https://chatgpt.com/share/689645d3-aa44-800c-9c9c-9a69a19552d2). I'm impressed!

Claude Sonnet 4 (also free) [gets pretty close](https://claude.ai/share/4c4e131c-dd77-414c-b3fb-f1bccada8780), but erroneously claims that the code errors at the end with a bogus argument:

> [...] when `__getitem__` returns `None` (at `k=10`), Python tries to iterate over `None` to continue the membership test, causing the error.

When I hint that its answer is incorrect without further elaboration, it hallucinates more.

I expect Opus 4.1 does better and would be a more fair comparison with GPT-5, but did not test it.

I also expect that nearly all new models would explain the behavior correctly if provided the output (or, equivalently, was able to run the code), but did not test this hypothesis either.

</details>
