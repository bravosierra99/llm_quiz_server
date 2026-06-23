# Numbers for Electronics — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the **Numbers for Electronics** area of
**Arduino Foundations**. These are the everyday numbers that show up when you start
coding the Elegoo kit: how time is counted in milliseconds, how computers count with
just on and off (binary bits), and how a sensor's reading turns into a number in a range.
Every statement here is *true* even though it's simple. Facts are synthesised from the
vetted free resources listed at the end; nothing is copied verbatim.

**How to use it:** this is the adult/teacher reference and the source the quiz questions
are drawn from. Pair it with the hands-on tools — read **Adafruit "How Blink Works"**
together for milliseconds, play the **CS Unplugged "Count the Dots"** binary cards for
bits, and explain ranges from **SparkFun's analog-to-digital** page (an adult read).

---

## F1 — Time in milliseconds

- A **second** is the chunk of time you already know (one "one-Mississippi").
- **"Milli" means one-thousandth (1/1000).** So a **millisecond (ms)** is one-thousandth
  of a second — a tiny sliver of time.
- That means **1000 milliseconds = 1 second**. (1000 of those tiny slivers add up to a
  whole second.)
- Arduino code measures waiting time in **milliseconds**. The command **`delay(1000)`**
  tells the board to wait **1000 ms, which is 1 second**, before doing the next thing.
- So `delay(500)` waits **half a second** (500 ms), and `delay(2000)` waits **2 seconds**.
- In the **Blink** program, the light turns on, `delay()` waits, then it turns off, waits
  again, and repeats forever — that wait is what you can *see* as the blink.
- **A smaller delay number means a FASTER blink** (less waiting between flashes); a
  **bigger number means a SLOWER blink** (more waiting). `delay(100)` blinks much faster
  than `delay(1000)`.

> Picture: a millisecond is to a second what one penny is to ten dollars — you need a
> whole thousand of them to make one. The blink speed is just *how long you wait* between
> turning the light on and off.

---

## F2 — Binary and bits

- Computers don't have ten fingers like we do. Deep down, a computer only knows **two**
  things: **ON** and **OFF** — like a light switch.
- We write ON as **1** and OFF as **0**. One of these on/off slots is called a **bit**.
- So **a bit can be only one of two values: 1 or 0** (on or off). That's it.
- **Computers store everything as bits** — numbers, letters, pictures, music, games —
  all of it is really just long strings of 1s and 0s. This way of counting with only
  1s and 0s is called **binary**.
- A bit by itself can't hold much, so we group bits together. **8 bits grouped together
  make 1 byte.** (A byte is a handy bundle of 8 on/off slots.)
- The famous **CS Unplugged "Count the Dots"** activity uses cards with dots, each card
  either face-up (on = 1) or face-down (off = 0). Flipping cards lets you make any number
  using only on and off.
- The trick is that each slot is worth **double** the one to its right. Reading the cards
  from right to left, the slots are worth: **1, 2, 4, 8, 16, 32, 64, 128**. Each value is
  the one before it doubled.
- You add up only the **on** cards to get the number. For example, an *on* 4-card plus an
  *on* 1-card makes **4 + 1 = 5**.
- With **8 bits** (the eight cards 1, 2, 4, 8, 16, 32, 64, 128) you can make every whole
  number from **0** (all off) up to **255** (all on). That's **256 different values** in all.

> Picture: binary is like counting with light switches instead of fingers. Each switch
> is worth double the one before it, and you just add up the ones you turned on.

---

## F3 — Number ranges and mapping

- A **range** is just the set of numbers something is allowed to be, from a **lowest** to a
  **highest**. For example, the numbers on a clock go in the range 1 to 12.
- Sensors and outputs on an Arduino turn things into numbers inside a fixed range. **The
  smallest number always means the lowest amount, and the biggest number means the most.**
- **PWM brightness uses the range 0 to 255.** When you set an LED's brightness with
  `analogWrite`, **0 means fully off** and **255 means fully bright**. A number in the
  middle, like 128, is medium brightness. (That top number 255 is the biggest value 8 bits
  can hold — see F2.)
- **`analogRead` uses the range 0 to 1023.** When the board reads an analog sensor (like a
  light sensor or the knob of a joystick), it gives back a whole number from **0 to 1023**.
  **0 is the lowest reading** and **1023 is the highest reading**.
- **A bigger reading means more** of whatever the sensor measures. For a light sensor, a
  **bigger number means more light**; for a turning knob, a **bigger number means you turned
  it further**.
- These are two different rulers: reading a sensor in is **0–1023**, but setting brightness
  or motor power out is **0–255**. They both start at 0 for "least" and go up to "most."
- Turning a number from one range into the matching spot in another range is called
  **mapping** — for example, taking a 0–1023 sensor reading and turning it into a 0–255
  brightness. Same idea every time: line up "lowest with lowest" and "highest with highest."

> Picture: a range is like a thermometer with a bottom and a top. The sensor's reading is
> the mark on the thermometer — low mark, small number; high mark, big number.

---

## Sources (all free; from the vetted list)

- **Adafruit — "How 'Blink' Works"** — learn.adafruit.com/adafruit-arduino-lesson-1-blink/how-blink-works — `setup()` runs once, `loop()` repeats, and `delay()` waits in milliseconds (1000 ms = 1 s). (F1)
- **CS Unplugged — Binary Numbers / "Count the Dots"** — classic.csunplugged.org/activities/binary-numbers (CC BY-NC-SA) — on/off dot cards = bits; card values 1, 2, 4, 8, 16, 32, 64, 128; 8 bits = 1 byte. (F2)
- **SparkFun — Analog-to-Digital Conversion** (adult reference, CC BY-SA 4.0) — learn.sparkfun.com/tutorials/analog-to-digital-conversion/all — analogRead gives a whole number 0–1023; bigger reading = more. (F3)
- Cross-references within Arduino Foundations: **A5 — Units** (milli = 1/1000; 1000 ms = 1 second).
