"""Build the Arduino Foundations → Numbers for Electronics question bank (area F).

Reads the child-facing KB markdown and emits banks/arduino-F-numbers.json in the
recursive node-tree import shape. Questions are written for a smart ~8-year-old with a
6th-grade ceiling: concrete, analogy-driven, short, and factually true.

Run:  python -m scripts.build_arduino_F   (from repo root)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = (ROOT / "research" / "arduino-foundations" / "F-numbers.md").read_text(encoding="utf-8")
OUT = ROOT / "banks" / "arduino-F-numbers.json"


def mcq(prompt, choices, answer, expl):
    return {"type": "mcq", "prompt": prompt, "choices": choices, "answer": answer, "explanation": expl}


def tf(prompt, answer, expl):
    return {"type": "truefalse", "prompt": prompt, "answer": answer, "explanation": expl}


def short(prompt, answer, expl):
    return {"type": "short", "prompt": prompt, "answer": answer, "explanation": expl}


F1 = [
    mcq("'Milli' means one of these — which?",
        ["One-thousandth (1/1000)", "One hundred", "One thousand times bigger", "One half"],
        "One-thousandth (1/1000)",
        "Milli means 1/1000, so a millisecond is one-thousandth of a second."),
    mcq("How many milliseconds make up one whole second?",
        ["1000", "100", "10", "60"], "1000",
        "Milli means 1/1000, so it takes 1000 milliseconds to make 1 second."),
    mcq("In Arduino code, what does delay(1000) tell the board to do?",
        ["Wait 1 second", "Wait 1000 seconds", "Wait 1 minute", "Blink 1000 times fast"],
        "Wait 1 second",
        "delay() counts in milliseconds, and 1000 ms = 1 second."),
    mcq("Which delay makes an LED blink FASTER?",
        ["delay(100)", "delay(1000)", "delay(2000)", "delay(5000)"], "delay(100)",
        "A smaller delay number means less waiting, so the blink is faster."),
    mcq("About how long does delay(500) make the board wait?",
        ["Half a second", "Five seconds", "Fifty seconds", "Five minutes"], "Half a second",
        "500 ms is half of 1000 ms, and 1000 ms = 1 second, so it waits half a second."),
    tf("delay(2000) makes the board wait about 2 seconds.",
       "True", "2000 ms is twice 1000 ms, and 1000 ms = 1 second, so it waits 2 seconds."),
    tf("A millisecond is longer than a whole second.",
       "False", "A millisecond is one-thousandth of a second, so it is much shorter."),
    short("delay() in Arduino code counts time in which unit?",
          "Milliseconds", "delay() waits in milliseconds, so delay(1000) waits 1 second."),
    mcq("In the Blink program, what actually makes the pause you can SEE between flashes?",
        ["The delay() command waiting", "The wire getting hot",
         "The board running out of power", "The LED changing color"],
        "The delay() command waiting",
        "delay() waits a set number of milliseconds, and that wait is the visible blink gap."),
]

F2 = [
    mcq("A single bit can be only one of how many values?",
        ["2", "8", "10", "100"], "2",
        "A bit is either 1 (on) or 0 (off) — just two possible values."),
    mcq("In binary, the number 1 stands for which?",
        ["On", "Off", "Ten", "Nothing at all"], "On",
        "We write ON as 1 and OFF as 0 — a bit is like a light switch."),
    mcq("What is the special name for counting using only 1s and 0s?",
        ["Binary", "Dozens", "Decimals", "Fractions"], "Binary",
        "Counting with only 1s and 0s (on and off) is called binary."),
    mcq("In the 'Count the Dots' cards, each slot is worth how much compared to the one on its right?",
        ["Double", "Half", "The same", "Ten times"], "Double",
        "Each binary slot is worth double the one to its right: 1, 2, 4, 8, 16..."),
    mcq("An 'on' 4-card plus an 'on' 1-card makes which number?",
        ["5", "3", "41", "14"], "5",
        "You add up only the ON cards: 4 + 1 = 5."),
    mcq("With 8 bits all turned ON, what is the biggest number you can make?",
        ["255", "256", "8", "1000"], "255",
        "8 bits go from 0 (all off) up to 255 (all on)."),
    mcq("Computers store pictures, music, and games as long strings of what?",
        ["1s and 0s", "letters only", "tiny photos", "magnets only"], "1s and 0s",
        "Computers store everything as bits — long strings of 1s and 0s."),
    mcq("Which value comes next after 8 when you keep doubling the binary cards?",
        ["16", "9", "10", "12"], "16",
        "Each card doubles: 1, 2, 4, 8, 16, 32... so after 8 comes 16."),
    short("What do you call a group of 8 bits?",
          "A byte", "8 bits grouped together make 1 byte."),
]

F3 = [
    mcq("When you set LED brightness with PWM, what range of numbers do you use?",
        ["0 to 255", "0 to 10", "1 to 100", "0 to 1023"], "0 to 255",
        "PWM brightness uses 0 to 255, where 0 is fully off and 255 is fully bright."),
    mcq("In the PWM brightness range, which number means fully OFF?",
        ["0", "255", "1", "128"], "0",
        "0 is the lowest value, so it means fully off; 255 means fully bright."),
    mcq("In the PWM brightness range, which number means fully BRIGHT?",
        ["255", "0", "100", "1"], "255",
        "255 is the top of the 0-255 range, so it means fully bright."),
    mcq("When the board reads an analog sensor with analogRead, what range does it give back?",
        ["0 to 1023", "0 to 255", "0 to 100", "1 to 12"], "0 to 1023",
        "analogRead gives a whole number from 0 to 1023."),
    mcq("In the analogRead range, which number is the HIGHEST reading?",
        ["1023", "255", "100", "999"], "1023",
        "1023 is the top of the 0-1023 range — the highest reading."),
    mcq("For a light sensor, a BIGGER reading number usually means…",
        ["More light", "Less light", "No power", "A broken sensor"], "More light",
        "A bigger reading means more of what the sensor measures — here, more light."),
    mcq("What is a 'range' of numbers?",
        ["The numbers from a lowest to a highest", "Only even numbers",
         "Only the number zero", "Numbers that never end"],
        "The numbers from a lowest to a highest",
        "A range is the set of numbers something can be, from its lowest to its highest."),
    mcq("Turning a 0-1023 reading into a matching 0-255 brightness is called what?",
        ["Mapping", "Blinking", "Charging", "Erasing"], "Mapping",
        "Mapping turns a number from one range into the matching spot in another range."),
    tf("analogRead gives back numbers from 0 to 255.",
       "False", "analogRead uses 0 to 1023; the 0-255 range is for PWM brightness out."),
]

BANK = {
    "topic": {
        "name": "Arduino Foundations",
        "description": "The science and coding ideas you need to understand the Elegoo Arduino kit — built for a curious grade-schooler.",
        "teaching_notes": "Target level: a smart 8-year-old, grade-6 ceiling. Keep it concrete and analogy-driven (water-in-pipes for electricity). Pair each area with its hands-on tool (PhET sims, Blockly Games). Simplifications must stay TRUE.",
    },
    "children": [
        {
            "name": "Numbers for Electronics",
            "source": {
                "title": "Numbers for Electronics — knowledge base",
                "content": KB,
            },
            "children": [
                {"name": "Time in Milliseconds", "questions": F1},
                {"name": "Binary & Bits", "questions": F2},
                {"name": "Number Ranges & Mapping", "questions": F3},
            ],
        },
    ],
}


def main():
    OUT.write_text(json.dumps(BANK, indent=2, ensure_ascii=False), encoding="utf-8")
    n = sum(len(leaf["questions"]) for leaf in BANK["children"][0]["children"])
    print(f"Wrote {OUT.relative_to(ROOT)} — {n} questions across "
          f"{len(BANK['children'][0]['children'])} sub-topics.")


if __name__ == "__main__":
    main()
