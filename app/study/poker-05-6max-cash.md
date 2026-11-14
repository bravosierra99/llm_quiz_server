---
title: "Poker 05 — 6-max Cash Game Equilibrium Strategies (100bb)"
summary: "Modern Poker Theory ch. 5: recommended pre-flop sizings, RFI ranges by position, SB limp/raise, playing vs 3-bets, GTO vs exploitative 3-betting, and defending vs opens and 4-bets from every seat."
order: 105
audience: bravosierra99
---

# Poker 05 — 6-max Cash Game Equilibrium Strategies (100bb)

*Study guide to Chapter 5 of* Modern Poker Theory *(Michael Acevedo). The chapter
is mostly 13×13 range charts. This guide gives the headline frequencies, the shape
of each range in words and the reasons behind them. Use the book for exact
hand-by-hand weights.*

## How to use baseline charts

- The solutions are for **6-max, 100bb, online $2/$5, 5% rake capped at $3**. Treat
  them as a starting point to adjust to your own games, not as a script.
- The goal is to understand **why** the solver plays a hand a certain way, using
  pot odds, equity, EqR, SPR, polarization, board coverage, MDF and blockers, so that
  you can work out new spots yourself. Don't just memorise grids.
- Every range was solved at the sizings below. If someone uses a different size,
  your response has to change.
- Odd one-off cells in a chart (for example K6s–K5s or 53s showing up in a range
  where nothing similar does) are usually **solver convergence noise**. Ignore them
  rather than treat them as a discovery.

## Recommended pre-flop sizings

| Situation | Open | 3-bet | 4-bet | 5-bet |
|---|---|---|---|---|
| 6-max, LJ/HJ/CO/BN | 2.5bb | **IP 8.5bb**, **OOP 10bb** (add 2–3bb when squeezing) | 23bb | all-in |
| SB open (folded to) | **3bb** | BB 3-bets to 9bb | SB 4-bets to 24bb | BB all-in |
| SB limp | (1bb) | BB raises to **3.5bb**; SB limp-reraise to 13bb | BB 28bb | SB all-in |
| Heads-up (BN vs BB) | 2.5bb | BB 10bb | BN 23bb | BB all-in |

- **Out of position, go bigger.** The SB opens larger than other seats, and an OOP
  3-bet is larger than an IP one, because the OOP player wants to discourage calls
  and lower the SPR so the IP player gets less value from position.
- Live games use bigger sizes, but they are usually deeper as well, so the post-flop
  SPRs end up about the same.

## Raise-first-in (RFI) strategy

**Every seat except the SB plays raise-or-fold.** There are four reasons not to open-limp:

1. Rake makes small pots worse.
2. Other seats don't get the SB's discount for completing.
3. A limp invites more callers, and in a multi-way pot your share of the pot is smaller.
4. The more players behind you, the more likely someone raises your limp. You then
   have to put in more money or fold and give up your equity.

Raising everything you play keeps the range **protected and easy to defend against
3-bets**.

| Seat | Opens | Players behind (with position on you) | Range shape |
|---|---|---|---|
| **LJ** | **17.1%** | 5 (3) | 77+ (66 often, smaller pairs rarely), most Axs, K9s+, Q9s+, JTs, T9s, a few K7s–K5s and small suited connectors; ATo+, KJo+, some KTo/QJo |
| **HJ** | **21.4%** | 4 (2) | 66+ (55 mostly, 22–44 sometimes), all Axs, K7s+ (some K6s–K5s), Q9s+, J9s+, T9s, part of 98s/T8s, a little of 87s–54s; ATo+, KJo+, KTo, some QTo/JTo/A9o |
| **CO** | **27.8%** | 3 (1) | 44+ (22–33 about half), all Axs, K4s+, Q6s+, J8s+, T8s+, 97s+, 87s, part of 76s/65s/54s; A9o+ (most A8o), KTo+, QTo+, JTo |
| **BN** | **43.4%** | 2 (0) | all pairs, all Axs and Kxs, almost all Qxs, J4s+, T6s+, suited connectors and one-gappers down to 53s; A5o+ (some A4o), K8o+, Q9o+, J9o+, T8o+, 98o |
| **SB** | **3x 24.4% / limp 37.7% / fold 37.9%** | 1 (but OOP all hand) | plays ~62%. See below |

What gets cut as you move earlier:
- **BN → CO**: K2s, Q5s–Q2s, J6s–J4s, A7o–A2o (CO opens only a sliver of A5o),
  offsuit connectors and most suited gappers. The BN now sits behind with position
  and can call or 3-bet.
- **CO → HJ**: small pairs, the worst offsuit broadways, suited connectors and weak
  suited Kx/Qx.
- **HJ → LJ**: mainly high-equity hands with good blockers. It keeps a small share of
  suited connectors and small pairs for **board coverage**.

**Exploit:** if the blinds overfold, the BN can widen to 55–60% or more, depending
on how weak and passive they are.

### Small blind: split into limp and raise

The SB is OOP for the whole hand, which hurts equity realization, but it pays only
half price to enter. The best answer is a **mixed limp/raise strategy**:

- Limping lets the SB **play more hands** at its discount, and keeps the overall
  **raise frequency low**, so BB 3-bets win less.
- Almost every hand the SB plays is **sometimes raised and sometimes limped**, even
  premiums like AA and KK. The limping range is therefore not capped.
- It folds only the worst hands: weak offsuit hands (K3o, Q5o, J6o, T6o and lower)
  and the bottom suited hands (92s, 83s–82s, 73s–72s, 62s, 52s, 42s, 32s).
- Its raise size is the largest of any seat (3bb), because it is OOP and wants to
  discourage calls.

**BvB lines after the SB acts**

| Spot | Frequencies | Notes |
|---|---|---|
| BB vs SB limp | raise 3.5x **40.6%** / check 59.4% | **Semi-polar** raise: hands happy to call a limp-reraise IP, plus easy raise/folds |
| SB limp vs BB 3.5x | limp-reraise 13.4% / call 39.8% / fold 46.8% | Limp-reraise is **linear** (high-equity hands that play well at low SPR if 4-bet) |
| SB limp-reraise faces 4-bet | — | AA flats (98%) as a slowplay; jams KK, QQ, AK always, plus part of JJ, TT and A5s |
| BB vs SB limp-reraise | 4-bet 7.3% / call 41.3% / fold 51.4% | 4-bets TT+, AK and some Ax/Kx blocker hands |
| SB 3x faces BB 3-bet | 4-bet 17.2% / call 37.4% / fold 45.4% | Middling hands hate 4-bet/folding, so they call. The 4-bet range is **polarized**: blocker hands that are fine calling or folding to a jam and cover boards if flatted. Stacks off vs a 5-bet with **66+, AKo, AQs+** |

## Facing a 3-bet as the opener

**4-bet / call / fold (%)**

| Opener | vs HJ | vs CO | vs BN | vs SB | vs BB |
|---|---|---|---|---|---|
| LJ | 21.8 / 15.1 / 63.1 | 23.8 / 13.8 / 62.4 | 21.9 / 23.3 / 54.9 | 11.5 / 36.6 / 51.9 | 9.5 / 38.8 / 51.7 |
| HJ | | 22.2 / 14.5 / 63.3 | 21.6 / 20.8 / 57.6 | 11.1 / 36.3 / 52.6 | 9.6 / 39.1 / 51.4 |
| CO | | | 20.6 / 20.4 / 59 | 11.1 / 35.8 / 53.1 | 10.3 / 37.6 / 52.1 |
| BN | | | | 8.1 / 48.9 / 43.1 | 8.6 / 47.3 / 44.5 |

| Average | 4-bet | Call | Fold |
|---|---|---|---|
| **Opener IP** (3-bet from the blinds) | ~10% | ~40% | ~50% |
| **Opener OOP** (3-bet from a later non-blind seat) | ~22% | ~17% | ~61% |

**The pattern.** When you have position, **mostly call**, keep a small **polarized**
4-bet range, and defend about half your opens. When you are OOP, **4-bet about twice
as often**, call much less, and fold about 60%. A 4-bet either takes the pot or
lowers the SPR, which shrinks the IP player's edge. Calling OOP realizes equity
poorly, so OOP you call less and fold more.

**Why polarized 3-bets are easier to call.** A polarized range dominates fewer of
your hands, so more of them have the equity and playability to call. The HJ's
opening range has **42.9%** equity against the CO's 3-bet range but **44.8%**
against the BN's. The BN has a flatting range, so its 3-bets are more polar, and
the HJ calls more against the BN (20.8%) than against the CO (14.5%).

**By 3-bettor:**
- **vs HJ (LJ opened):** The HJ plays 3-bet-or-fold, so its range is **linear** and
  overlaps the LJ's range heavily. The LJ mostly **4-bets** to lower the SPR and
  make the HJ fold some equity.
- **vs CO:** The CO's 3-bet range is a little wider than the HJ's, so the opener
  4-bets a little wider and is happier to get JJ and TT in.
- **vs BN:** The BN's 3-bets are more polar, so the opener calls more and its 4-bets
  also become more polar. Middling hands like AQs, AJs and KQs get called more often.
- **vs SB:** You have position, so you 4-bet less. Only **AA, KK and AKs** really
  want to get all-in. Suited broadways mostly call. The 4-bet bluffs come from
  suited hands: some suited broadways and the next tier below them. QQ and JJ
  like seeing flops, so they 4-bet less often.
- **vs BB:** The BB's range is polar and you are IP, so you mainly **call**. The HJ
  can start slowplaying AA some of the time. Typical 4-bet bluffs are **A5s–A3s,
  AQo–ATo and some suited Kx**. Suited broadways, suited connectors and big pairs
  make great calls.
- **BN vs either blind:** The BN responds almost the same way to both. It folds
  slightly less against the SB because the pot is a bit bigger: the BB's whole 1bb
  is dead money instead of the SB's 0.5bb. The blinds can put in the last bet, so
  the BN keeps a **polarized 4-bet range of blocker hands with board coverage**.
  Facing a 5-bet, it gets in with **66+ and AK**. 66 is rarely in the 4-bet range,
  but it goes all-in when it is.

## Playing vs 3-bets: general heuristics

- **Ranges are sized to be defendable.** If you open a BN-sized range (~43%) from the
  LJ (~17%), you can't defend enough of it (~48%) against all the players behind.
  You end up folding far more than 52% and calling with marginal hands that play
  badly post-flop.
- **Your 4-bets, and the players still to act, are what stop opponents 3-betting you
  constantly.** Defend enough that the bottom of a villain's 3-bet range is
  indifferent between 3-betting and folding.
- **Early opens get 3-bet more often** (more players behind, and they 3-bet with
  stronger ranges). Wide ranges are harder to defend, so open tighter early.
- **Good calls vs 3-bets:** suited broadways, suited connectors and pocket pairs.
  **Usually folds:** offsuit broadways and weak Ax, which realize equity poorly and
  have bad reverse implied odds.
- **Smaller 3-bet sizes mean you must defend more.** Bigger sizes let you fold more.
- **Rake matters less in pots already inflated pre-flop.** When 3-betting or
  4-betting, decide on ranges and equities.
- **Facing a 5-bet,** the general getting-in range is **TT+ and AK**.
- **Facing an open and a 3-bet (cold),** **cold 4-bet or fold**. Splitting into cold
  calls and cold 4-bets leaks information. Cold calling also lets the other players
  continue with hands they would fold to a 4-bet. Cold 4-bet about **3%** against
  tight ranges (LJ and HJ) and about **6%** against wide ones (BN open with an SB
  3-bet). The core is QQ+ and AK (plus most AQs). Against wider ranges it adds
  JJ–TT, AJs, KQs, KJs and AQo, then ATs, KTs and 99.

**Exploiting someone who 3-bets too much: first predict how they handle a 4-bet.**

| Their response to a 4-bet | Your exploit |
|---|---|
| Fold most of the time | 4-bet a **polarized** range and bluff with blocker hands (A5s) |
| Call wide, 5-bet only premiums | 4-bet a **linear** range for immediate value and a strong post-flop range |
| 5-bet jam wide | 4-bet and call off lighter (e.g. AQ) |

## Playing vs open raises: 3-betting principles

### GTO 3-betting
- Against strong, sound opponents, stick close to equilibrium. Randomize if you can,
  and defend your 3-bets properly against 4-bets.
- **Stronger opener ranges call for stronger bluffs.** Your 3-bet bluffs against the
  LJ should be better hands than your bluffs against the BN.
- **If you have a flatting range** (mostly the BN, or IP), **3-bet polarized**: the
  best hands plus the next tier. That tier is hands that are poor calls but have
  equity, good blockers or board coverage. High-equity hands that don't want to
  face a 4-bet go into the flats.
- **If you have no flatting range** (HJ, CO and SB facing opens), **3-bet linear**:
  only your best hands, and fold the rest.
- Whenever you split calls from raises and the villain can re-raise all-in, make the
  re-raising range **polarized**, so the high-equity hands that hate raise/folding
  are in the calling range.

### Exploitative 3-betting
- Against a weak or over-wide opener, 3-bet more often. Watch the other active
  players, though: if they notice, they can **cold 4-bet wider** and punish you,
  even though the weak player never adjusts.
- Use **alpha/MDF** to check whether a 3-bet bluff profits immediately:

> α = risk ÷ (risk + reward); the bluff profits at once if villain continues with less than (1 − α) of his range

**Worked example.** The game is live $2/$5 with $500 stacks. A loose SB opens to
$15 with about 76% of hands (1,014 combos). The BB holds K♦2♠ and 3-bets to $45. It
risks $40 to win the $20 in the pot, so α = 40/60 = ⅔. The bluff is profitable at
once if the SB continues with fewer than ⅓ × 1,014 ≈ **338 combos**.
- This fishy SB continues with **350 combos** (34.5%), so 3-betting any two cards
  is not automatically profitable.
- The K♦ blocks AK, KK, K6s+ and KTo+, which cuts his continuing range to **324
  combos**. With this hand the 3-bet bluff now profits at once.

| Exploit type | When | How |
|---|---|---|
| **Polarized** 3-bet | Villain 4-bets or folds more than he calls | Add blocker hands to the 3-bets. High-equity hands you don't want to 3-bet/fold (AJo, A5s, KJs) can flat |
| **Linear** 3-bet | Villain calls 3-bets more than he 4-bets | 3-bet high-equity, playable hands that dominate his flatting range |

## Defending vs opens: specific ranges

**3-bet / call / fold (%)**, where "—" means no calling range.

| Defender | vs LJ | vs HJ | vs CO | vs BN | vs SB |
|---|---|---|---|---|---|
| HJ | 8.1 / — / 91.8 | | | | |
| CO | 8.6 / — / 91.4 | 9.9 / — / 90.1 | | | |
| BN | 7.3 / 6.9 / 85.8 | 8.8 / 6.5 / 84.6 | 11.7 / 5.4 / 82.3 | | |
| SB | 7.3 / — / 92.7 | 8.7 / — / 91.3 | 10.9 / — / 89.1 | 15 / — / 85 | |
| BB | 5.8 / 22.8 / 71.2 | 7.6 / 23.9 / 68.5 | 9.7 / 25.7 / 64.6 | 13.4 / 43.4 / 43.2 | 16.3 / 48.3 / 35.4 |

**HJ and CO: 3-bet or fold.** About **8%** is the most the HJ can 3-bet against the
LJ while staying unexploitable.
- The HJ puts a small weight on 88–22 for board coverage (sets on many textures),
  and so that opponents can't use blockers against a range made of only specific hands.
- The CO 3-bets only 0.5% more than the HJ against the LJ (one fewer player behind,
  but the LJ's range is still strong).
- Against the HJ's ~21% opens, the CO 3-bets wider (some A9s, QTs, JTs). A wider
  3-bet range has to call more 4-bets (KJs, some ATs/KTs) to stay unexploitable.

**BN: the only seat that is never OOP post-flop**, so it has a **flatting range**
and 3-bets **polarized**.
- Flats are hands with playability and board coverage.
- The flats are protected by **slowplaying** some QQ, JJ, TT, 99 and AKo. Hands that
  can stand a squeeze also flat (part of AQs, AJs, ATs, KQs, KJs, KTs, QJs).
- Against later openers, the BN **flats less**, because the blinds squeeze more
  often against wider openers, and **3-bets more** (11.7% vs CO). The extra 3-bets
  are blocker and high-card hands: QJo, ATo, more suited Ax and offsuit broadways.

**SB: 3-bet or fold against every open, despite the discount.** A flat leaves the BB
behind. The BB can squeeze and force the SB off its equity, or call and realize its
own equity. The SB then plays OOP against two players at a high SPR, and rake comes
on top of that. The 3-bet range widens as the opener gets later: 7.3% vs LJ up to
**15% vs BN**. Against the BN it adds ATo, some KTo/QJo, A7s, Q9s and suited
connectors such as T8s and 76s.

**BB: the most important defense to master.** Most pots are an open and a BB defend.
Folding every BB hand would cost **100bb/100**, and over-folding invites steals.
- **vs LJ (tight, ~29% defend):** Few speculative hands have enough equity and EqR to
  call. The LJ also defends well against 3-bets, so keep 3-bet bluffs modest.
  - **AQo–ATo make poor 3-bets.** They must fold to a 4-bet and play badly OOP in
    3-bet pots.
  - The **best 3-bets are suited broadways**, then suited Ax, Kx, connectors and gappers.
  - The calls are the best offsuit broadways, the remaining pairs, and suited hands
    (Axs, Kxs, connectors, gappers).
  - **A9o is folded but K2s is called.** Offsuit, disconnected hands realize equity
    badly, especially against tight ranges.
- **vs HJ / CO:** The BB defends a little wider against each later seat (3.9% more
  vs CO than vs HJ). Even so, **K8o and Q9o fold vs a CO open**: offsuit hands with
  low connectivity struggle OOP at deep stacks.
- **vs BN (~57% defend):** The BN's range is so wide that its strong hands are
  diluted. Its ability to **barrel and overbet** is weaker, so the BB calls far more:
  most suited hands, offsuit Ax, connectors and broadways. Its 3-bets (13.4%) are
  **linear and aggressive**: big pairs, strong broadways, A5s–A4s and suited
  connectors, with no junk bluffs.
- **vs SB (~65% defend):** The BB has position, so its 3-bet range is **polarized**.
  The top is hands happy to jam or call a 4-bet IP. The bluffs are blocker and
  board-coverage hands happy to fold to a 4-bet (**offsuit Ax, K4o+**). The flats are
  medium hands that realize well IP. Only the worst rake-punished hands fold.

## Facing a 4-bet after 3-betting

**5-bet jam / call / fold (%)**

| 3-bettor | vs LJ 4-bet | vs HJ | vs CO | vs BN | vs SB |
|---|---|---|---|---|---|
| HJ | 18.4 / 43.3 / 38.3 | | | | |
| CO | 17.5 / 45.1 / 37.4 | 16.1 / 48.2 / 35.8 | | | |
| BN | 19.4 / 40 / 40.6 | 18.4 / 41.6 / 40 | 17.1 / 45.2 / 37.3 | | |
| SB | 20.6 / 45.7 / 33.8 | 20 / 46.8 / 32.8 | 18.6 / 52.2 / 29.2 | 17.3 / 56 / 26.5 | |
| BB | 21.4 / 42.2 / 36.4 | 21 / 42.5 / 36.5 | 18.8 / 49.6 / 31.5 | 19.4 / 54.1 / 26.5 | 12.6 / 46.2 / 41.2 |

Patterns:
- **Later 4-bettors have wider, more polar 4-bet ranges, so you call more and fold
  less**: fold ~34–40% against the LJ but **26.5%** against the BN.
- **AA is slowplayed more and more:** roughly 40–55% of the time against early 4-bets, and
  **100%** for the SB against a BN 4-bet and for the BB against an SB 4-bet. In
  position, calling is the main defense even against the LJ.
- **Jams vs early 4-bets** are mainly KK, AKs and part of AA/AKo. QQ only
  occasionally gets in against the LJ (≈5–16%). The LJ's 4-bet range is strong
  enough to continue about 58% of the time against a jam.
- **Small suited connectors and middle pairs call better than AQo, Kxs or Qxs.** They
  **unblock villain's bluffs**, even though they have less raw equity.
- **Suited wheel Ax (A5s–A3s) call well.** They block AA/AK, unblock bluffs like KJs,
  KTs, K9s and J9s, and keep good playability.
- **Non-premium 5-bet bluffs (ATs, A5s) first appear against late-position
  4-bets.** EP/MP 4-bet ranges are too strong and too full of blockers. LP 4-bets
  against the blinds rely less on blockers, which makes jamming blocker hands
  better. ATs and A5s have the most equity of the bluff candidates against strong
  ranges.
- **Rare hands in a 4-bet chart:** a 100% call on a hand you 3-bet only 4% of the
  time (54s for the BN vs HJ) means you almost never hold it there.
- **BB vs SB 4-bet:** The SB's 4-bet range is very polar and the BB has position, so
  the BB jams rarely (12.6%). It always slowplays AA, usually slowplays KK and AKs,
  and sometimes QQ and JJ. It calls anything playable and folds the bottom of its
  polar 3-bet range.

## Takeaways for the table

1. Open raise-or-fold from every seat but the SB, at about **17 / 21 / 28 / 43%**
   from LJ to BN. Open tighter the more players are behind you, especially players
   with position.
2. SB first in: mix limps and 3x raises, with strong hands in both. SB facing an
   open: **3-bet or fold, never flat**.
3. Facing a 3-bet: **IP, mostly call** (fold ~50%). **OOP, 4-bet ~2× as often**
   (fold ~60%). Call with suited broadways, suited connectors and pairs. Fold offsuit
   broadways and weak Ax.
4. With a flatting range, 3-bet polarized. In a 3-bet-or-fold spot, 3-bet linear.
   Pick stronger bluffs against stronger ranges.
5. BB: defend more as the opener gets later (~29% vs LJ up to ~65% vs SB). Fold
   offsuit disconnected hands against early opens, even A9o.
6. Exploit with math: a 3-bet bluff needs folds of α = risk ÷ (risk + reward), and
   your blockers shrink villain's continuing range. Shape your 4-bets by how the
   villain handles them.
7. Facing an open and a 3-bet, cold 4-bet or fold. Facing a 5-bet, TT+ and AK is the
   general getting-in range.
