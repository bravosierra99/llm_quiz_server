"""Build the Arduino Foundations → Signals & Sensors question bank (area D).

Reads the child-facing KB markdown and emits banks/arduino-D-signals-sensors.json in the
recursive node-tree import shape. Questions are written for a smart ~8-year-old with a
6th-grade ceiling: concrete, analogy-driven, short, and factually true.

Run:  python -m scripts.build_arduino_D   (from repo root)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = (ROOT / "research" / "arduino-foundations" / "D-signals-sensors.md").read_text(encoding="utf-8")
OUT = ROOT / "banks" / "arduino-D-signals-sensors.json"


def mcq(prompt, choices, answer, expl):
    return {"type": "mcq", "prompt": prompt, "choices": choices, "answer": answer, "explanation": expl}


def tf(prompt, answer, expl):
    return {"type": "truefalse", "prompt": prompt, "answer": answer, "explanation": expl}


def short(prompt, answer, expl):
    return {"type": "short", "prompt": prompt, "answer": answer, "explanation": expl}


D1 = [
    mcq("When the board SENSES the world (information comes IN), that is called…",
        ["Input", "Output", "A battery", "A resistor"], "Input",
        "Input means the board senses the world — information comes in."),
    mcq("When the board DOES something in the world (a signal goes OUT), that is called…",
        ["Output", "Input", "An atom", "A wire"], "Output",
        "Output means the board sends a signal out to make something happen."),
    mcq("A button that you press is an example of…",
        ["An input", "An output", "A battery", "A resistor"], "An input",
        "A button is an input — pressing it tells the board something."),
    mcq("An LED that the board turns on is an example of…",
        ["An output", "An input", "A sensor", "A switch you press"], "An output",
        "An LED is an output — the board makes it light up."),
    mcq("Which of these is an OUTPUT (the board doing something)?",
        ["A buzzer making a sound", "A button being pressed",
         "A light sensor reading the room", "A tilt switch being tipped"],
        "A buzzer making a sound",
        "A buzzer is an output — the board makes it buzz. The others are inputs."),
    mcq("Which of these is an INPUT (the board sensing something)?",
        ["A light sensor reading the room", "An LED lighting up",
         "A motor spinning", "A buzzer beeping"], "A light sensor reading the room",
        "A light sensor is an input — it senses the world for the board."),
    mcq("A common pattern for a project is…",
        ["Input → think → output", "Output → input → battery",
         "Resistor → wire → atom", "Volt → amp → ohm"], "Input → think → output",
        "The board reads an input, decides what to do, then drives an output."),
    mcq("'The board's eyes and ears' is a good picture for…",
        ["Input", "Output", "A resistor", "A battery"], "Input",
        "Input is like the board's eyes and ears — how it senses the world."),
    mcq("'The board's hands and voice' is a good picture for…",
        ["Output", "Input", "A wire", "An atom"], "Output",
        "Output is like the board's hands and voice — how it acts on the world."),
    tf("Input means information comes IN to the board (it senses the world).",
       "True", "Input = the board senses the world; information comes in."),
    tf("An LED that lights up is an example of an input.",
       "False", "An LED is an OUTPUT — the board makes it do something."),
    tf("A motor that the board spins is an output.",
       "True", "A motor is an output — the board makes it move."),
    tf("A pin on the board can be set up as an input OR an output (you choose in the program).",
       "True", "The same pin can be input or output, but does one job at a time."),
    short("Press a button to light an LED. Which part is the OUTPUT — the button or the LED?",
          "The LED", "The LED is the output; the button is the input."),
    short("Sensing the world is called input. What is it called when the board DOES something out in the world?",
          "Output", "Output is when the board sends a signal out to make something happen."),
]

D2 = [
    mcq("A DIGITAL signal has how many values?",
        ["Only two (on or off)", "A smooth range of many",
         "Exactly ten", "An unlimited number"], "Only two (on or off)",
        "Digital means just two values: ON or OFF (also called HIGH/LOW or 1/0)."),
    mcq("An ANALOG signal is best described as…",
        ["A smooth range of many values", "Only on or off",
         "Always exactly 5 volts", "Just the number zero"],
        "A smooth range of many values",
        "Analog is a smooth range — like a dimmer or a volume knob."),
    mcq("Which everyday thing works like a DIGITAL signal?",
        ["A normal light switch (up or down)", "A dimmer slider",
         "A volume knob", "A ramp"], "A normal light switch (up or down)",
        "A light switch is either up or down — two values, like digital."),
    mcq("Which everyday thing works like an ANALOG signal?",
        ["A dimmer switch", "A normal on/off light switch",
         "A doorbell button", "A light that is either on or off"], "A dimmer switch",
        "A dimmer can be anywhere from low to high — a smooth range, like analog."),
    mcq("A button (pressed or not pressed) is which kind of signal?",
        ["Digital", "Analog", "Both at once", "Neither"], "Digital",
        "A button has just two values — pressed or not — so it is digital."),
    mcq("On an Arduino UNO, a digital output pin is set to which two values?",
        ["Full voltage (ON) or zero (OFF)", "Any value from 0 to 1023",
         "Always 1.5 volts", "A smooth range"], "Full voltage (ON) or zero (OFF)",
        "Digital output is full voltage (5 V, ON) or zero (0 V, OFF) — two values."),
    mcq("Which of these is naturally ANALOG (it varies smoothly)?",
        ["How bright the room is", "Whether a button is pressed",
         "Whether a light is on or off", "Whether a door is open or shut"],
        "How bright the room is",
        "Room brightness can be any amount in between — it varies smoothly (analog)."),
    mcq("A staircase with only a top step and a bottom step is a picture of…",
        ["Digital (two values)", "Analog (a smooth range)",
         "Voltage", "Resistance"], "Digital (two values)",
        "Two steps and nothing between = digital. A smooth ramp = analog."),
    mcq("A smooth ramp you can stop anywhere along is a picture of…",
        ["Analog", "Digital", "A button", "An on/off switch"], "Analog",
        "A smooth ramp = analog (many values). Two steps = digital."),
    tf("Digital means only two values: ON or OFF.",
       "True", "Digital is two values — ON or OFF (HIGH/LOW, 1/0)."),
    tf("Analog signals can only be on or off, nothing in between.",
       "False", "That describes digital. Analog is a smooth range of many values."),
    tf("A volume knob that slides smoothly from quiet to loud is like an analog signal.",
       "True", "A volume knob is a smooth range — that's analog."),
    tf("The world outside is mostly analog, but computers think in digital.",
       "True", "Most real things vary smoothly (analog); computers use on/off (digital)."),
    short("A normal light switch is either up or down. Is that digital or analog?",
          "Digital", "Two values (up or down) means digital."),
    short("A dimmer switch can be set to any brightness in between. Is that digital or analog?",
          "Analog", "A smooth range of values is analog."),
]

D3 = [
    mcq("What does PWM let the board do with an LED?",
        ["Make it look half-bright (dim it)", "Turn it into a sensor",
         "Make it into a battery", "Cool it down"], "Make it look half-bright (dim it)",
        "PWM dims an LED (or slows a motor) by controlling how much of the time it's ON."),
    mcq("How does PWM actually work?",
        ["It switches the pin ON and OFF very fast", "It lowers the voltage smoothly",
         "It removes the resistor", "It cools the wire"],
        "It switches the pin ON and OFF very fast",
        "PWM blinks the pin ON/OFF fast; each ON is still full voltage."),
    mcq("When a PWM pin is ON, how much voltage is it putting out?",
        ["Full voltage (it is fully ON)", "Half voltage", "Zero", "A tiny trickle"],
        "Full voltage (it is fully ON)",
        "PWM doesn't turn the voltage down — when ON it's full voltage; it changes the ON-time."),
    mcq("With PWM, MORE on-time means the LED is…",
        ["Brighter", "Dimmer", "Off", "Cooler"], "Brighter",
        "More on-time = more average power = brighter LED (or faster motor)."),
    mcq("With PWM, LESS on-time means the motor runs…",
        ["Slower", "Faster", "Backwards", "Hotter"], "Slower",
        "Less on-time = less average power = slower motor (or dimmer LED)."),
    mcq("On the Arduino, what PWM number means always OFF?",
        ["0", "255", "128", "1023"], "0",
        "PWM goes 0 to 255. 0 = always OFF; 255 = always ON."),
    mcq("On the Arduino, what PWM number means always ON (full bright)?",
        ["255", "0", "128", "1023"], "255",
        "PWM goes 0 to 255. 255 = always ON (full bright/full speed)."),
    mcq("A PWM value of 128 (about halfway) means the pin is ON…",
        ["About half the time", "All of the time",
         "None of the time", "Only once"], "About half the time",
        "128 is roughly halfway, so the pin is ON about half the time — about half bright."),
    mcq("Why can't your eyes see the PWM blinking?",
        ["It happens far too fast to see", "The LED is invisible",
         "The room is dark", "It only blinks once a year"],
        "It happens far too fast to see",
        "PWM blinks hundreds of times a second — too fast to see, so it looks steady."),
    mcq("PWM is called 'fake-analog' because…",
        ["The result looks smooth, but the pin is only ever fully ON or OFF",
         "It uses fake electricity", "It only works on real analog parts",
         "It turns the voltage down"],
        "The result looks smooth, but the pin is only ever fully ON or OFF",
        "It looks like a smooth in-between value, but really it's just fast on/off."),
    tf("PWM works by switching the pin ON and OFF very fast.",
       "True", "PWM blinks the pin fast; the average ON-time sets the brightness/speed."),
    tf("PWM dims an LED by turning the voltage down to a low value.",
       "False", "PWM keeps full voltage when ON — it changes how much TIME the pin is ON."),
    tf("With PWM, a higher on-time makes an LED brighter.",
       "True", "More on-time = more average power = brighter."),
    short("On the Arduino, PWM uses numbers from 0 to what biggest number?",
          "255", "PWM goes from 0 (always off) to 255 (always on)."),
    short("PWM makes an LED look dim even though the pin is only ever fully on or fully off. What makes it look steady instead of blinking?",
          "It blinks too fast to see", "It blinks hundreds of times a second — too fast for your eyes."),
]

D4 = [
    mcq("What does a SENSOR do?",
        ["Changes something physical into electricity the board can measure",
         "Stores electricity like a battery", "Only makes light",
         "Blocks all current"],
        "Changes something physical into electricity the board can measure",
        "A sensor turns light, heat, distance, or tilt into electricity (then a number)."),
    mcq("A photocell senses…",
        ["Light", "Temperature", "Distance", "Smell"], "Light",
        "A photocell senses light — its resistance changes with brightness."),
    mcq("In bright light, a photocell's resistance…",
        ["Goes down", "Goes up to infinity", "Disappears", "Turns into voltage"],
        "Goes down",
        "Bright light lowers a photocell's resistance; darkness raises it."),
    mcq("Which sensor's resistance changes with TEMPERATURE?",
        ["A thermistor", "A photocell", "An ultrasonic sensor", "A tilt switch"],
        "A thermistor",
        "A thermistor is a resistor whose resistance changes with temperature."),
    mcq("How does an ultrasonic sensor measure DISTANCE?",
        ["It sends a sound pulse and times the echo coming back",
         "It weighs the object", "It tastes the air", "It counts the lights"],
        "It sends a sound pulse and times the echo coming back",
        "It times the echo; the longer the echo takes, the farther the object is."),
    mcq("With an ultrasonic sensor, a LONGER echo time means the object is…",
        ["Farther away", "Closer", "Brighter", "Hotter"], "Farther away",
        "Sound travels at a steady speed, so a longer echo means a farther object."),
    mcq("Bats find things in the dark by listening for echoes. What is this trick called?",
        ["Echolocation", "Photosynthesis", "Gravity", "Magnetism"], "Echolocation",
        "Echolocation — the same idea the ultrasonic distance sensor uses."),
    mcq("A tilt switch senses…",
        ["Whether it is tipped or flat", "How bright the room is",
         "The exact temperature", "The distance to a wall"],
        "Whether it is tipped or flat",
        "A tilt switch has a tiny ball that opens/closes a circuit when tipped."),
    mcq("Which sensor gives just TWO values (digital), not a smooth range?",
        ["A tilt switch", "A photocell", "A thermistor", "An ultrasonic sensor"],
        "A tilt switch",
        "A tilt switch is digital (tipped or not); the others give a range."),
    mcq("A photocell turns light into a changing _____ that the board reads as a number.",
        ["Resistance (and then voltage)", "Battery", "Magnet", "Sound"],
        "Resistance (and then voltage)",
        "Its resistance changes with light; the circuit turns that into a number."),
    tf("A sensor turns something physical (like light or heat) into a number the board can use.",
       "True", "Sensors translate the world into electricity, then numbers."),
    tf("An ultrasonic sensor measures distance by timing a sound echo.",
       "True", "It times how long the echo takes to bounce back."),
    tf("A thermistor's resistance changes when its temperature changes.",
       "True", "That's how it lets the board work out the temperature."),
    short("A photocell senses how bright the room is. What physical thing does a thermistor sense?",
          "Temperature", "A thermistor senses temperature — its resistance changes with heat."),
    short("Inside an ultrasonic distance sensor, what does it listen for after sending out a sound pulse?",
          "The echo", "It times the echo bouncing back to work out distance."),
]

BANK = {
    "topic": {
        "name": "Arduino Foundations",
        "description": "The science and coding ideas you need to understand the Elegoo Arduino kit — built for a curious grade-schooler.",
        "teaching_notes": "Target level: a smart 8-year-old, grade-6 ceiling. Keep it concrete and analogy-driven (water-in-pipes for electricity). Pair each area with its hands-on tool (PhET sims, Blockly Games). Simplifications must stay TRUE.",
    },
    "children": [
        {
            "name": "Signals & Sensors",
            "source": {
                "title": "Signals & Sensors — knowledge base",
                "content": KB,
            },
            "children": [
                {"name": "Input vs Output", "questions": D1},
                {"name": "Digital vs Analog", "questions": D2},
                {"name": "PWM (Fake-Analog)", "questions": D3},
                {"name": "Sensors: Turning the World into Numbers", "questions": D4},
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
