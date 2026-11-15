---
title: "Poker 10 — The Theory of Post-flop Play"
summary: "Modern Poker Theory ch. 10: why we bet (information and equity), folding/checking/calling/raising, equity buckets, pot-size raise maths, alpha/MDF on the flop, splitting ranges across bet sizes, SPR and polarization effects, geometric sizing, range merging, flop-specific sizing and using solvers."
order: 110
audience: bravosierra99
---

# Poker 10 — The Theory of Post-flop Play

*Study guide to Chapter 10 of* Modern Poker Theory *(Michael Acevedo). Read the
chapter for the pie charts, hand-range grids and toy-game tables; this guide
is the skeleton you should be able to rebuild from memory.*

The chapter's numbers come from aggregated GTO solutions of MTT-style spots
(antes, no rake, 20–40bb stacks), but the heuristics are meant to carry over to
most NLH post-flop play. Treat them as good approximations, not final answers.

## Why we bet

**"Value" and "bluff" are outcomes, not reasons.** Whether a bet turned out to
be a value bet (called by worse) or a bluff (folded out better) depends on the
exact hand villain held, which you don't know and don't control. The clean
value/bluff split only really describes a river where a perfectly polarized
range bets into bluff catchers. Everywhere else, betting can be right even when
only better hands call and no better hand folds.

Game theory reduces the reasons to bet to two:

1. **Leverage the informational advantage of knowing your own cards.**
2. **Realize your equity, or stop villain realizing his.**

### Reason 1 — the informational advantage

In a GTO model villain knows your whole strategy, so you can't "surprise" him
with an odd holding. Your only edge is that **you know your exact hand and he
only knows your range**. That gap is valuable when **villain's correct response
changes a lot depending on which hand you hold.**

- Suppose villain should fold vs your hand type A, call vs type B and raise vs
  type C. If your betting range is all type A, his decision is trivial (always
  fold). Mixing A, B and C into one range means no single response is right
  against all of it. **Range diversity creates the informational advantage.**
- **A mistake** in this sense is a decision villain would not make if he could
  see your hole cards, not a decision that is bad against your range. Even a
  perfect GTO player makes these: with a polarized betting range he must call
  some bluff catchers and lose to value, and fold some and lose to bluffs.
  (Contrast a non-GTO error, such as shoving a bluff catcher into a polarized
  range, which makes your decision trivial: call with the nuts, fold the air.)
- **What a strong betting range looks like:** villain's EV when he calls (or
  raises) varies widely depending on which part of your range you hold. Folding
  is always worth 0, so only calls and raises matter here.

**Clairvoyance toy game check** ($100 pot, $100 stacks, P1 holds AA or QQ half
each, P2 holds KK): P1's EV is **$75** with the option to bet and **$50** without
it, so **the option to bet is worth $25**, all of it from hidden information.
Played face up, P2 would call only against QQ and never against AA, betting
would be pointless, and both players would check and take $50. The equilibrium
(AA bets 100%, QQ bets 50%) only works because P2 can't see which is which.
(If P1 held only one hand type, nuts or air, P2's response would again be
trivial and betting would be worth nothing.)

**Board coverage.** The same idea across streets: if your play turns your hand
face up, you get exploited. A flop betting range made mostly of flush draws on a
two-tone board tells villain to call and then attack blank turns. **Good board
coverage** means your range can make strong hands on a wide variety of runouts
(all of them, in a perfectly balanced strategy). Both betting and checking
ranges need it.

### Reason 2 — realizing and denying equity

In the clairvoyance game both players have 50% equity, but the polarized player
(P1) captures more than half the pot, and more the deeper the stacks, because
his bet is always all-in:

| P1's stack (× pot) | P1's EV (pot = $100) |
|---|---|
| 0.1 | ~$54.6 |
| 0.5 | ~$66.7 |
| 1 | $75 |
| 2 | ~$83.3 |
| 10 | ~$95.4 |

(These follow from EV = 50 + 50·s/(1+s), where s = stack ÷ pot. The book prints
$83.5 for 2× pot; the formula gives $83.3.)

- **Deep stacks:** more streets to play, so **range balance matters more and raw
  equity less** — the better the opponent, the more so.
- **Short stacks:** the money goes in pre-flop or on the flop, so **raw equity
  dominates.**
- Betting realizes equity by denying villain's equity and by **setting up an
  SPR** that suits your range. Range composition drives everything, which is why
  the chapter introduces equity buckets.

## The other strategic actions

| Action | Key idea |
|---|---|
| **Folding** | Never fold when you could check for free — it is **strictly dominated**. Fold only when facing a bet and neither calling nor raising is +EV. |
| **Checking IP** | Checking back **removes a betting street** and immediately realizes equity (a free card or showdown). Helps the weak part of IP's range. |
| **Checking OOP** | Does **not** guarantee equity realization — you may face a bet and have to fold part of your range. So OOP's checking range must be balanced **on the flop**, while IP's checking range only needs to be balanced **on the average turn card**. |
| **Calling** | Realizes equity (heads-up), by reaching showdown or seeing another card. |
| **Raising** | A bet on top of a bet: same two reasons (information, equity realization/denial). |

**Why never fold when checking is free:** even terrible hands have some equity or
backdoor equity that free cards can realize; some can turn into bluffs later;
and above all, if you muck your worst hands, your checks become a strong,
readable range and opponents give you action only with strong hands.

**Every action narrows your range.** After an action you can only hold hands
that take that action. A classic rookie error is representing a hand the line
can't contain. Read your own range as carefully as villain's: **if villain's
story doesn't make sense, he probably doesn't have it.**

## Equity buckets (EQB)

Linear / polarized / condensed describe a whole range's shape and are fine
pre-flop, but too coarse post-flop. **Equity buckets** classify each hand by its
**hand-vs-range equity**:

| Bucket | Hand-vs-range equity |
|---|---|
| **Strong** | ≥ 75% |
| **Good** | 50% to < 75% |
| **Weak** | 33% to < 50% |
| **Trash** | < 33% |

Bucketing every hand shows a range's post-flop equity distribution and how far
it fits each morphology.

**A hand's value is dynamic** — it depends on the ranges and the board. Equity of
made hands, UTG vs BB, 40bb (IP / BB):

| Hand | A♥Q♦T♠ | T♥9♦8♠ (rainbow) | T♦9♥8♥ (two-tone) | T♥9♥8♥ (monotone) |
|---|---|---|---|---|
| Straight | 94 / 88 | 93 / 86 | 90 / 84 | 77 / 75 |
| Set | 91 / 81 | 83 / 82 | 81 / 80 | 74 / 73 |
| Two pair | 87 / 68 | 76 / 72 | 73 / 69 | 65 / 61 |
| Top pair | 82 / 53 | 69 / 58 | 69 / 54 | 60 / 51 |
| Middle pair | 77 / 42 | 66 / 54 | 63 / 52 | 54 / 47 |
| Bottom pair | 67 / 35 | 56 / 50 | 53 / 48 | 45 / 44 |

What to notice:

- UTG's top pair is **Strong (82%) on AQT** but only **Good (60%) on monotone
  T98**. For UTG, **two pair on AQT (87%) beats a set on any T98 flop** (74–83%).
- The same made hand is worth far less to the BB on AQT (top pair 53%, bottom
  pair 35%) — the board smashes UTG's range, not the BB's. UTG's *middle* pair
  there is still a Strong hand.
- On connected and suited boards every made hand loses equity, and the gap
  between the two players' values narrows.

**Average flop buckets, all 1,755 flops** (UTG vs BB and BN vs BB, 20–40bb GTO MTT
ranges):

| Bucket | IP (pre-flop raiser) | BB |
|---|---|---|
| Strong | **22%** | 7% |
| Good | **43%** | 25% |
| Weak | 29% | 23% |
| Trash | 6% | **45%** |

The raiser has three times the BB's share of strong hands; almost half the BB's
flop range is trash. Weak-hand shares are similar.

## Bet-sizing basics

NLH lets you bet any amount. Solvers can only handle a finite **betting
abstraction**, so the practical questions are: how many sizes do we need, does
GTO require infinitely many, and is there one optimal size? For humans, even a
few sizes across several streets quickly becomes unmanageable, and a strategy
too complex to execute can cost more than it gains.

### The pot-size raise

A **pot-size bet lays 2-to-1** (the caller needs 33%). To make a pot-size raise:

1. Match the bet you face.
2. Total the pot including your matching chips.
3. Add that total on top of your matching chips.

> raise-to amount = (%pot × pot after your call) + the bet you matched

$100 pot, villain bets $50: match $50 → pot $200 →
- pot-size raise: 200 + 50 = **$250 total**
- 50% raise: 100 + 50 = **$150**
- 25% raise: 50 + 50 = **$100**

### Alpha and MDF on the flop

"My bet only has to work X% and villain folds more than that, so it prints" is a
flawed argument. Alpha and MDF come from an EV equation that assumes **checking
is worth 0** and **a called bluff loses the whole bet**. On the flop neither is
true: almost every hand has equity, and called bluffs sometimes improve.

- IP only has to make his worst hands indifferent to **the EV of checking back**,
  not to 0 — so **the BB needs to defend far less than MDF says.**
- Called bluffs that pick up equity make c-bets **more profitable** than alpha
  suggests.
- Alpha/MDF matter more on the **river**, where equity is known. Elsewhere,
  compare the EV of every action; use alpha/MDF only as rough guides, never as
  the core of a strategy.

## Should you split your range across bet sizes?

### The [0-1] game

Each player gets a random number from 0 to 1 (higher wins), single street, OOP
checks, IP bets or checks, OOP may only call or fold. The solution uses
**infinitely many sizes**: pair each value hand with a bluff from the bottom,
and bet **bigger the stronger the value hand**.

Solver replica: IP and OOP each hold one combo of AA, KK … 55 (no blocker
overlap), board 2♥2♠2♦3♠3♥, stacks 2× pot, sizes pot / ⅔ / ⅓.

| Version | What IP does | IP EV (% pot) |
|---|---|---|
| **A** – OOP can't raise | AA bets pot, KK ⅔, QQ ⅓; bluffs with 55 (plus some 66) at all three sizes; JJ–77 check. Bet 15/14/15%, check 56% | **56.11** |
| **B** – OOP may x/r the ⅓ bet | ⅓ size abandoned; QQ moves to ⅔. Bet 15/28/0%, check 57% (forcing ⅓ anyway: ~54) | **54.98** |
| **C** – OOP may x/r any size | Single pot-size bet with KK+ (plus bluffs); QQ–66 check. Bet 30%, check 70% | **54.96** |
| **D** – all-in also allowed (SPR 2) | All-in: AA 42%, 55 26%. Pot: KK 100%, AA 58% (protects the pot line vs x/r), 55 74%. All-in 7%, pot 24%, check 69% | **55.06** |
| D at SPR 4 | All-in no longer used; pot only | 55 |
| Pot-size only | — | 55 |
| ⅓-pot only | — | 53.27 |

Lessons:

- In version A, a ⅓ bet means "QQ or 55" — **a capped size**. Once raising is
  allowed, villain attacks it with a polarized raise (AA, KK + bluffs). Every
  size that holds only a narrow slice of your range is a target.
- **All-in is special:** villain can only call or fold, so a split all-in /
  pot strategy can't be raised; at SPR 2 OOP can't exploit the split.
- One well-chosen size keeps nearly all the EV; **the wrong single size is what
  costs** (pot-only 55 vs ⅓-only 53.27).
- (One passage says all-in disappears at SPR 3; the summary table says SPR 4.)

### SPR effect (single street, [0-1] game)

| SPR | Preferred sizes (check ≈ 66–70% throughout) |
|---|---|
| ≤ 1 | **All-in** (75% pot at SPR 0.75; pot at SPR 1) |
| 1.5–2 | Split **pot + all-in** |
| 3 | Split **75% + 125%** (all-in dropped) |
| 5–10 | Split **75% + 150%** |

Dropping the less-used size (one size only) cost on average **0.21% of the pot**
(0.06–0.34% depending on SPR), the loss shrinking roughly as SPR falls.

### Conclusions on multiple sizes

- **Multiple sizes leak information** that villain can attack with raises and
  bets. The danger is worse on **early streets**, across **multiple streets**, and
  when runouts change hand values or blockers matter — use **fewer** sizes then.
- So GTO doesn't really need infinite sizes: the EV of a perfect size per hand
  is traded against what the extra information gives away. Even when solvers
  balance many sizes, the gain rarely justifies the difficulty for a human.
- Across 1,755 flops, **most flops have one or two dominant sizes**. Simplify:

| Solver output | Simplification (≈ no EV loss) |
|---|---|
| Two close sizes (25% vs 33%) split evenly | Keep the more frequent one — EVs are virtually identical |
| One dominant size + several rare ones | Drop the rare ones |
| Two sizes far apart | Replace both with one size in between |

- Removing **small** sizes usually **lowers** your betting frequency (hands
  profitable at a small size aren't at a large one); removing **large** sizes
  **raises** it.
- Against a GTO opponent, splitting by hand strength adds little; against a
  mistake-prone opponent, **exploitative size changes can be very profitable.**

## Is there an optimal bet size?

Bet size depends on **polarization** and **streets left**. Single street:
perfectly polarized vs bluff catchers → bet everything; the depolarized player
→ bet 0 (always check). Symmetric ranges ([0-1] game) → bet big, capped by SPR.

### Geometric bet sizing

With a polarized range over several streets, the EV-maximizing plan in the
multi-street clairvoyance game is **geometric**: bet the **same fraction of the
pot every street so the river bet is exactly all-in**.

> FP = SP × R^S &nbsp;&nbsp;→&nbsp;&nbsp; R = (FP ÷ SP)^(1/S)
>
> geometric bet = pot × (R − 1) ÷ 2

FP = final pot, SP = starting pot, R = pot growth per street, S = betting
streets. The ÷2 is because a called bet adds two bets to the pot.

**Shortcut (derived, not in the book):** with both players all-in at the end,
FP ÷ SP = **1 + 2 × SPR**. SPR 4, two streets → √9 = 3 → bet **pot**. SPR 13, three
streets → ∛27 = 3 → **pot** each street.

**Book example:** $5/$10 live, effective stack $1,000. SB opens to $35, BB calls;
pot $70, final pot $2,000, 3 streets. R = (2000/70)^(1/3) ≈ 3.06 → bet ≈ **1.03 ×
pot**: flop **$72.10**, turn **$220.63** into $214.20, river **$675.12** into $655.45.

Caveats:

- Deep stacks make geometric bets huge overbets.
- Real ranges are never perfectly polar vs pure bluff catchers. Bet too big and
  villain folds everything except hands that beat you, so value bets stop
  working — there's a **cap below the geometric size**, especially when deep.
- The message that survives: **a polarized range wants big bets across several
  streets.**

### Range polarization effect (single street)

Board 2♥2♠2♦2♣3♥ (pure pair-ranking), SPR 4, IP may bet 30/60/90/120% or all-in;
OOP checks but may raise; equity always 50/50.

| Game | IP range vs OOP range | IP EV | Strategy |
|---|---|---|---|
| A | QQ–66 vs AA–44 (IP very depolarized) | 50.00% | Check 100% |
| B | KK–55 vs AA–44 | 50.16% | Bet ~15% at 60%; check 85% |
| C | AA–44 vs AA–44 (symmetric) | 55.02% | 90% and 120% (~12–14% each); no all-in |
| D | AA–44 vs KK–55 | 62.16% | 120% (14.5%) slightly ahead of all-in (13.9%) |
| E | AA–44 vs QQ–66 (IP very polarized) | 69.23% | **All-in 32.7%** dominant; small/medium sizes unused |

**More polarization advantage → bigger sizes and more EV**; the 30% size is
essentially never used. Perfect polarization vs pure bluff catchers → all-in
only.

### Multi-street betting (turn with a river to come)

Same ranges, board 2♥2♠2♦2♣ (turn), SPR 4, same sizes; both players can act on
the river. Equities are no longer exactly 50/50.

| Game | IP EV | IP equity | IP turn strategy |
|---|---|---|---|
| A | 28.89% | 45.98% | Check 100% |
| B | 39.67% | 47.77% | **Check 100%** |
| C | 52.87% | 50.00% | 30% size 35%; check 65% |
| D | 67.94% | 52.24% | 30% 53%, 60% 19%; check 27% |
| E | 81.33% | 54.02% | 30% 52%, 60% 29%, 90% 9%; check 9% |
| F (OOP JJ–77) | 92.46% | 55.37% | Bets ~100%: 30% 56%, 90% 32%, 120% 11% |

- **Even a slight polarization disadvantage stops IP betting at all** with a street
  to come (in the single-street game B still bet a little). Checking back
  removes a street and takes the whole range to the river; betting would face
  x/r and force folds; overbetting a weaker range just loses.
- With symmetric ranges IP starts betting — but **small**. The geometric size for
  SPR 4 over two streets is pot, yet the solver bets far smaller; IP needs a much
  bigger polarization edge before big sizes dominate.
- **Range merging (game E):** bet **small, often, with strong and middling hands
  together**. If IP polarized (big bets with top and bottom, checking TT–88), OOP
  would bet the river into the capped checking range. A merged small bet raises
  betting frequency, and after OOP calls he usually checks the river, letting IP
  check back middling hands and realize equity.
- Multi-street play always helps the player with the polarized range.

**Conclusion:** the more polarized you are relative to villain, the bigger you
bet. With streets to come, bet **smaller and merged early**, and polarize on later
streets — unless your polarization edge is very large, in which case sizes
approach geometric (unless SPR is very high and villain may be trapping).
**All-ins on early streets are rare unless stacks are shallow.**

## Bet sizing by flop

Different flops shift equity and polarization differently, so GTO uses
flop-specific sizes. Test: BN vs BB SRP, 40bb, all 1,755 flops (weighted to
represent all 22,100): four c-bet sizes (min, ⅓, ½, ⅔) vs **⅓ only**.

| Simulation | IP EV (% pot) |
|---|---|
| Four sizes | 71.13 |
| ⅓ pot only | 70.98 |
| Loss | **0.14% of pot ≈ 0.9 bb/100** |

That's an **upper bound** on the loss from one size per flop: a solver allowed
all four sizes per combo can't do worse than one restricted to the single best
size per flop. It is spread over every flop, and assumes perfect play by both.

**The author rejects "one size fits all"** anyway. You aren't playing GTO
opponents. Board-appropriate sizes make your own hands easier to play and make
life harder for opponents unused to varied sizes; and if *they* use a GTO size
you know how to defend, while a non-GTO size is a leak to exploit.

**Example — J♠2♥2♦:** BB calls a UTG min-raise at 30bb. UTG's GTO play is to
**min-bet 100%**. If UTG c-bets ⅔ pot with the whole range, the BB exploits with
a **check-raise-only** strategy and UTG's EV falls well below GTO; the best
⅔-pot strategy (c-bet ~42%) still loses EV to the min-bet. A player who uses a
non-standard size probably isn't balancing it either — look for the exploit.

**Practical sizing:**

- Solvers are nearly indifferent between close sizes (25 vs 33%, 60 vs 67%).
  Mostly you just need to know whether a flop is a **"small-bet" or "big-bet"
  flop**.
- **MTT recommendation: two c-bet sizes, ⅓ and ⅔ pot.** More complex: add
  min-bets and ~120% overbets. Simplest: ⅓ everywhere — what most online MTT
  regs do. It's easy, lets you c-bet very often, forces villains to reveal
  information cheaply, and exploits the population's **overfolding to small bets**.
- Master at least one big and one small size. Against weak players play
  exploitatively and don't fear counter-exploitation until they actually fight
  back.
- You don't need perfect GTO to win — just better average decisions than your
  opponents, and keep improving.

## Bet sizing and modern solvers

- **A solver can't choose bet sizes** — you build the tree, and the sizes you
  give are the only ones that exist. Missing options skew results: if OOP can't
  x/r the flop, IP bets more often because his equity can't be denied. Give every
  player sensible responses, unless you're deliberately modelling a leak.
- **Each added size grows the tree exponentially** — slower to solve and harder
  to execute. Test common fractions (½, ⅔), not absurd ones.
- **The indifference trap:** near-equal EVs for betting and checking a combo hold
  only at equilibrium. If GTO bets every hand 50%, betting the top half 100% and
  checking the bottom half 100% has the same frequency but is badly exploitable
  (villain folds more to bets and attacks checks). Keep ranges roughly balanced
  with board coverage; before a big simplification, **lock it in the solver and
  re-run** to measure the loss vs a min-exploitative opponent.
- **Indifference is created by villain's play.** Against an opponent whose
  strategy is unbalanced, a "close" spot becomes binary: one action is simply
  better.

## Takeaways for the table

1. Bet because your range makes villain's correct response depend on your exact
   hand, or to realize/deny equity — not because a hand is "for value".
2. Never fold when you can check; check OOP only with a range that can defend.
3. Think in equity buckets: the raiser holds ~3× the strong hands and the BB ~45%
   trash on an average flop — but board texture moves every hand's value.
4. Fewer sizes on early streets: a size that holds only one slice of your range
   gets raised. Know whether the flop is a small-bet or big-bet flop; ⅓ and ⅔
   cover most MTT spots.
5. Polarized with streets to come → bet small and merged early, bigger later;
   big polarization edge → approach the geometric size (pot growth 1 + 2 × SPR).
6. Alpha/MDF overstate flop defence; compare the EV of every action.
7. Solver indifference only holds at equilibrium — against unbalanced opponents
   pick the clearly better action.
