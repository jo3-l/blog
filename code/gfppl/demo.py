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
