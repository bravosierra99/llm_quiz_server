---
title: "Poker 14 — GTO River Strategies"
summary: "Modern Poker Theory ch. 14: why the river suits toy games, building a river abstract model, polar vs bluff-catcher variants (nut-heavy, air-heavy, traps), the minimum full-range bet, optimal size vs traps, linear thresholds, solver studies, blockers, practical river heuristics and the Final Word."
order: 114
audience: bravosierra99
---

# Poker 14 — GTO River Strategies

*Study guide to Chapter 14 (and the closing Final Word) of* Modern Poker Theory
*(Michael Acevedo). The book prints its equations and most tables as images; the
formulas here are reconstructed and checked against the book's worked numbers.
See the book for the solver tables in full.*

## Why the river is different

Pots are biggest on the river and bets are often all-in, so this is where the most
money changes hands and mistakes cost the most. Solving a given river is trivial
for a solver (a split second). The hard part is the **input**: every player starts
the hand with the same 169 hands, but by the river the ranges have been shaped by
suits, the runout and every earlier action, so they are the hardest of any street
to estimate. And because most hands end before showdown, players get the least
practice on the river.

What makes the river *tractable* is four properties that toy games capture well:

| Property | Consequence |
|---|---|
| No cards to come | Hand values are fixed; no draws. Each hand has 100% or 0% against any one opposing hand |
| Equity is a count | Hand-vs-range equity = share of villain's range you beat + half the share you tie (50% equity = ahead of half, behind half) |
| History-independent ranking | All possible river hands rank from best to worst the same way, however they got there |
| No future betting | A call, or an IP check heads-up, ends the hand and realizes equity |

## Setting up a river abstract model

1. List every river hand in both ranges from strongest to weakest, marking which player holds it.
2. Give each hand a **weight** (how often that player has it).
3. Record the **blocker relationships** — a matrix of which hands remove which (every hand blocks itself; e.g. holding hand 6 might remove hands 8 and 9).
4. Build the **game tree**: pot, stacks, permitted bet sizes.

That is everything a solver uses. **How the players got there is irrelevant**: two
spots with the same structure have the same GTO solution, whatever the actual cards
(the "nuts" may be a full house, a flush or a straight).

**Why it matters:** there are thousands of possible rivers, so you need to
**bucket** them into types you can recognise and already know the answer to. If
you identify "I'm polarized, he holds only bluff-catchers", the answer is known:
jam the nuts plus the right ratio of bluffs; he calls 1 − Alpha.

## Tools carried over from earlier chapters

> Alpha = b ÷ (b + p) — how often a zero-equity bluff must work; how much the defender may fold
>
> MDF = 1 − Alpha = p ÷ (b + p)
>
> Bluff combos = Alpha × value combos (pot bet → 1 bluff per 2 value hands, i.e. bluffs are ⅓ of the betting range; in general the bluff share of the bet is b ÷ (p + 2b))

Reconstructed EV of a polar bettor against pure bluff-catchers (bet S × pot, enough
air to bluff the right amount, checked air wins nothing):

> **P1 EV = value share × (1 + Alpha)** pots

Each value hand wins the pot plus a call worth S × MDF = Alpha; bluffs and give-ups
are worth 0. This reproduces every EV quoted in the chapter (below).

## The river [0-1] game

Board 2♠2♣2♥2♦3♣ (so a pocket pair's rank is its whole value), pot 100, stacks 500
by default (varied to study SPR), heads-up, both players may bet, x/r, call, jam
and fold. Hands run from AA (best) to 33; suits are arranged so there are no
blocker effects (blockers get their own section).

Two families of model:

- **Polarized** — ranges don't overlap; every hand is clearly nuts, air, bluff-catcher or trap.
- **Linear** — both players can hold hands of any strength.

## Polarized models

### Perfectly polarized vs bluff-catcher

P1 is half nuts (KK–QQ), half air (77–66); P2 holds only bluff-catchers (JJ–88).

- P1's EV rises with bet size → **jam all the nuts and bluff Alpha × value** with air, giving up the rest.
- P2 **never bets** and calls 1 − Alpha with his whole range.
- Stack depth doesn't change the structure and **position is irrelevant**.

| Jam size | Alpha | P1 EV (½ × (1 + Alpha)) |
|---|---|---|
| 1× pot | 50% | 75% of pot |
| 2× pot | 67% | 83% |
| 4× pot | 80% | 90% |
| 10× pot | 91% | ~95% |

The **floor is 50%** (P1 wins half the time just by checking) and the **ceiling is
the pot** — if any strategy won P1 more than the pot, P2 would simply fold
everything. Past about 4× the gains are marginal.

### All of P1's range beats P2's

P2 has 0% equity, so he never adds a chip: he can't bet (P1 never folds) and must
fold to every bet. P1 gains nothing by betting at equilibrium, since P2 always
folds. **Exploit:** real players may not realise they're drawing dead — bet any size
(even tiny) they might call. At equilibrium position is irrelevant; exploitatively
P1 bets when IP and, when OOP, picks bet or check by what will extract more.

### Polarized with more nuts than air

P1 is 90% nuts, 10% air. If P1 bets pot with everything, P2 needs 33% but has
only 10% equity, so he must fold: P1 wins the **whole pot**, denying P2's equity.
The goal is the **smallest** full-range bet that does this — maximum EV for minimum
risk if P2 slowplayed a monster or the read is wrong.

Set P2's calling EV to zero (pot = 1, EQ = P2's equity vs P1's whole range, B = bet):

> EQ(1 + B) − (1 − EQ)B = 0 → **B_min = EQ ÷ (1 − 2EQ)**
>
> 90/10 example: 0.1 ÷ 0.8 = **12.5% pot**

| P2's equity | Smallest full-range bet |
|---|---|
| 10% | 12.5% pot |
| 15% | 21.4% |
| 20% | 33.3% |
| 25% | 50% |
| 30% | 75% |
| 33.3% | 100% |
| 35% | 116.7% |
| 40% | 200% |
| 45% | 450% |
| 50%+ | impossible |

It's the bluff-share formula run backwards: P1 can bet everything when his air
fraction is no more than b ÷ (p + 2b) for that size.

When P1 has the chips for B_min:

- P1's bluffs earn the full pot just like his value; P2's EV is 0.
- P2's best response is to **fold every bluff-catcher to every size**. If P2 called some size, P1 could load it with surplus value hands, while always keeping the full pot with a big size — so any calling only costs P2.
- Position is irrelevant: P2 never bets, P1 bets 100%.

If the stack is shorter than B_min, P1 can't bet everything: he bets all value plus
Alpha × value in bluffs, gives up the remaining air, and P2 defends 1 − Alpha.
*Derived example:* 60% nuts / 40% air needs a 2× bet; with only a pot-sized jam
P1 bets 60% value + 30% air, gives up 10%, and wins 0.6 × 1.5 = **0.9 pot**.

### Polarized with more air than nuts

P1 is 10% nuts, 90% air. P2's equity is over 50%, so no bet folds everything.
P1 plays the standard polar strategy: bet **as large as possible** with all the
nuts plus Alpha × value in bluffs, give up the rest.

- P2 is ahead 90% of the time **but still only checks**: P1 is polarized, so he folds his air and calls only with the nuts. Betting gets called by better, never by worse.
- P2 calls 1 − Alpha; any less and P1 bluffs more.
- **Why bet big:** the bluffs are indifferent at any size, but a bigger size carries more bluffs, so the give-up branch happens less often.
- Pot-sized jam: bet 10% value + 5% air = **15%** of the time; P1's EV = 0.1 × 1.5 = **15% of the pot**; P2 wins the other 85% (mostly when P1 gives up).
- Lesson: being ahead most of the time against a polarized range doesn't let you bet — you're forced to play passively.

### Polar vs bluff-catcher **with traps**

Holding only bluff-catchers leaves you at the mercy of the polar player, so P2's antidote is to slowplay
some nutted hands — **traps** — inside his checking range. Model: P1 50% nuts / 50%
air; P2 90% bluff-catchers + 10% traps that beat P1's value.

- Without traps, bigger is always better for P1. With traps, **the jam has a sweet spot**: with 10% traps P1's jam EV peaks near **SPR 1.25 (≈60% of the pot)**, then falls; from about SPR 4 a jam is no better than checking, and P1 checks everything for **45%** (his nuts win 90% of the time: 0.5 × 0.9).
- **A massive overbet into a range that can hold traps is a big EV mistake.** At low SPR the occasional trap costs little; at high SPR it's expensive.
- But betting less than all-in lets P2 **x/r**, turning his bluff-catchers into bluffs and P1's value hands into bluff-catchers. In that branch P2 is the polarized player, and the deeper the stacks the bigger he can raise and the more EV he takes.

*Derived check (reproduces the book's curve):* jam EV = ½(1 − T) + ½·S·(MDF − 2T),
T = trap share. A jam beats checking only while **MDF > 2T** — with 10% traps,
MDF > 20%, i.e. SPR < 4.

The best size trades these off. The book borrows Will Tipton's formula (*Expert
Heads-Up No-Limit Hold'em*; derived with calculus, not shown):

> B = [1 + S − T − 4S(1 + S)T + √((S + 2S²)² T)] ÷ [(1 + 2S)² T − 1]
>
> S = stack, B = bet (both in pots), T = trap share. If B ≥ S (or the denominator is negative) → jam; if B ≤ 0 → check.

Optimal bet by SPR and trap share (selected rows of the book's table):

| SPR | 1% traps | 10% | 20% | 30% | 40% |
|---|---|---|---|---|---|
| 0.5 | All-in | All-in | All-in | All-in | All-in |
| 1 | All-in | All-in | All-in | 55% | 11% |
| 1.5 | All-in | All-in | 90% | 26% | Check |
| 2 | All-in | All-in | 62% | 15% | Check |
| 3 | All-in | 147% | 41% | 6% | Check |
| 5 | All-in | 102% | 28% | Check | Check |
| 10 | 809% | 77% | 19% | Check | Check |

**Pattern: more traps or deeper stacks → smaller bet**, until the size approaches
zero and P1 checks his whole range.

With a few traps, P2 never leads and position doesn't matter. With **too many**
traps the game changes: P1 checks back 100%, P2's traps never get paid, so P2 starts
**leading some traps**. Equilibrium: lead some, slowplay just enough to protect the
checks — and now position matters.

**What x/r is really for.** It is a poor way to deny equity and a poor way to get
value. Its job is to **stop IP from value-betting thin and from bluffing a lot**
when you check. Just **10–20% traps** achieves both at most stack depths.

P2 still defends at MDF overall, so the bluff-catchers make up the difference:

> **P2 call % = MDF − % traps** (shares of P2's whole range)
>
> Pot-sized jam, 10% traps: 50% − 10% = 40% of the range calls with bluff-catchers (≈44% of the bluff-catchers)

## Linear distributions

Real ranges mix nuts, bluff-catchers and air. Rank every hand by equity from 1
(best) to 0 (worst). The bettor splits his range into three bands — **value on top,
checks in the middle, bluffs at the bottom** — so the *betting* range is polarized
even though the whole range is linear.

| Band | IP bettor | OOP, first to act |
|---|---|---|
| Top | Bet for value | Bet for value, check some as **traps** |
| Threshold | Weakest value bet: indifferent bet/check | — |
| Middle | Check back (checking EV > betting EV) | Bluff-catchers |
| Threshold | Strongest bluff: indifferent bet/check | — |
| Bottom | Bluff | Bluff (mixed) |

So an OOP checking range is never 100% bluff-catchers. Facing a bet:

- **All-in:** find the hand indifferent between calling and folding; call above it, fold below.
- **Not all-in:** **raise traps** (the top) plus a matching share of bluffs (the bottom), call the middle, fold the rest.

**Linear river play comes down to identifying the threshold hands.**

### The simple threshold formulas

Model: symmetric ranges spread evenly from 0 to 1; OOP can only bet or check;
checking hands have zero equity; IP calls or folds; no raises.

> **hc = b ÷ (b + p)** — the defender calls every hand better than hc
>
> **hb = [EQ_hc × (p + 2b) − b] ÷ (b + p)** — the bettor bets every hand better than hb, gives up the rest
>
> b = bet, p = pot, EQ_hc = equity of the threshold calling hand (= hc when ranges are symmetric and uniform)

- hc equals Alpha, so the defender continues with exactly **MDF** — that's what makes bluffs break even.
- hb is set so the threshold caller is indifferent: hands between hb and hc lose to every call (they are the bluffs), and they form exactly the b ÷ (p + 2b) bluff share.

| Bet | hc | Defender calls | hb | Bettor bets | Bluff share of bets |
|---|---|---|---|---|---|
| ½ pot | 1/3 | top 2/3 | 1/9 | 8/9 | 25% |
| Pot (book example, b = p = s) | 1/2 | top 1/2 | 1/4 | 3/4 | 33% |
| 2× pot | 2/3 | top 1/3 | 4/9 | 5/9 | 40% |

Pot example: hb = (½ × 3 − 1) ÷ 2 = ¼, so the bettor bets the top ¾; ⅔ of those
bets beat the threshold caller and ⅓ are pure bluffs — the 2-to-1 ratio that a
pot-sized bet requires. Once checks have equity and raises are allowed, the algebra
becomes impractical; study those spots in a solver.

## Solver studies of linear ranges

### Symmetric ranges (both players hold AA–55 once each)

Unlike the earlier [0-1] toy game, OOP may now bet.

**OOP first to act:**

| SPR | OOP plan |
|---|---|
| 1 and above | Bet **⅓ pot** (~31–37% of the time) with QQ–JJ, part of AA–KK and 55 as a bluff; check TT–66 plus most AA–KK to protect the checks |
| Below 1 | **Jam** (31% at SPR 0.75 → 62% at 0.25) with most of JJ+ and 55; still check 10–20% of the strong hands; the value range widens from JJ+ to 99+ as SPR falls to 0.25 |

**IP after OOP checks:**

| SPR | IP plan |
|---|---|
| 5+ | Never jam. Pot with most AA–KK (some AA–KK in the small size to guard against x/r), half pot with QQ–JJ; bluff 55 and some 66 in both sizes; check back TT–77 (checks ≈52% overall) |
| 2 | Jam most AA–KK, a smaller (75%) size with QQ and some JJ, bluff 66–55, check TT–77 |
| 1 and below | Jam a polar JJ+ / 66–55, check TT–77; value widens to 88+ by SPR 0.25 |

### Ranges overlap in the middle

P1 holds AA–55, P2 holds QQ–33. P1 has hands P2 can't have (AA–KK); P2 has hands
that lose to all of P1's (44–33).

**P1 IP, P2 OOP.** P2 never bets unless SPR is very small. P1 after a check:

- SPR 2+: **two sizes** — **jam AA–KK** (P2 can't have them, so there are no traps and the biggest size is right even at SPR 10) and **125% pot** with QQ (value that P2 can also hold). Bluff 55–66 and some 77; check back JJ–77. (≈33–38% jam, 16% at 125%.)
- SPR 1 and below: jam AA–JJ plus 55–66 (≈53–60%), check back TT–77.

**P1 OOP, P2 IP.**

- SPR 2+: jam AA–KK; bet **25% pot** with the overlapping top (QQ–TT — though most QQ is checked); bluff 66–55; check 99–77 plus a little AA–KK and most QQ for protection.
- SPR 1 and below: jam JJ+ and 66–55; bet **10% pot** with TT–99, a sliver of AA–JJ and some 66; check 88–77 plus some TT+. Shallower stacks move TT–99 into the jam.
- P2 (IP) after P1 checks: checks back 99–66, bets QQ–TT for value and bluffs some 55–33. Deep (SPR 10) he bets only half pot because a big bet risks a x/r; 75% at SPR 5–2; jams at SPR 1 and below.

**Pattern:** jam the value villain can't have or beat; use a smaller size with value
that overlaps his range; keep some strong hands in your checks.

## Blocker effects

Board 8♥3♥3♣2♥2♦, pot 100, stacks 500 (SPR 5). Villain always checks; Hero may bet
25, 50, 100 or all-in; Villain may x/r all-in against a non-all-in bet. Villain holds
45 unblocked flushes: 9 A♥-high (nut), 8 K-high, 7 Q-high, 6 J-high, 5 T-high,
4 9-high, 3 7-high, 2 6-high, 1 5-high.

**Example 1 — Hero has nut blockers.** Hero (IP): 9 nut flushes, 12 A♥ hands without
a flush (nut blocker), 24 lower-heart blockers, 6 low-spade hands that block nothing.
Villain never bets into Hero's polarized range, and Hero has far more bluffs than value.

- Whenever Hero holds the A♥, Villain **has no nut flush — zero traps**. Betting only the nut flushes plus A♥ bluffs turns the spot into pure polar vs bluff-catcher → **jam** with all value and Alpha × value bluffs. Bluffing with other blockers loses EV.
- Numbers: jam 500 into 100 → Alpha = 5/6, so 9 value combos take **7.5** A♥ bluffs (12 available). Villain's real range is 36 combos and must call 1/6 of it — 6 combos.
- A solver may display a higher calling frequency than 1 − Alpha because it counts **"ghost" nut flushes** Villain can't hold when Hero has the A♥. Strip them out and the real call rate is exactly 1 − Alpha.

**Example 2 — no nut blockers.** Hero can't remove the traps, so a big overbet loses
a lot; Hero **bets pot** instead.

- Best bluffs: the **low spades, not the K♥ blockers**. A non-nut blocker is worse than no blocker: if Hero bluffs with K♥ hands, Villain overfolds his K-high flushes and calls with more of his lower flushes.
- Pot bet → 4.5 bluffs per 9 value combos (6 low-spade combos available).
- A few nut blockers, not enough for all the value: **split** — jam as many nut flushes as the A♥ bluffs can support, pot-bet the rest of the value with low-spade bluffs.
- SPR 1 or less: always jam if there are enough nut blockers, give up the rest; top up with low spades if not.
- If Hero's value also includes non-nut flushes, flush blockers become better bluffs than non-blockers.

## Practical applications

### OOP river betting

**Range features that favour a high x/r frequency against IP's bet:**

- OOP has many hands that want to realize equity — traps cut IP's betting frequency, so those hands reach showdown.
- OOP's strong hands are few but nutted.
- IP's range wants to bet a lot when checked to.
- x/r protects OOP from IP's thin value bets.
- On dry boards after x/c, x/c, OOP has little pure air, so hands normally x/f (e.g. bottom pair) become x/r bluffs.

**Why bet OOP at all:** IP's checks realize his equity for free; betting denies that.
Bet when IP's range would check back a lot.

**After IP checks back the turn:** IP's range is condensed, OOP's more polarized →
OOP should bet the river about **20–30%** of the time. If IP checked back a turn on
which he'd usually bet a lot, his range is weak; if he checked back a turn that was
bad for him, the check-back range is stronger.

**Leading after x/c, x/c:** IP has double-barrelled, so he's polarized and OOP is
condensed — mostly hands that want a cheap showdown. Leads are rare, and happen
when the river (often turn and river together) flips the polarization: OOP suddenly
has many strong hands and IP wants to check back. Then OOP can lead **75%+**.
Examples: a four-flush or four-straight board, the river pairing the
second-highest board card, a runner-runner pair. Rare, but big enough EV to study.

### IP river betting

Simpler — OOP's checking range is mostly bluff-catchers.

- **Polarized range** → bet as big as possible with enough bluffs to make OOP indifferent.
- **Condensed range** → check back the middle, bet the top, bluff with the weakest.
- **Not very nutted** → still value-bet, but small, especially if OOP can trap. Too weak, or OOP has too many traps → check back and take the free showdown.
- When betting small, include a little of your nutted hands to protect against x/r (unneeded if OOP has no traps).

### IP vs river bets — exploits

| Villain tendency | Exploit |
|---|---|
| Rarely bets the river | Value-bet less thinly and fold more to his river bets. You can also c-bet the flop more: your lines that check later get many free showdowns, so marginal hands realize their equity |
| Often bets the river after IP checks the turn | C-bet the flop less, so you don't arrive with lots of air that checks the turn and folds to a lead; check back the turn with some hands able to raise a river bet |

### River calling

All bluff-catchers are equal on the river **except in what they block**.

| Your hand blocks | Adjust |
|---|---|
| His value range | Call more |
| His bluffs | Fold more |
| Both | Decide on other factors |
| Neither | Irrelevant, or slightly negative |

Decision points:

- Start from his value range: always call hands that beat it, even against very tight players.
- If his range lacks enough bluffs, don't call with bluff-catchers.
- Lots of air in his range → he's more likely to be bluffing.
- Image matters: seen as a calling station → expect a wider value range; seen as weak → a narrower value range and more bluffs.
- **Defending near 1 − Alpha** is a good approximation in most river spots.

## The river drives every earlier street

Work out which river situations suit you, then play earlier streets to arrive there
more often with the right range composition — your opponents are doing the same.
Solvers do exactly this, backwards: optimal river play → turn strategies that lead
to good rivers → flop → pre-flop, until both players are at equilibrium. An
imbalance on any street produces bad later spots, and spotting those is what
exploitative play is about.

## Final word

The book's aim was to give you the tools to find answers yourself, not every
answer. Software will keep changing, and it is useless without the fundamentals —
**solver output is not an oracle** to be followed blindly.

## Takeaways for the table

1. Classify the river first: polar vs bluff-catcher, nut-heavy, air-heavy, trapped or linear. Each type has a known solution.
2. Polarized with no traps behind → bet as big as you can, bluffs = Alpha × value. If villain can trap, shrink the size; with many traps, check.
3. Nut-heavy range → find the smallest bet that folds everything: EQ ÷ (1 − 2EQ).
4. Being ahead most of the time against a polarized range is not a reason to bet — check and defend near 1 − Alpha.
5. Keep 10–20% traps in your checking ranges to stop thin value bets and heavy bluffing.
6. Bluff with the nut blocker; without it, bluff with hands that block nothing rather than a lesser blocker.
7. When calling: blocking value → call more; blocking bluffs → fold more; no bluffs in his range → fold.
