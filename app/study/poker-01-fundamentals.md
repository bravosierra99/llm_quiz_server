---
title: "Poker 01 — Fundamentals"
summary: "Modern Poker Theory ch. 1: positions, vocabulary, combinatorics, pot odds, equity, EV, fold equity, equity realization, SPR and range shapes."
order: 101
audience: bravosierra99
---

# Poker 01 — Fundamentals

*Study guide to Chapter 1 of* Modern Poker Theory *(Michael Acevedo). Read the
chapter for the range charts and heatmaps; this guide is the skeleton you should
be able to rebuild from memory.*

## The premise of the whole book

**Profit = opponents' mistakes − our mistakes.** You can't control how opponents
play (beyond game selection), but you can always reduce your own mistakes. So GTO
study has two halves: **fix your own leaks**, and **learn what correct play looks
like so you can spot and exploit what others do wrong**. It is not just "balance
for its own sake".

## Positions (9-handed)

| Group | Seats | Notes |
|---|---|---|
| Early (EP) | UTG, UTG+1, UTG+2 | First to act pre-flop; removed first when the table is short |
| Middle (MP) | Lojack (LJ), Hijack (HJ) | 4th and 5th to act |
| Late (LP) | Cutoff (CO), Button (BN) | BN acts last on every post-flop street |
| Blinds | SB, BB | SB is first to act post-flop; BB is last to act pre-flop |

- **IP / OOP** – in position (acts last) / out of position.
- **First in** – action reaches you and nobody has voluntarily entered the pot.
- **Effective stack** – the smallest stack among active players; the most anyone can lose heads-up. Stack depth is always quoted in **big blinds**.

## Vocabulary worth owning

| Term | Meaning |
|---|---|
| **Nuts / effective nuts** | Best possible hand / a hand strong enough to play *as if* it were the nuts (77 on 8♥7♦2♦) |
| **Air** | No showdown value, no draw — can only win by bluffing |
| **Bluff catcher** | A hand that only beats bluffs |
| **Pure bluff vs semi-bluff** | Little/no chance to improve vs a decent chance to improve |
| **Showdown value** | Can realistically win at showdown against villain's range |
| **Nut advantage** | Effective-nut hands are a bigger share of your range than of villain's |
| **RFI** | Raise first in (open raise). A raise is a **2-bet** (the blind is bet #1) |
| **Steal / resteal** | RFI from CO, BN or SB / 3-betting a steal |
| **Isolate** | Raise a limper to play them heads-up |
| **Squeeze** | 3-bet after a raise *and* a call |
| **Cold call / cold 4-bet** | Calling a raise (or 3-bet/4-bet) / 4-betting with no money previously invested voluntarily |
| **C-bet** | Bet by the previous street's last aggressor |
| **Donk bet (lead)** | OOP player bets into the previous street's aggressor |
| **Overbet** | Bet larger than the pot |
| **Lines** | x/f, x/c, x/r, b/b (double barrel), b/b/b (triple barrel), l/f, l/r |
| **Toy game** | Simplified game that models one aspect of real poker |
| **Abstraction** | Simplifying the game: *information* abstraction bundles equivalent hands; *action* abstraction removes options (e.g. silly bet sizes) |
| **Rake** | House fee: timed, or a % of the pot (2.5–10%) usually capped, and usually **no flop, no drop** |

## Thinking in ranges

Beginners think about their own hand; better players put the villain on a hand;
good players assign a **range** and narrow it with each action; the best players
also think about **their own range** and how it fares against the villain's
(equity, polarization, balance, nut advantage).

**The split-range leak.** A villain who raises premiums and limps medium hands is
trivially exploitable: raise his limps (he's capped), fold your medium hands to
his raises (he's strong), and post-flop you know which boards he can't have hit
(a raise-range of only big pairs and big cards has no sets/straights on 8-7-6).
**Entering the pot only by raising with everything you play** makes you far
harder to read. Every action leaks information — construct ranges off the table
so the leak is small.

## Combinatorics

- 169 distinct starting hands: **13 pairs, 78 suited, 78 offsuit**.
- **1,326** total combos = 78 pair combos + 312 suited + 936 offsuit.

| Hand type | Combos | With card removal |
|---|---|---|
| Pocket pair | 6 | X(X−1)/2 where X = cards of that rank still available (3 left → 3 combos, 2 left → 1) |
| Unpaired (e.g. AK) | 16 | X × Y (available cards of each rank) |
| Suited | 4 | drops by one per blocked suit |
| Offsuit | 12 | |

By combo count, pairs are 5.9% of hands, suited 23.5%, offsuit 70.6%.

**Blockers** – cards in your hand or on the board remove combos from villain's
range. On A♣J♥9♥ holding A♦3♦, villain has only **1** combo of AA, 3 each of JJ
and 99, and 2×3 = 6 combos of AJ.

**Why this matters:** counting a 23% hijack opening range on A♣J♥9♥ shows it is
made hands and draws almost everywhere — only ~3% is pure air. Opening ranges
connect with far more boards than intuition suggests. Tools (Flopzilla, Equilab)
do this instantly; do it by hand a few times so the logic is internalised.

## Pot odds and outs

**Pot odds = risk : reward.** As a percentage:

> required equity = call ÷ (pot after you call)

Villain shoves $100 into $100: you call 100 to win 200 → 100/300 = **33.3%**.

**Outs** – unseen cards that make your hand best.

| Draw | Outs | Turn only | Turn + river |
|---|---|---|---|
| Gutshot | 4 | ~9% | ~17% |
| Two overcards | 6 | ~13% | ~24% |
| OESD | 8 | ~17% | ~32% |
| Flush draw | 9 | ~19% | ~35% |
| Flush draw + gutshot | 12 | ~26% | ~45% |
| Flush draw + OESD | 15 | ~32% | ~54% |

**Rule of 4 and 2:** outs × 4 with two cards to come, outs × 2 with one. (Only use
×4 when you will actually see both cards — e.g. facing an all-in.)

- **Backdoor draws** (flush or straight) complete ~4% of the time ≈ **one extra out**.
- **Dead outs** – outs that improve you but give villain a better hand. **Drawing dead** – all outs are dead.
- **Implied odds** – extra money you expect to win on later streets when you hit. **Reverse implied odds** – money you lose when you hit and are still second best.
- **Pot committed** – your price is better than your chance of winning needs to be, so folding is a mistake.

## Equity

Your share of the pot if all cards were dealt with no more betting.

- **Hand vs hand:** hands can't be ranked in a vacuum — equity is non-transitive. AKo beats JTs, 22 beats AKo, yet **JTs beats 22**.
- **Hand vs range:** assign a range from villain's actions, then compare your equity to the pot odds. (QTo with 43% facing a tight 10bb SB jam needing 45% is a fold.)
- **Range vs range:** how the board shifts the matchup. A CO opener has ~58.5% vs a BB caller pre-flop, but on 8♥7♠5♠ the BB is a slight favourite — so the opener must **check more**, even with AA, because the BB has the straights, sets, two pairs and combo draws and can check-raise a frequent c-bet.

Each hand must be played in the way that is best **in the context of the whole
range** — AA checks back 875ss not because it's weak but because the range needs
strong hands in the checking line.

Unblocking matters when bluff-catching: holding no hearts or spades when the
draws miss makes it *more* likely villain has the busted draw.

## Expected value (EV)

> EV = (%W × $W) − (%L × $R)

- EV of folding is **always 0** — money already in the pot isn't yours.
- Always pick the highest-EV action. Win rate = EV per hand × 100 → **bb/100**.
- Worked example: BN opens 2x with A5s, SB rejams 15bb with a 20% range. Equity 43.3%, win 18bb, risk 13bb → EV ≈ **+0.4bb**. Thin, but these edges repeated thousands of times separate pros from amateurs.
- **EV rescaled** = EV ÷ pot. Lets you compare actions as a fraction of the pot.

## Fold equity (FE)

> FE = (chance villain folds) × (villain's equity)

Strictly, it's the extra equity you gain because villain might fold; loosely, just
"how often they fold". 87s with 29% vs 33 on AK5 gains a huge amount by betting
because the 71%-equity pair folds most of the time.

**Break-even jam:** set EV = 0 and solve for the fold frequency. BB rejamming 15bb
with T5o over a 60% button open needs ~47% folds; a button calling with 28.8% of
hands folds 52% of his opens — so even T5o is (barely) profitable against a
too-wide opener who folds too much. **Wide ranges are hard to defend.**

## Equity realization (EqR)

With no betting, EV = equity × pot. With betting, hands that fold before showdown
hand their equity to the others.

> EV = Eq × EqR × pot − cost &nbsp;&nbsp;→&nbsp;&nbsp; EqR = (%EV captured) ÷ equity

- **Over-realize**: capture more of the pot than raw equity. **Under-realize**: less.
- Worked example: BB with 95o vs a 16% UTG open of 2bb. Pot odds need 17.8%; raw equity is 29.5%. But EqR is only ~58% → realised equity ~17.1% → **fold**. It needed ~61% EqR.
- **Raw equity alone overstates how wide you can defend.**

What drives playability:

| Factor | Effect |
|---|---|
| **Position** | IP can check behind and take a guaranteed free card; OOP often checks and faces a bet |
| **Hand strength** | Very strong and very weak hands are easy; **medium hands are the hard ones** |
| **Suitedness** | Suited hands realise ~**16% more** equity than offsuit (front- and backdoor flush draws) |
| **Connectedness** | Disconnected offsuit junk (Q2o) is among the worst — weak pairs, no draws |
| **Range advantage** | A strong range protects its weak hands: villain can't bet as aggressively, so you see free cards |

## Stack-to-pot ratio (SPR)

> SPR = effective stack ÷ pot

| SPR | What gains value |
|---|---|
| **Low (0–5)** | Top pairs and overpairs. Speculative hands suffer (little fold equity, low implied odds) |
| **Medium (6–11)** | Top pair is demoted; suited and connected hands gain |
| **High (11+)** | **Nuttiness** — sets, nut draws, big flushes and straights that can cooler. One pair struggles to reach showdown in big pots without backup equity |

Plan bet sizes ahead so you arrive at an SPR that suits your range.

## Range morphology

| Shape | Composition |
|---|---|
| **Linear** | The best hands downward with no gaps |
| **Polarized** | Strong value hands + weak bluffs, nothing in between (perfectly polarized = nuts or air) |
| **Condensed / depolarized** | Middle-equity hands; top and bottom removed |
| **Capped** | Missing the strongest hands |
| **Uncapped** | Contains all the strongest hands |

A condensed range is capped, but a capped range needn't be condensed. Whether a
range is capped depends on the **board**: a BB flat-calling range is capped on
A-J-T (no KQ, sets or top two) but not on 5-4-3. Real ranges are mixtures, not
pure types.

## Takeaways for the table

1. Count combos, not hands — and remember your own blockers.
2. Required equity = call ÷ final pot. Know the 4/2 rule cold.
3. Raw equity ≠ EV. Discount weak, offsuit, disconnected, out-of-position hands.
4. Board texture decides who has the range and nut advantage — not who raised.
5. Know your SPR before the flop bet goes in.
