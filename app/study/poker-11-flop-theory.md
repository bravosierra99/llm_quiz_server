---
title: "Poker 11 — The Theory of Flop Play"
summary: "Modern Poker Theory ch. 11: suit isomorphism, dynamic vs static boards, the flop classification scheme (structure, texture, rank, straights, families), flop subsets, when the BB should donk bet, what donking is worth, and the value of position."
order: 111
audience: bravosierra99
---

# Poker 11 — The Theory of Flop Play

*Study guide to Chapter 11 of* Modern Poker Theory *(Michael Acevedo). Read the
chapter for the charts; this guide is the skeleton you should be able to rebuild
from memory.*

**Where the numbers come from:** heads-up **single-raised pots (SRP), BB vs an
IP opener** (BN = widest range, UTG = tightest), at **20, 30 and 40bb**, with all
1,755 flops solved. These are MTT depths, so read the numbers as principles, not
100bb cash frequencies. EV is a **% of the pot**.

## Suit isomorphism

Things are **isomorphic** if a given set of properties can't tell them apart. No
suit is better than another, so 1,326 combos fold into 169 hands. In the same way,
the **22,100** flops reduce to **1,755 strategically unique flops**. A♠K♠Q♠ and
A♥K♥Q♥ give every range the same flushes, draws and sets, so J♠T♠ on the first plays
exactly like J♥T♥ on the second. That leaves fewer flops to learn and fewer for a
solver to compute.

## Dynamic vs static boards

**Volatility** (Tipton's term) is how likely later cards are to change which hands
are best. It depends on the flop **together with the ranges**.

- **Dynamic:** low, connected, with draws. Equities swing. On 8♥7♥3♦ (BB vs EP), any heart makes a flush, a 5, 6, 9, T or J can make a straight, and any overcard can out-pair top pair.
- **Static:** high, disconnected, rainbow. Good hands stay good and bad hands stay bad. On K♠7♦2♥ most runouts change little.

## The flop classification scheme

Even 1,755 flops per spot are too many to study one at a time. Flops that share
features tend to be played the same way, so **classify** them, study
representatives, and keep the whole game in view. There are five dimensions.

### 1. Structure

| Structure | Definition | Examples |
|---|---|---|
| **Trips** | All three cards the same rank | 7♥7♠7♦ |
| **Paired** | Two cards of one rank, either paired rainbow or paired two-tone | K♥K♣5♠, Q♦8♦8♣ |
| **Unpaired** | Three different ranks | Q♥7♦4♣, A♥K♥Q♠ |

### 2. Texture

| Texture | Definition | Examples |
|---|---|---|
| **Monotone** | All one suit | A♥K♥T♥ |
| **Two-tone** | Two cards share a suit. There are three subtypes: **high-mid** (top two suited), **mid-low** (bottom two suited) and **high-low** (top and bottom suited) | A♥K♥Q♠ (high-mid), J♥6♠5♠ (mid-low), A♥9♠2♥ (high-low) |
| **Rainbow** | Three different suits | Q♥9♠7♦ |

**How common each type is:**

| Category | Suit variants | Distinct flops | All flops | Share |
|---|---|---|---|---|
| Monotone | 4 | 286 | 1,144 | 5.18% |
| Two-tone | 12 | 858 | 10,296 | **46.59%** |
| Rainbow (unpaired) | 24 | 286 | 6,864 | 31.06% |
| Paired rainbow | 12 | 156 | 1,872 | 8.47% |
| Paired two-tone | 12 | 156 | 1,872 | 8.47% |
| Trips | 4 | 13 | 52 | 0.24% |
| **Total** | | **1,755** | **22,100** | 100% |

Almost half of all flops are two-tone, so a flush draw is possible on them. About
5% are monotone, about 17% are paired, and trips come about once in 400 flops.

### 3. Rank (the highest card)

"Kxx" means a king plus two cards no higher than a king. The higher the top card,
the more flops there are with it.

| Top card | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 222 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Flops | 4,804 | 4,052 | 3,364 | 2,740 | 2,180 | 1,684 | 1,252 | 884 | 580 | 340 | 164 | 52 | 4 |
| Share | 21.74% | 18.33% | 15.22% | 12.40% | 9.86% | 7.62% | 5.67% | 4.00% | 2.62% | 1.54% | 0.74% | 0.24% | 0.02% |

- Ace-high flops are the most common, at about **1 in 5**.
- About **85% of flops are 9-high or higher**, and only about **15% are 8-high or lower**. 7-high and 6-high flops, where the BB donks most, make up only about 6.6% of all flops together.

### 4. Number of possible flopped straights

| Straights | Board shape | Flops | Share |
|---|---|---|---|
| **3** | Three consecutive ranks, from QJT down to 543. JT9 allows KQ, Q8 and 87 | 512 | 2% |
| **2** | One gap, e.g. 875 (allows 96 and 64), plus KQJ and 432 | 1,280 | 6% |
| **1** | Two gaps, e.g. KT9 (allows only QJ) | 2,304 | 10% |
| **0** | Spread wider (e.g. AQ7), or paired or trips | 18,004 | 81% |

The edges of the deck cost straights. KQJ allows only AT and T9, and 432 allows only
A5 and 65. *(My addition, which the book's counts confirm: every ace-high board
allows at most one straight. AKQ allows only JT, and wheel boards such as A53 allow
only one.)* Zero-straight flops can be split further by how many OESDs they allow,
but the book only counts straights.

### 5. Families

Group the ranks: **H** = K Q J T, **M** = 9 8 7 6, **L** = 5 4 3 2, **A** = ace.
Then every flop belongs to a **family** such as AHL, HML or MLL. Flops in a family
often play almost alike. A54, A53, A52, A43, A42 and A32 are all "an ace with two
low cards". **Subfamilies** use the actual top card, e.g. 8ML or 7LL, or the actual
pair, e.g. 66L or 99A.

| Family | Distinct | All flops | | Family | Distinct | All flops |
|---|---|---|---|---|---|---|
| AAA | 1 | 4 | | HHH | 48 | 560 |
| AAH | 8 | 96 | | HHM | 152 | 1,920 |
| AAM | 8 | 96 | | HHL | 152 | 1,920 |
| AAL | 8 | 96 | | HMM | 152 | 1,920 |
| AHH | 38 | 480 | | **HML** | **320** | **4,096** |
| AHM | 80 | 1,024 | | HLL | 152 | 1,920 |
| AHL | 80 | 1,024 | | MMM | 48 | 560 |
| AMM | 38 | 480 | | MML | 152 | 1,920 |
| AML | 80 | 1,024 | | MLL | 152 | 1,920 |
| ALL | 38 | 480 | | LLL | 48 | 560 |

HML (one high, one mid and one low card) is the largest family, at about 18.5% of
all flops.

### Flop subsets

- **Coverage method:** pick the smallest set of flops that includes every card, suit pattern, pair and gap shape. This gave 103 flops, which isn't fully representative. The author's own hand-picked set couldn't go below 356.
- **Metric method:** pick the N flops whose equities and EVs best match the full game. More flops give more accuracy, **especially at high SPR**, where rare coolers create huge pots.
- These subsets were tuned for pre-flop accuracy, not post-flop strategy. That is why this chapter's data comes from solving all 1,755 flops.

## The flop donk bet (BB vs an IP opener)

**The spot:** someone opens from IP, it folds to the BB, and the BB calls. This is
the **most common situation in poker**, so it's worth getting right. A **donk bet**
is the BB leading into the pre-flop raiser.

**The folk rule:** the raiser "has the betting lead", so the BB checks. **Game
theory has no betting lead.** A bet is justified by **range composition,
informational advantage and SPR**, used to realize your equity or deny your
opponent's.

**The headline results** (BB vs BN and UTG, 20/30/40bb, 1/4- and 2/3-pot sizes):

| | Bet | Check | Equity | EV | EqR |
|---|---|---|---|---|---|
| BB, all flops | **2%** | 98% | 40% | 31% | 77% |
| IP after a check, all flops | **84%** | 16% | 60% | 69% | 115% |
| BB, 654r | **67%** | 33% | 51% | 54% | 107% |
| IP, 654r | 46% | 54% | 49% | 46% | 95% |
| BB, A76r | **0.3%** | 99.7% | 38% | 24% | 63% |
| IP, A76r | 99% | 1% | 62% | 76% | 123% |

The folk rule is right on average. Donking is rare and c-betting is common. But on a
few flops the solver leads a lot: 654r is the most-donked flop and A76r is among
the least.

### Why: what decides the EV of a bet

> EV(bet) = EV(villain folds) × %fold + EV(called) × %call + EV(raised) × %raise

A solver bets a hand only when betting earns at least as much as checking. The
stronger the villain's range, the less he folds, the more he raises and the less
equity you have when called, so betting into a strong range rarely pays.

### Range composition matters more than raw equity

Raw equity favours IP on A76r (62/38) and slightly favours the BB on 654r (51/49).
The **equity buckets** show the bigger picture. (Strong, good, weak and trash are
defined in Chapter 10.)

| Bucket | IP on 654r | BB on 654r | IP on A76r | BB on A76r |
|---|---|---|---|---|
| Strong | 4% | 7% | **31%** | 8% |
| Good | 35% | 40% | 26% | 17% |
| Weak | **51%** | 35% | 38% | 26% |
| Trash | 10% | 18% | 5% | **49%** |

- On A76r, any ace in IP's range is top pair with about **85%** equity against the BB. On 654r a top pair has only about 65%, and IP's ace-x hands as a group (mostly ace-high on this board) average about **49%**, which makes them **weak hands**.
- **On 654r**, IP's weak hands fear a check-raise, so IP checks back more to take free cards. The BB's lead makes those hands fold or pay (**equity denial**), and lets the BB realize its own equity with a balanced lead. IP has few strong hands to raise for value, so it can't support many bluff-raises either. Against a 1/4-pot lead, IP raises only **20%** on 654r, compared with **53%** on A76r.
- **On A76r**, IP can c-bet its whole range without fear. A lead gets raised so often that the denial runs the other way, against the BB. The BB also doesn't need to lead for value, because IP bets anyway.

### Splitting your range when you're weak: A76r, BN vs BB, 30bb

| BB strategy | Donk % | Total EV | EqR | EV after checking | EV after leading |
|---|---|---|---|---|---|
| GTO (check everything) | 0% | **25.0** | 63% | 25.0 | – |
| Lead only top pair or better | 10% | 12.8 | 32% | **5.6** | 80.5 |
| Lead only weak hands | 44% | 11.7 | 29% | 40.6 | **−25.0** |
| Lead everything | 100% | 12.8 | 32% | – | 12.8 |

- **Leading only strong hands:** the leads are very profitable but rare. The 90% of hands that check now hold nothing strong, so IP attacks them and their EV falls from 25 to 5.6. Total ≈ 0.1 × 80.5 + 0.9 × 5.6 ≈ **13**. IP can also fold weak hands that would otherwise have c-bet.
- **Leading only weak hands:** IP raises 100%. The BB loses its share of the pot and its 1/4-pot bet, which is −25%. Mixing bluffs into the leads just makes IP call wider and raise more.
- **Rule:** with a large range disadvantage, **don't split your range. Check 100%.**

### The four donk-frequency groups

| Group | Approx. flops | Avg donk | BB equity | BB EV | BB EqR | Typical flops |
|---|---|---|---|---|---|---|
| **High (50%+)** | ~34 | 60% | 50% | 52% | **103%** | 6xx and 7xx with 1–3 possible straights |
| **Mid (25–50%)** | ~100 | 34% | 48% | 47% | 97% | Lower connected 8xx–5xx boards (8MM, 8ML, 8LL, 7ML, 7LL, 6LL, 5LL) with 1–3 straights. The only monotone flop is 764. Paired: 766, 755, 655 |
| **Low (10–25%)** | ~181 | 16% | 45% | 43% | 94% | Less connected ALL, 9MM and 8xx–4LL boards, plus most boards paired with a 9 or lower (99A, 88A, 77x, 66x, 55x, 44x, 33M) |
| **None (0–10%)** | All the rest, the vast majority | ~1% | 39% | 30% | **76%** | Trips, monotone, high paired, disconnected two-tone, Hxx and Axx |

- The family labels **overlap between groups**. Connectedness, suits and pairing decide which group a flop falls into, not the family label on its own.
- **The donk frequency is an effect, not a cause.** The way the ranges hit the board gives the BB more equity and EV, and the high donk frequency follows from that.

### High donk flops (50%+)

- These are 6-high and 7-high boards with one to three possible straights. **More possible straights → smaller lead and higher frequency.** Rainbow boards are led more than two-tone ones, and monotone boards are led much less.
- 654r is led 67% and 765r about 70%. The two-tone versions are mostly led less.
- **The shape of the ranges:** IP is 4% strong, 35% good, **50% weak** and 11% trash. The BB is 7% strong, **41% good**, 32% weak and 20% trash. The BB is **more polarized** and ahead in strong and good hands, like the Clairvoyance toy game, where the polarized player bets.
- **30–40bb:** the BB leads strong hands 73%, good 64%, weak 59% and trash 49%, mostly at **1/4 pot**. The 2/3 size is used only about 5%. A small lead lets the BB call a raise and still see the turn.
- **20bb:** **2/3 pot** is preferred. At this SPR the BB is happy to get all-in with its many good-equity hands, so the bigger bet wins folds and gets the money in while its equity is high. The strongest hands still prefer the small size.
- The **checking range still needs strong and good hands**.
- The BB leads more against **UTG (67%) than against the BN (53%)**, because a tight UTG range misses these boards more.

### Example: BB vs UTG on 654r, 30bb

| Class | How often it's led | Detail |
|---|---|---|
| **Strong** | 77% | **Straights:** 32 91%, 87 80%, 73 only 50%. **Sets:** 66 94%, but 55 and 44 only 16–31%. **Two pair:** 54 96%, 64 94%, 65 73% |
| **Good** | 70% | **Overpairs:** TT and 99 100%, 88 and 77 38%. **Top pair** 78%, **second pair** 71%, **third pair** 65%. In each, the best kickers and the combos with an OESD lead most, and middle kickers check more. **Underpairs** 22–33 78%, with 22 led more than 33 |
| **Weak** | 61% | **OESDs** 67%, with 7x led more than 3x. **Ace-high** 67%, **in reverse order**: A9s ~99% but AQs only ~40%. **King-high** 54%, also in reverse. **Gutshots** 70%, and more often with two overcards |
| **Trash** | 62% | Air leads more when it has a backdoor flush draw |

**The heuristic, partly my reading of the book's short reasons:** lead most with
hands that are **vulnerable** and **don't block the hands IP continues with**.
Check more with hands that block IP's continuing range or are less vulnerable. 32
is the weakest straight and is led most. 65 blocks the most and is the least
vulnerable two pair, so it is led least. The small sets don't block IP's top pairs,
which will bet when checked to, while top set blocks them and so leads.

### Mid donk flops (25–50%)

- The BB leads about **35%** against both UTG and the BN, because the equity distribution barely changes between them.
- IP has slightly more equity (52 vs 48), but the **BB's range is more polarized** (mostly strong, good and trash). IP still holds many weak hands that want free cards.
- **30–40bb:** strong hands use the **bigger size on paired boards** and the smaller size on unpaired boards. Hands are led **in order of equity**, the most equity leading most. The hand types are the same as on high donk flops, but the BB leads less often and checks more so its checking range stays protected.
- **20bb:** the leads are extremely polarized (strong, good and trash) and mostly use **2/3 pot**. The 1/4 size is used mainly with weak hands, plus a little of everything for balance.

### Low donk flops (10–25%)

- On these flops, which number about 181, **IP's range clearly dominates**. The BB has 45% equity and **under-realizes** it (94% EqR, capturing 43% of the pot). The BB's trash now outnumbers its weak hands, and its strong and good share is well below IP's. **Checking becomes the main strategy.**
- The leads that remain are more polarized, so **2/3 pot** is preferred (9%) over 1/4 pot (7%). Stack depth changes little.

### No donk flops (0–10%)

- These are most flops: trips, monotone, high paired, disconnected two-tone, and any high-card or ace-high board.
- The BB has 39% equity, a 76% EqR and an EV of 30% of the pot, and leads only about 1%. It lacks enough strong hands to split its range, so removing the lead costs almost nothing. **Check 100%.**

## What donking is worth

**654r, BB vs BN, 30bb, 5.6bb pot, 1/4-pot lead only:**

| BB strategy | Donk | BB EV | bb/100 | EqR |
|---|---|---|---|---|
| GTO | 57.4% | 51.9% | 290.81 | 100.6% |
| Always check | 0% | 50.8% | 284.31 | 98.35% |
| Always donk | 100% | 50.8% | 284.54 | 98.4% |

- Even on one of the best leading flops, **never donking costs only about 1.1% of the pot** (about 6.5bb/100). Leading 100% costs about the same (6.27bb/100) against a minimally exploitative opponent. On A76r, removing the lead costs nothing.
- **Overall:** heavy donking happens only on a few rare flops, so "always check" loses very little, and donk strategies are hard to execute. They're worth studying for tough games or against opponents who handle leads badly.
- **Exploitative leads:**
  - **Blocking bet:** if a villain c-bets a lot but raises a lead only when strong, lead small with some weak hands. You see a cheap card, and a raise tells you he is strong.
  - **Inducing:** if a villain raises almost every lead, lead your very strong hands. This can be counter-exploited, so it needs a solid read.

## The power of position

**The experiments:** BN (49% open) vs BB (64% call), 30bb, on 654r and A76r, with
sizes of 1.25× pot, 2/3 pot and 1/4 pot.

### Experiment 1: swap the positions but keep the ranges

**BN range:**

| BN range | Flop | Bet | Check | Equity | EV | EqR |
|---|---|---|---|---|---|---|
| IP (normal) | A76r | 98% (mostly 2/3) | 2% | 59.9% | **75.0%** | 124% |
| OOP (swapped) | A76r | 99% (mostly 1.25× and 1/4) | 1% | 59.9% | **68.3%** | 114% |
| IP (normal) | 654r | 48% | 52% | 48.4% | **48.1%** | 99% |
| OOP (swapped) | 654r | 9% (mostly 1.25×) | 91% | 48.4% | **38.4%** | 79% |

- **A76r (−6.7% of the pot):** IP bets 2/3 pot to set up **three barrels**. OOP plays a **two-street game**: overbet the flop and then jam or check the turn, or check and then check-raise all-in or fold. Fewer streets means less exposure to IP's edge.
- **654r (−9.7% of the pot):** **51% of this range is weak hands.** IP would check them back for a free card, but OOP gets bet into and has to give up equity. So OOP must **check many strong hands that can check-raise**, which makes IP bet less and lets the weak hands realize equity.

**BB range** (in the swapped solve, OOP checks to it 100%):

| BB range | Flop | Bet | Check | Equity | EV | EqR |
|---|---|---|---|---|---|---|
| OOP (normal) | A76r | 0% | 100% | 40.1% | **25.0%** | 63% |
| IP (swapped) | A76r | ~0% | ~100% | 40.1% | **37.8%** | 94% |
| OOP (normal) | 654r | 57% | 43% | 51.6% | **51.9%** | 101% |
| IP (swapped) | 654r | 56% (almost all 1/4) | 44% | 51.6% | **61.9%** | 120% |

- **A76r (+12.8% of the pot):** the range still checks back almost everything, because a bet would be check-raised too often. But it takes **free turns** instead of folding hands that would have improved.
- **654r (+10% of the pot):** the same hands bet, now almost entirely with the 1/4 size.

### Experiment 2: give both players the same range

Averaged over 654r and A76r, with both players holding the BB range or both holding
the BN range:

| | 1.25× | 2/3 | 1/4 | Check | Equity | EV | EqR |
|---|---|---|---|---|---|---|---|
| IP | 0.9% | 17.8% | 33.6% | 47.8% | 50% | **55.1%** | **110%** |
| OOP | 5.9% | 4.7% | 7.6% | 82.0% | 50% | **44.9%** | **90%** |

With identical ranges, IP takes about 5% of the pot more than its equity share and
OOP about 5% less. Other experiments agree: **position is worth roughly 5–10% of
the pot.** OOP checks far more often and, when it bets, overbets more.

### Why position wins and how OOP fights back

- **Information:** IP acts last on every street and sees OOP's action before deciding. The more streets left, the bigger the edge.
- **Depth:** deeper stacks (higher SPR) help IP and hurt OOP.
- **OOP's tools:** bigger sizes, which win the pot now or **reduce the SPR**; and **checking 100%** on flops with a big range disadvantage, which gives away no information.
- **A weak range is much worse OOP than IP.** Strong ranges realize their equity from either seat. Weak ranges OOP under-realize badly.
- **History:** BBs once over-folded to steals, so openers widened to attack them. BBs then over-corrected, defending too many marginal hands that realize poorly OOP. Solvers have since pushed BB defence close to optimal.

## Takeaways for the table

1. **Classify every flop** by structure, texture, top card, straight count and family. Similar flops play alike.
2. **As the BB against a single raiser, check by default.** On ace-high, broadway, high paired, monotone, trips and disconnected flops, check 100%.
3. **Lead on low, connected, rainbow 6-high and 7-high boards** (654, 765, 764). Lead often, small at 30bb or deeper, and include draws and air. Lead more against tight early-position ranges.
4. **When your range is behind, don't split it.** Leading only strong hands empties your checking range.
5. **Range composition beats raw equity.** The side with more strong hands and fewer weak ones gets to bet.
6. **Position is worth about 5–10% of the pot.** OOP: check more, size up, play fewer streets. IP: use smaller bets and set up three barrels.
7. **Lead only on a read:** block-bet against players who only raise strong hands, and lead the nuts against players who raise every lead.
