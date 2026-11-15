---
title: "Poker 12 — The Flop Continuation-bet (c-bet)"
summary: "Modern Poker Theory ch. 12: why IP must c-bet, c-bet frequency and size by board structure, texture, connectedness and top card, the frequency × size grid with six worked flops, OOP c-bets vs a cold-caller, 3-bet pots, and BB c-bet defence (fold, call, x/r)."
order: 112
audience: bravosierra99
---

# Poker 12 — The Flop Continuation-bet (c-bet)

*Study guide to Chapter 12 of* Modern Poker Theory *(Michael Acevedo). The chapter
is mostly solver charts. This guide keeps the numbers and patterns that matter at
the table. Unless noted, the data are GTO solves at 20–40bb with MTT ranges and
12.5% antes.*

Reminders from ch. 10–11: the equity buckets are **Strong** ≥ 75%, **Good** 50–75%,
**Weak** 33–50% and **Trash** < 33%. The flop families use A = ace, H = K–T,
M = 9–6 and L = 5–2.

## Why IP must c-bet

- If IP (UTG or BN vs the BB) **always checks back** the flop, it loses **~26bb/100**. The BB can drop donk-betting almost for free (ch. 11), but IP can't drop c-betting.
- The BB seldom donks, and its checking range stays balanced, so IP's strategy is the same whether the BB donks like a solver or never donks.
- **Non-GTO donkers** usually donk all-strong or all-weak hands. If he donks only strong hands, his checks are weak: overfold your bottom range to the donk and c-bet very often when he checks. If he donks only weak hands, his checks are strong: bluff-raise the donks, slowplay strong hands that need no protection, and check back a bit more to dodge his x/r.

## The overall IP picture vs the BB

| IP | Equity | EV (share of pot) | EqR | 2/3 | 1/2 | 1/3 | Min | Check |
|---|---|---|---|---|---|---|---|---|
| UTG (~15% range) | 63% | 73% | 115% | 17% | 19% | 30% | 25% | **9%** |
| BN (~44% range) | 59% | 67% | 115% | 11% | 9% | 19% | 43% | **18%** |

- **More strong hands than villain → bet more often and bigger.** Strong hands protect everything else you bet. UTG's tighter range c-bets more and larger, while the BN relies on min-bets.
- **Stack depth:** big bets and overbets matter more as stacks get deeper. Shallow, you don't need them to get the stacks in, and committing a lot of your stack at low SPR is pointless. **The all-in is the exception:** it's used *more* when shallow, because the risk/reward is better and jamming guarantees you realize your equity.

| Bucket | Default | Exceptions and reasons |
|---|---|---|
| **Strong** | Bet to build the pot | Some **trap** by checking, when they block villain's continuing range or are so far ahead that a free card is harmless. Trapping also protects your checking range |
| **Good** | Bet for value and protection | **Pot control:** check back when the BB is polarized to hands that beat you or have almost no equity |
| **Weak** | Check vs a strong range that can x/r you off your equity | **Semi-bluff** when villain is weak and can't x/r much |
| **Trash** | Bet *more often* than weak hands (a **pure bluff**) | It rarely improves when checked and lives on fold equity. Bet/folding it to a x/r costs little |

## Board → c-bet frequency and size (IP vs the BB)

| Structure | Share of flops | IP EV | EqR | C-bet pattern |
|---|---|---|---|---|
| **Trips** | 0.24% | **81%** | 126% | Never checked; mostly 1/3 pot; lower trips use bigger sizes more |
| **Paired** | 16.94% | 68% | 112% | **Min-bet 70%**, 1/3 15%, check 14%; 2/3 never |
| **Unpaired** | 82.82% | 69% | 116% | Mixed: 2/3 15%, 1/2 14%, 1/3 23%, min 32%, check 16% |

**Why min-bet paired boards?** The BB is **polarized**. Its trips give it counterplay, and
its many trash and weak hands fold to *any* size. A tiny bet makes those hands show
their weakness, and IP loses the minimum when it bet/folds the bottom of its range.
**General rule: if IP's range is depolarized (mostly good-not-great, little trash), bet
small. If IP is polarized (more strong, weak and trash), bet bigger.** Boards paired
with a **low or middle card favour the BB** and are checked most.

| Texture | Share of flops | IP EV | Check | Sizes |
|---|---|---|---|---|
| **Monotone** | 5% | **66% (lowest)** | **12% (most c-bet)** | 1/3 41%, min 36%; big sizes rare |
| Two-tone | 47% | 69% | 17% | Spread across all four sizes |
| Rainbow | 31% | 70% | 17% | Most big bets |

- **Monotone:** IP's strong hands lose value, and the BB's trash becomes flushes or picks up flush draws. Like a paired board, **the BB is polarized and IP depolarized**, so **bet small and often**. Small bets still fold the BB's hopeless hands without overcommitting IP's good-not-great hands. **Betting big on monotone is a classic mistake.** It folds the weak hands you want to keep in and isolates you against hands that beat you or have big equity. Using only 1/3 pot or min-bets loses almost nothing.
- **Two-tone:** IP holds ~24% strong hands to the BB's 5%, so big sizes appear far more than on monotone.
- **Rainbow:** IP's edge is biggest. Strong hands stay strong, with no flush-draw swings, so IP can triple-barrel and get the stacks in by the river.

**Connectedness.** The BB has more offsuit connectors than IP, so **each extra possible
straight helps the BB** and lowers the c-bet rate:

| Possible flopped straights | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| IP checks (all flops) | 13% | 21% | 37% | 41% |

Among zero-straight flops, those allowing **three OESDs** are c-bet least, and with the
biggest sizes, because IP's strong hands need protection. The book's prose also gives
check rates of 10 / 17 / 28 / 31% for 0–3 straights. These seem to describe monotone
flops only. On those boards deeper stacks check more too.

| Top card | 2 (only 222) | **A** | 3 | K | Q, T | Middle/low |
|---|---|---|---|---|---|---|
| C-bet | 100% | **96%** | 93% | 88% | 85% | Lowest; **6-high is the floor at 62%** |

**Families:**
- The least c-bet unpaired families are **LLL, MMM, MML, MLL and HMM**: low and connected.
- On monotone boards every family is checked rarely (≈3% to 32%), almost always with 1/3 pot or min-bets.
- On two-tone boards, ace-high families are bet ~97–99%, and **big**. Low connected families are checked heavily (LLL 46%, MMM 43%).

## The c-bet grid: frequency × size

Classify each flop by GTO c-bet frequency, either **high (80%+)**, **mid (60–80%)** or
**low (< 60%)**. Then classify it by preferred size, either **big (1/2–2/3 pot)** or
**small (min or 1/3 pot)**.

**The BB's buckets set the size:**
- On big-size flops the BB has only **4–5% strong** and **19–36% good** hands. That's a depolarized range with many hands that can call, so **size up**.
- On small-size flops the BB has **7–9% strong** (about twice as many) and 20–27% good. More of its hands can raise, so **size down**.
- IP c-bets more often as the BB's trash share rises, and less often as IP's own range becomes depolarized.

**What the frequency band tells you:**
- **High:** c-bet 100% for little or no EV loss. IP's range advantage leaves the BB nothing to attack with.
- **Mid:** the ranges are closer, and a 100% c-bet costs EV even vs weak players. **Split your range:** check back good-not-great hands that want a small pot and a free turn, and bet a **polarized** range, which is why **bigger sizes** take over.
- **Low:** mostly checks.

IP's best flops are **high frequency with a big size**. The BB's best flops are **low
frequency with a small size**, where equities run close.

**The "information bet" myth.** Some players bet hands that should check, to keep the
"betting lead" or avoid tricky turns. They get raised off their equity, or they call the
x/r and fold the turn. Play for the highest EV, not to win every pot. Sometimes the best
play is to give up.

## Six worked flops (40bb, IP vs the BB)

| | Big size | Small size |
|---|---|---|
| **High %** | UTG on **A♥Q♦3♠** | UTG on **Q♥J♥T♥** |
| **Mid %** | UTG on **9♥8♥4♦** | BN on **J♠6♥6♦** (c-bets 72%) |
| **Low %** | BN on **8♥6♦2♠** | BN on **5♥5♦4♥** |

**A♥Q♦3♠ (high %, big).**
- UTG holds AA, QQ and AK, while the BB would have 3-bet those, so **the BB lacks the nuts**. UTG bets big over several streets and turns 72% equity into **85% of the pot**.
- **C-betting 100% at 2/3 pot keeps all the EV.** C-betting 100% at 1/3 pot loses ~1% of the pot.
- **Vs a rare min x/r (~5%),** UTG folds ~30% (small pairs, K-high without a gutshot, air), 3-bets ~18% (AK, AJ, sets, plus a few bluffs) and calls 52% (any top or middle pair, gutshots).

**Q♥J♥T♥ (high %, small).**
- UTG has the range edge, but the BB is polarized: it has many hands that fold to a big bet and many strong hands happy to call one. A big bet lets the BB fold correctly and continue only with its strong hands. **A min-bet keeps its dominated weak hands in.**
- **Min-betting 100% loses nothing.** One size keeps almost all the EV, so you don't need the solver's tiny mixes.
- **Vs a x/r** (mostly made hands and draws), UTG almost **never 3-bets**. It calls ~65% (two pair+, pair plus straight draw, any flush draw) and folds ~35%.

**9♥8♥4♦ (mid %, big).**
- A single 2/3-pot size keeps nearly all of IP's EV (69% of the pot).
- **A 100% c-bet costs 4.25% of the pot (−24bb/100)**, because the BB's x/r rate jumps from **~4% to ~48%**.
- AA and top and middle set check ~8%. Middle pairs and OESDs mostly check, while flush draws and combo draws mostly bet. Top pair checks 24%, and the better the kicker, the more it bets. The lone trash hand, 65s, bets ~95%.
- **Vs a min x/r,** UTG folds ~32% (overcards without a BDFD), 3-bets ~21%, mostly as jams (overpairs, TPTK, the nut flush draw), and calls ~47%.

**J♠6♥6♦ (mid %, small).**
- The BB is polarized and fairly strong, with **8.9% trip sixes to the BN's 5%**, so a big size is out. But 52% of its range is trash that can't face even a min-bet, so the BN still c-bets 72%.
- Quads and JJ block the BB's continuing hands, so they trap some of the time. Overpairs check more when they block the BB's backdoor flush draws: **K♣K♦ c-bets more than K♠K♥**, which blocks both the spade and heart BDFDs.
- TT–22 bet half the time. Suited A-high bets **linearly** (AKs/AQs 100%, A5s–A2s 34%), because better A-high has more equity vs a x/r, blocks top pair and gets called by worse A-high. Air bets 75%.
- **Vs a x/r** (~27%, polarized), the BN folds ~35% (air, A/K-high with one overcard), min-3-bets 11% (A6, K6, backdoor bluffs) and calls 54%.

**8♥6♦2♠ (low %, big).**
- The BB has few strong hands, which favours a big size. But the BN has many good and weak hands that want a free turn, so it makes a **polarized big bet at a low frequency**.
- Keep strong hands for brick runouts: with one size, **just check top set**. **Leak:** betting every strong and good hand leaves a capped checking range that gets attacked later.
- Small and middle pairs mostly check. 77 bets half, for value from 6x.
- Hands that can't call a x/r bet **reverse-linearly**, so **K9o bets more than KQo**. Strong Kx does fine on many turns, while weak Kx is a better bet/fold. OESDs mostly check, while gutshots and Q-high with two overcards mostly bet. Weak Q/J/T-high usually bets, but some must check, or the c-bet range gets too weak.
- **Vs a rare x/r (~8%),** the BN folds 43% (air and overcards without a BDFD always), calls 34% and **jams 23%** (QQ–99, TPGK+, two overcards with a BDFD).

**5♥5♦4♥ (low %, small).**
- The BN has no real range advantage and is mostly good hands (depolarized), so many hands check.
- Strong hands are slowplayed ~28%: quads mostly check, while trips almost always bet. **Overpairs bet reverse-linearly: TT 76%, JJ 64%, QQ 50%, KK 40%, AA 22%.** Big pairs need less protection and make great bluff-catchers after checking.
- 66–99 almost always bet. OESDs mostly bet and gutshots mostly check. Air bets ~64%, mostly as a bet/fold.
- **It's c-bet less than J66** because the BB's would-be trash has flush draws, OESDs or gutshots here, so **its range is less polarized**.
- **Vs a x/r,** the BN 3-bets 19%, calls 56% and folds 25%.

**On mixing:** don't memorize these splits. Against humans one action is usually clearly
best. Mixing is a defence against strong players, and exact frequencies are neither
possible nor necessary.

## Way ahead or way behind

Sometimes IP checks a lot even though betting its range would profit. This happens
when the BB is **polarized to monsters and air**. Example: **A♠T♥T♦, UTG vs BB,
30bb.** IP is 57% strong, 37% good, 5% weak and 1% trash. The BB is 7%, 12%, 0%
and 81%.

- **Check back** many good hands for pot control, plus a big chunk of strong hands as traps.
- **Bet** all trash and most weak hands, balanced with the remaining strong and some good hands. The trash wins the pot now, and the checked range bluff-catches later.

**Facing a flop x/r:**
- If villain x/rs less than equilibrium, he's missing bluffs, so **overfold**. Against the right villain, even some strong hands can fold.
- If his x/r range leans to draws, **3-bet** good and strong hands that want protection.
- If he's polarized to nuts or bluffs, **bluff-catch** and don't raise medium hands.

## IP c-bet guidelines

- A rough feel for each player's buckets is enough. If villain has lots of trash, c-bet often. If he has few strong hands compared to you, **size up**.
- If you expect folds or raises, **bet small and often**. If you expect calls, size up.
- **Bet/folding a high-equity hand on the flop is a disaster.** If you can't range-bet without facing frequent x/rs, split your range.
- Put some strong hands in your checking range, especially ones that block villain's continuing range, so his stabs can't run you over.
- The *types* of hands the solver checks barely change from flop to flop. Only how often it checks them changes.
- Unsure about a hand? **Ask what happens if you're raised.** If it hates a x/r and one is likely, check. Unsure about the whole range? Default to **1/3 pot** in most short- and mid-stack spots.
- If the BB never donks on good donking flops, c-bet **less** than equilibrium. His checking range is stronger, so he'll x/r more.
- If a hand can get three streets of value, start by betting the flop. Hands with backdoor equity but no showdown value make good semi-bluffs.
- **Multiway:** blockers matter more than raw strength. Play passively and bet draws only when they're to the nuts.
- Don't try to bluff recreational players off top pair. A simple plan beats no plan.

## OOP c-betting (the raiser vs a BN cold-caller)

**Why it's different:**
- **Closer ranges.** Against the blinds IP faces a 50–70% range, but a cold-caller holds only ~4–20%. The closer the ranges, the less incentive to bet.
- **No free turn.** An OOP check doesn't guarantee a turn card, because IP can bet. So the OOP **checking range must be stronger** and able to withstand aggression right away.

| Hero (OOP) | Stack | Hero EQ | Hero EV | Hero EqR | Hero checks |
|---|---|---|---|---|---|
| UTG | 40bb | 55.4% | 54.4% | 98% | 32% |
| UTG | 20bb | 53.8% | 51.3% | 95% | 44% |
| CO | 40bb | 50.1% | 46.2% | 92% | **76%** |
| CO | 20bb | 49.0% | 42.8% | 87% | **82%** |

- The OOP raiser **under-realizes in every setup**. The BN paid for that edge pre-flop by risking a squeeze and multiway pots.
- **Two sizes are enough:** a big bet (3/4 pot at 40bb, 2/3 at 20bb) plus a min-bet or 1/3 pot.
- **The CO can check 100% at almost no cost**, much as the BB can skip donking. It's also a **population exploit**: most players auto-stab when checked to (GTO stabs about half the time), so a check-raise-heavy plan profits. It also cuts the SPR and the positional disadvantage.
- **Leak:** c-betting weak and trash hands OOP, then check-folding the turn. An observant opponent floats and bets every turn.
- UTG checks its **strong hands 19%** of the time, more than 3× as often as when IP, so its checks can x/r.

**The trash pattern reverses.** IP c-bets trash *more* than good and weak hands. OOP
c-bets **good and weak hands more than trash**. OOP acts first on the turn, so a flop
bet full of air would leave a weak, exploitable turn range. Instead it checks its trash
and mostly folds it, and its stronger checking range sees more x/x flops.

| Texture (UTG vs BN, 40bb) | Check | Why |
|---|---|---|
| Trips | ~2% | UTG has the overpairs, and the BN's suited connectors are trash |
| Paired rainbow | 15% | **Big sizes, especially on low pairs.** The BN's tight range rarely has trips, so IP is capped and OOP isn't (the reverse of IP vs the BB) |
| Rainbow | 23% | OOP's polarization advantage means bigger sizes |
| Two-tone | 35% | Flush draws cut the equity and EqR of OOP's strong hands |
| Monotone | **50%** | Small bets; the texture helps IP a lot |

On Axx and high flops OOP has the range advantage and c-bets most. Middle and low
flops are even, so OOP plays passively. The BN's flats are full of suited connectors and
small and middle pairs, so **connected, dynamic boards favour the caller**, and **static,
disconnected boards favour the raiser**.

## C-betting in 3-bet pots (40bb, 12.5% ante)

The ranges are narrower. The 3-bettor's flop range is more **polarized** and the caller's
more **condensed**. The **SPR is 1.7–2**, and the sizes tested were all-in, 1/2, 1/3 and
1/4 pot.

| 3-bettor | Avg equity | Avg EV | Avg EqR | Checks |
|---|---|---|---|---|
| IP (BN, CO, UTG+1) | 55.9% | 62.7% | 112% | ~38% |
| OOP (SB, BB) | 54.5% | 54.6% | 100% | SB 21%, BB 33% |

The 3-bettor holds about **2:1 the strong hands** and **1.5:1 the good hands**, and
**about a third of the caller's range is trash**, so **small sizes** are preferred,
especially IP.

**IP 3-bettor:**
- The strategy simplifies to **1/4 pot only**, with ~38% checked back.
- **Population leak:** people c-bet far too much, because they always bet their air. It works only because players don't x/r 3-bet pots enough, so **the counter from OOP is to x/r more**.
- Many strong hands check back, especially ones that block villain's continuing range. **QQ on Q82r checks 68%.**
- **Texture:** trips and paired rainbow boards are bet most. **Two-tone (40% checked) and monotone (47%) are checked most.** On two-tone boards the caller can x/r with many flush draws and push you off, so checking lets your good and weak hands realize equity.
- **Top card:** low boards and Kxx are bet most. **Qxx and Jxx** are checked a lot, because they hit the caller and demote IP's hands to second or third pair.
- **Axx is c-bet only ~53%**, though most players bet it ~100%. The board is static and polarizes the caller into strong hands, medium hands that can't call twice, and trash that won't improve much. At this SPR the money goes in over two streets anyway. Checking gains information when OOP acts on the turn, protects the check-back range with strong hands, and lets medium hands realize equity.

**OOP 3-bettor:**
- OOP realizes less than IP, because its checks must withstand aggression. It sometimes bets **bigger**, to deny IP a cheap price and to lower the SPR.
- The **SB's 3-bet range is a bit stronger** than the BB's, so the SB c-bets more.
- OOP c-bets more often than IP on almost every texture, with bigger sizes. **Monotone is the exception** (~44% checked, close to IP).
- **Axx: 77% OOP vs 53% IP**, with similar buckets. OOP doesn't want to give IP a free turn and then act first, so it bets.

## C-bet defence (BB vs IP, 40bb single-raised pot)

### Don't defend by MDF
MDF (pot ÷ (pot + bet)) ignores equity and range shape.

| C-bet | MDF | Pot odds (equity needed to call) |
|---|---|---|
| 1/4 pot | 80% | 16.7% |
| 1/3 pot | 75% | 20% |
| 1/2 pot | 66.7% | 25% |
| 2/3 pot | 60% | 28.6% |

**A♥Q♦3♠, BB vs UTG, 1/3-pot c-bet.**
- MDF says defend 75%, but the BB is 70% trash. That trash averages **16% equity** against the **20%** the price needs, so calling with it is −EV, and raising is worse.
- **GTO folds 58% and defends 42%.** UTG profits betting any two cards, so just fold hands like 96s with a BDFD, weak K-high or a small pair.
- The pre-flop call was still right, because other flops pay you back. Folding is 0 EV, which often makes it the best option.

**Read the range that takes the line.** A min-bet and a pot-sized bet come from
different ranges. Against a player who bets only strong hands and checks medium ones,
**overfold**.

### Averages and sizing
IP can c-bet 1/4, 1/3, 1/2 or 2/3 pot. The BB can x/r big (50% pot) or small (25%, a
min-raise vs 2/3), call or fold.

| Buckets | Strong | Good | Weak | Trash | BB's response to a c-bet |
|---|---|---|---|---|---|
| BB vs UTG | 5% | 21% | 24% | **50%** | fold 46%, call 38%, x/r 15% |
| BB vs BN | 8% | 26% | 26% | **40%** | fold 41%, call 44%, x/r 15% |

**The BB's folds are almost all trash, so its trash share sets its fold rate.**

| BB vs UTG, by c-bet size | x/r | Call | Fold |
|---|---|---|---|
| Min-bet | 20% (mostly big) | 47% | 33% |
| 1/3 pot | 16% | 39% | 45% |
| 1/2 pot | 13% | 35% | 51% |
| 2/3 pot | ~11% (mostly small) | 31% | 57% |

- **x/r big vs small c-bets, and small vs big ones.** Against a min-bet, a small x/r never prices out IP's weakest hands, because bet/calling stays cheap, so the BB raises bigger to keep them indifferent. Against a big c-bet a min-raise is enough and avoids overcommitting. **All-in x/rs are the exception:** their risk:reward improves when IP bets big.
- **Smaller c-bets get x/r more**, because a small-bet range is more depolarized.

**By bucket:**
- **Strong:** mostly x/r, but many x/c to raise later, which protects the calling range.
- **Good:** mostly call. Some x/r, namely those that need protection and don't block IP's continuing range (top pair on middle boards, bottom two pair on high boards, combo draws).
- **Weak:** mostly call. About a third fold and ~15% x/r.
- **Trash:** mostly fold, with a few x/r bluffs.

### Defence guidelines
- Don't split your range early unless you have enough strong hands for both a x/r and a x/c range.
- **Flop x/r ranges are polarized:** hands happy to get it in vs a 3-bet, plus raise/folds. Don't x/r a hand too good to fold but not good enough to get in.
- With lots of equity but little showdown value, or a hand that will lose value later, play aggressively now.
- **Deeper stacks need stronger hands to x/r.**
- **Blockers:** a value x/r should *not* block villain's continuing range. On 9♥8♥4♥, **44 makes a better x/r than 99**. A bluff x/r *should* block his continuing range, not his bluffs.
- Your x/r range isn't simply your strongest hands. It's the hands that like a lower SPR and have the right blockers.
- Bottom pair is hard to x/c over several streets, so put some in the x/r range.
- Don't give up A-high and K-high too fast, especially against small bets. But a range full of trash should fold a lot, whatever the bet size or MDF.
- Flush draws and OESDs aren't the nuts. Keep some in the x/c range for board coverage.

## Defence examples (BB, 40bb)

**vs UTG 2/3 pot on A♥Q♦3♠** (the BB folds 68%):
- Top pair never folds.
- **Pocket pairs between the Q and the 3, even JJ and TT, always fold**, because their two outs aren't clean.
- **Low kickers beat high ones.** Q8s–Q2s always call, while QJ–Q9 without a BDFD fold about half. **K3s always folds, while 53s x/rs 43%.** A low kicker is usually live, while a K kicker is often dominated. Bottom pair works as a semi-bluff, not a call-down hand.
- K-high and other air (48% of the range) always fold.

**vs UTG min-bet on Q♥J♥T♥:**
- **Slowplay the straight flush.** UTG rarely has a flush, and when it does, the money goes in anyway.
- Low flushes x/r ~88%, while the A-high and K-high flushes mostly call.
- **Top pair has only ~44% equity, so it isn't a strong hand here.**
- OESDs continue only when drawing to the nut straight.

**vs UTG 2/3 pot on 9♥8♥4♦** (the BB x/rs only ~4%, or ~15% vs a 1/3-pot bet):
- **Sets x/r only ~12%**, and 99 and 88 almost always call. "Sets must x/r because of the draws" is a myth, since draws are only ~10.5% of UTG's range. With so few strong combos, keeping its information edge matters more, and the BB **donks the turn** on good runouts instead.
- **Overpairs JJ–TT are the most x/r'd hands**, good but vulnerable.
- Two pair: **98 and 84 x/r more than 94**. Top two is the most nutted, and bottom two needs protection and doesn't block top pair. Top-and-bottom (94) blocks IP's top pairs.
- **OESDs always call.** They do fine vs the c-bet range but are dominated by IP's 3-bets.

**vs BN min-bet on J♠6♥6♦** (the BB x/rs ~27%, mostly big):
- Full houses rarely x/r: J6 needs no protection and blocks top pair.
- **Trips x/r ~80%, reverse-linearly.** Trips with a high kicker prefer to call, because they block IP's overcards and overpairs.
- Air with backdoor draws supplies the x/r bluffs.

## Takeaways for the table

1. Read the BB's buckets. If it has lots of trash, bet often. If it has few strong hands, bet big. If it's polarized (paired or monotone boards), bet small.
2. On mid-frequency flops, **split your range**. Check medium hands that want a free turn and bet a polarized range big. Never bet a hand you'd fold to a x/r "for information".
3. Possible straights and low or middle cards cut the c-bet rate, because the BB's connectors hit those boards.
4. OOP vs a cold-caller, bet far less, check some strong hands, and **check trash rather than bluffing it**.
5. In 3-bet pots c-bet small (1/4 pot) but check back often, including Axx when IP.
6. Defend by equity, not MDF. Fold trash freely, x/r big vs small bets and small vs big ones, and pick x/rs by SPR and blockers.
