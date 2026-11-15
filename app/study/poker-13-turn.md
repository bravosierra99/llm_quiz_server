---
title: "Poker 13 — GTO Turn Strategies"
summary: "Modern Poker Theory ch. 13: what drives turn decisions, key strategy lines after a flop check-through (x/x) and a c-bet and call (x/b/c), range shapes on the turn, turn-card categories, and how each turn card changes who bets, how often and how big on 9♥8♥4♦."
order: 113
audience: bravosierra99
---

# Poker 13 — GTO Turn Strategies

*Study guide to Chapter 13 of* Modern Poker Theory *(Michael Acevedo). Every
example is the BB defending against a UTG open at 40bb, continuing the four flop
studies of the previous chapter. Read the chapter for the bar charts and
per-card heatmaps; this guide pulls out the numbers and, more importantly, the
reasons behind them.*

## Turn play is flop play with more history

A turn decision rests on the same four inputs as a flop decision: **pot size,
effective stacks, the ranges and the board**. Pot and stacks are given; the
real work is rebuilding the ranges from the action and seeing how the new card
reshapes them.

- A solver needs only **ranges, board, stacks, pot and a betting abstraction**.
  It has no idea who bet last or whether the flop went x/x or x/b/c. **Betting
  history matters to humans only because it tells us what the ranges are.**
- You can't memorise solver output for every line, or compute GTO per combo at
  the table. Instead learn the **key strategy lines**, the **range shapes** they
  produce, and how runouts move equity around. Each spot is a new puzzle made of
  familiar pieces.
- Getting good at that puzzle takes **deliberate practice**: focused,
  goal-driven review rather than mindless volume.

## Key strategy lines

**Key strategy lines** are the lines that happen most often and have the
biggest effect on long-term EV. You don't need every route to the turn; these
eight nodes cover most of what matters.

| Flop line | Turn node | Notation |
|---|---|---|
| Flop checks through | OOP acts first | x/x/? |
| | IP faces a turn bet | x/x/b/? |
| | IP after OOP checks again | x/x/x/? |
| | OOP faces IP's stab | x/x/x/b/? |
| IP c-bets, OOP calls | OOP acts first (donk) | x/b/c/? |
| | IP faces a turn donk | x/b/c/d/? |
| | IP after OOP checks | x/b/c/x/? |
| | OOP faces the second barrel | x/b/c/x/b/? |

The four study flops: **A♥Q♦3♠** (dry, ace-high), **Q♥J♥T♥** (monotone,
connected), **9♥8♥4♦** (two-tone, dynamic) and **J♠6♥6♦** (paired, static).
(The text sometimes gives the ace-high flop other suits; the solver tables use
the rainbow A♥Q♦3♠.)

## After the flop checks through (x/x)

### Range shapes: the flop picture, flipped

- **IP's check-back range** — at equilibrium it still covers the board and is
  fairly balanced, but it is **somewhat capped and much more condensed** than
  the c-betting range, because most strong hands bet the flop.
- **OOP's range** — with no flop donk range, OOP still holds its **entire
  pre-flop calling range**: **far wider** than IP's and **uncapped**.
- So OOP is now the **more polarized** player and IP the more condensed one —
  the reverse of the flop. That is why **OOP builds a turn betting (probe)
  strategy** after x/x.

### When IP's check-back range is unbalanced

A human check-back range usually lacks the solver's board coverage: heavily
capped on many turns and over-represented on others. OOP's best response
punishes it.

- **Never checking back sets on a 9-8-4 flop (99, 88).** On a blank 2♣ turn
  OOP's betting jumps from 27% to 77% and IP's EV on that card falls from 54% to
  41% of the pot. If IP also never checks back a flush draw or any strong hand,
  a flush-completing 5♥ drops IP's EV to **11%**. (The book runs this on a
  9♥8♥4♥ version of the flop and the digits don't match the 9♥8♥4♦ charts below
  — keep the direction, not the numbers.)
- **Checking back A♥Q♦3♠ with only made hands.** Players know this flop should
  be c-bet a lot but still balk at betting weak Ax, KK, Qx, JJ and TT. The
  check-back is then nearly all made hands with little air — close to **face
  up** — and OOP can play accurately against it.
- **Slipping AA into that check-back doesn't fix it.** With an ace on board and
  an ace in OOP's hand, only **one combo of AA** is left. OOP can play its Ax
  aggressively without much fear, and can **check/fold comfortably against a
  delayed c-bet**.

### OOP first to act

| Flop | x/x frequency | OOP EQ | OOP bets | Sizes: 1.2x / 2/3 / 1/3 |
|---|---|---|---|---|
| A♥Q♦3♠ | 0.8% | 30% | ~14% | 6 / 5 / 2 |
| Q♥J♥T♥ | 0.1% | 37% | ~15% | 7 / 3 / 5 |
| J♠6♥6♦ | 33% | 44% | ~29% | 18 / 5 / 6 |
| 9♥8♥4♦ | 33% | 48% | ~58% | 12 / 13 / 32 |

- On **A♥Q♦3♠ and Q♥J♥T♥** IP almost never checks back at equilibrium — its
  turn range is just 1–1.4 combos, a tiny slice of many different hands. Copying
  such micro-mixes is impractical and unnecessary.
- **9♥8♥4♦**: OOP probes most, mainly **small (1/3)**, because many turns help
  its wide range.
- **J♠6♥6♦**: OOP probes less but mostly **overbets (1.2x)** — a polarized range
  on a static board.
- Within each flop, the strategy swings hard by turn card (see the case study).

### IP facing the turn probe (x/x/b)

| Spot | Raise | Call | Fold |
|---|---|---|---|
| 9♥8♥4♦ vs 1/3-pot | ~20% | 56% | 24% |
| J♠6♥6♦ vs 1.2x-pot | 0% | 48% | 52% |

On 9♥8♥4♦, OOP bets more often and smaller, so its betting range is
**condensed** and IP holds enough strong hands to **raise** about one time in
five (the text says 19%, the chart 20%). On J♠6♥6♦, OOP's overbet range is
**polarized** and IP has few strong hands by comparison, so it **never raises**
— it just calls or folds.

### IP after OOP checks again (x/x/x)

A common node: 14% of all hands on 9♥8♥4♦, 24% on J♠6♥6♦. OOP's double-checked
range has 41% equity on both.

| Flop | IP bets | Main size |
|---|---|---|
| 9♥8♥4♦ | ~49% | 2/3 pot (25%), then 1/3 (19%), 1.2x (4%) |
| J♠6♥6♦ | ~54% | 1/3 pot (44%) |

- **Dynamic board → bigger stab.** On a board as wet as 9♥8♥4♦, OOP would have
  bet most strong hands by now, so after two checks it is weak and IP can use
  2/3 pot.
- **Static board → small stab.** On J♠6♥6♦ strong hands stay strong, so OOP can
  slowplay without much risk of being outdrawn, and weak hands rarely improve.
  OOP therefore checks most of its range, which stays **polarized** (traps plus
  junk). A small bet folds out the junk cheaply and risks little against the
  traps.

### OOP facing IP's stab (x/x/x/b)

| Spot | Check-raise | Call | Fold |
|---|---|---|---|
| 9♥8♥4♦ vs 2/3 | ~9% (mostly small, ~2% jams) | 39% | 52% |
| J♠6♥6♦ vs 1/3 | 16% | 39% | 44% |

OOP folds more on 9♥8♥4♦ because the bet is **bigger**. It check-raises more
on J♠6♥6♦ because its range is polarized (the slowplayed traps) and the bet is
small. If IP overbet J♠6♥6♦ instead, OOP would check-raise only ~3%.

## After a flop c-bet and call (x/b/c)

### Range shapes

IP c-bets most of its strong hands *and* its trash, so the c-bet range is
**polarized**. OOP folds most trash and raises some strong hands, so its
calling range arrives on the turn **condensed**. Equities run close (47–53%
either way), but **polarization favours the previous aggressor** and the caller
holds the most condensed range.

### OOP first to act (turn donk)

| Flop | x/b/c frequency | OOP EQ | OOP donks | Main size |
|---|---|---|---|---|
| A♥Q♦3♠ | 24.5% | 53% | ~13% | 1/3 (11%) |
| Q♥J♥T♥ | 43.7% | 48% | ~6% | 1/3 |
| 9♥8♥4♦ | 36% | 52% | ~32% | 1/3 (29%) |
| J♠6♥6♦ | 33.7% | 47% | ~6% | 1/3 |

- Default: **check to the raiser**, because OOP holds the depolarized range.
- As with flop donks, some turns flip the shapes — polarizing OOP and condensing
  IP — and on those OOP leads much more.
- Donks are **small**. After x/x OOP is polarized and uses sizes up to 1.2x pot;
  when it donks (flop, or turn after x/b/c) its range is condensed and it bets
  small. **Range shape drives bet size.**

### IP facing a turn donk (x/b/c/d)

| Flop | Raise | Call | Fold |
|---|---|---|---|
| A♥Q♦3♠ | 32% | 43% | 25% |
| Q♥J♥T♥ | 22% | 58% | 20% |
| 9♥8♥4♦ | 50% (28% all-in) | 22% | 28% |
| J♠6♥6♦ | ~34% | 49% | 17% |

A rare line (1.5–10% of hands). IP has **position and an uncapped range**, so
it **seldom folds and raises a lot**. In real games players donk the flop far
less than they could and auto-check the turn without asking how the card
changed the ranges.

### IP after OOP checks (x/b/c/x)

| Flop | Line frequency | IP bets | Main size |
|---|---|---|---|
| A♥Q♦3♠ | 21% | ~54% | 2/3 (46%) |
| Q♥J♥T♥ | 41% | ~63% | 1/3 (45%) |
| 9♥8♥4♦ | 24% | ~64% | 2/3 (38%) |
| J♠6♥6♦ | 32% | ~57% | mixed, incl. 13% at 1.2x |

- A very common line — probably more so in practice, since most players donk
  far less than the solver.
- After OOP checks twice, **IP is very polarized and OOP condensed**. On turns
  that give IP many more strong hands than OOP, IP sizes up, sometimes to
  **overbets**.
- On **A♥Q♦3♠**, OOP stays capped on most turns, so IP keeps betting **2/3 pot
  with the plan of jamming the river** at a high frequency.

### OOP facing the second barrel (x/b/c/x/b)

| Flop | Bet faced | Check-raise | Call | Fold |
|---|---|---|---|---|
| A♥Q♦3♠ | 2/3 | ~4% (mostly jams) | 53% | 43% |
| Q♥J♥T♥ | 1/3 | 18% | 48% | 34% |
| 9♥8♥4♦ | 2/3 | ~13% (mostly jams) | 44% | 43% |
| J♠6♥6♦ | 1/3 | 14% | 50% | 35% |

OOP is in a tough spot: a real **equity disadvantage** (43–45%), a **very
depolarized** range, and an IP range even more polarized than on the flop.
Against 1/3 pot it folds about a third and raises more; against 2/3 it folds
about 43%.

## Turn-card categories

There are 49 possible turns on every flop, so group them as you did flops. A
card can sit in more than one group.

| Category | Definition |
|---|---|
| **Paired board** | Pairs one of the flop cards |
| **Flush** | Completes a flush |
| **Straight** | Completes an open-ended straight draw |
| **Ace** | A special card that often has a big effect |
| **Overcard** | Higher than the board's top card |
| **Brick / blank** | Doesn't connect with the board in any meaningful way |

**Overcards and undercards** are split further into those that **bring a
backdoor flush draw** and those that don't. The label is only shorthand: the
real question is **whose range the card helps**, both overall and at the top.

## Case study 1 — 9♥8♥4♦ after x/x (BB vs UTG, 40bb)

### The ranges going into the turn

| Hand class | UTG (checked back) | BB |
|---|---|---|
| Strong | 15% | 21% |
| Good | 31% | 27% |
| Weak | 43% | 13% |
| Trash | 11% | 39% |

UTG is **condensed** (74% good or weak); BB is **polarized** (60% strong or
trash) and has more strong hands. BB has the **polarization advantage** on many
turns, hence its high betting frequency.

### How BB bets by hand class

| BB class | Bets | Sizes: 1.2x / 2/3 / 1/3 |
|---|---|---|
| Strong | 77% | 21 / 24 / 32 |
| Good | 54% | ~2 / 4 / 48 |
| Trash | 53% | 15 / 14 / 24 |
| Weak | 43% | 13 / 10 / 20 |

- Strong hands bet most and use most of the big bets.
- **Good hands bet almost only 1/3 pot**; the big sizes belong to the polarized
  part of the range.
- **Trash bets more often than weak hands**: it has no showdown value and makes
  the natural bluff, while weak hands keep some showdown value and check more.

### By turn rank

| Turn | BB bets | Notes |
|---|---|---|
| 5 | 82% | Completes 7-6; BB's best card |
| 2, 3 | 74% | Low bricks |
| 6, 7 | 72% | Complete straights; mostly 1/3 pot |
| 4 | 69% | Pairs the board; mixed sizes |
| T | 58% | |
| 8, 9 | 54–55% | Pair the board; mostly big sizes (1.2x and 2/3) |
| J | 49% | |
| Q | 42% | |
| K | 33% | Mostly 1/3 |
| A | 8% | BB checks 92% |

**By suit:** clubs and spades ~60% bets (16% overbets), diamonds ~56%, **hearts
~53% with only 7% overbets**.

The book's summary: **low cards that complete straights, board-pairing 9s, 8s
and 4s, and hearts are good turns for BB**; **overcards that complete few
straights — aces above all — are good for UTG**, whose range is full of big
cards. Note that "good for BB" is not the same as "BB bets more": the 8 and 9
are favourable yet bet at only an average frequency (with bigger sizes), and
hearts are the suit BB bets *least*.

### EV by turn card

- Average turn: BB has **48% equity but captures 53% of the pot** — it
  over-realizes (EqR ≈ 53 ÷ 48 ≈ 110%).
- **Worst** turns for BB: **offsuit aces (A♠/A♣)**, EV down to **~26%** of the
  pot. **Best**: **offsuit 5s (5♠/5♣)**, EV up to **~64%**.
- EQ and EV move together, but the highest-equity card isn't necessarily the
  highest-EV card — distribution and realization matter as well.

### Same flop, same line, two turns

| Class | UTG on A♠ | BB on A♠ | UTG on 5♠ | BB on 5♠ |
|---|---|---|---|---|
| Strong | 54% | 9% | 6% | 28% |
| Good | 22% | 10% | 31% | 27% |
| Weak | 23% | 25% | 51% | 9% |
| Trash | 1% | 56% | 12% | 36% |

The ace makes over half of UTG's range strong and most of BB's range trash; the
5 does roughly the opposite. One card can redraw the whole range morphology,
and the equilibrium strategies follow.

### Mindset: hands get demoted

A hand that was strong on the flop can be ordinary on the turn. That is
predictable — it happens at a calculable rate — not a curse. Poker is about
**how much equity you have, how it is distributed, and how well you realize it
while stopping your opponent realizing theirs**. Play the new range picture,
not the hand you had a street ago; if you know both ranges you will have the
best of it over time even when you lose a big pot.

## Case study 2 — 9♥8♥4♦ after x/b/c (BB vs UTG, 40bb)

### BB first to act

- Average turn: BB has slightly **more equity (~52%) yet under-realizes,
  capturing 48.6%** of the pot; UTG (~48%) captures 51.4%.
- BB donks on turns where UTG **lacks dominant strong hands** and holds many
  weaker hands that would like to check back.

| Turn | BB donks (almost all 1/3 pot) |
|---|---|
| 8 | ~74% |
| 9 | ~66% |
| 5, 4, 2, 3, 6 | 41–47% |
| 7 | ~36% |
| T | ~24% (mostly 2/3) |
| J, Q, A | ~5% |
| K | ~1% |

**By suit:** clubs and spades ~37%, diamonds ~29%, hearts ~22% (half of it at
2/3).

- **Best donk cards:** board-pairing 9, 8, 4; straight-completing 7, 6, 5; low
  offsuit blanks.
- **Worst:** aces and other high cards, and **diamonds**, which hit UTG's
  backdoor diamond draws.
- **Hearts:** BB does well on them and holds *more* flushes than UTG, yet leads
  them less, because **UTG holds more of the nut flushes**. More flushes is not
  the same as the nut advantage.
- EV extremes for BB: worst = **offsuit kings (K♣/K♠)**; best = **offsuit 5s
  (5♣/5♠)**.
- On a flop this dynamic, both equity distributions swing violently by turn.
  BB bets aggressively on the turns that hand it a big range advantage; UTG
  plays passively on those.

### UTG when BB checks (x/b/c/x)

After two OOP checks UTG has a large **polarization advantage** and **splits
its range** as on the flop: it **bets most strong hands** and **checks back
most good, medium-strength hands** that don't want to bet and fold to a raise
and are happy to see a free river. Overall it bets about two-thirds of the time
(the summary chart shows ~64%, the text "over 65%"), mostly **2/3 pot**.

- **By hand class:** strong hands bet the most; **good hands check the most**
  (about two-thirds of the time); weak and trash hands sit in between.
- **Ace:** UTG's most frequent betting card (2/3 and 1/3).
- **King:** the card UTG overbets most.
- **9, 8, 4 (pairing cards):** bad cards for UTG, yet it still bets them often,
  **with 1/3 pot**. BB would have donked its strong hands on these cards, so its
  check is weak, and much of BB's range doesn't connect with the pairing card —
  a small bet takes plenty of folds.
- **Most other turns:** a more polarized betting range and bigger sizes (mainly
  2/3).
- **By suit:** hearts are bet least.
- **EV:** UTG does best on high cards, especially **offsuit aces and kings**.
  The **A♥ and K♥ are worse for UTG** than their offsuit versions because they
  **block many of UTG's flush combos**.

(The per-card and per-class charts average out to a lower overall bet
frequency, about 45%, than the summary chart; use them for which cards and
hands bet more or less, not for the overall rate.)

### BB facing the 2/3-pot second barrel (x/b/c/x/b)

- Both players have split their ranges several times. UTG checked back much of
  its medium strength, so its bet is **very polarized**; BB has already bet or
  raised many strong hands, so its range is weak against the barrel. BB **folds
  over 40%** on average.
- BB check-raises about **14%**, almost all **all-in**: at 40bb a smaller raise
  would commit too many chips anyway. The weaker check-raises are **semi-bluffs
  with enough equity to call the shove** once committed.
- Some strong hands are **slowplayed as calls**, so the check-call range stays
  protected even on brick runouts.
- **By turn:** BB defends most on low bricks (2, 3: ~36% folds), folds most on
  the **ace (~60%, calling only ~21%)** and the king (~47%); it check-raises
  most on T and J (~18%) and least on the 4 (~3%). Hearts are the only suit
  with a noticeable small raise.
- **Equity vs EV:** BB has **45% equity but captures only ~21%** of the pot;
  UTG has 55% with an **EqR of 144%**, capturing **~79%** (55 × 1.44 ≈ 79). BB's
  EqR is therefore about 21 ÷ 45 ≈ 47% (the book prints 77%, which doesn't
  reproduce its own 21%).

## Cheat sheet: turn cards on 9♥8♥4♦ (BB vs UTG)

| Node | Bettor's best turns | Bettor's worst turns | Size tendency | Why |
|---|---|---|---|---|
| x/x, BB first | Low cards: 5, 2, 3, 6, 7 | A (checks 92%), K, Q | 1/3 on straight cards; big on 8/9 pairs | BB's wide, uncapped range vs UTG's condensed check-back |
| x/b/c, BB donks | 8 and 9 pairs, 7-6-5, low blanks | A, K, Q, J; diamonds; hearts led less | 1/3 | Card polarizes BB and leaves UTG few dominant hands |
| x/b/c/x, UTG bets | A (most often), K (overbets) | 9, 8, 4 — but still bet often, small | 2/3 usually; 1/3 on pairing cards | BB's check on pairing cards has few strong hands |
| x/b/c/x/b, BB defends | Low bricks 2, 3 | A (folds ~60%), K | Check-raises are jams | BB is condensed and already stripped of strong hands |

## Takeaways for the table

1. Rebuild both ranges from the line, then ask who is polarized and who is
   condensed — that decides who bets, how often and how big.
2. After the raiser checks back, the caller holds the wide, uncapped range:
   probe often, especially on low and straight-completing cards. As the raiser,
   check back a range with some strong hands, or it becomes face up.
3. After x/b/c, check to the raiser by default; lead small on cards that pair
   the board or complete low straights, not on aces and high cards.
4. As the raiser after x/b/c/x, bet strong hands, check medium ones; size up
   (even overbet) on cards that favour you, and bet small on cards where the
   caller's check means it lacks strong hands.
5. Overcards, especially aces, favour the pre-flop raiser; low connecting cards
   favour the caller. Count who holds the *nut* flushes, not just the flushes.
6. Facing a turn donk with position and an uncapped range, rarely fold — raise
   a lot.
7. At around 40bb, turn check-raises are shoves; only raise hands that can
   happily call it off.
