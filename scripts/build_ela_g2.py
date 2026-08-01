#!/usr/bin/env python3
"""Build a comprehensive Grade 2 English Language Arts (ELA / Reading) bank.

Aligned to the Maryland College and Career-Ready Standards for English Language
Arts, Grade 2 (MSDE framework, built on the Common Core ELA standards) — the
standards Anne Arundel County Public Schools (AACPS) teaches to (via the Core
Knowledge Language Arts curriculum, measured with DIBELS). Strands: Reading
Foundational Skills (RF.2), Reading Literature (RL.2), Reading Informational
Text (RI.2), Language (L.2), and Writing (W.2).

Follow-on to banks/ela-g1.json: the grade-2 reading half of the
grade-acceleration review set (see scripts/build_ela_g1.py for the rationale —
AACPS keys acceleration on READING and MATH achievement).

Everything is TEXT-ONLY (no "look at the picture", no audio). Comprehension
items carry their short passage INLINE in the prompt so the question is
self-contained. Each chapter carries a plain-language knowledge base (for a
6-8 year old / a parent reading along) that also serves as source material the
app can quote when explaining a topic.

Run:  python scripts/build_ela_g2.py   ->  writes banks/ela-g2.json
"""
import json
import os
import random

random.seed(2)  # deterministic output so re-runs don't churn the bank

OUT = os.path.join(os.path.dirname(__file__), "..", "banks", "ela-g2.json")


# --- small builders (identical contract to build_ela_g1.py) -----------------
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


SRC = ("\n\n## Sources\n"
       "- MSDE, *Grade 2 Maryland College and Career Readiness Standards* "
       "(ELA standards sheet).\n"
       "- Common Core State Standards for ELA, Grade 2.\n"
       "- AACPS Elementary Reading (Integrated Literacy / CKLA).\n")


# --- Chapter 1: Long & Short Vowels + Silent E (RF.2.3a) --------------------
def ch_long_short():
    qs = [
        mcq("Which word has a LONG a (the a says its name)?",
            "cake", ["cat", "map", "hand"],
            "In 'cake' the silent e makes the a say its name: /ay/. "
            "Cat, map, and hand all have the short a."),
        mcq("Which word has a SHORT i?",
            "sit", ["bike", "light", "tie"],
            "'Sit' is a closed syllable, so the i is short. Bike, light, and "
            "tie all have the long i."),
        mcq("Add a silent e to 'kit'. What word do you get?",
            "kite", ["kitten", "kits", "kid"],
            "kit + e = kite. The silent e makes the i say its name."),
        mcq("In the word 'cape', what does the final e do?",
            "It is silent and makes the a long",
            ["It is read out loud", "It makes the a short", "It does nothing"],
            "The 'magic e' is silent — its job is to make the earlier vowel "
            "say its name: cap → cape."),
        mcq("The word 'hop' ends in a consonant (a closed syllable). Its vowel "
            "sound is usually ____.",
            "short", ["long", "silent", "loud"],
            "A closed syllable (vowel then consonant) usually has a SHORT "
            "vowel: hop, cap, sit."),
        mcq("The word 'go' ends with its vowel (an open syllable). The o says "
            "____.",
            "its name (long o)", ["its short sound", "nothing", "/j/"],
            "An open syllable ends with the vowel, and the vowel is usually "
            "LONG: go, he, hi, my."),
        mcq("Which word means a toy that flies on a string: 'kit' or 'kite'?",
            "kite", ["kit"],
            "The silent e changes the word AND the meaning: a kit is a set of "
            "things; a kite flies in the sky."),
        mcq("Which pair shows a short vowel changing to a long vowel when "
            "silent e is added?",
            "rob → robe", ["run → runs", "hop → hops", "red → reds"],
            "rob → robe: the o changes from short to long. Adding -s never "
            "changes the vowel sound."),
        mcq("Which word has a SHORT u?",
            "cup", ["cute", "use", "mule"],
            "'Cup' is closed, so the u is short. Cute, use, and mule have the "
            "long u."),
        mcq("Which word has a LONG o?",
            "bone", ["hot", "stop", "frog"],
            "The silent e in 'bone' makes the o long. Hot, stop, and frog "
            "have the short o."),
        tf("The long sound of a vowel 'says the letter's name.'",
           True, "Long a says 'a' (cake), long e says 'e' (he), long i says "
           "'i' (bike), and so on."),
        tf("In 'cube', you say the final e out loud.",
           False, "The final e is SILENT — its job is to make the u long."),
        tf("'Plan' and 'plane' have the same vowel sound.",
           False, "'Plan' has a short a; the silent e in 'plane' makes the a "
           "long."),
        short("Add a silent e to 'tub' to make a new word. What is it?",
              "tube", "tub + e = tube. The u changes from short to long."),
        short("Is the vowel sound in 'stop' long or short?",
              "short", "'Stop' is a closed syllable, so the o is short."),
    ]
    kb = (
        "# Grade 2 ELA — Long & Short Vowels + Silent E\n\n"
        "**Standard: RF.2.3a** — tell long and short vowels apart in regularly "
        "spelled one-syllable words.\n\n"
        "## Big ideas\n"
        "- Every vowel (a, e, i, o, u) has a **short** sound (cat, bed, sit, "
        "hot, cup) and a **long** sound — the long sound **says the letter's "
        "name** (cake, he, bike, bone, cute).\n"
        "- **Closed syllable** (ends in a consonant): vowel is usually "
        "**short** — cap, hid, hop, cub.\n"
        "- **Open syllable** (ends with the vowel): vowel is usually **long** "
        "— he, go, hi, my.\n"
        "- **Silent e (magic e)**: a final e is silent and makes the earlier "
        "vowel **long** — cap→cape, kit→kite, hop→hope, cub→cube, tub→tube, "
        "can→cane, mad→made, plan→plane, rob→robe.\n"
        "- Silent e changes the **meaning** too: a kit is a set of things; a "
        "kite flies." + SRC)
    return {"name": "Long & Short Vowels + Silent E",
            "source": {"title": "Long & short vowels — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 2: Vowel Teams & Diphthongs (RF.2.3b) --------------------------
def ch_vowel_teams():
    qs = [
        mcq("What sound do the letters 'ai' make in 'rain'?",
            "long a", ["short a", "long i", "short e"],
            "'ai' is a vowel team for long a: rain, mail, train, paint."),
        mcq("Which spelling of long a usually comes at the END of a word?",
            "ay (like 'play')", ["ai (like 'rain')", "a_e (like 'cake')",
            "au (like 'haul')"],
            "'ay' ends words (play, day, stay); 'ai' goes in the middle "
            "(rain, mail)."),
        mcq("What sound do the letters 'ee' make in 'feet'?",
            "long e", ["short e", "long i", "long a"],
            "'ee' is a vowel team for long e: see, feet, tree, sleep."),
        mcq("What sound do the letters 'oa' make in 'boat'?",
            "long o", ["short o", "long a", "/ow/ as in cow"],
            "'oa' is a vowel team for long o: boat, coat, road, soap."),
        mcq("What sound do the letters 'igh' make in 'night'?",
            "long i", ["long e", "short i", "/g/ then /h/"],
            "'igh' says long i, and the g and h are silent: light, night, "
            "high, right."),
        mcq("Which word has the same vowel sound as 'moon'?",
            "food", ["book", "good", "foot"],
            "'oo' has two sounds. Food matches moon (long oo); book, good, "
            "and foot use the other, shorter oo sound."),
        mcq("Which word has the same 'oo' sound as 'book'?",
            "foot", ["moon", "food", "zoo"],
            "Book, look, good, and foot share the short oo sound; moon, "
            "food, and zoo share the long one."),
        mcq("What sound do the letters 'ou' make in 'cloud'?",
            "/ow/ as in cow", ["long o", "long u", "short o"],
            "'ou' in the middle of a word usually says /ow/: out, house, "
            "cloud, found."),
        mcq("The /oy/ sound is spelled 'oi' in the middle of a word and ____ "
            "at the end.",
            "oy", ["ow", "oa", "io"],
            "Middle: oi (boil, coin, point). End: oy (boy, toy, enjoy)."),
        mcq("'When two vowels go walking, the first one does the talking' "
            "means the first vowel usually says ____.",
            "its name (the long sound)", ["its short sound", "nothing",
            "/w/"],
            "In teams like ai, ea, oa, ee, the FIRST vowel is usually long "
            "and the second is silent: boat = long o. (A helpful rule of "
            "thumb, not a law — 'bread' breaks it.)"),
        mcq("Which word has 'ow' saying long o, like 'snow'?",
            "grow", ["cow", "town", "down"],
            "'ow' has two sounds: long o (snow, grow, show) and /ow/ (cow, "
            "town, down). You may have to try both."),
        tf("'ay' usually comes at the end of a word, like in 'play' and "
           "'day'.",
           True, "That's the spelling rule: ai in the middle, ay at the end."),
        tf("The letters 'ea' ALWAYS say long e.",
           False, "'ea' usually says long e (eat, team) but sometimes short "
           "e (bread, head, breakfast). Try both sounds."),
        short("Which two letters make the long a sound in 'rain'?",
              "ai", "'ai' is the vowel team: r-AI-n."),
        short("The /aw/ sound at the END of a word (like 'saw' and 'draw') "
              "is spelled with which two letters?",
              "aw", "'aw' ends words (saw, draw, lawn); 'au' goes in the "
              "middle (haul, August, because)."),
    ]
    kb = (
        "# Grade 2 ELA — Vowel Teams & Diphthongs\n\n"
        "**Standard: RF.2.3b** — know the sounds of the common vowel teams.\n\n"
        "## The teams\n"
        "- **Long a:** ai (rain — middle), ay (play — end)\n"
        "- **Long e:** ee (feet), ea (eat — but sometimes short e: bread), "
        "ey (key, monkey)\n"
        "- **Long i:** igh (night), ie (pie — but sometimes long e: field), "
        "y at the end of a short word (my, fly)\n"
        "- **Long o:** oa (boat — middle), ow (snow — end), oe (toe)\n"
        "- **/oo/ sounds:** oo like 'moon' (food, zoo) or like 'book' (good, "
        "foot); ue (blue), ew (new), ui (fruit)\n"
        "- **Diphthongs (gliding sounds):** ou/ow say /ow/ (out, cow); oi/oy "
        "say /oy/ (coin, boy)\n"
        "- **/aw/:** au (because — middle), aw (saw — end)\n\n"
        "## Big ideas\n"
        "- 'When two vowels go walking, the first one does the talking' — "
        "often true (boat, rain, feet), but not always (bread, cow).\n"
        "- **Position rules:** ai/oa/oi/au in the middle; ay/ow/oy/aw at the "
        "end.\n"
        "- Some teams have TWO sounds (ea, oo, ow, ie) — if the first sound "
        "makes a silly word, try the other one." + SRC)
    return {"name": "Vowel Teams & Diphthongs",
            "source": {"title": "Vowel teams — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 3: Bossy R (r-controlled vowels) -------------------------------
def ch_bossy_r():
    qs = [
        mcq("What sound do the letters 'ar' make in 'car'?",
            "/ar/ like in 'star'", ["long a", "short a", "/or/ like in 'corn'"],
            "When r follows a, it makes the /ar/ sound: car, farm, star, "
            "shark."),
        mcq("Which THREE spellings all make the same /er/ sound?",
            "er, ir, ur", ["ar, or, er", "ai, ay, ea", "er, or, ar"],
            "er (her), ir (bird), and ur (fur) all say exactly the same /er/ "
            "sound."),
        mcq("Which word has a bossy-r (r-controlled) vowel?",
            "corn", ["coat", "cone", "cot"],
            "In 'corn' the r changes the o to the /or/ sound. The other "
            "words have plain long or short o."),
        mcq("In 'bird', which two letters make the /er/ sound?",
            "ir", ["bi", "rd", "b"],
            "b-IR-d: the ir team says /er/, the same sound as in 'her' and "
            "'fur'."),
        mcq("In 'star', the a is ____.",
            "changed by the r (neither long nor short)",
            ["long", "short", "silent"],
            "The 'bossy r' takes over: the vowel is neither long nor short — "
            "it makes a brand-new sound."),
        mcq("Which word has the same vowel sound as 'her'?",
            "bird", ["barn", "born", "bear"],
            "her (er), bird (ir), and fur (ur) all share /er/. Barn is /ar/ "
            "and born is /or/."),
        mcq("Which word has the /or/ sound, like 'corn'?",
            "storm", ["star", "stir", "stem"],
            "'Storm' has or. Star is /ar/, stir is /er/, and stem has a "
            "plain short e."),
        mcq("The /er/ sound in 'Thursday' is spelled with which letters?",
            "ur", ["er", "ir", "or"],
            "Th-UR-sday. The /er/ sound has three spellings — you have to "
            "remember which word uses which."),
        mcq("Which word has the /air/ sound, like 'hair'?",
            "chair", ["car", "corn", "curl"],
            "'air' and 'are' words (hair, chair, care, share) make the /air/ "
            "sound."),
        tf("A vowel followed by r is usually neither long nor short — the r "
           "changes its sound.",
           True, "That's why r is called 'bossy': it bosses the vowel into a "
           "new sound (car, corn, her)."),
        tf("'Fur' and 'first' have the same vowel sound.",
           True, "ur and ir both say /er/ — fur and first rhyme in the "
           "middle."),
        tf("'Car' and 'care' have the same vowel sound.",
           False, "'Car' says /ar/; 'care' says /air/. The silent e changes "
           "the sound."),
        short("Which two letters make the /or/ sound in 'fork'?",
              "or", "f-OR-k: the o plus r make the /or/ sound."),
        short("Which letter is the 'bossy' one that changes a vowel's sound "
              "in words like 'car', 'bird', and 'corn'?",
              "r", "R after a vowel changes ('bosses') the vowel's sound."),
    ]
    kb = (
        "# Grade 2 ELA — Bossy R (R-Controlled Vowels)\n\n"
        "**Standard: RF.2.3b** — vowel + r makes a new sound (neither long "
        "nor short).\n\n"
        "## The five spellings\n"
        "- **ar** = /ar/ — car, farm, star, shark, party\n"
        "- **or** = /or/ — corn, fork, storm, horse, morning\n"
        "- **er** = /er/ — her, fern, sister, water\n"
        "- **ir** = /er/ — bird, girl, first, shirt\n"
        "- **ur** = /er/ — fur, turn, hurt, purple, Thursday\n\n"
        "## Big ideas\n"
        "- When a vowel is followed by **r**, the r 'bosses' it into a new "
        "sound — the vowel is **neither long nor short**.\n"
        "- **er, ir, and ur all make the SAME sound** (/er/): her = bird = "
        "fur in the middle. Spelling them right takes memory.\n"
        "- More r teams: **ore** (more, store), **are** (care, share) and "
        "**air** (hair, chair) both say /air/; **ear** says /ear/ in hear "
        "and year but /er/ in earn and learn." + SRC)
    return {"name": "Bossy R (R-Controlled Vowels)",
            "source": {"title": "Bossy r — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 4: Tricky Spellings (soft c/g, silent letters, ck/tch/dge) -----
def ch_tricky_spellings():
    qs = [
        mcq("What sound does the c make in 'city'?",
            "/s/ (soft c)", ["/k/ (hard c)", "/ch/", "/j/"],
            "c says /s/ when followed by e, i, or y: cent, city, cycle, "
            "face, pencil."),
        mcq("c makes its SOFT /s/ sound when it is followed by which "
            "letters?",
            "e, i, or y", ["a, o, or u", "any consonant", "r or l"],
            "Soft c before e/i/y (city, cent, fancy); hard /k/ everywhere "
            "else (cat, cup, clap)."),
        mcq("What sound does the g make in 'giant'?",
            "/j/ (soft g)", ["/g/ (hard g)", "/k/", "it is silent"],
            "g often says /j/ before e, i, or y: gem, giant, gym, cage, "
            "magic."),
        mcq("What sound does the g make in 'gate'?",
            "/g/ (hard g)", ["/j/ (soft g)", "/h/", "it is silent"],
            "Before a, o, u, or a consonant, g keeps its hard sound: gate, "
            "go, gum, glad."),
        mcq("Which word is an EXCEPTION where g stays hard even before i or "
            "e?",
            "girl", ["gem", "giant", "gym"],
            "Memorize the exceptions: get, give, girl, gift, begin — hard g "
            "even though e or i follows."),
        mcq("Which letter is silent in 'knee' and 'know'?",
            "k", ["n", "e", "w"],
            "In kn- words the k is silent: knee, know, knock."),
        mcq("Which letter is silent in 'write' and 'wrong'?",
            "w", ["r", "i", "t"],
            "In wr- words the w is silent: write, wrong, wrap."),
        mcq("Which letter is silent in 'lamb' and 'thumb'?",
            "b", ["m", "l", "a"],
            "In -mb words the b is silent: lamb, comb, thumb, climb."),
        mcq("Right after a short vowel, the /k/ sound at the end of a word "
            "is spelled ____.",
            "ck (duck, stick)", ["k (book)", "c (picnic)", "ke (bake)"],
            "Short vowel → -ck: back, duck, stick, clock. After anything "
            "else use k or ke: book, bake."),
        mcq("Which word is spelled correctly?",
            "catch", ["cach", "katch", "cattch"],
            "The /ch/ sound right after a short vowel is spelled -tch: "
            "catch, match, pitch."),
        mcq("The /j/ sound at the end of 'badge' and 'bridge' is spelled "
            "-dge because it comes after a ____.",
            "short vowel", ["long vowel", "consonant", "silent e"],
            "Short vowel → -dge (badge, edge, judge). Otherwise -ge: cage, "
            "huge, large."),
        mcq("Which word follows the FLOSS rule (double the last letter after "
            "a short vowel)?",
            "bell", ["bake", "boat", "bird"],
            "f, l, s, and z double after a short vowel in one-syllable "
            "words: stuff, bell, miss, buzz."),
        mcq("What sound does 'ch' make in 'school'?",
            "/k/", ["/ch/ as in chin", "/sh/", "/s/"],
            "ch usually says /ch/ (chin), but sometimes /k/ (school) or "
            "/sh/ (chef). Try another sound if the first doesn't make a "
            "word."),
        tf("In 'knock', you pronounce the k.",
           False, "The k in kn- is silent: you say 'nock'."),
        tf("The word 'buzz' ends in a double z because the u is short.",
           True, "That's the FLOSS rule — double f, l, s, or z after a short "
           "vowel."),
        short("Which letter is silent in 'comb'?",
              "b", "In -mb words (comb, lamb, thumb) the b is silent."),
        short("Soft c (as in 'city') makes the same sound as which letter?",
              "s", "Soft c says /s/: city sounds like 'sity'."),
    ]
    kb = (
        "# Grade 2 ELA — Tricky Spellings\n\n"
        "**Standards: RF.2.3e, L.2.2d** — flexible sounds and spelling "
        "patterns.\n\n"
        "## Soft and hard c and g\n"
        "- **c** = /s/ before **e, i, y** (cent, city, cycle, face, pencil); "
        "otherwise /k/ (cat, cot, cup, clap).\n"
        "- **g** = /j/ before **e, i, y** (gem, giant, gym, cage, magic); "
        "otherwise /g/ (gate, go, gum).\n"
        "- Soft-g exceptions to memorize: **get, give, girl, gift, begin**.\n\n"
        "## Silent letters\n"
        "- **kn** — silent k: knee, know, knock\n"
        "- **wr** — silent w: write, wrong, wrap\n"
        "- **mb** — silent b: lamb, comb, thumb, climb\n\n"
        "## End-of-word spelling patterns (after a SHORT vowel, use the "
        "bigger spelling)\n"
        "- /k/: **-ck** after a short vowel (duck, stick); else k/ke (book, "
        "bake)\n"
        "- /ch/: **-tch** after a short vowel (catch, pitch); else -ch "
        "(bench, teach, coach)\n"
        "- /j/: **-dge** after a short vowel (badge, edge, judge); else -ge "
        "(cage, huge, large)\n"
        "- **FLOSS rule**: double f, l, s, z after a short vowel in a "
        "one-syllable word (stuff, bell, miss, buzz)\n\n"
        "## Spellings with more than one sound — try both!\n"
        "- **ea**: team / bread · **oo**: moon / book · **ow**: snow / cow · "
        "**ie**: pie / field · **ch**: chin / school / chef · **y** at the "
        "end: my (long i) / baby (long e)" + SRC)
    return {"name": "Tricky Spellings & Silent Letters",
            "source": {"title": "Tricky spellings — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 5: Two-Syllable Words & Syllable Types (RF.2.3c) ---------------
def ch_syllables():
    qs = [
        mcq("How many syllables are in 'rabbit'?",
            "2", ["1", "3", "4"],
            "rab-bit: clap it out — two beats, two syllables."),
        mcq("Where do you split 'rabbit' into syllables?",
            "rab / bit", ["ra / bbit", "rabb / it", "r / abbit"],
            "Two consonants between vowels: split between them (VC/CV) — "
            "rab/bit, bas/ket, win/ter."),
        mcq("Where do you split 'tiger' into syllables?",
            "ti / ger", ["tig / er", "t / iger", "tige / r"],
            "One consonant between vowels: usually split BEFORE it (V/CV) — "
            "ti/ger, pa/per, mu/sic."),
        mcq("Why is the i in 'tiger' long?",
            "Its syllable ends with the vowel (an open syllable)",
            ["The r makes it long", "The e at the end makes it long",
             "All i's are long"],
            "ti/ger — 'ti' is an open syllable, and open syllables have long "
            "vowels."),
        mcq("A closed syllable (like 'rab' in rabbit) has a ____ vowel "
            "sound.",
            "short", ["long", "silent", "bossy"],
            "Closed syllables end in a consonant and the vowel is short: "
            "rab, nap, in."),
        mcq("Where do you split 'table'?",
            "ta / ble", ["tab / le", "t / able", "tabl / e"],
            "Consonant-le: count back three letters (b + le) — ta/ble, "
            "lit/tle, pur/ple."),
        mcq("Where do you split the compound word 'sunset'?",
            "sun / set", ["su / nset", "suns / et", "sunse / t"],
            "Compound words split between the two small words: sun/set, "
            "cup/cake, base/ball."),
        mcq("Every syllable has exactly one ____.",
            "vowel sound", ["consonant", "silent letter", "capital letter"],
            "One vowel sound per syllable — that's what makes it a "
            "syllable."),
        mcq("Which word has an OPEN first syllable (so its first vowel is "
            "long)?",
            "music", ["napkin", "rabbit", "basket"],
            "mu/sic — 'mu' ends in its vowel, so the u is long. The others "
            "start with closed (short-vowel) syllables."),
        mcq("In 'cupcake', what kind of syllable is 'cake'?",
            "silent e (the e makes the a long)",
            ["closed", "open", "bossy r"],
            "cup/cake — 'cake' is a vowel-consonant-e syllable: silent e, "
            "long a."),
        mcq("In 'robot', the first o is ____.",
            "long, because ro is an open syllable",
            ["short, because ro is closed", "silent", "changed by r"],
            "ro/bot — the first syllable ends with its vowel, so the o says "
            "its name."),
        tf("'Baby' has two syllables.",
           True, "ba-by: two beats. The y at the end says long e."),
        tf("In 'winter', you split between the n and the t.",
           True, "win/ter — two consonants between vowels split down the "
           "middle (VC/CV)."),
        short("How many syllables are in 'butterfly'?",
              "3", "but-ter-fly: three beats, three syllables."),
        short("Every syllable must have how many vowel sounds?",
              "1", "Exactly one vowel sound per syllable."),
    ]
    kb = (
        "# Grade 2 ELA — Two-Syllable Words & Syllable Types\n\n"
        "**Standard: RF.2.3c** — decode two-syllable words with long "
        "vowels.\n\n"
        "## The six syllable types\n"
        "1. **Closed** — ends in a consonant, vowel is SHORT: rab-bit, "
        "nap-kin\n"
        "2. **Open** — ends with the vowel, vowel is LONG: ti-ger, mu-sic, "
        "ba-by\n"
        "3. **Silent e** — vowel-consonant-e, vowel is LONG: cup-cake, "
        "rep-tile\n"
        "4. **Vowel team** — two vowels together: rain-bow, sea-son\n"
        "5. **Bossy r** — vowel + r: gar-den, cor-ner, tur-tle\n"
        "6. **Consonant-le** — ends in -le: ta-ble, lit-tle, pur-ple\n\n"
        "## How to split a word\n"
        "- **Two consonants between vowels → split between them** (VC/CV): "
        "rab/bit, win/ter, bas/ket.\n"
        "- **One consonant between vowels → try splitting BEFORE it** "
        "(V/CV): ti/ger, pa/per, o/pen — the first syllable is open, so its "
        "vowel is long.\n"
        "- If that doesn't make a real word, split AFTER it (VC/V): cab/in, "
        "riv/er, lem/on — first vowel short.\n"
        "- **Compound words** split between the small words: sun/set, "
        "cup/cake.\n"
        "- **Consonant-le**: count back three letters: lit/tle, ta/ble.\n"
        "- Every syllable has exactly **one vowel sound**." + SRC)
    return {"name": "Two-Syllable Words & Syllable Types",
            "source": {"title": "Syllables — knowledge base", "content": kb},
            "questions": qs}


# --- Chapter 6: Prefixes & Suffixes (RF.2.3d, L.2.4b-c) ---------------------
def ch_prefixes_suffixes():
    qs = [
        mcq("The prefix 'un-' means ____.",
            "not (or the opposite of)", ["again", "before", "full of"],
            "unhappy = NOT happy; unlock = the opposite of lock."),
        mcq("What does 'unhappy' mean?",
            "not happy", ["very happy", "happy again", "happy before"],
            "un- (not) + happy = not happy."),
        mcq("The prefix 're-' means ____.",
            "again", ["not", "before", "without"],
            "redo = do again; reread = read again; replay = play again."),
        mcq("What does 'retell' mean?",
            "tell again", ["not tell", "tell first", "tell loudly"],
            "re- (again) + tell = tell again."),
        mcq("The prefix 'pre-' means ____.",
            "before", ["after", "not", "again"],
            "preheat = heat BEFORE; preschool = school that comes before "
            "regular school."),
        mcq("What does 'disagree' mean?",
            "to not agree", ["to agree again", "to agree a lot",
            "to agree first"],
            "dis- (not / opposite of) + agree = not agree."),
        mcq("What does 'misspell' mean?",
            "to spell a word wrong", ["to spell again",
            "to spell before", "to spell well"],
            "mis- means wrongly or badly: misspell, misplace, misbehave."),
        mcq("The suffix '-ful' means ____.",
            "full of", ["without", "again", "a person who"],
            "joyful = full of joy; helpful = full of help; careful = full "
            "of care."),
        mcq("What does 'fearless' mean?",
            "without fear", ["full of fear", "afraid", "fear again"],
            "-less means WITHOUT: fearless, careless, homeless."),
        mcq("'Quickly' means ____.",
            "in a quick way", ["not quick", "more quick", "a quick person"],
            "-ly turns a describing word into an adverb: quickly = in a "
            "quick way."),
        mcq("When you compare TWO things, use -er; when you compare THREE OR "
            "MORE, use ____.",
            "-est", ["-ing", "-ly", "-ness"],
            "taller (of two), tallest (of three or more)."),
        mcq("A 'baker' is ____.",
            "a person who bakes", ["more bake", "bakes again",
            "without baking"],
            "The -er ending can mean 'a person who ___s': baker, teacher, "
            "farmer, singer."),
        mcq("'Kindness' means ____.",
            "being kind", ["not kind", "kind again", "a kind person"],
            "-ness means the state of being: kindness, darkness, sadness."),
        mcq("What is the root (base) word in 'helpful'?",
            "help", ["ful", "helpf", "hel"],
            "The root word is the smallest word part that means something "
            "on its own: help + ful."),
        tf("'Preview' means to view (look at) something before.",
           True, "pre- (before) + view = look before."),
        short("Add a prefix to 'lock' to make a word that means the "
              "opposite. What word do you get?",
              "unlock", "un- + lock = unlock, the opposite of lock."),
        short("What is the root (base) word in 'careless'?",
              "care", "care + less = without care."),
    ]
    kb = (
        "# Grade 2 ELA — Prefixes & Suffixes\n\n"
        "**Standards: RF.2.3d, L.2.4b-c** — decode words with prefixes and "
        "suffixes, and use them as MEANING clues.\n\n"
        "## Prefixes (added to the FRONT)\n"
        "- **un-** = not / opposite of — unhappy, unlock, unfair, untie\n"
        "- **re-** = again / back — redo, retell, reread, replay\n"
        "- **pre-** = before — preschool, preheat, pretest, preview\n"
        "- **dis-** = not / opposite of — disagree, dislike, disappear\n"
        "- **mis-** = wrongly — misspell, misplace, misbehave\n\n"
        "## Suffixes (added to the END)\n"
        "- **-ful** = full of — joyful, helpful, careful, colorful\n"
        "- **-less** = without — fearless, careless, helpless\n"
        "- **-ly** = in a ___ way (makes adverbs) — quickly, slowly, sadly\n"
        "- **-er / -est** = more / most — taller (compares 2), tallest "
        "(compares 3+)\n"
        "- **-er** can also mean 'a person who ___s' — teacher, baker, "
        "farmer\n"
        "- **-ness** = being ___ — kindness, darkness, sadness\n"
        "- **-y** = having / like — rainy, sunny, sleepy, lucky\n\n"
        "## Big idea\n"
        "The **root (base) word** is the smallest part that means something "
        "on its own. Prefix + root + suffix: un + help + ful. If you know "
        "the root and the parts, you can figure out a brand-new word." + SRC)
    return {"name": "Prefixes & Suffixes",
            "source": {"title": "Prefixes & suffixes — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 7: Word Endings & Spelling Rules -------------------------------
def ch_endings():
    qs = [
        mcq("Adding '-ed' to a verb makes it tell about the ____.",
            "past (it already happened)", ["future", "present", "beginning"],
            "jump → jumped: the -ed shows it already happened."),
        mcq("In 'wanted', the -ed sounds like ____.",
            "/id/ (an extra syllable)", ["/t/", "/d/", "it is silent"],
            "After t or d, -ed adds a syllable: want-ed, need-ed, "
            "plant-ed."),
        mcq("In 'jumped', the -ed sounds like ____.",
            "/t/", ["/id/ (an extra syllable)", "/ed/", "/d/"],
            "-ed has three sounds: /t/ (jumped, walked), /d/ (played, "
            "called), /id/ (wanted)."),
        mcq("In 'played', the -ed sounds like ____.",
            "/d/", ["/t/", "/id/ (an extra syllable)", "/p/"],
            "After most sounds, -ed just says /d/: played, smiled, "
            "called."),
        mcq("run + ing = ____",
            "running", ["runing", "runnning", "runeing"],
            "Doubling rule: short word, one vowel, one final consonant → "
            "double the consonant before -ing: run → running."),
        mcq("hop + ed = ____",
            "hopped", ["hoped", "hopt", "hopedd"],
            "Double the p to keep the o short: hopped. ('Hoped' with one p "
            "comes from 'hope'.)"),
        mcq("bake + ing = ____",
            "baking", ["bakeing", "bakking", "bakinge"],
            "Drop-e rule: drop the silent e before adding -ing: bake → "
            "baking."),
        mcq("cry + ed = ____",
            "cried", ["cryed", "crided", "cryd"],
            "Y rule: consonant + y → change y to i: cry → cried, happy → "
            "happier."),
        mcq("play + ed = ____",
            "played", ["plaied", "playd", "plaid"],
            "A VOWEL comes before the y in 'play', so just add the ending: "
            "played, playing."),
        mcq("happy + er = ____",
            "happier", ["happyer", "happller", "hapier"],
            "Consonant + y: change the y to i, then add -er: happier."),
        mcq("Add -es (instead of just -s) after which letters?",
            "s, x, z, ch, sh", ["a, e, i, o, u", "b, c, d", "only y"],
            "buses, foxes, wishes, lunches — after s, x, z, ch, sh you need "
            "-es (it adds a syllable)."),
        mcq("What is the plural of 'fox'?",
            "foxes", ["foxs", "foxies", "fox"],
            "fox ends in x, so add -es: foxes."),
        mcq("What is the plural of 'baby'?",
            "babies", ["babys", "babyes", "babbies"],
            "Consonant + y: change y to i and add -es: babies."),
        tf("To write 'crying', you change the y to i.",
           False, "Keep the y before -ing: crying, playing, trying. (The y "
           "only changes before -ed, -er, -es, -est.)"),
        short("big + est = ? (Spell the whole word.)",
              "biggest", "Doubling rule: big → biggest (double g)."),
        short("smile + ed = ? (Spell the whole word.)",
              "smiled", "Drop the silent e, then add -ed: smiled."),
    ]
    kb = (
        "# Grade 2 ELA — Word Endings & Spelling Rules\n\n"
        "**Standards: RF.2.3d, L.2.2d** — endings and the spelling changes "
        "they cause.\n\n"
        "## The endings\n"
        "- **-s / -es** = more than one, or a present verb (cats; boxes — "
        "use -es after s, x, z, ch, sh)\n"
        "- **-ed** = past tense (it already happened)\n"
        "- **-ing** = happening now\n"
        "- **-er / -est** = more / most\n\n"
        "## The three sounds of -ed\n"
        "- /t/ — jumped, walked, laughed\n"
        "- /d/ — played, smiled, called\n"
        "- /id/ (extra syllable) — wanted, needed, planted (after t or d)\n\n"
        "## The four spelling-change rules\n"
        "1. **Doubling rule**: one syllable + one vowel + one final "
        "consonant → DOUBLE the consonant: run→running, hop→hopped, "
        "big→bigger, sad→saddest.\n"
        "2. **Drop-e rule**: silent e? Drop it before -ed/-ing/-er/-est: "
        "bake→baking, smile→smiled, nice→nicer.\n"
        "3. **Y rule**: consonant + y → change y to i (cry→cried, "
        "happy→happier) — but KEEP the y before -ing (crying). Vowel + y → "
        "just add the ending (play→played).\n"
        "4. **-es rule**: after s, x, z, ch, sh add -es (bus→buses, "
        "fox→foxes, wish→wishes); consonant + y nouns → -ies "
        "(baby→babies)." + SRC)
    return {"name": "Word Endings & Spelling Rules",
            "source": {"title": "Endings & spelling rules — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 8: Sight Words & Homophones (RF.2.3f) --------------------------
def ch_sight_homophones():
    qs = [
        mcq("Choose the right word: '____ going to the park after lunch.'",
            "They're", ["Their", "There", "Theyre"],
            "They're = they are. 'They are going to the park' makes sense."),
        mcq("Choose the right word: 'The dog wagged ____ tail.'",
            "its", ["it's", "its'", "it is"],
            "its (no apostrophe) = belonging to it. It's = it is — 'the dog "
            "wagged it is tail' makes no sense."),
        mcq("'It's' is short for ____.",
            "it is", ["belonging to it", "it was", "sits"],
            "The apostrophe shows squeezed-together words: it's = it is."),
        mcq("Choose the right word: 'I want to come, ____!'",
            "too", ["two", "to", "tow"],
            "too = also. to = toward (go to school). two = the number 2."),
        mcq("Choose the right word: 'She has ____ cats.'",
            "two", ["too", "to", "tu"],
            "two = the number 2."),
        mcq("Choose the right word: '____ my best friend.'",
            "You're", ["Your", "Youre", "Yore"],
            "You're = you are. Your = belonging to you (your coat)."),
        mcq("Choose the right word: 'I ____ the answer.'",
            "know", ["no", "now", "knew"],
            "know = to have it in your head (silent k). no = the opposite "
            "of yes."),
        mcq("Choose the right word: 'Come over ____ and sit down.'",
            "here", ["hear", "heer", "hair"],
            "here = this place. hear = to listen with your ears (hear has "
            "'ear' inside it!)."),
        mcq("Choose the right word: 'Please ____ your name at the top.'",
            "write", ["right", "rite", "wright"],
            "write = make letters with a pencil (silent w). right = correct, "
            "or the opposite of left."),
        mcq("Which word is spelled correctly?",
            "because", ["becuz", "becase", "beecause"],
            "'Because' is a grade-2 word to memorize: b-e-c-a-u-s-e."),
        mcq("Which is the correct spelling of the word that sounds like "
            "'sed'?",
            "said", ["sed", "sayed", "saide"],
            "'Said' is irregular — it doesn't sound the way it's spelled: "
            "s-a-i-d."),
        mcq("Choose the right word: '____ is a swing at the playground.'",
            "There", ["Their", "They're", "Theyre"],
            "There = a place (or 'there is/are'). Their = belonging to "
            "them."),
        tf("'Friend' is spelled f-r-i-e-n-d.",
           True, "A tricky word to memorize — the i comes before the e."),
        tf("'Their' names a place, like 'over their.'",
           False, "Their = belonging to them (their house). The place word "
           "is THERE."),
        short("Spell the word that means 'also', as in 'Me ____!'",
              "too", "too (with two o's) = also, or more than enough."),
        short("The contraction 'they're' is short for which two words?",
              "they are", "they + are squeeze into they're."),
    ]
    kb = (
        "# Grade 2 ELA — Sight Words & Homophones\n\n"
        "**Standard: RF.2.3f** — read and spell grade-2 irregular words.\n\n"
        "## Grade-2 sight words (memorize — many don't follow the rules)\n"
        "always, around, because, been, before, best, both, buy, call, "
        "cold, does, don't, fast, first, five, found, gave, goes, green, "
        "its, made, many, off, or, pull, read, right, sing, sit, sleep, "
        "tell, their, these, those, upon, us, use, very, wash, which, why, "
        "wish, work, would, write, your.\n\n"
        "Other tricky words: again, could, does, enough, friend, great, "
        "heard, know, laugh, listen, once, people, pretty, said, says, "
        "school, should, sure, thought, through, together, want, water, "
        "were, where, who, whole.\n\n"
        "## Homophones (sound the same, spelled differently)\n"
        "- **their** (belonging to them) / **there** (a place) / "
        "**they're** (they are)\n"
        "- **to** (toward) / **too** (also; too much) / **two** (2)\n"
        "- **your** (belonging to you) / **you're** (you are)\n"
        "- **its** (belonging to it) / **it's** (it is)\n"
        "- know/no · knew/new · write/right · hear/here · one/won · "
        "son/sun · would/wood\n\n"
        "**Tricks:** hear has EAR inside it. If you can say 'it is' in the "
        "sentence, write it's; otherwise its." + SRC)
    return {"name": "Sight Words & Homophones",
            "source": {"title": "Sight words & homophones — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 9: Reading Stories (RL.2.1/3/5) --------------------------------
def ch_stories():
    p1 = ("Read the story:\n\n"
          "\"Mia lost her red mitten on the way to school. Her hand felt "
          "cold all morning, and she was sad. At recess, her friend Ben saw "
          "something red under the slide. It was the mitten! Mia smiled and "
          "said, 'Thank you, Ben. You are a good friend.'\"\n\n")
    p2 = ("Read the story:\n\n"
          "\"Jayla lined up for the big race with a nervous feeling in her "
          "tummy. First she stumbled at the start, and two runners passed "
          "her. Next she took a deep breath and pumped her arms harder. "
          "Then, just before the finish line, she passed both runners. "
          "Jayla did not win first place, but she felt proud because she "
          "never gave up.\"\n\n")
    p3 = ("Read the story:\n\n"
          "\"Grandpa and Leo planted tiny seeds in the spring. Every day "
          "Leo watered the dirt, but nothing happened for two weeks. Leo "
          "wanted to quit. 'Be patient,' Grandpa said with a wink. One "
          "sunny morning, Leo ran outside and saw little green sprouts "
          "standing in a row like soldiers.\"\n\n")
    qs = [
        # Passage 1 — The Lost Mitten
        mcq(p1 + "What was Mia's problem?",
            "She lost her mitten", ["She was late for school",
            "She lost her friend", "She broke the slide"],
            "The very first sentence tells the problem: 'Mia lost her red "
            "mitten.'"),
        mcq(p1 + "Who solved the problem?",
            "Ben", ["Mia", "the teacher", "Mia's mom"],
            "Ben saw something red under the slide — he found the mitten."),
        mcq(p1 + "Where was the mitten found?",
            "under the slide", ["on the bus", "in Mia's desk",
            "at Mia's house"],
            "'Ben saw something red under the slide.'"),
        mcq(p1 + "How did Mia's feelings change in the story?",
            "from sad to happy", ["from happy to sad", "she stayed sad",
            "from angry to scared"],
            "She 'was sad' while her hand was cold, then 'Mia smiled' when "
            "Ben found the mitten."),
        mcq(p1 + "WHY did Mia's hand feel cold all morning?",
            "Her mitten was lost", ["It was summer", "She forgot her coat",
            "The classroom was hot"],
            "Cause and effect: losing the mitten (cause) made her hand cold "
            "(effect)."),
        # Passage 2 — The Big Race
        mcq(p2 + "What happened FIRST in the race?",
            "Jayla stumbled at the start", ["Jayla passed two runners",
            "Jayla took a deep breath", "Jayla felt proud"],
            "The word 'First' signals it: 'First she stumbled at the "
            "start.'"),
        mcq(p2 + "How did Jayla feel at the START of the race?",
            "nervous", ["proud", "angry", "sleepy"],
            "'…with a nervous feeling in her tummy.'"),
        mcq(p2 + "Why did Jayla feel proud even though she didn't win?",
            "She never gave up", ["She won first place",
            "She ran the slowest", "She beat her best friend"],
            "The story says she 'felt proud because she never gave up.'"),
        mcq(p2 + "What is the central message (lesson) of this story?",
            "Keep trying and don't give up",
            ["Winning is the only thing that matters",
             "Never run in races", "Fast runners are better people"],
            "Jayla is proud because she kept going — the lesson is about "
            "not giving up, not about winning."),
        mcq(p2 + "Which words in this story signal the ORDER of events?",
            "First, Next, Then", ["red, blue, green", "big, bigger, biggest",
            "happy, sad, proud"],
            "First, next, and then are temporal (time-order) words."),
        # Passage 3 — The Surprise in the Garden
        mcq(p3 + "What is the setting of this story?",
            "a garden in spring", ["a beach in summer",
            "a classroom in winter", "a store at night"],
            "They planted seeds in the spring and the sprouts came up "
            "outside — the setting is a garden in spring."),
        mcq(p3 + "How did Leo respond when nothing happened for two weeks?",
            "He wanted to quit", ["He laughed", "He planted more seeds",
            "He watered the seeds twice as much"],
            "'Leo wanted to quit.' Noticing how a character responds to a "
            "problem is a big grade-2 skill."),
        mcq(p3 + "What lesson does Grandpa teach Leo?",
            "Be patient — good things take time",
            ["Never plant seeds", "Water washes seeds away",
             "Quit if something is slow"],
            "'Be patient,' Grandpa said — and the sprouts came up after "
            "waiting."),
        mcq(p3 + "The sprouts stood in a row 'like soldiers.' What does "
            "this comparison help you picture?",
            "The sprouts standing straight and tall in a line",
            ["The sprouts wearing helmets", "The sprouts marching away",
             "The garden being a battlefield"],
            "Comparing sprouts to soldiers paints a picture: straight, "
            "tall, in a neat row."),
        # Story structure concepts
        mcq("The BEGINNING of a story usually ____.",
            "introduces the characters, setting, and problem",
            ["solves the problem", "gives the moral", "lists the chapters"],
            "The beginning introduces the story; the ending concludes "
            "(wraps up) the action."),
        mcq("The ENDING of a story usually ____.",
            "concludes the action (wraps things up)",
            ["introduces the characters", "asks the reader questions",
             "starts a new problem"],
            "By the end, the problem is usually solved and the action "
            "concludes."),
        tf("A character's feelings can change from the beginning of a story "
           "to the end.",
           True, "Watching feelings change (sad → happy, nervous → proud) "
           "is part of understanding the story."),
        short("The trouble a character faces in a story is called the "
              "____.",
              "problem", "Stories usually have a problem and a solution."),
    ]
    kb = (
        "# Grade 2 ELA — Reading Stories\n\n"
        "**Standards: RL.2.1, RL.2.3, RL.2.5, RL.2.7.** Understanding "
        "stories at grade 2.\n\n"
        "## Story elements\n"
        "- **Characters** — who the story is about (people or animals)\n"
        "- **Setting** — where AND when it happens\n"
        "- **Problem** — the trouble the character faces\n"
        "- **Solution** — how the problem gets fixed\n"
        "- **Plot** — the events in order: beginning, middle, end\n\n"
        "## Big ideas\n"
        "- The **beginning introduces** the characters, setting, and "
        "problem; the **ending concludes** the action.\n"
        "- Grade 2 asks HOW characters **respond** to big events: what do "
        "they do, and how do they feel? Feelings often **change** (sad → "
        "happy, nervous → proud).\n"
        "- **Ask and answer** who, what, where, when, why, and how — and "
        "point to the words that prove your answer (text evidence).\n"
        "- **Cause and effect**: the cause is WHY it happened; the effect "
        "is WHAT happened. (Mia lost her mitten → her hand was cold.)\n"
        "- Time-order words (**first, next, then, finally**) signal the "
        "order of events." + SRC)
    return {"name": "Reading Stories",
            "source": {"title": "Reading stories — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 10: Fables, Folktales & Morals (RL.2.2) ------------------------
def ch_fables():
    p1 = ("Read the fable:\n\n"
          "\"All fall, Pip the squirrel buried acorns near the old oak "
          "tree. His brother Rex just played in the leaves and laughed at "
          "him. When winter came, snow covered the ground, and there was "
          "nothing left to eat. Pip dug up his acorns and shared them with "
          "Rex. 'Next fall,' said Rex, 'I will work first and play "
          "later.'\"\n\n")
    p2 = ("Read the story:\n\n"
          "\"A little blue boat sat tied to the dock while big ships "
          "sailed to sea. 'I am too small to matter,' the boat sighed. One "
          "foggy night, a big ship could not find the harbor. The little "
          "boat's tiny light blinked and blinked until the ship followed "
          "it safely home. After that, the little blue boat never called "
          "itself small again.\"\n\n")
    qs = [
        mcq("A fable is a short story that usually has ____ and teaches a "
            "moral.",
            "animal characters that talk and act like people",
            ["real people from history", "no characters at all",
             "only machines"],
            "Fables star talking animals and end with a lesson (moral). "
            "Aesop is the most famous fable teller."),
        mcq("The lesson a fable teaches is called its ____.",
            "moral", ["setting", "title", "rhyme"],
            "The moral is the lesson, often stated right at the end of the "
            "fable."),
        mcq("What is the moral of 'The Tortoise and the Hare'?",
            "Slow and steady wins the race",
            ["Always take a nap", "Fast animals always win",
             "Never race a friend"],
            "The speedy hare naps; the slow, steady tortoise keeps going "
            "and wins."),
        mcq("In 'The Boy Who Cried Wolf', why does no one come when the "
            "real wolf appears?",
            "The boy had lied so many times that no one believed him",
            ["The town was empty", "The wolf was friendly",
             "The boy didn't yell loudly enough"],
            "The moral: if you lie, people won't believe you when you tell "
            "the truth."),
        mcq("What is the moral of 'The Ant and the Grasshopper'?",
            "Work hard and prepare for the future",
            ["Music is a waste of time", "Winter never comes",
             "Ants are mean"],
            "The ant stores food all summer; the grasshopper plays and "
            "goes hungry when winter comes."),
        mcq("In 'The Lion and the Mouse', the tiny mouse frees the lion "
            "from a net. What is the moral?",
            "Even a small friend can be a big help",
            ["Lions are weak", "Never help anyone",
             "Mice are smarter than lions"],
            "Kindness is repaid — and being small doesn't mean you can't "
            "help."),
        mcq("A folktale is a story that ____.",
            "was passed down by telling over many years",
            ["one famous author wrote last year",
             "is always about real events", "must rhyme"],
            "Folktales are handed down by word of mouth; the author is "
            "usually unknown."),
        mcq("A fairy tale is a folktale that usually has ____.",
            "magic in it", ["only true facts", "no characters",
            "a table of contents"],
            "Fairy tales have magic — spells, fairies, talking objects — "
            "and often start 'Once upon a time.'"),
        mcq("A tall tale is a funny story famous for ____.",
            "wild exaggeration", ["being completely true", "having no hero",
            "being very short"],
            "Tall tales stretch the truth in giant ways — like Paul Bunyan "
            "being taller than the trees."),
        # Passage: The Two Squirrels
        mcq(p1 + "What is the moral of this fable?",
            "Work and get ready before you play",
            ["Never share acorns", "Winter is fun",
             "Laughing is bad"],
            "Rex says it himself: 'I will work first and play later.'"),
        mcq(p1 + "Which classic fable is this story most like?",
            "The Ant and the Grasshopper", ["The Tortoise and the Hare",
            "The Boy Who Cried Wolf", "The Lion and the Mouse"],
            "One character prepares for winter while the other plays — "
            "just like the ant and the grasshopper."),
        mcq(p1 + "Why was there nothing for Rex to eat in winter?",
            "He played all fall instead of storing food",
            ["Pip stole his food", "The oak tree fell down",
             "He was too small to eat acorns"],
            "Rex 'just played in the leaves' while Pip buried acorns."),
        mcq(p1 + "What kind act does Pip do?",
            "He shares his acorns with Rex",
            ["He laughs at Rex", "He hides the acorns from Rex",
             "He moves to a new tree"],
            "Even though Rex laughed at him, Pip shared — kindness is part "
            "of the lesson."),
        # Passage: The Little Blue Boat
        mcq(p2 + "What is the central message of this story?",
            "Small ones can do big, important things",
            ["Big ships are useless", "Never sail at night",
             "Stay tied to the dock"],
            "The little boat's tiny light saved a big ship — small doesn't "
            "mean unimportant."),
        mcq(p2 + "Which classic fable has a message most like this story?",
            "The Lion and the Mouse", ["The Fox and the Grapes",
            "The Tortoise and the Hare", "The Boy Who Cried Wolf"],
            "Both teach that even the small can be a big help."),
        mcq(p2 + "How does the little boat feel at the beginning, and how "
            "does it change?",
            "It feels too small to matter, then feels proud",
            ["It feels proud, then small", "It never changes",
             "It feels angry, then sleepy"],
            "It sighs 'I am too small to matter' — but 'never called "
            "itself small again' after saving the ship."),
        tf("A fable's moral is often stated at the end of the story.",
           True, "Fables usually finish by telling you the lesson."),
        short("What do we call a story passed down by telling, whose "
              "author is unknown — a folktale or a biography?",
              "folktale", "Folktales are passed down by word of mouth over "
              "many years."),
    ]
    kb = (
        "# Grade 2 ELA — Fables, Folktales & Morals\n\n"
        "**Standard: RL.2.2** — recount fables and folktales and find their "
        "central message, lesson, or moral.\n\n"
        "## Story kinds\n"
        "- **Fable** — short story, usually talking animals, teaches a "
        "**moral** (Aesop's fables)\n"
        "- **Folktale** — passed down by telling; author unknown\n"
        "- **Fairy tale** — folktale with magic ('Once upon a time…')\n"
        "- **Tall tale** — wild exaggeration for laughs (Paul Bunyan)\n"
        "- **Legend** — old story about a hero, partly based on real "
        "people or places\n\n"
        "## Famous fables and their morals\n"
        "- **The Tortoise and the Hare** — slow and steady wins the race\n"
        "- **The Boy Who Cried Wolf** — if you lie, people won't believe "
        "you when you tell the truth\n"
        "- **The Ant and the Grasshopper** — work hard and prepare for the "
        "future\n"
        "- **The Lion and the Mouse** — even small friends can be a big "
        "help; kindness is repaid\n"
        "- **The Fox and the Grapes** — it's easy to pretend you didn't "
        "want what you can't have\n"
        "- **The Crow and the Pitcher** — think your way out of a problem, "
        "little by little\n"
        "- **The Wind and the Sun** — gentleness works better than force\n"
        "- **The Goose That Laid the Golden Eggs** — greed can lose you "
        "what you already have\n\n"
        "## Big idea\n"
        "The **central message** (or moral) is the big idea the story "
        "wants you to learn. Ask: what did the character learn? What "
        "should I remember from this?" + SRC)
    return {"name": "Fables, Folktales & Morals",
            "source": {"title": "Fables & morals — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 11: Poems, Points of View & Comparing Stories ------------------
def ch_poems_versions():
    p1 = ("Read the story:\n\n"
          "\"'Rain is the worst,' groaned Sam, staring out the window at "
          "his dry soccer ball. In the next room, his sister Ana cheered "
          "and grabbed her paint set. 'Rain is the best,' she said. 'Now I "
          "have all day to finish my picture.'\"\n\n")
    qs = [
        mcq("Words that end with the same sound, like 'cat' and 'hat', "
            "____.",
            "rhyme", ["repeat", "alliterate", "whisper"],
            "Rhyming words share their ending sound: cat/hat, night/light, "
            "away/play."),
        mcq("Which pair of words rhymes?",
            "night / light", ["night / nose", "cat / dog", "run / walk"],
            "Night and light both end in the -ight sound."),
        mcq("The steady beat in a poem that you could clap along to is "
            "called ____.",
            "rhythm", ["rhyme", "a caption", "a moral"],
            "Rhythm is the pattern of beats — clap 'TWIN-kle TWIN-kle "
            "LIT-tle STAR' and you can feel it."),
        mcq("'Run, run, as fast as you can!' appears again and again in "
            "The Gingerbread Man. That is called ____.",
            "repetition (a repeated line)", ["rhyme", "alliteration",
            "a glossary"],
            "Saying a line again and again is repetition — it makes the "
            "story fun to say and easy to remember."),
        mcq("'Silly Sally sang seven songs' is an example of ____.",
            "alliteration (words starting with the same sound)",
            ["rhyme", "repetition", "a moral"],
            "Alliteration = several words that START with the same sound: "
            "S-s-s-s."),
        mcq("A word that sounds like the noise it names, like 'buzz' or "
            "'pop', is called ____.",
            "onomatopoeia", ["a rhyme", "a stanza", "a syllable"],
            "Buzz, crash, pop, hiss — the word makes the sound."),
        mcq("A group of lines in a poem, like a paragraph in a story, is "
            "called a ____.",
            "stanza", ["chapter", "caption", "sentence"],
            "Poems are built from stanzas — groups of lines with a space "
            "between groups."),
        mcq("Why do poets use rhyme, rhythm, and repeated lines?",
            "To give the poem music and feeling",
            ["To make the poem longer", "To hide the meaning",
             "Because it is a rule"],
            "Those word choices supply rhythm and meaning — they make a "
            "poem feel musical and help you feel something."),
        # Point of view
        mcq(p1 + "How do Sam and Ana feel about the SAME rainy day?",
            "Sam hates it, but Ana loves it",
            ["They both love it", "They both hate it",
             "Neither one cares"],
            "Two characters can have different points of view about the "
            "same event."),
        mcq(p1 + "Why does Ana think rain is the best?",
            "She gets all day to paint her picture",
            ["She loves soccer", "She wants to get wet",
             "She hates painting"],
            "'Now I have all day to finish my picture.'"),
        mcq(p1 + "How do you know the exact words each character says?",
            "The words are inside quotation marks",
            ["They are in capital letters", "They rhyme",
             "They are at the end of the story"],
            "Quotation marks show dialogue — the words a character "
            "actually says."),
        mcq("When a story is told by a character using 'I' and 'we', it "
            "is told in the ____ person.",
            "first", ["third", "second", "last"],
            "First person = a character tells it (I, we). Third person = "
            "an outside narrator (he, she, they)."),
        # Comparing versions
        mcq("Cinderella (France) and Yeh-Shen (China) are two versions of "
            "the same story. What stays the SAME?",
            "A kind, mistreated girl gets magical help and is rewarded",
            ["The girl is helped by fish bones in both",
             "Both happen in France", "Both girls wear glass slippers"],
            "Versions from different cultures keep the same big shape — "
            "kind girl, magical helper, happy ending — but change the "
            "details."),
        mcq("When you tell how two versions of a story are ALIKE and "
            "DIFFERENT, you are ____.",
            "comparing and contrasting", ["rhyming", "editing",
            "alphabetizing"],
            "Compare = find what's the same; contrast = find what's "
            "different."),
        mcq("Which signal word tells you two things are DIFFERENT?",
            "but", ["both", "same", "also"],
            "both/same/alike signal likeness; but/different/unlike signal "
            "difference."),
        tf("Two characters in the same story always feel the same way "
           "about what happens.",
           False, "Characters can have different points of view — like Sam "
           "and Ana on the rainy day."),
        short("What do we call words that end with the same sound, like "
              "'day' and 'play'?",
              "rhyme", "They rhyme — same ending sound."),
    ]
    kb = (
        "# Grade 2 ELA — Poems, Points of View & Comparing Stories\n\n"
        "**Standards: RL.2.4, RL.2.6, RL.2.9.**\n\n"
        "## Poem words\n"
        "- **Rhyme** — same ending sound: cat/hat, night/light\n"
        "- **Rhythm** — the beat you can clap along to\n"
        "- **Repetition** — a line said again and again ('Run, run, as "
        "fast as you can!')\n"
        "- **Alliteration** — words starting with the same sound ('Silly "
        "Sally sang…')\n"
        "- **Onomatopoeia** — a word that sounds like its noise (buzz, "
        "pop, crash)\n"
        "- **Stanza** — a group of lines, like a paragraph\n"
        "These choices give a poem **music and feeling**.\n\n"
        "## Points of view (RL.2.6)\n"
        "- Different characters can **think and feel differently** about "
        "the same events.\n"
        "- **Dialogue** = the words characters say, inside **quotation "
        "marks**; tags like *said/asked/shouted/whispered* tell who is "
        "talking and how.\n"
        "- **First person** = a character tells the story (I, we). "
        "**Third person** = an outside narrator (he, she, they).\n\n"
        "## Comparing versions of a story (RL.2.9)\n"
        "- The same story can be told by different authors or cultures: "
        "*Cinderella* (France), *Yeh-Shen* (China), *The Rough-Face Girl* "
        "(Algonquin).\n"
        "- What stays the same: the roles, the basic plot, the lesson. "
        "What changes: names, setting, magical details, endings.\n"
        "- Signal words — alike: **both, same, also**; different: **but, "
        "unlike, however**." + SRC)
    return {"name": "Poems, Points of View & Comparing Stories",
            "source": {"title": "Poems & comparing stories — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 12: Informational Text & Text Features (RI.2.2/5) --------------
def ch_info_features():
    p1 = ("Read about honeybees:\n\n"
          "\"A honeybee hive is a busy place. Worker bees fly from flower "
          "to flower collecting a sweet liquid called nectar. Back at the "
          "hive, bees turn the nectar into honey and store it in wax rooms "
          "called cells. One hive can hold thousands of bees, but only one "
          "queen. Without honeybees, many plants could not make seeds.\"\n\n")
    qs = [
        mcq(p1 + "What is the main topic of this text?",
            "honeybees and their hive", ["flowers", "wax candles",
            "how to keep pets"],
            "Every sentence tells about honeybees and the hive — that's "
            "the main topic."),
        mcq(p1 + "What is nectar?",
            "a sweet liquid bees collect from flowers",
            ["a kind of wax", "a baby bee", "a type of honey plant"],
            "The text defines it right there: 'a sweet liquid called "
            "nectar.'"),
        mcq(p1 + "How many queens live in one hive?",
            "one", ["thousands", "two", "none"],
            "'…thousands of bees, but only one queen.'"),
        mcq(p1 + "What are the wax rooms where honey is stored called?",
            "cells", ["nests", "cubbies", "jars"],
            "'…store it in wax rooms called cells.'"),
        mcq(p1 + "Why do plants need honeybees?",
            "Without bees, many plants could not make seeds",
            ["Bees water the plants", "Bees eat weeds",
             "Bees keep plants warm"],
            "The last sentence gives the reason plants depend on bees."),
        mcq("The MAIN TOPIC of a whole text is ____.",
            "what the whole text is mostly about",
            ["the first word", "what one sentence says",
             "the number of pages"],
            "Ask: 'What is this MOSTLY about?' A repeated idea or a "
            "repeated word is a clue."),
        mcq("In a multi-paragraph text, each paragraph usually has ____.",
            "its own focus (what that paragraph is mostly about)",
            ["its own author", "its own title page", "its own glossary"],
            "Grade 2 asks for the main topic of the WHOLE text and the "
            "focus of EACH paragraph."),
        mcq("A table of contents is found at the ____ of a book and lists "
            "____.",
            "front; the chapters with their page numbers",
            ["back; word meanings", "front; word meanings",
             "back; the author's name"],
            "Table of contents = front of the book, chapters in order with "
            "page numbers."),
        mcq("A glossary is ____.",
            "an alphabetical list of important words WITH THEIR MEANINGS, "
            "at the back",
            ["a list of chapters at the front",
             "an alphabetical list of topics with page numbers",
             "a picture with labels"],
            "Glossary = meanings of words. Don't mix it up with the index, "
            "which gives page numbers."),
        mcq("An index is ____.",
            "an alphabetical list of topics with page numbers, at the back",
            ["a list of word meanings", "the name of the book",
             "a labeled drawing"],
            "Index = where to FIND each topic. Glossary = what words "
            "MEAN."),
        mcq("You want to know what the word 'nectar' means in a bee book. "
            "Where should you look?",
            "the glossary", ["the index", "the table of contents",
            "the cover"],
            "The glossary gives meanings of important words."),
        mcq("You want to find every page that talks about 'queen bees'. "
            "Where should you look?",
            "the index", ["the glossary", "the title", "a caption"],
            "The index lists topics alphabetically with every page number "
            "where they appear."),
        mcq("The words printed under or next to a picture, telling what "
            "it shows, are called a ____.",
            "caption", ["heading", "glossary", "stanza"],
            "Captions explain pictures."),
        mcq("Why is a word sometimes printed in BOLD (dark) letters in an "
            "informational book?",
            "It is an important word — often defined in the glossary",
            ["It is a mistake", "It rhymes",
             "The printer ran out of ink"],
            "Bold print flags important vocabulary."),
        mcq("A labeled drawing that shows the parts of something or how "
            "it works is called a ____.",
            "diagram", ["caption", "index", "stanza"],
            "Diagrams show parts and how things work — great for 'how a "
            "machine works.'"),
        mcq("Headings (section titles) help a reader ____.",
            "find the part about a topic quickly",
            ["skip the whole book", "learn word meanings",
             "count the pages"],
            "A heading tells what a section is about, so you can jump "
            "straight to what you need."),
        tf("The index of a book is at the front.",
           False, "The index is at the BACK. The table of contents is at "
           "the front."),
        short("Which text feature — glossary or index — tells you what a "
              "word MEANS?",
              "glossary", "Glossary = meanings; index = page numbers for "
              "topics."),
    ]
    kb = (
        "# Grade 2 ELA — Informational Text & Text Features\n\n"
        "**Standards: RI.2.1, RI.2.2, RI.2.4, RI.2.5.**\n\n"
        "## Main topic and paragraph focus\n"
        "- **Main topic** = what the WHOLE text is mostly about.\n"
        "- **Focus of a paragraph** = what THAT paragraph is mostly "
        "about.\n"
        "- The **main idea** is the most important point; **key details** "
        "tell more about it. The first sentence (topic sentence) often "
        "holds the main idea.\n\n"
        "## Text features and their jobs\n"
        "- **Title** — what the whole text is about\n"
        "- **Table of contents** — FRONT; chapters in order with page "
        "numbers\n"
        "- **Heading / subheading** — what a section is about\n"
        "- **Caption** — words that explain a picture\n"
        "- **Bold print / italics** — flags an important word\n"
        "- **Glossary** — BACK; alphabetical list of words WITH MEANINGS\n"
        "- **Index** — BACK; alphabetical list of topics WITH PAGE "
        "NUMBERS\n"
        "- **Diagram** — labeled drawing showing parts or how something "
        "works\n"
        "- **Chart/table** — facts in rows and columns\n"
        "- **Map** — shows where\n"
        "- **Electronic menu / icon** — what to click on a website\n\n"
        "**Top mix-up:** glossary and index are both alphabetical and at "
        "the back — the glossary gives **meanings**, the index gives "
        "**page numbers**." + SRC)
    return {"name": "Informational Text & Text Features",
            "source": {"title": "Text features — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 13: Sequence, Cause & Effect, Author's Purpose (RI.2.3/6/8) ----
def ch_info_skills():
    p1 = ("Read about butterflies:\n\n"
          "\"A butterfly begins life as a tiny egg on a leaf. First, a "
          "caterpillar hatches from the egg and eats leaves day and night. "
          "Next, the caterpillar makes a hard case around itself called a "
          "chrysalis. Inside the chrysalis, its body slowly changes. "
          "Finally, a butterfly breaks out, dries its wings, and flies "
          "away.\"\n\n")
    p2 = ("Read about the Chesapeake Bay:\n\n"
          "\"The Chesapeake Bay is the largest estuary in the United "
          "States. An estuary is a place where fresh river water mixes "
          "with salty ocean water. The Bay touches two states, Maryland "
          "and Virginia. Blue crabs, oysters, and striped bass all live in "
          "its waters. Many Maryland families catch and eat blue crabs "
          "every summer.\"\n\n")
    p3 = ("Read this:\n\n"
          "\"Every bike rider should wear a helmet. A helmet protects "
          "your head if you fall. Doctors say helmets stop many serious "
          "injuries every year. A helmet also keeps sun and rain off your "
          "face. Smart riders buckle their helmets before every single "
          "ride.\"\n\n")
    qs = [
        # Butterfly sequence
        mcq(p1 + "What hatches from the egg?",
            "a caterpillar", ["a butterfly", "a chrysalis", "a bird"],
            "'First, a caterpillar hatches from the egg.' The butterfly "
            "comes at the very end."),
        mcq(p1 + "What does the caterpillar do right BEFORE its body "
            "starts to change?",
            "makes a hard case (chrysalis) around itself",
            ["flies away", "dries its wings", "lays an egg"],
            "Order matters: eat → make a chrysalis → change inside → "
            "break out."),
        mcq(p1 + "What is a chrysalis?",
            "the hard case a caterpillar makes around itself",
            ["a kind of leaf", "a baby butterfly's name", "a bird's nest"],
            "The text defines it: 'a hard case around itself called a "
            "chrysalis.'"),
        mcq(p1 + "Which words signal the ORDER of the steps?",
            "First, Next, Finally", ["tiny, hard, slowly",
            "egg, leaf, wing", "day, night, away"],
            "First, next, then, and finally are sequence words — they "
            "show what order steps happen in."),
        # Cause and effect
        mcq("'Because it rained, the game was canceled.' What is the "
            "CAUSE?",
            "the rain", ["the canceled game", "the players",
            "the field"],
            "The cause is WHY it happened (rain); the effect is WHAT "
            "happened (the game was canceled)."),
        mcq("'The power went out, so we lit candles.' What is the "
            "EFFECT?",
            "we lit candles", ["the power going out", "the storm",
            "the candles melting"],
            "The effect is what happened as a result. Signal words: "
            "because, so, since."),
        # Chesapeake
        mcq(p2 + "What is an estuary?",
            "a place where fresh river water mixes with salty ocean water",
            ["a kind of blue crab", "a fishing boat",
             "a Maryland town"],
            "The second sentence is a definition — informational texts "
            "often define their big words right in the text."),
        mcq(p2 + "Which two states does the Chesapeake Bay touch?",
            "Maryland and Virginia", ["Maryland and Delaware",
            "Virginia and Ohio", "Texas and Florida"],
            "'The Bay touches two states, Maryland and Virginia.'"),
        mcq(p2 + "What is the author's main purpose in this text?",
            "to give facts about (describe) the Chesapeake Bay",
            ["to make you buy a crab", "to tell a made-up story",
             "to teach you to swim"],
            "It's full of facts — the purpose is to inform/describe."),
        mcq(p2 + "Which of these is a FACT from the text (not an "
            "opinion)?",
            "Blue crabs live in the Chesapeake Bay",
            ["Crabs taste better than pizza", "Summer is the best season",
             "Everyone should visit the Bay"],
            "A fact can be proven true. 'Tastes better' and 'best' are "
            "opinions."),
        # Helmet — point and reasons
        mcq(p3 + "What is the author's main point?",
            "Every bike rider should wear a helmet",
            ["Bikes are dangerous and should be banned",
             "Helmets are too hot", "Riding in rain is fun"],
            "The first sentence states the point; the rest gives "
            "reasons."),
        mcq(p3 + "Which reason does the author give to SUPPORT the "
            "point?",
            "A helmet protects your head if you fall",
            ["Helmets come in many colors", "Bikes are fast",
             "Doctors ride bikes"],
            "Authors back up their points with reasons — protection is "
            "reason number one."),
        mcq(p3 + "The author of this text is mostly trying to ____.",
            "persuade you to wear a helmet", ["entertain you with a story",
            "teach you to ride a bike", "describe kinds of bikes"],
            "It tells you what you SHOULD do — that's persuading."),
        # Purpose concepts
        mcq("The three main author's purposes are to persuade, to inform, "
            "and to ____.",
            "entertain", ["exercise", "erase", "explode"],
            "P-I-E: Persuade (change your mind), Inform (teach facts), "
            "Entertain (tell an enjoyable story)."),
        mcq("A made-up story about a talking dog is written mostly to "
            "____.",
            "entertain", ["inform", "persuade", "give directions"],
            "Stories entertain; fact books inform; ads and opinion pieces "
            "persuade."),
        mcq("Which sentence is an OPINION?",
            "Spiders are creepy", ["A spider has eight legs",
            "Spiders spin webs", "Some spiders live in houses"],
            "An opinion is what someone thinks or feels — it can't be "
            "proven. Clue words: think, feel, best, worst, creepy."),
        tf("A fact is something that can be proven true.",
           True, "Facts can be checked ('a spider has eight legs'); "
           "opinions are thoughts and feelings."),
        short("In 'Because the snow fell all night, school was closed' — "
              "what one word names the cause?",
              "snow", "The snow (falling all night) is WHY school "
              "closed."),
    ]
    kb = (
        "# Grade 2 ELA — Sequence, Cause & Effect, Author's Purpose\n\n"
        "**Standards: RI.2.3, RI.2.6, RI.2.8 (+ fact vs. opinion).**\n\n"
        "## Connections between ideas (RI.2.3)\n"
        "- **Sequence** = steps or events in order. Signal words: first, "
        "next, then, after that, finally.\n"
        "- Sequences to know: butterfly life cycle (egg → caterpillar → "
        "chrysalis → butterfly); frog (egg → tadpole → froglet → frog); "
        "plant (seed → sprout → plant → flower → new seeds).\n"
        "- **Cause and effect**: the cause is WHY it happened; the effect "
        "is WHAT happened. Signal words: because, so, since, as a "
        "result.\n\n"
        "## Author's purpose (RI.2.6)\n"
        "- **P**ersuade — change your mind or get you to do something "
        "(ads, opinion pieces)\n"
        "- **I**nform — teach facts (fact books, articles)\n"
        "- **E**ntertain — tell an enjoyable story\n"
        "- Authors make **points** and support them with **reasons** "
        "(RI.2.8) — listen for 'because.'\n\n"
        "## Fact vs. opinion\n"
        "- **Fact** — can be proven true: 'A spider has eight legs.'\n"
        "- **Opinion** — what someone thinks or feels: 'Spiders are "
        "creepy.' Clue words: think, feel, believe, best, worst, "
        "favorite, should." + SRC)
    return {"name": "Sequence, Cause & Effect, Author's Purpose",
            "source": {"title": "Informational reading skills — knowledge "
                       "base", "content": kb},
            "questions": qs}


# --- Chapter 14: Nouns & Pronouns (L.2.1a-c) --------------------------------
def ch_nouns_pronouns():
    qs = [
        mcq("A word that names a whole GROUP, like 'team' or 'flock', is "
            "called a ____ noun.",
            "collective", ["proper", "silent", "past-tense"],
            "Collective nouns name groups: team, class, family, crowd, "
            "herd, flock."),
        mcq("A group of cows or elephants is called a ____.",
            "herd", ["flock", "school", "litter"],
            "A herd of cows; a flock of birds; a school of fish."),
        mcq("A group of birds is called a ____.",
            "flock", ["herd", "pride", "deck"],
            "Birds (and sheep) come in flocks."),
        mcq("A group of fish is called a ____.",
            "school", ["class", "herd", "pack"],
            "A school of fish — yes, the same word as the school you "
            "attend!"),
        mcq("A group of wolves is called a ____.",
            "pack", ["swarm", "bunch", "choir"],
            "A pack of wolves; a swarm of bees; a pride of lions."),
        mcq("A group of puppies born together is called a ____.",
            "litter", ["pile", "band", "army"],
            "A litter of puppies or kittens."),
        mcq("What is the plural of 'foot'?",
            "feet", ["foots", "feets", "footes"],
            "Foot → feet is an irregular plural — no -s ending, the word "
            "changes."),
        mcq("What is the plural of 'child'?",
            "children", ["childs", "childes", "childrens"],
            "Child → children. Irregular plurals must be memorized."),
        mcq("What is the plural of 'tooth'?",
            "teeth", ["tooths", "toothes", "teeths"],
            "Tooth → teeth, just like foot → feet."),
        mcq("What is the plural of 'mouse'?",
            "mice", ["mouses", "mousees", "mices"],
            "Mouse → mice. (Goose → geese works the same way.)"),
        mcq("What is the plural of 'woman'?",
            "women", ["womans", "womens", "woman"],
            "Man → men and woman → women."),
        mcq("What is the plural of 'sheep'?",
            "sheep (it stays the same)", ["sheeps", "shoop", "sheepes"],
            "Some words don't change at all: one sheep, two sheep — same "
            "for fish, deer, and moose."),
        mcq("What is the plural of 'leaf'?",
            "leaves", ["leafs", "leafes", "leave"],
            "f changes to v: leaf → leaves, wolf → wolves, knife → "
            "knives."),
        mcq("Which word correctly completes: 'I made this card ____.'",
            "myself", ["meself", "myselves", "ourselves"],
            "Reflexive pronouns point back at the doer: I → myself, we → "
            "ourselves."),
        mcq("Which word correctly completes: 'We built the fort ____.'",
            "ourselves", ["ourself", "myself", "themself"],
            "we → ourselves; they → themselves; he → himself."),
        mcq("Which of these is NOT a real word?",
            "hisself", ["himself", "herself", "themselves"],
            "It's 'himself,' never 'hisself' — and 'themselves,' never "
            "'theirselves.'"),
        tf("The plural of 'fish' is 'fishes.'",
           False, "Fish stays fish: one fish, two fish. (Dr. Seuss got it "
           "right!)"),
        short("What is the plural of 'goose'?",
              "geese", "Goose → geese, like tooth → teeth."),
        short("What is the plural of 'man'?",
              "men", "Man → men; woman → women."),
    ]
    kb = (
        "# Grade 2 ELA — Nouns & Pronouns\n\n"
        "**Standards: L.2.1a (collective nouns), L.2.1b (irregular "
        "plurals), L.2.1c (reflexive pronouns).**\n\n"
        "## Collective nouns — one word for a whole group\n"
        "team (players) · class (students) · family · crowd · audience · "
        "band (musicians) · herd (cows) · flock (birds, sheep) · pack "
        "(wolves) · swarm (bees) · school (fish) · litter (puppies) · "
        "pride (lions) · colony (ants, penguins) · bunch (grapes)\n\n"
        "## Irregular plurals — no -s; the word changes (memorize!)\n"
        "foot→feet · tooth→teeth · child→children · man→men · woman→women "
        "· mouse→mice · goose→geese · person→people · leaf→leaves · "
        "wolf→wolves · knife→knives · shelf→shelves · half→halves\n"
        "Stay the SAME: fish, sheep, deer, moose.\n\n"
        "## Reflexive pronouns — point back at the doer\n"
        "myself, yourself, himself, herself, itself, ourselves, "
        "yourselves, themselves.\n"
        "'I made it **myself**.' 'We built it **ourselves**.'\n"
        "**Not words:** hisself, theirselves." + SRC)
    return {"name": "Nouns & Pronouns",
            "source": {"title": "Nouns & pronouns — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 15: Verbs, Adverbs & Sentences (L.2.1d-f) ----------------------
def ch_verbs_sentences():
    qs = [
        mcq("What is the past tense of 'sit'?",
            "sat", ["sitted", "sits", "sitting"],
            "Sit → sat is irregular — no -ed. 'Yesterday I sat by the "
            "window.'"),
        mcq("What is the past tense of 'go'?",
            "went", ["goed", "gone to", "goes"],
            "Go → went. Irregular past-tense verbs change the whole "
            "word."),
        mcq("What is the past tense of 'eat'?",
            "ate", ["eated", "eaten", "eats"],
            "Eat → ate: 'Last night we ate pizza.'"),
        mcq("What is the past tense of 'tell'?",
            "told", ["telled", "tells", "telling"],
            "Tell → told; sell → sold."),
        mcq("What is the past tense of 'hide'?",
            "hid", ["hided", "hides", "hidden up"],
            "Hide → hid: 'The dog hid the bone yesterday.'"),
        mcq("What is the past tense of 'catch'?",
            "caught", ["catched", "catches", "caughted"],
            "Catch → caught; teach → taught; think → thought; buy → "
            "bought."),
        mcq("What is the past tense of 'fly'?",
            "flew", ["flied", "flys", "flying"],
            "Fly → flew; grow → grew; know → knew; throw → threw."),
        mcq("What is the past tense of 'write'?",
            "wrote", ["writed", "written down", "writes"],
            "Write → wrote: 'She wrote a letter last week.'"),
        mcq("An adjective describes a ____; an adverb describes a ____.",
            "noun; verb", ["verb; noun", "sentence; letter",
            "person; place"],
            "Adjective → thing ('the QUICK dog'). Adverb → action ('ran "
            "QUICKLY') — how, when, or where."),
        mcq("Choose the right word: 'The dog ran ____ across the yard.'",
            "quickly", ["quick", "quickest", "more quick"],
            "You're describing HOW it ran (an action) — use the adverb "
            "'quickly.'"),
        mcq("Choose the right word: 'The ____ music woke the baby.'",
            "loud", ["loudly", "loudest of all", "louder than"],
            "You're describing the music (a thing/noun) — use the "
            "adjective 'loud.'"),
        mcq("Which sentence is correct?",
            "He sings well.", ["He sings good.", "He sing goodly.",
            "He singing good."],
            "'Good' is an adjective; to describe HOW someone sings you "
            "need the adverb 'well.'"),
        mcq("Many adverbs end in which two letters?",
            "-ly", ["-ed", "-es", "-un"],
            "quickly, slowly, loudly, kindly, sadly — the -ly ending "
            "means 'in a ___ way.'"),
        mcq("A complete sentence needs a subject (who or what) and a "
            "____.",
            "predicate (what the subject does or is)",
            ["rhyme", "picture", "question mark"],
            "Subject + predicate = complete thought. 'Ran to the store.' "
            "has no subject — it's a fragment."),
        mcq("Which of these is a COMPOUND sentence (two complete thoughts "
            "joined together)?",
            "It rained, so we stayed inside.",
            ["The big brown dog barked.", "Ran fast down the hill.",
             "My favorite lunch."],
            "Two complete thoughts joined by a comma + joining word (and, "
            "but, or, so) make a compound sentence."),
        mcq("Which joining words can glue two sentences into a compound "
            "sentence?",
            "and, but, or, so", ["the, a, an", "very, really, quite",
            "in, on, under"],
            "'I like pizza, AND my sister likes tacos.' 'It rained, SO we "
            "stayed inside.'"),
        mcq("Which of these is a FRAGMENT (not a complete sentence)?",
            "Under the big bed.", ["The cat hid under the bed.",
            "We looked everywhere.", "She found the cat."],
            "'Under the big bed.' has no subject doing anything — it's "
            "only a piece of a sentence."),
        mcq("Expand this sentence with a detail: 'The dog barked.' Which "
            "choice ADDS detail correctly?",
            "The big brown dog barked loudly at the mail truck.",
            ["The dog.", "Barked barked barked.", "Dog the barked."],
            "Expanding = adding describing words and details while "
            "keeping the sentence complete."),
        tf("The past tense of 'run' is 'runned.'",
           False, "Run → ran. It's irregular — no -ed."),
        short("What is the past tense of 'see'?",
              "saw", "See → saw: 'I saw a deer yesterday.'"),
        short("What is the past tense of 'make'?",
              "made", "Make → made: 'We made cookies last night.'"),
    ]
    kb = (
        "# Grade 2 ELA — Verbs, Adverbs & Sentences\n\n"
        "**Standards: L.2.1d (irregular past tense), L.2.1e (adjectives "
        "vs. adverbs), L.2.1f (simple & compound sentences).**\n\n"
        "## Irregular past-tense verbs (no -ed — the word changes)\n"
        "sit→sat · go→went · see→saw · eat→ate · run→ran · come→came · "
        "tell→told · hide→hid · say→said · make→made · give→gave · "
        "take→took · ride→rode · write→wrote · sing→sang · swim→swam · "
        "fall→fell · fly→flew · grow→grew · know→knew · throw→threw · "
        "catch→caught · teach→taught · think→thought · buy→bought · "
        "bring→brought · sleep→slept · keep→kept · stand→stood · "
        "break→broke · get→got · do→did · have→had\n"
        "Stay the same: put, cut, hit, let, read (spelling).\n\n"
        "## Adjective or adverb?\n"
        "- **Adjective** describes a NOUN: 'the **quick** dog.'\n"
        "- **Adverb** describes a VERB — how/when/where: 'ran "
        "**quickly**.' Many end in **-ly**.\n"
        "- Describing a thing → adjective; describing an action → "
        "adverb.\n"
        "- Watch out: 'He sings **well**' (not 'good').\n\n"
        "## Sentences\n"
        "- **Complete sentence** = subject (who/what) + predicate (what "
        "they do or are). A **fragment** is missing a part.\n"
        "- **Simple sentence** = one complete thought.\n"
        "- **Compound sentence** = two complete thoughts joined by a "
        "**comma + and/but/or/so**: 'It rained, so we stayed inside.'\n"
        "- **Expand** a sentence by adding details; **rearrange** it by "
        "saying it another way." + SRC)
    return {"name": "Verbs, Adverbs & Sentences",
            "source": {"title": "Verbs & sentences — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 16: Capitals, Commas & Apostrophes (L.2.2) ---------------------
def ch_mechanics():
    qs = [
        mcq("Which sentence is capitalized correctly?",
            "We watched fireworks on the Fourth of July.",
            ["We watched fireworks on the fourth of july.",
             "we watched fireworks on the Fourth Of July.",
             "We watched Fireworks on the fourth of July."],
            "Holidays are capitalized: Fourth of July, Thanksgiving, "
            "Halloween."),
        mcq("Which word in this list should be capitalized: 'cereal, "
            "cheerios, breakfast, bowl'?",
            "cheerios", ["cereal", "breakfast", "bowl"],
            "Product (brand) names are capitalized: Cheerios, Lego. The "
            "plain thing — cereal, blocks — stays lowercase."),
        mcq("Which sentence capitalizes the place names correctly?",
            "We crossed the Chesapeake Bay to visit Annapolis.",
            ["We crossed the chesapeake bay to visit annapolis.",
             "We crossed the Chesapeake bay to visit annapolis.",
             "we crossed the chesapeake Bay to visit Annapolis."],
            "Geographic names — bays, cities, states — are capitalized: "
            "Chesapeake Bay, Annapolis, Maryland."),
        mcq("Which is written correctly?",
            "Maryland", ["maryland", "MaryLand", "mary land"],
            "State names are always capitalized."),
        mcq("In a friendly letter, a comma goes after the greeting. Which "
            "is correct?",
            "Dear Grandma,", ["Dear Grandma.", "Dear, Grandma",
            "dear grandma"],
            "The greeting takes a comma: 'Dear Grandma,'"),
        mcq("Which letter CLOSING is punctuated correctly?",
            "Your friend,", ["Your friend.", "Your, friend",
            "your friend!"],
            "Closings take a comma too: 'Your friend,' / 'Love,' / "
            "'Sincerely,'"),
        mcq("In a contraction, the apostrophe shows ____.",
            "where letters were taken out",
            ["the end of a sentence", "a question",
             "that a word is important"],
            "isn't = is not: the apostrophe replaces the missing o."),
        mcq("'Can't' is short for ____.",
            "cannot", ["can it", "candy", "could not"],
            "can + not squeeze into can't."),
        mcq("Which contraction means 'will not'?",
            "won't", ["willn't", "wan't", "whon't"],
            "The odd one out: will not → won't (memorize it)."),
        mcq("'Let's go to the park!' — 'let's' is short for ____.",
            "let us", ["lets", "letters", "let is"],
            "let's = let us."),
        mcq("Which shows that the bone belongs to the dog?",
            "the dog's bone", ["the dogs bone", "the dog bone's",
            "the dogs' bone"],
            "Add apostrophe + s to a singular noun to show owning: the "
            "dog's bone, Maria's book."),
        mcq("Choose the right word: '____ starting to rain!'",
            "It's", ["Its", "Its'", "It"],
            "It's = it is: 'It is starting to rain.' Its (no apostrophe) "
            "= belonging to it."),
        mcq("Which sentence is correct?",
            "The bird flapped its wings.", ["The bird flapped it's wings.",
            "The bird flapped its' wings.", "The bird flapped it wings."],
            "Belonging to it = its, with NO apostrophe. It's always means "
            "'it is.'"),
        mcq("What are the five parts of a friendly letter?",
            "date, greeting, body, closing, signature",
            ["title, chapters, glossary, index, cover",
             "subject, verb, noun, comma, period",
             "beginning, middle, end, moral, title"],
            "Date at the top, 'Dear ___,' (greeting), the message (body), "
            "'Your friend,' (closing), and your name (signature)."),
        tf("The sentence 'i live in maryland' is written correctly.",
           False, "The pronoun I and the state Maryland are both "
           "capitalized: 'I live in Maryland.'"),
        tf("Days of the week and months, like Monday and July, are "
           "capitalized.",
           True, "Monday, Tuesday, January, July — always capital "
           "letters."),
        short("Write the contraction for 'is not.'",
              "isn't", "is + not = isn't; the apostrophe replaces the "
              "missing o."),
        short("Write the contraction for 'they are.'",
              "they're", "they + are = they're."),
    ]
    kb = (
        "# Grade 2 ELA — Capitals, Commas & Apostrophes\n\n"
        "**Standard: L.2.2a-c.**\n\n"
        "## Capitalize\n"
        "1. The first word of every sentence, and the pronoun **I**\n"
        "2. Names of people and pets (and titles: Dr. Lee)\n"
        "3. **Holidays** — Thanksgiving, Halloween, Fourth of July\n"
        "4. **Product (brand) names** — Lego, Cheerios (but: blocks, "
        "cereal)\n"
        "5. **Geographic names** — Annapolis, Maryland, Chesapeake Bay, "
        "Atlantic Ocean (but plain words like 'city' or 'river' alone "
        "stay lowercase)\n"
        "6. Days and months — Monday, July\n\n"
        "## Commas in letters\n"
        "- After the greeting: **Dear Grandma,**\n"
        "- After the closing: **Your friend,** / **Love,**\n"
        "- Friendly-letter parts: date, greeting, body, closing, "
        "signature.\n\n"
        "## Apostrophes\n"
        "- **Contractions** — two words squeezed into one; the apostrophe "
        "replaces the missing letters: isn't, don't, can't, I'm, you're, "
        "we'll, they're, let's (= let us). Odd one: will not → "
        "**won't**.\n"
        "- **Possessives** — apostrophe + s shows owning: the dog's "
        "bone, Maria's book.\n"
        "- **The its/it's trap**: it's = it is; its (no apostrophe) = "
        "belonging to it." + SRC)
    return {"name": "Capitals, Commas & Apostrophes",
            "source": {"title": "Capitals & punctuation — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 17: Vocabulary (L.2.4, L.2.5) ----------------------------------
def ch_vocabulary():
    qs = [
        mcq("'The ENORMOUS elephant was too big to fit through the door.' "
            "What does 'enormous' mean?",
            "very big", ["very small", "gray", "friendly"],
            "Context clues: 'too big to fit' tells you enormous means "
            "very big."),
        mcq("'Maya was FAMISHED after skipping lunch, so she ate two "
            "sandwiches.' What does 'famished' mean?",
            "very hungry", ["very tired", "very angry", "full"],
            "She skipped lunch and ate two sandwiches — the clues point "
            "to very hungry."),
        mcq("A 'birdhouse' is ____.",
            "a house for birds", ["a bird that looks like a house",
            "a house shaped like a bird", "a kind of tree"],
            "Compound words = two words joined: bird + house = a house "
            "for birds."),
        mcq("Which word is a COMPOUND word (two smaller words joined "
            "together)?",
            "sunflower", ["sunny", "flowers", "yellow"],
            "sun + flower = sunflower. Others: raincoat, cupcake, "
            "mailbox, backpack."),
        mcq("What two words make up 'bookshelf'?",
            "book + shelf", ["books + elf", "boo + kshelf",
            "book + self"],
            "A bookshelf is a shelf for books."),
        mcq("The word 'bat' can mean an animal OR a baseball stick. 'A "
            "bat flew out of the cave at night.' Which meaning is used?",
            "the animal", ["the baseball stick", "a hat", "a kind of "
            "cave"],
            "It FLEW out of a cave — only the animal meaning makes "
            "sense. Context decides!"),
        mcq("'The dog's BARK woke the neighbors.' Which meaning of "
            "'bark' is this?",
            "the sound a dog makes", ["the outside of a tree",
            "a small boat", "a kind of park"],
            "Bark = dog sound or tree covering. A dog's bark waking "
            "people = the sound."),
        mcq("Which pair are SYNONYMS (words with almost the same "
            "meaning)?",
            "big / large", ["hot / cold", "up / down", "day / night"],
            "Synonyms mean nearly the same thing: big/large, happy/glad, "
            "fast/quick."),
        mcq("Which pair are ANTONYMS (opposites)?",
            "empty / full", ["small / tiny", "begin / start",
            "shut / close"],
            "Antonyms are opposites: empty/full, hot/cold, day/night."),
        mcq("Put these in order from GENTLEST to STRONGEST throw: ____",
            "toss → throw → hurl", ["hurl → toss → throw",
            "throw → toss → hurl", "toss → hurl → throw"],
            "Shades of meaning: toss (gentle), throw (normal), hurl "
            "(hard!)."),
        mcq("Which word is the STRONGEST way to say 'mad'?",
            "furious", ["annoyed", "grumpy", "bothered"],
            "annoyed → mad → angry → furious: furious is boiling-over "
            "mad."),
        mcq("Which word means to look at something for a LONG time "
            "without looking away?",
            "stare", ["glance", "blink", "peek"],
            "glance = a quick look; stare = a long, steady look."),
        mcq("'Whisper', 'say', 'shout', 'scream' — this list is ordered "
            "from ____.",
            "quietest to loudest", ["loudest to quietest",
            "shortest to longest", "first to last"],
            "Shades of meaning: whisper (quietest) up to scream "
            "(loudest)."),
        mcq("You read a word you don't know and there are no clues in "
            "the sentence. Which book tells you its meaning?",
            "a dictionary", ["an atlas", "a phone book",
            "a chapter book"],
            "A beginning dictionary lists words in alphabetical order "
            "and gives meanings and spellings."),
        mcq("The root word 'care' can grow into which family of words?",
            "careful, careless, caring", ["carrot, carry, cart",
            "car, card, care", "scare, scary, scared"],
            "A root word plus prefixes/suffixes makes a word family: "
            "care → careful (full of care), careless (without care)."),
        tf("'Butterfly' means a fly made of butter.",
           False, "Watch out — some compound words aren't the sum of "
           "their parts! A butterfly is an insect."),
        short("What do we call two words with OPPOSITE meanings, like "
              "'hot' and 'cold' — synonyms or antonyms?",
              "antonyms", "Antonyms are opposites; synonyms are "
              "near-twins."),
        short("What is the root (base) word of 'helper', 'helpful', and "
              "'helpless'?",
              "help", "All three grow from the root word 'help.'"),
    ]
    kb = (
        "# Grade 2 ELA — Vocabulary: Figuring Out New Words\n\n"
        "**Standards: L.2.4, L.2.5.**\n\n"
        "## Five ways to figure out a new word (L.2.4)\n"
        "1. **Context clues** — use the other words in the sentence: "
        "'The ENORMOUS elephant was too big to fit' → enormous = very "
        "big.\n"
        "2. **Prefix clues** — un+happy = not happy; re+tell = tell "
        "again.\n"
        "3. **Root words** — know 'help', unlock helper, helpful, "
        "helpless.\n"
        "4. **Compound words** — read the two words inside: birdhouse = "
        "house for birds. (Careful: a butterfly is not a fly made of "
        "butter!)\n"
        "5. **Glossary or dictionary** — look it up (alphabetical "
        "order).\n\n"
        "## Multiple-meaning words\n"
        "bat (animal / baseball stick) · bark (dog sound / tree "
        "covering) · ring (jewelry / bell sound) · trunk (elephant nose "
        "/ tree stem / car storage) · duck (bird / bend down) · watch "
        "(look at / wristwatch). The SENTENCE tells you which meaning "
        "fits.\n\n"
        "## Synonyms, antonyms, shades of meaning\n"
        "- **Synonyms** — almost the same: big/large, happy/glad, "
        "fast/quick\n"
        "- **Antonyms** — opposites: hot/cold, empty/full, day/night\n"
        "- **Shades of meaning** — related words in strength order:\n"
        "  - toss → throw → hurl\n"
        "  - glance → look → stare → glare\n"
        "  - whisper → say → shout → scream\n"
        "  - glad → happy → thrilled → overjoyed\n"
        "  - annoyed → mad → angry → furious\n"
        "  - big → large → huge → enormous" + SRC)
    return {"name": "Vocabulary: Figuring Out New Words",
            "source": {"title": "Vocabulary — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 18: Writing (W.2.1-3, W.2.5) -----------------------------------
def ch_writing():
    qs = [
        mcq("An OPINION piece starts by introducing the topic and then "
            "____.",
            "states an opinion and gives reasons for it",
            ["lists only facts", "tells a made-up story",
             "asks the reader to leave"],
            "Opinion writing: topic → opinion → reasons → linking words → "
            "concluding statement."),
        mcq("Which sentence states an OPINION for an opinion piece?",
            "I think dogs are the best pets.",
            ["Dogs have four legs.", "Some dogs are brown.",
             "A puppy is a young dog."],
            "'I think… the best…' — that's an opinion (what you think). "
            "The rest are facts."),
        mcq("Which linking words connect an opinion to its reasons?",
            "because, and, also", ["once, upon, time",
            "who, what, where", "a, an, the"],
            "'Dogs are the best BECAUSE they are loyal. ALSO, they love "
            "to play.'"),
        mcq("How should an opinion piece END?",
            "with a concluding statement, like 'That is why…'",
            ["with a brand-new topic", "mid-sentence",
             "with a spelling list"],
            "Wrap it up: 'That is why dogs are the best pets.'"),
        mcq("An INFORMATIVE (teaching) piece develops its topic using "
            "____.",
            "facts and definitions", ["opinions and feelings",
            "rhymes and songs", "made-up characters"],
            "Informative writing teaches with facts (can be proven) and "
            "definitions (what words mean)."),
        mcq("Which sentence belongs in an INFORMATIVE piece about "
            "spiders?",
            "A spider has eight legs.", ["Spiders are the creepiest.",
            "I hate spiders.", "Once upon a time, a spider talked."],
            "Informative = facts, not opinions or make-believe."),
        mcq("A NARRATIVE is writing that ____.",
            "tells about events in the order they happened",
            ["lists facts about a topic",
             "argues for an opinion", "defines hard words"],
            "A narrative recounts an event or sequence of events, with "
            "details and a closing."),
        mcq("Which words are TEMPORAL (time-order) words for a "
            "narrative?",
            "first, next, then, finally", ["because, also, and",
            "big, bigger, biggest", "who, which, what"],
            "Temporal words signal event order: 'FIRST we packed. NEXT "
            "we drove. FINALLY we arrived.'"),
        mcq("A good narrative includes details about the writer's "
            "actions, thoughts, and ____.",
            "feelings", ["spelling", "grades", "margins"],
            "Actions + thoughts + feelings make the story real for the "
            "reader."),
        mcq("What does it mean to give a narrative 'a sense of "
            "closure'?",
            "an ending that wraps the story up",
            ["a list of new questions", "a cliffhanger",
             "a title page"],
            "Close the story: how it turned out, how you felt, or a "
            "final thought."),
        mcq("Your teacher says: 'Write about your trip to the beach and "
            "what happened.' Which kind of writing is this?",
            "narrative", ["opinion", "informative", "poetry"],
            "Telling what happened, in order = narrative."),
        mcq("Your teacher says: 'Write what you THINK is the best season "
            "and why.' Which kind of writing is this?",
            "opinion", ["narrative", "informative", "biography"],
            "What you think + why = opinion writing."),
        mcq("Your teacher says: 'Teach the reader facts about "
            "butterflies.' Which kind of writing is this?",
            "informative", ["opinion", "narrative", "fable"],
            "Teaching facts = informative/explanatory writing."),
        mcq("REVISING your writing means ____; EDITING means ____.",
            "making it better with details and word changes; fixing "
            "capitals, spelling, and punctuation",
            ["fixing spelling; adding details",
             "reading it aloud; throwing it away",
             "writing a title; drawing a cover"],
            "Revise = improve the ideas and words. Edit = fix the "
            "mistakes (capitals, punctuation, spelling)."),
        tf("The sentence 'I think summer is the best season' could start "
           "an opinion piece.",
           True, "'I think' plus 'the best' states an opinion the piece "
           "can back up with reasons."),
        short("Which word — 'because', 'the', or 'under' — links an "
              "opinion to a reason?",
              "because", "'I like winter BECAUSE I love snow' — because "
              "glues opinion to reason."),
    ]
    kb = (
        "# Grade 2 ELA — Writing\n\n"
        "**Standards: W.2.1 (opinion), W.2.2 (informative), W.2.3 "
        "(narrative), W.2.5 (revise & edit).**\n\n"
        "## The three kinds of writing\n"
        "**Opinion (W.2.1)** — what you think, and why:\n"
        "1. Introduce the topic → 2. State your opinion ('I think…') → "
        "3. Give reasons → 4. Link them with **because, and, also** → "
        "5. Concluding statement ('That is why…').\n\n"
        "**Informative (W.2.2)** — teach the reader:\n"
        "1. Introduce the topic → 2. Develop it with **facts and "
        "definitions** → 3. Concluding statement. No opinions — just "
        "what can be proven.\n\n"
        "**Narrative (W.2.3)** — tell what happened:\n"
        "1. Recount the events **in order** → 2. Add details about "
        "**actions, thoughts, and feelings** → 3. Use **temporal words** "
        "(first, next, then, later, finally) → 4. End with **closure** "
        "(wrap it up).\n\n"
        "## Which kind does the prompt want?\n"
        "- 'What do you THINK…?' → opinion\n"
        "- 'TEACH the reader about…' → informative\n"
        "- 'Tell about a time when…' → narrative\n\n"
        "## Making it better (W.2.5)\n"
        "- **Revising** = improving the writing: add details, reorder, "
        "choose stronger words.\n"
        "- **Editing** = fixing mistakes: capitals, punctuation, "
        "spelling." + SRC)
    return {"name": "Writing: Opinion, Informative & Narrative",
            "source": {"title": "Writing — knowledge base", "content": kb},
            "questions": qs}


def build():
    chapters = [
        ch_long_short(), ch_vowel_teams(), ch_bossy_r(),
        ch_tricky_spellings(), ch_syllables(), ch_prefixes_suffixes(),
        ch_endings(), ch_sight_homophones(), ch_stories(), ch_fables(),
        ch_poems_versions(), ch_info_features(), ch_info_skills(),
        ch_nouns_pronouns(), ch_verbs_sentences(), ch_mechanics(),
        ch_vocabulary(), ch_writing(),
    ]
    bank = {
        "subject": {
            "name": "Grade 2 Reading & Language Arts (Anne Arundel County)",
            "description": "Comprehensive second-grade English Language Arts, "
                           "aligned to the Maryland College and Career-Ready "
                           "Standards (the standards AACPS teaches to, via "
                           "the CKLA curriculum): phonics & word study, "
                           "reading comprehension (stories, fables, poems, "
                           "informational text), grammar & conventions, "
                           "vocabulary, and writing. Follow-on to the "
                           "grade-1 reading bank.",
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
