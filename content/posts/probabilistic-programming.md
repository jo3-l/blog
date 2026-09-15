---
title: Nuking stats problems with a probabilistic programming language
date: '2026-09-12'
summary: Writing a compiler for a probabilistic programming language using probability generating functions in 200 lines of Python, following "Compiling with Generating Functions" (Li and Zhang)
tags: [math, programming]
---

<!-- prettier-ignore-start -->

Consider the following contrived problem, which you might see in a particularly evil statistics textbook.

> A machine produces parts; the number $N$ made in a shift follows a $\mathrm{Poisson}(20)$ distribution. At the start of each shift the machine is recalibrated, and with probability 0.1 the calibration is off. When calibration is off, each part is defective with probability 0.6; when it's fine, 0.05.
>
> An inspector checks every part produced during a shift, rejecting a defective part with probability 0.9 and mistakenly rejecting a good part with probability 0.02. For one shift, you observe the number $R$ of parts the inspector rejected. Given that $R \ge 1$, how many defective parts do you expect were shipped that shift?

I don't know about you, but I would not be happy to see this problem on an exam.[^1]

[^1]: See the appendix directly above this footnote for a solution by hand.

But what if I told you that you could describe this problem declaratively in a programming language, and run it through a compiler that computes the right answer _exactly_ (notably, not an estimation using a Monte Carlo simulation)?

In this blog post, I will demonstrate how to write a compiler that takes the following _probabilistic program_

```ppl
n <- poisson(20)
miscalibrated <- bernoulli(0.1)

fn part(d) {
    defective <- bernoulli(d)
    rejected  <- if defective then bernoulli(0.9) else bernoulli(0.02)
    shipped   <- if rejected then 0 else defective
    (rejected, shipped)
}

(r, s) <- if miscalibrated then sum n { part(0.6) } else sum n { part(0.05) }

observe r != 0 # equivalently r >= 1
return s
```

and compiles it into a [_probability generating function (pgf)_](https://en.wikipedia.org/wiki/Probability_generating_function) that specifies the probability distribution of `s` exactly. The expectation of `s`, and thus the answer to the original problem, can be recovered straightforwardly given the pgf by taking derivatives. The whole compiler will fit in 200 lines of Python.

**References.** The implementation and all the ideas in this blog post follow the (very nice) paper ["Compiling with Generating Functions" (Li and Zhang)](https://dl.acm.org/doi/10.1145/3747534). Indeed, the compiler we shall implement is a small toy subset of the one described in that paper. All mistakes and oddities are mine, and I intentionally deviate from the paper in places for narrative simplicity. In addition, though I will give intuition for most mathematical results I need along the way via examples, I defer to the paper for all formal proofs.

### A high-level view of probablistic programming and compilers

In my opinion, the best way to interpret the program above is not as a series of procedural instructions that are executed repeatedly under different seeds. Rather, **the program is just syntax sugar for defining a particular exact statistical model** in a declarative way; such programs are called [probabilistic programs](https://en.wikipedia.org/wiki/Probabilistic_programming). The role of a compiler for such a program is to lower the program into a representation of the statistical model that allows one to easily query properties of the distribution, for example to answer questions such as "what is the probability of [given event] in this model" or "what is the expectation of this variable within the model?"

In the specific compiler we build in this post, we choose to represent the statistical model by the joint probability generating function of the variables involved. Each line of the probabilistic program manipulates the pgf in some way, for instance by extending it with a new random variable (potentially derived from some existing random variables) or conditioning on some event. The beauty of this approach is that every language construct can be implemented naturally as an operation on the probability generating function.

## Probability generating functions

First, let's review the definition of probability generating functions (pgfs). If one is familiar with the notion of the moment generating function or characteristic function of a distribution, the pgf can be viewed as an analogue that is particularly well-suited for discrete random variables.

Let $X$ be a discrete random variable with support in the non-negative integers $\{0, 1, ...\}$. The **probability generating function (pgf)** of $X$, denoted by $G_X(x)$, is defined by the series in which the coefficient of $x^k$ is the probability $P[X = k]$. That is,
$$ G_X (x) = P[X=0] + P[X=1]x^1 + P[X=2]x^2 + \cdots = \sum_{k=0}^\infty P[X = k]x^k. $$

**Example.** The pgf of a biased coin $X \sim \mathrm{Bernoulli}(0.7)$ is $0.3x^0 + 0.7x^1$.

The definition generalizes readily to multivariate random variables. Indeed, given a multivariate random variable $\mathbf{X} = (X_1, ..., X_n)$, the **multivariate probability generating function** of $\mathbf{X}$ is the series in $n$ variables $x_1, ..., x_n$ in which the coefficient of $x_1^{k_1} \cdots x_n^{k_n}$ is the joint probability $P[X_1 = k_1, \dots, X_n = k_n]$. That is,

$$
G_\mathbf{X} (x_1, ..., x_n) = \sum_{k_1, \dots, k_n \ge 0} P[X_1 = k_1, \dots, X_n = k_n]x_1^{k_1} \cdots x_n^{k_n}
$$

where the sum runs over the joint support.

Many properties of the original distribution can be recovered easily from the pgf; see [Wikipedia](https://en.wikipedia.org/wiki/Probability_generating_function#Properties). Since our original problem deals with expectations, let me show how to recover that property: on differentiating the pgf we find

$$
\frac{d}{dx} G_X (x) = \sum_{n=0}^\infty n x^{n-1} P[X = n],
$$

and in particular, evaluating at $x=1$ yields

$$
\left.\frac{d}{dx} G_X (x)\right|_{x=1} = \sum_{n=0}^\infty nP[X=n] = E[X].
$$

Thus, given the pgf $G_X (x)$ of a random variable $X$, the expectation of $X$ is given by $G_X'(1)$. Other moments of $X$ can be recovered similarly.

## Compiling with gfs

We are now ready to begin assembling our compiler. Let me reiterate the key idea: a probabilistic program is just a sequence of statements that build up a statistical model (roughly) line-by-line, and the statistical model is represented by the joint probability generating function of the current set of variables. A natural implementation strategy is to model each language construct as a rule that accepts the gf `e` representing the current statistical model, and transforms it to a new gf `e'`.[^2] In this section, we'll therefore build up little helpers to handle various constructs in our language incrementally, starting from variable declarations. (For simplicity we'll represent generating functions as sympy objects; a better implementation would roll their own optimized representation.) Then, after implementing all these rules, we'll write a small parser that accepts programs in the syntax of the original example and converts them to gfs by calling our helpers.

[^2]: The original paper refers to these functions as _gf transformers_.

### Declaring variables following Bernoulli, Poisson, and Dirac distributions

Let's start by implementing the rule for a statement of the form `y <- bernoulli(theta)`, introducing a new random variable `y` sampling from a Bernoulli distribution of constant parameter $\theta$. We need to write a function that, given the old gf, returns a new gf including the newly declared variable `y`.

To do so, we require two facts about pgfs:

- the pgf of a $Y \sim\mathrm{Bernoulli}(\theta)$ distribution is $P[Y=0] + P[Y=1]y = (1-\theta) + \theta y$;
- if $X$ and $Y$ are independent with pgfs $G_X$ and $G_Y$ respectively, then the pgf of $(X, Y)$ is $G_X(x) G_Y (y)$.

    **Proof.** I'll give a proof of this second claim that illustrates a useful general formulation of pgfs. One can check that, by definition,
    the pgf of $X$ is $G_X (x) = E_X [x^X]$, the pgf of $Y$ is $G_Y (y) = E_Y [y^Y]$, and the joint pgf of $(X, Y)$ is
    $G_{XY} (x, y) = E[x^X y^Y]$. Since $X$ and $Y$ are independent, the last expectation splits as $G_{XY} (x, y) = E[x^X] E[y^Y]$.
    The result follows. $\square$

Applying these facts in our setting, since `y` is a new random variable independent from all the existing variables in the base statistical model `e`, the new gf `e'` is just given by multiplying `e` with the pgf of `y`. This gives rise to the following implementation of `bernoulli(y, theta)`, which returns a function that transforms the gf in the correct fashion:

```py
import sympy as sp

def bernoulli(y, theta): # y is a sympy variable
    """y <- bernoulli(theta)."""
    return lambda e: e * (1 - theta + theta * y)
```

We can implement an analogus rule for declaring a variable following a Poisson distribution. If $Y \sim \mathrm{Poisson}(\lambda)$, a direct computation shows that the pgf $G_Y (y) = \exp(\lambda (y - 1))$, and thus

```py
def poisson(y, lambda_):
    """y <- poisson(lambda)."""
    return lambda e: e * sp.exp(lambda_ * (y-1))
```

Finally, for good measure, we ought to also add support for declaring constant variables (for instance, `y <- 5`), which we can interpret as a Dirac distribution: if $Y \leftarrow c$ a constant, then $Y$ takes on the value $c$ with probability $1$. The pgf in this case is therefore $G_Y (y) = \sum_{k \ge 0} P[Y = k] y^k = y^c$, and hence

```py
def const(y, c):
    """y <- c."""
    return lambda e: e * y**c
```

**Example.** Using these rules, we can already express some (completely trivial) statistical models. Let's write a short helper that runs a sequence of transformers and returns the resulting generating function:
```py
def to_gf(*ts):
    # start with the trivial gf representing empty statistical model with no variables,
    # and one outcome with probability 1
    e = sp.Integer(1)
    for transformer in ts:
        e = transformer(e)
    return e 
```

The following snippet effectively declares two independent variables $X \sim \mathrm{Bernoulli}(0.5)$ and $Y \sim \mathrm{Bernoulli}(0.3)$, and says that the joint pgf of $(X, Y)$ is $(0.5x + 0.5)(0.3y + 0.7)$, as it should.

```py
>>> x, y = sp.symbols('x y')
>>> to_gf(bernoulli(x, 0.5), bernoulli(y, 0.3))
(0.5*x + 0.5)*(0.3*y + 0.7)
```

### Conditional distributions

With variable declarations out the way, we're ready to move on to something more interesting: describing conditional distributions. First, let's implement conditioning on events of the form $\{X \ne 0\}$ and $\{X = 0\}$. For instance, the program
```ppl
X <- poisson(10)
observe X != 0
```
describes the conditional probability distribution $X \mid X \ne 0$. How should the generating function change upon encountering such a statement? For intuition, let's work out exactly the case above by hand. Let $G(x)$ denote the (unconditional) pgf of $X$. We are interested in deriving the conditional pgf of $X \mid X \ne 0$ from $G$. Call this conditional pgf $G_\mathrm{cond}$; by definition,
$$
\begin{align*}
G_\mathrm{cond} (x) &= \sum_{k \ge 0} P(X = k \mid X \ne 0) x^k \\
&= \sum_{k \ge 0} \frac{P(X = k \text{ and } X \ne 0)}{P(X \ne 0)} x^k \\
&= \frac{1}{P(X \ne 0)} \sum_{k \ge 1} P(X = k) x^k.
\end{align*}
$$
Now, recall that the original unconditional pgf $G(x) = \sum_{k \ge 0} P(X = k)x^k$. One sees that $P(X = 0) = G(0)$ and $P(X \ne 0) = 1 - G(0)$, and moreover $\sum_{k \ge 1} P(X = k)x^k = G(x) - G(0)$. Therefore
$$
G_\mathrm{cond} (x) = \frac{1}{1 - G(0)} (G(x) - G(0)). 
$$

In other words, we kill off the terms corresponding to the event $X = 0$, and then rescale to ensure that the probabilities still sum to 1[^3]. The general case is analogous: compute $G - G|_{X=0}$ and then rescale accordingly.

[^3]: It's also possible to not rescale intermediate gfs during compilation (allowing unnormalized measures). The original paper takes this approach, and in a production implementation one would certainly want this optimization, but for simplicity I'll work only with normalized measures in this post.

```py
def total_mass(e):
    return e.subs({v: 1 for v in e.free_symbols})

def observe(x):
    """observe x != 0."""
    def transform(e):
        survivors = e - e.subs(x, 0)
        return survivors / total_mass(survivors)
    return transform
```

Similarly, we have the dual

```py
def observe_zero(x):
    """observe x == 0."""
    def transform(e):
        survivors = e.subs(x, 0)
        return survivors / total_mass(survivors)
    return transform
```

Continuing with this idea, we next implement if-else conditional statements of the form

```ppl
...
x <- if y then e1 else e2
```

which declares that `x <- e1` if `y` is nonzero, and `x <- e2` otherwise. The idea is surprisingly simple. Imagine compiling two separate programs conditioning on the cases $Y \ne 0$ and $Y = 0$ respectively:
```ppl
...
observe y != 0
x1 <- e1
```
and
```ppl
...
observe y = 0
x2 <- e2
```
Using what we've implemented already, we can compute the conditional pgf $G_\mathrm{then}$ of $X \mid Y \ne 0$ and the conditional pgf $G_\mathrm{else}$ of $X \mid Y = 0$. Then the pgf of $X$ is just the sum of $G_\mathrm{else}$ and $G_\mathrm{then}$ scaled appropriately using the law of total probability:
$$
G = P[Y \ne 0]\, G_\mathrm{then} + P[Y = 0]\, G_\mathrm{else}.
$$
This gives the following rule, in which `then` and `else_` are the transformers compiled from `e1` and `e2` respectively (both writing into the same new variable `x`):

```py
def if_(y, then, else_):
    """x <- if y then e1 else e2 (`then`, `else_` are the transformers for `x <- e1`, `x <- e2`)."""
    def transform(e):
        p_zero = total_mass(e.subs(y, 0))   # P[Y = 0]
        g_then = then(observe(y)(e))        # pgf of ..., X | Y != 0
        g_else = else_(observe_zero(y)(e))  # pgf of ..., X | Y == 0
        return (1 - p_zero) * g_then + p_zero * g_else
    return transform
```

### Summing iid variables

We are, in fact, nearly finished the implementation of the language rules necessary to compile the original program! Only one major construct remains, namely the `sum n { body }` that sums `n` iid variables following the probability distribution specified by `body`. For instance,

```ppl
X <- poisson(10)
Y <- sum X { bernoulli(0.5) }
```
declares $Y = B_1 + \cdots + B_X$, where $B_i \sim \mathrm{Bernoulli}(0.5)$ iid and $X \sim \mathrm{Poisson}(10)$. In particular $Y \mid X \sim \mathrm{Binomial}(X, 0.5)$.

As usual, for intuition, let's work out the joint pgf of $(X, Y)$ in this case. We first recall the following easy results:
- if $X$ and $Y$ are independent, then the pgf of $X + Y$ is $G(x) = G_X (x) G_Y (x)$;
- by induction, if $X_1, \dots, X_n$ are iid with pgf $G_1 (x)$, then the pgf of $X_1 + \cdots + X_n$ is $G(x) = G_1(x)^n$.

Using these results, we can compute the joint pgf of $(X, Y)$ in the example above by conditioning on $X$, the number of iid copies:
$$
\begin{align*}
G(x, y) &= \sum_{n \ge 0} \sum_{k \ge 0} P[X = n, Y = k] x^n y^k \\
&= \sum_{n \ge 0} \sum_{k \ge 0} P[Y = k \mid X = n]P[X = n] x^n y^k \\
&= \sum_{n \ge 0} P[X = n]x^n \left(\sum_{k \ge 0} P[Y = k \mid X = n]y^k \right) \\
&\stackrel{(*)}{=} \sum_{n \ge 0} P[X = n]x^n G_\mathrm{bern}^n (y) \\
&= \sum_{n \ge 0} P[X = n]\, (x G_\mathrm{bern} (y))^n \\
&= G_X (x G_\mathrm{bern} (y)).
\end{align*}
$$
(*) follows since $Y \mid X = n$ is distributed as the iid sum of $n$ $\mathrm{Bernoulli}(0.5)$ variables by definition, so has pgf $G_\mathrm{bern}^n(y)$ by the earlier result.

This example suggests that the joint pgf is the original pgf with the count variable $x$ replaced by $x G_{\mathrm{body}}$, where $G_{\mathrm{body}}$ denotes the pgf of the body of the loop. Thus we get

```py
def sum_(n, body):
    """y <- sum n { body } (`body` is the transformer for `y <- body`)."""
    def transform(e):
        body_gf = to_gf(body)
        return e.subs(n, n * body_gf)
    return transform
```

### A short example

We are done with all the language rules that compile program fragments to generating functions. Before we write a parser and wire everything up, let me demonstrate that the rules already do something useful when called by hand. Here's an easier (but still contrived) problem that uses all of them at once:

> A hen lays a $\mathrm{Poisson}(6)$ number of eggs. On a rainy day, which happens with probability $0.3$, each egg hatches with probability $0.2$; otherwise each egg hatches with probability $0.5$. You come back and find that at least one chick has hatched. What is the probability that it rained?

In our language, this is

```ppl
rainy  <- bernoulli(0.3)
eggs   <- poisson(6)
chicks <- if rainy then sum eggs { bernoulli(0.2) }
                   else sum eggs { bernoulli(0.5) }
observe chicks != 0
```

and calling the rules directly as follows yields the joint pgf of $(\text{rainy}, \text{eggs}, \text{chicks})$ conditioned on $\text{chicks} \ne 0$:

```py
>>> r, n, c = sp.symbols('r n c')
>>> e = to_gf(
...     bernoulli(r, sp.Rational(3, 10)),
...     poisson(n, 6),
...     if_(r, sum_(n, bernoulli(c, sp.Rational(1, 5))),
...            sum_(n, bernoulli(c, sp.Rational(1, 2)))),
...     observe(c),
... )
>>> print(sp.simplify(e))
(-3*r*exp(24*n/5) + 3*r*exp(6*n*(c + 4)/5) - 7*exp(3*n) + 7*exp(3*n*(c + 1)))/(-3*exp(24/5) - 7*exp(3) + 10*exp(6))
```

We are interested in $P[R = 1]$. To obtain the marginal pgf of $R$ from the joint, we set $n = c = 1$. The desired probability $P[R = 1]$ of rain is then given by the coefficient on $r$:
```py
>>> posterior = sp.expand(sp.simplify(e.subs({n: 1, c: 1})))
>>> sp.N(posterior.coeff(r, 1))
0.239647855425313
```

Observing that some eggs hatched is evidence against rain (rain makes hatching less likely), so the posterior probability $0.24$ has dropped from the prior $0.3$, as one would hope.

All that remains now is to write a parser so that we don't have to call the rules by hand, and finally tackle the original problem.

### Wiring everything up

The frontend for the compiler is bog-standard, so I will elide most of the details. The full code is available [on my GitHub](https://github.com/jo3-l/blog/tree/main/code/gfppl) and fits in <200 lines of code, as promised in the post title. We use [parsy](https://github.com/python-parsy/parsy), a Python parser combinator library, to first parse the source program into a top-level `Block` structure containing a list of statements. 

```py
type Stmt = VarDecl | ObserveNonzero | ObserveZero | Return | FnDecl
type Expr = VarRef | FnCall | NumLit | Tuple | IfThen | Sum

@dataclass
class Block: # { stmts... result } (result is the block's value, if any)
    stmts: list[Stmt]
    result: Expr | None = None
```

Then it suffices to recursively walk through the list of statements and call the rules defined earlier, maintaining a set of live variables and the current generating function as we go. Here's a heavily abridged version that illustrates the general idea and structure (again, gory details on the GitHub).

```py
type GF = sp.Expr
type Env = dict[str, sp.Expr]  # name -> sympy symbol or constant

def compile(prog: Block) -> tuple[GF, sp.Symbol | None]:
    """Return (pgf of the returned variable, its symbol)."""
    fns: dict[str, FnDecl] = {}
    ret: sp.Symbol | None = None

    def lookup(x: NumLit | VarRef, env: Env) -> sp.Expr:
        """Look up the value of `x` in `env` as a sympy expression."""
        return x.val if isinstance(x, NumLit) else env[x.name]

    def run(stmts: list[Stmt], env: Env, e: GF) -> GF:
        """
        Evaluate the list of statements in order,
        and return the resulting gf.
        """
        for s in stmts:
            match s:
                # other cases elided
                case VarDecl(bindings, expr):
                    ys = [sp.Dummy(b) for b in bindings]
                    e = bind(ys, expr, env, e)
                    env.update(zip(bindings, ys))
        return e

    def block(b: Block, env: Env, ys: list[sp.Symbol], e: GF) -> GF:  # ys <- { b }
        """
        Evaluate the statements within the block in order
        and bind the results to ys.
        """
        local = env.copy()
        return bind(ys, b.result, local, run(b.stmts, local, e))

    def bind(ys: list[sp.Symbol], x: Expr, env: Env, e: GF) -> GF:  # ys <- x
        """
        Evaluate the expression x and bind the results to ys.
        """
        match x:
            # other cases elided
            case IfThen(cond, then_, else_):
                g_then = lambda e: block(then_, env, ys, e)
                g_else = lambda e: block(else_, env, ys, e)
                return if_(env[cond.name], g_then, g_else)(e)

    e = run(prog.stmts, {}, sp.Integer(1))
    return marginalize(e, e.free_symbols - {ret}), ret
```

## Solving the problem

At last, we can enjoy the fruits of our labor.

```py
import sympy as sp
from gfppl import compile, parse


def expectation(e, x):
    """E[X] = G_X'(1)."""
    return sp.diff(e, x).subs(x, 1)


PROG = """
n <- poisson(20)
miscalibrated <- bernoulli(0.1)

fn part(d) {
    defective <- bernoulli(d)
    rejected  <- if defective then bernoulli(0.9) else bernoulli(0.02)
    shipped   <- if rejected then 0 else defective
    (rejected, shipped)
}

(r, s) <- if miscalibrated then sum n { part(0.6) } else sum n { part(0.05) }

observe r != 0 # equivalently r >= 1
return s
"""

gf, s = compile(parse(PROG))
print("pgf of s:", sp.simplify(gf))
print("E[s | r >= 1] =", sp.N(expectation(gf, s)))
```

We get

```
pgf of s: (9*exp(_s/10 - 69/50) - 9*exp(_s/10 - 1/10) + exp(6*_s/5 - 304/25) - exp(6*_s/5 - 6/5))*exp(274/25)/(-10*exp(274/25) + 1 + 9*exp(242/25))
E[s | r >= 1] = 0.246710146687313
```

and the second line gives us the long-coveted answer: we expect $0.247$ defective parts to be shipped during the shift. The moral of the story is: several days of toiling away with generating functions and sympy is preferable to half an hour of manual computation to solve a contrived stats problem. Wait, hold on...

## Conclusion

Writing this blog post has convinced me that probabilistic programming languages are incredibly useful tools for statistical modeling---jokes on wasted implementation time aside, if you compare with the [manual solution](#appendix-solving-the-problem-by-hand) in the appendix, I think it is indisputable that the probabilistic program is far preferable: it is easy to write and to modify for any future changes. Assuming that the compiler is correct, it is also easy to check that the program describes a statistical model that matches the problem statement.

I find the implementation here using generating functions particularly delightful, and if you feel the same way, I strongly recommend that you read [Li and Zhang's original paper](https://dl.acm.org/doi/10.1145/3747534). It provides rigorous proofs as opposed to all my handwaving here, in addition to describing how to implement many more language constructs than the subset I have here. Generating functions are of course far from the only way to implement a compiler for a probabilistic programming language compiler; there are many other compiliation strategies in the literature with different tradeoffs, and the paper offers a nice comparison.

In the end, I hope you enjoyed implementing this odd compiler and working through wacky pgf computations as much as I did. It was a ton of fun!

## Appendix: solving the problem by hand

**LLM usage statement.** This solution is due to Fable 5.1. I was not clever enough to come up with the main trick myself. (That's kind of the point of the blog post---I don't need to be that clever with a probabilistic programming language in hand!) I verified the correctness and then rewrote the argument for clarity.

The problem is a nightmare to do by hand without the following fact about Poisson distributions:

**Lemma.** (Splitting property of Poisson distributions) Let $X \sim \mathrm{Poisson}(\lambda)$ be a Poisson distribution, and suppose that each event falls independently into one of $k$ bins with probability $p_1, \dots, p_k$ respectively ($p_1 + \dots + p_k = 1$). Let $X_1, \dots, X_k$ be the number of events in each bin respectively. Then the $X_i$'s are independent and each follows a Poisson distribution $X_i \sim \mathrm{Poisson}(\lambda p_i)$ (i.e., $X$ _splits_ into multiple Poisson distribution).

**Proof.** Induct on the result of [this Math Stack Exchange post](https://math.stackexchange.com/q/1777427/1674765).

In view of this lemma, the idea is relatively simple. Condition on the calibration state $C$, so that the defect probability $d$ is fixed: $d = 0.6$ when $C$ is off and $d = 0.05$ otherwise. Each of the $N \sim \mathrm{Poisson}(20)$ parts then falls independently into one of three bins: rejected with probability $p_R = 0.9d + 0.02(1-d)$, shipped and defective with probability $p_S = 0.1d$, or shipped and fine with the remaining probability. Letting $R$ and $S$ be the counts in the first two bins, the splitting property gives
$$ R \sim \mathrm{Poisson}(20 p_R), \quad S \sim \mathrm{Poisson}(20 p_S) $$
with $R, S$ independent. We seek the expectation $E[S \mid R \ge 1]$.

Writing the desired conditional expectation as a ratio and conditioning on $C$ gives
$$
E[S \mid R \ge 1] = \frac{E[S \cdot \mathbf{1}\{R \ge 1\}]}{P[R \ge 1]}
= \frac{\sum_c P[C = c]\; E[S \cdot \mathbf{1}\{R \ge 1\} \mid C = c]}{\sum_c P[C = c]\; P[R \ge 1 \mid C = c]}.
$$
Given $C = c$, the variables $S$ and $R$ are independent, so the expectation in the numerator factors as $E[S \mid C = c]\, P[R \ge 1 \mid C = c]$. Conditional on $C$, both $R$ and $S$ are (by the argument of the first paragraph) Poisson distributions with known parameter. Direct computation yields
$$
E[S \mid R \ge 1] = \frac{0.9 \cdot 0.1\,(1 - e^{-1.28}) + 0.1 \cdot 1.2\,(1 - e^{-10.96})}{0.9\,(1 - e^{-1.28}) + 0.1\,(1 - e^{-10.96})} \approx 0.2467,
$$
agreeing with the result of our program.

<!-- prettier-ignore-end -->
