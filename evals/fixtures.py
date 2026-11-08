"""Fixed, non-personal fixtures for the quiz model eval. Keep them small: every
case runs once per model, and the judge sees an excerpt of each.

Changing a fixture changes the numbers, so bump `suite_version` in run.py when
you do (history is compared within a suite version)."""

WINE_KB = """\
## What wine is
- Wine is an alcoholic drink made from the fermented juice of grapes.
- Yeast converts the natural sugar in ripe grapes into alcohol (ethanol) and carbon dioxide, releasing heat.

## The end of fermentation
- Fermentation stops when the yeast has used up all the sugar, or when the alcohol level gets high enough
  (around 15% abv) to kill the yeast. A winemaker can also stop it early by chilling the wine or adding alcohol.
- If all the sugar is converted, the wine is dry. If sugar remains, it has residual sugar and tastes sweeter.

## Sweetness scale
- Dry: little or no residual sugar (e.g. Muscadet, Sancerre).
- Off-dry / medium: a touch of sweetness.
- Sweet: high residual sugar (e.g. Sauternes, made from grapes affected by noble rot).

## Fortified wines
- Fortified wines (e.g. Port, Sherry) have grape spirit added, raising the alcohol to about 15-22% abv.
- Port is fortified during fermentation, which stops it early and leaves it sweet.
"""

GENERATE = [
    {"id": "source-wine", "mode": "source", "topic": "Wine fundamentals: fermentation and sweetness",
     "source": WINE_KB, "n": 5, "difficulty": "medium", "types": ["mcq", "truefalse", "short"]},
    {"id": "topic-kids", "mode": "topic", "topic": "The water cycle (3rd grade science)",
     "n": 5, "difficulty": "easy", "types": ["mcq"]},
]

_CTX = "Subject: Wine (WSET Level 1). Chapter: Fermentation and sweetness."

VERIFY = [
    {"id": "already-correct", "context": _CTX, "expect_fix": False, "expect_answer": "alcohol and carbon dioxide",
     "question": {"type": "mcq", "prompt": "During fermentation, yeast converts grape sugar into what?",
                  "choices": ["Alcohol and carbon dioxide", "Water and oxygen", "Tannin and acid"],
                  "answer": "Alcohol and carbon dioxide", "explanation": "That is alcoholic fermentation."}},
    {"id": "wrong-tf-key", "context": _CTX, "expect_fix": True, "expect_answer": "true",
     "question": {"type": "truefalse",
                  "prompt": "Fermentation can stop on its own when the alcohol level gets high enough to kill the yeast.",
                  "choices": ["True", "False"], "answer": "False", "explanation": "Yeast never stops by itself."}},
    {"id": "wrong-mcq-key", "context": _CTX, "expect_fix": True, "expect_answer": "sauternes",
     "question": {"type": "mcq", "prompt": "Which of these is a sweet wine?",
                  "choices": ["Muscadet", "Sauternes", "Sancerre"], "answer": "Muscadet",
                  "explanation": "Muscadet is sweet."}},
]

TUTOR = [
    {"id": "kid-why-rain",
     "context": ("LEARNER NOTES: Age 8. Reads at about a 2nd-grade level. Loves dinosaurs. Gets discouraged if "
                 "answers are long.\n\nSTUDY MATERIAL:\nWater evaporates from oceans and lakes when the sun warms "
                 "it. The water vapor rises, cools, and condenses into tiny droplets that form clouds. When the "
                 "droplets join and get heavy, they fall as rain or snow (precipitation). The water collects in "
                 "rivers, lakes and oceans and the cycle repeats.\n\nQUESTION BEING STUDIED: What makes it rain?"),
     "history": [], "message": "but why does the rain fall down and not stay up in the cloud?", "max_chars": 700},
    {"id": "adult-followup",
     "context": "LEARNER NOTES: Adult studying for WSET Level 1. Wants precise terms.\n\nSTUDY MATERIAL:\n" + WINE_KB,
     "history": [{"role": "user", "content": "What is residual sugar?"},
                 {"role": "assistant", "content": "Residual sugar is the grape sugar left in the wine after "
                                                  "fermentation stops."}],
     "message": "So is residual sugar the same thing as how sweet a wine tastes?", "max_chars": 1200},
]

REVIEW = [
    {"id": "planted-bad-key", "must_flag": r"oxygen|answer key|key (looks|is|seems) (wrong|incorrect)",
     "rows": [
         {"chapter": "Fermentation", "type": "short", "prompt": "What gas is released during fermentation?",
          "answer": "Oxygen", "attempts": 9, "correct": 1, "pct": 11},
         {"chapter": "Sweetness", "type": "mcq", "prompt": "Which grape condition is used to make Sauternes?",
          "answer": "Noble rot", "attempts": 8, "correct": 3, "pct": 38},
         {"chapter": "Fortified", "type": "truefalse",
          "prompt": "Port is fortified during fermentation, which leaves it sweet.",
          "answer": "True", "attempts": 7, "correct": 3, "pct": 43},
     ]},
]

GUIDE = [
    {"id": "kid-nouns-verbs", "topic": "Nouns and verbs (2nd grade grammar)",
     "note": "For my 7 year old. Keep it fun.",
     "kb": ("- A noun is a person, place, thing or animal (girl, park, ball, dog).\n"
            "- A verb is an action word: what someone or something does (run, jump, eat).\n"
            "- Most sentences need at least one noun and one verb: 'The dog runs.'")},
]
