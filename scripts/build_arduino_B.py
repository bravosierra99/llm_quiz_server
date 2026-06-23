"""Build the Arduino Foundations → Circuits question bank (area B).

Reads the child-facing KB markdown and emits banks/arduino-B-circuits.json in the
recursive node-tree import shape. Questions are written for a smart ~8-year-old with a
6th-grade ceiling: concrete, analogy-driven, short, and factually true.

Run:  python -m scripts.build_arduino_B   (from repo root)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = (ROOT / "research" / "arduino-foundations" / "B-circuits.md").read_text(encoding="utf-8")
OUT = ROOT / "banks" / "arduino-B-circuits.json"


def mcq(prompt, choices, answer, expl):
    return {"type": "mcq", "prompt": prompt, "choices": choices, "answer": answer, "explanation": expl}


def tf(prompt, answer, expl):
    return {"type": "truefalse", "prompt": prompt, "answer": answer, "explanation": expl}


def short(prompt, answer, expl):
    return {"type": "short", "prompt": prompt, "answer": answer, "explanation": expl}


B1 = [
    mcq("What is a circuit?",
        ["A complete loop that current can travel around", "A single straight wire with one end",
         "A pile of batteries", "A kind of metal"], "A complete loop that current can travel around",
        "A circuit is a complete loop: source → wire → load → back to the source."),
    mcq("In a circuit, what do we call the part that DOES a job with the electricity, like a light or a buzzer?",
        ["The load", "The source", "The wire", "The gap"], "The load",
        "The load is the part that uses the electricity to do something, like an LED or a motor."),
    mcq("In a circuit, what usually supplies the push (the voltage)?",
        ["The source, like a battery", "The load, like a bulb",
         "The plain wire", "A gap in the loop"], "The source, like a battery",
        "The source — usually a battery — provides the voltage that moves the current."),
    tf("If there is a break or gap anywhere in the loop, the current stops.",
       "True", "A circuit only works when the loop is complete; any gap stops the flow."),
    tf("A circuit can work even when the loop has a gap in it.",
       "False", "The loop must be complete — a gap anywhere stops the current."),
    short("A circuit is a complete WHAT that current travels around?",
          "Loop", "A circuit is a complete loop: source → wire → load → back again."),
    mcq("What does a switch do in a circuit?",
        ["Makes or breaks the loop to turn the load on or off", "Adds more electricity to the battery",
         "Changes copper into rubber", "Makes the wire longer"],
        "Makes or breaks the loop to turn the load on or off",
        "A switch completes the loop (on) or opens a gap in it (off)."),
    mcq("You unplug one wire so the loop has a gap. What happens to the light bulb?",
        ["It turns off", "It gets brighter", "It stays exactly the same", "It changes color"], "It turns off",
        "A gap breaks the loop, so the current stops and the load turns off."),
    mcq("Which three things does a circuit usually need?",
        ["A source, a path (wire), and a load", "Three batteries and nothing else",
         "Only a wire", "Water, a pipe, and a pump"], "A source, a path (wire), and a load",
        "A circuit needs a source (push), a path (wire), and usually a load (the thing powered)."),
    mcq("A circuit is like a toy train on a circular track. What happens if you lift out one piece of track?",
        ["The train stops because the loop is broken", "The train speeds up",
         "The train jumps the gap", "Nothing changes"], "The train stops because the loop is broken",
        "Just like current, the train can only keep going if the loop is unbroken."),
    tf("When a battery dies, it can break a circuit just like a loose wire can.",
       "True", "A dead battery stops supplying the push, so the loop no longer works."),
    tf("When a circuit is broken, there is leftover electricity that keeps the load running for a while.",
       "False", "There is no leftover flow — if the loop is open, the current stops everywhere in it."),
    short("In a circuit, what do we call the path that the current travels along, usually made of copper?",
          "The wire", "The wire is the conductor path the current travels along."),
    short("What part of a circuit do you flip to complete or break the loop on purpose?",
          "A switch", "A switch makes or breaks the loop to turn the load on or off."),
    mcq("Connecting a battery straight back to itself with only wire and no load is called a…",
        ["Short circuit", "Parallel circuit", "Schematic", "Switch"], "Short circuit",
        "A short circuit has no load to limit the current, so the wire and battery get very hot — it's dangerous."),
]

B2 = [
    mcq("A battery has two different ends, + and −. What is this 'two different ends' idea called?",
        ["Polarity", "Gravity", "Resistance", "A schematic"], "Polarity",
        "Polarity means the two ends are different: a positive (+) terminal and a negative (−) terminal."),
    mcq("What do we call the + end and the − end of a battery?",
        ["Terminals", "Loads", "Switches", "Insulators"], "Terminals",
        "The ends of a battery are its terminals: the positive (+) terminal and the negative (−) terminal."),
    tf("Connecting only the + side of a battery is enough to make current flow.",
       "False", "The charge needs a full path back to the other terminal, or nothing flows."),
    mcq("Why does current need a complete path back to the battery?",
        ["So the charge has a way to return all the way around the loop", "So the battery can melt",
         "So the wire turns to gold", "It doesn't — one wire is enough"],
        "So the charge has a way to return all the way around the loop",
        "Current only flows if it can leave one terminal and return to the other — a full loop."),
    mcq("By the agreement engineers use, current is drawn flowing OUT of which terminal?",
        ["The positive (+) terminal", "The negative (−) terminal",
         "The ground only", "Neither one"], "The positive (+) terminal",
        "Conventional current is drawn leaving +, going around the loop, and returning to −."),
    short("What is the agreed-upon direction engineers use to DRAW current called? (Two words.)",
          "Conventional current", "Conventional current is drawn from + around the loop back to −."),
    mcq("What does GND stand for in electronics?",
        ["Ground", "Gold", "Grand", "Gadget"], "Ground",
        "GND stands for ground, the common 0-volt reference point in the circuit."),
    mcq("On an Arduino, GND (ground) is best described as…",
        ["The common 0-volt point everything is measured against", "A wire stuck into the dirt outside",
         "The most positive point in the circuit", "The brightest LED"],
        "The common 0-volt point everything is measured against",
        "Ground is the 0-volt reference and the − (return) side of the circuit, not the dirt outside."),
    tf("On a battery-powered Arduino, 'ground' means a wire pushed into the soil outside.",
       "False", "In small electronics, ground is the circuit's own 0-volt reference point, not the earth."),
    tf("Voltage is always a difference between two points, so we pick ground as the 'zero' to measure from.",
       "True", "Ground is the agreed 0 volts; the 5V pin is 5 volts ABOVE ground."),
    mcq("The 5V pin on an Arduino is 5 volts measured compared to what?",
        ["Ground (0 volts)", "The sun", "The biggest LED", "100 volts"], "Ground (0 volts)",
        "Ground is the 0-volt reference; the 5V pin sits 5 volts above it."),
    mcq("An LED only lets current through one way, so when you place it you must…",
        ["Put it in the right way around (mind its polarity)", "Soak it in water first",
         "Connect only its long leg", "Place it any way — it never matters"],
        "Put it in the right way around (mind its polarity)",
        "An LED has polarity: it only works when its + and − sides face the right way."),
    tf("A plain resistor works no matter which way around you connect it.",
       "True", "A plain resistor has no polarity, so either direction works (unlike an LED)."),
    short("What single word means a part has a + side and a − side that must face the right way?",
          "Polarity", "Polarity is having distinct + and − ends, like a battery or an LED."),
    short("GND is short for what word?",
          "Ground", "GND means ground — the 0-volt reference and return side of the circuit."),
]

B3 = [
    mcq("In a SERIES circuit, how many paths does the current have to follow?",
        ["One single path", "Many separate paths", "No path at all", "Exactly five paths"], "One single path",
        "Series means in a line: one single loop runs through every part, one after another."),
    mcq("In a PARALLEL circuit, the current has…",
        ["More than one path (multiple branches)", "Only one single path",
         "No path back to the source", "A path made of rubber"], "More than one path (multiple branches)",
        "Parallel means side-by-side: each part gets its own branch, so there are multiple paths."),
    mcq("'In a line, one after another' describes which kind of circuit?",
        ["Series", "Parallel", "Short", "Broken"], "Series",
        "Series parts are connected end-to-end so one single path runs through all of them."),
    mcq("'Side-by-side, each with its own branch' describes which kind of circuit?",
        ["Parallel", "Series", "Schematic", "Ground"], "Parallel",
        "Parallel parts each get their own branch back to the source."),
    tf("In a series circuit, if one part breaks, everything goes off.",
       "True", "There's only one path, so breaking it anywhere opens the whole loop."),
    tf("In a parallel circuit, if one branch breaks, the other branches keep working.",
       "True", "Each branch is its own loop, so the others still have a complete path."),
    tf("In a parallel circuit, breaking one branch turns off every other branch too.",
       "False", "Only the broken branch stops; the other branches keep their own complete paths."),
    short("Old holiday lights where ONE burned-out bulb made the WHOLE string go dark were wired how?",
          "Series", "Series has one single path, so one broken bulb opens the whole loop."),
    mcq("The lights in different rooms of a house can be turned off one at a time without affecting the others. How are they wired?",
        ["Parallel", "Series", "In a short circuit", "In a single line"], "Parallel",
        "Parallel gives each light its own branch, so turning one off leaves the others on."),
    mcq("Series is like a single-lane road. What happens if one car stalls?",
        ["The whole line stops", "The other cars drive around it",
         "The road gets wider", "Nothing — traffic keeps flowing"], "The whole line stops",
        "With only one path, one blockage stops everyone — just like a series circuit."),
    mcq("Parallel is like a road that splits into several lanes. If one lane is blocked…",
        ["Traffic still gets through on the other lanes", "All lanes stop",
         "The road disappears", "Cars turn into bulbs"], "Traffic still gets through on the other lanes",
        "Multiple paths mean blocking one still leaves the others open — like a parallel circuit."),
    tf("Series means the parts are connected end-to-end in a single loop.",
       "True", "Series parts share one single path, one after another."),
    short("How many paths does the current have in a PARALLEL circuit — one, or more than one?",
          "More than one", "Parallel circuits have multiple branches, so the current has more than one path."),
    short("A switch is usually placed in SERIES with a part. What word means 'in a line, one single path'?",
          "Series", "Series means in a line; a series switch can open the one path to turn the part off."),
    mcq("Builders often put several LEDs in PARALLEL on a breadboard. Why?",
        ["So each one lights up on its own branch independently", "So one burnout turns them all off",
         "To make them share a single path", "To turn them into resistors"],
        "So each one lights up on its own branch independently",
        "Parallel gives each LED its own path, so they light independently of each other."),
]

B4 = [
    mcq("What is a schematic?",
        ["A map of a circuit that uses symbols to show connections", "A photograph of the real parts",
         "A kind of battery", "A long copper wire"], "A map of a circuit that uses symbols to show connections",
        "A schematic shows how parts connect, using symbols instead of pictures of the real parts."),
    mcq("A schematic is most like which of these?",
        ["A subway map showing which stops connect", "A photo of a real circuit board",
         "A ruler that measures distance", "A bag of resistors"], "A subway map showing which stops connect",
        "Like a subway map, a schematic shows what connects to what, not what things look like."),
    tf("On a schematic, a line between two symbols means a wire connects them.",
       "True", "Lines are wires; they show that two parts are joined by a connection."),
    mcq("On a schematic, what does a DOT where two lines cross usually mean?",
        ["The wires are truly connected there", "The wires are broken there",
         "There is a battery there", "Nothing at all"], "The wires are truly connected there",
        "A junction dot means a real connection; no dot usually means the wires just cross without touching."),
    tf("A schematic shows the real-life distance between parts on the board.",
       "False", "A schematic shows the CONNECTIONS, not the real shape or distance — parts may be far apart in real life."),
    short("A schematic uses simple SYMBOLS instead of pictures to show what?",
          "How parts connect", "A schematic maps which parts are connected to which."),
    mcq("What is a breadboard used for?",
        ["Building circuits by pushing in wires and parts, with no soldering", "Cutting bread",
         "Storing batteries only", "Measuring voltage"], "Building circuits by pushing in wires and parts, with no soldering",
        "A breadboard lets you build and change circuits quickly with no soldering."),
    mcq("Inside a breadboard, what connects certain holes together?",
        ["Hidden metal strips", "Tiny magnets", "Drops of water", "Glued paper"], "Hidden metal strips",
        "Hidden metal strips under the plastic join groups of holes so parts on a strip are wired together."),
    tf("On a breadboard, the five holes in one little row-segment on one side of the center gap are connected to each other.",
       "True", "Each five-hole segment on one side of the gap shares a metal strip, so those holes are joined."),
    tf("On a breadboard, the center gap connects the left side of a row to the right side.",
       "False", "The center gap SEPARATES the two sides — a row on the left is not connected to the row on the right."),
    mcq("Why does a breadboard have a gap (ravine) down the middle?",
        ["So you can straddle a chip across it without shorting its two sides together", "To make it look nice",
         "To hold extra wires", "To store electricity"],
        "So you can straddle a chip across it without shorting its two sides together",
        "The gap keeps the two sides apart so a chip's two rows of legs aren't connected to each other."),
    mcq("The long + (red) and − (blue) strips along the edges of a breadboard are called the…",
        ["Power rails", "Center gap", "Schematic", "Loads"], "Power rails",
        "The power rails run the long way down the edges to carry power (+) and ground (−) anywhere on the board."),
    tf("The long power rails run the OPPOSITE direction from the little five-hole rows.",
       "True", "Power rails run the long way down the edges; the five-hole rows run across, toward the center gap."),
    short("On a breadboard, what carries power and ground along the long edges? (Two words.)",
          "Power rails", "The +/− power rails run down the edges to bring power and ground anywhere."),
    short("A schematic tells you WHAT should connect. What board do you use to actually MAKE the connections without soldering?",
          "A breadboard", "A breadboard is where you build the circuit by pushing parts into connected holes."),
]

BANK = {
    "topic": {
        "name": "Arduino Foundations",
        "description": "The science and coding ideas you need to understand the Elegoo Arduino kit — built for a curious grade-schooler.",
        "teaching_notes": "Target level: a smart 8-year-old, grade-6 ceiling. Keep it concrete and analogy-driven (water-in-pipes for electricity). Pair each area with its hands-on tool (PhET sims, Blockly Games). Simplifications must stay TRUE.",
    },
    "children": [
        {
            "name": "Circuits",
            "source": {
                "title": "Circuits — knowledge base",
                "content": KB,
            },
            "children": [
                {"name": "What a Circuit Is", "questions": B1},
                {"name": "Polarity & Ground", "questions": B2},
                {"name": "Series vs Parallel", "questions": B3},
                {"name": "Schematics & Breadboards", "questions": B4},
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
