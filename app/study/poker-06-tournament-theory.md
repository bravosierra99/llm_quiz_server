---
title: "Poker 06 — The Theory of Tournament Play"
summary: "Modern Poker Theory ch. 6: variance, MTT metrics (ITM, Total vs Average ROI, ABI), volume vs ROI, bankroll and game selection, mental game, tournament life, ICM, cEV vs $EV, risk premium, FGS and the gambler's ruin."
order: 106
audience: bravosierra99
---

# Poker 06 — The Theory of Tournament Play

*Study guide to Chapter 6 of* Modern Poker Theory *(Michael Acevedo). Cash games
are usually 6-max, no antes, 100bb; MTTs are 9-handed with antes and shifting stack
depths, and above all they **pay by finishing place, not by chips held**. This
chapter covers judging MTT results and knowing when chips stop behaving like money.*

## Variance

**Variance** is how widely actual results scatter around expectation (EV): low
variance means results bunch near EV, high variance means they spread far from it.

> Variance = S² (S = the standard deviation your tracker reports)
>
> Variance = Σ(xᵢ − x̄)² ÷ (n − 1)

Check: data (1, 6, 11) → mean 6 → squared deviations 25 + 0 + 25 = 50 → ÷ 2 =
**25**, so S = **5**. In poker, xᵢ is your win rate in each 100-hand chunk and x̄
is your overall win rate.

Two things decide how far your *results* stray from your *true* win rate:

- **How widely the chunks spread** around your average. This is largely a property
  of the game and format:

| Game | Typical SD (bb/100) |
|---|---|
| NLH full ring | 60–80 |
| NLH 6-max | 75–120 |
| PLO full ring | 100–140 |
| PLO 6-max | 120–160 |

- **Sample size.** The uncertainty in your *observed* win rate shrinks with the
  square root of the sample: 100× the hands → 1/10 the SD (67bb/100 SD: ±67 after
  100 hands, ±6.7 after 10,000, ±0.67 after 1,000,000). **Volume tames variance.**

**A higher win rate doesn't change the SD, but it slashes the chance of being down**
(same SD, simulated cash players):

| | 2.5bb/100 | 5bb/100 |
|---|---|---|
| Chance of a loss over 10k hands | ~35% | ~23% |
| Chance of a loss over 100k hands | ~12% | ~1% |
| Minimum bankroll | 2,690bb | 1,345bb |

Doubling the win rate halves the bankroll needed. Use a variance calculator (e.g.
PokerDope) to plan for realistic downswings rather than trusting your gut.

### Why tournaments swing harder

- **Chips can't be cashed.** You're paid only for finishing in the money (usually
  the top **15–18%**), so even a 10bb/100 chip win rate can't tell you how much, or
  whether, you'll earn.
- **Not every pot costs the same.** A lost 50bb flip in a cash game costs 50bb at
  any hour, and you can reload. Ten hours into an MTT, with 90%+ of the field gone,
  it can cost a fortune in prize equity, and you can't rebuy into that spot.

## Tournament metrics

A chip win rate measures chip accumulation, not money-making, so MTT skill needs
other yardsticks (SharkScope tracks them online).

| Metric | What it is | Weakness on its own |
|---|---|---|
| **Total cashes / earnings** | Sum of prizes | Ignores buy-ins, travel, tax: $100k cashed − $60k of missed buy-ins − $20k travel = $20k pre-tax |
| **Profit** | Cashes minus buy-ins | One lucky score can make a long-term loser look good; $2M cashed on $3M of buy-ins is −$1M |
| **ITM%** | How often you cash | Says nothing about how deep you go |
| **Total ROI** | (total won − total invested) ÷ total invested | A single big score can dominate it |
| **Average ROI** | Each event's ROI, averaged | Best single read of your edge vs the fields you play |
| **ABI** | Average buy-in | The unit for bankroll management |

**ITM benchmarks.** Online (non-bounty) winners cash about **15–18%**. Much lower
usually means too loose on bubbles or over-aggressive early. Much higher usually
means **too passive on bubbles**: squeaking into a min-cash instead of building a
stack that can win. Live, some players reach **30–50%** ITM because fields are
softer.

**Total vs Average ROI.** 2,000 × $109 = $218,000 invested and $300,000 cashed →
Total ROI = 82,000 ÷ 218,000 = **37.6%**. Now a terrible player loses 1,999 $109
events, then wins $300k in one $1,050 event: his Total ROI is also ~**37%**, the
same as a consistent winner with the same totals. But his Average ROI =
(1,999 × −100% + 1 × (300,000 − 1,050) ÷ 1,050) ÷ 2,000 = (−1,999 + 285) ÷ 2,000 =
**−85.7%**. Every event counts once, so one fluke can't drown out 1,999 losses.
Even so, over a finite sample neither sign of Average ROI guarantees the result.

## What results actually tell you

Simulated 2,000 × $109 MTTs (fields of ~300, $218,000 invested):

| Avg ROI | EV | P(loss) | Worst run | Best run |
|---|---|---|---|---|
| −25% | −$54,500 | 99% | −$108,755 | +$6,520 |
| −10% | −$21,800 | 84% | −$81,440 | +$36,865 |
| 0% | $0 | 52% | −$56,630 | +$88,690 |
| +10% | +$21,800 | 20% | −$45,035 | +$95,575 |
| +25% | +$54,500 | 1% | −$17,330 | +$131,905 |
| +50% | +$109,000 | 0% | +$35,575 | +$194,275 |

- After 2,000 events a −25% player can still be up, and a −10% player's best run
  (+$37k) beats a +10% player's *expectation* (+$22k). A −10% player running hot
  and a +50% player running cold both finish near +$36k.
- A breakeven player can end anywhere from about −$57k to +$89k. Many "successful"
  players are breakeven or losers who ran well; some strong players quit during a
  bad run.

Over **200** events it's far noisier: a genuine +25% player still loses money
**28%** of the time (a +50% player 10%), and a −25% player is sometimes up ~$19k.
Never judge skill by money won over a small sample.

## Decreasing variance, increasing profit

The two main levers are **raise your Average ROI** and **raise your volume**, in
that order. Volume only multiplies an edge you already have; grinding games you
can't beat just loses faster.

| Choice | Upside | Downside |
|---|---|---|
| Higher stakes | More $ per event | Tougher fields → lower ROI; few events → low volume → more variance |
| Turbos | More volume | Lower ROI: little time to out-play weak players, mostly shallow pre-flop poker |
| Bounty events | Lower variance | Lower EV for a strong player: part of the pool becomes bounties, and weak players collect some before busting. They favour weaker players |
| Live MTTs | Higher ROI (softer fields) | Low volume, so results take much longer to converge |

**Play vs study.** New players: about **50/50**; volume is for learning, and some
lessons only come from playing. Winning players: about **80/20** play/study. Extra
study then moves the bottom line less than volume, but stopping entirely lets an
improving field pass you.

**Raising ROI.** Easiest: play lower stakes. Hardest, and the real one: become
better than your opposition. That starts with winning chips at every stack depth,
plus MTT soft skills: tournament life, bubbles, how equilibrium shifts by stage,
population tendencies, live reads, bankroll management, mental game.

> **GTO is about exploitation, not balance.** Equilibrium is what results when both
> players maximally exploit each other. If opponents don't notice what you're doing,
> or can't counter-adjust, you have no need to be balanced against them.

Tournament poker is overwhelmingly exploitative: learn the theory, then study
opponents and don't fear an unorthodox play.

## Bankroll management

1. Bankroll = a large share of net worth for a pro; for a recreational player, an
   amount you can afford to lose but still care about.
2. Keep **at least 200 buy-ins** (at your ABI); **1,000** if you want the risk of
   ruin near zero.
3. Pros: hold **6+ months** of living expenses *outside* the bankroll, a year or
   more to avoid money stress.
4. Live players can hold fewer buy-ins (higher ROI and smaller fields mean smaller
   swings per event) but must budget **travel**, which quietly turns many winners
   into losers.

**Backing with makeup.** A common deal splits profit 50/50, with losses
accumulating as **makeup** that must be repaid before anything is split. Down
$5,000, then win $10,000 → $5,000 clears makeup and the other $5,000 is split,
$2,500 each. Win $10,000 in your first event (no makeup) → $5,000 each. Strong
players negotiate 55/45 or 60/40; some live deals are 40/60 with the backer paying
travel. Backing lets you play higher than your own roll allows.

## Game selection and ABI

Choose events by **edge**. Only the best player in the world with an infinite
bankroll should simply play the biggest games. For everyone else, smaller games,
with **higher ROI and lower variance**, usually beat bigger games with lower ROI and
higher variance.

You can't fill a schedule at one buy-in, so you play a range and track your
**ABI**: $100, $200 and $500 → ABI = **$267**. But a **wide spread of buy-ins adds
variance** even at the same ABI, because the few big events carry a huge share of
the money at risk and never get enough volume to average out:

| 2,000 events, 25% ROI | Invested | EV | P(loss) | Worst run | Best run |
|---|---|---|---|---|---|
| Wide spread ($109 to $10,300; ABI ≈ $235) | $471,050 | $117,763 | 30% | −$262,450 | +$1.44M |
| Every event ≈$235 | $468,000 | $117,000 | 3% | −$36,127 | +$374,486 |

Same EV, **10× the chance of losing**. Count shots in ABIs: with an ABI around
$100, one $10k and one $5k event together are ~**150 buy-ins**.

**What winners' numbers look like** (top online pros): ITM ~15–18%, Average ROI
~35–50%, Total ROI often well below Average ROI (one: 37% vs 9%). They usually
finish in the bottom 10% of a field less than 10% of the time and in the top 10%
more than 10% of the time. Losing players are typically playing above their skill
level, bust early too often and reach the late stages too rarely. The cure is to
drop stakes, study fundamentals, and get coaching or a study group.

## The mental game

Mental game is key, especially in MTTs. Winners and losers sit at opposite ends:

| Winners | Losers |
|---|---|
| Positive; understand variance yet own their results | Negative; blame luck, the site, the dealers |
| Work ethic (study plus volume); seek feedback | Lazy; reject criticism |
| Emotions in check; long-term focus | Often on tilt; short-term focus |
| Seek weaker games; only as many tables as they can play their A-game on | Ego drives them into tough games; too many tables on autopilot |
| Healthy habits, good sleep before big events, pre/post-session routines | Junk food, substance abuse, partying before events, straight from bed to the tables |
| Discuss hands with a network of strong players | Tell bad-beat stories |

## Tournament life

The winner holds all the chips, but equivalently the winner is the **last player
standing**. Tournaments reward *survival* (outlasting others), not busting people
yourself. **Tournament life** is the value of still having chips, and chip EV (cEV)
misses two parts of it:

**1. EV of future hands.** First hand of a big event, 50,000 chips at 75/150
(~333bb). A maniac in the SB shoves blind; you have J8o in the BB. J8o has 51.48% vs
a random hand, so calling is worth about **+10.9bb** in chips (1,090bb/100), yet you
should fold. Waiting to call him with, say, AA is worth about **+235bb**. Staying
alive keeps access to far better spots.

**2. EV of a higher payout.** Surviving lets you climb the pay ladder as others
bust, so **folding has positive value in a tournament**, unlike a cash game, where
the EV of folding is always zero.

Both are hard to quantify, so models were built: **ICM** and **FGS**.

## The Independent Chip Model (ICM)

**Example SNG:** 10 players × $10 = $100 pool, paying $50 / $30 / $20, 1,000
starting chips each. Win all 10,000 chips and you get $50: 100% of the chips, 50% of
the money. Doubling up on hand one doesn't double your stack's value.

> **Principle of diminishing chip value:** the chips you risk are worth more than
> the chips you can win, and the more chips you have, the less each one is worth.

ICM turns stacks into **prize-pool equity**. From stack sizes it estimates each
player's chance of finishing in each place and multiplies by the payouts (use a
calculator such as HoldemResources).

Four left in that SNG:

| Player | Stack | Chip % | ICM $ |
|---|---|---|---|
| A | 6,000 | 60% | $40.39 |
| B | 1,800 | 18% | $24.53 |
| C | 1,200 | 12% | $18.85 |
| D | 1,000 | 10% | $16.24 |

A's 60% can't be worth $60: first prize is only $50 and A won't always win. D's
10% is worth far more than $10.

**Deals.** ICM is the standard for final-table deals but tends to **overvalue short
stacks**. **Chip chop** (pay by chip share) **overvalues big stacks**; here A would
get $60, more than first prize.

**Two kinds of EV:**
- **cEV**: the average chips an action gains.
- **$EV**: the average money it gains, based on prize-pool equity.

In cash games they're identical (ignoring rake). **In MTTs, decide on $EV.**

### Push/fold on the bubble (same SNG, 4 left, 3 paid, blinds 50/100)

| Seat | Stack | cEV push | ICM push |
|---|---|---|---|
| CO | 1,000 | 26.2% | 14.2% |
| BN | 1,200 | 32.1% | 15.7% |
| SB | 1,800 | 42.4% | 14.9% |
| BB | 6,000 | — | — |

With the chip leader in the BB, everyone shoves **half as wide or less** than cEV
says. Many +cEV shoves are −$EV.

Swap the BN and BB stacks (BN 6,000, BB 1,200) and the leader on the BN shoves
**any two cards** (cEV: 27.4%), because the others can only call him very tightly.
The SB (1,800) also shoves 100% when folded to, against a 1,200 BB, while the
1,000 CO still shoves only ~14%.

- **Payout structure matters:** top-heavy payouts reward aggression; flat payouts
  reward tight play.
- **ICM pressure only works on ICM-aware players.** The SB's 14.9% shove assumes the
  BB calls only 6.7%. If the BB calls a cEV range (23.8%), **both** blinds lose $EV
  and it flows to the players not in the hand, even though the SB played
  "correctly". Watch who actually folds before you lean on them.

Modern solvers include ICM; run bubble and final-table spots off the table to
build a feel for deviating from chip-EV play.

### ICM's limitations

- Treats the hand in isolation: ignores rising blinds and the future value of a big
  stack that can bully others.
- Assumes equal skill and ignores table image.
- Only workable for a few players (a final table or two), so useless early.
- Ignores **position**: 4bb on the BN is worth far more than 4bb UTG.

Still an excellent $EV approximation for final tables, bubbles and SNGs.

### ICM rules of thumb

- Call off **tighter** than in cash games.
- Pass on **marginal +cEV** spots.
- **Medium stacks** must play tight while short stacks are around, especially on
  the bubble.
- **Big stacks** can lean on medium stacks, who can only stack off with very tight
  ranges.

## Risk premium

Because chips won are worth less than chips risked, the pot you're playing for is
effectively smaller than its chip count. **Risk premium** is the extra equity, on
top of the chip-EV break-even, that a play needs to be +$EV.

> Required $ equity = $R ÷ ($W + $R)
>
> Risk premium = required $ equity − required chip equity

**Worked example.** Same SNG bubble, blinds 50/100. The BN (6,000) shoves any two,
the SB (1,800) folds, and you're in the BB with 1,200 and AKo. ICM calling ranges
here are only AA–TT for the SB and, once the SB folds, AA–88, AKs and AQs for the
BB. AKo has 65.32% vs any two.

- **Chips:** you risk 1,100 more. Winning takes you from 1,100 (after a fold) to
  2,450, a gain of 1,350. cEV = 0.6532 × 1,350 − 0.3468 × 1,100 ≈ **+500 chips**.
  Break-even = 1,100 ÷ 2,450 ≈ **45%**.
- **Money:** your stack is worth **$18.02** after a fold and **$27.12** after a
  winning call, so $W = $9.10; losing busts you, so $R = $18.02. $EV = 0.6532 × 9.10
  − 0.3468 × 18.02 ≈ **−$0.31**. Break-even = 18.02 ÷ 27.12 = **66.4%**.
- **Risk premium ≈ 20%.** It is 66.4% − 45% ≈ 21.5%; the book's break-even line
  uses 1,250 for the chips won, giving 47% and a printed **19.44%**. Either way, AKo,
  a big chip favourite, is a fold.

**Typical MTT risk premiums** (your stack, facing the opponent's):

| You ↓ / vs → | Big stack | Mid stack | Short stack |
|---|---|---|---|
| **Big stack** | 18–25% | 6–8% | 2–4% |
| **Mid stack** | 13–15% | 10–12% | 5–7% |
| **Short stack** | 9–12% | 8–10% | 7–10% |

Clashes between big stacks are the most expensive; mid stacks facing the chip
leader need a lot extra; a big stack calling a short stack needs very little.

What moves it:
- **Payout structure:** flatter → *higher*; top-heavy → lower; **winner-take-all →
  zero** (no ladder to climb).
- **Very short stacks** in the field raise everyone else's, especially other short
  stacks'.
- **Bet size:** largest when calling for your stack; vs a min-raise it can be under
  2%, which still trims the marginal bottom of a BB defending range.
- It applies **post-flop**: a BB with a high risk premium vs the opener struggles to
  call down and realizes less equity → **defend tighter**.
- It applies to **betting** too: vs an opener with a high risk premium against
  *you*, **defend wider**, since he can't barrel freely.

## Future Game Simulation (FGS)

FGS runs ICM over several future hands, weighting each outcome by its probability,
so it captures what ICM misses: **position relative to the blinds, blind/ante size
relative to stacks, and the blinds moving round**. It helps most when blinds are
about to rise, when very short stacks risk losing playability or fold equity, and
when a short stack is likely to bust or blind out soon (bubbles, satellites).

Limits: much slower to compute; push/fold only, few players, so useless early in an
MTT; and only meaningfully different from ICM at tables of **6 or fewer with stacks
under 10bb and some at 5bb or less**. Most affected positions: **UTG, SB, BB**.

Both models teach **diminishing chip value**, but only at or near the money. For
early stages and skill edges, look at the gambler's ruin.

## The gambler's ruin

Two players flip for one chip at a time until one has everything.

**Fair game:** your chance of going broke equals your *opponent's* share of the
chips.

> P(P1 goes broke) = n₂ ÷ (n₁ + n₂)

Six chips each → 50% each. P1 with 8 and P2 with 5 → P1 goes broke 5/13 ≈ 38%, P2
8/13 ≈ 62%. Even at fair odds, the shorter stack is more likely to lose.

**Unfair game** (P1 wins each flip with probability p, q = 1 − p):

> P(P1 wins everything) = [1 − (q/p)^n₁] ÷ [1 − (q/p)^(n₁ + n₂)]

With 20 chips in play, Hero's chance of winning:

| Hero's chips | Fair (p = 0.50) | Edge (p = 0.52) | Deficit (p = 0.48) |
|---|---|---|---|
| 2 | 10% | 19% | 4% |
| 4 | 20% | 34% | 10% |
| 5 | 25% | 41% | 12% |
| 10 | 50% | 69% | 31% |
| 15 | 75% | 88% | 59% |

- **Fair:** linear, so every chip is worth exactly 5%.
- **Edge:** **concave**. Doubling 2 → 4 chips doesn't double your chance; the first
  chips are worth most (~0.096 each) and the last least (~0.021). Diminishing chip
  value appears from skill alone, with no payout structure at all.
- **Deficit:** convex. Doubling 2 → 4 *more* than doubles your chance; the last chip
  is the most valuable (~0.096).

**A 0-cEV flip for 5 chips with 10 chips:** your new chance is the average of the
5-chip and 15-chip values. With an edge, (41% + 88%) ÷ 2 ≈ 64.5% < 69%, so the flip
**costs** you. With a deficit, (12% + 59%) ÷ 2 ≈ 35.5% > 31%, so it **helps**.

> **With a skill edge, be risk-averse and skip marginal gambles. With a skill
> deficit, gamble for big chunks of your stack.**

Against a weak player, grind him down post-flop rather than flipping for a huge
pot: variance is the weaker player's best friend. A casino would rather you play
100 × $20 blackjack hands than one $2,000 hand, because low variance makes its edge
near-certain.

## The big picture

No model captures every MTT variable, and copying a winner's style can backfire
because it's tuned to *their* metagame. Chip values keep changing, so **tournament
equilibrium is dynamic**; the key skill is **shifting gears**, knowing when to pass
on small edges and when to push them, using equilibrium charts as a baseline.

## Takeaways for the table

1. Judge yourself by Average ROI over a big sample, not by cashes or a few scores.
   Even 200 events say very little.
2. Bankroll: 200+ ABIs (1,000 to be near-safe), keep your buy-in spread narrow, and
   count every big shot in ABIs.
3. Decide on $EV: call off tighter and skip marginal +cEV flips, all the more with
   a skill edge (and the flatter the payouts). Winner-take-all → play for chips.
4. On a bubble, big stacks attack medium stacks, medium stacks tighten while short
   stacks remain, and nobody can be pressured if they ignore ICM.
5. Defend tighter when *you* have a high risk premium against the opener, and wider
   when *he* has a high one against you.
6. Equilibrium is the starting point. Exploit opponents who won't or can't adjust.
