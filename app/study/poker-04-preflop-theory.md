---
title: "Poker 04 — The Theory of Pre-flop Play"
summary: "Modern Poker Theory ch. 4: blinds, antes and win rates, the value of complex strategies vs push/fold, the variables that shape RFI ranges, rake and bunching effects, limping, open pushing, pre-flop bet-sizing and general pre-flop heuristics."
order: 104
audience: bravosierra99
---

# Poker 04 — The Theory of Pre-flop Play

*Study guide to Chapter 4 of* Modern Poker Theory *(Michael Acevedo). Read the
chapter for the range charts and the EV/frequency diagrams; this guide is the
skeleton you should be able to rebuild from memory.*

## Why pre-flop matters

A pre-flop mistake is a **systematic error**: it is carried forward and distorts
every later decision in the hand (flop, turn, river). Noticing it later rarely
lets you undo it. Sound pre-flop ranges are the backbone of everything else.

## Blinds, antes and win rate

**Why anyone plays anything but AA:** there is dead money in the pot. Without
blinds and antes everyone would wait for aces (or, deep enough, hands with the
implied odds to crack them). The blinds force a fight.

**Win rate** measures skill edge over the player pool in **bb/100**. If everyone
at the table is equally skilled, everyone's win rate is zero and, in raked
games, all of them lose the rake.

> win rate (bb/100) = winnings ÷ big blind ÷ hands played × 100

Live example: ~300 hands per 10-hour session, 5 days a week, 4 weeks a month →
~6,000 hands a month, **72,000 a year**. $100,000 won in a year at $5/$10 is
10,000bb over 72,000 hands ≈ **13.9bb/100**.

- **Game selection.** Win rate depends on who you play. 2bb/100 at $10/$20 is
  $40 per 100 hands; 10bb/100 at $2/$5 is $50 per 100 hands — the smaller game
  pays more *and* swings less, because variance bites hardest where your edge is
  thin.
- **Sample size.** 100,000 hands gives a rough idea; about 1,000,000 are needed
  for statistical significance.
- **Live vs online.** Live win rates are much higher because live games are
  softer. An online multi-tabler can play ~3,000 hands a day (~720,000 a year) —
  ten live-years of experience in one — which alone makes the average online
  regular tougher.

### The pot you are fighting for

At 6-max with no ante there are 1.5bb in the pot each hand = **150bb/100**.
Nobody can win all of it: some hands never fold, and re-raises force you to fold
and forfeit your equity. Split evenly, each of six seats would earn 25bb/100,
but position skews this heavily.

Typical online 6-max win rates by seat (bb/100):

| Seat | Large winner | Decent winner | Break-even | Slight loser | Big loser |
|---|---|---|---|---|---|
| BB | −30 | −35 | −44 | −45 | −66 |
| SB | −12 | −15 | −21 | −21 | −32 |
| EP | 12 | 10 | 7 | 6 | −5 |
| MP | 18 | 15 | 12 | 8 | −4 |
| CO | 25 | 20 | 18 | 15 | 7 |
| BN | 35 | 30 | 28 | 24 | 17 |
| **Average** | **8** | **4** | **0** | **−2** | **−14** |

- **The blinds always lose.** The BB starts each hand at −100bb/100 and the SB
  at −50bb/100; the job there is to lose *less* than that, not to win.
- **The BN earns the most** because it plays the most hands profitably; win rate
  falls the further you sit from it. Even a big loser is positive on the BN and CO.
- **Most players lose.** You must claw back the −150bb/100 the two blind seats
  start with (−100 BB, −50 SB; spread over six seats that's −25bb/100 overall)
  *plus* rake (typically 5–10bb/100; at online micro-stakes it can be high enough
  that even strong players can't win — check rake structure, rakeback and VIP
  deals before choosing a site). In ante games you also post the ante: a 12.5%
  ante costs 12.5bb/100.

### Maximising win rate = always take the highest-EV action

Your win rate is the sum of the EVs of every hand in every seat. Folding is 0,
so play a hand only if some action is non-negative — and then pick the **best**
action, not merely a profitable one.

Worked example — 9-max MTT, 12.5% ante, 20bb effective, folded to the SB
(options: push, raise to 2.5bb, limp, fold). Win rate of each action in bb/100:

| Hand | Push 20bb | Raise 2.5bb | Limp | Best |
|---|---|---|---|---|
| AA | 583 | **719** | 676 | Raise |
| AJo | **312** | 290 | 301 | Push |
| Q7s | 68 | 72 | **74** | Limp |
| 72o | −63 | −25 | −4 | Fold (0) |

- Shoving AA is +EV but costs **136bb/100** against raising — a bigger mistake
  than shoving 72o (−63). **"It's +EV" is not a justification**; every action
  must be compared with all the alternatives.
- Summed over all 1,326 combos, the SB captures ~33% of the 2.625bb pot
  (**88bb/100**) and the BB ~67% (175bb/100). Any deviation from the highest-EV
  action against a GTO opponent can only lower that.
- In cash games win rate converts directly to money. In tournaments chips aren't
  linear in dollars, but win rates still reveal skill and leaks.

## Complex strategies vs push/fold

Solver comparison at 8–25bb, 0.5/1 blinds, no ante. Hero may fold, limp, raise
to 2bb / 2.5bb / 3bb, or push:

- **SB (3-max):** BN folds, Hero is **OOP** vs the BB.
- **BN (heads-up):** Hero is **IP** vs the BB.

With push/fold only the two spots are identical; the extra options are what
position gets to use.

Averages across 8–25bb:

| | Push/fold only | SB, OOP (3-max) | BN, IP (HU) |
|---|---|---|---|
| EV (% of pot) | 38.22% | 42.84% | 52.82% |
| EV (bb/100) | 57.32 | 64.25 | 79.23 |
| Fold | 51.63% | 35.97% | 9.81% |
| Push | 48.37% | 25.98% | 12.38% |
| Limp | — | 16.32% | 58.83% |
| Raise 2bb | — | 8.39% | 18.98% |
| Raise 2.5bb | — | 8.08% | 0% |
| Raise 3bb | — | 5.26% | 0% |

What it shows:

- **More options = more EV**: +4.62% of the pot (~7bb/100) OOP, +14.6%
  (~22bb/100) IP. The loss from push/fold is tiny when very shallow and grows
  with stack depth, **especially in position**.
- **Push/fold folds the most**, so it caps how many hands you can play
  profitably — and its fold frequency climbs as stacks deepen.
- **Pushing:** dominant for the BN under 10bb, almost unused above 17bb (3.88%
  at 15bb, 1.70% at 17bb, 0.69% at 20bb, 0.06% at 25bb). The SB pushes far more
  because being all-in **cancels the disadvantage of being OOP**; for the SB,
  pushing stays vital up to ~17bb.
- **Limping:** the BN's dominant play (≈59% vs ≈16% for the SB) and, per the
  book, roughly as important at every depth. For the SB limping grows as stacks
  deepen and wide open-pushing stops being possible.
- **Raise size:** the BN only ever min-raises. Bigger sizes appear only OOP:
  min-raise dominates short, **2.5x from 15bb**, 3x appears at 20bb and dominates
  at 25bb. **OOP, size up as stacks get deeper**; IP, bigger sizes add little.

**Conclusions**

1. Extra options raise your expectation, but rarely-used, low-EV options can
   cost more in execution errors than they add. **Simplify as far as you can
   without hurting EV.**
2. Practical simplifications: push/fold is fine at ≤10bb in most spots; the BN
   can simply never push with 15bb+ at negligible cost; but **removing BN limps
   heads-up costs real EV**.
3. **Corollary — against a better player, simplify.** Complexity favours whoever
   handles it better. Getting AJs in pre-flop against TT is ~50% no matter who
   is sitting across from you.

## Playing first in

Knowing what to open when folded to is arguably the most valuable thing to
learn. Like chess openings, memorised baseline ranges free your attention for
harder decisions, let you recognise when to widen or tighten, and let you
extrapolate to new spots. Well-built ranges also play better post-flop (board
coverage, playability). The baseline is a **starting point**: once you know what
balanced looks like, opponents' imbalances become visible.

**A typical online 6-max cash EP (LJ) RFI — 2.5x, ~17.65% of hands:** 44+, all
suited aces, K8s+, Q9s+, JTs, ATo+, KJo+, QJo. Note what is absent: **JTo is not
a standard EP open**, nor are 22–33, suited connectors below JTs, or A9o.

### Variables that shape pre-flop ranges

**1. Absolute hand strength** (strength in a vacuum)

| Component | Why it matters |
|---|---|
| **High card value** | Ax > Kx > Qx … |
| **Pocket pairs** | Higher is better (KK > 55) |
| **Suitedness** | More raw equity *and* better playability. A♥5♥ can flop nut flushes, and a two-card flush is disguised and gets paid; a four-flush board with one ace doesn't |
| **Connectedness** | More, and more nutty, straights. T9 makes four straights (three are the nuts), T8 three (two nuts), T7 two (one nut) |

Good hands have **at least two** of these: 87s lacks high cards but is suited
and connected; AKo lacks suitedness but has maximum high-card value. The earlier
the seat, the more high-card strength is required — at 6-max with no ante the BN
can open Q2s, while the worst queen the LJ opens is Q9s.

**2. Pot size.** More dead money → more hands are profitable. Folded to the BN
with 10bb at a 9-max table: push **46%** with a 12.5% ante (pot 2.625bb), only
**33%** without antes (pot 1.5bb).

**3. Bet-size.** The bottom of your range is barely profitable, so the bigger
you raise relative to the pot, the fewer hands you can play — you lose more each
time a steal fails and you fold to a re-raise.

**4. Likelihood of being raised.** Opponents who under-defend can be opened on
very wide, occasionally with 100% of hands. Good opponents re-raise, deny your
equity, and so cap how wide you can go.

Worked example — Hero opens Q7s to 3bb from the SB, 100bb, pot 1.5bb:

> EV(raise) = 1.5 × %fold + EV(called) × %call − 2.5 × %3-bet

EV when called can't be negative (worst case Hero wins 0% of the pot), so only
3-bets can make the raise lose. With Villain 3-bet-or-fold and Hero folding to
every 3-bet:

> 1.5 × (1 − x) − 2.5x < 0 &nbsp;→&nbsp; x > 1.5 ÷ 4 = **37.5%**

In general, **break-even 3-bet frequency = pot ÷ (pot + amount risked)**. No
sane BB 3-bets 37.5% — and one who did would be wide open to exploitation.

More players behind means more 3-bets. With each player 3-betting ~7%:

> total 3-bet frequency = 1 − (1 − 0.07)^(players behind)

UTG at 9-max (8 behind): 1 − 0.93⁸ ≈ **44%**. Opening Q7s to 2.5x there (ignoring
calls): 0.56 × 1.5 − 0.44 × 2.5 ≈ −0.26bb = **−26bb/100**.

**This is the main reason the BN plays more hands than UTG**: fewer players left
means fewer 3-bets.

**5. Rake.** Rake taken from the pot lowers the profitability of every hand, so
marginal raises and calls turn −EV. The higher the rake, the **tighter** the
ranges, and actions that can win the pot pre-flop take precedence over passive
ones. It is a main reason cash games use larger sizings than tournaments (to
discourage calls); tournament rake is paid with the buy-in, so it doesn't touch
in-game decisions and more passive play is viable.

Heads-up $5/$10, 100bb — no rake vs 4.3% rake capped at $2.20:

| Spot | Action | No rake | Raked |
|---|---|---|---|
| BN first in | Raise 2.5bb | 70.1% | 76.4% |
| | Limp | 18.3% | 6.9% |
| | Fold | 11.6% | 16.7% |
| BB vs 2.5x | 3-bet to 10bb | 19.9% | 22.7% |
| | Call | 55% | 45% |
| | Fold | 25% | 32.3% |

Same pattern both sides: **more raising, less limping/calling, more folding.**

**6. Bunching effect.** Folded hands were disproportionately weak, so the
players still to act are more likely to hold strong ones. After six folds at a
9-max table, the BN must open **tighter** than a BN at a genuinely 3-handed
table. Solver push ranges (12.5% ante, 10–15bb) versus a classic push/fold
calculator that ignores bunching:

| Seat | Push tighter by (average) |
|---|---|
| SB | 4.9% |
| BN | 2.2% |
| CO | 1.7% |
| HJ | 0.9% |
| LJ | 0.3% |

Example: SB with 10bb — the calculator says 58.3%, the 9-max solver 52.1%. The
effect grows with the number of folds in front, so it matters most in the SB and
is negligible in early position. (The table's absolute push percentages don't
match the chapter's other 12.5%-ante push figures — e.g. SB 74.7% at 10bb below —
so it was probably built with a different setup; trust the *deltas*, not the
absolute numbers.)

## Limping

### Open limping

| For | Against |
|---|---|
| Plays more hands for the minimum price | You play post-flop most of the time, and opponents realise equity they would have folded to a raise |
| | **Splits your range early**, leaking hand-strength information |

How a limping range goes wrong: limp only small pairs, weak suited aces and
suited connectors and your hits and misses are transparent by flop. Limp only
medium hands and opponents raise freely because you can never limp/re-raise. Add
strong hands for balance and your raising range gets weaker — and your
limp/call range is *still* capped on many flops, since the best hands
limp/re-raised.

Where it belongs: solvers limp mainly **blind vs blind in rake-free games**
(tournaments). In practice populations under-defend their blinds, over-fold to
c-bets, 3-bet too little and don't peel enough, so **raising keeps a lot of
extra value and stays the default**. The author expects limping to spread,
especially in tournaments; the book uses it only where it adds significant EV.

### Facing limpers

Open limps are rare online above micro-stakes and common live — same cause both
places: weak players. **An open limp from any seat other than the SB marks a
player who is probably not strong.** Adjust to the type:

| Limper type | Adjustment |
|---|---|
| **Weak-passive** (rarely raises, check-folds when missing) | Isolate very wide and take pots down post-flop. How wide depends on the players behind: if they 3-bet, raise about your normal RFI range for that seat; if they call a lot (multiway), favour suited connectors, pocket pairs, Axs; if they're passive and unaware, almost anything playable |
| **Sticky** (won't fold) | Play hands that flop good top pairs; value-bet any top pair and most second pairs for three streets. Semi-bluffing is fine, but give up when the draw bricks and never run stone-cold bluffs |
| **Aggressive** (check-raises, leads) | Don't isolate wide — strong hands that can take heat. Check medium hands for pot control and bluff-catch; be willing to stack off with good-but-not-great hands |
| **Trappy** (limps AA/AK to limp-raise) | Over-limp suited/connected hands and small pairs (others fear the limp-raise, and his range is face-up post-flop). When you raise, polarise: hands that can stand a 3-bet plus good-blocker hands you happily raise/fold |

## Open pushing

Shoving is the most powerful bet: **every hand realises 100% of its equity**.
The cost is risking the whole stack and losing the option to fold your weak
hands to a 3-bet. So **the more chips you have and the more players behind, the
less you should shove.**

- 9-max, 12.5% ante, 10bb: UTG pushes **14.4%**, the SB **74.7%** (eight players
  to get through vs one).
- BN, same game: **41.5%** at 12bb, **37.2%** at 15bb — more at risk, tighter.
- Under 10bb you can open push from any seat.

Maximum stack depth at which open pushing is still used (MTT, 12.5% ante):

| SB | BN | CO | HJ | LJ | UTG+2 | UTG+1 | UTG |
|---|---|---|---|---|---|---|---|
| 25bb | 20bb | 15bb | 15bb | 15bb | 12bb | 12bb | 12bb |

Range shapes:

| Strategy | Range | Contents |
|---|---|---|
| Shove or fold (whole range shoved) | **Linear** | The top hands — best equity when called |
| Shoving range within shove/raise/fold | **Condensed** | Too good to raise/fold, not good enough to raise/call, decent equity when called: Axs, Q9s, 87s |
| Non-all-in raising range within shove/raise/fold | **Polar** | Premiums happy to raise/call (KK) + blocker hands that raise/fold (Axo) |

## Pre-flop bet-sizing guidelines

| Factor | Direction | Why |
|---|---|---|
| Earlier position | Smaller | More players can wake up with a re-raising hand |
| Wider range | Bigger | More of their hands have the equity to call the same size vs a wide range |
| Players behind have rejam stacks (<25bb) | **Min-raise** | Gives the worst possible price on their all-in |
| Deeper stacks | Bigger | Speculative hands get better implied odds — discourage calls, especially from players with position |
| Polarised re-raise when villain mostly re-raises or folds | Smallest possible | Minimises the loss on your raise/fold hands |
| OOP | Bigger | Lowers the SPR, shrinking the IP player's advantage |
| IP | Smaller | You keep the positional edge even when called — but small sizes give callers a better price to defend more hands |

- **Facing** a bet or raise: the bigger it is, the fewer hands you need to
  defend to stay unexploitable.
- **Vary size by situation, never by hand.** Different sizes for different
  positions or stack depths are fine; sizing by hand strength hands out
  information that will be used against you.
- Similar sizes have nearly identical EV (2.25bb vs 2.3bb is noise). Solvers are
  indifferent *provided the opponent responds correctly* — so in practice **the
  best size is the one that drags opponents into an unfamiliar part of the game
  tree** where they make the most mistakes.
- There is no solved "correct" open size; the goal is low risk with high fold
  equity, and exploitative sizing vs specific opponents is always available.

## General pre-flop heuristics

1. **Play a range that is strong relative to the hands still to act.** If
   someone has already entered voluntarily, it must also be strong against
   *their* range — the CO's raising range over an UTG limp is tighter than its
   RFI range. Each seat plays the hands with positive expectation against the
   remaining players, rake included.
2. **Mixed-strategy hands are threshold hands.** The worst hands in a GTO
   opening range are 0EV, indifferent between raising and folding (card removal
   makes mixing common). Against weak opponents who don't fight back enough,
   these become clear raises and you can add more.
3. **When you open wider than normal as an exploit and get 3-bet, over-fold.**
   The exploit was that 3-bets are rare; fold the off-range hands and even the
   bottom of your usual calling range.
4. **For marginal opens, look at the BN, SB and BB** — they give the most
   action. If they're tight, steal freely.
5. **Randomise between equal-EV actions** to stay unpredictable: an RNG online;
   live, a clock's second hand or card colour/suit (top card red = 50%, first
   card a chosen suit = 25%). Randomising matters **less live**: soft games make
   decisions more binary, live reads break ties, and nobody gathers enough hands
   to decode your frequencies.
6. **Widen exploitatively from the threshold outward.** First take the mixed
   hands to 100% (A9o played 25% → always), then add their neighbours (A8o, A7o)
   — not random junk like Q4o. This is harder to spot, and if you're wrong the
   added hands still have the right blockers and lose less.
7. **Think a few steps ahead.** If you wouldn't know what to do facing a
   re-raise, take the passive line: call instead of 3-betting a medium hand,
   check instead of betting post-flop. Before opening, ask who can 3-bet, what
   you do then, and what happens if a 4-bet gets 5-bet. A hand too good to
   4-bet/fold should just call the 3-bet.

**Two kinds of leak**

- **Wrong frequencies** — easiest to find and fix, especially online where HUD
  stats expose it. If the optimal LJ RFI is ~17% and you open 22%, cut the extra
  5% if you're being punished for it.
- **Wrong hands at the right frequency** — much harder to see, and the main
  reason regulars stall when moving up: the stats look fine but the range
  composition isn't.

## Takeaways for the table

1. Don't ask "is this +EV?" — ask "is this the *highest*-EV option?" Shoving
   aces at 20bb is the bigger mistake than shoving 72o.
2. Most of your profit comes from the BN and CO; in the blinds the goal is to
   lose less than the blind you posted.
3. Open tighter the more players are behind and the higher the rake; when raked,
   prefer raising or folding to limping and calling.
4. Choose your raise size by position, stack depth and range width — never by
   hand strength. Min-raise into rejam stacks; go bigger when deep and OOP.
5. Shove less as your stack grows and as more players remain; under ~10bb
   push/fold is fine, and it is a good equaliser against a better player.
6. A non-SB open limper is usually weak — identify which kind before choosing
   between isolating wide, value-betting relentlessly, tightening up or
   over-limping.
7. Exploit by pushing threshold hands to 100% and adding their neighbours, and
   fold more than usual when the 3-bet you didn't expect arrives.
