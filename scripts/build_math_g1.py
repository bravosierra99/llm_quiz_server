#!/usr/bin/env python3
"""Build a comprehensive Grade 1 math question bank for the quiz app.

Aligned to the Maryland College and Career-Ready Standards for Mathematics,
Grade 1 (MSDE framework) — the standards Anne Arundel County Public Schools
(AACPS) teaches to. Four domains: Operations & Algebraic Thinking (1.OA),
Number & Operations in Base Ten (1.NBT), Measurement & Data (1.MD), Geometry
(1.G).

Arithmetic questions are GENERATED with computed answers (so they can't be
wrong); conceptual questions are curated. Each chapter carries a knowledge base
(plain-language, for a 6–7 year old / a parent reading along) that also serves as
source material the app can quote when explaining a topic.

Run:  python scripts/build_math_g1.py   ->  writes banks/math-g1.json
"""
import json
import os
import random

random.seed(1)  # deterministic output so re-runs don't churn the bank

OUT = os.path.join(os.path.dirname(__file__), "..", "banks", "math-g1.json")


# --- small builders ---------------------------------------------------------
def mcq(prompt, answer, distractors, explanation):
    """An MCQ; choices = answer + distractors, shuffled, de-duped, max 4."""
    seen, choices = set(), []
    for c in [answer, *distractors]:
        s = str(c)
        if s not in seen:
            seen.add(s)
            choices.append(s)
    choices = choices[:4]
    if str(answer) not in choices:
        choices[-1] = str(answer)
    random.shuffle(choices)
    return {"type": "mcq", "prompt": prompt, "choices": choices,
            "answer": str(answer), "explanation": explanation}


def tf(prompt, answer, explanation):
    return {"type": "truefalse", "prompt": prompt,
            "answer": "True" if answer else "False", "explanation": explanation}


def short(prompt, answer, explanation):
    return {"type": "short", "prompt": prompt, "answer": str(answer),
            "explanation": explanation}


def num_distractors(ans, lo=0):
    """Plausible wrong numbers near `ans` (off-by-one/two), clamped to >= lo."""
    cand = [ans + 1, ans - 1, ans + 2, ans - 2, ans + 10]
    out = []
    for c in cand:
        if c >= lo and c != ans and c not in out:
            out.append(c)
    return out[:3]


# --- Chapter 1: Addition & Subtraction Within 20 ----------------------------
def ch_within20():
    qs = []
    # Addition facts: a representative, comprehensive spread within 20.
    add_pairs = [(2, 3), (4, 1), (5, 5), (6, 2), (7, 3), (8, 4), (9, 1),
                 (6, 6), (7, 8), (9, 9), (8, 5), (4, 7), (3, 9), (6, 7), (5, 8)]
    for a, b in add_pairs:
        s = a + b
        qs.append(mcq(f"What is {a} + {b}?", s, num_distractors(s),
                      f"{a} + {b} = {s}. You can count on from {max(a, b)}: "
                      f"{max(a, b)} … {', '.join(str(max(a,b)+i) for i in range(1, min(a,b)+1))}."))
    # Subtraction facts within 20.
    sub_pairs = [(5, 2), (8, 3), (9, 4), (10, 6), (12, 5), (14, 7), (11, 3),
                 (15, 8), (13, 6), (17, 9), (16, 7), (10, 4), (12, 8), (18, 9)]
    for a, b in sub_pairs:
        d = a - b
        qs.append(mcq(f"What is {a} - {b}?", d, num_distractors(d),
                      f"{a} - {b} = {d}. Start at {a} and count back {b}."))
    # "Make ten" strategy.
    qs.append(mcq("To add 8 + 5, you can first make ten: 8 + 2 = 10, then add the "
                  "rest. How much is left to add after making ten?", 3, [5, 2, 8],
                  "8 needs 2 to make ten, and 5 = 2 + 3, so 3 is left. 10 + 3 = 13."))
    qs.append(mcq("Make ten to add 9 + 6. After 9 + 1 = 10, how many more do you add?",
                  5, [6, 4, 1], "9 + 1 = 10 uses 1 of the 6, leaving 5. 10 + 5 = 15."))
    # Counting on / back.
    qs.append(short("Count on to add: 7 + 3. Say 7, then count up three. What number "
                    "do you land on?", 10, "7 … 8, 9, 10. So 7 + 3 = 10."))
    # Doubles.
    for n in (3, 4, 6, 7, 8):
        qs.append(mcq(f"What is the double {n} + {n}?", 2 * n, num_distractors(2 * n),
                      f"A double adds a number to itself: {n} + {n} = {2*n}."))
    # Fact-family relationship.
    qs.append(tf("If 6 + 7 = 13, then 13 - 7 = 6.", True,
                 "Addition and subtraction are opposites (a fact family): 6 + 7 = 13, "
                 "13 - 7 = 6, and 13 - 6 = 7 all go together."))
    qs.append(mcq("Which subtraction belongs to the same fact family as 4 + 9 = 13?",
                  "13 - 9 = 4", ["13 - 3 = 10", "9 - 4 = 5", "13 + 4 = 17"],
                  "The fact family for 4, 9, 13 includes 13 - 9 = 4 and 13 - 4 = 9."))
    qs.append(tf("Adding zero to a number changes it. For example, 7 + 0 = 8.", False,
                 "Adding zero changes nothing: 7 + 0 = 7."))
    kb = (
        "# Grade 1 Math — Addition & Subtraction Within 20\n\n"
        "**Standards: 1.OA.C.5, 1.OA.C.6 (also 1.OA.A.1).** First graders add and "
        "subtract within 20 and become *fluent* within 10.\n\n"
        "## Big ideas\n"
        "- **Count on** to add: for 7 + 3, start at 7 and count up 3 → 8, 9, 10.\n"
        "- **Count back** to subtract: for 10 - 2, start at 10 and count back 2 → 9, 8.\n"
        "- **Doubles** are quick to learn: 6 + 6 = 12, 8 + 8 = 16.\n"
        "- **Make ten:** to add 8 + 5, give 2 to the 8 to make 10, then add the rest "
        "(5 = 2 + 3), so 8 + 5 = 10 + 3 = 13.\n"
        "- **Fact families** link addition and subtraction: 4, 9, 13 give 4 + 9 = 13, "
        "9 + 4 = 13, 13 - 4 = 9, 13 - 9 = 4.\n"
        "- **Adding 0** leaves a number unchanged: 7 + 0 = 7.\n\n"
        "## Sources\n"
        "- Maryland State Department of Education — *Grade 1 Mathematics Framework* "
        "(MCCRSM), domain Operations & Algebraic Thinking.\n"
        "- Common Core State Standards for Mathematics, Grade 1 (1.OA).\n"
    )
    return {"name": "Addition & Subtraction Within 20",
            "source": {"title": "Within 20 — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 2: Addition & Subtraction Word Problems ------------------------
def ch_word_problems():
    qs = [
        mcq("Maya has 6 stickers. Her friend gives her 5 more. How many stickers does "
            "Maya have now?", 11, [10, 12, 1],
            "Putting together: 6 + 5 = 11 stickers."),
        mcq("There are 9 ducks in the pond. 4 ducks swim away. How many ducks are "
            "left?", 5, [13, 6, 4], "Taking away: 9 - 4 = 5 ducks."),
        mcq("Sam has 7 red blocks and 6 blue blocks. How many blocks in all?", 13,
            [12, 1, 14], "Put the groups together: 7 + 6 = 13."),
        mcq("A plate has 12 grapes. You eat 5. How many grapes are left?", 7,
            [17, 8, 6], "Take from: 12 - 5 = 7 grapes."),
        mcq("Liam had some marbles. He found 4 more and now has 11. How many did he "
            "start with?", 7, [15, 4, 8],
            "Start unknown: ? + 4 = 11, so 11 - 4 = 7 marbles."),
        mcq("There are 8 birds on a branch. Some fly away and 3 are left. How many "
            "flew away?", 5, [11, 3, 8],
            "Change unknown: 8 - ? = 3, so 8 - 3 = 5 birds flew away."),
        mcq("Add three numbers: 2 + 4 + 3.", 9, [8, 10, 6],
            "Add two at a time: 2 + 4 = 6, then 6 + 3 = 9."),
        mcq("Add three numbers: 5 + 5 + 2.", 12, [10, 13, 11],
            "5 + 5 = 10 (a make-ten pair), then 10 + 2 = 12."),
        mcq("There are 10 apples. 6 are red and the rest are green. How many are "
            "green?", 4, [16, 5, 6], "Take apart: 10 - 6 = 4 green apples."),
        mcq("Ava has 5 crayons. Ben has 8 crayons. How many MORE crayons does Ben "
            "have than Ava?", 3, [13, 2, 4],
            "Compare: 8 - 5 = 3 more crayons for Ben."),
        tf("For 'Tom has 4 cars and gets 3 more,' you should add to find how many he "
           "has now.", True, "Getting more means putting together: 4 + 3 = 7."),
        short("A box holds 6 crayons. Another box holds 7 crayons. How many crayons "
              "altogether?", 13, "6 + 7 = 13 crayons."),
    ]
    kb = (
        "# Grade 1 Math — Addition & Subtraction Word Problems\n\n"
        "**Standards: 1.OA.A.1, 1.OA.A.2.** Solve word problems within 20, including "
        "adding three numbers, with the unknown in any position.\n\n"
        "## Problem types\n"
        "- **Add to / put together** (how many in all) → add.\n"
        "- **Take from / take apart** (how many left) → subtract.\n"
        "- **Compare** (how many more / fewer) → subtract the smaller from the larger.\n"
        "- **Start or change unknown:** ? + 4 = 11 means 11 - 4 = 7.\n\n"
        "## Strategy\n"
        "Read the story, decide if a group is getting bigger (add) or smaller "
        "(subtract), then write a number sentence and solve. For three numbers, add "
        "two at a time and look for make-ten pairs.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.OA.A).\n"
        "- Common Core State Standards for Mathematics, Grade 1.\n"
    )
    return {"name": "Addition & Subtraction Word Problems",
            "source": {"title": "Word problems — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 3: The Equal Sign & Finding the Unknown -----------------------
def ch_equations():
    qs = [
        mcq("What does the equal sign (=) mean?",
            "The two sides are the same amount", ["Add the numbers",
            "The answer comes next", "The bigger number"],
            "The equal sign means both sides have the same value, like a balanced "
            "scale: 3 + 4 = 7 and also 7 = 3 + 4."),
        tf("This equation is true: 5 + 2 = 7.", True, "5 + 2 = 7, so it is true."),
        tf("This equation is true: 6 = 6.", True,
           "Both sides are 6, so it is true. An equation can have one number on a side."),
        tf("This equation is true: 4 + 3 = 8.", False, "4 + 3 = 7, not 8, so it is false."),
        tf("This equation is true: 2 + 5 = 5 + 2.", True,
           "Both sides equal 7. Order doesn't change the sum (commutative property)."),
        mcq("Find the unknown: 8 + ? = 11.", 3, [19, 4, 2],
            "Think 8 plus what makes 11? 11 - 8 = 3."),
        mcq("Find the unknown: ? + 6 = 10.", 4, [16, 5, 3],
            "What plus 6 makes 10? 10 - 6 = 4."),
        mcq("Find the unknown: 12 - ? = 7.", 5, [19, 6, 4],
            "12 take away what leaves 7? 12 - 7 = 5."),
        mcq("Find the unknown: 9 = 4 + ?", 5, [13, 6, 4],
            "4 plus what makes 9? 9 - 4 = 5. The unknown can be on either side."),
        mcq("Because order doesn't change a sum, 3 + 8 is the same as which?",
            "8 + 3", ["8 - 3", "3 - 8", "8 + 8"],
            "The commutative property: 3 + 8 = 8 + 3 = 11."),
        tf("To add 7 + 6, knowing 6 + 7 = 13 helps because order doesn't change the "
           "sum.", True, "7 + 6 = 6 + 7 = 13."),
        short("Find the missing number: 10 - ? = 4.", 6, "10 - 6 = 4, so the missing "
              "number is 6."),
    ]
    kb = (
        "# Grade 1 Math — The Equal Sign & Finding the Unknown\n\n"
        "**Standards: 1.OA.B.3, 1.OA.B.4, 1.OA.D.7, 1.OA.D.8.**\n\n"
        "## The equal sign\n"
        "`=` means **the same as** — both sides balance. So 3 + 4 = 7, 7 = 3 + 4, and "
        "6 = 6 are all true. An equation like 4 + 3 = 8 is **false** because 4 + 3 is 7.\n\n"
        "## Finding the unknown\n"
        "A box or question mark stands for a missing number: 8 + ? = 11. Use a related "
        "subtraction to find it: 11 - 8 = 3. Subtraction can be thought of as a missing "
        "addend: 12 - 5 = ? is the same as 5 + ? = 12.\n\n"
        "## Properties (strategies)\n"
        "- **Order doesn't change a sum** (commutative): 3 + 8 = 8 + 3.\n"
        "- You can group numbers in any order when adding three.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.OA.B, 1.OA.D).\n"
    )
    return {"name": "The Equal Sign & Finding the Unknown",
            "source": {"title": "Equations — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 4: Counting & Numbers to 120 ----------------------------------
def ch_counting():
    qs = []
    for start in (47, 89, 108, 99, 60, 115):
        qs.append(mcq(f"What number comes right after {start}?", start + 1,
                      num_distractors(start + 1),
                      f"Counting up one from {start} gives {start + 1}."))
    for n in (50, 80, 100, 70, 116):
        qs.append(mcq(f"What number comes right before {n}?", n - 1,
                      num_distractors(n - 1),
                      f"Counting back one from {n} gives {n - 1}."))
    qs.append(mcq("Count by tens: 10, 20, 30, 40, ?", 50, [41, 60, 45],
                  "Counting by tens, after 40 comes 50."))
    qs.append(mcq("Keep counting by tens: 70, 80, 90, ?", 100, [91, 110, 99],
                  "After 90 comes 100 when counting by tens."))
    qs.append(tf("When you count, 120 comes after 119.", True,
                 "First graders count all the way to 120; 119, then 120."))
    qs.append(short("Write the number for one hundred five.", 105,
                    "One hundred five is written 105."))
    qs.append(mcq("Which number is one hundred twelve?", 112, [102, 120, 121],
                  "One hundred twelve = 112 (1 hundred, 1 ten, 2 ones)."))
    qs.append(short("Count on by ones from 116: 116, 117, ___. What comes next?", 118,
                    "After 117 comes 118."))
    kb = (
        "# Grade 1 Math — Counting & Numbers to 120\n\n"
        "**Standard: 1.NBT.A.1.** Count to 120 starting at any number, and read and "
        "write numerals.\n\n"
        "## Big ideas\n"
        "- Count forward from **any** number, not just 1 (e.g., 47, 48, 49 …).\n"
        "- **After** means +1; **before** means -1.\n"
        "- **Count by tens:** 10, 20, 30 … 120.\n"
        "- Read and write numbers: 'one hundred five' is **105**; 'one hundred twelve' "
        "is **112**.\n"
        "- The counting sequence goes all the way to **120**.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.NBT.A).\n"
    )
    return {"name": "Counting & Numbers to 120",
            "source": {"title": "Counting to 120 — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 5: Place Value — Tens and Ones --------------------------------
def ch_place_value():
    qs = []
    for n in (34, 58, 72, 90, 47, 60, 19):
        tens, ones = n // 10, n % 10
        qs.append(mcq(f"How many TENS are in the number {n}?", tens,
                      [ones, tens + 1, n],
                      f"{n} is {tens} ten(s) and {ones} one(s)."))
        qs.append(mcq(f"How many ONES are in the number {n}?", ones,
                      [tens, ones + 1, n],
                      f"{n} is {tens} ten(s) and {ones} one(s)."))
    qs.append(mcq("Which number has 4 tens and 6 ones?", 46, [64, 406, 10],
                  "4 tens and 6 ones make 46."))
    qs.append(mcq("What is 5 tens and 0 ones?", 50, [5, 500, 55],
                  "5 tens and 0 ones make 50. Decade numbers are tens with no ones."))
    qs.append(tf("The number 17 is made of 1 ten and 7 ones.", True,
                 "10 + 7 = 17, so 1 ten and 7 ones."))
    qs.append(tf("In the number 80, there are 8 ones.", False,
                 "80 is 8 tens and 0 ones, not 8 ones."))
    qs.append(short("A bundle of ten and 3 more ones is what number?", 13,
                    "1 ten + 3 ones = 13."))
    qs.append(mcq("Ten is a bundle of how many ones?", 10, [1, 100, 2],
                  "Ten ones make one ten — that's a bundle of 10."))
    kb = (
        "# Grade 1 Math — Place Value: Tens and Ones\n\n"
        "**Standard: 1.NBT.B.2.** Understand that two digits show **tens** and **ones**.\n\n"
        "## Big ideas\n"
        "- **10 is a bundle of ten ones** — one 'ten'.\n"
        "- In a two-digit number, the **left** digit tells the tens and the **right** "
        "digit tells the ones. In **46**: 4 tens and 6 ones.\n"
        "- Numbers **11–19** are one ten and some ones (17 = 1 ten + 7 ones).\n"
        "- **Decade numbers** 10, 20 … 90 are that many tens and **0 ones** (80 = 8 "
        "tens, 0 ones).\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.NBT.B).\n"
    )
    return {"name": "Place Value — Tens and Ones",
            "source": {"title": "Place value — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 6: Comparing Numbers (>, <, =) --------------------------------
def ch_compare():
    qs = []
    pairs = [(34, 28), (56, 65), (19, 91), (40, 40), (73, 37), (60, 59), (88, 80)]
    for a, b in pairs:
        if a > b:
            ans, why = ">", f"{a} has more, so {a} > {b}."
        elif a < b:
            ans, why = "<", f"{a} has less, so {a} < {b}."
        else:
            ans, why = "=", f"{a} and {b} are the same, so {a} = {b}."
        qs.append(mcq(f"Compare: {a} ___ {b}. Which sign is correct (>, <, or =)?",
                      ans, [">", "<", "="], why + " (> means greater, < means less, "
                      "= means equal.)"))
    qs.append(mcq("Which number is greater, 45 or 54?", 54, [45, "They are equal", 9],
                  "Compare tens first: 5 tens beats 4 tens, so 54 > 45."))
    qs.append(mcq("Which number is less, 72 or 27?", 27, [72, "They are equal", 99],
                  "2 tens is less than 7 tens, so 27 < 72."))
    qs.append(tf("The sign > means 'greater than'.", True,
                 "> points to the smaller number; the big open side faces the bigger "
                 "number. 8 > 3."))
    qs.append(tf("63 < 36 is true.", False, "63 has 6 tens and 36 has 3 tens, so 63 is "
                 "greater: 63 > 36."))
    qs.append(short("Use the right word: 50 is ______ than 40 (greater or less)?",
                    "greater", "5 tens is more than 4 tens, so 50 is greater than 40."))
    kb = (
        "# Grade 1 Math — Comparing Numbers\n\n"
        "**Standard: 1.NBT.B.3.** Compare two two-digit numbers using **>**, **<**, "
        "and **=**.\n\n"
        "## How to compare\n"
        "1. **Compare the tens first.** More tens = greater number (54 > 45).\n"
        "2. If the tens are the same, **compare the ones**.\n"
        "3. If both digits match, the numbers are **equal** (40 = 40).\n\n"
        "## The signs\n"
        "- **>** means *greater than*: 8 > 3.\n"
        "- **<** means *less than*: 3 < 8.\n"
        "- **=** means *equal to*: 6 = 6.\n"
        "The open (big) side of < or > always faces the **bigger** number.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.NBT.B).\n"
    )
    return {"name": "Comparing Numbers (>, <, =)",
            "source": {"title": "Comparing numbers — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 7: Two-Digit Addition & Subtraction ---------------------------
def ch_two_digit():
    qs = []
    # 10 more / 10 less (mental).
    for n in (34, 50, 67, 89, 23):
        qs.append(mcq(f"What is 10 MORE than {n}?", n + 10, [n + 1, n - 10, n + 20],
                      f"10 more changes only the tens: {n} → {n + 10}."))
    for n in (45, 70, 38, 90):
        qs.append(mcq(f"What is 10 LESS than {n}?", n - 10, [n - 1, n + 10, n - 20],
                      f"10 less changes only the tens: {n} → {n - 10}."))
    # Two-digit + one-digit (no and with regrouping).
    for a, b in [(23, 4), (45, 3), (52, 6), (37, 2)]:
        qs.append(mcq(f"What is {a} + {b}?", a + b, num_distractors(a + b),
                      f"Add the ones: {a % 10} + {b} = {a % 10 + b}, keep {a // 10} tens. "
                      f"{a} + {b} = {a + b}."))
    # Two-digit + multiple of ten.
    for a, b in [(24, 30), (53, 20), (41, 40), (16, 50)]:
        qs.append(mcq(f"What is {a} + {b}?", a + b, [a + b + 10, a + b - 10, a + b + 1],
                      f"Add tens to tens: {a // 10} tens + {b // 10} tens, keep "
                      f"{a % 10} ones. {a} + {b} = {a + b}."))
    # Subtract multiples of ten.
    for a, b in [(70, 30), (90, 40), (60, 60), (50, 20), (80, 10)]:
        qs.append(mcq(f"What is {a} - {b}?", a - b, [a - b + 10, a - b - 10, a + b],
                      f"Subtract tens from tens: {a // 10} tens - {b // 10} tens = "
                      f"{(a - b) // 10} tens. {a} - {b} = {a - b}."))
    qs.append(tf("10 more than 47 is 57.", True, "Only the tens go up by one: 47 → 57."))
    qs.append(tf("To find 10 less than 80, you count back ten ones one at a time.", False,
                 "You don't have to count one at a time — 10 less just drops the tens "
                 "digit by one: 80 → 70."))
    qs.append(short("A toy costs 40 cents. You add 30 cents more. How many cents?", 70,
                    "40 + 30 = 70 cents (4 tens + 3 tens = 7 tens)."))
    kb = (
        "# Grade 1 Math — Two-Digit Addition & Subtraction\n\n"
        "**Standards: 1.NBT.C.4, 1.NBT.C.5, 1.NBT.C.6.**\n\n"
        "## 10 more, 10 less (in your head)\n"
        "Adding or subtracting 10 changes **only the tens digit** — the ones stay the "
        "same. 47 + 10 = 57; 47 - 10 = 37. No counting one-by-one needed.\n\n"
        "## Adding within 100\n"
        "- **Two-digit + one-digit:** add the ones to the ones (23 + 4 = 27).\n"
        "- **Two-digit + tens:** add tens to tens (24 + 30 = 54).\n"
        "Sometimes the ones make a new ten (regrouping): 37 + 2 = 39, but 38 + 5 makes "
        "another ten.\n\n"
        "## Subtracting tens\n"
        "Subtract multiples of ten from multiples of ten by taking tens from tens: "
        "70 - 30 = 40 (7 tens - 3 tens = 4 tens).\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.NBT.C).\n"
    )
    return {"name": "Two-Digit Addition & Subtraction",
            "source": {"title": "Two-digit add/subtract — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 8: Measurement & Length ---------------------------------------
def ch_measurement():
    qs = [
        mcq("A pencil is longer than a crayon. The crayon is longer than an eraser. "
            "Which is longest?", "The pencil", ["The crayon", "The eraser",
            "They are equal"],
            "If pencil > crayon and crayon > eraser, then the pencil is the longest "
            "(comparing indirectly)."),
        mcq("A snake is shorter than a rope. The rope is shorter than a hose. Which is "
            "SHORTEST?", "The snake", ["The rope", "The hose", "They are equal"],
            "Snake < rope < hose, so the snake is shortest."),
        mcq("You measure a book with paper clips and it is 6 clips long. The clips "
            "must be laid end to end with...", "no gaps and no overlaps",
            ["big gaps", "clips on top of each other", "only one clip"],
            "Length units must touch end-to-end with no gaps or overlaps, or the "
            "measurement is wrong."),
        mcq("A marker is 5 cubes long. A glue stick is 8 cubes long. Which is longer?",
            "The glue stick", ["The marker", "They are equal", "The cubes"],
            "8 cubes is more than 5 cubes, so the glue stick is longer."),
        mcq("If a ribbon is 4 paper clips long, how many paper clips would 2 of those "
            "ribbons be, laid end to end?", 8, [4, 6, 2],
            "4 clips + 4 clips = 8 clips."),
        tf("To compare two pencils fairly, you should line up their ends at the same "
           "starting point.", True,
           "Measuring length means starting both objects at the same line, then seeing "
           "which reaches farther."),
        tf("It is okay to leave gaps between the cubes when you measure how long "
           "something is.", False, "Gaps make the measurement wrong; units must touch."),
        short("Three sticks: a short, a medium, and a long one. If you put them in "
              "order shortest to longest, which comes FIRST?", "the short stick",
              "Ordering by length starts with the shortest."),
    ]
    kb = (
        "# Grade 1 Math — Measurement & Length\n\n"
        "**Standards: 1.MD.A.1, 1.MD.A.2.** Order and compare lengths, and measure with "
        "same-size units.\n\n"
        "## Big ideas\n"
        "- **Order by length:** put objects shortest → longest.\n"
        "- **Compare indirectly:** if A is longer than B, and B is longer than C, then "
        "A is longer than C (you don't have to compare A and C directly).\n"
        "- **Line up the ends:** start both objects at the same line to compare fairly.\n"
        "- **Measure with units** (cubes, paper clips) laid end to end with **no gaps "
        "and no overlaps**. The length is the number of units.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.MD.A).\n"
    )
    return {"name": "Measurement & Length",
            "source": {"title": "Measurement — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 9: Telling Time -----------------------------------------------
def ch_time():
    qs = [
        mcq("The hour hand points to 3 and the minute hand points to 12. What time is "
            "it?", "3:00", ["12:00", "3:30", "6:00"],
            "Minute hand on 12 means o'clock; hour hand on 3 means 3:00."),
        mcq("When the minute hand points straight up to the 12, the time is at the...",
            "o'clock (the hour)", ["half hour", "minute", "second"],
            "Minute hand on 12 = exactly o'clock, like 5:00."),
        mcq("The minute hand points to 6. This means it is...", "half past the hour",
            ["o'clock", "almost midnight", "noon only"],
            "Minute hand on 6 means 30 minutes — half past the hour, like 4:30."),
        mcq("The hour hand is between 2 and 3, and the minute hand points to 6. What "
            "time is it?", "2:30", ["3:30", "2:00", "6:30"],
            "Half past 2 is 2:30; the hour hand sits between 2 and 3."),
        mcq("How would you write 'seven o'clock' on a digital clock?", "7:00",
            ["7:30", "70:0", "12:07"], "Seven o'clock is 7:00."),
        mcq("How do you write 'half past nine'?", "9:30", ["9:00", "10:30", "9:15"],
            "Half past means 30 minutes after the hour: 9:30."),
        tf("On a clock, the SHORT hand is the hour hand.", True,
           "The short hand shows the hour; the long hand shows the minutes."),
        tf("6:30 means half past six.", True, "30 minutes after 6 is half past six."),
        short("Write the time when the hour hand is on 8 and the minute hand is on 12.",
              "8:00", "Minute hand on 12 = o'clock, so 8:00."),
    ]
    kb = (
        "# Grade 1 Math — Telling Time\n\n"
        "**Standard: 1.MD.B.3.** Tell and write time in **hours** and **half-hours** "
        "using analog and digital clocks.\n\n"
        "## Reading a clock\n"
        "- The **short hand** is the **hour** hand; the **long hand** is the **minute** "
        "hand.\n"
        "- Minute hand on **12** → **o'clock** (e.g., 3:00).\n"
        "- Minute hand on **6** → **half past** the hour, written **:30** (e.g., 4:30). "
        "At half past, the hour hand sits **between** two numbers.\n\n"
        "## Writing time\n"
        "Digital time is written hour:minutes — seven o'clock is **7:00**, half past "
        "nine is **9:30**.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.MD.B).\n"
    )
    return {"name": "Telling Time",
            "source": {"title": "Telling time — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 10: Data & Graphs ---------------------------------------------
def ch_data():
    qs = [
        mcq("A picture graph shows 5 cats, 3 dogs, and 4 birds. How many pets in all?",
            12, [11, 13, 8], "Add the categories: 5 + 3 + 4 = 12 pets."),
        mcq("Using the pets above (5 cats, 3 dogs, 4 birds), which group has the MOST?",
            "Cats", ["Dogs", "Birds", "They are equal"],
            "5 cats is the largest number, so cats are the most."),
        mcq("Using the pets above (5 cats, 3 dogs, 4 birds), which group has the "
            "FEWEST?", "Dogs", ["Cats", "Birds", "They are equal"],
            "3 dogs is the smallest number, so dogs are the fewest."),
        mcq("5 cats and 4 birds — how many MORE cats than birds?", 1, [9, 2, 0],
            "Compare: 5 - 4 = 1 more cat."),
        mcq("A class votes: 6 like apples, 6 like bananas. Which is true?",
            "They are equal", ["Apples win", "Bananas win", "Nobody voted"],
            "6 equals 6, so the two groups are the same."),
        tf("A graph with up to three categories can show how many are in each group.",
           True, "First-grade graphs organize data into up to three categories and let "
           "you compare them."),
        tf("If 7 kids like red and 2 like blue, more kids like blue.", False,
           "7 is greater than 2, so more kids like red."),
        short("Stickers: 3 stars, 5 hearts, 2 moons. How many stickers altogether?", 10,
              "3 + 5 + 2 = 10 stickers."),
    ]
    kb = (
        "# Grade 1 Math — Data & Graphs\n\n"
        "**Standard: 1.MD.C.4.** Organize, represent, and interpret data with up to "
        "**three categories**.\n\n"
        "## What to do with a graph\n"
        "- Count **how many in each** category.\n"
        "- Find the **total** by adding the categories.\n"
        "- Compare: which has **most**, which has **fewest**, and **how many more** one "
        "has than another (subtract).\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.MD.C).\n"
    )
    return {"name": "Data & Graphs",
            "source": {"title": "Data & graphs — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 11: Shapes & Their Attributes ---------------------------------
def ch_shapes():
    qs = [
        mcq("How many sides does a triangle have?", 3, [4, 2, 5],
            "A triangle always has 3 straight sides and 3 corners."),
        mcq("How many sides does a square have?", 4, [3, 5, 6],
            "A square has 4 equal sides and 4 corners."),
        mcq("How many corners (vertices) does a rectangle have?", 4, [3, 2, 6],
            "A rectangle has 4 sides and 4 corners."),
        mcq("Which is a DEFINING attribute of a triangle (always true)?",
            "It has three sides", ["It is red", "It is big", "It points up"],
            "Defining attributes (like 3 sides) make it a triangle. Color, size, and "
            "direction do NOT change what shape it is."),
        mcq("A shape is closed, with 3 straight sides. What is it?", "A triangle",
            ["A square", "A circle", "A rectangle"],
            "3 straight sides → triangle."),
        mcq("Which solid shape can roll and has a point on top?", "Cone",
            ["Cube", "Cylinder", "Rectangular prism"],
            "A cone has a round bottom and a point on top, and it can roll."),
        mcq("Which solid shape has 6 square faces?", "Cube",
            ["Cone", "Cylinder", "Sphere"], "A cube has 6 equal square faces."),
        mcq("You put two squares side by side. What new shape can they make?",
            "A rectangle", ["A triangle", "A circle", "A cone"],
            "Two equal squares joined make a rectangle — composing shapes."),
        mcq("Two triangles can be put together to make a...", "square or rectangle",
            ["circle", "cone", "single triangle"],
            "Two matching triangles can form a square or rectangle."),
        tf("A big triangle and a small triangle are both still triangles.", True,
           "Size doesn't change the shape — both have 3 sides, so both are triangles."),
        tf("A circle has straight sides and corners.", False,
           "A circle is round — no straight sides and no corners."),
        short("How many corners does a triangle have?", 3,
              "A triangle has 3 corners (vertices), one for each pair of sides."),
    ]
    kb = (
        "# Grade 1 Math — Shapes & Their Attributes\n\n"
        "**Standards: 1.G.A.1, 1.G.A.2.** Tell shapes apart by **defining attributes** "
        "and **build** new shapes from smaller ones.\n\n"
        "## Defining vs non-defining\n"
        "- **Defining** attributes decide the shape: number of **sides** and **corners**, "
        "straight vs round. A triangle is *anything* with 3 straight sides.\n"
        "- **Non-defining** attributes do NOT matter: color, size, and which way it "
        "points. A big red triangle and a small blue triangle are both triangles.\n\n"
        "## Common shapes\n"
        "- **Triangle:** 3 sides, 3 corners. **Square:** 4 equal sides, 4 corners. "
        "**Rectangle:** 4 sides, 4 corners. **Circle:** round, no corners.\n"
        "- **Solids:** cube (6 square faces), cylinder (rolls, flat ends), cone (point "
        "on top), sphere (ball).\n\n"
        "## Composing shapes\n"
        "Put shapes together to make new ones: two squares → a rectangle; two triangles "
        "→ a square or rectangle.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.G.A).\n"
    )
    return {"name": "Shapes & Their Attributes",
            "source": {"title": "Shapes — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 12: Equal Shares — Halves & Fourths ---------------------------
def ch_fractions():
    qs = [
        mcq("You cut a circle into 2 equal parts. Each part is called a...", "half",
            ["fourth", "whole", "third"],
            "Two equal parts are halves; one part is 'a half'."),
        mcq("You cut a square into 4 equal parts. Each part is called a...",
            "fourth (quarter)", ["half", "whole", "double"],
            "Four equal parts are fourths, also called quarters."),
        mcq("Which pizza is cut into FOURTHS?", "A pizza cut into 4 equal pieces",
            ["A pizza cut into 2 equal pieces", "A pizza cut into 3 pieces",
             "A whole pizza"], "Fourths means 4 equal pieces."),
        mcq("To be a fair half, the two pieces must be...", "equal in size",
            ["different sizes", "any size", "one big and one small"],
            "Halves and fourths must be EQUAL shares — same size pieces."),
        mcq("Which is BIGGER, one half of a cookie or one fourth of the same cookie?",
            "one half", ["one fourth", "they are equal", "neither"],
            "More cuts make smaller pieces. Two pieces (halves) are bigger than four "
            "pieces (fourths)."),
        mcq("If you split a sandwich into 4 equal parts, how many parts make the whole "
            "sandwich?", 4, [2, 1, 3],
            "All 4 fourths together make one whole."),
        mcq("Two halves of an apple make...", "one whole apple", ["two apples",
            "a fourth", "a half"], "Two equal halves join back into one whole."),
        tf("Cutting a shape into 4 equal parts gives fourths.", True,
           "4 equal parts = fourths (quarters)."),
        tf("More equal pieces means each piece is bigger.", False,
           "More pieces means each one is SMALLER — a fourth is smaller than a half."),
        short("What do we call one of two equal parts of a whole?", "a half",
              "One of two equal parts is a half."),
    ]
    kb = (
        "# Grade 1 Math — Equal Shares: Halves & Fourths\n\n"
        "**Standard: 1.G.A.3.** Partition circles and rectangles into **two** and "
        "**four** equal shares.\n\n"
        "## Big ideas\n"
        "- **Halves:** 2 equal parts. One part is **a half**.\n"
        "- **Fourths (quarters):** 4 equal parts. One part is **a fourth**.\n"
        "- Shares must be **equal** — same-size pieces — to be fair halves or fourths.\n"
        "- All the parts together make **one whole** (two halves = one whole; four "
        "fourths = one whole).\n"
        "- **More pieces = smaller pieces.** A half is **bigger** than a fourth of the "
        "same shape.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 Mathematics Framework* (1.G.A).\n"
    )
    return {"name": "Equal Shares — Halves & Fourths",
            "source": {"title": "Halves & fourths — knowledge base", "content": kb},
            "questions": qs}


def build():
    chapters = [
        ch_within20(), ch_word_problems(), ch_equations(), ch_counting(),
        ch_place_value(), ch_compare(), ch_two_digit(), ch_measurement(),
        ch_time(), ch_data(), ch_shapes(), ch_fractions(),
    ]
    bank = {
        "subject": {
            "name": "Grade 1 Math (Anne Arundel County)",
            "description": "Comprehensive first-grade math, aligned to the Maryland "
                           "College and Career-Ready Standards (the standards AACPS "
                           "teaches to): operations, place value, measurement & data, "
                           "and geometry.",
        },
        "chapters": chapters,
    }
    total = sum(len(c["questions"]) for c in chapters)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    print(f"wrote {os.path.normpath(OUT)}")
    print(f"{len(chapters)} chapters, {total} questions")
    for c in chapters:
        print(f"  {len(c['questions']):>3}  {c['name']}")


if __name__ == "__main__":
    build()
