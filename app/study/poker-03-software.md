---
title: "Poker 03 — Modern Poker Software"
summary: "Modern Poker Theory ch. 3: equity calculators, range analysis tools, EV decision trees, pre-flop Nash calculators, AI vs solvers, Nash distance, PioSOLVER, MonkerSolver and GTO training apps."
order: 103
audience: bravosierra99
---

# Poker 03 — Modern Poker Software

*Study guide to Chapter 3 of* Modern Poker Theory *(Michael Acevedo). A short
chapter: a tour of the tool classes used to study the game. The product names
matter less than knowing **what question each class of tool can answer, what it
assumes, and where its output stops being trustworthy**.*

## The toolbox at a glance

| Class | Example | Answers | Does not answer |
|---|---|---|---|
| **Equity calculator** | Power Equilab (PokerStove was the ancestor) | How much equity does a hand/range have vs a hand/range? | EV, or what to do |
| **Range analysis tool** | Flopzilla | How does a range hit a board, by hand category? | EV, or what to do |
| **EV decision tree** | CardRunners EV (CREV) | What is the EV of each action, *given the ranges and strategies I typed in*? | What villain's strategy actually is |
| **Pre-flop Nash calculator** | Holdem Resources Calculator (HRC) | What are the equilibrium push/fold ranges? | Anything involving post-flop play |
| **Self-play AI** | PokerSnowie | What does a strong self-taught bot do here? | Whether that is verifiably GTO; how to exploit |
| **GTO solver** | PioSOLVER, MonkerSolver | What is the equilibrium for this tree, and how close to equilibrium is it? | Anything outside the tree you built |
| **GTO training app** | GTO Poker | What does a pre-solved expert solution say? | Custom spots, custom sizes, exploits |

The classes run from "pure arithmetic, you supply all the thinking" to "full
strategy output, you supply the tree". The further along, the more the result
depends on the setup.

## Equity calculators

The most basic and most essential tool: hand vs hand, hand vs range, range vs
range. Modern ones add equity graphs, heatmaps and some range analysis.

- **Good at:** quick, intuitive range entry; fast results; **multiway** equities; custom playability profiles.
- **Limits:** only equity and simple maths. **No EV and no strategic advice**, and only shallow post-flop range analysis.

Why the limit matters: equity assumes the hand is checked down. It ignores
betting, so it ignores equity realization (ch. 1) — a calculator tells you your
share of the pot at showdown, not whether a call or bet makes money.

## Range analysis tools

Enter a range and see how it connects with any flop, split into categories: top
pair, sets, straights, flush draws, backdoor draws and so on.

- **Good at:** equity **per combo**; studying **card removal**; filtering a range by hand category and carrying it across turns and rivers; fast and simple.
- **Limits:** again **no EV or advice**; can't build complex decision trees; mostly a **heads-up** tool; little use **pre-flop**.

Use it to answer "how often does this range have top pair or better / a draw /
nothing on this texture?" — the raw material for judging who has range and nut
advantage.

## EV decision trees

You build a tree of player actions and the tool computes the EV at every
decision point.

- **Good at:** reports equity **and EV** per action; pre-flop and post-flop; multiway; thorough range filtering; **MES** (maximally exploitative strategy) calculations; **ICM** for SNG/MTT final tables; can include **bounties and rake**; accounts for **card removal and bunching**; scripting to automate work.
- **Limits:** you must enter **everything** — each player's range at every node, pot, bet and raise sizes, stack depths. Building trees is slow, the learning curve is steep, and above all it **needs villain's full strategy, or assumptions in its place**.

That last point is the key idea: an EV tree does not find a strategy, it
**evaluates** one. The EV it reports is only as good as the ranges you assumed.
That makes it the natural tool for exploitative work ("if this player folds X%
here, what is my best response?") and a poor one for discovering equilibrium.

## Pre-flop Nash calculators

Before solvers these were the standard MTT/SNG tool. They approximate
equilibrium **push/fold** strategies and are at their best with **shallow
stacks where nobody has a calling (flatting) range** — every decision is
all-in or fold, so no post-flop play needs modelling.

- **Good at:** unexploitable shoves and calls; fast; pre-flop MES; strategies with EV; bounties; **ICM and FGS** (Future Game Simulation); final tables.
- **Limits:** **no post-flop play**; no card-removal or bunching effects.

**Why they break at deeper stacks.** Once stacks are deep enough for non-all-in
raises, the calculator has to apply an *action abstraction*, and both available
ones bias the answer:

| Abstraction | Who it helps | Distortion |
|---|---|---|
| **Remove the option to call** a non-all-in raise | The raiser — defenders can only shove or fold, so they play tighter | **Opening ranges come out too wide**, and tilted toward good **blockers** while ignoring post-flop **playability** |
| **Allow calls, then check the hand down** | The caller — marginal hands realize **100% of their equity** | **Calling ranges come out too wide** |

Either way the pre-flop strategy is wrong, so trust these tools for push/fold
only.

## AI and what "solved" means

- **Beating the best humans is not solving the game.** A stronger AI can always come along and beat the previous one. **Solving** means computing a GTO solution that cannot lose to *any* opponent in a fair game.
- **Perfect vs imperfect information.** In chess or checkers everything is visible; in poker the hole cards are hidden. Every non-trivial competitive game solved so far has been a perfect-information game, apart from limit hold'em heads-up. Hidden information makes a game much harder to solve than its size suggests.

| Game | Size (order of magnitude) | Status |
|---|---|---|
| Checkers | 5 × 10^20 | Solved, 2007 |
| Heads-up limit hold'em (HULHE) | 3.19 × 10^14 decision points | Solved 2015 (Cepheus, U. of Alberta, **CFR+** — counterfactual regret minimization) on a 200-node cluster |
| Chess / shogi / Go | 10^47 / 10^71 / 10^170 | Superhuman AI (AlphaZero, AlphaGo), not solved |
| Heads-up no-limit hold'em (HUNLHE) | 10^160 — more than the atoms in the universe (10^82) | Libratus (Carnegie Mellon) beat top pros over 120,000 hands in 2017; not solved |

HULHE is *smaller* than checkers yet was solved eight years later and needed far
more hardware — the cost of imperfect information.

**Where the frontier is.** Multiway pots, unlimited bet sizes and varying stack
depths in big-bet games (NLH, PLO) are still out of reach: tournaments, 6-max
and full-ring cash are nowhere near fully solved. The practical workaround is to
**cut the game into smaller pieces** and solve those with limited bet sizes and
sensible abstractions. The result is a good *approximation* of GTO, not the
solution.

## Self-play AI software

These programs start from a random strategy and play trillions of hands against
themselves; lines that work are reinforced, lines that fail are weakened.

- **Good at:** fast, easy, almost no input, modest hardware; imports your hand histories and scores them against its strategy; pre-flop and range advice; challenge mode with error statistics.
- **Limits:**
  - It **does not solve for GTO** — the output is whatever the program believes is good against *itself*.
  - **Unverifiable**: it can't explain its plays and can't guarantee unexploitability.
  - Limited or fixed bet sizes.
  - Only its core strategy — **no exploitative adjustments** against weak players.
  - The strategy **drifts over time** as it keeps training, which makes it awkward to learn from.

## GTO solvers

Solvers are **Nash equilibrium calculators** for pre- and post-flop play. For
any **heads-up** post-flop spot they solve limit or no-limit hold'em with
arbitrary ranges and bet sizes to very high accuracy. Some go further: multiway
pre- and post-flop, and bigger games such as PLO.

A claim of "this is GTO" needs proof, because the full game is unsolved. The
proof is the **Nash distance**.

### Nash distance (ε)

A Nash equilibrium strategy maximizes its result against its **nemesis** (the
worst-case opponent), so in a zero-sum game it cannot lose. Exact equilibrium is
usually unattainable in complex games, so we settle for an **ε-Nash
equilibrium**: a strategy pair that loses at most ε to a worst-case opponent.

How to measure it for a candidate strategy pair:

> 1. Compute both players' EV under the pair.
> 2. Let P1 switch to his MES against P2's strategy; his EV gain is ε1.
> 3. Let P2 switch to his MES against P1's strategy; his EV gain is ε2.
> 4. **Nash distance = max(ε1, ε2)**

- ε = 0 → exact equilibrium. Small ε → close to GTO. Large ε → far from it.
- It can be measured **without knowing what the true equilibrium looks like** — that is what makes solver output verifiable and self-play AI output not.
- Solvers report it (PioSOLVER as a **% of the pot**) and let you set a target accuracy as the stopping condition. Longer runs lower ε, but once it is very small the solver oscillates rather than reaching zero.

**Why a small ε is good enough.** To take ε from you, a villain would need you
to play every combo at every node exactly like the solver, know that entire
strategy, compute the MES against it, and execute it flawlessly. None of that
happens. For a human, a small-ε solution is indistinguishable from perfect GTO.

**The author's thresholds** (arbitrary, but the community broadly agrees that
strategies barely change below them):

| Simulation | Target |
|---|---|
| Flop (post-flop) solve | **0.35% of the pot** |
| PioSOLVER pre-flop solve | **3.5 bb/100** |

- Wider ranges, higher SPR and bigger trees make a low ε harder and slower to reach.
- In pre-flop sims the **pre-flop ranges converge much faster than post-flop play**, and most of the leftover exploitability sits on the **river**. That is why a looser threshold, measured in bb/100, is acceptable.
- In abstraction-based solvers most exploitability comes from the simplified **post-flop** play. How much of that leaks into the pre-flop ranges is unknown, so "how exploitable are these pre-flop ranges?" can't be answered directly.

**Why trust the output anyway.** Different solvers run at high-quality settings
produce very similar strategies, and solver results agreed with older tools
(EV trees, push/fold Nash calculators) and established theory. Independent
methods converging on the same answer is the evidence.

### PioSOLVER — the accurate heads-up solver

Solves HUNLHE equilibria for arbitrary starting ranges, stack sizes and bet
sizes to a chosen accuracy.

- **Good at:** equity, EV, **EqR** and full strategies; very accurate; **MES and MinES** (minimally exploitative strategy); **aggregate reports** across many flops; limit and no-limit; ICM; scripting; works with other tools; heads-up pre-flop solver.
- **Limits:** **heads-up only**. Demanding hardware — tree complexity is capped by your machine, especially deep stacks with many sizes or the pre-flop solver. Big trees take a long time. Steep learning curve, and it presumes poker knowledge. **Setting a sim up correctly is the hard part**; browsing it afterwards is easy. Saved sims are large, so river strategies can be dropped and recomputed on the fly.

### MonkerSolver — the versatile multiway solver

Solves hold'em **and Omaha**, from any street, with **any number of players**,
by using abstractions to shrink the game.

- **Good at:** multiway NLH and PLO; ICM; **rake** adjustment; equity graphs; easy browsing of finished sims; range export.
- **Limits:** **abstraction costs accuracy** — the bigger the game, the coarser the solution. Better hardware permits finer abstractions, so high accuracy means very powerful machines or rented servers. Pre-flop trees can take **weeks**. Rough interface, very steep learning curve, tedious tree building, weak range analysis, **no aggregate reports**.

**The trade-off between the two:** Pio is precise but confined to two players;
Monker handles the multiway and PLO spots Pio can't, and pays for it in
accuracy.

## GTO training web apps

Libraries of **precomputed** solutions (6-max and HU cash, MTTs, HU SNGs, 3-max
jackpot SNGs, several stack depths) built by experts with private and
commercial solvers.

- **Good at:** nothing to install, no hardware, minimal input, **instant** answers; high-accuracy, rake-adjusted, multiway pre- and post-flop solutions; a growing library; post-flop analytics.
- **Limits:** **fixed bet sizes**; **precomputed only**, so no custom spots; core GTO strategy only, **no exploitative strategies**.

They suit a player who wants to learn GTO play without running calculations.

## What every tool has in common

1. **Each one answers a narrower question than it seems to.** Equity is not EV; an EV tree is not an equilibrium; an equilibrium for *your tree* is not the solution to poker.
2. **Output inherits the quality of the input.** Ranges, bet sizes, stack depths and abstractions are choices you (or the app's authors) made. Restricting options — no calls, no post-flop betting, three bet sizes — changes the answer, sometimes in a known direction.
3. **Only solvers and Nash/EV tools can tell you how to exploit a specific opponent** (via MES against an assumed strategy). Self-play AI and training apps give a core strategy and stop.

## Takeaways for the table

1. Match the tool to the question: equity → calculator; "how does this range hit?" → range analyzer; "what if villain plays like this?" → EV tree; "what is the equilibrium?" → solver.
2. Push/fold charts from Nash calculators are reliable at shallow stacks. Don't extend them to depths where flatting exists — they open too wide or call too wide, depending on the abstraction.
3. Treat solver output as an approximation for the tree you built. Check the Nash distance and remember the bet sizes and ranges were your assumptions.
4. Don't worry about a small ε. Nobody can know and perfectly counter your whole strategy; your execution errors are far bigger.
5. For multiway and PLO spots expect coarser answers than for heads-up NLH spots — study patterns, not exact frequencies.
6. A GTO core strategy is a baseline. No tool will tell you how a particular weak opponent deviates; you supply that read, then compute or reason out the exploit.
