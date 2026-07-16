---
title: Perspectives on LLM-assisted development
date: '2026-07-14'
summary: Articles and posts about LLM-assisted development that I found interesting and are not slop, plus some of my opinions
tags: [llms]
---

Work in progress.[^1]

[^1]: I'm hoping to add my commentary on all the posts I link here eventually, but that may be a ways away.

This post collects various content about LLM-assisted development that I think contain interesting ideas and are written by humans, along with some of my own commentary. It is a bit disoganized: I have wanted to blog about my thoughts on the direction of the software development industry for some time, but have hemmed and hawed over how to phrase things. In the end, I decided that I should simply dump all my thoughts, for otherwise no blog would ever be written, and the result is this post.

## Prelude

I have conflicted thoughts on LLM-assisted development.[^2]

[^2]: I characterize myself as a skeptic that has warmed more to the concept (and actively use coding agents these days.) I'm sure that some folks will call me stuck in the past, and some will call me a once-promising programmer turned vibecoder. That's OK, although the polarization of discourse makes me sad.

Without doubt, there is a part of me that is saddened by the reduced need for writing code by hand. For many years, I enjoyed playing with and discussing the shape of the code that I write at a microscopic level. I took pleasure in learning trivia about the languages I use and closely following their development. There was a period in my life where, nearly every day, I would browse the open list of [TC39 proposals](https://github.com/tc39) and read through the discussion comments. What I am trying to articulate is that code is not merely a means to an end to me: I love the feeling of writing and polishing code.

Yet I also enjoy building things, and solving user problems. My first real open-source contributions (to a Discord bot called [YAGPDB](https://yagpdb.xyz)) were purely motivated by missing features that I wanted to use. The bot's codebase was in Go, a language totally foreign to me at the time, and I implemented my change purely by mimicking code that seemed related: copy, paste, tweak a few things until it did what I wanted. A LLM would probably have done a more thorough job :-) Later on, I did learn Go proper, but in large part my contributions remained rooted in user problems. After slogging through some support threads from users in the YAGPDB community Discord, I'd attempt to find patterns in the types of questions they raised, and repeat.

In this way, I think it's fair to claim that I am both a software craftsman and a builder. Historically--until early this year, perhaps--my position on LLMs and coding was split in two. With my craftsman hat on, I felt that I ought to reject LLM-assisted development, and feel only sadness about the direction of the industry. On the other hand, with my builder hat on, I felt that I should certainly try out LLM-assisted development. Yet whenever I did so I felt only frustration. The tool was slower than I imagined; it interrupted my train of thought; and it generated objective slop. I found it difficult to reconcile my experience with reports from respectable developers I follow.

It eventually became clear to me that I was missing some nuance about how to work with LLMs effectively, but what this was I could not tell. But whenever I attempted to learn how to work with LLMs in a more principled way by looking for posts and guides on the web, I was swamped by a deluge of clearly AI-generated content. When even the official OpenAI and Anthropic documentation is AI-generated with minimal signs of human intervention, what am I to do?

---

With these points in mind, the rest of this post attempts to do two things:

1. Collect _human-written_ posts that contain interesting ideas about LLM-assisted development (and offer some commentary.) I don't necessarily agree with all the positions in the linked posts, but I do think that they are worth reading, to inform your own thinking and improve your mental model of where LLMs can help you and where they cannot.

2. Argue that LLMs can benefit the software craftsman too--one who cares about the shape of the code need not necessarily despair and flee the industry.

## Jagged edges

The first thing I think one should appreciate about LLMs is that their output quality can have surprisingly high variance. There are "hard" problems that (to my surprise) the LLM does exceptionally well on, and conversely there are "easy" problems that (to my surprise, again) the LLM fails on.[^3]

[^3]: The difficulty levels in quotation marks are relative to my judgement. Maybe my hard problems are trivial to you.

If you don't believe this assertion, the spoiler below includes some examples in the first category: in other words, "hard" problems that LLMs did exceptional on. On the other hand, if you already agree that LLMs can surpass humans in various interesting settings, you'd better skip this section, because it will sound like advertising for the AI labs.

<details>

<summary>Show examples</summary>

- [OpenAI models conclusively beat world-class competitive programmers at algorithmic contests](https://x.com/FakePsyho/status/2075128093891801305).
- [OpenAI models conclusively beat world-class competitive programmers at heuristic contests](https://x.com/FakePsyho/status/2074814988389359691), with a [significantly shorter and simpler solution](https://x.com/FakePsyho/status/2074874368489148552)
- [Fable 5 identifies a massive performance improvement in a critical subsystem of the Ghostty terminal](https://github.com/ghostty-org/ghostty/pull/13209/)
- [Fable 5 ports Bun from Zig to Rust while seemingly improving user-facing product quality](https://bun.com/blog/bun-in-rust#bun-is-better-in-rust): the port is controversial (and the link goes to an Anthropic blog, which certainly should not be trusted on face value), but I have not seen evidence for the claim that, from an end user perspective, the Rust release of Bun was noticeably more buggy than the Zig version. I will remove this item if I receive credible information otherwise.

  To make it clearer what the achievement is to me: Fable 5 ported a massive Zig codebase (of questionable quality, admittedly) to a Rust codebase (of similarly questionable quality) faster and more cost-effectively than a human, without introducing more user-facing issues. This is interesting and impressive to me.

- [OpenAI models resolve a longstanding mathematical conjecture of sufficient importance that the result could be published in a top academic journal](https://openai.com/index/model-disproves-discrete-geometry-conjecture/): not related to programming, but as a wannabe mathematician I feel the need to include this :-)

</details>

To reiterate, the point of this section is as follows. I am _not_ arguing that LLMs can solve every hard problem (that would certainly be a reason to despair!) but rather that it definitely can solve hard problems, and that it's a bit tricky to see the pattern in which problems it can solve. Thus you should approach LLMs with an open mind; they may well surprise you occasionally instead of frustate you.

## How sane humans use LLMs

In this section, I collect some experience reports from sane human developers (so, most of the lunatics from my Twitter feed do not count) on LLM-assisted workflows.

- ["My AI Adoption Journey", Mitchell Hashimoto](https://mitchellh.com/writing/my-ai-adoption-journey)
  - Probably the first post that got me to question whether there is something legitimately interesting in the LLM-assisted development space. Mitchell's stellar technical reputation helped here.
  - I agree with the point that it is worth trying to replicate your work with LLMs for some time at the start, _even if_ it is excruciatingly slower than doing it by hand, to be able to build a good understanding of the tool. When I was going through this initial learning process myself, there were several times where--after finishing a Claude session with multiple rounds--I felt the irritating sense that I could have written this code a whole lot faster myself. Eventually you get a slightly better sense of what the tool is useful for, and the feeling goes away. Sometimes the feeling is just plain hubris too and an overestimate of how fast I can actually code.
  - The section on "outsourcing the slam dunks"--letting agents work away on tickets that you are almost certain they will complete successfully while you do other work--is very important to me. For some reason, at the start of my LLM-assisted development journey, I had this idea that the only way to work with LLMs was as a pair programmer, sitting there twiddling my thumbs and iterating with Claude. But if you still enjoy coding by hand, you don't have to give that up: you can still benefit by having background agents[^2] work away on some menial tasks, and review their output at your leisure. In this way you purely improve your throughput without losing much sanity.
- ["Agentic Coding Recommendations", Armin Ronacher](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)--note that this post is about a year old, and Armin states that he doesn't expect it to age well, but I think that there are some durable ideas
  - The advice on writing scripts for LLMs to use (and the specific recommendations Armin lists) still feels relevant to me. Though agents have gotten a whole lot more intelligent in the year since, reducing the number of intermediate commands that an LLM needs to run to test a change helps with context bloat and speeds up the process overall.
- ["Know thine enemy: A critical engagement with AI-assisted software development", Amy J. Ko](https://medium.com/bits-and-behavior/know-thine-enemy-a-critical-engagement-with-ai-assisted-software-development-e41d9b058ab1)
  - On the weaknesses of generative AI.
- ["Talk more to your coding agents", Will Jones](https://www.datawill.io/posts/2026-06-my-agent-workflow/)
- ["How I use LLMs as a staff engineer in 2026", Sean Goedecke](https://www.seangoedecke.com/how-i-use-llms-in-2026/)
- ["Artificial adventures", Jamie Brandon](https://www.scattered-thoughts.net/writing/artificial-adventures/)
- ["From a Luddite to a Vibe-Coder"](https://www.redpill-linpro.com/techblog/2026/03/20/from-luddite-to-vibe-coder.html)
  - Lots of AI-generated images, but the text seems human-written and is worth a skim, I think.

## LLMs can benefit craftsmen too

- ["Using AI to write better code more slowly", Nolan Lawson](https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/)
- ["The Short Leash AI Coding Method For Beating Fable", Greg Slepak](https://blog.okturtles.org/2026/07/short-leash-ai-method/)

## The future

- ["Rewriting Bun in Rust", Jarred Sumner](https://bun.com/blog/bun-in-rust)
  - No, I'm not saying that Bun is the future, and this post probably has Anthropic marketing's fingers on it. But there are some interesting, if brief, technical details about how dynamic workflows were used to port Bun in a more systematic way than "rewrite in Rust, make no mistakes!" that are worth reading.
- ["The Coming Loop", Armin Ronacher](https://lucumr.pocoo.org/2026/6/23/the-coming-loop/)
- ["In defense of not understanding your codebase", Sean Goedecke](https://www.seangoedecke.com/in-defense-of-not-understanding-your-codebase/)
- ["A new era for software testing", Salvatore Sanfilippo aka antirez](https://antirez.com/news/168)
- ["Control the ideas, not the code", Salvatore Sanfilippo](https://antirez.com/news/169)

## Tutorials for Claude, Codex, etc.

This section is about actually figuring out, mechanically, how to get started with your coding harness of choice (how it works, what the commands do, what the key terminology is.) Unfortunately I have not found a good introductory tutorial that is human-written... so there is some slop in this section, albeit somewhat useful slop.

- ["How to Build an Agent", Thorsten Ball](https://ampcode.com/notes/how-to-build-an-agent)
  - Not slop. Really great blog that shows the inner workings of an agentic coding harness (i.e., how you go from something like the original ChatGPT to something that can edit files and so on.)
  - It helped me build a better mental model for what `Claude|Codex|...` do under the hood, and why it's important to keep threads short when possible (to avoid quadratic scaling.) Also just plain interesting. You should have an idea of what your tools know under the hood.
- ["Agentic Engineering Patterns", Simon Willison](https://simonwillison.net/guides/agentic-engineering-patterns/)
  - Not slop. That said, it's not a tutorial per se and hence doesn't fit perfectly in this section. But it has some useful content.
- ["How I Use Every Claude Code Feature", Shrivu Shankar](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
  - The clanker definitely had a hand in the writing of this piece, but I'm pretty sure the human did too. And it's kind of useful!
- ["Best practices for Claude Code", Anthropic](https://code.claude.com/docs/en/best-practices)
  - Has that slop texture to it, but just hold your nose and tolerate it.
- If you want to skip the middleman, you can also just ask Claude or Codex or whatever you're using about specific commands and features of the harness. It's not bad.
