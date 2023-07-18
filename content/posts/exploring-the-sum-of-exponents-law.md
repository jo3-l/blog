---
title: Exploring the Sum of Exponents Law
date: '2022-04-24'
summary: An induction proof of the sum of exponents law for integral exponents, b^x × b^y = b^(x + y).
description: An induction proof of the sum of exponents law for integral exponents, b^x × b^y = b^(x + y).
tags: [math]
katex: true
---

The sum of exponents law, $b^x \cdot b^y = b^{x+y}$, is well-known -- indeed,
it's one of the first properties that's taught when students are introduced to
the concept of exponentiation. Though it's easy to reason intuitively as to why
this property holds for integral exponents:

$$
2^{3 + 2} = 2^5 = \underbrace{2 \cdot 2 \cdot 2}\_{2^3} \cdot \underbrace{2 \cdot 2}\_{2^2}
$$

it's a little more difficult to provide a rigorous proof. In this post, we do
just that using induction. (There exist more straightforward approaches using
comparatively advanced methods, such as the properties of $\exp$, but we stick
to the basics here because it makes for a more interesting post.)

# The Sum of Exponents Law

Formally, the exponent law can be stated as follows:

> For positive real $b$, the property $$ b^x \cdot b^y = b^{x + y} $$ holds for
> integer $x$, $y$.

It's worth noting that the law holds for $x$, $y$ real, but we concern ourselves
only with the integer case in this blog.

# Defining Exponentiation

We start by defining exponentiation for integral powers recursively:

$$
b^x =
    \begin{cases}
        \dfrac{1}{b^{-x}}, & \text{if $x < 0$} \\\\
        1, & \text{if $x = 0$} \\\\
        b \cdot b^{x-1}, & \text{if $x > 0$}
    \end{cases}
$$

# Lemma 1.1

> $b^{x + y} = b^x \cdot b^y$ for all $x, y \in \mathbb{Z^+}$.

_Proof._ We induct on $x$.

**Base case.** If $x = 1$, then $b^{x + y} = b^{y + 1} = b \cdot b^y$ by
definition, which is equal to $b^x \cdot b^y = b^1 \cdot b^y = b \cdot b^y$.

**Induction step.** Let $x \in \mathbb{Z^+}$ be arbitrary and suppose $b^{x + y}
= b^x \cdot b^y$ for all $y \in \mathbb{Z^+}$. Then

$$
\begin{align*}
	b^{(x + 1) + y} &= b^{x + y + 1} \\\\
		&= b \cdot b^{x + y} && \text{(by definition)} \\\\
		&= b \cdot b^{x} \cdot b^y && \text{(by induction hypothesis)} \\\\
		&= b^{x + 1} \cdot b^y && \text{(by definition)}
\end{align*}
$$

as desired. $\square$

# Lemma 1.2

> $b^{x - y} = b^x \cdot b^{-y}$ for all $x, y \in \mathbb{Z^+}$ such that $x
> \geq y$.

_Proof._ We induct on $x$.

**Base case.** If $x = 1$, then $y$ must also be $1$ to satisfy the condition
$x \geq y$. Substituting, we have $b^{1 - 1} = b^0 = 1$ which is equal to
$b^1 \cdot b^{-1} = 1$.

**Induction step.** Let $x \in \mathbb{Z^+}$ be arbitrary and suppose $b^{x - y}
= b^x \cdot b^{-y}$ for all $y \in \mathbb{Z^+}$ such that $x \geq y$. Then

$$
\begin{align*}
	b^{(x + 1) - y} &= b^{x - y + 1} \\\\
	&= b \cdot b^{x - y} && \text{(by definition)} \\\\
	&= b \cdot b^x \cdot b^{-y} && \text{(by induction hypothesis)} \\\\
	&= b^{x + 1} \cdot b^{-y} && \text{(by definition)}
\end{align*}
$$

as desired. $\square$

# Theorem 1.3

> $b^{x + y} = b^x \cdot b^y$ for all $x, y \in \mathbb{Z}.$

_Proof._ If $x, y \in \mathbb{Z^+}$ then the theorem is true by Lemma 1.1.
Otherwise, we have the following cases.

**Case 1.** _Exactly one of $x, y$ is negative._

Without loss of generality, suppose $x < 0$ and $y > 0$. We consider two
sub-cases: $|x| < |y|$, $|x| \geq |y|$.

First consider the case where $|x| < |y|$. Then

$$
\begin{align*}
b^x \cdot b^y &= b^{-(-x)} \cdot b^y \\\\
	&= b^y \cdot b^{-(-x)} \\\\
	&= b^{y - (-x)} && \text{(by Lemma 1.2)} \\\\
	&= b^{x + y}.
\end{align*}
$$

Otherwise we have $|x| \geq |y|$. Taking the reciprocal of $b^x \cdot b^y$ yields

$$
\begin{align*}
\frac{1}{b^x \cdot b^y} &= \frac{1}{b^x} \cdot \frac{1}{b^y} \\\\
	&= b^{-x} \cdot b^{-y} && \text{(by definition)} \\\\
	&= b^{-x - y} && \text{(by Lemma 1.3)} \\\\
	&= b^{-(x + y)} \\\\
	&= \frac{1}{b^{x + y}} && \text{(by definition)}.
\end{align*}
$$

Thus, $\dfrac{1}{b^x \cdot b^y} = \dfrac{1}{b^{x + y}}$. Taking the reciprocal
of both sides gives the desired result.

**Case 2.** _Both $x$ and $y$ are negative._

$$
\begin{align*}
b^x \cdot b^y &= \frac{1}{b^{-x}} \cdot \frac{1}{b^{-y}} \\\\
    &= \frac{1}{b^{-x} \cdot b^{-y}} \\\\
    &= \frac{1}{b^{-x - y}} && \text{(by Lemma 1.2)} \\\\
	&= \frac{1}{b^{-(x + y)}} \\\\
    &= b^{x + y} && \text{(by definition of exponentiation)}.
\end{align*}
$$

**Case 3.** _One or more of $x$, $y$ is 0._

Without loss of generality suppose $x = 0$. Then $b^x \cdot b^y = 1 \cdot b^y =
b^y$ which is equal to $b^{x + y} = b^{0 + y} = b^y$ as desired. $\square$
