# Components — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the **Components** area of **Arduino Foundations**.
Written to be *true* even though it's simple — every analogy below (one-way street, tiny
bucket, electric lever) is a way to *picture* a real fact, not a replacement for it. Facts
are synthesised from the vetted free resources listed at the end; nothing is copied verbatim.

**How to use it:** this is the adult/teacher reference and the source the quiz questions are
drawn from. Pair it with the hands-on tools — **PhET Capacitor Lab: Basics** (for how charge
builds up on two plates) and **PhET Magnets & Electromagnets** (battery + coil = electromagnet,
the heart of motors and relays) — so she *sees* it. Components are the little parts you plug
into a circuit; each one does one job.

---

## C1 — Resistors (they limit the current)

- A **resistor** is a little part whose job is to **make it harder for current to flow** —
  it **resists** the current, which is where the name comes from.
- Why would you ever want *less* current? Because too much current can **damage parts**. A
  resistor keeps the current down to a **small, safe amount**.
- The classic Arduino story: an **LED** (a tiny light) can only take a little current. If you
  wire an LED straight to the battery with **no resistor**, too much current rushes through
  and the LED **burns out** — it can flash bright once and then never light again.
- The fix is to put a resistor **in line with** (right next to) the LED. The resistor holds
  the current back so the LED gets just enough to glow — and it keeps glowing.
- A resistor turns a little of the electrical energy into **heat** as it slows the current.
  (That's normal and safe for the tiny amounts here.)
- Resistors don't care which way around you plug them in — they work **either direction**.

> Picture: a resistor is like a **kink or a pinch in a hose**. The water still gets through,
> but less of it, so whatever is downstream doesn't get blasted.

---

## C2 — LEDs & Diodes (a one-way street for current)

- A **diode** is a part that lets current flow **only one way**. Think of it as a
  **one-way street**: current can go through in the forward direction, but the diode
  **blocks** it from going backward.
- An **LED** is a special kind of diode. LED stands for **Light-Emitting Diode** — a diode
  that **makes light** when current flows through it the correct (forward) way.
- Because a diode only works one way, an LED has a **+ side and a − side** (this is called
  its **polarity**). It only lights up when you connect it the right way round.
- How to tell which leg is which: on a fresh LED the **longer leg is the + side** (the
  **anode**). The longer leg goes toward the **positive** part of the circuit.
- If you plug an LED in **backward**, current can't flow through it, so it simply **doesn't
  light** (it's not "broken" — just facing the wrong way).
- LEDs still need a **resistor** (see C1) to keep the current small and safe.

> Picture: a diode is a **turnstile** at a gate — you can push through one way, but it won't
> let you go back the other way.

---

## C3 — Capacitors (a tiny, fast rechargeable bucket)

- A **capacitor** is a part that can **store a little electric charge** and then **let it
  back out** again. Inside, it has **two metal plates** with a gap between them; charge
  builds up on the plates.
- A good picture is a **tiny rechargeable bucket** for charge: you fill it up (charge it),
  and later you can pour it back out (discharge it).
- A capacitor is **not a battery**. A battery makes its energy from chemicals inside and can
  power things for a long time. A capacitor only **holds** charge you put into it, it holds
  only a **little**, and it fills and empties **very fast**.
- Capacitors are great at **smoothing things out** — they can soak up a sudden surge and give
  charge back a moment later, so the power to other parts stays steady.
- A capacitor does **not make electricity** on its own — it only stores charge that the
  circuit gives it, and gives that charge back.

> Picture: a battery is like a **water tank** that holds a lot for a long time; a capacitor is
> like a **small cup** you can fill and tip out again in a blink.

---

## C4 — Switches, Transistors & Relays (a small signal controls a bigger one)

- A **switch** simply **opens or closes** a circuit. Closed = the loop is complete and current
  flows (light **on**). Open = there's a gap, so current stops (light **off**). A light switch
  on your wall is exactly this.
- A **transistor** is like a switch with **no moving parts** that a **small electric signal**
  can flip on and off. The big idea: a **small** current or voltage at one pin **controls a
  bigger** current flowing through the transistor. That's how a tiny Arduino pin can switch
  something that needs more power than the pin can give on its own.
- A **relay** does the same "small controls big" job, but with a real moving part. Inside is
  an **electromagnet**: send a **small** current through it and it becomes magnetic and
  **physically pulls a switch closed**, which turns on a **much bigger** circuit. Let the small
  current stop and the switch springs back open.
- So a relay is like an **electric lever**: a little push on one side moves something much
  heavier on the other side. You can hear it **click** when it switches.
- Why this matters for Arduino: the board's pins are small and weak, so transistors and relays
  let a **little Arduino signal control big things** like a motor or a household lamp — safely.

> Picture: flipping a tiny light switch (the small signal) that makes a **giant door**
> (the big circuit) swing open. You barely push; the big thing moves.

---

## C5 — Buzzers & Speakers (electricity makes something vibrate → sound)

- **Sound is vibration.** When something shakes back and forth quickly, it pushes the air,
  and those tiny pushes travel to your ear as sound.
- A **buzzer** and a **speaker** both turn **electricity into sound** by making a part
  **vibrate**. Electricity makes a small piece move back and forth fast, the air wiggles, and
  you hear a tone.
- The **faster** the vibration (more wiggles each second), the **higher** the pitch (squeakier).
  Slower vibration makes a **lower** pitch (deeper). The speed of the vibration is its
  **frequency**.
- An **active buzzer** has its own tone built in — give it power and it just buzzes one note.
  A **passive buzzer** (or a speaker) needs the circuit to tell it **how fast to vibrate**, so
  you can make different pitches and even little tunes.
- A speaker often uses a **coil and a magnet**: the changing electric current makes the coil
  push and pull against the magnet, which vibrates a cone and pushes the air — that's the sound.

> Picture: pluck a guitar string and it **shakes the air**; a speaker is a part that the
> electricity "plucks" thousands of times a second to make a steady tone.

---

## C6 — Motors (electricity + magnetism → spinning and motion)

- A **motor** turns **electricity into motion**. The secret ingredient is **magnetism**: when
  current flows through a coil of wire it becomes an **electromagnet** (a magnet you can switch
  on and off with electricity).
- Magnets **push and pull** on each other (opposite poles attract, same poles repel). A motor
  uses an electromagnet pushing and pulling against other magnets to make a shaft **spin**.
- A **DC motor** just **spins** when you give it power — fast and continuous. Great for wheels
  and fans. (A transistor often switches it on, because a motor needs more current than an
  Arduino pin can give — see C4.)
- A **servo motor** doesn't spin freely; it **turns to a set angle** (like "point to 90°") and
  holds there. You tell it the angle and it goes there. Great for steering and robot arms.
- A **stepper motor** moves in **small, precise steps**, one click at a time, by switching its
  electromagnets in order. Great when you need to move an **exact** amount — like a 3D printer.

> Picture: hold two magnets and feel them shove each other — a motor is that shove, sped up and
> aimed in a circle so a shaft keeps spinning.

---

## Sources (all free; vetted in the lesson plan)

- **Build Electronic Circuits — What is a resistor?** — build-electronic-circuits.com/what-is-a-resistor/ — resistor limits current; the LED-burns-out-without-one story (C1).
- **Explain That Stuff — Diodes & LEDs** — explainthatstuff.com/diodes.html — "a diode is the electrical equivalent of a one-way street"; LEDs make light; polarity (C2).
- **PhET Capacitor Lab: Basics** — phet.colorado.edu/en/simulations/capacitor-lab-basics (CC BY) — charge builds up on two plates (C3).
- **Explain That Stuff — How relays work** — explainthatstuff.com/howrelayswork.html — switch a tiny current and it switches on a much larger current (C4).
- **PhET Magnets & Electromagnets** — phet.colorado.edu/en/simulations/magnets-and-electromagnets (CC BY) — battery + coil = electromagnet; the basis of motors & relays (C4, C6).
- **Exploratorium — Cup Speaker (Science Snack)** — exploratorium.edu/snacks/cup-speaker — build a speaker: electricity → vibration → sound (C5).
- **(adult reference, CC BY-SA 4.0) SparkFun:** *Transistors — introduction* (a small signal controls a bigger one, C4) · *Capacitors* (two plates store charge, C3) · *Motors and selecting the right one* ("What makes a motor move? …magnetism!", C6).
