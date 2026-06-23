"""Seed FleetQuiz with a sample Arduino subject so the full quiz loop is usable
(and testable) without the LLM. Idempotent: skips if the subject already exists.

Run:  python -m seed   (inside the container or a local venv)
"""
import json

from app.db import get_conn, init_db

SUBJECT = ("Arduino Experiments", "Hands-on electronics & coding for the Arduino starter kit.")

CHAPTERS = {
    "Chapter 1 — LEDs & Blinking": [
        ("mcq", "Which Arduino function makes a digital pin output HIGH or LOW?",
         ["digitalWrite()", "analogRead()", "Serial.print()", "delay()"],
         "digitalWrite()",
         "digitalWrite(pin, HIGH/LOW) sets a digital pin's voltage on or off."),
        ("mcq", "What is the purpose of a resistor in series with an LED?",
         ["To limit the current so the LED isn't damaged", "To make the LED brighter",
          "To store energy", "To convert AC to DC"],
         "To limit the current so the LED isn't damaged",
         "Without a current-limiting resistor, too much current flows and can burn out the LED."),
        ("truefalse", "An LED only lights up when current flows through it in the correct direction.",
         [], "True",
         "LEDs are diodes — they conduct in one direction. The longer leg (anode) goes to +."),
        ("short", "What does the delay(1000) function do in a blink sketch?",
         [], "Pauses the program for 1000 milliseconds (1 second).",
         "delay() takes milliseconds, so 1000 = 1 second."),
    ],
    "Chapter 2 — Buttons & Inputs": [
        ("mcq", "Which function reads whether a button is pressed on a digital pin?",
         ["digitalRead()", "digitalWrite()", "analogWrite()", "pinMode()"],
         "digitalRead()",
         "digitalRead(pin) returns HIGH or LOW depending on the pin's voltage."),
        ("truefalse", "A pull-down resistor keeps an input pin at a known LOW value when the button is not pressed.",
         [], "True",
         "Pull-down (or pull-up) resistors prevent the input from 'floating' to random values."),
        ("short", "What does pinMode(7, INPUT) tell the Arduino?",
         [], "That pin 7 will be used to read input rather than drive output.",
         "pinMode configures a pin as INPUT, OUTPUT, or INPUT_PULLUP."),
    ],
}


def seed():
    init_db()
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM chapters WHERE name = ? AND parent_id IS NULL", (SUBJECT[0],)).fetchone()
        if existing:
            print(f"Topic '{SUBJECT[0]}' already exists (id={existing['id']}); skipping seed.")
            return
        # The root topic is a node with parent_id NULL; chapters are its children.
        sid = conn.execute(
            "INSERT INTO chapters (parent_id, name, description) VALUES (NULL, ?, ?)", SUBJECT).lastrowid
        for pos, (cname, qs) in enumerate(CHAPTERS.items()):
            cid = conn.execute(
                "INSERT INTO chapters (parent_id, name, position) VALUES (?, ?, ?)",
                (sid, cname, pos)).lastrowid
            for qtype, prompt, choices, answer, expl in qs:
                conn.execute(
                    "INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (cid, qtype, prompt, json.dumps(choices), answer, expl))
        print(f"Seeded '{SUBJECT[0]}' with {len(CHAPTERS)} chapters.")


if __name__ == "__main__":
    seed()
