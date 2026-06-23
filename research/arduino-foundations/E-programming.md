# Programming Basics — Knowledge Base (for a smart 8-year-old, grade-6 ceiling)

A plain-language study reference for the **Programming** concept area of **Arduino
Foundations**. Written to be *true* even though it's simple — the examples are tiny on
purpose, and everything tied to Arduino's `setup()`/`loop()` or to block-coding
(Scratch/Blockly) is a real fact, not a made-up rule. Facts are synthesised from the
vetted free resources listed at the end; nothing is copied verbatim.

**How to use it:** this is the adult/teacher reference and the source the quiz questions
are drawn from. Pair it with the hands-on tools — **Blockly Games** (Maze for loops &
if, Music for functions) and **Scratch** (variables, My Blocks, operators) — and with
**Adafruit's "How Blink Works"** so she sees `setup()` and `loop()` on a real Arduino.

> Big idea: a computer is fast but not clever. It does **exactly** what you tell it, in
> the exact **order** you tell it. Programming is writing those instructions clearly.

---

## E1 — What a program is (an algorithm)

- A **program** is a set of instructions a computer follows to do a job.
- The plan behind it is an **algorithm**: a **precise, step-by-step list of instructions**
  to do a task or solve a problem. A recipe and the steps to brush your teeth are
  everyday algorithms.
- The computer follows the steps **exactly** and **in order** — it does **not** guess
  what you *meant*. If a step is in the wrong place, the computer still does the wrong
  thing. (That's why a tiny mistake — a **bug** — can break a program.)
- The steps must be **clear and unambiguous**: each one says exactly what to do, with no
  "you know what I mean."
- Example algorithm for "make toast": 1) get bread, 2) put it in the toaster, 3) push the
  lever down, 4) wait, 5) take the toast out. Swap steps 1 and 3 and it won't work.

> In Scratch or Blockly, the **blocks you stack from top to bottom** are the program; the
> idea of those ordered steps is the algorithm.

---

## E2 — Sequence, and Arduino's `setup()` / `loop()`

- **Sequence** means the steps run **in order, one after another, top to bottom** — unless
  you use something special (like a loop or an `if`) to change that.
- Every Arduino program (called a **sketch**) has **two special functions**:
  - **`setup()`** runs **once**, right at the start, when the board powers on or is reset.
    You use it to get ready — for example, telling a pin it will be an output.
  - **`loop()`** runs **after `setup()`**, and then **repeats forever** (over and over)
    until the board is turned off or reset. You put the main, repeating actions here.
- The famous **Blink** program lives in `loop()`: turn the LED **on**, wait, turn it
  **off**, wait — and because `loop()` repeats, the LED blinks again and again.
- Order matters: `setup()` **always runs before** `loop()`. You can't blink the LED in
  `loop()` correctly if you forgot to set up the pin in `setup()` first.

> Block-coding compare: `setup()` is like Scratch's **"when green flag clicked"** start,
> and `loop()` is like wrapping your blocks in a **"forever"** block.

---

## E3 — Variables & data types

- A **variable** is a **labeled box that holds a value**. You give the box a **name**, and
  the computer remembers whatever value you put inside.
- A variable can **change**: that's *why* it's called a *variable* (it can vary). You can
  put a new value in the box later, and the old value is replaced.
- A **data type** tells the computer **what kind of value** the box holds. Common ones:
  - **`int`** — a whole number (no fraction), like `5`, `0`, or `-3`. (Short for *integer*.)
  - **`float`** — a number that can have a decimal point, like `3.5`.
  - **`bool`** — a true/false value (`true` or `false`).
  - **`char`** — a single character, like the letter `A`.
- Tiny Arduino example: `int count = 0;` makes an `int` box **named** `count` and puts
  `0` in it. Later `count = count + 1;` changes the value inside to `1`.
- Variables are handy because you can **use the name** instead of repeating the number,
  and **change it in one place**.

> In Scratch you "make a variable," give it a name, and use **"set"** and **"change"**
> blocks — same idea: a named box whose value you can change.

---

## E4 — Functions

- A **function** is a **named action** (a mini-program) you can **call** (run) by its name,
  as many times as you like, without rewriting the steps.
- A function can take **inputs** (also called **arguments** or **parameters**) — values you
  hand it inside the parentheses `()` to tell it exactly what to do.
- Some functions also **give back** a value (a result you can use).
- Real Arduino functions you'll call:
  - **`delay(1000)`** — wait. The input `1000` means wait **1000 milliseconds = 1 second**.
  - **`digitalWrite(pin, HIGH)`** — turn a pin **on** (HIGH) or **off** (LOW). It takes
    **two** inputs: which pin, and HIGH or LOW.
  - **`pinMode(pin, OUTPUT)`** — set a pin to be an output (used in `setup()`).
- You can also **write your own** function and give it a name, then call it whenever you
  need those steps — this saves repeating yourself and keeps the program tidy.

> In Scratch these are **"My Blocks"** (blocks you make and name); in **Blockly Games:
> Music**, you build a function once and call it to play the tune again.

---

## E5 — If / Else (making decisions)

- An **`if`** statement lets a program **make a decision**: it does something **only when a
  condition is true**.
- A **condition** is a question with a **yes/no (true/false)** answer, like "is the button
  pressed?" or "is `count` greater than 5?"
- **`else`** gives a **backup plan**: do this **other** thing when the condition is **not**
  true (false).
- Plain-words shape: **IF** (it is raining) **THEN** take an umbrella, **ELSE** wear a hat.
- Arduino example: `if (buttonPressed) { turn LED on } else { turn LED off }` — the LED
  follows the button. Only **one** of the two paths runs each time, depending on the
  condition.
- The condition decides; the **curly braces `{ }`** hold the steps for each path.

> In Scratch/Blockly these are the **"if … then"** and **"if … then … else"** blocks; the
> hexagon-shaped condition slot is the true/false question.

---

## E6 — Loops (repeating)

- A **loop** **repeats steps** so you don't have to write them over and over.
- A **`for`** loop repeats a **set number of times** — like "do this **10 times**." You set
  a count, and it stops when the count is reached.
- A **`while`** loop repeats **as long as a condition stays true** — it keeps going while
  the condition holds, and stops when the condition becomes false.
- Example: a `for` loop can blink an LED **5 times**; a `while` loop can keep beeping
  **while a button is held down** and stop when it's let go.
- Watch out: if a `while` loop's condition **never** becomes false, the loop **never
  stops** — that's an **infinite loop**. (Arduino's `loop()` is *meant* to repeat forever,
  so that's the on-purpose kind.)

> In **Blockly Games: Maze** you use **"repeat"** loops to walk the path with fewer blocks;
> in Scratch they're the **"repeat (10)"** and **"repeat until"** blocks.

---

## E7 — Comparing & operators

- An **operator** is a symbol that **does something** to values — like math symbols `+`,
  `-`, `*` (times), `/` (divide).
- **`=` (one equals sign) means "put into the box"** — it's **assignment**. `x = 5;` puts
  `5` into the variable `x`. It does **not** ask a question.
- **`==` (two equals signs) means "is equal?"** — it **compares** and answers **true or
  false**. `x == 5` asks "is `x` equal to 5?" (This is a super common mix-up!)
- **Comparison operators** ask true/false questions about sizes:
  - **`>`** means **greater than** (bigger). `7 > 3` is **true**.
  - **`<`** means **less than** (smaller). `2 < 9` is **true**.
  - **`>=`** is "greater than or equal to"; **`<=`** is "less than or equal to";
    **`!=`** means "not equal."
- These comparisons are exactly the **conditions** an `if` or a `while` checks (E5, E6).

> In Scratch these are the green **Operators blocks** — `+`, `-`, and the `=`, `>`, `<`
> compare blocks that report **true/false** for an `if`.

---

## Sources (all free; from the vetted list)

- **Simple English Wikipedia — Algorithm** — simple.wikipedia.org/wiki/Algorithm (CC BY-SA) — "a list of steps that can be followed to solve a problem" (E1).
- **Simple English Wikipedia — Variable (computer science)** — simple.wikipedia.org/wiki/Variable_(computer_science) (CC BY-SA) — a named place that stores a value that can change (E3).
- **Adafruit — How "Blink" Works** — learn.adafruit.com/adafruit-arduino-lesson-1-blink/how-blink-works — `setup()` runs once, `loop()` repeats, `delay()` in milliseconds (E2, E4).
- **Scratch Wiki — Variable** — en.scratch-wiki.info/wiki/Variable (CC BY-SA) — set/change a named value (E3).
- **Scratch Wiki — My Blocks** — en.scratch-wiki.info/wiki/My_Blocks (CC BY-SA) — make and name your own blocks = functions (E4).
- **Scratch Wiki — Control Blocks** — en.scratch-wiki.info/wiki/Control_Blocks (CC BY-SA) — forever/repeat loops and if/else (E2, E5, E6).
- **Scratch Wiki — Operators Blocks** — en.scratch-wiki.info/wiki/Operators_Blocks (CC BY-SA) — `+ - * /`, `=`, `>`, `<` and true/false (E7).
- **Blockly Games** — blockly.games (open source, free) — Maze = loops & conditionals (E5, E6); Music = functions (E4).
- **code.org (Ages 5–11)** — code.org/students — block-based coding gateway for sequence, loops, conditionals.
