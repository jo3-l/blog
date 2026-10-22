---
title: The algebraic structure of regular expressions
date: '2026-10-17'
summary: Converting NFAs to regular expressions by solving linear systems of equations
tags: [programming, math]
---

<!-- prettier-ignore-start -->

Consider the following non-deterministic finite automaton (NFA):

{{< figure src="/nfa.svg" alt="NFA with two states" width="450" align="center" >}}

From formal language theory, we know that NFAs are equivalent to regular expressions, in the sense that for every NFA there is a regular expression that recognizes the same set of strings as the NFA. So, **what is an equivalent regular expression for the NFA above?**

In this post, I'd like to share a rather peculiar method to answer such questions by solving a system of linear equations over regular expressions[^1]. Then, in order to justify this method rigorously, I'll discuss two different approaches to put an algebraic structure on regular expressions---namely, Kleene algebras and non-commutative power series.

[^1]: I first learnt this method from [Dr. Christian Urban](https://www.kcl.ac.uk/people/christian-urban)'s course on compilers and formal languages at KCL on exchange.

## A suspicious question

To the question, let $r_0$ be a regular expression that matches strings that end in state $Q_0$ when you run them through the automaton, and similarly let $r_1$ be a regular expression that matches strings ending in state $Q_1$. Although we don't know what $r_0$ and $r_1$ are yet---if we did, we'd be done!---we can write down some constraints that they ought to satisfy. For instance, from the NFA diagram, the only way to get to state $Q_0$ is if we haven't seen any characters yet (an empty string), or if we were previously in state $Q_1$ and saw the character $b$. In other words, the regular expression $r_0$ should match either the empty string, or $r_1$ followed by the character $b$.

Let's now agree on two conventions for writing regular expressions: instead of using | to denote alternation as in $r_1 |r_2$, we will instead write $r_1 + r_2$, and additionally we'll use $\mathbf{1}$ to denote the regular expression matching the empty string. We'll also agree that two regular expressions are equal if they match the same set of strings. Using these strange conventions, we get
$$ r_0 = \mathbf{1} + r_1 b \tag{1} $$
which says that $r_0$ matches either the empty string, or $r_1$ followed by the character $b$, as required. Similarly, for $r_1$, we have the equation
$$ r_1 = r_1 a + r_0 a. \tag{2} $$

We now throw caution to the wind completely and attempt to solve these equations algebraically, ignoring that we haven't the faintest clue what manipulations on these "regular expression equations" are legal or what laws they obey, if any.

By manipulating equation (2), we get
$$ r_1 - r_1 a = r_0 a \implies r_1(\mathbf{1} - a) = r_0 a \implies r_1 = r_0 a ({\mathbf{1} - a})^{-1}. $$
Everyone and their mother knows that $(\mathbf{1} - a)^{-1}$ is just the sum of the infinite geometric series $\mathbf{1} + a + a^2 + \cdots$. Alas, we can't have a regular expression of infinite length, but recalling that $+$ means alternation, the expression $\mathbf{1} + a + a^2 + \cdots$ seems like it matches all the strings that are the character $a$ repeated. But that's just the regular expression $a^*$! So:
$$ r_1 = r_0 a a^*. \tag{3} $$

Now substitute (3) into (1) to get $r_0 = \mathbf{1} + r_0 a a^* b$. By applying our questionable geometric series trick again,
$$ r_0 = (a a^* b)^*. $$
Substituting into (3) yields
$$ r_1 = \boxed{(a a^* b)^* a a^*} $$
and since $Q_1$ is the only accepting state of the automaton, this regexp should match exactly the strings that are accepted by the NFA. And it truly does! This is the right answer to the original problem (!)

What the hell just happened?

---

Somewhat surprisingly, it turns out that this method does work in general! However, to understand what's going on beneath the surface, we clearly first need to put some kind of _algebraic structure_ on regular expressions that allows us to manipulate them formally. The goal of the rest of this post is to build up to two sensible algebraic interpretations of regular expressions.

## Regular expressions revisited

To start, we should clarify what we mean by a regular expression: only basic features such as sequencing, alternation, and repetition ($*$) are permitted; fancy stuff like capturing groups, backreferences, and the like are all out of scope. Formally:

> **Definition (regular expression).** A _regular expression_ (regexp) is a recursive datatype given by one of the following cases:
> 
> - $\mathbf{1}$, matching the empty string
> - a literal symbol $c \in \Sigma$, where $\Sigma$ is a fixed alphabet of valid symbols
> - a sequence $r_1 \cdot r_2$ of two smaller regexps $r_1, r_2$; often we will omit the $\cdot$ symbol and just juxtapose the regexps
> - an alternation $r_1 + r_2$
> - or a repetition $r^*$.

(There's in fact one more case, which we'll get to later---in particular there is also such as a thing as $\mathbf{0}$; see the first paragraph of the next section.)

We declare two regexps to be equal when they match the same set of strings. Formally, we define recursively a function $\mathcal{L}(r)$ that returns the set of strings that $r$ matches: $\mathcal{L}(\mathbf{1}) = \{\epsilon\}$, $\mathcal{L}(r_1 + r_2) = \mathcal{L}(r_1) \cup \mathcal{L(r_2)}$, etc. (What should the definition for $\mathcal{L}(r_1 \cdot r_2)$ be?[^2]) Two regexps are then equal if $\mathcal{L}(r_1) = \mathcal{L}(r_2)$.

[^2]: After a bit of pondering one arrives at the definition $\{s_1 s_2 : s_1 \in \mathcal{L}(r_1), s_2 \in \mathcal{L}(r_2)\}$, where $s_1 s_2$ denotes the concatenation of strings $s_1$ and $s_2$.

As you have probably inferred, the object $\mathbf{1}$ and the operations $+$, $\cdot$ behave somewhat like their real number counterparts. Here's a non-exhaustive list of nice properties:

- addition is commutative: $a + b = b + a$, since both match either $b$ or $a$.
- $\mathbf{1}$ is the identity with respect to multiplication: $\mathbf{1} \cdot a = a$, since the left side means "match $\mathbf{1}$, then match $a$", and $\mathbf{1}$ matches the empty string.
- multiplication distributes over a sum: $a\cdot (b + c) = ab + ac$, since the left side means "match $a$, then either $b$ or $c$, which is the same as matching either $ab$ or $ac$".

There are some oddities, of course. For instance:

- everything is idempotent with respect to $+$: we have $r + r = r$ for all regexps $r$.
- we do not have multiplicative inverses in general.[^3]
- multiplication is not commutative: in general $r_1 \cdot r_2 \ne r_2 \cdot r_1$, since $r_1 \cdot r_2$ means to match $r_1$ followed by $r_2$ and the order matters.

[^3]: Consider the regexp $a$ matching the literal character $a$. Then, if $a^{-1}$ is a multiplicative inverse of $a$, we must have $$\mathcal{L}(aa^{-1}) = \{s_1 s_2 : s_1 \in \mathcal{L}(a), s_2 \in \mathcal{L}(a^{-1})\}$$
  and in particular this set cannot equal $\mathcal{L}(\mathbf{1}) = \{\epsilon\}$: the displayed set is either empty, or contains one or more strings starting with character $a$.

## Rings, semirings, and Kleene algebras

Perhaps you suspect at this point that the set of regular expressions $(R, +, \cdot)$ forms a (non-commutative) ring. One obvious issue is that we don't have an identity for addition; note that $\mathbf{1}$ is not neutral with respect to addition, since $\mathbf{1} + a$ matches both the empty string and $a$, not just $a$. This issue is easily remedied by adding a new object $\mathbf{0}$ that matches _no strings_ at all to the definition of regular expression. One can check that $\mathbf{0}$ is indeed neutral with respect to addition and possesses various properties that something called zero ought to.

Unfortunately, even with $\mathbf{0}$ the regular expressions do not have a ring structure for entirely trivial reasons. Indeed, additive inverses do not exist in general: given a regular expression $r$, what is $-r$? (One might be tempted to define it as the regular expression matching the complement of the language matched by $r$, but unfortunately this does not play well with our existing definitions.[^4])

[^4]: Every regular expression $r$ is idempotent with respect to $+$, since matching either $r$ or $r$ is the same as matching $r$; that is, $r + r = r$. If additive inverses exist, adding $-r$ then gives $r = \mathbf{0}$. But $r$ was arbitrary, so this says that the only regular expression is $\mathbf{0}$---no good!

Thus $(R, +, \cdot)$ is not a ring. However, one can actually check that the lack of additive inverses is the _sole_ obstruction to $(R, +, \cdot)$ being a ring. There is a name for structures that are almost rings but lack only additive inverses: _semirings_.

> **Definition (semiring).** A semiring $(R, +, \cdot)$ satisfies all the ring axioms, except that additive inverses need not exist.

> **Proposition.** The set of regular expressions $R$ equipped with alternation as addition $+$ and sequencing as multiplication $\cdot$ forms a semiring.

_Proof_. All the proofs in this post are left as exercises, partly because I am lazy :-) and partly because I think that the definitions and statements of results are more important than the proofs. $\square$

But this does not explain everything. In particular, we have not said how the star operation $r^*$ fits into the algebraic structure. If you recall how we "solved" the equation $r_1 = r_1 a + r_0 a$ by heuristically writing "$r_1 (1 - a) = r_0 a$" and then using a "geometric series expansion" to get $r_1 = r_0 a a^*$, it seems that the star operation acts as a kind of pseudoinverse.

The notion of a _Kleene algebra_ extends the notion of a semiring to include the $*$ operation.

> **Definition (Kleene algebra).** A Kleene algebra $(K, +, \cdot, *)$ is an idempotent semiring $(K, +, \cdot)$ with a unary operation $*$ such that
>
> - for all $a \in K$, we have $1 + a(a^*) \le a^*$ and $1 + (a^*)a \le a^*$,
> - for all $a, x \in K$, if $ax \le x$ then $a^*x \le x$, and if $xa \le x$ then $x(a^*) \le x$,
>
> where $x \le y$ means $x + y = y$.

For intuition about the definition of $\le$, observe that generally we may interpret $+$ in a semiring as a kind of union operation, and so $x + y = y$ is equivalent to $y$ "including" $x$. In the setting of regular expressions, we see that $r_1 + r_2 = r_2$ implies that $r_2$ matches all the strings that $r_1$ does (and potentially more).

> **Proposition**. The set of regular expressions $(R, +, \cdot, *)$ is a Kleene algebra.

In fact, regular expressions are the _prototypical_ example of a Kleene algebra; that is, Kleene algebras were introduced to study regular expressions!

In any case, from the defining axioms of a Kleene algebra, we can deduce the following

> **Lemma (Arden's lemma)**. In a Kleene algebra, $ba^*$ is the least solution of $x = xa + b$ with respect to $\le$.

which (under a mild technical condition) validates our original rule $r = p + rs \implies r = ps^*$ used to solve the system of regular expressions at the start of the post.

### The end of the story?

Kleene algebras are a cromulent and classical interpretation of regular expressions. Yet, one element of the Kleene algebra viewpoint that I personally find unsatisfying is that we originally "derived" the rule $r = p + r s \implies r = ps^*$ by heuristically manipulating $r - rs = r(1 - s) = p$, then multiplying by the inverse of $1-s$ and using a geometric series expansion to get $$r = p(1-s)^{-1} = p(1 + s + s^2 + \cdots) = ps^*.$$
From the viewpoint of Kleene algebras, even though the end result is justified by Arden's lemma and $*$ can be understood as a kind of pseudoinverse, the intermediate steps are nothing more than a heuristic and cannot be justified formally.

One would be excused for dismissing the argument above as nothing more than wishful thinking that chances upon the right answer---but in fact we _can_ make this argument fully rigorous in the right setting. In particular, by interpreting regular expressions as formal noncommutative power series or _formal power series over words_, the "inverse" of a regular expression exists in a larger ring. In the last section of this post I will outline this viewpoint and sketch nice proofs of existence and uniqueness of solutions.

## Formal power series over words

The motivation for this section is as follows: if you squint at a regular expression such as $x y + y x$, it looks uncannily like a power series in two variables $x$ and $y$. In fact, I claim this intuition is _perfectly valid_, and moreover it lets us subtract and invert things formally! The only sublety is that we need to work with a slightly exotic type of noncommutative power series[^5]. To this end, let's properly define what we mean by a _noncommutative power series_, also known as a _formal power series over words_.

[^5]: Or maybe noncommutative power series are a triviality to you. Who knows?

### Some definitions

We build up to the notion of a formal noncommutative power series from more familiar definitions.

> **Definition (formal power series in one variable)**. Let $R$ be a ring. Then $R[[X]]$ denotes the ring of formal power series $\sum_{n=0}^\infty a_n X^n$ in the indeterminate $X$ with coefficients in $R$.

> **Definition (formal power series in multiple commuting variables)**. Let $R$ be a ring. Then $R[[X_1, ..., X_r]]$ denotes the ring of formal power series $\sum_{k_1, \dots, k_r \ge 0} a_\mathbf{k} X_1^{k_1} \cdots X_r^{k_r}$ in $r$ commuting indeterminates $X_1, ..., X_r$ with coefficients in $R$.

By _commuting indeterminates_, we mean that we can freely interchange the order in a product: $X_1 X_2 X_1 = X_1 X_1 X_2 = X_1^2 X_2$. This allows us to rewrite any product of indeterminates in the canonical form $X_1^{k_1} \cdots X_r^{k_r}$.

If we drop this condition, and instead adjoin _non-commutative_ indeterminates, we naturally obtain the definition of formal noncommutative power series. We indicate noncommutativity by using angled brackets instead of square brackets: that is, in $R[[X_1, X_2]]$ the indeterminates $X_1$ and $X_2$ commute, whereas in $R\langle\langle X_1, X_2\rangle\rangle$ they do not.

Let's think about what the power series living in $R\langle\langle X_1, X_2\rangle\rangle$ look like. In particular, what form do individual terms take? In the commutative case each term had the form $c X_1^{k_1}X_2^{k_2}$, which does not distinguish between (say) $5 x_1 x_2 x_1 x_1$ and $5 x_1^3 x_2$. In the noncommutative case these terms are distinct, so we should instead think about terms having the form
$$ c X_{w_1} X_{w_2} \cdots X_{w_m} $$
where $w_1, \dots, w_m$ is a finite sequence of 1s and 2s. The term $x_1 x_2 x_1 x_1$ corresponds to $(1, 2, 1, 1)$, whereas $x_1^3 x_2$ corresponds to $(1, 1, 1, 2)$, which is a different sequence.

In this way, we see that the power series living in $R\langle\langle X_1, \dots, X_m\rangle\rangle$ are naturally indexed by _words_ (finite sequences) where each symbol is in $\{1,...,m\} =: \Sigma$, of the form $\sum_{\omega \in \Sigma^*} a_\omega X_\omega$. This leads us to the definition

> **Definition (formal power series on words)**. Let $R$ be a ring and $\Sigma$ be a finite alphabet of symbols. Then $R\langle\langle \Sigma \rangle\rangle$ denotes the ring of formal noncommutative power series $\sum_{\omega \in \Sigma^*} a_\omega X_\omega$.

and as a special case

> **Definition (formal power series in multiple noncommuting variables)**. Let $R$ be a ring. Then $R\langle\langle X_1, \dots, X_n \rangle \rangle$ denotes the ring of formal power series $\sum_{\omega \in \{1,\dots,n\}^*} a_\omega X_\omega$.

It took us a bit to arrive at the right definitions, but I hope that the scenic route we took above gives some intuition for why power series on words is a natural non-commutative generalization of regular power series.

> **Remark.** We can also see $R\langle\langle \Sigma \rangle\rangle$ as the set of functions $f : \Sigma^* \to R$ assigning each word a value in $R$. (Why is this equivalent?)

### Regular expressions are just power series

As alluded to earlier, regular expressions map to noncommutative power series over words in a natural way: for instance, we can think of

$$ r = a(a b + a c) = a a b+ a a c $$

as a noncommutative power series in indeterminates $a$, $b$, $c$ over $\mathbb{Z}$, where the coefficient on $a a b$ is $1$ and the coefficient on $a a c$ is also $1$. Note that the coefficients need not always be 0/1 in general: consider $a b + (c + a)b$, which expands to $a b + c b + a b = 2 a b + cb$. The coefficient $2$ on $ab$ counts the number of ways for the regular expression to match $ab$: see ${\color{red}ab} + (c + {\color{red}a}){\color{red}b}$. More generally, the coefficient on a word $\omega$ counts the number of distinct parse trees for $\omega$ (the number of different 'ways' for the regular expression to match $\omega$).

What is the analogue of the star operation in $\mathbb{Z}\langle\langle \Sigma\rangle\rangle$? It seems that we're a bit stuck now, but let's try the most naive definition possible: define $r^*$ as shorthand for the infinite sum $1 + r + r^2 + r^3 + \cdots$. The beauty is that this sum really does exist under some assumptions on $r$!

> **Theorem.** Let $R$ be a ring and suppose that $r \in R\langle\langle \Sigma \rangle\rangle$ has no constant term. Then $1 - r$ is invertible and moreover its inverse is $1 + r + r^2 + \cdots$.

With this in hand, we can define the correspondence between regular expressions and formal power series formally.

> **Definition (power series interpretation of regexp).** Let $R$ denote the semiring of regular expressions over $\Sigma$. Recall that $\mathbb{Z}\langle\langle \Sigma \rangle\rangle$ denotes the ring of formal power series on words over $\Sigma$.
>
> Define the _power series interpretation_ of a regular expression $r$, denoted $[r]$, by
>
> - $[\mathbf{0}] = 0$
> - $[\mathbf{1}] = 1$
> - $[r_1 + r_2] = [r_1] + [r_2]$
> - $[r_1 r_2] = [r_1] [r_2]$
> - $[r^*] = (1 - [r])^{-1}$ whenever $r$ does not match the empty string.
>
> Here $[\cdot]$ is a partial function $R \to \mathbb{Z}\langle\langle \Sigma \rangle\rangle$.

> **Theorem.** Let $r$ be a regular expression and suppose $[r]$ exists. Then the coefficient on each word $\omega \in \Sigma^*$ in $[r]$ counts the number of ways that $r$ matches $\omega$.

> **Corollary.** Let $r$ be a regular expression and suppose $[r]$ exists. Then the set of strings matched by $r$ is exactly the set of words with nonzero coefficient in the power series $[r]$.

The condition $r$ does not match the empty string in $[r^*]$ guarantees that $[r]$ has no constant term and hence $1 - [r]$ is invertible. Intuitively, when $r$ matches the empty string, we should not expect $r^*$ to have a well-defined power series interpretation since there are infinitely many ways for $r^*$ match the empty string, hence the constant term of $[r^*]$ must be $\infty$, which is not in $\mathbb{Z}$.

---

In the power series interpretation of regular expressions, the heuristic argument that we originally made has a completely rigorous interpretation in $\mathbb{Z}\langle\langle \Sigma \rangle\rangle$, since subtraction is well-defined and the geometric series expansion $(1-r)^{-1} = 1 + r + r^2 + \cdots$ is valid whenever $r$ has no constant term!

Working in $\mathbb{Z}\langle\langle \Sigma \rangle\rangle$ also permits us to prove that the system of linear equations arising from NFA to regexp conversion has a solution. Indeed, take a $\epsilon$-free NFA with states $Q_1, \dots, Q_n$, initial states $I$ and accepting states $F$. Define a row vector $\mathbf{u}$ by $u_i = 1$ if $Q_i \in I$ and $u_i = 0$ otherwise. Also define a $n \times n$ matrix by
$$ \textstyle A_{ji} = \sum_{c \in \Sigma\ : \ \text{exists transition } Q_j \xrightarrow{c} Q_i} c. $$
For instance, if the alphabet is $\{a, b\}$ and the NFA contains transitions $Q_1 \xrightarrow{a} Q_2$ and $Q_2 \xrightarrow{b} Q_2$, then $A_{12} = a + b$.

Each entry of $A$ is a nonempty sum of literal symbols (as there are no $\epsilon$-transitions), so $A$ has no constant term. Writing $\mathbf{r} = (r_1, \dots, r_n)$, the equations $r_i = u_i + \sum_j r_j A_{ji}$ produced by our method become the single matrix equation
$$ \mathbf{r} = \mathbf{u} + \mathbf{r} A. $$

We can then prove

> **Theorem (existence and uniqueness).** Let $A$ and $\mathbf{u}$ be as above. Then the system $\mathbf{r} = \mathbf{u} + \mathbf{r}A$ has a unique solution $\mathbf{r} \in \mathbb{Z}\langle\langle \Sigma \rangle\rangle^n$, given by
> $$ \mathbf{r} = \mathbf{u}(I_{n \times n} - A)^{-1} = \mathbf{u}(\mathrm{Id} + A + A^2 + \cdots). $$
> Moreover, the coefficient of a word $w$ in $r_i$ is the number of paths in the NFA that start in a state of $I$, read $w$, and end in $Q_i$. In particular, the words with nonzero coefficient in $\sum_{Q_i \in F} r_i$ are exactly the words accepted by the NFA.

The above result is not entirely complete, in the sense that it only guarantees a solution in $\mathbb{Z}\langle\langle \Sigma \rangle\rangle$, which may not correspond to a valid regular expression. Indeed, since the interpretation of a regular expression $[r]$ is the power series in which the coefficient on each word records the number of ways for $r$ to match the word, no power series with negative coefficients corresponds to a regular expression. One might then hope that every power series with non-negative coefficients corresponds to a regular expression, but this is not true either.[^6]

[^6]: Indeed, taking $\Sigma = \{a,b\}$, suppose that the power series $\sum_{n\ge 0} 1 \cdot a^nb^n \in \mathbb{Z}\langle\langle\Sigma\rangle\rangle$ corresponds to a regular expression $r$. The set of strings matched by $r$ must then be the set of words with nonzero coefficient in $[r]$, so that $r$ matches the language $\{a^nb^n : n\ge 0\}$---but this language is not regular.

In other words, only certain power series in $\mathbb{Z}\langle\langle \Sigma \rangle\rangle$ can be converted back into valid regular expressions. Let $\mathbb{N}^\text{rat} \langle\langle \Sigma \rangle\rangle$ denote the subsemiring of power series corresponding to valid regular expressions. It turns out that one can prove that the Gaussian elimination-like process we used to solve the original example problem stays in $\mathbb{N}^\text{rat} \langle\langle \Sigma \rangle\rangle$, which fills the gap in the result.

## Conclusion

There's lots more interesting things to say on this topic, but for now I will leave this post here---I hope it was a fun introduction to some more mathematical aspects of regular expressions. The ideas here are all quite classic, so let me conclude with a brief chronology:
- Kleene invented regular expressions in 1951;
- Schützenberger made the connection between automata and noncommutative power series in 1961;
- Arden proved that $x = xa + b$ has solution $x = ba^*$, also in 1961;
- Brzozowski popularized the linear system method to convert NFAs to regexps in his seminal 1964 paper on derivatives of regular expressions;
- and Kozen introduced the modern definition of Kleene algebra used in this post in 1991, though similar ideas were around earlier.

<!-- prettier-ignore-end -->
