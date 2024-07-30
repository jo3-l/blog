---
title: Exploring the Sum of Exponents Law
date: '2022-04-24'
summary: 'Some practice with induction: a proof of the sum of exponents law for integer exponents.'
description: 'Some practice with induction: a proof of the sum of exponents law for integer exponents.'
tags: [math]
katex: true
---

The sum of exponents law, $b^x \cdot b^y = b^{x+y}$, is well-known---indeed, it was one of the first
properties that I learnt after being introduced to the concept of exponentiation. Though it's easy
to reason intuitively as to why this property holds for integral exponents,

$$
2^{3 + 2} = 2^5 = \underbrace{2 \cdot 2 \cdot 2}\_{2^3} \cdot \underbrace{2 \cdot 2}\_{2^2},
$$

I wanted to see how difficult it'd be to formalize this argument with induction. Let's take a look!

## The sum of exponents law

The statement we aim to prove is the following:

> **Sum of Exponents Law for Integer Exponents.** For positive real $b$, the equation $$ b^x \cdot
> b^y = b^{x + y} $$ holds for all integer $x$, $y$.

This law holds for $x$, $y$ real, but we concern ourselves only with the easiest integer case in
this blog. Perhaps someday there will be a follow-up post...

## Defining exponentiation

We first need a definition of exponentiation for integer powers to work with. A recursive definition
is convenient for induction:

$$
b^x =
    \begin{cases}
        \dfrac{1}{b^{-x}}, & \text{if $x < 0$} \\\\
        1, & \text{if $x = 0$} \\\\
        b \cdot b^{x-1}, & \text{if $x > 0$}
    \end{cases}
$$

## Adding positive exponents

We can immediately address the trivial case where both exponents are positive integers.

> **Lemma 1.1.** For all $x, y \in \mathbb{Z^+}$, we have $b^{x + y} = b^x \cdot b^y$.

_Proof._ We induct on $x$.

**Base case.** If $x = 1$, then $b^{x + y} = b^{y + 1} = b \cdot b^y$ by definition, which is equal
to ${b^x \cdot b^y = b^1 \cdot b^y = b \cdot b^y}$.

**Induction step.** Let $x \in \mathbb{Z^+}$ be arbitrary and suppose $b^{x + y} = b^x \cdot b^y$
for all $y \in \mathbb{Z^+}$. Then

$$
\begin{align*}
	b^{(x + 1) + y} &= b^{x + y + 1} \\\\
		&= b \cdot b^{x + y} \\\\
		&= b \cdot b^{x} \cdot b^y && \text{(by induction hypothesis)} \\\\
		&= b^{x + 1} \cdot b^y
\end{align*}
$$

as desired. $\square$

## Subtracting positive exponents

Lemma 1.1 covers the case of two positive exponents (and, indirectly, the case of two negative
exponents); we still have no way to deal with exponents of different signs. The following lemma
addresses this gap:

> **Lemma 1.2.** For all $x, y \in \mathbb{Z^+}$ where $x \geq y$, we have $b^{x - y} = b^x \cdot b^{-y}$.

Equivalently, this lemma claims that $b^{x + y} = b^x \cdot b^y$ where $y$ is _negative_ and $|x| \geq |y|$;
however, the original presentation in terms of subtracting positive exponents is more amenable to induction.

_Proof._ We induct on $x$.

**Base case.** If $x = 1$, then the condition $x \geq y$ forces $y = 1$. Substituting, we have ${b^{1 - 1} = b^0 = 1}$
which is equal to $b^1 \cdot b^{-1} = 1$.

**Induction step.** Let $x \in \mathbb{Z^+}$ be arbitrary and suppose $b^{x - y}
= b^x \cdot b^{-y}$ for all $y \in \mathbb{Z^+}$ such that $x \geq y$. Then

$$
\begin{align*}
	b^{(x + 1) - y} &= b^{x - y + 1} \\\\
	&= b \cdot b^{x - y} \\\\
	&= b \cdot b^x \cdot b^{-y} && \text{(by induction hypothesis)} \\\\
	&= b^{x + 1} \cdot b^{-y}
\end{align*}
$$

as desired. $\square$

## The full proof

We are now equipped to tackle the full proof where $x$ and $y$ are unrestricted aside from being
integers. Broadly speaking, Lemma 1.1 covers the case where $x$ and $y$ are both positive or both
negative, and Lemma 1.2 covers the case where one is negative and the other positive; all that
remains is to carefully invoke them and handle the straightforward case where one exponent is zero.

To recall, the statement we aim to prove was:

> **Sum of Exponents Law for Integer Exponents.** For positive real $b$, the equation $$ b^x \cdot
> b^y = b^{x + y} $$ holds for all integer $x$, $y$.

_Proof._ We consider the following cases.

**Case 1.** _Both $x$ and $y$ are positive._ Lemma 1.1 discusses precisely this case.

**Case 2.** _Both $x$ and $y$ are negative._ Then $-x$ and $-y$ are both positive, so taking the
reciprocal allows us to apply Lemma 1.1 as follows:

$$
\begin{align*}
b^x \cdot b^y &= \frac{1}{b^{-x}} \cdot \frac{1}{b^{-y}} \\\\
    &= \frac{1}{b^{-x} \cdot b^{-y}} \\\\
    &= \frac{1}{b^{-x - y}} && \text{(by Lemma 1.1)} \\\\
	&= \frac{1}{b^{-(x + y)}} \\\\
    &= b^{x + y}.
\end{align*}
$$

**Case 3.** _Exactly one of $x, y$ is negative._

Without loss of generality, suppose $x < 0$ and $y > 0$. We consider two
sub-cases: ${|x| < |y|}$ and ${|x| \geq |y|}$.

First consider the case where $|x| < |y|$. We manipulate the expression into a form suitable for
Lemma 1.2:

$$
\begin{align*}
b^x \cdot b^y &= b^{-(-x)} \cdot b^y \\\\
	&= b^y \cdot b^{-(-x)} \\\\
	&= b^{y - (-x)} && \text{(by Lemma 1.2)} \\\\
	&= b^{x + y}.
\end{align*}
$$

Otherwise we have $|x| \geq |y|$, in which case taking the reciprocal again admits Lemma 1.2:

$$
\begin{align*}
\frac{1}{b^x \cdot b^y} &= \frac{1}{b^x} \cdot \frac{1}{b^y} \\\\
	&= b^{-x} \cdot b^{-y} \\\\
	&= b^{-x - y} && \text{(by Lemma 1.2)} \\\\
	&= b^{-(x + y)} \\\\
	&= \frac{1}{b^{x + y}}.
\end{align*}
$$

**Case 4.** _At least one of $x$, $y$ is 0._

Without loss of generality, suppose $x = 0$. Then $b^x \cdot b^y = 1 \cdot b^y = b^y$ which is equal
to $b^{x + y} = b^{0 + y} = b^y$ as desired.

In all four cases, the law holds and so we are done. $\square$
