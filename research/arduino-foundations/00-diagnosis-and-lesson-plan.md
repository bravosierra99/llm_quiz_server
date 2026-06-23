# Arduino Foundations — Prerequisite Diagnosis & Lesson Plan

**Goal:** Get a smart 8-year-old (target a 6th-grade ceiling) to the point where the
**25 Elegoo Super Starter Kit (UNO) lessons** make sense — the *concepts behind* the
lessons, not the wiring steps. Built from the Elegoo manual's actual content
(Lessons 0–24) plus the science/programming each lesson silently assumes.

This is the **diagnosis** (what she needs to know) and the **ordered lesson plan**
(prerequisites first). Vetted free resources are added per concept area below.

---

## What the kit actually teaches (Lessons 0–24)

| # | Lesson | Concepts it leans on |
|---|--------|----------------------|
| 0 | Installing IDE | what a program/IDE is |
| 1 | Libraries & Serial Monitor | programs, libraries, serial communication |
| 2 | Blink | circuit, digital output, delay/time (ms), setup/loop |
| 3 | LED | current-limiting resistor, Ohm's law, polarity |
| 4 | RGB LED | mixing light (color), PWM, analogWrite, functions |
| 5 | Digital Inputs (button) | input vs output, pull-up/pull-down, if-statements, digital signal |
| 6 | Active buzzer | sound from electricity, digital output |
| 7 | Passive buzzer | sound = frequency/tone, loops |
| 8 | Tilt ball switch | switches, gravity/orientation, digital input |
| 9 | Servo | motors→motion, angle, PWM control signal, libraries |
| 10 | Ultrasonic sensor | sound waves, echo, distance = speed×time, analog→number |
| 11 | DHT11 temp/humidity | temperature, humidity, sensors→data |
| 12 | Analog joystick | analog signal, analogRead, ranges (0–1023), coordinates |
| 13 | IR receiver | infrared light, encoding/decoding signals |
| 14 | LCD display | output devices, characters, libraries |
| 15 | Thermometer (thermistor) | resistance changes with temperature, analog read |
| 16 | 8 LED with 74HC595 | shift register, **binary**, bits, saving pins |
| 17 | Serial Monitor | variables, data, debugging, communication |
| 18 | Photocell | light→resistance, analog sensing |
| 19 | 74HC595 + segment display | binary, bit patterns, encoding digits |
| 20 | 4-digit 7-segment | multiplexing, binary, loops, timing |
| 21 | DC motors | electricity→motion, magnetism, transistor as switch, current |
| 22 | Relay | electromagnet, switching big loads with a small signal |
| 23 | Stepper motor | electromagnets in sequence, precise steps |
| 24 | Stepper + IR remote | combining input (IR) + output (motor) |

---

## Concept areas (prerequisite-ordered tree)

The lesson plan is an **ordered progression**, not a bag of topics. Later areas
depend on earlier ones. Areas with `· L1/L2` have two difficulty levels — L1 is the
first-pass "smart 8-year-old" version; L2 pushes toward the 6th-grade ceiling.

### A. Electricity Basics  *(foundation — everything needs this)*
- **A1.** Atoms, charge, electrons (+ and −) — *L1*
- **A2.** Current = flow of charge; Voltage = the "push"; Resistance = how hard it is to flow
  (water-in-pipes analogy) — *L1/L2*
- **A3.** Conductors vs insulators — *L1*
- **A4.** Ohm's law (V, I, R relate; more voltage → more current; more resistance → less)
  — *L2, qualitative only*
- **A5.** Units & prefixes: volt, amp, ohm, milli- (mA, ms) — *L1*

### B. Circuits  *(needs A)*
- **B1.** A circuit is a complete loop: source → wire → load → back — *L1*
- **B2.** Polarity, +/−, ground (GND) — *L1*
- **B3.** Series vs parallel — *L2*
- **B4.** Reading a simple schematic; breadboard basics (how rows connect) — *L1 practical*

### C. Components  *(needs A, B)*
- **C1.** Resistor — limits current (protects the LED) — *L1*
- **C2.** LED / diode — one-way light, has polarity — *L1*
- **C3.** Capacitor — stores a little charge — *L2 (kit has them; manual doesn't dwell)*
- **C4.** Switch, transistor & relay — *switching*: a small signal controls a bigger one — *L2*
- **C5.** Buzzer / speaker — electricity → sound — *L1*
- **C6.** Motors (DC, servo, stepper) — electricity + magnetism → motion — *L2*

### D. Signals & Sensors  *(needs A, C)*
- **D1.** Input vs output — *L1*
- **D2.** Digital (on/off) vs analog (a range) signals — *L1/L2*
- **D3.** PWM — fake-analog by blinking fast (brightness, speed) — *L2*
- **D4.** Sensors turn the world into numbers: light (photocell), temperature
  (thermistor), distance (ultrasonic echo), tilt — *L1/L2*

### E. Programming Basics  *(parallel track — needed from Lesson 0)*
- **E1.** What a program / algorithm is (precise step-by-step instructions) — *L1*
- **E2.** Sequence + the Arduino `setup()` runs once / `loop()` repeats forever — *L1*
- **E3.** Variables & data types (a labeled box that holds a number; `int`) — *L1/L2*
- **E4.** Functions (a named action you can call, with inputs) — *L2*
- **E5.** Conditionals — `if` / `else` make decisions — *L1/L2*
- **E6.** Loops — repeat with `for` / `while` — *L2*
- **E7.** Comparison & operators (=, ==, >, <) — *L2*

### F. Numbers for electronics  *(needs A5; supports D, E)*
- **F1.** Time in milliseconds; `delay()` — *L1*
- **F2.** Binary & bits — on/off counting (why 8 LEDs = 1 byte; segment displays) — *L2*
- **F3.** Ranges & mapping: 0–255 (PWM), 0–1023 (analogRead) — *L2*

### G. Physical science behind the sensors  *(needs A; interleaves with D)*
- **G1.** Light — emitting (LED) & sensing (photocell), color mixing, infrared — *L1/L2*
- **G2.** Sound — vibration & frequency (pitch); buzzers/tone — *L1/L2*
- **G3.** Heat & temperature — *L1*
- **G4.** Sound waves & echo → measuring distance (ultrasonic) — *L2*
- **G5.** Magnetism & electromagnets — how motors & relays move — *L2*

---

## Teaching order (the actual plan)

1. **E1–E2** (what a program is) + **A1–A3** (electricity) — start both tracks gently.
2. **A4–A5, B1–B2** (circuits & units) — enough to understand Blink (L2) & LED (L3).
3. **C1–C2** (resistor, LED) + **F1** (ms/delay) — Lessons 2–3 fully make sense.
4. **E3, E5, D1–D2** (variables, if, input/output, digital vs analog) — Lessons 4–8.
5. **D3 (PWM), E4, G1–G2** (functions, light, sound) — Lessons 4, 6–7, 9.
6. **D4, G3–G4, F3** (sensors, heat, echo, ranges) — Lessons 10–15, 18.
7. **F2 (binary), E6** (loops) — Lessons 16, 19–20.
8. **C4, C6, G5, B3, C3** (switching, motors, magnetism, series/parallel, caps) — Lessons 21–24.

Coverage check: every Elegoo lesson maps to ≥1 area in §"What the kit teaches".

---

## Teach-from maps  *(plan step → exact resource → quiz)*

Each concept code below tells you **where to actually teach it**. "Play/build" = a
hands-on sim she drives; "read" = a short page (you can read it aloud); "(you explain)"
= an adult-level reference you teach *from*. After each concept, the matching quiz
sub-topic in the app reinforces it. **All seven areas (A–G) are built** — each area's
teach-from table is below, in teaching order.

### Area A — Electricity Basics

| Concept | What she learns (one line) | Teach it with | Then quiz |
|---|---|---|---|
| **A1** charge & electrons | atoms have + protons and − electrons; current = electrons moving | **Play:** [PhET Build an Atom](https://phet.colorado.edu/en/simulations/build-an-atom) · **Read:** [Ducksters: Electric Current](https://www.ducksters.com/science/physics/electric_current.php) | *What Electricity Is* |
| **A2** current · voltage · resistance | the water-pipe trio (flow / push / narrow pipe) | **Build:** [PhET Circuit Construction Kit: DC](https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc) · **(you explain):** [SparkFun water-analogy table](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law/all) | *Current, Voltage & Resistance* |
| **A3** conductors & insulators | metal lets current flow; rubber/plastic don't | **Read:** [Ducksters: Conductors & Insulators](https://www.ducksters.com/science/physics/electrical_conductors_and_insulators.php) · **Try:** in PhET CCK, swap a wire for an eraser | *Conductors & Insulators* |
| **A4** Ohm's law (qualitative) | more push → more current; more resistance → less | **Read:** [Ducksters: Ohm's Law](https://www.ducksters.com/science/physics/ohms_law.php) · **Build:** in PhET CCK change the battery/resistor and watch the current meter | *Ohm's Law* |
| **A5** units (V, A, Ω, milli) | volt/amp/ohm; milli = 1/1000; 5 V board, ~20 mA LED, 1000 ms = 1 s | **(you explain):** [SparkFun V/I/R](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law/all) (units & mA) · **Read:** [Adafruit Blink](https://learn.adafruit.com/adafruit-arduino-lesson-1-blink/how-blink-works) for milliseconds | *Units: Volts, Amps & Ohms* |

### Area B — Circuits

| Concept | Teach it with | Then quiz |
|---|---|---|
| **B1** a circuit is a complete loop | **Build:** [PhET CCK: DC](https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc) (build a loop, then break it) · **(you explain):** [SparkFun: What is a Circuit?](https://learn.sparkfun.com/tutorials/what-is-a-circuit/all) | *What a Circuit Is* |
| **B2** polarity, +/−, ground (0 V reference) | **Build:** [PhET CCK: DC](https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc) · **(you explain):** [SparkFun: What is a Circuit?](https://learn.sparkfun.com/tutorials/what-is-a-circuit/all) | *Polarity & Ground* |
| **B3** series vs parallel (one path vs many) | **Build:** [PhET CCK: DC](https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc) (break one bulb in each) · **(you explain):** [SparkFun: Series & Parallel](https://learn.sparkfun.com/tutorials/series-and-parallel-circuits/all) | *Series vs Parallel* |
| **B4** schematics & breadboards | **(you explain):** [SparkFun: Read a Schematic](https://learn.sparkfun.com/tutorials/how-to-read-a-schematic/all) + [Use a Breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard/all) | *Schematics & Breadboards* |

### Area C — Components

| Concept | Teach it with | Then quiz |
|---|---|---|
| **C1** resistor — limits current | **Read:** [Build Electronic Circuits — What is a resistor?](https://www.build-electronic-circuits.com/what-is-a-resistor/) (the LED-burns-out story) | *Resistors* |
| **C2** LED / diode — one-way, polarity | **Read:** [Explain That Stuff — Diodes & LEDs](https://www.explainthatstuff.com/diodes.html) | *LEDs & Diodes* |
| **C3** capacitor — stores a little charge | **Play:** [PhET Capacitor Lab: Basics](https://phet.colorado.edu/en/simulations/capacitor-lab-basics) | *Capacitors* |
| **C4** switch / transistor / relay — small controls big | **Read:** [Explain That Stuff — How relays work](https://www.explainthatstuff.com/howrelayswork.html) · **(you explain):** [SparkFun Transistors](https://learn.sparkfun.com/tutorials/transistors/introduction) | *Switches, Transistors & Relays* |
| **C5** buzzer / speaker — electricity → vibration → sound | **Build:** [Exploratorium — Cup Speaker](https://www.exploratorium.edu/snacks/cup-speaker) | *Buzzers & Speakers* |
| **C6** motors — electricity + magnetism → motion | **Play:** [PhET Magnets & Electromagnets](https://phet.colorado.edu/en/simulations/magnets-and-electromagnets) · **(you explain):** [SparkFun Motors](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all) | *Motors* |

### Area D — Signals & Sensors

| Concept | Teach it with | Then quiz |
|---|---|---|
| **D1** input vs output | **(you explain):** [SparkFun: Analog vs Digital](https://learn.sparkfun.com/tutorials/analog-vs-digital/all) · **Try:** button lights an LED on the kit | *Input vs Output* |
| **D2** digital vs analog | **(you explain):** [SparkFun: Analog vs Digital](https://learn.sparkfun.com/tutorials/analog-vs-digital/all) · **Try:** light switch (digital) vs dimmer/volume knob (analog) | *Digital vs Analog* |
| **D3** PWM (fake-analog) | **Try:** watch an LED dim on a `~` PWM pin (`analogWrite` 0→255) · **(you explain):** [SparkFun: Analog vs Digital](https://learn.sparkfun.com/tutorials/analog-vs-digital/all) *(no dedicated kid PWM resource exists — this is the closest vetted page)* | *PWM (Fake-Analog)* |
| **D4** sensors → numbers | **Read:** [SparkFun Photocell](https://learn.sparkfun.com/tutorials/photocell-hookup-guide/photocell-overview) · [CK-12 Thermistors](https://www.ck12.org/flexi/physical-science/electronic-component/what-are-thermistors-in-physics/) · [NPS Echolocation](https://www.nps.gov/subjects/bats/echolocation.htm) · **(you explain):** [SparkFun ADC](https://learn.sparkfun.com/tutorials/analog-to-digital-conversion/all) (the 0–1023 number) | *Sensors: Turning the World into Numbers* |

### Area E — Programming Basics

| Concept | Teach it with | Then quiz |
|---|---|---|
| **E1** what a program/algorithm is | **Read:** [Simple English Wikipedia — Algorithm](https://simple.wikipedia.org/wiki/Algorithm) | *What a Program Is* |
| **E2** sequence + `setup()`/`loop()` | **Read:** [Adafruit — How "Blink" Works](https://learn.adafruit.com/adafruit-arduino-lesson-1-blink/how-blink-works) | *Setup & Loop* |
| **E3** variables & data types | **Read/Play:** [Scratch Wiki — Variable](https://en.scratch-wiki.info/wiki/Variable) | *Variables & Data Types* |
| **E4** functions | **Read:** [Scratch Wiki — My Blocks](https://en.scratch-wiki.info/wiki/My_Blocks) · **Play:** [Blockly Games — Music](https://blockly.games/music) | *Functions* |
| **E5** if / else | **Play:** [Blockly Games — Maze](https://blockly.games/maze) · **Read:** [Scratch Wiki — Control Blocks](https://en.scratch-wiki.info/wiki/Control_Blocks) | *If / Else (Making Decisions)* |
| **E6** loops (for / while) | **Play:** [Blockly Games — Maze](https://blockly.games/maze) · **Read:** [Scratch Wiki — Control Blocks](https://en.scratch-wiki.info/wiki/Control_Blocks) | *Loops (Repeating)* |
| **E7** comparing & operators | **Read/Play:** [Scratch Wiki — Operators Blocks](https://en.scratch-wiki.info/wiki/Operators_Blocks) | *Comparing & Operators* |

### Area F — Numbers for Electronics

| Concept | Teach it with | Then quiz |
|---|---|---|
| **F1** time in milliseconds | **Read:** [Adafruit — How "Blink" Works](https://learn.adafruit.com/adafruit-arduino-lesson-1-blink/how-blink-works) | *Time in Milliseconds* |
| **F2** binary & bits | **Play:** [CS Unplugged — Binary "Count the Dots"](https://classic.csunplugged.org/activities/binary-numbers/) ([PDF](https://classic.csunplugged.org/documents/activities/binary-numbers/unplugged-01-binary_numbers.pdf)) | *Binary & Bits* |
| **F3** number ranges & mapping | **(you explain):** [SparkFun — Analog-to-Digital Conversion](https://learn.sparkfun.com/tutorials/analog-to-digital-conversion/all) | *Number Ranges & Mapping* |

### Area G — Physical Science Behind the Sensors

| Concept | Teach it with | Then quiz |
|---|---|---|
| **G1** light — emit/sense, RGB mixing, infrared | **Play:** [PhET Color Vision](https://phet.colorado.edu/en/simulations/color-vision) · **(you explain):** [SparkFun Photocell](https://learn.sparkfun.com/tutorials/photocell-hookup-guide/photocell-overview) | *Light* |
| **G2** sound — vibration, pitch, frequency | **Play:** [PhET Sound Waves](https://phet.colorado.edu/en/simulations/sound-waves) · **Read:** [Explain That Stuff — Sound](https://www.explainthatstuff.com/sound.html) | *Sound* |
| **G3** heat & temperature | **Read:** [Ducksters — Heat](https://www.ducksters.com/science/heat.php) | *Heat & Temperature* |
| **G4** sound waves & echo → distance | **Read:** [NPS — Echolocation](https://www.nps.gov/subjects/bats/echolocation.htm) | *Sound Waves & Echo* |
| **G5** magnetism & electromagnets | **Play:** [PhET Magnets & Electromagnets](https://phet.colorado.edu/en/simulations/magnets-and-electromagnets) · **(you explain):** [SparkFun Motors](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all) | *Magnetism & Electromagnets* |

**Suggested rhythm per concept:** play/read the resource together (10–15 min) → talk
through one analogy → take that sub-topic's quiz in the app → move on. The app's spaced
repetition will bring back anything she misses.

---

## Vetted free resources

*(Filled in after each candidate is actually fetched & checked for: resolves · free /
openly licensed · age-appropriate ≤ grade 6. Dead/paywalled/too-advanced rejected.)*

Every link below was **fetched and confirmed this session** (resolves · free · at-level),
with a verifying quote. Resources marked **(adult-read)** run a bit above grade 6 in
prose — use them as *your* source to explain from, not as her reading. Two excellent
libraries — **CK-12** and **BBC Bitesize** — block automated fetching, so they're listed
under "Check in a browser" rather than as verified; they're worth a manual look.

### A–B. Electricity & Circuits
- **[PhET — Circuit Construction Kit: DC](https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc)** — *interactive sim · free, CC BY · grade 4+ hands-on* — drag-and-drop batteries, bulbs, resistors; covers series, parallel & Ohm's law with no math. **Best first tool for circuits.**
- **[PhET — Build an Atom](https://phet.colorado.edu/en/simulations/build-an-atom)** — *interactive sim · free, CC BY · grade 4+* — add/remove protons & electrons, watch charge change. Makes +/− concrete (A1).
- **[Ducksters — Electric Current](https://www.ducksters.com/science/physics/electric_current.php)** — *website · free · grade 4–6* — current as flowing charge, water-in-pipes. "…thought of like the flowing of water through a pipe."
- **[Ducksters — Ohm's Law](https://www.ducksters.com/science/physics/ohms_law.php)** — *website · free · grade 5–6* — voltage=pressure, resistance=pipe width, qualitative (A4).
- **[Ducksters — Conductors & Insulators](https://www.ducksters.com/science/physics/electrical_conductors_and_insulators.php)** — *website · free · grade 4–6* — copper vs rubber (A3).
- **(adult-read)** SparkFun, CC BY-SA 4.0 — the canonical clear explanations to teach from: [What is Electricity?](https://learn.sparkfun.com/tutorials/what-is-electricity/all) · [Voltage, Current, Resistance & Ohm's Law](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law/all) (the gold water-analogy table) · [What is a Circuit?](https://learn.sparkfun.com/tutorials/what-is-a-circuit/all) · [Series & Parallel](https://learn.sparkfun.com/tutorials/series-and-parallel-circuits/all) · [How to Read a Schematic](https://learn.sparkfun.com/tutorials/how-to-read-a-schematic/all) · [How to Use a Breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard/all).

### C. Components
- **[PhET — Capacitor Lab: Basics](https://phet.colorado.edu/en/simulations/capacitor-lab-basics)** — *sim · free, CC BY · grade 5+* — charges build up on plates (C3).
- **[PhET — Magnets & Electromagnets](https://phet.colorado.edu/en/simulations/magnets-and-electromagnets)** — *sim · free, CC BY · grade 4+* — battery + coil = electromagnet; the basis of motors & relays (C6, G5).
- **[Explain That Stuff — Diodes & LEDs](https://www.explainthatstuff.com/diodes.html)** — *website · free · grade 5–7* — "a diode is the electrical equivalent of a one-way street" (C2).
- **[Explain That Stuff — How relays work](https://www.explainthatstuff.com/howrelayswork.html)** — *website · free · grade 5–7* — "switch it on with a tiny current and it switches on … a much larger electric current" (C4).
- **[Build Electronic Circuits — What is a resistor?](https://www.build-electronic-circuits.com/what-is-a-resistor/)** — *website · free · grade 5–6* — the LED-burned-out story; resistor protects the LED (C1). **Flagship Arduino concept.**
- **[Exploratorium — Cup Speaker (Science Snack)](https://www.exploratorium.edu/snacks/cup-speaker)** — *hands-on activity · free · grade 4–6* — build a speaker: electricity → sound (C5).
- **(adult-read)** SparkFun CC BY-SA 4.0: [Transistors intro](https://learn.sparkfun.com/tutorials/transistors/introduction) (C4) · [Capacitors](https://learn.sparkfun.com/tutorials/capacitors/all) · [Motors](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all) ("What makes a motor move? …magnetism!").

### D + G. Signals, Sensors & the physical science behind them
- **[PhET — Color Vision](https://phet.colorado.edu/en/simulations/color-vision)** — *sim · free, CC BY · grade 4+* — mix red/green/blue light (G1, RGB LED).
- **[PhET — Sound Waves](https://phet.colorado.edu/en/simulations/sound-waves)** — *sim · free, CC BY · grade 4+* — change frequency → change pitch (G2, buzzer).
- **[Explain That Stuff — Sound](https://www.explainthatstuff.com/sound.html)** — *website · free · grade 5–7* — "Sound is the energy things produce when they vibrate" (G2).
- **[Ducksters — Heat](https://www.ducksters.com/science/heat.php)** — *website · free · grade 5–6* — temperature = how fast molecules move (G3).
- **[NPS — Echolocation](https://www.nps.gov/subjects/bats/echolocation.htm)** — *website · free, US-gov public domain · grade 4–6* — sound bounces back = the ultrasonic-sensor idea (G4).
- **[SparkFun — Photocell overview](https://learn.sparkfun.com/tutorials/photocell-hookup-guide/photocell-overview)** — *website · free, CC BY-SA · grade 6* — light changes resistance (D4, photocell).
- **[CK-12 — What are thermistors?](https://www.ck12.org/flexi/physical-science/electronic-component/what-are-thermistors-in-physics/)** — *website · free · grade 6–7* — resistance changes with temperature (D4, thermometer).
- **(adult-read)** [SparkFun — Analog vs Digital](https://learn.sparkfun.com/tutorials/analog-vs-digital/all) (D2) · [Analog-to-Digital Conversion](https://learn.sparkfun.com/tutorials/analog-to-digital-conversion/all) (0–1023 ranges, F3).

### E + F. Programming & Numbers
- **[Simple English Wikipedia — Algorithm](https://simple.wikipedia.org/wiki/Algorithm)** — *website · free, CC BY-SA · grade 4–5* — "a list of steps that can be followed to solve a problem" (E1).
- **[Adafruit — How 'Blink' Works](https://learn.adafruit.com/adafruit-arduino-lesson-1-blink/how-blink-works)** ([PDF](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-arduino-lesson-1-blink.pdf)) — *website + downloadable PDF · free · beginner* — setup-runs-once / loop-repeats / delay in ms, on real Arduino (E2, F1).
- **[Blockly Games](https://blockly.games/about?lang=en)** — *interactive · open source, free · age 8+* — Maze=loops+conditionals, Turtle=loops, Music=functions (E4–E6). **Best hands-on coding for her.**
- **[code.org — Ages 5–11](https://code.org/students)** — *interactive courses · free · age 5–11* — block-based coding gateway.
- **Scratch Wiki (CC BY-SA):** [Variables](https://en.scratch-wiki.info/wiki/Variable) (E3) · [My Blocks=functions](https://en.scratch-wiki.info/wiki/My_Blocks) (E4) · [Control Blocks=loops & if](https://en.scratch-wiki.info/wiki/Control_Blocks) (E5–E6) · [Operators](https://en.scratch-wiki.info/wiki/Operators_Blocks) (E7).
- **[CS Unplugged — Binary "Count the Dots"](https://classic.csunplugged.org/activities/binary-numbers/)** ([PDF activity](https://classic.csunplugged.org/documents/activities/binary-numbers/unplugged-01-binary_numbers.pdf)) — *downloadable PDF · CC BY-NC-SA · age 7+* — on/off cards = bits; 8 bits = a byte (F2). **Perfect for the shift-register lessons.**

### Check in a browser (great, but block automated fetch — verify manually)
- **CK-12 Foundation** physical-science flexbooks (electric circuits/current, free, CC BY-NC) — bot-blocked to the fetcher but a top-tier free middle-school option.
- **BBC Bitesize** (electricity, conductors/insulators, analogue vs digital) — crawler-blocked here; excellent UK primary/KS3 level.
- **Khan Academy** (basic electrical quantities; intro to programming) — JS-rendered, free, can't be quote-verified by fetch.

</content>
</invoke>
