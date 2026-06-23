"""Build the Arduino Foundations → Physical Science Behind the Sensors question bank (area G).

Reads the child-facing KB markdown and emits banks/arduino-G-physical-science.json in the
recursive node-tree import shape. Questions are written for a smart ~8-year-old with a
6th-grade ceiling: concrete, analogy-driven, short, and factually true.

Run:  python -m scripts.build_arduino_G   (from repo root)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = (ROOT / "research" / "arduino-foundations" / "G-physical-science.md").read_text(encoding="utf-8")
OUT = ROOT / "banks" / "arduino-G-physical-science.json"


def mcq(prompt, choices, answer, expl):
    return {"type": "mcq", "prompt": prompt, "choices": choices, "answer": answer, "explanation": expl}


def tf(prompt, answer, expl):
    return {"type": "truefalse", "prompt": prompt, "answer": answer, "explanation": expl}


def short(prompt, answer, expl):
    return {"type": "short", "prompt": prompt, "answer": answer, "explanation": expl}


G1 = [
    mcq("Which tiny part MAKES light when electricity flows through it?",
        ["An LED", "A photocell", "A buzzer", "A battery"], "An LED",
        "An LED (light-emitting diode) makes light when current flows through it."),
    mcq("Which part SENSES light, so the Arduino can tell if a room is bright or dark?",
        ["A photocell", "An LED", "A speaker", "A magnet"], "A photocell",
        "A photocell (light sensor) senses light; an LED makes light."),
    mcq("Screens and the RGB LED make every color by mixing which three colors of light?",
        ["Red, green, and blue", "Red, yellow, and blue",
         "Black, white, and gray", "Orange, purple, and green"], "Red, green, and blue",
        "Mixing red, green, and blue light can make every color."),
    mcq("Red light + green light + blue light, all bright together, look like what color?",
        ["White", "Black", "Brown", "Purple"], "White",
        "Adding all three colors of light together makes white."),
    mcq("Infrared is best described as…",
        ["Light we can't see", "A loud sound", "A kind of magnet", "Very cold water"],
        "Light we can't see",
        "Infrared is real light just past the red we can see — our eyes can't see it."),
    mcq("How does a TV remote (or the kit's IR remote) send its message?",
        ["With quick blinks of infrared light", "With loud beeps",
         "With a magnet", "With a long wire"], "With quick blinks of infrared light",
        "Remotes send messages as fast blinks of invisible infrared light."),
    mcq("When you mix LIGHT, adding more colors makes things…",
        ["Brighter", "Darker", "Colder", "Heavier"], "Brighter",
        "Adding more colored light makes it brighter; mixing paint instead gets darker."),
    mcq("You turn red, green, and blue light all OFF. What do you see?",
        ["Black", "White", "Yellow", "Blue"], "Black",
        "No light at all looks black."),
    tf("Light travels in straight lines and is the fastest thing there is.",
       "True", "Light zooms in straight lines, faster than anything else."),
    tf("An LED senses light, and a photocell makes light.",
       "False", "It's the other way around: an LED makes light; a photocell senses it."),
    tf("Infrared light is something our eyes can see easily.",
       "False", "Infrared is light our eyes CANNOT see."),
    tf("Mixing red light and green light (with no blue) makes yellow.",
       "True", "Red light plus green light look yellow."),
    short("What do we call the tiny part that makes light when electricity flows through it?",
          "An LED", "An LED (light-emitting diode) makes light from electricity."),
    short("A TV remote sends its message using a kind of light we can't see. What is that light called?",
          "Infrared", "Remotes send messages as blinks of invisible infrared light."),
    short("Name one of the three colors of light that screens mix to make every color.",
          "Red", "Screens mix red, green, and blue light."),
]

G2 = [
    mcq("What makes a sound in the first place?",
        ["Something vibrating", "Something getting cold",
         "Something turning into a magnet", "A bright light"], "Something vibrating",
        "Sound is made when something vibrates — wiggles back and forth fast."),
    mcq("A FAST vibration makes a sound that is…",
        ["High-pitched", "Low-pitched", "Silent", "Colorful"], "High-pitched",
        "Faster vibration means a higher pitch; slower vibration means a lower pitch."),
    mcq("'Pitch' means how ___ a sound is.",
        ["High or low", "Loud or quiet", "Warm or cold", "Near or far"], "High or low",
        "Pitch is how high or low a sound is."),
    mcq("Frequency means…",
        ["How many wiggles happen each second", "How loud a sound is",
         "How warm something is", "How bright a light is"],
        "How many wiggles happen each second",
        "Frequency is the number of vibrations (wiggles) each second."),
    mcq("Frequency is measured in which unit?",
        ["Hertz (Hz)", "Volts (V)", "Ohms (Ω)", "Meters (m)"], "Hertz (Hz)",
        "Frequency is measured in hertz: 1 Hz means 1 wiggle per second."),
    mcq("How does a buzzer make its sound?",
        ["By vibrating", "By glowing", "By getting hot", "By spinning a wheel"], "By vibrating",
        "A buzzer makes sound by vibrating, just like other sound makers."),
    mcq("Which buzzer can play different notes because the Arduino picks its frequency?",
        ["The passive buzzer", "The active buzzer", "The photocell", "The LED"],
        "The passive buzzer",
        "A passive buzzer vibrates at the frequency the Arduino tells it, so it can play notes."),
    mcq("A tiny bird's tweet is very high, and a big drum is very low. This difference is the sound's…",
        ["Pitch", "Color", "Temperature", "Weight"], "Pitch",
        "Pitch is how high or low a sound is."),
    tf("If nothing vibrates, there is no sound.",
       "True", "Sound needs vibration — no vibration, no sound."),
    tf("Slower vibration makes a HIGHER pitch.",
       "False", "Slower vibration makes a LOWER pitch; faster makes higher."),
    tf("If you gently touch your throat while you hum, you can feel it vibrating.",
       "True", "That buzzing feeling is the vibration that makes your humming sound."),
    tf("Higher frequency means a higher pitch.",
       "True", "More wiggles per second (higher frequency) sounds higher."),
    short("Sound is made when something does what — wiggles back and forth fast?",
          "Vibrates", "Sound is made when something vibrates."),
    short("We measure how fast something vibrates as its frequency. What unit is frequency measured in?",
          "Hertz", "Frequency is measured in hertz (Hz) — wiggles per second."),
    short("Which is higher in pitch: a sound from a fast vibration or a slow vibration?",
          "Fast", "Faster vibration makes a higher pitch."),
]

G3 = [
    mcq("Temperature tells you how fast the tiny ___ in something are moving.",
        ["Molecules", "Magnets", "Wires", "Colors"], "Molecules",
        "Temperature is a measure of how fast an object's molecules are moving."),
    mcq("Something HOTTER has molecules that are…",
        ["Moving faster", "Moving slower", "Standing perfectly still", "Turning into light"],
        "Moving faster",
        "Hotter means the molecules are jiggling and moving faster."),
    mcq("Heat always flows from…",
        ["Hotter things to colder things", "Colder things to hotter things",
         "Big things to small things", "Light things to heavy things"],
        "Hotter things to colder things",
        "On its own, heat always flows from hot toward cold."),
    mcq("Why does an ice cube make your hand feel cold?",
        ["Heat flows out of your hand into the ice", "Cold flows out of the ice into your hand",
         "The ice makes your hand vibrate", "The ice turns into a magnet"],
        "Heat flows out of your hand into the ice",
        "Heat flows from your warmer hand into the colder ice, so your hand feels cold."),
    mcq("Which kit part changes its resistance when its temperature changes?",
        ["A thermistor", "An LED", "A buzzer", "A magnet"], "A thermistor",
        "A thermistor's resistance changes with temperature, so the Arduino can read the temperature."),
    mcq("The kit's DHT11 sensor measures temperature and what else?",
        ["Humidity (water vapor in the air)", "Loudness", "Brightness", "Speed"],
        "Humidity (water vapor in the air)",
        "The DHT11 measures both temperature and humidity."),
    mcq("Colder molecules are moving…",
        ["Slower", "Faster", "In a circle only", "Backward in time"], "Slower",
        "Colder means the molecules are moving more slowly."),
    mcq("A warm cookie left in a cool room will…",
        ["Cool down", "Get hotter", "Start to glow", "Become a magnet"], "Cool down",
        "Heat flows from the hot cookie to the cooler room, so the cookie cools down."),
    tf("Even in something that looks perfectly still, the molecules are always jiggling.",
       "True", "Molecules are always moving, even in things that look still."),
    tf("Heat can flow from a cold thing into a hot thing all by itself.",
       "False", "On its own, heat only flows from hotter to colder."),
    tf("A thermistor is a part whose resistance changes when its temperature changes.",
       "True", "The Arduino reads that changing resistance to find the temperature."),
    tf("Hotter means the molecules are moving more slowly.",
       "False", "Hotter means molecules move FASTER; colder means slower."),
    short("Temperature measures how fast the tiny what are moving inside something?",
          "Molecules", "Temperature is how fast an object's molecules are moving."),
    short("Heat always flows from hotter things to which kind of things?",
          "Colder", "On its own, heat flows from hot to cold."),
    short("What do we call the tool we use to measure temperature?",
          "A thermometer", "A thermometer measures temperature; the kit uses electronic ones."),
]

G4 = [
    mcq("Sound travels through the air as a…",
        ["Wave", "Magnet", "Beam of light", "Wire"], "Wave",
        "Sound travels as a wave — a moving pattern of pushes in the air."),
    mcq("When a sound wave bounces back off a hard wall, the bounced-back sound is called an…",
        ["Echo", "LED", "Atom", "Volt"], "Echo",
        "A bounced-back sound is an echo, like a shout coming back in a tunnel."),
    mcq("Which animal squeaks and listens for echoes to fly around in the dark?",
        ["A bat", "A fish", "A snail", "A worm"], "A bat",
        "Bats use echoes (echolocation) to find bugs and walls in the dark."),
    mcq("Using echoes to 'see' with sound is called…",
        ["Echolocation", "Photosynthesis", "Magnetism", "Gravity"], "Echolocation",
        "Bats and dolphins use echolocation — finding things by their echoes."),
    mcq("The ultrasonic distance sensor measures distance by…",
        ["Timing how long the echo takes to come back", "Looking at the color of an object",
         "Feeling how warm an object is", "Weighing the object"],
        "Timing how long the echo takes to come back",
        "It sends a chirp and times the echo; a longer time means a farther object."),
    mcq("With the ultrasonic sensor, a LONGER time for the echo to return means the object is…",
        ["Farther away", "Closer", "Hotter", "Heavier"], "Farther away",
        "Sound travels at a steady speed, so a longer echo time means more distance."),
    mcq("'Ultrasonic' sound is sound that is…",
        ["Too high-pitched for people to hear", "Very colorful",
         "Too quiet to matter", "Made of light"], "Too high-pitched for people to hear",
        "Ultrasonic means a pitch too high for human ears to hear."),
    mcq("Which travels FASTER through the air?",
        ["Light", "Sound", "They are exactly the same speed", "Neither one moves"], "Light",
        "Light is almost a million times faster than sound — that's why you see lightning before thunder."),
    tf("An echo is a sound that bounces back to you.",
       "True", "When a sound wave hits a hard surface, it can bounce back as an echo."),
    tf("Sound travels much faster than light.",
       "False", "It's the opposite — light is much faster than sound."),
    tf("The ultrasonic sensor works a lot like a bat using echoes.",
       "True", "Both send out sound and use the returning echo to sense what's around them."),
    tf("If the echo comes back very quickly, the object is far away.",
       "False", "A quick echo means the object is CLOSE; a slow echo means it's far."),
    short("What do we call a sound that bounces back off a hard surface?",
          "An echo", "A bounced-back sound is an echo."),
    short("Bats find their way in the dark by listening for the echoes of their squeaks. What is this skill called?",
          "Echolocation", "Using echoes to sense the world is called echolocation."),
    short("The ultrasonic sensor sends a chirp and times the echo. What does it figure out from that time?",
          "Distance", "A longer echo time means the object is farther away — that's the distance."),
]

G5 = [
    mcq("A magnet pulls strongly on which material?",
        ["Iron", "Plastic", "Wood", "Glass"], "Iron",
        "Magnets pull on iron (and steel, which is mostly iron), not on plastic or wood."),
    mcq("Every magnet has two ends called…",
        ["Poles (North and South)", "Wires", "Volts", "Atoms"], "Poles (North and South)",
        "Every magnet has a North pole and a South pole."),
    mcq("Two North poles brought close together will…",
        ["Push away from each other", "Pull together",
         "Stick forever", "Turn into iron"], "Push away from each other",
        "Same poles repel; opposite poles (N and S) attract."),
    mcq("A North pole and a South pole brought close together will…",
        ["Pull toward each other", "Push away from each other",
         "Make a sound", "Disappear"], "Pull toward each other",
        "Opposite poles attract — N pulls toward S."),
    mcq("What do you get when you wind a wire into a coil and run electric current through it?",
        ["An electromagnet", "A photocell", "A thermometer", "A battery"], "An electromagnet",
        "A coil with current flowing makes an electromagnet — a magnet you can switch on and off."),
    mcq("The best thing about an electromagnet is that you can…",
        ["Turn its magnetism on and off", "See through it",
         "Make it sing", "Eat it"], "Turn its magnetism on and off",
        "Turn the current on and it's magnetic; turn it off and the magnetism goes away."),
    mcq("What makes a motor spin?",
        ["Electromagnets pushing and pulling on magnets inside it",
         "Light shining on it", "It getting cold", "A sound playing nearby"],
        "Electromagnets pushing and pulling on magnets inside it",
        "A motor turns electricity into motion using magnetic push and pull."),
    mcq("A relay is a switch that is moved by a…",
        ["An electromagnet", "A photocell", "A beam of light", "A drop of water"],
        "An electromagnet",
        "In a relay, a tiny current works an electromagnet whose pull flips a bigger switch."),
    tf("Magnets pull on plastic and wood just as strongly as on iron.",
       "False", "Magnets pull on iron and steel, but not on plastic, wood, copper, or aluminum."),
    tf("Electricity and magnetism are connected: current flowing in a wire makes a magnetic field.",
       "True", "A flowing current makes a magnetic field — that's how electromagnets work."),
    tf("Turning the current OFF in an electromagnet makes its magnetism go away.",
       "True", "An electromagnet is magnetic only while current flows; switch it off and it stops."),
    tf("Two South poles will pull toward each other.",
       "False", "Same poles repel (push apart); only opposite poles attract."),
    short("Magnets and electromagnets make motors and relays move. What do you wind a wire into to make an electromagnet?",
          "A coil", "Winding the wire into a coil and running current through it makes an electromagnet."),
    short("Every magnet has two poles. One is North — what is the other one called?",
          "South", "Every magnet has a North pole and a South pole."),
    short("In a relay, a tiny current works an electromagnet that flips a switch. Name one other kit part that moves using electromagnets.",
          "A motor", "Motors spin using electromagnets pushing and pulling on magnets inside."),
]

BANK = {
    "topic": {
        "name": "Arduino Foundations",
        "description": "The science and coding ideas you need to understand the Elegoo Arduino kit — built for a curious grade-schooler.",
        "teaching_notes": "Target level: a smart 8-year-old, grade-6 ceiling. Keep it concrete and analogy-driven (water-in-pipes for electricity). Pair each area with its hands-on tool (PhET sims, Blockly Games). Simplifications must stay TRUE.",
    },
    "children": [
        {
            "name": "Physical Science Behind the Sensors",
            "source": {
                "title": "Physical Science — knowledge base",
                "content": KB,
            },
            "children": [
                {"name": "Light", "questions": G1},
                {"name": "Sound", "questions": G2},
                {"name": "Heat & Temperature", "questions": G3},
                {"name": "Sound Waves & Echo", "questions": G4},
                {"name": "Magnetism & Electromagnets", "questions": G5},
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
