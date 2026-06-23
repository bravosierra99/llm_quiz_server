# Signals & Sensors — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the **Signals & Sensors** concept area of
**Arduino Foundations**. Written to be *true* even though it's simple — every analogy
below (a dimmer switch, blinking-too-fast-to-see) is a way to picture a real fact, not a
replacement for it. Facts are synthesised from the vetted free resources listed at the
end; nothing is copied verbatim.

**How to use it:** this is the adult/teacher reference and the source the quiz questions
are drawn from. Pair it with hands-on tools — flick a real light switch (digital), slide a
real dimmer (analog), watch an LED dim on PWM — so she *sees* it. This area needs Area A
(electricity) and Area C (components like LEDs and resistors) first.

---

## D1 — Input vs Output (the board's senses and its actions)

A microcontroller board (like the Arduino) is the "brain" of a project. To be useful, a
brain needs two things: a way to **sense** the world, and a way to **do** things in the
world.

- **Input = the board SENSES the world.** Information comes *in* to the board.
  - Example: a **button** — when you press it, the board can tell.
  - Example: a **light sensor** — the board can tell if the room is bright or dark.
- **Output = the board DOES something in the world.** The board sends signals *out*.
  - Example: an **LED** — the board can turn the light on or off.
  - Example: a **buzzer** — the board can make a sound; a **motor** — the board can make
    something spin.
- A whole project is usually **input → think → output**: the board reads an input,
  decides what to do, then drives an output. (Press the button *(input)* → light the LED
  *(output)*.)
- The same physical pin on the board can be set up as an input **or** an output, but for
  one job it does one or the other. You tell the board which one in your program.

> Picture: **input** is the board's *eyes and ears*; **output** is its *hands and voice*.

---

## D2 — Digital vs Analog (two values, or a smooth range)

Signals are how information travels as electricity. There are two big kinds:

- **Digital = only two values: ON or OFF** (also called HIGH/LOW or 1/0). Like a normal
  **light switch** — it's either up or down, nothing in between.
  - A **button** is digital: pressed or not pressed.
  - The board makes a digital output by putting the pin at **full voltage (ON)** or at
    **zero (OFF)** — for the Arduino UNO that's 5 volts or 0 volts.
- **Analog = a smooth range of many values**, not just two. Like a **dimmer switch** or a
  **volume knob** — it can be anywhere from all-the-way-down to all-the-way-up, and every
  amount in between.
  - The brightness of the room, the temperature, how far you slide a knob — these are
    naturally analog: they vary smoothly.
- So: **digital is like steps you can count on one hand (just 2);** **analog is like a
  ramp** you can stop anywhere along.
- The world outside is mostly analog (smooth). Computers think in digital (on/off). A big
  job of a sensor circuit is turning analog things into numbers the board can use (see D4).

> Picture: a staircase with only a top step and a bottom step = **digital**. A smooth ramp
> = **analog**.

---

## D3 — PWM: fake-analog by blinking very fast

Here's a puzzle: a digital output can only be **ON or OFF** — so how can the board make an
LED look *half* bright, or run a motor at *half* speed? The trick is **PWM**, which stands
for **Pulse-Width Modulation**. (You don't need the long name — "blink fast" is the idea.)

- **PWM means switching the pin ON and OFF very fast, over and over.** Each time it turns
  ON, it's still **full voltage** — PWM does *not* turn the voltage down. It just controls
  **how much of the time** the pin spends ON versus OFF.
- **More ON-time = more average power = brighter LED / faster motor.** Less ON-time =
  dimmer / slower.
  - ON half the time → about half as bright.
  - ON most of the time → almost full bright.
- Your eyes can't see the blinking because it happens **so fast** (hundreds of times a
  second) — it just looks like a steady, in-between brightness. (Same reason a fast-spinning
  fan looks like a blur.)
- On the Arduino you set PWM with a number **from 0 to 255**:
  - **0** = always OFF (off / stopped).
  - **255** = always ON (full bright / full speed).
  - A number in the middle, like 128, means ON about half the time (about half bright).
- This is called **"fake-analog"** because the *result* looks smooth and in-between, even
  though the pin is really only ever fully ON or fully OFF.

> Picture: flick a light switch on-off-on-off faster than you can see. If you leave it ON
> longer each time, the room *looks* brighter on average — even though the bulb is only
> ever fully on or fully off.

---

## D4 — Sensors: turning the world into numbers

A **sensor** is a part that **changes something physical (light, heat, distance, tilt)
into electricity** the board can measure — and the board turns that into a **number**. That
number is what your program reads and reacts to.

- **Light → a photocell (photoresistor).** A photocell's **resistance changes with light:**
  bright light makes its resistance go **down**; darkness makes it go **up**. The circuit
  turns that changing resistance into a changing voltage, and the board reads it as a
  number — so the board can tell *how bright* the room is.
- **Temperature → a thermistor.** A thermistor is a special resistor whose **resistance
  changes with temperature.** As it gets warmer or cooler, its resistance changes in a
  known way, so the board can work out the temperature as a number.
- **Distance → an ultrasonic sensor (echo).** It sends out a quick **sound pulse too
  high-pitched for us to hear**, then listens for the **echo** bouncing back off an object.
  **The longer the echo takes to come back, the farther away the object is** (sound travels
  at a steady speed, so time tells you distance). This is the same trick bats use —
  **echolocation.**
- **Tilt → a tilt switch.** Inside is a tiny ball; when you **tip** the part, the ball
  rolls and either **closes or opens** a little circuit. A tilt switch is **digital** — it
  only says "tipped" or "not tipped" (two values), unlike the photocell, thermistor, and
  ultrasonic sensor, which give a **range** of values.
- The board reads an analog (range) sensor as a number on a scale — on the Arduino UNO,
  **analog inputs come in as a number from 0 to 1023** (this is a different scale from the
  0–255 used for PWM *output* — don't mix them up). A small number means a small reading; a
  big number means a big reading.

> Picture: a sensor is a **translator** that turns "the world" (bright/dark, hot/cold,
> near/far, tipped/flat) into a **number the board understands.**

---

## Sources (all free; from the vetted resource list)

- **SparkFun — Analog vs Digital** — learn.sparkfun.com/tutorials/analog-vs-digital/all
  (CC BY-SA, *adult-read*) — digital = two values, analog = a smooth range (D2; also the
  closest vetted reference for the PWM "blink fast" idea, D3).
- **SparkFun — Analog-to-Digital Conversion** —
  learn.sparkfun.com/tutorials/analog-to-digital-conversion/all (CC BY-SA, *adult-read*) —
  how an analog reading becomes a number on a 0–1023 scale (D4).
- **SparkFun — Photocell overview** —
  learn.sparkfun.com/tutorials/photocell-hookup-guide/photocell-overview (CC BY-SA) — a
  photocell's resistance changes with light (D4).
- **CK-12 — What are thermistors?** —
  ck12.org/flexi/physical-science/electronic-component/what-are-thermistors-in-physics/ —
  a thermistor's resistance changes with temperature (D4).
- **NPS — Echolocation** — nps.gov/subjects/bats/echolocation.htm (US-gov public domain) —
  sound bounces back as an echo; the idea behind the ultrasonic distance sensor (D4).
