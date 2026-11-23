---
title: Musings on using LLMs for learning
date: '2026-11-22'
summary: Some concrete examples of how I'm using LLMs to learn things in math and CS
tags: [math, programming, llms]
---

## Introduction

In this post, I want to describe some ways I've been using LLMs to aid in learning concepts across math and computer science, with various concrete examples of past conversations with LLMs I've had[^1]. I am interested in hearing about how others are using LLMs toward the same goal, so if you read this post I invite you to email me with your thoughts :-)

It's worth first considering whether LLMs should be involved in learning at all. I believe that some degree of friction is essential to learning: if everything is easy to you then either you are a supergenius or something is wrong. Consequently, in a perfect world with unlimited time, I believe that one should generally minimize the amount of external input while learning, for the often struggle is rewarded with very strong intuition. (Indeed, considering each of the examples I present below, I think you could reasonably argue that running through the same process without a LLM would have benefitted me more.) Alas, we live in an imperfect world where our time and patience to learn things is limited. By shortcutting select parts of the process with a LLM, the hope is that we can learn more using the same time and energy without sacrificing too much, if anything.

[^1]: The responses from the LLM shown in this post are lightly abridged (I have revised them to be more brief), but the content is essentially unchanged.

## Iterating on summaries of concepts

An indicator that someone understands a topic thoroughly is that they can offer a short summary that correctly explains the key points, yet can readily elaborate on any aspect when interrogated. More pithily, compression is intelligence. Motivated by this, one way I've been using LLMs is to try to poke holes in my attempted summary of [insert concept/paper/...], and also suggest any subleties that are missing. (Typically modern LLMs will poke holes and identify subleties without being explicitly prompted to do so.) Here are two examples.

1. I was trying to understand the usual formal semantics of while-loops in probabilistic programming languages.

   > **Me:** The characterization of a while-loop in Kozen's classical measure transformer semantics captures the intuition that unrolling it once does not change anything. That is, `while (cond) body` should have same semantics as `if (cond) { body; while (cond) body }`, and the characterization just writes this out as a fixed-point equation. Right?
   >
   > **LLM:** Right, but with one addition: the unrolling equation doesn't uniquely determine the loop in general, so the semantics takes the _least_ fixed-point solution.

2. I was trying to grok the paper ["Generating Functions Meet Occupation Measures: Invariant Synthesis for Probabilistic Loops"](https://arxiv.org/abs/2601.13991v1).

   > **Me:** Suppressing the details for a moment, the big idea seems just to be educated guessing of the posterior measure (the probability generating function after the while loop is accounted for, with a fixed input measure), and the key ingredient is a characterization of the while loop semantics with a fixed input measure (from which one can build a verification predicate). In particular the authors don't use Kozen's measure transformer semantics for loops since that characterization is 'second-order' in the sense that it doesn't mention the input measure. Is this the right idea?
   >
   > **LLM:** Yes, that's the right picture, with one correction that matters and two refinements. The correction: what gets guessed is the occupation measure $\nu$, not the posterior. Refinements: the algorithm is "guess the shape, solve for the rest", and the verification predicate needs more than the fixed-point equation because [...]

I think this kind of 'progressive disclosure' style of learning with LLMs is somewhat effective: first obtain a good high-level understanding, then (with LLM assistance) identify which details lie just one level lower and understand them, and repeat. LLMs are quite good at careful review, especially when one provides a baseline reference to compare against (for instance, a section of a textbook or a paper). Unfortunately, they are somewhat less effective at suggesting an optimal sequence of concepts for learning a subject, though their suggestions can be useful. In addition, in my opinion it is still important to try to write the summary yourself, since otherwise it is far too easy to convince yourself that you understand all the LLM output when the opposite is true.

## Exploring alternate proof methods

I've found LLMs to be very useful for exploring alternative proof methods for a result where the argument I currently have is unsatisfactory. By unsatisfactory, I mean that the argument seems unintuitive---not understanding the argument is a different issue and in such cases I endeavor to just keep thinking about it without LLM assistance until I understand it. LLMs can easily search through different proofs of the result and come up with new proofs that use only certain machinery (or, conversely, avoid certain machinery) on the fly as well.

Here are two examples.

1. I was trying to understand the intuition behind Axler's proof of countable subadditivity of the outer measure. I could easily follow the textbook argument line-by-line but it seemed like the essence was somewhat obscured. In particular, I could not clearly see the symmetry between the (easy) argument for _finite_ subadditivity and the (still easy, but slightly less so) argument for countable subadditivity. Indeed, in the finite case one can appeal to the general property that $\inf A + \inf B \le \inf (A + B)$ for arbitrary sets $A$, $B$, but the general proof Axler presents doesn't seem like it uses anything similar to this result at first glance.

   After a bit of thought I felt that the argument for the countable case could probably be recast using some kind of a generalization of this result on infimums. So I asked:

   > **Me:** Is this lemma true, false, or not well-formed? Only answer 'true'/'false'/'not well-formed' without providing a proof. Let $S_1, S_2, \dots$ be a sequence of sets. Then $$\sum_{n=1}^\infty \inf S_i = \inf\left\{\sum_{n=1}^\infty s_n : s_n \in S_n \text{ for all $n \in \mathbb{N}$}\right\}$$
   > in the extended reals.
   >
   > **LLM:** not well-formed
   >
   > **Me:** (after some thought) restrict the $S_i$'s to be non-negative nonempty
   >
   > **LLM:** true
   >
   > **Me:** (after some thought) Review my proof carefully: [a proof of countable subadditivity of the outer measure using my lemma]

   This example also illustrates the idea that one can "adjust the difficulty" (thereby retaining some degree of friction) when using LLMs to learn by explicitly constraining the form of the response.

2. I was reading Axler's argument that there exist disjoint subsets $A, B \subset \mathbb{R}$ such that $m^*(A \cup B) \ne m^*(A) + m^*(B)$, where $m^*$ denotes the outer measure. The argument is by contradiction and somewhat indirect in the sense that one does not really get a good sense of what the witness sets $A, B$ are other than that Vitali sets is involved. Rewriting the argument by contraposition does not help too much either.

   Thus I was motivated to ask a LLM first for a more direct example:

   > **Me:** Can we give a direct example of disjoint $A, B$ for which $m^*(A \cup B) \ne m^*(A) + m^*(B)$?
   >
   > **LLM:** Yes, a Bernstein set: choose $B \subseteq [0, 1]$ such that both $B$ and $[0,1]\setminus B$ meet every uncountable closed subset of $[0,1]$ using transfinite recursion. Then argue using the inner measure that $B$ and $[0,1] \setminus B$ forms a counterexample.
   >
   > **Me:** Is there an argument that does not use the inner measure?
   >
   > **LLM:** Yes, ...
   >
   > **Me:** What is the minimal background I need to construct a Bernstein set using transfinite recursion? What are some references for transfinite recursion and this construction?

   After digesting this counterexample I then returned to Axler's original argument using a Vitali set.

   > **Me:** [description of Axler's argument] Is there a way to extract a direct counterexample $A, B$?
   >
   > **LLM:** Yes, take $A = V$ and $B = [0,1]\setminus V$. [some standard argument that's not quite what I'm looking for]
   >
   > **Me:** Is there a slicker way of demonstrating that $m^*([0,1] \setminus V) = 1$?
   >
   > **LLM:** Yes, if you are able to use [...] and Steinhaus's theorem.
   >
   > **Me:** Is there a straightforward proof of Steinhaus' theorem if one only uses the outer measure?
   >
   > **LLM:**[^2] Yes, see Stromberg, "An elementary proof of Steinhaus's theorem", _Proc Amer. Math Soc. 36 (1972), p. 308_.

   [^2]: Originally the LLM just restated a variant of Stromberg's proof without attribution. I suspected it didn't come up with such a nicely worded proof on the fly, so asked for a citation upon which the LLM referred me to Stromberg. The attribution issue with LLMs is well and alive, I suppose.

   I then ran through this proof myself. It's quite elegant and perhaps I will clean up and post my notes on this someday.

## Building toy codebases to explore subjects

The final way that I am using LLMs for learning is somewhat computer-science specific and involves scaffolding a programming project in which I can play with toy examples, fill in the most important parts of the code myself, and see results easily, while leaving all other grunt project work to the LLM. It is easiest to explain using the example of my blog post on [building a compiler for a probabilistic programming language](https://jo3-l.dev/posts/probabilistic-programming/) using generating function. I[^3] wrote this post to better understand the papers ["Exact Bayesian Inference on Discrete Models via Probability Generating Functions"](https://arxiv.org/abs/2305.17058) and ["Compiling with Generating Functions"](https://dl.acm.org/doi/10.1145/3747534). After an initial read through, I realized that I really needed to play around with code and work through some more examples carefully myself. However, although both the papers come with code for their respective compilers, these codebases are not optimal playgrounds for learning: they are very featureful (whereas ideally one would start with a subset of features and build incrementally), somewhat optimized for performance, and written in a systems language (which obscures the underlying theoretical concepts).

[^3]: Just to be clear, all the prose in that blog post was written by hand. There is no LLM-generated text. However, some of the code is LLM-generated, as I describe below.

Thus I wanted to develop a small project that compiles a small, toy probabilistic programming language using the ideas in the papers. Moreover I wanted to run this compiler on a somewhat realistic statistical problem exercising most of the concepts in the two papers. However, I was not interested in writing all parts of this compiler; I only wanted to implement the compilation rules that lower AST nodes to generating functions. With LLMs, this was possible:

> **Me:** Can you come up with an interesting statistical modeling problem that is difficult to solve by hand but can be tackled with a PPL? I will then write a minimal 'compiler'/'interpreter' using this compiling-with-GFs idea. The problem should be such that it uses a reasonable range of ideas from the paper.
>
> **LLM:** [some initial idea that is too complicated]
>
> **Me:** What about a slightly simpler example that is more understandable at a glance? Let's give up on using all the paper's machinery.
>
> [some problem refinement]
>
> **Me:** How hard is this to solve by hand?
>
> **LLM:** [gives a direct solution]
>
> **Me:** Let's consider the following probabilistic program to solve this problem: [...] Suggest a sequence of implemetnation milestones that allows us to immediately compile simple statistical models at the start and builds up incrementally to the final result.
>
> [more back-and-forth]
>
> **Me:** Generate the frontend for this compiler.

I then derived all the compilation rules by hand, coded them up, and wrote the blog post. I think the result is a very accessible introduction to the idea of exact inference for probabilistic programming languages using generating functions. And it wouldn't exist without LLMs: the 'activation energy' required to find a suitable, nontrivial problem in statistics, solve it by hand, write the compiler frontend, ... before getting to what I actually want to do (think about compilation rules) is simply too high.

## Closing thoughts

As of late 2026 I find modern LLMs helpful for learning math and computer science; however, they are far from a silver bullet. In particular---and perhaps this is a contrarian opinion---I don't believe it is necssary to drastically restructure how math/CS are taught yet. The role of LLMs in learning for me as described here is largely similar to a highly available human expert (akin to a tutor or professor). The exception is the third technique (building toy codebases), which offers a markedly different approach to learning computer science than in the pre-LLM era. However, I have not used it enough to have an opinion on whether more computer science courses should adopt such a technique.

In any case, I hope this post left you with some ideas for how to integrate LLMs into your learning process if you desire, though many of the techniques I discuss are fairly trivial. I am also new to this strange era of machine intelligence in our pockets, so I am sure there are many more useful techniques yet to be disseminated.
