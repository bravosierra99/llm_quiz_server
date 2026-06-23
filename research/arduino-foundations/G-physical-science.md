# Physical Science Behind the Sensors — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the **physical science** that makes the Arduino kit's
sensors and outputs work — light, sound, heat, echoes, and magnetism. Written to be *true*
even though it's simple: every analogy here is a way to picture a real fact, not a
replacement for it. Facts are synthesised from the vetted free resources at the end;
nothing is copied verbatim.

**How to use it:** this is the adult/teacher reference and the source the quiz questions are
drawn from. Pair it with the hands-on tools — **PhET Color Vision** (mixing light),
**PhET Sound Waves** (frequency → pitch), and **PhET Magnets & Electromagnets** — so she
*sees* and *hears* it.

---

## G1 — Light (LEDs, photocells, color, infrared)

- **Light is a kind of energy that travels.** It zooms in straight lines, and it is the
  **fastest thing there is** — fast enough to go all the way around the Earth many times in
  one second. (That's why you see a faraway lightning flash before you hear its thunder:
  light gets to you almost instantly, but sound is much slower.)
- An **LED** (light-emitting diode) is a tiny part that **makes light** when electricity
  flows through it. Lots of the kit's lessons blink LEDs.
- A **photocell** (also called a light sensor or LDR) does the opposite — it **senses
  light**. It changes how much it resists electric current depending on how bright it is, so
  the Arduino can "tell" if a room is light or dark.
- **Mixing colored light:** screens and the kit's **RGB LED** make every color by mixing
  just **three** colors of light: **red, green, and blue**.
  - Red light + green light + blue light, all together and bright, look **white**.
  - Red light + green light (no blue) make **yellow**.
  - Turn them all **off** and you get **black** (no light).
  - This is *mixing light*, which is different from mixing paint. With **paint**, mixing more
    colors makes things darker; with **light**, adding more colors makes things **brighter**.
- **Infrared (IR) is light we can't see.** Our eyes only see a small band of light called
  "visible light." Just past the red end is **infrared** — real light, but invisible to us.
  - TV **remotes** and the kit's **IR remote** send messages as quick blinks of infrared
    light. The IR receiver on the board "sees" those invisible blinks and decodes them.

> Picture: light is like an invisible super-fast messenger. An LED is a tiny flashlight that
> sends it; a photocell is a tiny eye that notices it.

---

## G2 — Sound (vibration, pitch, frequency, buzzers)

- **Sound is made when something vibrates** — wiggles back and forth very fast. The wiggling
  pushes on the air around it, and that push travels to your ears as sound. No vibration,
  no sound.
- You can feel this: gently touch your throat while you hum — you feel it **buzzing**. That
  buzzing *is* the vibration making the sound.
- **Pitch** is how **high or low** a sound is (a tiny bird's tweet is high; a big drum is
  low).
- **Faster vibration → higher pitch.** Slower vibration → lower pitch.
- We measure how fast something vibrates as its **frequency** — the number of wiggles each
  second. Frequency is measured in **hertz (Hz)**: 1 Hz means 1 wiggle per second, so
  **higher frequency = higher pitch**.
- A **buzzer** makes sound by **vibrating**. In the kit:
  - An **active buzzer** has its own vibrating part built in — give it power and it just
    beeps at one pitch.
  - A **passive buzzer** vibrates at whatever **frequency** the Arduino tells it to, so you
    can play different notes (different pitches) by choosing different frequencies.

> Picture: sound starts as a wiggle. Wiggle fast for a squeaky high note, wiggle slow for a
> deep low note.

---

## G3 — Heat & Temperature (molecules, heat flow, thermistors)

- Everything is made of tiny particles called **molecules** (and atoms), and they are always
  **jiggling and moving** — even in things that look perfectly still.
- **Temperature tells you how fast those molecules are moving (their jiggling energy).**
  - **Hotter = molecules moving faster.**
  - **Colder = molecules moving slower.**
- **Heat always flows from hotter things to colder things** — never the other way on its own.
  That's why a warm cookie cools down in a cool room, and why an ice cube in your hand makes
  your hand feel cold (heat flows *out* of your hand into the ice).
- We measure temperature with a **thermometer**. The kit uses electronic temperature sensors:
  - A **thermistor** is a part whose **resistance changes when its temperature changes**. The
    Arduino measures that resistance and works out the temperature from it.
  - The kit's **DHT11** sensor measures both **temperature** and **humidity** (how much water
    vapor is in the air).

> Picture: temperature is a speedometer for jiggling molecules. Heat is the warmth that
> always slides "downhill," from hot toward cold.

---

## G4 — Sound Waves & Echo (measuring distance with ultrasonic)

- Sound travels through the air as a **wave** — a moving pattern of pushes and pulls in the
  air, spreading out from whatever is vibrating, a bit like ripples spreading on a pond.
- **Sound is much slower than light.** Sound travels about **340 meters every second** in
  air — fast, but you can almost picture it moving. (Light is almost a million times faster.)
- When a sound wave hits a hard surface, it can **bounce back**. A bounced-back sound is an
  **echo** (like shouting in a tunnel and hearing yourself again a moment later).
- Animals and machines use echoes to "see" with sound, called **echolocation**:
  - **Bats** squeak and listen for the echoes bouncing off bugs and walls to fly in the dark.
  - Dolphins do it underwater.
- The kit's **ultrasonic distance sensor** works the same way. *Ultrasonic* means sound too
  high-pitched for people to hear. The sensor:
  1. Sends out a quick **chirp** of ultrasonic sound.
  2. **Times** how long the echo takes to come back.
  3. Because sound travels at a known speed, **a longer time means the object is farther
     away** — so the Arduino can turn that time into a **distance**.

> Picture: it's like clapping in a canyon with a stopwatch — the longer you wait for the
> echo, the farther away the wall must be.

---

## G5 — Magnetism & Electromagnets (how motors and relays move)

- A **magnet** pulls on certain metals — especially **iron** (and steel, which is mostly
  iron). It does **not** pull on most other materials, like plastic, wood, copper, or
  aluminum.
- Every magnet has **two ends called poles: a North (N) and a South (S).**
  - **Opposite poles attract** (N pulls toward S).
  - **Same poles repel** (N pushes away N; S pushes away S).
  - (This pull-and-push rule is a lot like the +/− charges in electricity.)
- **Electricity and magnetism are connected.** When electric current flows through a wire, it
  makes a small magnetic field around the wire.
- An **electromagnet** uses that fact: wind the wire into a **coil**, run current through it,
  and the coil becomes a **magnet you can switch on and off**.
  - Turn the current **on** → it's magnetic. Turn it **off** → the magnetism goes away.
- This is how the kit's moving parts work:
  - A **motor** (DC, servo, or stepper) spins because electromagnets **push and pull** on
    magnets inside it, turning electricity into motion.
  - A **relay** is a switch moved by an electromagnet: a tiny current energizes the coil,
    and the coil's pull flips a switch to turn a much bigger circuit on or off.

> Picture: an electromagnet is a magnet with an on/off button. Flip current on, it grabs;
> flip it off, it lets go — and that grabbing is what makes motors spin and relays click.

---

## Sources (all free; from the vetted resource list)

- **PhET Color Vision** — phet.colorado.edu/en/simulations/color-vision (CC BY) — mixing red,
  green & blue light (G1, RGB LED).
- **PhET Sound Waves** — phet.colorado.edu/en/simulations/sound-waves (CC BY) — change the
  frequency, hear the pitch change (G2, passive buzzer).
- **Explain That Stuff — Sound** — explainthatstuff.com/sound.html — "Sound is the energy
  things produce when they vibrate" (G2).
- **Ducksters — Heat** — ducksters.com/science/heat.php — temperature = how fast molecules
  move; heat flows hot → cold (G3).
- **NPS — Echolocation** — nps.gov/subjects/bats/echolocation.htm (US-gov public domain) —
  bats time the echo of their calls to locate things; the ultrasonic-sensor idea (G4).
- **PhET Magnets & Electromagnets** — phet.colorado.edu/en/simulations/magnets-and-electromagnets
  (CC BY) — a battery + coil makes an electromagnet; the basis of motors & relays (G5).
- **(adult-read)** SparkFun, CC BY-SA 4.0: *Photocell hookup guide* (light changes
  resistance, G1) and *Motors* ("What makes a motor move? …magnetism!", G5).
