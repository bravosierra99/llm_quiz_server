---
title: "Poker 09 — MTT Equilibrium Strategies: Playing Versus 3-bets"
summary: "Modern Poker Theory ch. 9: what to weigh when 3-bet, 2x opens vs rejams (10–25bb), jam/call/fold vs non-all-in 3-bets (25–40bb) and sized 4-bets deep (60–80bb), with frequencies and range shapes."
order: 109
audience: bravosierra99
---

# Poker 09 — MTT Equilibrium Strategies: Playing Versus 3-bets

*Study guide to Chapter 9 of* Modern Poker Theory *(Michael Acevedo). The chapter
is mostly range charts (Hand Ranges 267–336). This guide gives you the frequencies,
the trends across stack depths and positions, and the shape of the ranges in
words. Look at the charts in the book for the exact cells.*

## What to weigh when you're 3-bet

The charts are equilibrium baselines. In-game, run through these factors:

| Factor | Question to ask | Why it matters |
|---|---|---|
| **Your position** | How strong is my opening range? | Sets how strong the hands you're choosing your defence from are |
| **Villain's position** | How strong is their 3-bet range? | Earlier 3-bettors are stronger and bluff less |
| **Players left to act** | How many still act behind the 3-bettor? | More players behind → villain is less likely to be bluffing → you need to defend **fewer** hands to be unexploitable |
| **Bet size** | Is it all-in? Can I 4-bet with fold equity? Is the price right? | Facing a jam you can only call or fold; facing a small 3-bet, calling is cheaper |
| **Relative position** | Will I be IP post-flop? | IP realizes equity far more easily, so it calls more; OOP leans on 4-bet or fold |
| **Range morphology** | Is the 3-bet range polarized or linear? How does my hand play against it? | Decides whether your hand wants a flop or wants to get it in now |
| **Risk premium** | How deep in the event? Who has the higher risk premium in this matchup? | ICM pressure makes marginal calls worse |
| **Future situations** | If I call and lose, what does my stack become? If I win? | Losing may cost you raise/fold ability or put you in awkward ICM spots; winning may make you chip leader, able to pressure medium stacks |
| **Bluffing** | Is this villain over- or under-bluffing here? | The main reason to deviate from the baseline |
| **Profitability** | Is the call about 0 cEV? | A break-even chip call is usually **slightly −$EV** in a tournament, so lean towards folding |

**How to use the charts.** Not every position and stack depth is covered, but the
ranges shift smoothly (roughly linearly) with stack depth and position. Learn the
**trends** and interpolate the gaps. More important than memorizing cells is
understanding *which kinds of hands* raise, call or fold, and *why*. Rounding and
simplifying the frequencies is fine. No human will exploit small imprecision, as
long as the core ideas are right.

## Short stack: 2x open vs a rejam (10–25bb)

Facing a rejam you have only two options, call or fold, and there's no post-flop
play to worry about. Playability is irrelevant. **Call with the top x% of your
opening range ranked by equity against the rejam range** for that stack depth.

All percentages below are **shares of the opener's own 2x range**, not of all
hands. Fold is the remainder.

Overall average: **call ≈ 45% (44.96%), fold ≈ 55% (55.04%)**.

### Stack depth matters most

| Effective stack | Opener calls |
|---|---|
| 10bb | 57.7% |
| 12bb | 52.0% |
| 15bb | 47.8% |
| 17bb | 43.9% |
| 20bb | 37.8% |
| 25bb | 30.6% |

**The deeper the rejam, the less you defend.** Part of the reason is price. Having
invested only 2bb, you must put in a much bigger share of the final pot when the
jam is bigger. *Illustration (not from the book; ignoring antes):* BB jams 10bb over your
2bb open with the SB folded. You call 8 to win a 20.5bb pot, which needs ~39%
equity. Against a 25bb jam you call 23 into 50.5bb, which needs ~45.5%. Antes
lower both figures.

### Who jammed

| Rejammer | Opener calls |
|---|---|
| UTG+1 | 39.3% |
| UTG+2 | 40.7% |
| LJ | 41.7% |
| HJ | 42.7% |
| CO | 44.2% |
| BN | 45.4% |
| BB | 46.1% |
| SB | **48.8%** |

- **The earlier the jammer's seat, the tighter you call.** More players were left
  to act behind them, so their range is stronger.
- **Exception: the SB is called lighter than the BB.** The BB can simply call the
  open and close the action, so it flats many hands and its jam range is
  stronger. The SB jams a wider range.

### Who opened

| Opener | Calls |
|---|---|
| BN | 42.1% |
| UTG | 44.7% |
| HJ | 44.7% |
| UTG+1 | 44.8% |
| UTG+2 | 45.6% |
| LJ | 45.7% |
| CO | 45.7% |

The opener's seat barely moves the defence share (42–46%; the BN, with the
widest min-raise range, is lowest). Stack depth (58% → 31%) and the jammer's seat
(39% → 49%) matter far more. A stronger opening range defends a similar
*percentage* because it also faces stronger jams.

### Selected spots (call % of the 2x range)

| Opener vs rejammer | 15bb | 25bb |
|---|---|---|
| BN vs BB | 42.6% | 29.5% |
| BN vs SB | 44.9% | 31.6% |
| CO vs BB | 45.1% | 31.0% |
| CO vs SB | 50.2% | 31.3% |
| CO vs BN | 43.8% | 31.6% |
| LJ vs BB | 47.9% | 32.5% |
| LJ vs SB | 51.3% | 33.9% |
| LJ vs HJ | 46.2% | 27.2% |
| UTG vs BB | 50.3% | 30.5% |
| UTG vs SB | 52.9% | 34.5% |
| UTG vs HJ | 45.7% | 30.6% |
| UTG vs UTG+1 | **41.0%** | **27.9%** |

Individual spots don't always follow the averages exactly. For example, CO at
25bb calls a BN jam slightly more often than a BB jam. Trust the trend, not the
decimal.

### Range shapes

- **BN 15bb vs BB jam (call 42.6%).** It calls pairs 77+, suited aces A5s and up,
  KTs+, QTs+, AKo and AQo. It folds the weak part of the min-raise range: offsuit
  broadways and connectors (KTo, QTo, JTo, K9o, T9o, J8o…), low suited Kx/Qx/Jx,
  suited connectors (87s, 76s, 86s) and A3o/A2o. Suited connectors fold here even
  though they play well post-flop, because only equity counts against a jam. Hands
  like small pairs, A4s–A2s, AJo and KQo aren't in the BN's 15bb min-raise range
  at all (they're handled differently first-in).
- **UTG 15bb vs UTG+1 jam (call 41%), the tightest spot.** It calls AA down to
  about 88, AK, AQ (suited and offsuit) and AJs. It folds hands that look strong:
  ATs and lower suited aces, KQs, KJs, KTs, AJo, KQo, 77 and 66. A jam with seven
  players left behind is very strong.

## Mid stack: open vs a non-all-in 3-bet (25–40bb)

Now there are three options: **jam, call or fold**. At these depths the solver's
only 4-bet size is **all-in**. The 3-bet sizes in the charts are larger from the
blinds (about 3–3.5x) than from IP 3-bettors (about 2.75–3.25x).

### Position relative to the 3-bettor is the big split

| Opener is… | Jam | Call | Fold |
|---|---|---|---|
| **IP** (3-bet came from a blind) | 13.2% | **48.1%** | 38.7% |
| **OOP** (3-bet came from a later seat) | **22.8%** | 35.5% | 41.7% |
| All spots | 19.0% | 40.5% | 40.5% |

- **IP:** fold less and **call more**. Position lets you realize equity post-flop,
  so you flat and play.
- **OOP:** **4-bet much more** and call less. Flatting out of position realizes
  equity poorly, so hands that continue prefer to get it in now.

By opener seat:

| Opener | IP vs blinds (jam / call / fold) | OOP (jam / call / fold) |
|---|---|---|
| BN | 12.7 / 44.5 / 42.8 | — |
| CO | 13.1 / 45.9 / 41.0 | 20.3 / 37.1 / 42.6 |
| HJ | 12.8 / 49.8 / 37.5 | 20.7 / 38.1 / 41.2 |
| LJ | 12.5 / 51.0 / 36.5 | 21.8 / 37.3 / 40.8 |
| UTG+2 | 12.9 / 50.9 / 36.2 | 22.2 / 37.9 / 39.9 |
| UTG+1 | 13.5 / 49.1 / 37.4 | 22.7 / 37.3 / 40.0 |
| UTG | **15.2** / 45.6 / 39.3 | **25.0** / 30.2 / 44.7 |

UTG jams the most in both cases because it has the strongest range. OOP jam
frequency rises steadily as the opener's seat gets earlier. The BN folds the most
to blind 3-bets because its opening range is the widest.

### Stack depth pulls IP and OOP in different directions

| | 25bb | 30bb | 40bb |
|---|---|---|---|
| IP jam | 16.7% | 12.7% | 10.3% |
| IP call | 44.6% | 48.1% | 51.6% |
| IP fold | 38.7% | 39.2% | 38.1% |
| OOP jam | 23.0% | 22.6% | 22.9% |
| OOP call | 44.2% | 39.2% | **23.0%** |
| OOP fold | 32.8% | 38.2% | **54.1%** |

- **IP, deeper → jam less, call more.** A bigger stack makes taking the flop in
  position more valuable and a jam riskier, so jams turn into flats. Fold stays
  ~38–39%.
- **OOP, deeper → the jam share stays ~23%, but calls collapse into folds.** With
  more chips behind there's more post-flop betting to survive out of position, so
  equity realization gets worse. A jam realizes all its equity at once, which is
  why the jam share doesn't move.
- **Rule of thumb:** IP, 4-bet more when short and call more when deep. OOP, call
  more when short and fold more when deep.

### Which hands jam and which call

| Jam (all-in 4-bet) | Why |
|---|---|
| **Mid–small pocket pairs** | Decent equity against the hands that call a jam, but they miss most flops and play badly post-flop. All-in banks their equity |
| **Big offsuit Ax** (AQo–ATo) | Good equity vs calls and they block AA/AK, but offsuit and easily dominated, so poor playability |
| **Small suited Ax** (A5s–A2s) | Ace blocker plus equity, yet weak post-flop as one-pair hands |

| Call | Why |
|---|---|
| **AA, KK** | Strong enough to flat. They don't need protection and they keep the 3-bettor's bluffs in |
| **Suited connectors, suited broadways, big suited Ax** | Playability: they make flushes, straights, strong draws and good top pairs, and they realize equity well post-flop (especially IP) |

How often each hand jams or calls shifts with stack depth and relative position.
The principle is that **raw equity without playability → jam; playability →
call**.

### Selected spots (jam / call / fold %)

| Spot | 25bb | 40bb |
|---|---|---|
| BN vs BB (IP) | 12.4 / 45.4 / 42.2 | 8.8 / 45.4 / 45.7 |
| BN vs SB (IP) | 21.1 / 33.1 / 45.8 | 10.4 / 52.1 / 37.5 |
| CO vs BB (IP) | 12.2 / 49.6 / 38.2 | 9.6 / 46.8 / 43.6 |
| LJ vs BB (IP) | 13.2 / 49.0 / 37.8 | 7.8 / 56.2 / 36.0 |
| UTG vs BB (IP) | 17.2 / 44.5 / 38.3 | 10.0 / 49.5 / 40.5 |
| CO vs BN (OOP) | 22.9 / 38.3 / 38.8 | 18.0 / 30.9 / 51.0 |
| LJ vs HJ (OOP) | 21.8 / 42.7 / 35.5 | 19.3 / 24.7 / 56.0 |
| UTG vs UTG+1 (OOP) | 22.5 / 37.8 / 39.7 | **26.1 / 9.7 / 64.2** |

Against the SB, openers jam noticeably more than against the BB (BN 21.1% vs
12.4% at 25bb, and the same for every opener at 25bb). This is consistent with
the SB 3-betting a wider range, for the same reason the SB's rejams are weaker.

### Range shapes

- **BN 25bb vs BB 3-bet (12.4 / 45.4 / 42.2).** It jams AKs, AKo, AQo, AJo, most
  ATo, A5s–A2s, 44 and 33. It flats AA and KK, QQ down to about 55, AQs–A6s,
  nearly all suited Kx, suited broadways, T9s/98s/87s/76s, and KQo, KJo, QJo. It
  folds weak offsuit hands (K9o, Q9o, J9o, T9o and below), A3o/A2o and the bottom
  of the suited range (Q7s-, J7s-, 97s-, 86s, 75s, 65s, 54s).
- **BN 40bb vs BB 3.5x (8.8 / 45.4 / 45.7).** Same skeleton, but the jams shrink to
  AK, AQo, part of AJo, A5s/A3s/A2s and a few pairs. AA–QQ, suited Ax/Kx, suited
  broadways and KQo/KJo/ATo flat.
- **CO 25bb vs BN 2.75x, OOP (22.9 / 38.3 / 38.8).** The jam range is wide: AKs,
  AQs, AKo, AQo, AJo, KK, QQ, most mid and small pairs (JJ–TT, 88–77, 44, with
  66/55 mixed) and A7s–A4s. AA still flats, along with AJs–A8s, A3s/A2s, suited
  Kx, QJs–Q9s, JTs, J9s, T9s, 99, 87s, 86s, 76s, 65s, 54s, KQo and KJo. Most
  offsuit broadways below KJo and offsuit A8o–A5o fold.
- **UTG 40bb vs UTG+1 3.25x, OOP (26.1 / 9.7 / 64.2), the extreme.** The jams are
  mostly value: AA–TT and AK, plus slices of suited aces. Only a sliver flats
  (AQs, 55, 76s, 65s and slices of 99–66). **AQo, AJo, ATo, KQo, KJs and ATs–A6s
  all fold.** Deep, OOP, against an early 3-bet with many players behind, calling
  almost disappears.

## Big stack: open vs a non-all-in 3-bet (60–80bb)

### All-in 4-bets give way to sized 4-bets

At 60–80bb the solver mostly stops jamming and 4-bets to a non-all-in size.

| Opener is… | Jam | Sized 4-bet | **Total 4-bet** | Call | Fold |
|---|---|---|---|---|---|
| **IP** vs blinds | 0.95% | 6.11% | **7.06%** | **55.4%** | 37.5% |
| **OOP** vs later seats | 2.17% | 18.23% | **20.40%** | 37.1% | 42.5% |

Comparison with 25–40bb:

| | 25–40bb | 60–80bb |
|---|---|---|
| IP total 4-bet | 13.2% (all jams) | 7.1%, **roughly half** |
| IP call | 48.1% | 55.4% |
| OOP total 4-bet | 22.8% (all jams) | 20.4% (18.2% sized + 2.2% jam) |
| OOP call | 35.5% | 37.1% |

- **IP 4-betting roughly halves; OOP 4-betting dips only modestly.** (The book's
  text quotes the OOP figure as falling to 18.23%, which counts the sized 4-bets
  only. Including jams it's 20.4%.)
- **Calling rises in both cases.** Bigger stacks make post-flop play more
  attractive, especially in position. Many hands would rather see a flop than
  4-bet, get 5-bet, and fold away the equity they've already invested.
- The OOP call rate isn't a straight line: it fell to ~23% at 40bb but sits at
  ~37% at 60–80bb, where sized 4-bets exist. Don't extrapolate the 25→40bb
  collapse to deep stacks.

By opener seat (total 4-bet / call / fold):

| Opener | IP vs blinds | OOP |
|---|---|---|
| BN | 7.95 / 48.6 / 43.5 | — |
| CO | **8.83** / 52.6 / 38.6 | 18.45 / 38.7 / 42.9 |
| HJ | 7.13 / 56.4 / 36.5 | 18.95 / 41.0 / 40.1 |
| LJ | 7.38 / 57.2 / 35.5 | 19.17 / 39.1 / 41.7 |
| UTG+2 | 6.53 / 57.6 / 35.9 | 19.89 / 38.0 / 42.1 |
| UTG+1 | 5.83 / 57.7 / 36.5 | 20.55 / 36.0 / 43.5 |
| UTG | 5.83 / **58.1** / 36.1 | **22.03** / 34.9 / 43.1 |

IP against the blinds, late openers 4-bet the most and EP openers call the most.
OOP it flips, and UTG 4-bets the most.

### Why the blinds must 3-bet bigger when deep

Deep and in position, the opener has a big incentive to flat. If the blinds keep
their 3-bets small, the opener can call a very wide range and realize equity with
hands that would fold to a proper size. So the blinds should **size up their
3-bets as stacks get deeper**. The chart frequencies assume they do.
*Exploit:* against blinds who 3-bet small when deep, flat wider in position.

### After you 4-bet: facing a 5-bet

This is simple: **call with premiums and fold the blocker-type bluffs** (the Ax/Kx
hands you 4-bet mainly for their blockers).

### EP vs the blinds: you barely need to 4-bet

The blinds' 3-bet ranges are very **polarized** (strong value plus bluffs). Against
that, few IP hands gain from 4-betting. Value hands do better calling and letting
the bluffs keep firing, and medium hands don't want to 4-bet into the value part.
An EP opener can therefore play an almost **no-4-bet strategy** against blind
3-bets.

### Range shapes (60bb, 2.3x open; jams and sized 4-bets lumped as "4-bet")

- **BN vs BB 3-bet, IP (4-bet 7.4 / call 52.4 / fold 40.2).** **AA is a pure flat.**
  The 4-bets are a thin mix: AKs, most KK, part of AKo, slivers of AQo/TT/99, and a
  few small pairs and low suited hands. The call range is huge: essentially every
  suited ace and suited king, most suited queens and connectors down to 53s–64s,
  the pairs, offsuit broadways and AJo/ATo/A9o. It folds weak offsuit hands (K9o
  and below, Q9o, J9o, T9o, 98o, 87o, most A8o–A2o) and the very bottom of the
  suited range.
- **CO vs BN 3-bet, OOP (4-bet 18.3 / call 39 / fold 42.8).** **Here AA is a pure
  4-bet**, along with KK, QQ, JJ, AKs and much of AK/AQo. TT and part of 99 also
  4-bet. The bluff 4-bets are blocker hands such as KJo, K4s and A2s/A3s. It calls
  the other suited aces, KQs–K5s, QJs–Q9s, JTs, J9s, T9s, T8s, 98s, 87s, 76s, 65s,
  54s, 88–22, AJo, ATo and KQo. It folds QJo, KTo, QTo, JTo, A8o–A5o and the weaker
  suited hands.
- **UTG vs BB 3-bet, IP (4-bet 4.3 / call 59.5 / fold 36.2).** This is a
  near-pure flatting strategy. AA, AK, KK–TT, most suited aces, KQs, KJs, QJs,
  T9s, 87s, 76s, 65s and 44 call, and 99–55 mix calls with folds. The 4-bets are slivers plus a
  blocker bluff like K6s. AJo, ATo and KQo fold.

Compare AA in the two 60bb spots. In position against a polarized blind 3-bet it
flats. Out of position against a wide BN 3-bet it 4-bets.

## Trend summary

| Depth | Your options | IP vs blinds | OOP vs later seat |
|---|---|---|---|
| 10–25bb vs a jam | Call / fold | Call ~45% overall; 58% at 10bb → 31% at 25bb | (same; no post-flop) |
| 25–40bb | Jam / call / fold | Jam 13%, call 48%; deeper → fewer jams, more calls | Jam 23%, call 35%; deeper → calls collapse to folds |
| 60–80bb | Sized 4-bet / jam / call / fold | 4-bet 7%, call 55% | 4-bet 20%, call 37% |

## Takeaways for the table

1. **Facing a short-stack rejam, only equity matters.** Call the top of your range
   by equity against the jam range. Defend less as the jam gets deeper, and less
   against earlier seats. Call SB jams a bit lighter than BB jams.
2. **Position on the 3-bettor decides between flatting and 4-betting.** IP, call a
   lot. OOP, 4-bet (jam at 25–40bb) or fold more, and fold even more as stacks
   deepen.
3. **Jam the hands with equity but no playability** (small/mid pairs, AQo–ATo,
   A5s–A2s). **Flat the playable hands** (suited connectors, suited broadways, big
   suited aces) and often AA/KK.
4. **At 60bb+, 4-bets become sized, IP 4-betting about halves, and everyone calls
   more.** EP openers can almost stop 4-betting IP against the blinds' polarized
   3-bets.
5. **Facing a 5-bet, call premiums and fold blocker bluffs.**
6. **If you're a blind and stacks are deep, 3-bet bigger.** Otherwise the opener
   flats you profitably with half the deck.
7. **A ≈0 cEV call is a fold in a tournament.** ICM makes it slightly −$EV.
