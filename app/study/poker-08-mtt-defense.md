---
title: "Poker 08 — MTT Equilibrium Strategies: Defense"
summary: "Modern Poker Theory ch. 8: responding to open raises and open shoves, overcalling, BB vs SB (push, raise, limp), and defending the BB, SB, BN, CO, HJ and UTG+1 at 15/25/40/60bb."
order: 108
audience: bravosierra99
---

# Poker 08 — MTT Equilibrium Strategies: Defense

*Study guide to Chapter 8 of* Modern Poker Theory *(Michael Acevedo). The chapter
is ~125 solver range grids (Hand Ranges 140–266). This guide gives the headline
frequencies and the shape of each range; open the book for the exact cells.
All numbers are 9-handed MTT equilibrium solutions (the same solver set-up as
the previous chapter: chip-EV, no ICM, with antes).*

## The four forces that shape every defending range

Everything in the chapter is one of these four ideas applied to a seat and a stack:

| Force | Effect on your defence |
|---|---|
| **Opener's range strength** (earlier seat = stronger) | Less fold equity → fewer rejams and bluffs, tighter value range, better hands used as bluffs |
| **Your position** | The BB closes the action at a discount and defends very wide; every other seat defends tight because players are left to act and (for the SB) you'll be OOP |
| **Stack depth** | Shallow: rejam (3-bet = all-in). Deeper: small 3-bets appear, jams disappear, playability matters more than raw equity |
| **Players behind** | The more players who can call or squeeze, the more dangerous it is to split your range into flats — so earlier seats flat less and 3-bet-or-fold more |

## Average response to an open raise

**By your seat** (averaged over stack depths and opener positions; blind-vs-blind excluded):

| Your seat | All-in | 3-bet | Call | Fold | Total 3-bet |
|---|---|---|---|---|---|
| BB | 4.7% | 5.9% | 60.3% | 29.1% | 10.6% |
| SB | 6.2% | 6.0% | 10.6% | 76.8% | 12.2% |
| BN | 3.4% | 4.4% | 12.9% | 79.3% | 7.8% |
| CO | 3.2% | 4.0% | 8.7% | 84.1% | 7.3% |
| HJ | 2.7% | 4.0% | 6.4% | 86.9% | 6.7% |
| LJ | 2.3% | 3.8% | 5.0% | 84.7%* | 6.1% |
| UTG+2 | 2.0% | 3.9% | 3.5% | 90.7% | 5.8% |
| UTG+1 | 1.8% | 3.9% | 2.6% | 91.7% | 5.7% |

*\*as printed in the book; the row doesn't sum to 100% (≈88.9% would).*

What to remember:

- **The BB is a different animal**: it folds only ~29% and calls ~60%. Every other seat folds 77–92%.
- **The SB is the most aggressive seat** (highest total 3-bet, ~12%) but calls little: it is OOP with the BB still behind, so it prefers to end the hand or take the lead.
- **The BN is the best flatting seat** outside the blinds (~13% calls): guaranteed position, only the blinds behind.
- Moving earlier, **calling collapses** (13% → 2.6%) while the non-all-in 3-bet stays ~4%. Early seats play 3-bet-or-fold.

**By the opener's seat** (your response averaged over all your possible seats):

| Opener | All-in | 3-bet | Call | Fold | Total 3-bet |
|---|---|---|---|---|---|
| BN | 9.6% | 9.5% | 35.3% | 45.5% | 19.1% |
| CO | 6.8% | 6.7% | 28.3% | 58.2% | 13.5% |
| HJ | 5.1% | 5.3% | 23.2% | 66.4% | 10.5% |
| LJ | 4.0% | 4.8% | 19.9% | 71.3% | 8.8% |
| UTG+2 | 3.2% | 4.4% | 16.8% | 73.4% | 7.6% |
| UTG+1 | 2.7% | 4.0% | 15.3% | 78.1% | 6.6% |
| UTG | 2.3% | 3.8% | 14.0% | 79.7% | 6.0% |

A BN open gets 3-bet about **three times as often** as a UTG open (19% vs 6%) and
folded to far less (46% vs 80%).

## Facing an open shove

> **One-third rule:** if calling costs **more than 1/3 of your stack**, rejam instead of calling. If it costs **less than 1/3**, just call with your whole continuing range.

- Over 1/3: you're committed anyway, so shove to isolate. Exception: heavy ICM/bubble spots, where you may flat and even fold if someone else comes in behind.
- Under 1/3: no need to risk your stack with deep players still to act. A **min-re-raise** is an option when the shove is small and you want to be heads-up.
- Example: UTG jams 6bb, everyone else has 35bb. In the CO, **flat the 6bb**. Players behind should play straightforwardly (rejam only their best hands) because your flatting range still holds all the premiums alongside the lighter calls.
- How wide to call depends on **pot odds, your position, and the shover's position/stack**. Earlier shover and deeper shove → tighter call.
- Practise with a push/fold app, then compare the theoretical shoving ranges with what people actually shove. Many shove too tight (call tighter) or too loose (call wider).

## Overcalling (raise and a call in front of you)

**Play tighter than you would against a raise alone.** This feels backwards (more
dead money, and the caller didn't 3-bet so is capped), but the caller's range is
still strong and can stand a 3-bet, so marginal squeezes and marginal overcalls
both end up playing post-flop against strong ranges.

- Because the range is tight, most of it prefers **3-betting (squeezing) to cold-calling**.
- Hands that do overcall well keep their equity multi-way and can dominate: **suited Ax, suited connectors, suited broadways, small/medium pairs**.
- Worst multi-way hands: **offsuit high-low and offsuit gappers (K5o, Q7o)** — dominated, poor equity realization, worse OOP.

## Big blind vs small blind

BvB is the **only spot where the BB has position for the whole hand**, so its EqR
is far higher than against any other opener and it can defend very wide. The SB
responds by **limping a lot** and by **raising big (or all-in)** to cut the BB's odds.

### BB vs SB open jam

| Stack | Call | Fold |
|---|---|---|
| 10bb | 44.5% | 55.5% |
| 12bb | 38.4% | 61.6% |
| 15bb | 28.9% | 71.1% |
| 17bb | 27.6% | 72.4% |
| 20bb | 23.4% | 76.6% |
| 25bb | 17.8% | 82.2% |

- Bigger jam = worse pot odds = tighter call.
- **12bb:** all pairs, all Ax, broadways, all Kxs, K5o+, Q7s+, J8s+, T8s+. A little tighter at 15bb.
- **25bb:** 33+, A7o+, A6s+, suited broadways, KQo, QJo. (QJo makes it and KJo doesn't — QJo has more equity against the SB's jamming range.)
- These are **tighter than push/fold charts** suggest, because of the bunching effect and because a SB who can also limp or raise small jams a different range than a jam-or-fold SB.

### BB vs SB raise

| Stack | SB size | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|---|
| 17bb | 2.5x | 15.4% | – | 62.7% | 15.4%* |
| 20bb | 2.5x | 11.9% | – | 70.2% | 17.9% |
| 25bb | 3.3x | 10.6% | – | 53.8% | 35.6% |
| 30bb | 3.5x | 5.4% | 7.0% | 49.4% | 38.2% |
| 40bb | 3.5x | – | 12.3% | 52.0% | 35.7% |
| 60bb | 3.5x | – | 12.0% | 54.3% | 33.6% |
| 80bb | 3.5x | – | 12.3% | 55.3% | 32.3% |

*\*as printed; the 17bb row doesn't sum to 100%.*

- **Below 30bb the BB's only 3-bet size is all-in.** It **traps 88+** by calling and **rejams high-equity, poor-playability hands: 77–22 and offsuit Ax**.
- The BB's fold frequency roughly doubles (≈15–18% → ≈32–38%) from the 2.5x opens at 17–20bb to the 3.3–3.5x opens at 25bb+, consistent with why the SB sizes up: worse odds for the BB.
- **40bb:** no jams. 3-bet is **polarized**: TT+, AJ+ for value; bluffs are mostly **offsuit** hands chosen for blockers (Axo, Kxo) or board coverage (J7o, T4s, 98o). Versus a 4-bet jam the BB calls **66+, AJs+, ATo+** (46%).
- **60bb:** same ~12% total, but bluffs are spread thinly over more hand types for better board coverage. Versus a 2.6x 4-bet: 5-bet jam 27.4% (JJ+, AQ+), call 14.2% (best suited connectors, AJ, smaller pairs), fold 58.5%. **AA slowplays 68%** of the time.

### BB vs SB limp

| Stack | All-in | Raise | Raise size | Check |
|---|---|---|---|---|
| 10bb | 29.6% | 16.4% | 2x | 53.9% |
| 12bb | 20.3% | 25.2% | 2.5x | 54.5% |
| 15bb | 8.2% | 33.7% | 3x | 58.1% |
| 17bb | 10.4% | 33.6% | 3x | 56.0% |
| 20bb | 7.6% | 34.4% | 3x | 58.0% |
| 25bb | 4.4% | 37.8% | 3.3x | 57.8% |
| 30bb | 2.1% | 40.8% | 3.5x | 57.1% |
| 40bb | – | 44.0% | 3.5x | 56.0% |
| 60bb | – | 43.8% | 3.5x | 56.2% |
| 80bb | – | 43.7% | 3.5x | 56.3% |

- **Rule: on average check ~56%, attack ~44%** (checks stay within 54–58% at every depth). Only the mix of jam vs raise changes.
- **Size grows with depth: 2x at 10bb → 3.5x at 30bb.** The solver wants even bigger when deeper, but 3.5x loses almost nothing, and the author thinks bigger is overkill — real limping ranges are unbalanced and **over-fold to raises**, so smaller sizes work exploitatively against weak players.
- **Jamming range (short):** blockers + high equity + terrible post-flop realization → **small pairs, offsuit Ax and Kx**.
- **Raising range:** polarized — hands happy to raise/call a limp-jam, plus board-coverage hands that raise/fold.
- **At ~12–15bb, check back every suited hand that can't raise/call.** Raising it and folding to a limp-jam throws away its equity.
- **25bb:** fewer jams (same hand types); the raise range adds a little of the worst suited hands (J4s, 96s, 62s) for playability.
- **40–60bb:** no jams; a wider mix of suited and offsuit raises. Being limp-raised is no disaster because the BB is IP and deep enough to call with its best suited hands.
- Versus a limp-jam the BB calls 43.4% at 15bb and 29.8% at 25bb. Versus a limp-raise it folds about half (49.6% at 40bb, 53% at 60bb).

## Defending the BB vs an in-position raiser

| Stack | Opener | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|---|
| 15bb | BN | 18.0% | – | 58.2% | 23.8% |
| 15bb | CO | 16.4% | – | 60.4% | 23.2% |
| 15bb | LJ | 11.0% | – | 66.7% | 22.3% |
| 15bb | UTG | 7.4% | – | 70.6% | 22.0% |
| 25bb | BN | 11.4% | 8.2% | 65.9% | 14.6% |
| 25bb | CO | 8.8% | 5.5% | 67.1% | 18.6% |
| 25bb | LJ | 5.1% | 5.0% | 66.8% | 23.2% |
| 25bb | UTG | 2.1% | 4.7% | 66.0% | 27.2% |
| 40bb | BN | 3.0% | 14.1% | 58.6% | 24.2% |
| 40bb | CO | 1.3% | 11.5% | 56.2% | 31.0% |
| 40bb | LJ | 0.2% | 7.8% | 54.2% | 37.8% |
| 40bb | UTG | – | 5.8% | 49.1% | 45.0% |
| 60bb | BN | – | 16.8% | 65.1% | 18.1% |
| 60bb | CO | – | 11.7% | 63.1% | 25.2% |
| 60bb | LJ | – | 7.4% | 56.5% | 36.0% |
| 60bb | UTG | – | 5.3% | 50.6% | 44.1% |

### 15bb — jam or call, fold a flat ~22%

- Too shallow for a non-all-in 3-bet. Average: jam 12.1%, call 65.3%, fold 22.6%.
- **The fold frequency doesn't move with the opener's seat.** What moves is the split: jams fall 18% → 7.4% from BN to UTG and calls rise to fill the gap.
- **What to rejam:** hands that are *ahead of the opening range but realize equity badly post-flop* — better to get the money in now.
  - Most **pocket pairs**. Exceptions: **AA/KK slowplay vs LP**; the smallest pairs mix vs EP.
  - **Offsuit Ax vs LP**; versus EP there's less fold equity, so **suited Ax** replaces them.
- **The kicker lesson.** KQs has great equity when called, yet it *calls* against every seat, while **K5s–K3s rejam**. Strong Kx coolers the opener post-flop and plays well, so it loses value by ending the hand. Weak-kicker Kx gains most from fold equity and still has adequate equity when called.
- Same pattern with suited aces vs a LJ open: **jam AKs–AJs** (too strong not to), **flat ATs–A6s and A2s** (playable, dominating), **jam A5s–A3s** (blocker + fold equity).

### 25bb — small 3-bets appear, EP folds rise

- Average fold still ~22.5%, but now **14.6% vs BN up to 27.2% vs UTG** (~28% vs EP): deep enough that weak hands can't realize equity OOP against strong ranges.
- **Jams** shrink with opener strength (11.4% → 2.1%). Pairs and Axo love to jam; weaker pairs and Ax get added as the opener gets wider.
- **Non-all-in 3-bet** is steady at ~5% (8.2% vs BN) and **polarized**: JJ+, the strongest Axs, a few premium suited connectors, plus a small frequency of **offsuit blocker bluffs** (A8o–A2o, K6o–K2o, some Qxo/Jxo).
- Versus a 4-bet (a jam at this depth) the BB continues ~56–60%.

### 40bb — jams nearly gone, fold much more vs EP

- Too deep to rejam most seats: 3% vs BN, zero vs UTG. No fold equity against narrow ranges.
- **Fold rises steeply: 24.2% vs BN → 45% vs UTG.** Average defence 62.9%.
- **The "I can outplay him" leak.** Regs defend any two vs EP opens because the opener's range is defined. But equity and EqR don't care: **wide + OOP + tight opponent + high SPR** produces tough call-downs and spewy bluffs on boards that "hit the BB".
- **Versus EP: defend tighter, 3-bet rarely, and bluff with better hands.** Value shrinks from **99+, ATs+, AJ+ vs BN** to **TT+, AK vs UTG**; fewer value hands means fewer bluffs, and the bluffs vs UTG are entirely different hands from those vs BN.
- Versus a 4-bet the BB continues about half the time (47–50%).

### 60bb — slightly wider, less polarized

- Average defence ticks up to 65.6% (from 62.9%). Either weaker hands gain implied odds, or it's an artefact of the simulation design.
- **Overbet caveat.** IP's main weapon for cutting OOP's EqR when deep is the **overbet**, and sims that allow overbets should show less BB defence. Players under-use overbets today, so these ranges hold up — but **trim the weakest defends against tough opponents who overbet and apply pressure**.
- 3-bet range is **less polarized** than at 40bb: more suited, playable hands. Frequency 16.8% vs BN down to 5.3% vs UTG.
- **Versus a 4-bet:** healthy flatting range vs LP (call 40.5% vs BN, 36.5% vs CO) but close to **5-bet-or-fold vs EP** (call 13.1% vs LJ, 6.1% vs UTG; jam 36.6% and 40.3%).

## Defending the small blind

| Stack | Opener | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|---|
| 15bb | BN | 28.2% | – | 0.0% | 71.8% |
| 15bb | CO | 22.5% | – | 0.1% | 77.4% |
| 15bb | LJ | 14.7% | – | 5.4% | 79.9% |
| 15bb | UTG | 9.4% | – | 11.6% | 79.0% |
| 25bb | BN | 14.2% | 6.5% | 6.0% | 73.2% |
| 25bb | CO | 11.2% | 5.5% | 9.9% | 73.3% |
| 25bb | LJ | 6.4% | 5.3% | 12.6% | 75.7% |
| 25bb | UTG | 3.5% | 4.8% | 14.2% | 77.5% |
| 40bb | BN | 2.3% | 14.1% | 11.7% | 71.8% |
| 40bb | CO | 1.0% | 12.1% | 12.7% | 74.2% |
| 40bb | LJ | 1.0% | 8.0% | 12.2% | 78.8% |
| 40bb | UTG | – | 6.6% | 12.7% | 80.7% |
| 60bb | BN | – | 16.2% | 17.2% | 66.6% |
| 60bb | CO | – | 12.3% | 15.6% | 72.2% |
| 60bb | LJ | – | 8.1% | 13.9% | 78.1% |
| 60bb | UTG | – | 5.6% | 13.8% | 80.6% |

- **15bb (VPIP ~22%):** **rejam-or-fold vs LP** — 28.2% vs BN, 22.5% vs CO, zero calls. From MP back the opener is too strong for the weaker jams to get folds, so hands that are no longer profitable jams but still profitable calls become **flats** (11.6% vs UTG). Since the BB usually comes along, the flats are hands that hold equity multi-way: **suited connectors, small suited Ax, broadways**. **AA slowplays 25–33%.**
- **25bb:** VPIP falls as the opener gets stronger. Offsuit hands are mostly folded, except **Axo rejams vs LP**. Offsuit broadways can call vs LP, fold vs EP. **Small pairs: rejam vs LP, call vs EP** (no fold equity). **3-bet/fold hands get stronger vs EP**: A5s–A2s, AJo, ATo vs EP, compared with A8o–A3o, KJo, KTo vs BN.
- **40bb:** the solver's jam range is tiny (88–66, 44, 33, AQo, AJo, A4s, A3s, KJs, KTs, QTs, JTs) — the author **drops it entirely** in practice. **Calls are flat at ~12% vs every seat**; medium Axo and offsuit broadways sometimes call vs LP and fold vs EP. **The 3-bet does the adjusting: 6.6% vs UTG → 14.1% vs BN.** Vs BN, value widens to AQs–ATs, AJo, 55+ and 3-bet/folds to A9o–A7o, K7s–K5s, offsuit broadways.
- **60bb (VPIP ~24%; 33.4% vs BN, 19.4% vs UTG):** 3-bet **more playable hands**, since you'll usually see a flop OOP. IP is too deep to 4-bet jam, so the SB can **call many 4-bets** (53.8% vs BN) with high-equity hands that play well in 4-bet pots. Versus EP 4-bets it shifts toward jamming (38.5% vs UTG).

## Defending the button

| Stack | Opener | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|---|
| 15bb | CO | 14.3% | – | 4.1% | 81.6% |
| 15bb | LJ | 10.6% | – | 4.0% | 85.4% |
| 15bb | UTG | 7.5% | – | 5.0% | 87.5% |
| 25bb | CO | 5.9% | 3.0% | 13.5% | 77.5% |
| 25bb | LJ | 3.5% | 3.5% | 13.8% | 79.3% |
| 25bb | UTG | 1.2% | 3.7% | 14.6% | 80.5% |
| 40bb | CO | – | 7.5% | 19.6% | 72.9% |
| 40bb | LJ | – | 6.9% | 16.9% | 76.3% |
| 40bb | UTG | – | 5.2% | 15.9% | 78.9% |
| 60bb | CO | – | 11.5% | 16.9% | 71.6% |
| 60bb | LJ | – | 8.6% | 15.6% | 75.8% |
| 60bb | UTG | – | 5.5% | 16.3% | 78.3% |

*(15bb UTG row is from the summary table; the grid caption in the book repeats the LJ numbers.)*

- **15bb (VPIP ~15%):** mostly rejam, with a small steady **flat of ~4–5%**: middle/small pairs, suited broadways, suited Ax and **slowplayed AA**.
- **25bb (VPIP ~21%):** rejam 5.9% vs CO but only 1.2% vs UTG — the author **scraps the tiny EP jam ranges** for simplicity. Small 3-bet steady at ~3.3%, calls steady at ~14%. Flats are high-equity hands that benefit from position: small/medium pairs, suited Ax, suited connectors, broadways, plus **AA/KK traps**.
- **40bb:** **no all-in range.** VPIP 21.1% vs UTG → 27.1% vs CO, with 3-bets and calls both growing as the opener widens. 3-bet is polarized: **offsuit medium-kicker Ax and offsuit broadways as bluffs vs LP, replaced by suited Ax vs EP**; middle-to-low **Kxs** are good bluffs throughout. Flats: middle/small pairs, Axs, suited connectors, suited broadways, plus offsuit broadways vs LP.
- **60bb:** calls stay ~16–17%; the 3-bet shrinks as the opener strengthens (11.5% → 5.5%). Range is very polarized, but **don't 3-bet trash** — you will play deep post-flop against a strong range. Versus a 4-bet: jam 31–36%, call 12–19%, fold ~50%.

## Defending the cutoff

| Stack | Opener | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|---|
| 15bb | HJ | 13.3% | – | – | 86.7% |
| 15bb | LJ | 11.7% | – | – | 88.3% |
| 15bb | UTG | 8.3% | – | – | 91.7% |
| 25bb | LJ | 2.8% | 3.8% | 10.0% | 83.4% |
| 25bb | UTG | 1.2% | 4.2% | 9.7% | 85.0% |
| 40bb | LJ | – | 6.2% | 12.3% | 81.5% |
| 40bb | UTG | – | 4.9% | 12.8% | 82.3% |
| 60bb | LJ | – | 7.5% | 11.7% | 80.8% |
| 60bb | UTG | – | 5.2% | 13.0% | 81.8% |

- **15bb: no flatting range at all.** Unlike the BN, the CO has the BN behind who can call or squeeze; splitting the range is too risky, so **rejam everything playable**. Vs UTG (8.3%): **66+, AJo+, ATs+, KTs+, QJs**. Vs HJ (13.3%): add A9s, A5s, ATo, KQo.
- **25bb:** the jam range is narrow → in practice play **3-bet/call/fold**. 3-bet ~3.8%, narrow and polarized. Flat ~10% with a **capped** range: mid/small pairs, suited broadways, ATo+, KJo+. Capped is fine because **the opener's strong range protects you** (players behind must respect it). The flat stays ~10% even vs wider openers: the CO might end up OOP to the BN, which limits how much it can peel.
- **40bb:** 3-bet/call/fold. Polarized 3-bet, 4.9% vs UTG → 6.7% vs HJ. Best bluffs: **mid-to-low suited Ax and Kx, AJo, ATo, KQo**; vs wider ranges add KJo and K9s–J9s and widen value to 88+, AQo+. Flats: mid/small pairs, suited Ax, suited broadways, premium suited connectors, occasional AA/AKs slowplay.
- **60bb:** 3-bet is **blocker-driven** (small frequencies of suited and offsuit Ax, Kx). Flats: suited broadways, suited Ax, suited connectors, pairs, AKo–AJo. **Versus a UTG 4-bet: mostly jam (39%) with a tiny call (7.7%); versus a later 4-bet: call rises to ~22%, jam falls to ~29%, and AA slowplays.** Reason: the 3-bet range vs UTG is more polarized, so its continues play better as 5-bets than calls.

## Defending the hijack

| Stack | Opener | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|---|
| 15bb | LJ | 10.4% | – | – | 89.6% |
| 15bb | UTG | 8.5% | – | – | 91.5% |
| 25bb | LJ | 1.8% | 4.5% | 7.3% | 86.4% |
| 25bb | UTG | 1.1% | 3.9% | 8.0% | 87.0% |
| 40bb | LJ | – | 6.1% | 9.2% | 84.7% |
| 40bb | UTG | – | 4.9% | 8.9% | 86.3% |
| 60bb | LJ | – | 7.4% | 8.8% | 83.8% |
| 60bb | UTG | – | 5.2% | 9.3% | 85.5% |

- **15bb:** rejam a **linear** range, ~9.3% on average. Vs UTG (8.5%): 66+, AJo+, ATs+, KTs+, QJs. Vs the LJ (10.4%) add some A9s, KQo and JTs.
- **25bb:** the solver jams only ~1.45% → **ignore the jam range**. Simplification rule: **a call/rejam mix becomes a pure call; a 3-bet/rejam mix becomes a pure non-all-in 3-bet.** 3-bet ~4.4%, polarized: top of range plus bluffs such as **ATs–A7s, AJo, ATo, KTs, K9s, KQo** — *stronger* bluffs than the CO or BN use. Call ~7.3%: 99–55, AQo, AJo, KQo, suited broadways, some suited Ax (AQs–A8s, A7s, A5s, A4s).
- **40bb:** 3-bet ~5.5%, polarized; 3-bet/folds are mid-to-low suited Ax, AJo, ATo, KQo and some Kxs. Calls: pairs, AQo, AJo, KQo, suited broadways, suited connectors (**more suited connectors the wider the opener**).
- **60bb:** 3-bet ~6.1% (7.4% vs LJ, 5.2% vs UTG). The 3-bet/fold hands are high-equity, good-blocker, playable: **AQo–ATo, A9s–A5s, KQo, KJs–K8s**. Calls: pairs, AQo–AJo, KQo, suited broadways, suited Ax, a few premium suited connectors. Versus a UTG 4-bet: jam 39.2%, call 6.9%, fold 53.9%. Versus a LJ 4-bet: jam 28.2%, call 24.5%.

## Defending UTG+1 (vs UTG)

| Stack | All-in | 3-bet | Call | Fold |
|---|---|---|---|---|
| 15bb | 7.2% | – | – | 92.8% |
| 25bb | – | 5.1% | 3.6% | 91.2% |
| 40bb | – | 4.8% | 4.0% | 91.2% |
| 60bb | – | 5.7% | 2.9% | 91.4% |

- **Fold ~91–93% at every depth.**
- **15bb:** rejam a linear ~7% range, nothing else.
- **25bb:** no jam range. Flat 3.6% (**JJ–66, AQo+, suited broadways**). 3-bet 5.1%, **less polarized** than LP/MP 3-bets at this depth — the 3-bet/fold hands are stronger.
- **40bb:** 3-bet 4.8% with more suited Ax (**A9s–A5s**) and fewer suited broadways; the suited broadways move into the (4%) flatting range.
- **60bb: 3-bet more (5.7%), call less (2.9%).** At 40bb UTG answers a 3-bet mainly by **4-bet jamming**, which makes UTG+1 fold a lot and denies its equity. At 60bb UTG mostly **calls and plays OOP**, so the 3-bettor realizes its equity in position and can profitably 3-bet wider. Versus a 4-bet at 60bb: jam 40.5%, call 4.4%.

## Cross-cutting patterns

| Pattern | Why |
|---|---|
| **Rejam hands = high equity, low playability** (small pairs, offsuit Ax, weak-kicker Kx/Axs) | They gain from fold equity and from never playing a flop; they're still OK when called |
| **Strong, playable hands flat** (KQs, ATs–A6s, big pairs as traps) | They dominate the opener's range and realize equity well post-flop |
| **Offsuit blockers bluff vs LP; suited Ax bluff vs EP** | Vs wide ranges fold equity carries offsuit hands; vs tight ranges you get called more and need equity + playability |
| **Value shrinks → bluffs shrink** | Polarized ranges keep a ratio; fewer value 3-bets vs EP means fewer bluffs |
| **Jams fade out by ~40bb** | Too little pre-flop fold equity, especially vs narrow EP ranges, so the solver keeps the deeper hands for small 3-bets and flats |
| **The author drops tiny jam ranges** (SB 40bb; BN 25bb vs EP; CO and HJ 25bb entirely) | Negligible EV, much simpler to execute |
| **Flats shrink the more players are behind** | Squeeze risk and possibly playing OOP; a strong opener gives a capped flatting range some protection |
| **Versus 4-bets at 60bb: call vs LP, jam-or-fold vs EP** | 3-bet ranges vs EP are more polarized, leaving few hands that want to call |
| **AA (and sometimes KK) slowplays** in the blinds and on the BN | Protects the flatting range and traps wide openers |

## Takeaways for the table

1. **Ask "who opened?" first.** Versus the BN you 3-bet ~3x as often as versus UTG. Versus EP: tighter, fewer 3-bets, better bluffs.
2. **In the BB, fold ~22% at 15bb to a min-raise, but ~45% at 40–60bb vs UTG.** "Any two because I'll outplay him" is a leak; OOP + deep + tight opener kills EqR.
3. **Rejam the hands that hate flops** (small pairs, Axo, weak-kicker suited kings and aces). **Flat the hands that love them** (KQs, medium suited aces).
4. **Short (15bb) and not in the blinds or on the BN: rejam or fold.** CO, HJ and UTG+1 have no flatting range. The SB is rejam-or-fold vs LP but flats multi-way-friendly hands vs EP; the BN keeps a small ~4–5% flat. Real flatting ranges arrive at 25bb+ and are biggest on the BN.
5. **By 40bb, put the jam button away** and play 3-bet/call/fold with a polarized 3-bet.
6. **BvB as the BB: attack limps ~44% of the time**, sizing 2x at 10bb up to 3.5x at 30bb+, and don't raise/fold suited hands when short. Call SB jams tighter than push/fold charts say.
7. **Facing an open shove: call if it costs under 1/3 of your stack, rejam if over.** After a raise *and* a call, tighten up and prefer squeezing to overcalling.
