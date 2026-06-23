"""Build the Arduino Foundations → Electricity Basics question bank (sample area A).

Reads the child-facing KB markdown and emits banks/arduino-A-electricity.json in the
recursive node-tree import shape. Questions are written for a smart ~8-year-old with a
6th-grade ceiling: concrete, analogy-driven, short, and factually true.

Run:  python -m scripts.build_arduino_A   (from repo root)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = (ROOT / "research" / "arduino-foundations" / "A-electricity-basics.md").read_text(encoding="utf-8")
OUT = ROOT / "banks" / "arduino-A-electricity.json"


def mcq(prompt, choices, answer, expl):
    return {"type": "mcq", "prompt": prompt, "choices": choices, "answer": answer, "explanation": expl}


def tf(prompt, answer, expl):
    return {"type": "truefalse", "prompt": prompt, "answer": answer, "explanation": expl}


def short(prompt, answer, expl):
    return {"type": "short", "prompt": prompt, "answer": answer, "explanation": expl}


A1 = [
    mcq("Everything around us — your hand, the air, a wire — is made of tiny building blocks called what?",
        ["Atoms", "Magnets", "Volts", "Wires"], "Atoms",
        "Everything is made of atoms, pieces so small you usually can't see them."),
    mcq("Which tiny part of an atom has a negative (−) charge?",
        ["Electron", "Proton", "Neutron", "Magnet"], "Electron",
        "Electrons are negative, protons are positive, and neutrons have no charge."),
    mcq("In a metal wire, electric current is made when which tiny parts move along together?",
        ["Electrons", "Whole atoms staying in place", "Drops of water", "Beams of light"], "Electrons",
        "Electric current is moving charge — in a wire it's electrons flowing in the same direction."),
    tf("Two things with the SAME charge push away from each other.",
       "True", "Same charges repel (push apart); opposite charges attract (pull together)."),
    tf("A proton has a positive (+) charge.",
       "True", "Protons are positive, electrons are negative."),
    short("What do we call electricity that builds up and stays put — like the zap after rubbing your socks on a carpet?",
          "Static electricity",
          "Static electricity stays put; current electricity flows along in a loop."),
]

A2 = [
    mcq("If electricity were water in a pipe, the CURRENT is most like…",
        ["How much water flows through the pipe", "The pressure pushing the water",
         "How narrow the pipe is", "The color of the pipe"],
        "How much water flows through the pipe",
        "Current is how much charge flows past a spot — like how much water flows."),
    mcq("In the water picture, VOLTAGE is most like…",
        ["The pressure pushing the water", "How much water flows",
         "What the pipe is made of", "How warm the water is"],
        "The pressure pushing the water",
        "Voltage is the push that makes charge move, like water pressure."),
    mcq("RESISTANCE is most like…",
        ["A narrow or clogged pipe that slows the water", "A bigger pump",
         "Adding more water", "Making the pipe shorter"],
        "A narrow or clogged pipe that slows the water",
        "Resistance is how hard it is for charge to flow — a narrow pipe slows it down."),
    tf("A battery gives the 'push' (voltage) that makes current flow.",
       "True", "A battery is like a pump: it provides the voltage that moves the charge."),
    tf("A pipe with MORE resistance lets MORE current flow through it.",
       "False", "More resistance means LESS current — a narrower pipe lets less through."),
    short("What part of a circuit (like a pump) provides the push that makes current flow?",
          "A battery", "A battery provides the voltage — the push that moves the charge."),
]

A3 = [
    mcq("Which of these is a good CONDUCTOR of electricity?",
        ["Copper", "Rubber", "Plastic", "Glass"], "Copper",
        "Metals like copper, gold, and aluminum are good conductors."),
    mcq("Which of these is an INSULATOR (does NOT let electricity flow easily)?",
        ["Rubber", "Copper", "Gold", "Aluminum"], "Rubber",
        "Rubber, plastic, glass, and wood are insulators."),
    tf("Wires have metal inside because metal is a good conductor.",
       "True", "The metal core carries the current easily."),
    tf("Plastic is wrapped around wires because plastic is a good conductor.",
       "False", "Plastic is an INSULATOR — it keeps the electricity safely inside the wire."),
    mcq("Why are most metals good conductors?",
        ["Some of their electrons are free to move", "They are shiny",
         "They are heavy", "They feel cold"],
        "Some of their electrons are free to move",
        "Free-moving electrons can carry the current; in insulators electrons are held tightly."),
    short("A wire has a copper core wrapped in plastic. Which part is the insulator?",
          "The plastic", "Plastic is the insulator; the copper core is the conductor."),
]

A4 = [
    mcq("You turn UP the voltage (push) and keep resistance the same. The current will…",
        ["Increase", "Decrease", "Stay exactly the same", "Disappear"], "Increase",
        "More push means more current flows."),
    mcq("You turn UP the resistance and keep the voltage the same. The current will…",
        ["Decrease", "Increase", "Double", "Stay the same"], "Decrease",
        "More resistance means less current can get through."),
    tf("More resistance means less current can flow.",
       "True", "Resistance fights the flow, so higher resistance = lower current."),
    mcq("Engineers write Ohm's Law as V = I × R. What does the I stand for?",
        ["Current", "Voltage", "Resistance", "Insulator"], "Current",
        "V is voltage, I is current, and R is resistance."),
    tf("We add a resistor in front of an LED to make MORE current flow.",
       "False", "The resistor adds resistance to keep the current SMALL and safe, so the LED isn't damaged."),
    short("In Ohm's law, what happens to the current if you make the push (voltage) bigger?",
          "It increases", "More voltage pushes more current through."),
]

A5 = [
    mcq("What unit do we measure voltage in?",
        ["Volts", "Amps", "Ohms", "Grams"], "Volts",
        "Voltage is measured in volts (V)."),
    mcq("What unit do we measure electric current in?",
        ["Amps", "Volts", "Ohms", "Meters"], "Amps",
        "Current is measured in amps (A), short for amperes."),
    mcq("What unit do we measure resistance in?",
        ["Ohms", "Volts", "Amps", "Seconds"], "Ohms",
        "Resistance is measured in ohms, shown with the symbol Ω."),
    mcq("An Arduino UNO board runs on how many volts?",
        ["5 volts", "1 volt", "100 volts", "1000 volts"], "5 volts",
        "The Arduino UNO runs on 5 volts."),
    tf("'Milli' means one-thousandth, so 1000 milliseconds equals 1 second.",
       "True", "Milli = 1/1000, so 1000 ms = 1 second. This unit comes back in coding."),
    mcq("A small current, like an LED's, is about 20 mA. What does 'mA' stand for?",
        ["Milliamps", "Megavolts", "Many amps", "Milliohms"], "Milliamps",
        "mA means milliamps — thousandths of an amp — used for small currents."),
    short("How many milliseconds are in one second?",
          "1000", "Milli means one-thousandth, so there are 1000 ms in 1 second."),
]

BANK = {
    "topic": {
        "name": "Arduino Foundations",
        "description": "The science and coding ideas you need to understand the Elegoo Arduino kit — built for a curious grade-schooler.",
        "teaching_notes": "Target level: a smart 8-year-old, grade-6 ceiling. Keep it concrete and analogy-driven (water-in-pipes for electricity). Pair each area with its hands-on tool (PhET sims, Blockly Games). Simplifications must stay TRUE.",
    },
    "children": [
        {
            "name": "Electricity Basics",
            "source": {
                "title": "Electricity Basics — knowledge base",
                "content": KB,
            },
            "children": [
                {"name": "What Electricity Is (charge & electrons)", "questions": A1},
                {"name": "Current, Voltage & Resistance", "questions": A2},
                {"name": "Conductors & Insulators", "questions": A3},
                {"name": "Ohm's Law", "questions": A4},
                {"name": "Units: Volts, Amps & Ohms", "questions": A5},
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
