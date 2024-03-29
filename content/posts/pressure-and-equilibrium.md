---
title: Pressure and Equilibrium
date: '2023-07-18'
summary: A mathematical explanation of the effect of changes in pressure on equilibrium position.
description: A mathematical explanation of the effect of changes in pressure on equilibrium position.
tags: [math, chemistry]
katex: true
---

Recently, while studying chemical equilibrium, I came across the following statement
in my textbook:

> An increase in pressure favours the side of an equilibrium reaction that has
> the smaller number of gas molecules.

Although there is a simple explanation for why this statement holds true using
Le Chatelier's principle, I thought it'd be a fun exercise to derive it
mathematically by comparison of the equilibrium constant $K_c$ and the reaction
quotient $Q$. (More importantly, writing this blog post provides me an excuse to
_not_ learn more chemistry and do math instead, which is always preferable.)

# Outline of Approach

Recall that if $Q < K_c$ then the products are favored and conversely if $Q >
K_c$ the reactants are favored. Thus, if we can somehow show that, in the
event of an increase in pressure, $Q$ is greater than $K_c$ if and only if
there are fewer moles of gas on the reactant side (and similar for the case
where $Q$ is smaller), then we'll have proven the desired claim.

# Proof

Consider the general reaction

$$
\ce{aA_{(g)} + bB_{(g)} + \dots <=> rR_{(g)} + sS_{(g)} + \dots}
$$

where $A$, $B$, $\dots$ are the reactants and $R$, $S$, $\dots$ are the
products.

Suppose the system is currently in equilibrium. Then the initial reaction quotient $Q_0$
and the equilibrium constant $K_c$ must necessarily be equal, so

$$
Q_0 = K_c = \frac{[R]^r[S]^s\cdots}{[A]^a[B]^b\cdots}. \tag{1}
$$

Our goal now is to relate concentration to the total pressure of the system, say $P_0$.
Recall that concentration $c = n/V$ where $n$ denotes the number of
moles and the $V$ the volume. Rearranging the ideal gas law $PV = nRT$ to
isolate $n/V$ yields

$$
\frac{n}{V} = \frac{P}{RT} = c. \tag{2}
$$

Note that we cannot directly substitute this back into Equation 1 yet as each
gas has its own partial pressure -- that is, the $P$ for each gas is different.
To account for this, recall that

$$
p_X = p_{\Sigma} \frac{n_X}{n_{\Sigma}}
$$

that is, the partial pressure is the total pressure scaled by the mole fraction.
Combining this with Equation 2 yields an expression for the concentration of
any gas (say $X$) in the reaction in terms of the total pressure of the system:

$$
c_X = [X] = \frac{p_X}{RT} = \frac{P_0n_{\Sigma}}{RTn_X} \tag{3}
$$

Substituting the final expression for concentration into Equation 1 and
factoring out the part dependent on pressure, we get

$$
\begin{align*}
Q_0 = K_c &= \cfrac{\left(\cfrac{P_0n_{\Sigma}}{RTn_R}\right)^r\left(\cfrac{P_0n_{\Sigma}}{RTn_S}\right)^s\cdots}{\left(\cfrac{P_0n_{\Sigma}}{RTn_A}\right)^a\left(\cfrac{P_0n_{\Sigma}}{RTn_B}\right)^b\cdots} \\\\
    &= \cfrac{{P_0}^{r + s + \dots}}{{P_0}^{a + b + \dots}} \cfrac{\left(\cfrac{n_{\Sigma}}{RTn_R}\right)^r\left(\cfrac{n_{\Sigma}}{RTn_S}\right)^s\cdots}{\left(\cfrac{n_{\Sigma}}{RTn_A}\right)^a\left(\cfrac{n_{\Sigma}}{RTn_B}\right)^b\cdots}. \tag{4}
\end{align*}
$$

(_Aside: Substituting the expression for concentration in terms of partial pressure gives us
a rather interesting result; see [Appendix 1](#appendix-1)._)

For brevity write
$$ \Delta n = \overbrace{(r + s + \cdots)}^{\text{tot. num of product moles}} - \underbrace{(a + b + \cdots)}\_{\text{tot. num of reactant moles}} \tag{5} $$
such that the
pressure factor in front is just ${P_0}^{\Delta n}$. Also put

$$
C = \cfrac{\left(\cfrac{n_{\Sigma}}{RTn_R}\right)^r\left(\cfrac{n_{\Sigma}}{RTn_S}\right)^s\cdots}{\left(\cfrac{n_{\Sigma}}{RTn_A}\right)^a\left(\cfrac{n_{\Sigma}}{RTn_B}\right)^b\cdots}
$$

so Equation 4 simplifies to just

$$
Q_0 = K_c = C{P_0}^{\Delta n}. \tag{6}
$$

Now consider what happens when the pressure is increased to $P_1$. The
equilibrium constant $K_c$ does not change since it is only affected by
temperature. What about the reaction quotient, $Q_1$? The factor $C$ from
Equation 6 remains the same, so the only change is replacing $P_0$ with $P_1$:

$$
Q_1 = C{P_1}^{\Delta n}.
$$

Evidently the reaction quotient $Q_1$ is no longer equal to the equilibrium constant,
so the equlibrium position will shift to restore equilibrium. To determine whether
the forward or reverse reaction will be favored, we just need to compare $Q_1$ to $K_c$.
Without loss of generality, consider the case where $Q_1$ is smaller:

$$
\begin{align*}
Q_1 &< K_c \\\\
CP_1^{\Delta n} &< CP_0^{\Delta n} \\\\
P_1^{\Delta n} &< P_0^{\Delta n}.
\end{align*}
$$

Since $P_1 > P_0$, this can only be the case if $\Delta n < 0$. But we defined $\Delta n$ as the
total moles of gas on the product side subtract the total moles of gas on the reactant side, so

$$
\begin{align*}
\Delta n &< 0 \\\\
\sum n_{\rm{products}} - \sum n_{\rm{reactants}} &< 0 \\\\
\sum n_{\rm{products}} &< \sum n_{\rm{reactants}}.
\end{align*}
$$

In other words, $Q_1 < K_c$ if and only if there are fewer moles of gas on the
product side. But $Q_1 < K_c$ also implies that the equilibrium position should
shift rightward (favoring products.) The analysis for the case in which there are
fewer moles of gas on the reactant side is similar -- the equilibrium position
shifts leftward favoring reactants, which is what we wanted to show. $\square$

## Appendix 1: Equilibrium Constant for Partial Pressures {#appendix-1}

As part of our proof, we derived the following relationship (Equation 3):

$$
c_X = [X] = \frac{p_X}{RT} = \frac{P_0n_{\Sigma}}{RTn_X}.
$$

Recall that we originally substituted the final expression,

$$
\frac{P_0n_{\Sigma}}{RTn_X}
$$

back into the equilibrium constant expression (leading to Equation 4). However,
if instead we substitute the expression

$$
\frac{p_X}{RT}
$$

then we get something rather intriguing:

$$
\begin{align*}
K_c &= \cfrac{\left(\cfrac{p_R}{RT}\right)^r\left(\cfrac{p_S}{RT}\right)^s\cdots}{\left(\cfrac{p_A}{RT}\right)^a\left(\cfrac{p_B}{RT}\right)^b\cdots} \\\\
    &= \frac{{p_R}^r{p_S}^s\cdots}{{p_A}^a{p_B}^b\cdots} (RT)^{(a + b + \dots) - (r + s + \dots)}.
\end{align*}
$$

Indeed, observe that at constant temperature, the factor
$$ (RT)^{(a + b + \dots) - (r + s + \dots)} $$
is constant. But if the temperature is constant $K_c$ must, too, be constant,
so that means the expression

$$
\frac{{p_R}^r{p_S}^s\cdots}{{p_A}^a{p_B}^b\cdots}
$$

is a constant as well! This expression may thus be viewed as a kind of
equlibrium constant, the difference being that it is calculated using partial
pressures instead of concentration. For this reason, it is often referred to as
the
[_equilibrium constant using partial pressures_](<https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Equilibria/Chemical_Equilibria/Calculating_An_Equilibrium_Concentrations/Calculating_an_Equilibrium_Constant_Using_Partial_Pressures>),
denoted $K_p$. The relationship between $K_c$ and $K_p$ is readily given by
isolating $K_p$ in Equation 7:

$$
\begin{align*}
K_c &= K_p (RT)^{(a + b + \dots) - (r + s + \dots)} \\\\
K_p &= K_c (RT)^{(r + s + \dots) - (a + b + \dots)} \\\\
K_p &= K_c (RT)^{\Delta n}
\end{align*}
$$

where $\Delta n$ is as defined in Equation 5.
