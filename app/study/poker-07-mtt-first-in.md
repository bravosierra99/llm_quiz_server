---
title: "Poker 07 — MTT Equilibrium Strategies: Playing First In"
summary: "Modern Poker Theory ch. 7: MTT open, 3-bet, squeeze and 4-bet sizing, short-stack push/fold charts, and first-in strategy (shove, raise, limp, fold) for every seat from SB to UTG at 10–80bb."
order: 107
audience: bravosierra99
---

# Poker 07 — MTT Equilibrium Strategies: Playing First In

*Study guide to Chapter 7 of* Modern Poker Theory *(Michael Acevedo). The chapter
is mostly range grids (Hand Ranges 88–139) plus one action-frequency table per
seat. This guide gives the headline frequencies and how each range changes with
stack depth; open the book for the exact cells. Unless stated otherwise, numbers
are chip-EV (no ICM) solver equilibria for 9-max with a 12.5% ante (1.125bb of
antes in every pot).*

## Set-up and planning

- Focus depths are **15, 25, 40 and 60bb**, where most tournament action happens; the summary tables run 10–80bb.
- **Deep with no ante** (first levels): less dead money, so ranges are **tighter** and close to cash-game ranges without rake; speculative hands gain value and flatting/post-flop play becomes more attractive.
- **Under 10bb, play push/fold**: a more complex strategy gains almost nothing.
- **Plan before you open.** Know your stack, who is left to act, their stacks, and how likely they are to 3-bet or call. Decide *before* raising whether the hand is a **raise-fold or a raise-call**, and whether it plays better as an **open shove or a min-raise**. The same hand may call a 15bb jam but not a 20bb one, or call from one seat but not another. Most short-stack blunders (especially when multi-tabling) come from autopiloting this.

## Open-raise sizing

**Size barely matters as long as the range fits the size.** Bigger opens force tighter ranges, or the bottom of the range loses money. Sweet spot: **2–2.5bb from UTG to BN, 2.5–3.5bb blind vs blind**.

**Below 25bb (the rejam zone), min-raise.** Two reasons:

1. **Raise-folding is cheaper.** UTG with 10bb, BB jams. Opened 3x: call 7 into 14.6 (better than 2:1, need ~32%), so you're committed with any sane hand. Opened 2x: call 8 into 13.6 (1.7:1, need ~37%), so you can fold the bottom of your range.
2. **Big opens give rejams a better price.** Ignoring equity when called, a jam needs:

> break-even fold % = risk ÷ (risk + pot it wins)

CO opens 2.5x at 20bb: the BB risks 19 to win 5.125 (2.5 + 0.5 + 1 + 1.125 antes), so it needs **78.8%** folds. Open 2x instead: the pot is 4.625 and the jam needs **80.4%**. Every chip added to the open makes the rejam cheaper.

Deeper and in general:

- **From 30–35bb**: a rejam risks too much for too little, so open **2.3x**. That cuts villains' implied odds and makes peeling weak hands harder. **100bb+: 2.3–2.5x**; no evidence that bigger earns more.
- **Bigger sizes deep and OOP; smaller from early position.** One size for every seat is fine: scaling size with position adds complexity for little EV. In the solver ranges UTG and UTG+1 keep opening **2x even at 40–60bb**, while UTG+2 to BN use **2.3x** from 40bb.
- **SB opens**: the non-all-in raise appears at **17bb as 2.5x**, grows to **3.3x at 25bb** and **3.5x from 30bb**. The solver likes up to 5x deeper, but 3.5x loses almost nothing.
- Small sizes still work online because fields over-fold to them. As players learn that calling and realizing equity is always an option, sizes are trending up; old click-back 5-bets are extinct.

## 3-bet, squeeze and 4-bet sizing

**3-bet sizes** (total bb). "AI / 5" = mix of jamming and a small 3-bet; "vs open" is the open size assumed.

| Stack | IP | SB | BB | vs open |
|---|---|---|---|---|
| <20 | AI | AI | AI | 2x |
| 20–23 | AI / 5 | AI / 5.5 | AI / 5.5 | 2x |
| 24–27 | AI / 5.5 | AI / 6.5 | AI / 6.5 | 2x |
| 28–35 | 6 | AI / 7 | AI / 7 | 2.3x |
| 36–45 | 7 | 8 | 8 | 2.3x |
| 46–65 | 7.5 | 9 | 9 | 2.3x |
| 66–99 | 8 | 9.5 | 9.5 | 2.3x |
| 100+ | 8.5 | 10 | 10 | 2.5x |

**Squeeze sizes** (open + caller in front):

| Stack | IP | SB | BB | vs open |
|---|---|---|---|---|
| <20 | AI | AI | AI | 2x |
| 20–23 | AI / 6 | AI | AI | 2x |
| 24–27 | AI / 6.5 | AI / 7 | AI / 7 | 2x |
| 28–35 | AI / 7 | AI / 7 | AI / 7 | 2.3x |
| 36–45 | 8 | AI / 10 | AI / 10 | 2.3x |
| 46–65 | 8 | 10 | 10 | 2.3x |
| 66–99 | 10 | 12 | 12 | 2.3x |
| 100+ | 10 | 13.5 | 13.5 | 2.5x |

Read-off: IP 3-bets are ~2.5–3.5× the open; blind 3-bets run from ~3× when shallow to ~4× when deep. Squeezes are bigger than 3-bets, and the jam option lasts deeper for squeezes and for the blinds.

- **SB 3-bets a bit smaller than the BB** (the author's preference; the table prints identical numbers). The BB behind can wake up with a hand, so a smaller size saves chips, and the SB 3-bet range is less polarized, so it minds being called less.
- **One-third rule:** if a 3-bet would put **over 1/3 of your stack** in, you're pot-committed with anything but trash. With a weak hand, **jam instead**, leaving villain only call or fold.
- **Under 40bb, 4-bets are all-in only.** A smaller 4-bet either commits you anyway or is so small that villain can flat and realize equity. **50–100bb**: non-all-in 4-bets to **2.25–2.5x IP, 2.5–3x OOP**. **5-bets are always all-in.**

## Short-stack push/fold charts

Hand Ranges 88–95 give, per seat, the **largest stack (bb) at which each hand can be open-shoved**; black cells shove at **any stack ≤10bb**. Example: from the SB, **95s shoves at 10bb but 95o only at 5bb or less**. These charts are a separate model (HRC with FGS, push or fold only), so they won't match the solver tables below, where min-raises and limps exist.

| Seat | Shoves at 10bb |
|---|---|
| SB | Nearly everything; only the weakest offsuit hands and some weak low suited hands need a shorter stack |
| BN | Any pair, any ace, any suited king, K6o+, Q5s+, Q9o+, J7s+, J9o+, T7s+, T9o, 96s+, 86s+, 75s+, 65s, 54s |
| UTG | 33+, A7s+, A5s, K9s+, Q9s+, J9s+, T9s, ATo+, KQo (22, A4s, KJo, 98s from ~9bb; A9o and A8o from 8bb) |

Ranges widen quickly as the stack shrinks and the seat gets later; pairs, aces and suitedness carry the most weight. CO to UTG+1 sit between BN and UTG; see the book.

## The whole table at a glance

Total VPIP (%) when folded to you (BN without limps):

| Seat | 10bb | 15bb | 25bb | 40bb | 60bb | 80bb | Avg |
|---|---|---|---|---|---|---|---|
| SB | 79.6 | 85.2 | 82.1 | 80.8 | 85.0 | 86.8 | **83.1** |
| BN | 38.9 | 39.3 | 46.3 | 50.9 | 54.4 | 55.5 | **45.4** |
| CO | 31.4 | 30.2 | 34.3 | 36.4 | ~37 | ~37 | **33.6** |
| HJ | 27.7 | 23.8 | 27.8 | 28.6 | 28.1 | 28.2 | **26.9** |
| LJ | 22.6 | 20.2 | 24.1 | 23.6 | 22.7 | 22.4 | **22.5** |
| UTG+2 | ~19.5 | 17.4 | 21.3 | 20.6 | 18.8 | ~19 | **19.6** |
| UTG+1 | 17.0 | 15.6 | 18.6 | 17.6 | 16.8 | 16.5 | **16.7** |
| UTG | 15.4 | 14.1 | 16.8 | 15.8 | 15.1 | 14.1 | **15.2** |

*(The book's CO 60/80bb and UTG+2 10/80bb rows don't add up; "~" values follow the trend.)*

1. **Late seats widen as stacks deepen** (BN +16.6 points from 10 to 80bb; CO ~31 → ~37). Position is worth more deep. The blinds' best counter, the rejam, has poor risk/reward beyond ~40bb, so they can't deny the BN its equity, and the BN's EqR, already the highest at the table, keeps growing.
2. **MP and EP peak at 25–30bb, then flatten or shrink.** With players behind they'll often be OOP, and deeper stacks magnify that disadvantage, so they can't expand.
3. **The fewer players behind, the wider**: averages fall from SB 83% and BN 45% to UTG 15%.
4. Observation from the tables: most seats are tightest around 12–15bb, between the wide push/fold zone and 25bb.

## When shoves vanish and min-raises appear

| Seat | At 10bb | Shoves gone by | Notes |
|---|---|---|---|
| SB | Push/limp/fold (51% shove) | 30bb (1.8% at 25bb) | No non-all-in raise until 17bb |
| BN | 33.5% shove, 5.4% raise | 25bb (3.5% at 20bb) | ~50/50 shove vs min-raise at 15bb |
| CO | Pure push/fold | 20bb | Min-raises from 12bb |
| HJ | Pure push/fold | 20bb | Min-raise from 12bb, dominant at 15bb |
| LJ | 20.3% shove, 2.3% raise | 17bb | Unlike CO/HJ, already has a raise-fold range at 10bb |
| UTG+2 | Shoves + 5.9% raise | 17bb | 2.2% shove at 15bb, but those hands are indifferent to a min-raise, so just raise/fold |
| UTG+1 | 12.8% shove, 4.1% raise | 17bb | ~50/50 at 12bb |
| UTG | 11.0% shove, 4.4% raise | 15bb | Mixed 10–14bb |

**Why:** an open shove risks your stack against everyone behind; the more players left, the likelier someone **wakes up with a premium**, so earlier seats shove less and switch to min-raising sooner. Late seats stop shoving as stacks deepen because **a shove gives up position**, the BN's biggest edge.

**The shove/min-raise split** (CO at 15bb is the model): shove hands **too good to raise-fold but not good enough to raise-call**. Min-raise hands **happy to call a jam** plus blocker hands that make good top pairs and **fold easily to a rejam**.

## Small blind (avg VPIP 83%)

The widest seat: **already half a blind in, only one player left**.

| Stack | All-in | Raise | Limp | Fold |
|---|---|---|---|---|
| 10bb | 51.0 | — | 28.6 | 20.4 |
| 12bb | 42.2 | — | 40.0 | 17.7 |
| 15bb | 23.7 | — | 61.5 | 14.8 |
| 17bb | 18.0 | 16.3 (2.5x) | 50.1 | 15.6 |
| 20bb | 13.0 | 17.3 (2.5x) | 54.8 | 14.9 |
| 25bb | 1.8 | 29.8 (3.3x) | 50.5 | 17.9 |
| 30bb | 0 | 31.8 (3.5x) | 48.2 | 19.9 |
| 40bb | 0 | 26.4 (3.5x) | 54.4 | 19.2 |
| 60bb | 0 | 15.1 (3.5x) | 69.9 | 15.0 |
| 80bb | 0 | 12.0 (3.5x) | 74.8 | 13.2 |

Shoves shrink and **limping becomes dominant**; raising peaks around 30bb, then gives way to limps.

**15bb** (shove 23.7 / limp 61.5 / fold 14.8)
- Shove: **blockers** (Ax, Kx); **66–22** (equity vs calling ranges, poor post-flop EqR); **98s–65s** (plenty of equity but can't call a jam themselves).
- Limp: **traps that can call a jam** (77+, broadways, suited Ax/Kx) plus **weak hands happy to limp-fold** that do fine in limped pots (Q2o, J8o, T4s, 73s).
- Limp, BB jams: call 21.3% of limps. Limp, BB raises 3x: jam 12.9 / call 49.1 / fold 38.

**25bb** (shove 1.8 / raise 3.3x ~30 / limp ~50 / fold 17.9)
- Shove only **44–22 and A9o/A8o**.
- Raise is **polarized**: hands that can call a jam (66+, A8o+, A5s+, best broadways), plus **blocker** hands (A7o–A2o, Kxo) and hands that play well in raised pots (KJo, QTo, J8s, 74s).
- Limp: traps (AKo–A9o, 99–44) plus equity hands that don't want to raise and fold to a jam (KTo, Q9s, 76s).
- Limp vs jam: call 15.2%. Limp vs 3.3x: jam 11 / call 43.7 / fold 45.4. Raise vs jam: call 30.1%.

**40bb** (raise 3.5x 26.4 / limp 54.4 / fold 19.2): no shoves; most hands mix, **stronger hands raising more often, weaker hands limping more often**.
- Limp vs 3.5x raise: **limp-jam 5.9%** (99, 88, 77, 33, 22, AQo, AJo, a little ATo/A5o/A4o); **re-raise to 2.75x 6.4%** (55+, AT+, KQs, blocker bluffs with Axo/Kxo); call 42; fold 45.6.
- Raise vs BB 3-bet: jam 13.1 / call 40.4 / fold 46.5.

**60bb** (raise 15.1 / limp 69.9 / fold 15): no hand raises 100% of the time; many limp 100%.
- Limp vs raise: too deep to limp-jam; the only re-raise is **3.4x** (11.7%): hands happy to stack off, plus blockers with board coverage. Call 47, fold 41.3.
- Raise vs 3-bet: jamming (AKo, A5s at a small frequency) is negligible, so drop it and **4-bet to 2.6x** (8.4%) with **KK, QQ, AK, AQo** plus blocker bluffs. **AA slowplays by calling**; many suited hands call; most offsuit and disconnected hands fold.

## Button

The BN's superpower: **nobody can enter behind it and force it to play OOP.**

**With limping allowed** (avg VPIP 44.5%, limps 11.7% overall):

| Stack | All-in | Min-raise | Limp | Fold |
|---|---|---|---|---|
| 10bb | 32.6 | — | 8.5 | 58.9 |
| 12bb | 27.3 | — | 14.8 | 57.9 |
| 15bb | 21.4 | 8.9 | 11.4 | 58.3 |
| 20bb | 8.0 | 25.4 | 12.9 | 53.7 |
| 30bb | 0 | 43.0 | 8.2 | 48.8 |

- 10–12bb: **push/limp/fold, no min-raises** (limping beats min-raising). From 15bb min-raising matters because it keeps post-flop play IP. No shoves at 30bb. **40bb+: no limps.** Rejamming is riskier for the blinds, so opening is better: the BN defends 3-bets by **calling IP** and realizes equity it would lose folding to a jam.
- Limps: traps, weak suited hands that like cheap flops, offsuit high-mid hands that flop top pairs and straight draws.
- **Why BN limps are rare in practice:** hard to balance; more variance and more 3-way pots (the SB gets a great price to complete); less EV than SB limps (no discount, no guarantee of heads-up); and **BBs still over-fold to BN min-raises**.

**Raise/fold only** (what modern games play):

| Stack | 10 | 12 | 15 | 17 | 20 | 25 | 30 | 40 | 60 | 80 |
|---|---|---|---|---|---|---|---|---|---|---|
| All-in | 33.5 | 27.2 | 20.8 | 14.6 | 3.5 | 0 | 0 | 0 | 0 | 0 |
| Raise | 5.4 | 10.6 | 18.5 | 25.6 | 38.4 | 46.3 | 48.6 | 50.9 | 54.4 | 55.6 |

- **15bb**: ~50/50 shove (20.8) vs 2x (18.5). Shove the hands with equity vs calls but poor playability: **66–22, AJo–A2o, offsuit broadways, premium suited connectors**.
- **25bb** (2x, 46.3%): no shoves. **High-card value beats playability**: **K7o** (its king blocks the blinds' rejams) is worth more than **74s**. **33 and 22 fold**: they're **reverse blockers** (they don't block the blinds' rejamming hands, so you get re-shoved more and must fold); called, they mostly play as underpairs (passive and denied equity, or bluffing with few outs); and implied odds are poor at 25bb.
- **40bb** (2.3x, 50.9%): suited gappers (playability) and small pairs (implied odds) gain. Fewer 4-bets than at 25bb: the higher SPR rewards the BN's post-flop EqR.
- **60bb** (2.3x, 54.4%): wider still; fewer 4-bet jams (non-all-in 4-bets now exist); the main defence vs 3-bets is **flatting IP**.

## Cutoff (avg 33.6%)

**No limping from the CO back** (author's choice): players behind can over-limp or raise, the EV gained is too small for the added complexity, and limps for every 9-max seat blow up the solver tree. Raise/fold is also how modern games play.

- Pure push/fold at 10bb (31.4%); min-raises from 12bb; shoves 13.6% at 15bb, 6.7% at 17bb, gone at 20bb.
- **15bb** (shove 13.6 / 2x 16.5): shove the too-good-to-raise-fold, not-good-enough-to-raise-call hands: **KTo, QJo, T9s, small/medium pairs, small Axs, mid-high Axo**. Min-raise hands **happy to call a jam** (good Ax, mid-high pairs, suited broadways) plus blocker hands that make good top pairs and **fold easily to a rejam**.
- **25bb** (2x, 34.3%): no shoves. **33/22 fold from every seat except the SB**: too deep to jam, too shallow for set-mining implied odds.
- **40bb** (2.3x, 36.4%): adds **33, 22** and extra suited hands (K2s, Q4s, T6s, 96s). **60bb**: nearly the same range.

## Hijack (avg 26.9%)

Middle position is tighter: more players behind, more often OOP.

- Push/fold at 10bb (27.7%); min-raise appears at 12bb and dominates at 15bb (2x 16.1 vs shove 7.7); shoves fade at 17bb (2.4%) and are gone from 20bb.
- **25bb** (27.8%): high-card value, meaning hands that make strong top pairs or good flush draws.
- **40bb** (28.6%): adds a few deeper-stack hands (33, 96s, 54s); shape barely changes.
- **60bb** (~28%): same frequency, new shape. It **drops weak high-low hands (K3s, A7o, Q6s)** and adds hands that can flop big (22, small suited connectors).

## Lojack (avg 22.5%)

- **15bb** (shove 4.9 / 2x 15.3): a small shove range of hands that want to get all-in and realize all their equity: **77–55, AQo, AJo, A9s, A8s, JTs+**. No shoves from 17bb.
- **25bb** (24.1%): a big jump from 15bb (20.2%). Adds hands that flop top pairs and draws (**J8s, T8s, 98s**) but **folds 44 and 33** (too deep to jam).
- **40bb** (23.6%): similar size, shifts **from high-card value toward connectedness**.
- **60bb** (23%): slightly tighter; trims marginal suited broadways, small pairs and low suited connectors.

## UTG+2 (avg 19.6%)

Early position: **six or more players to get through**, so speculative hands lose value (more 3-bets, more OOP play) and VPIP drops under 20%. **Open-shoving falls too**: more players behind means someone is likelier to wake up with a premium. The trend continues the earlier you sit.

- **15bb**: the 2.2% shove range is indifferent to a min-raise, so **play raise/fold**. No shoves from 17bb.
- **25bb** (21.3%, the peak with 30bb): adds **baby Ax** and the best suited connectors.
- **40bb** (20.6%): offsuit broadways lose value; small suited connectors gain.
- **60bb** (19%): 87s–65s and weak suited high-low hands (K7s, K6s, Q8s, J8s) struggle. The range moves to **stronger, less-dominated hands** and adds **44, 33** (they flop sets and are easy to play).

## UTG+1 (avg 16.7%)

- **12bb**: about **50/50 shove vs min-raise** (7.9 / 7.7). **15bb**: effectively raise/fold.
- **25bb** (18.6%, the peak): adds **A4s, A3s** and the strongest suited connectors.
- **40bb** (17.6%, 2x): shrinks toward hands that flop **the nuts or nut draws**. Weaker offsuit broadways lose value: they struggle vs 3-bets, and top pair is worth less deeper.
- **60bb** (16.5%, 2x): tighter again; offsuit broadways and suited connectors become nearly unplayable; focus on **raw equity and blockers**.

## UTG (avg 15.2%)

- The tightest seat. **10–14bb: mix shoves and min-raises** (10bb: 11.0 / 4.4). **15bb+: raise/fold only**, 2x at every depth.
- VPIP peaks at **20–30bb** (16.8% at 25bb) and falls to ~14% at 80bb. **The size barely changes; the hand types do.** Shallow: high equity and blockers. Deep: hands that make the nuts or nut draws. Offsuit broadways decline; suited connectors and small pairs enter at a low frequency, mainly for **board coverage**.

## Hand classes across the chapter

| Hand class | Short (≤15bb) | ~25bb | Deep (40–60bb) |
|---|---|---|---|
| Small pairs (22–44) | Strong shoves: equity vs calls, poor EqR | **Fold** outside the SB (too deep to jam, too shallow to set-mine); SB still shoves 44–22 | Return as set-mining hands (CO/HJ 40bb, UTG+2 60bb) |
| Offsuit Ax / Kx | Shoves and blocker raises | Blocker opens (BN K7o, SB A7o–A2o) | Weak high-low hands drop (HJ loses A7o at 60bb) |
| Suited connectors | Shoves (can't call a jam) | Opens from LJ and later; only the best from EP | Gain in late/mid seats; struggle from EP at 60bb |
| Offsuit broadways | Shoves and opens (high card, top pairs) | Opens | Decline from EP: can't call 3-bets, top pair worth less |

## Takeaways for the table

1. Before opening short, know whether the hand is a raise-fold or raise-call, and whether it's a shove or a min-raise.
2. Under ~25bb min-raise (except from the SB); from 30–35bb open ~2.3x; jam rather than make a 3-bet that commits a third of your stack.
3. Shove the hands too good to raise-fold but too weak to raise-call; min-raise the ones that can call a jam and the easy raise-folds.
4. In the SB, limp a lot, with traps in the limping range, and limp more as stacks deepen.
5. Late seats open wider as stacks deepen. Early seats peak around 25bb, then tighten and swap offsuit broadways for hands that make the nuts.
6. At ~25bb, fold 33/22 first in from every seat but the SB.
