---
title: Proving the Sum of Exponents Law
date: '2022-04-24'
summary: |
  Recently, while reading about proofs of logarithm laws, I was reminded of the sum of exponents law; b^x * b^y = b^(x + y).
  Given that this well-known rule is amongst the first things taught when students are introduced to exponentials in pre-calculus, I naively assumed that it would be trivial to prove.

  I was wrong.
description: How I learned I really didn't understand exponents
tags: [math]
katex: true
---

Recently, while reading about proofs of logarithm laws, I was reminded of the sum of exponents law; $b^x \cdot b^y = b^{x + y}$.
Given that this well-known rule is amongst the first things taught when students are introduced to exponentials in pre-calculus, I naively assumed that it would be trivial to prove.

I was wrong.

# The Sum of Exponents Law

The sum of exponents law goes like such:

> For all $b \in \mathbb{R^+}, x \in \mathbb{R}, y \in \mathbb{R}$, $b^x \cdot b^y = b^{x + y}$.

How exactly do we go about proving this? One method is to start with a proof for integral exponents, then use that to prove correctness for rational exponents, and finally extend to real exponents.

# Integral Exponents

Intuitively, it is not difficult to see why the sum of exponents law holds for integral exponents, assuming that exponentiation is defined as repeated multiplication:

$$
b^x \cdot b^y = \overbrace{\underbrace{b \times b \times \cdots \times b}\_{\text{$x$ times}} \times \underbrace{b \times b \times \cdots \times b}\_{\text{$y$ times}}}^{\text{$x + y$ times}}
$$

However, proving it rigorously is surprisingly challenging. We start by defining exponentiation as a recursive function:

$$
b^x =
    \begin{cases}
        1 / b^{-x}, & \text{if $x < 0$} \\\\
        1, & \text{if $x = 0$} \\\\
        b \cdot b^{x-1}, & \text{otherwise}
    \end{cases}
$$

Using this definition, we will prove that the law holds for positive integers using induction, and then extend that to all integers.

## Lemma 1.1

> $b^{x + y} = b^x \cdot b^y$ for all $b \in \mathbb{R^+}, x \in \mathbb{Z^+}, y \in \mathbb{Z^+}$.

_Proof._ We proceed by induction on $x$.

**Base Case:** If $x = 1$, then $b^{x + y} = b^{y + 1} = b \cdot b^y$ by definition, which is equal to $b^x \cdot b^y = b^1 \cdot b^y = b \cdot b^y$.

**Induction Step:** Let $x$ be an arbitrary positive integer and suppose $b^{x + y} = b^x \cdot b^y$ for all positive integers $y$. Then

$$
\begin{align*}
	b^{(x + 1) + y} &= b^{x + y + 1} \\\\
		&= b \cdot b^{x + y} && \text{(by definition of exponentiation)} \\\\
		&= b \cdot b^{x} \cdot b^y && \text{(by induction hypothesis)} \\\\
		&= b^{x + 1} \cdot b^y && \text{(by definition of exponentiation)}.
\end{align*}
$$

<div align="right">$\square$</div>

## Lemma 1.2

> $b^{x - y} = b^x \cdot b^{-y}$ for $x \in \mathbb{Z^+}, y \in \mathbb{Z^+}$ s.t. $x \geq y$.

_Proof._ We proceed by induction on $x$.

**Base Case:** If $x = 1$, the only valid choice for $y$ is $1$. Substituting, we have $b^{1 - 1} = b^0 = 1$ which is equal to $b^1 \cdot b^{-1} = 1$.

**Induction Step:** Let $x$ be an arbitrary positive integer and suppose $b^{x - y} = b^x \cdot b^{-y}$ for all positive integers $y$ s.t. $x \geq y$. Then

$$
\begin{align*}
	b^{(x + 1) - y} &= b^{x - y + 1} \\\\
	&= b \cdot b^{x - y} && \text{(by definition of exponentiation)} \\\\
	&= b \cdot b^x \cdot b^{-y} && \text{(by induction hypothesis)} \\\\
	&= b^{x + 1} \cdot b^{-y} && \text{(by definition of exponentiation)}.
\end{align*}
$$

<div align="right">$\square$</div>

## Theorem 1.3

> $b^{x + y} = b^x \cdot b^y$ for all $b \in \mathbb{R^+}, x \in \mathbb{Z}, y \in \mathbb{Z}.$

_Proof._ If $x \in \mathbb{Z^+}, y \in \mathbb{Z^+}$ then the theorem is true by Lemma 1.1. Otherwise, we have the following cases.

**Case 1:** _Exactly one of $x, y$ is negative._

W.L.O.G assume $x < 0$ and $y > 0$. We consider two sub-cases: $|x| < |y|$ and $|x| \geq |y|$. Note that since $x$ is negative, $|x| = -x$.

First consider $|x| < |y|$. Then

$$
\begin{align*}
b^x \cdot b^y &= b^{-(-x)} \cdot b^y \\\\
	&= b^y \cdot b^{-(-x)} \\\\
	&= b^{y - (-x)} && \text{(by Lemma 1.2 as $y > -x$)} \\\\
	&= b^{x + y}.
\end{align*}
$$

Otherwise we have $|x| \geq |y|$. Taking the reciprocal of $b^x \cdot b^y$ yields

$$
\begin{align*}
\frac{1}{b^x \cdot b^y} &= \frac{1}{b^x} \cdot \frac{1}{b^y} \\\\
	&= b^{-x} \cdot b^{-y} && \text{(by definition of exponentiation)} \\\\
	&= b^{-x - y} && \text{(by Lemma 1.3 as $-x \geq y$)} \\\\
	&= b^{-(x + y)} \\\\
	&= \frac{1}{b^{x + y}} && \text{(by definition of exponentiation)}.
\end{align*}
$$

Thus, $\dfrac{1}{b^x \cdot b^y} = \dfrac{1}{b^{x + y}}$. Taking the reciprocal of both sides again gives the result.

**Case 2:** _Both $x$ and $y$ are negative._

$$
\begin{align*}
b^x \cdot b^y &= \frac{1}{b^{-x}} \cdot \frac{1}{b^{-y}} \\\\
    &= \frac{1}{b^{-x} \cdot b^{-y}} \\\\
    &= \frac{1}{b^{-x - y}} && \text{(by Lemma 1.2 as $-x > 0, -y > 0$)} \\\\
	&= \frac{1}{b^{-(x + y)}} \\\\
    &= b^{x + y} && \text{(by definition of exponentiation)}.
\end{align*}
$$

**Case 3:** _One or more of $x$, $y$ is 0._

W.L.O.G. assume $x = 0$. Then $b^x \cdot b^y = 1 \cdot b^y = b^y$ which is equal to $b^{x + y} = b^{0 + y} = b^y$ as desired.

<div align="right">$\square$</div>

# Rational Exponents

We now extend our proof to cover rational exponents. First, let us define what exponentiation with rational exponents means.

For any real number $b > 0$ and positive integer $n$, let $b^{1/n}$ denote the unique positive rational number $r$ s.t. $r^n = b$.
Then, for a rational number $\frac{p}{q}$ where $p \in \mathbb{Z}, q \in \mathbb{Z^+}$ are coprime, define $b^{\frac{p}{q}}$ to be equal to $(b^{1/q})^p$.

Given this definition, we can reduce the sum of exponents law for rational exponents to integral exponents, which we know to be true. In order to perform this reduction, we will need a couple more lemmas:

## Lemma 2.1

> $(ab)^n = a^n \cdot b^n$ for all $a \in \mathbb{R}, b \in \mathbb{R}, n \in \mathbb{Z}$.

_Proof._ We consider three cases.

**Case 1:** _$n$ is greater than $0$._

We proceed by induction on $n$.

**Base Case:** If $n = 1$, then $(ab)^1 = a \cdot b = a^1 \cdot b^1$.

**Induction Step:** Let $n$ be an arbitrary positive integer and suppose $(ab)^n = a^n \cdot b^n$ for all $a \in \mathbb{R}, b \in \mathbb{R}$. Then

$$
\begin{align*}
(ab)^{n + 1} &= ab \cdot (ab)^n && \text{(by definition of exponentiation)} \\\\
	&= ab \cdot a^n \cdot b^n && \text{(by induction hypothesis)} \\\\
	&= a^{n + 1} \cdot b^{n + 1} && \text{(by definition of exponentiation)}.
\end{align*}
$$

**Case 2:** _$n$ is $0$._

Then $(ab)^n = 1 = a^n \cdot b^n = a^0 \cdot b^0$, as desired.

**Case 3:** _$n$ is less than $0$._

Then

$$
\begin{align*}
(ab)^n &= \frac{1}{(ab)^{-n}} && \text{(by definition of exponentiation)} \\\\
	&= \frac{1}{a^{-n} \cdot b^{-n}} && \text{(by Case 1 as $-n > 0$)} \\\\
	&= \frac{1}{a^{-n}} \cdot \frac{1}{b^{-n}} \\\\
	&= a^{n} \cdot b^{n} && \text{(by definition of exponentiation)}.
\end{align*}
$$

<div align="right">$\square$</div>

## Lemma 2.2

> $a^n = b^n \implies a = b$ for all $a \in \mathbb{R^+}, b \in \mathbb{R^+}, n \in \mathbb{Z} \setminus \\{0\\}$.

_Proof._ We consider two cases.

**Case 1:** _$n$ is greater than $0$._

We proceed by induction on $n$.

**Base Case:** $a^1 = b^1 \implies a = b$ as desired.

**Induction Step:** Let $n$ be an arbitrary positive integer s.t. $a^n = b^n$. By Theorem 1.3, $a^{n+1} = a^n \cdot a$ and $b^{n+1} = b^n \cdot b$. Thus $a^{n+1} = b^{n+1} \iff a^n \cdot a = b^n \cdot b$. As $a^n = b^n$, we have $a = b$ as desired.

**Case 2:** _$n$ is less than $0$._

Taking the reciprocal of both sides gives $\frac{1}{a^n} = \frac{1}{b^n} \iff a^{-n} = b^{-n}$. As $-n$ is positive, we have $a = b$ by case 1, completing the proof.

<div align="right">$\square$</div>

## Theorem 2.2

> $b^{x + y} = b^x \cdot b^y$ for all $b \in \mathbb{R^+}, x \in \mathbb{Q}, y \in \mathbb{Q}$.

Write $x$ as $p/q$ where $p \in \mathbb{Z}, q \in \mathbb{Z^+}$ and $p, q$ are coprime. Likewise write $y$ as $r/s$ where $r$ and $s$ are similarly restricted.

Then the R.S. of the equation becomes $b^{\frac{p}{q}} \cdot b^{\frac{r}{s}}$. Taking the $qs$-th power of this expression yields

$$
\begin{align*}
(b^{\frac{p}{q}} \cdot b^{\frac{r}{s}})^{qs} &= b^{\frac{p}{q} \cdot qs} \cdot b^{\frac{r}{s} \cdot qs} && \text{(by Lemma 2.1)} \\\\
	&= b^{ps} \cdot b^{qr} \\\\
	&= b^{ps + qr} && \text{(by Theorem 1.3)}.
\end{align*}
$$

This is equivalent to the L.S. of the equation raised to the $qs$-th power, which is

$$
\begin{align*}
(b^{\frac{p}{q} + \frac{r}{s}})^{qs} &= b^{(\frac{p}{q} + \frac{r}{s}) \cdot qs} && \text{(by Lemma 2.1)} \\\\
	&= b^{\frac{p}{q} \cdot qs + \frac{r}{s} \cdot qs} \\\\
	&= b^{ps + qr}.
\end{align*}
$$

As $qs \in \mathbb{Z}$ and $qs \neq 0$, we conclude that the L.S. is equal to the R.S. by Lemma 2.2.

<div align="right">$\square$</div>

# Real Exponents

We are finally prepared to prove the sum of exponents law for real exponents. However, a problem immediately arises when we attempt to define exponentiation at this stage.

While it was relatively trivial to define exponentiation for integral exponents as repeated multiplication and rational exponents using n-th roots and integral exponentiation,
it is not clear at first how we should go about doing the same for real exponents. For example, what exactly does $2^\pi$ mean?

It turns out that there are multiple ways of defining exponentiation for real exponents. The approach that we take here relies on the fact that any real number can be expressed as the limit of a sequence of rational numbers. Hence, we can define real exponents in terms of rational exponents by continuity. For example, we can define $2^\pi$ to be the limit of the sequence $2^3, 2^{3.1}, 2^{3.14}, 2^{3.141}, 2^{3.1415}, \cdots.$

Formally, for a real number $r$ and a base $b > 0$, we define $b^r$ thusly. Let $S$ be an infinite sequence of rational numbers that converges to $x$; that is, $\lim_{n \to \infty} S_n = x$.
Then $b^x$ can be defined as

$$
\lim_{n \to \infty} b^{S_n}
$$

## Theorem 3.1

> $b^{x + y} = b^x \cdot b^y$ for all $b > 0, x \in \mathbb{R}, y \in \mathbb{R}$.

_Proof._

$$
\begin{align*}
b^{x + y} &= \lim_{n \to \infty} b^{P_n + R_n} && \text{(where $\lim_{n \to \infty} P_n = x, \lim_{n \to \infty} R_n = y$)} \\\\
	&= \lim_{n \to \infty} b^{P_n} \cdot b^{R_n} \\\\
	&= \lim_{n \to \infty} b^{P_n} \cdot \lim_{n \to \infty} b^{R_n} \\\\
	&= b^x \cdot b^y.
\end{align*}
$$

<div align="right">$\square$</div>
