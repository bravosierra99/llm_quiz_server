# Circuits — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the second concept area of **Arduino Foundations**.
Written to be *true* even though it's simple — every analogy below (a loop, a road, a
city map) is a way to picture a real fact, not a replacement for it. Facts are
synthesised from the vetted free resources listed at the end; nothing is copied verbatim.

This area builds on **Electricity Basics (Area A)**: you already know that current is
moving charge, that voltage is the push, and that resistance fights the flow. Here you
learn how those pieces are wired together into a working **circuit**.

**How to use it:** this is the adult/teacher reference and the source the quiz questions
are drawn from. Pair it with the hands-on tool — **PhET Circuit Construction Kit: DC** —
so she can build a loop, break it, and *watch* the bulb go on and off.

---

## B1 — What a circuit is (a complete loop)

- A **circuit** is a **complete loop** that electric current can travel around. The
  current goes: **source → wire → load → wire → back to the source**, around and around.
  - The **source** is what supplies the push (the voltage) — usually a **battery** (or the
    Arduino's 5-volt pin).
  - The **wire** is the path the current travels along (a conductor, like copper).
  - The **load** is the part that *does a job* using the electricity — a light bulb, an
    **LED**, a buzzer, a motor.
- The big rule: **the loop has to be complete.** If there is any gap or break anywhere in
  the loop, the current **stops** and the load turns off.
- A **switch** works by making or breaking that loop on purpose. Flip it one way and the
  loop is complete (current flows, light on); flip it the other way and you open a gap in
  the loop (current stops, light off).
- A break that you *didn't* mean to make — a loose wire, a dead battery — stops the
  circuit too. There is no "leftover" electricity that keeps going; if the loop is open,
  the flow stops everywhere in it.

> Picture: a circuit is like a **toy train on a circular track**. The train (current) can
> only keep going if the loop of track is unbroken. Lift out one piece of track and the
> train can't get past — it stops. The battery is the engine that keeps it moving.

A circuit needs **at least these three things**: a **source** (push), a **path** (wire),
and usually a **load** (the thing being powered). Connecting a source straight back to
itself with only wire and no load is a **short circuit** — that's dangerous because
nothing is there to limit the current, so the wire and battery get very hot. (That's one
big reason an LED needs a resistor — more in Area C.)

---

## B2 — Polarity and ground (+, −, and GND)

- A battery has **two ends**, and they are different. This "two different ends" idea is
  called **polarity**:
  - the **positive (+)** end, called the **positive terminal**, and
  - the **negative (−)** end, called the **negative terminal**.
- Current needs **a full path that leaves one terminal and comes all the way back to the
  other**. It is not enough to connect just the + side — the charge has to have a way to
  **return**, or nothing flows. (Think of a slide: kids can only keep going down if there's
  also a ladder back up to the top. A one-way trip with no way back stops the line.)
- **The direction we draw current:** by long-standing agreement, engineers draw
  **current as flowing out of the + terminal**, around the loop through the load, and
  **back into the − terminal**. This agreed-upon direction is called **conventional
  current**. (Inside a metal wire the actual tiny electrons drift the *other* way, from −
  toward +, because they are negative — but everyone *labels and draws* circuits using the
  + → − convention. Both facts are true; they're just two ways of describing the same loop.)
- **GND stands for "ground."** On an Arduino and in most electronics, **ground is the
  common 0-volt point** — the reference everything else is measured against, and the
  **− (return) side** of the circuit. Voltage is always a *difference between two points*,
  so we pick ground as the "zero" and measure other points up from it (the 5V pin is "5
  volts **above** ground").
- Important: in small electronics, **GND does not mean the dirt outside.** It's an
  electrical *reference point* inside the circuit, not a wire stuck in the soil. (House
  wiring really does connect to the earth, but a battery-powered Arduino circuit's "ground"
  is just its own 0-volt return line.)
- **Polarity matters for some parts.** An **LED** only lets current through **one way**, so
  it has to be put in the right way around (long leg toward +). A plain resistor or a plain
  light bulb works either way. (More on which parts care about direction in Area C.)

---

## B3 — Series vs parallel (one path vs many paths)

There are two basic ways to connect more than one part in a circuit:

- **Series = in a line, one single path.** The parts are connected end-to-end, so the
  *same one loop* runs through all of them, one after another. The current has **only one
  road** to follow.
- **Parallel = side-by-side, multiple paths.** Each part gets its **own branch** back to
  the source, so the current has **more than one road** it can take.

The clearest, always-true difference is what happens when **one part breaks**:

- **Series:** because there's only one path, **breaking any one part opens the whole loop**,
  and **everything goes off.** This is the old-style string of holiday lights where if one
  bulb burned out, the *entire* string went dark — they were wired in series.
- **Parallel:** each branch is its own loop back to the source, so if **one branch breaks,
  the others keep working.** The lights in the rooms of a house are wired in parallel — turn
  off (or unplug) one lamp and the others stay on.

> Picture: **series** is a single-lane road where everyone follows the same line — one
> stalled car and the whole line stops. **Parallel** is a road that splits into several
> lanes that rejoin later — block one lane and traffic still gets through on the others.

Why it matters for Arduino: a breadboard build often puts several LEDs **in parallel** (each
with its own resistor) so they light independently, and a switch is put **in series** with a
part so the switch can turn just that part on and off.

---

## B4 — Schematics and breadboards (the map and the build-board)

**A schematic is a map of a circuit.**

- A **schematic** is a drawing that shows **how parts are connected**, using simple
  **symbols** instead of pictures of the real parts. It's like a **subway map**: it doesn't
  show what the train looks like, it shows *which stops connect to which*.
- A few symbols she'll meet:
  - a **battery / power source** (gives the push),
  - a **resistor** (a zigzag or a rectangle),
  - an **LED** (a triangle with an arrow, pointing the way current flows through it),
  - a **switch** (a little lever that opens or closes the loop),
  - **ground (GND)** (a small downward stack of lines).
- **Lines are wires, and dots are connections.** A line between two symbols means a wire
  joins them. A **dot** where lines cross means they are **truly connected**; **no dot**
  usually means the wires just *cross over* without touching.
- A schematic shows the **connections, not the real-life shape or distance.** Two parts
  drawn close together might be far apart on the real board, and that's fine — the map only
  promises *what connects to what*.

**A breadboard is a board for building circuits with no soldering.**

- A **breadboard** is full of little holes you push wires and parts into. Under the
  plastic, **hidden metal strips** connect certain holes together, so parts that share a
  strip are wired together automatically.
- **The middle of the board (the rows):** there's a **gap (a center ravine) down the
  middle.** On **each side** of that gap, the holes are joined in **short rows of five**
  that run *across* (toward the gap). The **five holes in one row-segment on one side are
  connected to each other** — but **the gap separates the two sides**, so a row on the left
  of the gap is *not* connected to the row on the right. (The gap is there on purpose so you
  can straddle a chip across it without shorting its two sides together.)
- **The edges (the power rails):** along the long edges are **two long strips** marked
  **+ (red)** and **− (blue)**. These **run the long way down the board** (the *opposite*
  direction from the little five-hole rows) and are used to carry **power (+)** and
  **ground (−)** to anywhere on the board.
- So to build a circuit you plug parts into holes that share the right strips, and use
  short jumper wires to join the strips you want connected. A schematic tells you *what*
  should connect; the breadboard is *where* you actually make it connect.

> Picture: a breadboard is like a **parking lot painted with rows of spaces** — cars in the
> same painted row are "together," and a painted line (the center gap) keeps the two halves
> apart. The long curb lanes around the edge are the power rails everyone can reach.

---

## Sources (all free; fetched & verified)

- **PhET Circuit Construction Kit: DC** — phet.colorado.edu/en/simulations/circuit-construction-kit-dc (CC BY) — build a loop, break it, and watch the bulb; series & parallel hands-on with no math. **Best first tool for circuits.**
- **SparkFun (adult reference, CC BY-SA 4.0):** *What is a Circuit?* — learn.sparkfun.com/tutorials/what-is-a-circuit/all — a circuit is a complete loop; open vs closed; short circuit.
- **SparkFun: Series and Parallel Circuits** — learn.sparkfun.com/tutorials/series-and-parallel-circuits/all — one path vs many paths; distilled to the kid level (the math is left out on purpose).
- **SparkFun: How to Read a Schematic** — learn.sparkfun.com/tutorials/how-to-read-a-schematic/all — symbols, lines = wires, junction dots = real connections.
- **SparkFun: How to Use a Breadboard** — learn.sparkfun.com/tutorials/how-to-use-a-breadboard/all — five-hole rows on each side of the center gap; long +/− power rails along the edges.
- **Ducksters (as needed)** — ducksters.com/science/physics — supporting kid-level background on current and circuits.
