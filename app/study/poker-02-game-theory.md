---
title: "Poker 02 — The Elements of Game Theory"
summary: "Modern Poker Theory ch. 2: game-theory vocabulary, MES and counter-exploitation, Nash equilibrium, indifference, the AA/QQ vs KK toy game, alpha and MDF (incl. multiway), passive/active exploitation, MES vs MinES, GTO in multiway pots, bet-size math."
order: 102
audience: bravosierra99
---

# Poker 02 — The Elements of Game Theory

*Study guide to Chapter 2 of* Modern Poker Theory *(Michael Acevedo). The
chapter's range charts are worth a look in the book; everything else — the
definitions, the toy game, and the bet-size arithmetic — should be rebuildable
from this page.*

## Core vocabulary

| Term | Meaning |
|---|---|
| **Game** | Any interaction where each player's payoff depends on the others' decisions |
| **Utility** | How much a player values an outcome; higher = preferred. A perfect player's utility is simply EV — real players' utility is bent by fear, ego and embarrassment |
| **Zero-sum game** | One player's gain is exactly the others' loss. Poker is zero-sum **if you ignore rake and ICM** |
| **Strategy** | A complete plan: what you do at *every* possible decision point |
| **Pure strategy** | Always the same action at a given decision point |
| **Mixed strategy** | Two or more actions at the same decision point, each at some frequency |
| **Dominated strategy** | One that does worse than some alternative no matter what opponents do |

Dominance, for two strategies A and B:

| Relationship | Meaning |
|---|---|
| B **strictly dominates** A | B is better than A against *every* opponent action |
| B **weakly dominates** A | B is better against at least one opponent action and equal against all the rest |
| A and B **intransitive** | Neither dominates: which is better depends on what the opponent does |

Strictly dominated plays are never rational, so the first step in solving any
spot is to delete them.

## Maximally exploitative strategy (MES)

The **MES** is the most profitable response to an opponent's **fixed** strategy.
You need to know their *entire* strategy to compute it.

- It is found **hand by hand**: play each of the 1,326 combos the most
  profitable way; the value of the game is the sum of those per-hand EVs.
- **No loss leaders.** Nothing is ever played less profitably "for balance" or
  to "protect the range". A hand is +EV or it isn't.
- A hand can only be **mixed** if the actions have **identical EV**.

**Worked example — HU push/fold, 10bb (100 chips, blinds 5/10).** BN shoves
100% of hands. BB must call 90 to win a final pot of 200:

> required equity = 90 ÷ 200 = 45%

BB's MES is to call every hand with ≥45% equity vs a random hand — **66.2%** of
hands — and fold the rest. BB then captures 13.77 of the 15 chips in the middle
(~92%); the any-two-cards shover keeps 1.22 (~8%).

## Counter-exploitation and the road to equilibrium

An MES assumes the opponent stands still. An opponent who adapts will compute
*their* MES against *your* MES, and so on:

| Iteration | BN shoves | BB calls | BN EV | BB EV |
|---|---|---|---|---|
| 1 – BN shoves everything, BB plays MES | 100% | 66.2% | 1.22 | 13.77 |
| 2 – BN re-adjusts to that calling range | 46.6% | 66.2% | 6.25 | 8.48 |
| 3 – BB re-adjusts | 46.6% | 30.3% | 4.23 | 10.75 |
| **Nash equilibrium** | **58.3%** | **37.4%** | **4.55** | **10.45** |

(EVs in chips out of the 15-chip pot.) Repeat long enough and the strategies
stop moving: neither player can improve. If the strategies just flip back and
forth without settling, move only a **small step** toward the best response each
iteration instead of jumping all the way — this is in essence how solvers
converge.

The lesson in the table: BB's exploit earned 13.77 **only while the read was
right**. One adjustment by BN and the same calling range earns 8.48 — *less* than
the 10.45 that the equilibrium calling range guarantees against anything.

## Nash equilibrium (= "GTO")

A set of strategies where:

1. every player knows everyone else's exact strategy (clairvoyance),
2. all players are maximally exploiting each other at once,
3. **nobody can gain by changing strategy unilaterally**.

Because an equilibrium strategy *is* an MES (against an unexploitable opponent),
it inherits the MES properties:

- every hand is played as profitably as possible — **GTO never sacrifices EV for balance**;
- strictly dominated plays never appear;
- a hand is mixed only when its options have equal EV.

**Why GTO is worth having**

| Property | Consequence |
|---|---|
| **Guaranteed minimum EV** | It assumes the opponent knows your strategy and responds perfectly, so heads-up nobody can gain an edge on you: you break even or profit |
| **No levelling wars** | It doesn't depend on reads, so you never have to out-guess anyone |
| **Passive profit** | Against anything other than a perfect counter, your EV is *above* equilibrium, and rises as the opponent gets worse |
| **The cost** | It earns less than a strategy tailored to a specific opponent's mistakes |

Hence the working model for strong players: a sound GTO baseline against tough
or unknown opponents, plus exploitative adjustments as reads firm up.

## The indifference principle

If a hand is mixed at equilibrium, **every action it takes with non-zero
frequency has the same EV** — the player is indifferent. And the reason they are
indifferent is that **the opponent is playing in exactly the way that makes them
so**. Indifference in your hand tells you something about your opponent's
strategy.

This is what "balance" really means. In the 10bb game:

- BN shoves 58.3%. Why not more? BB calls just often enough that the **worst
  hand in the shoving range (43s) breaks even**. If 43s made money, BN would add
  more hands; if it lost money, BN would drop it and a new hand would be the
  bottom. So 43s is mixed (~74% shove, 26% fold). Shove it more and BB can call
  wider and make it −EV.
- BB calls 37.4%. The bottom of the calling range (**Q6s**) breaks even and is
  mixed (~39% call). Call it more and BN tightens up, making it −EV.

**The bottom of every range is a break-even hand, pinned there by the
opponent's frequencies.**

## The clairvoyance toy game

River, pot **$100**, stacks **$100**, board 3♠3♥3♣2♦2♠.
**P1** (OOP) holds A♠A♥ or Q♣Q♦, half each — a perfectly **polarized** range of
nuts and air. **P2** (IP) holds K♣K♦ — a pure **bluff catcher**. Each player has
50% equity. Both know each other's strategy.

### Step 1 — delete dominated plays

| Dominated play | Why |
|---|---|
| P1 folding AA | It always wins |
| P1 calling a bet with QQ | It can never win; calling just loses the bet |
| P2 betting KK | AA never folds and QQ never calls — a bet only loses more to AA |
| P1 checking AA | P2 never bets, so a check wins nothing extra |

What's left: P1 always bets AA; the only questions are P1's size, how often QQ
bluffs, and how often KK calls. (Take the size as all-in for now.)

### Step 2 — pure strategies fail

- **QQ always bluffs** → betting range is half bluffs; P2 always calls and
  makes $50, double the $25 he gets at equilibrium.
- **QQ never bluffs** → P2 always folds; AA wins only the pot, QQ loses at
  showdown; P2 again makes $50.

So P1 must mix, and the right mix makes KK **indifferent** between call and fold.

### Step 3 — P1's bluffing frequency

Calling EV for P2 with win-rate W: W(b + p) − (1 − W)b. Set to 0 (the EV of folding):

> W = b ÷ (2b + p) — exactly P2's **pot odds**

On the river the bluff catcher wins exactly as often as the bettor is bluffing,
so: **the share of bluffs in a polarized river betting range equals the pot odds
you offer.** Pot-size bet → 100/300 = 1/3 bluffs, 2/3 value.

> bluff-to-value ratio = b ÷ (b + p)

Pot-size bet → 1 bluff per 2 value combos. P1 has AA half the time and bets it
always, so QQ bets **50%** of the time. P1 bets 75% overall and checks 25%.

### Step 4 — P2's calling frequency

P2 must make QQ indifferent between bluffing (EV = (1 − c)p − cb) and checking
(EV = 0):

> **MDF** (minimum defense frequency) = c = p ÷ (b + p)
>
> **Alpha** = fold frequency = b ÷ (b + p) = 1 − MDF

Pot-size bet → KK calls 50%, folds 50%. **Alpha is how often a zero-equity bluff
must work to break even**; MDF is how much the defender must continue to stop
bluffs being automatically profitable. Note alpha has the same formula as the
bluff-to-value ratio.

P2 is indifferent with KK, yet still **must** call at the right frequency: never
calling lets P1 bluff every QQ; always calling lets P1 stop bluffing altogether.

### Solution

| | Strategy | EV |
|---|---|---|
| **P1** | AA: bet $100 always. QQ: bet 50%, check 50% | **$75** (AA $150, QQ $0) |
| **P2** | vs check: check back. vs bet: call 50%, fold 50% | **$25** |

P2's whole $25 comes from the one branch where QQ gives up (25% of the time ×
$100). Calling and folding against the bet are both worth $0.

**Equity is not EV.** Both players have 50% equity; the polarized player takes
75% of the pot. Being polar against a bluff catcher is worth real money.

### Two more results

- **Position is irrelevant in a pure nuts/air vs bluff-catcher spot.** With P2
  OOP he checks 100% (betting KK is still dominated) and P1 plays the same
  strategy.
- **The perfectly polar player's best size is all-in.** A bigger bet permits
  more bluffs, so the QQ-gives-up branch — P2's only income — shrinks.

| Bet (into $100) | P1 EV | QQ bluff freq | P1 bets overall |
|---|---|---|---|
| $25 | $60 | 20% | 60% |
| $50 | ~$66.7 | 33% | 66.7% |
| $100 | $75 | 50% | 75% |
| $200 | ~$83 | 67% | ~83% |
| $300 | $87.5 | 75% | 87.5% |
| $1,000 | ~$95 | 91% | ~95% |

> P1 EV = p − ½ · p · p ÷ (b + p). With an infinite bet P1 takes the whole pot.

(This is the theoretical root of overbetting: the more polar your range and the
more capped/condensed theirs, the bigger you want to bet.)

## Alpha and MDF in practice

> Alpha = bet ÷ (bet + pot) &nbsp;&nbsp;&nbsp; MDF = 1 − Alpha = pot ÷ (bet + pot)

("bet" = the amount you are *risking*.)

**Example — stealing with 72o.** Live MTT, 9-handed with a 12.5% ante, folded to
Hero in the SB, pot 2.625bb. BB (20bb) is tight and defends only ~50.8%, i.e.
folds 49.2%. Hero raises to 2.5bb, risking 2bb more:

> Alpha = 2 ÷ (2 + 2.625) ≈ 43%

BB folds more than 43%, so the raise prints **even assuming Hero loses every
time he is called**: 0.4917 × 2.625 − 0.5083 × 2 ≈ +0.274bb = **+27.4bb/100**.
Against this BB, any two cards are a profitable steal. (The worst-case
assumption is useful: if it's profitable with zero equity, it's profitable.)

From BB's side, MDF = 1 − 0.43 = **57%** — but the solver's actual defence here
is **82.1%**. **MDF is a floor against zero-equity bluffs, not the GTO defending
frequency**: real raising hands have equity, and the BB is getting a good price
closing the action.

### Multiway alpha

With several players left to act, the bet must get through **all** of them:

> fold each opponent needs = (Alpha)^(1/n) — the n-th root, n = opponents left
>
> individual MDF = 1 − n-th root of Alpha
>
> combined fold frequency = product of the individual fold frequencies

**Example — BN open, 6-max cash, no ante.** Pot 1.5bb, raise to 2.5bb:
Alpha = 2.5 ÷ 4 = **62.5%**. Each blind must fold √0.625 ≈ **79%** for any two
cards to profit, so each must defend at least **21%**.

**HUD check:** BB folds to steals 69%, SB 87%. Both look high, but
0.69 × 0.87 = **60%** < 62.5% — **not** an automatic profit with a zero-equity
hand. Multiply the fold stats; don't eyeball them.

The same formula works for any number of opponents and post-flop (e.g. multiway
c-bets), as long as the bluff is assumed to have no equity.

## Exploitation: passive and active

| Type | What you do | Risk |
|---|---|---|
| **Passive** | Just play equilibrium. Heads-up, any deviation by the opponent can't raise their EV and may lower it — the loss is yours. The weak player self-exploits | None |
| **Active – maximal (MES)** | Deviate to the single most profitable counter to their strategy | Largest gain, largest exposure |
| **Active – minimal (MinES)** | Small deviation that accounts for their leak *and* for their best counter-adjustment | Small gain, essentially unexploitable |

"Exploitative player" in normal usage means a maximally exploitative one.

### How much does MES add, and what does it risk?

HU push/fold, 15bb, Hero in the SB. GTO: shove 45.7%; BB's GTO call is 28.5%.
EVs in bb/100:

| Villain calls | MES shove % | GTO gains | MES gains | MES edge over GTO | Loss if villain is really GTO | Loss if counter-exploited |
|---|---|---|---|---|---|---|
| 28.5% (GTO) | 45.7% | 0 | 0 | 0 | 0 | 0 |
| 31.4% (10% loose) | 37.6% | 0.5 | 1 | 0.5 | −0.5 | −1.8 |
| 35.6% (25% loose) | 35.1% | 2 | 4 | 2 | −1 | −3.2 |
| 57% (100% loose) | 37.9% | 21.1 | 27.4 | 6.3 | −1.3 | −2.5 |
| 25.7% (10% tight) | 55.4% | 0.1 | 0.5 | 0.4 | −0.6 | −1.7 |
| 21.4% (25% tight) | 80.1% | 1 | 5.6 | 4.6 | −6.6 | −22.1 |
| 14.3% (50% tight) | 100% | 4.8 | 29.4 | 24.6 | −16.9 | −62.4 |
| **Average** | | | | **+6.4** | **−4.5** | **−15.6** |

Reading it:

- **GTO already collects most of the money from the worst players** — 21.1 of
  the 27.4 available against the calling station.
- **Against callers the exploit is "tighten up"** and the adjustment is small
  and cheap to be wrong about.
- **Against nits the exploit is "shove far wider"** — big gain, but the downside
  is 2–3× the upside and a jump from ~46% to 100% shoves is easy to spot.
- On average MES risks about 15.6 to gain 6.4.
- Two separate dangers: the opponent **adapts**, or your **read was wrong** — in
  which case *you* are the one who deviated to a worse strategy. Maximal
  exploitation needs high confidence.

### Minimally exploitative strategy (MinES)

Back to the toy game, but P2 calls **55%** instead of 50%.

| Hero's strategy | QQ bluffs | AA EV | QQ EV | Hero EV |
|---|---|---|---|---|
| GTO | 50% | $155 | −$5 | **$75.00** |
| MinES | 45% | $155 | −$4.50 | **$75.25** |
| MES | 0% | $155 | $0 | **$77.50** |

GTO gains *nothing* here: AA earns $5 more (0.55 × 200 + 0.45 × 100 = 155) but
the bluffs lose exactly as much (each bluff: 0.45 × 100 − 0.55 × 100 = −$10,
made half the time). Passive exploitation only pays when the opponent's mistake
is a pure loss, not a shift between two options you've made equal.

MES (never bluff) gains $2.50/hand — but Hero now bets 50% of rivers instead of
75% and shows AA every time. If Villain responds by **always folding**, Hero
makes $50: a loss of $25/hand versus GTO, **10× what the exploit was earning**.
So the exploit must run 10 hands for every hand it gets countered just to break
even. Countered 2 hands in 10: 8 × 2.5 − 2 × 25 = −$30. Countered only the last
5 of 50: 45 × 2.5 − 5 × 25 = −$12.50.

**MinES builds the leak into the game.** Model Villain as feeling an extra cost
**X** whenever he folds to a bluff (ego, fear of being bluffed). Indifference
with X:

> Villain's call frequency = (p + X) ÷ (p + X + b) = 0.55 → X ≈ $22.2
>
> Hero's QQ betting frequency q: q(p + b) − b = −X·q → q = 100 ÷ 222.2 ≈ 45%

Bluffing 45% instead of 50% earns only +$0.25/hand ($25 per 100 hands), but
Villain **cannot counter it** except by fixing the leak itself.

Practical features of MinES:

- Computed in a solver by **node-locking**: fix the assumed leak, let Villain
  play optimally everywhere else, re-solve. You need only the *leak*, not
  Villain's whole strategy (which MES requires).
- The solution already accounts for Villain's best counter-adjustments.
- Adjustments are small, so they're hard to notice and can run for a long time.
- If Villain returns to equilibrium, so must you.

| Sub-type | When you adjust | Example vs someone who over-folds to flop c-bets |
|---|---|---|
| **Reactive** | After the leak has shown up in the hand | C-bet the normal range; on turn and river, account for his now-stronger continuing range |
| **Proactive** | Before the mistake, anticipating it | C-bet more often |

Use both: c-bet more, then on later streets remember **your** range is wider
than normal and **his** is tighter than normal.

## GTO in multiway pots

Heads-up, equilibrium play **cannot lose**. That guarantee also covers any hand
**from the moment only two players remain** — e.g. CO opens, BN 3-bets, blinds
fold; UTG opens and it folds to the BB; HJ opens, BN calls, SB 3-bets, HJ folds.

With three or more players live there is **no such guarantee**. One player's
mistake is not shared out evenly; who collects depends on position and stacks,
and a player can lose EV **while playing their equilibrium strategy**.

**Example — 3-max, 12bb each.** BN's equilibrium shove is 32.1%; a fish shoves
only 16%. EVs in bb/100:

| | BN | SB (Hero) | BB |
|---|---|---|---|
| All play Nash | +22 | −16.7 | −5.4 |
| BN is the fish, blinds play Nash | +19.8 | −21.2 | +1.5 |
| BN is the fish, blinds play MES | +16.6 | −19.9 | +3.3 |

The fish loses EV — and so does Hero in the SB: −4.5bb/100 by sticking to GTO,
still −3.2bb/100 after adjusting. The BB scoops all the gain. (Over many hands
Hero sits in the BB as often as the SB, so he still profits from the fish
overall.)

Conclusion: multiway, GTO is a **near-unexploitable starting point**, not a
final answer. And everywhere, GTO is a tool that supplements thinking about the
actual opponents — it doesn't replace it.

## Poker math everyone should know

Normalise the pot to 1 and express the bet **b** as a fraction of it.

> pot odds (equity the caller needs) = b ÷ (2b + 1)
>
> Alpha (how often a bluff must work) = b ÷ (b + 1)
>
> MDF = 1 − Alpha = 1 ÷ (b + 1)
>
> polarized river betting range: bluffs = b ÷ (2b + 1), value = the rest

| Bet (× pot) | Pot odds / bluff share | Odds laid | Alpha | MDF |
|---|---|---|---|---|
| 0.10 | 8% | 11 : 1 | 9% | 91% |
| 0.25 | 17% | 5 : 1 | 20% | 80% |
| 0.33 | 20% | 4 : 1 | 25% | 75% |
| 0.40 | 22% | 3.5 : 1 | 29% | 71% |
| 0.50 | 25% | 3 : 1 | 33% | 67% |
| 0.60 | 27% | 2.7 : 1 | 38% | 63% |
| 0.67 | 29% | 2.5 : 1 | 40% | 60% |
| 0.75 | 30% | 2.3 : 1 | 43% | 57% |
| 1.00 | 33% | 2 : 1 | 50% | 50% |
| 1.25 | 36% | 1.8 : 1 | 56% | 44% |
| 1.50 | 38% | 1.7 : 1 | 60% | 40% |
| 2.00 | 40% | 1.5 : 1 | 67% | 33% |
| 3.00 | 43% | 1.3 : 1 | 75% | 25% |
| 5.00 | 45% | 1.2 : 1 | 83% | 17% |

Reading one row — **half pot**: the caller needs 25% (3-to-1); your polarized
range should be 75% value, 25% bluffs; a zero-equity bluff must work 33% of the
time; the defender must continue with 67%.

Patterns to notice: the bluff share can never reach 50%, however big the bet;
bigger bets *allow more bluffs* and *force fewer calls*; small bets must be
defended very widely.

## Takeaways for the table

1. Memorise the five workhorse sizes: ⅓ pot → 25% alpha / 75% MDF / 20% bluffs; ½ → 33 / 67 / 25; ⅔ → 40 / 60 / 29; ¾ → 43 / 57 / 30; pot → 50 / 50 / 33.
2. Before bluffing, compute alpha and ask whether they really fold that often. Multiway, **multiply** the fold frequencies — two players who each fold 75% only fold 56% together.
3. MDF is a floor for bluff catchers against a polar range, not a target: it ignores the equity of the bettor's bluffs and of your own hand.
4. Polar range vs capped range → bet big. Your bluffing frequency rises with your bet size.
5. Never play a hand badly "for balance". GTO plays every hand at maximum EV; mixing happens only when options are equal.
6. Default to GTO against unknowns and good players; it already wins from bad ones. Exploit in small steps unless the read is solid — being countered or being wrong costs more than the exploit earns, especially when the adjustment is "bluff/shove much more".
7. Multiway, GTO promises nothing. Watch who is in the pot and who benefits from the fish's mistake.
