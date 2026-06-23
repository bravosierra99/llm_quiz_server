# Electricity Basics — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the first concept area of **Arduino Foundations**.
Written to be *true* even though it's simple — every analogy below (water-in-pipes,
one-way street) is a way to picture a real fact, not a replacement for it. Facts are
synthesised from the vetted free resources listed at the end; nothing is copied verbatim.

**How to use it:** this is the adult/teacher reference and the source the quiz questions
are drawn from. Pair it with the hands-on tools — **PhET Build an Atom** (for charge) and
**PhET Circuit Construction Kit: DC** (for current/voltage/resistance) — so she *sees* it.

---

## A1 — What electricity is (charge & electrons)

- **Everything is made of atoms** — pieces so tiny you can't see them even with most
  microscopes. Everything around you (your hand, the air, a wire) is made of atoms.
- Each atom has even smaller parts:
  - **Protons** — have a **positive (+)** charge.
  - **Electrons** — have a **negative (−)** charge.
  - **Neutrons** — have **no** charge (neutral).
- **Charge** is a property that makes things push or pull on each other:
  - **Opposite charges attract** (＋ pulls toward −).
  - **Same charges repel** (＋ pushes away ＋; − pushes away −).
- **Electric current** (the electricity that runs gadgets) is **electric charge moving** —
  in a metal wire, it's **electrons flowing** through the wire, all in the same direction.
- **Static electricity** is different: it's charge that *builds up and stays put* (like the
  zap after you rub your socks on a carpet), instead of flowing in a loop.

> Picture: electrons are like a crowd of tiny negative passengers. When they all shuffle
> along a wire together, that moving crowd **is** the electric current.

---

## A2 — Current, voltage, and resistance (the water-in-pipes picture)

The easiest way to picture electricity is **water flowing through pipes**:

| Electricity word | What it means | Water picture | Measured in |
|---|---|---|---|
| **Current** | How *much* charge flows past a spot each second | How much **water flows** through the pipe | **amps (A)** |
| **Voltage** | The **push** that makes charge move | The **water pressure** pushing the water | **volts (V)** |
| **Resistance** | How **hard it is** for charge to flow | A **narrow or clogged** pipe slowing the water | **ohms (Ω)** |

- A **battery** is like a pump: it provides the **voltage** (the push). With no push,
  nothing flows.
- More **resistance** is like a skinnier pipe — it lets **less** current through.
- These three always work together (see Ohm's Law, A4).

---

## A3 — Conductors and insulators

- A **conductor** lets electric current flow through it **easily**. Most **metals** are
  good conductors — **copper, gold, aluminum**. (That's why wires are made of metal.)
- An **insulator** does **not** let current flow easily. **Plastic, rubber, glass, wood,
  and dry air** are insulators.
- A real wire is **both**: a **copper** core (conductor) wrapped in **plastic** (insulator),
  so the electricity stays inside the wire and doesn't shock you.
- Why the difference? In conductors, some electrons are free to roam between atoms, so they
  can carry current. In insulators, the electrons are held tightly and can't move along.

---

## A4 — Ohm's Law (the rule that ties them together)

Ohm's Law is the rule connecting voltage, current, and resistance. Said in kid words:

- **More voltage (more push) → more current flows.** Push harder, more water moves.
- **More resistance → less current flows.** A narrower pipe lets less water through.

The grown-up version is a little equation: **Voltage = Current × Resistance**, often written
**V = I × R** (engineers use the letter **I** for current). She doesn't need the math yet —
the *direction* of each effect is the important idea, and it's exactly why an LED needs a
resistor (next area): the resistor adds resistance to keep the current small and safe.

---

## A5 — Units: volts, amps, ohms (and "milli")

- **Volt (V)** — the unit of **voltage**. An Arduino UNO runs on **5 volts**. A single AA
  battery is **1.5 volts**.
- **Amp (A)** — the unit of **current** (short for *ampere*).
- **Ohm (Ω)** — the unit of **resistance** (the symbol is the Greek letter omega, Ω).
- **"milli" means one-thousandth (1/1000).** So:
  - a **milliamp (mA)** is 1/1000 of an amp — small currents (like an LED's ~**20 mA**)
    are measured in mA.
  - a **millisecond (ms)** is 1/1000 of a second — `delay(1000)` waits 1000 ms = **1 second**.
    (This unit comes back in the programming lessons.)

---

## Sources (all free; fetched & verified)

- **PhET Build an Atom** — phet.colorado.edu/en/simulations/build-an-atom (CC BY) — protons/electrons & charge.
- **PhET Circuit Construction Kit: DC** — phet.colorado.edu/en/simulations/circuit-construction-kit-dc (CC BY) — current/voltage/resistance, Ohm's law, hands-on.
- **Ducksters: Electric Current** — ducksters.com/science/physics/electric_current.php — current as flowing charge, water analogy.
- **Ducksters: Ohm's Law** — ducksters.com/science/physics/ohms_law.php — voltage=pressure, resistance=pipe width.
- **Ducksters: Conductors & Insulators** — ducksters.com/science/physics/electrical_conductors_and_insulators.php.
- **SparkFun (adult reference, CC BY-SA 4.0):** *What is Electricity?* and *Voltage, Current, Resistance & Ohm's Law* (the water-analogy table; LED current "safely under 20mA").
</content>
