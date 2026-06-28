#!/usr/bin/env python3
"""Build a comprehensive Grade 1 English Language Arts (ELA / Reading) bank.

Aligned to the Maryland College and Career-Ready Standards for English Language
Arts, Grade 1 (MSDE framework, built on the Common Core ELA standards) — the
standards Anne Arundel County Public Schools (AACPS) teaches to. Strands:
Reading Foundational Skills (RF.1), Reading Literature (RL.1), Reading
Informational Text (RI.1), Language (L.1), and Writing (W.1).

This is the non-math half of a first-grade grade-acceleration ("skip grade 1")
review set. AACPS models its acceleration decision on the Iowa Acceleration
Scale, which keys on READING and MATH achievement (plus ability/aptitude and
developmental factors) — content subjects like science/social studies are not the
gatekeeping measure — so reading is the right non-math subject to drill.

Everything is TEXT-ONLY (no "look at the picture", no audio): rhyming, vowel
sounds, digraphs, sight words, grammar, and comprehension all work on the page.
Comprehension items carry their short passage INLINE in the prompt so the
question is self-contained. Each chapter carries a plain-language knowledge base
(for a 6-7 year old / a parent reading along) that also serves as source material
the app can quote when explaining a topic.

Run:  python scripts/build_ela_g1.py   ->  writes banks/ela-g1.json
"""
import json
import os
import random

random.seed(1)  # deterministic output so re-runs don't churn the bank

OUT = os.path.join(os.path.dirname(__file__), "..", "banks", "ela-g1.json")


# --- small builders (identical contract to build_math_g1.py) ----------------
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


# --- Chapter 1: Sentences & Print Concepts ----------------------------------
def ch_sentences():
    qs = [
        mcq("Which one is a complete sentence?",
            "The dog ran fast.", ["The big dog.", "Ran fast.", "Under the bed."],
            "A complete sentence tells a whole idea — who/what (the dog) and what "
            "happens (ran fast). The others are just pieces."),
        mcq("Every sentence should begin with a ____.",
            "capital letter", ["small letter", "number", "period"],
            "Sentences start with a capital (uppercase) letter."),
        mcq("A telling sentence (a statement) ends with a ____.",
            "period ( . )", ["question mark ( ? )", "comma ( , )", "capital letter"],
            "A statement tells something and ends with a period."),
        mcq("An asking sentence (a question) ends with a ____.",
            "question mark ( ? )", ["period ( . )", "comma ( , )", "exclamation mark"],
            "A question asks something and ends with a question mark."),
        mcq("Which sentence is a question?",
            "Where is my hat?", ["I lost my hat.", "I found my hat.", "My hat is red."],
            "It asks something and ends with '?', so it is a question."),
        mcq("Which mark ends a sentence that shows strong feeling, like 'Watch out'?",
            "exclamation mark ( ! )", ["period ( . )", "question mark ( ? )", "comma"],
            "An exclamation shows excitement or strong feeling and ends with '!'."),
        mcq("Which sentence is written correctly?",
            "We went to the park.", ["we went to the park.",
            "We went to the park", "we went to the park"],
            "It starts with a capital 'W' and ends with a period."),
        mcq("How many words are in this sentence: 'The cat is black.'?",
            "4", ["3", "5", "6"],
            "Words are groups of letters with spaces between them: The / cat / is / "
            "black = 4 words."),
        mcq("A command (telling someone to do something), like 'Sit down,' is also "
            "called a ____ sentence.",
            "telling", ["asking", "rhyming", "naming"],
            "A command tells someone to do something; it usually ends with a period."),
        tf("Sentences are read from left to right, and top to bottom on the page.",
           True, "We read English left-to-right and top-to-bottom."),
        tf("The first word of a sentence starts with a lowercase letter.",
           False, "The first word starts with a CAPITAL (uppercase) letter."),
        tf("'the sun is hot' is written correctly.",
           False, "It needs a capital 'T' at the start and a period at the end: "
           "'The sun is hot.'"),
        short("What punctuation mark belongs at the end of: 'Do you like dogs'?",
              "question mark", "It is an asking sentence, so it ends with a question "
              "mark ( ? )."),
        short("Fix the start of this sentence: 'my name is Sam.' What should the "
              "first letter be?", "M", "The first word of a sentence is capitalized: "
              "'My name is Sam.'"),
    ]
    kb = (
        "# Grade 1 ELA — Sentences & Print Concepts\n\n"
        "**Standards: RF.1.1, L.1.1j, L.1.2a-b.** First graders learn how a sentence "
        "looks and works.\n\n"
        "## Big ideas\n"
        "- A **sentence** tells a whole idea: who or what, and what happens "
        "('The dog ran.').\n"
        "- Every sentence **begins with a capital letter**.\n"
        "- A **telling sentence (statement)** ends with a **period** ( . ).\n"
        "- An **asking sentence (question)** ends with a **question mark** ( ? ).\n"
        "- A sentence with strong feeling ends with an **exclamation mark** ( ! ).\n"
        "- **Words** are letters grouped together with **spaces** between them.\n"
        "- We read **left to right** and **top to bottom**.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 English Language Arts Framework* — Reading: Foundational "
        "Skills (Print Concepts) and Language (Conventions).\n"
        "- Common Core State Standards for ELA, Grade 1 (RF.1.1, L.1.1-2).\n"
    )
    return {"name": "Sentences & Print Concepts",
            "source": {"title": "Sentences & print concepts — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 2: Phonological Awareness (rhyme, syllables, sounds) ------------
def ch_phonological():
    qs = []
    # Rhyming families: pick a target, the answer rhymes, distractors don't.
    rhyme_sets = [
        ("cat", "hat", ["dog", "sun", "cup"]),
        ("pig", "wig", ["pot", "man", "bed"]),
        ("sun", "fun", ["sit", "top", "leg"]),
        ("bed", "red", ["bug", "cap", "fox"]),
        ("hop", "top", ["hen", "rat", "lip"]),
        ("ring", "king", ["road", "milk", "fast"]),
        ("cake", "lake", ["card", "cone", "kite"]),
        ("light", "night", ["lamp", "long", "list"]),
    ]
    for word, ans, wrong in rhyme_sets:
        qs.append(mcq(f"Which word rhymes with '{word}'?", ans, wrong,
                      f"'{word}' and '{ans}' end with the same sound."))
    # Odd-one-out rhyme.
    qs.append(mcq("Which word does NOT rhyme with the others?",
                  "dog", ["bat", "cat", "hat"],
                  "bat, cat, and hat rhyme (-at). 'dog' does not."))
    # Syllable counting (claps / beats).
    syl = [("dog", 1), ("rabbit", 2), ("butterfly", 3), ("pencil", 2),
           ("cat", 1), ("banana", 3), ("table", 2), ("elephant", 3)]
    for word, n in syl:
        wrong = [str(x) for x in (1, 2, 3, 4) if x != n][:3]
        qs.append(mcq(f"How many syllables (beats) are in '{word}'? "
                      f"(Clap it out.)", str(n), wrong,
                      f"'{word}' has {n} beat{'s' if n != 1 else ''} when you clap it."))
    # First / beginning sound.
    qs.append(mcq("What sound does 'sun' begin with?", "/s/", ["/m/", "/t/", "/b/"],
                  "'sun' starts with the /s/ sound, the letter s."))
    qs.append(mcq("Which word begins with the same sound as 'ball'?",
                  "bat", ["dog", "cup", "fan"],
                  "'ball' and 'bat' both begin with /b/."))
    qs.append(mcq("What sound does 'map' END with?", "/p/", ["/m/", "/a/", "/t/"],
                  "The last sound in 'map' is /p/."))
    qs.append(mcq("What is the middle (vowel) sound in 'cat'?", "/a/",
                  ["/c/", "/t/", "/o/"],
                  "c-a-t: the middle sound is the short /a/."))
    # Blending sounds into a word.
    qs.append(mcq("Blend these sounds together: /d/ /o/ /g/. What word is it?",
                  "dog", ["dot", "got", "den"],
                  "/d/ + /o/ + /g/ blends into 'dog'."))
    qs.append(mcq("Blend these sounds: /s/ /i/ /t/. What word is it?",
                  "sit", ["set", "sat", "sip"],
                  "/s/ + /i/ + /t/ blends into 'sit'."))
    # Segmenting.
    qs.append(short("Say the three sounds in the word 'map' one at a time. "
                    "What is the FIRST sound?", "/m/",
                    "m-a-p: the first sound is /m/."))
    # Long vs short vowel by ear.
    qs.append(mcq("Which word has a SHORT vowel sound?", "cap",
                  ["cape", "cake", "rain"],
                  "'cap' has the short /a/. cape, cake, and rain have the long /A/."))
    qs.append(mcq("Which word has a LONG vowel sound (says its name)?", "bee",
                  ["bed", "bib", "bus"],
                  "'bee' has the long /E/ sound. The others have short vowels."))
    return {"name": "Phonological Awareness (Rhyme, Syllables, Sounds)",
            "source": {"title": "Phonological awareness — knowledge base",
                       "content": (
        "# Grade 1 ELA — Phonological Awareness\n\n"
        "**Standard: RF.1.2.** Hearing and playing with the sounds in spoken words "
        "— the listening skill underneath reading.\n\n"
        "## Big ideas\n"
        "- **Rhyming words** end with the same sound: cat / hat / bat.\n"
        "- **Syllables** are the beats in a word — clap them: dog = 1, rab-bit = 2, "
        "but-ter-fly = 3.\n"
        "- Words have a **beginning, middle, and ending sound**: 'cat' = /k/ /a/ /t/.\n"
        "- **Blending** joins sounds into a word: /d/ /o/ /g/ -> 'dog'.\n"
        "- **Segmenting** breaks a word into its sounds: 'map' -> /m/ /a/ /p/.\n"
        "- A **short vowel** makes its quick sound (cap, bed, pig, hot, cup); a "
        "**long vowel** says its own name (cape, bee, kite, boat, mule).\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Foundational Skills "
        "(Phonological Awareness).\n"
        "- Common Core State Standards for ELA, Grade 1 (RF.1.2).\n")},
            "questions": qs}


# --- Chapter 3: Phonics — Short Vowels & Consonants (CVC) --------------------
def ch_phonics_short():
    qs = []
    # Short-vowel identification.
    short_vowel = [
        ("cat", "a"), ("net", "e"), ("pig", "i"), ("dog", "o"), ("sun", "u"),
        ("map", "a"), ("bed", "e"), ("lip", "i"), ("pot", "o"), ("cup", "u"),
    ]
    for word, v in short_vowel:
        wrong = [x for x in "aeiou" if x != v][:3]
        qs.append(mcq(f"Which short vowel do you hear in '{word}'?", v, wrong,
                      f"'{word}' has the short '{v}' sound in the middle."))
    # Which word has a given short vowel.
    qs.append(mcq("Which word has the short 'a' sound?", "ham",
                  ["hen", "hot", "hut"],
                  "'ham' has short /a/. hen=/e/, hot=/o/, hut=/u/."))
    qs.append(mcq("Which word has the short 'o' sound?", "fox",
                  ["fan", "fin", "fun"],
                  "'fox' has short /o/."))
    qs.append(mcq("Which word has the short 'u' sound?", "bug",
                  ["bag", "big", "bog"],
                  "'bug' has short /u/."))
    # Beginning consonant.
    begin = [("tap", "t"), ("man", "m"), ("rug", "r"), ("jam", "j"),
             ("van", "v"), ("yes", "y"), ("zip", "z")]
    for word, c in begin:
        wrong = [x for x in "bdfk" if x != c][:3]
        qs.append(mcq(f"What letter makes the FIRST sound in '{word}'?", c, wrong,
                      f"'{word}' begins with the /{c}/ sound — the letter '{c}'."))
    # Ending consonant.
    qs.append(mcq("What letter makes the LAST sound in 'bus'?", "s",
                  ["b", "u", "t"], "'bus' ends with the /s/ sound — the letter 's'."))
    qs.append(mcq("What letter makes the LAST sound in 'red'?", "d",
                  ["r", "e", "t"], "'red' ends with /d/ — the letter 'd'."))
    # Change a sound -> new word.
    qs.append(mcq("Change the first sound of 'cat' to /h/. What new word do you get?",
                  "hat", ["bat", "cap", "hit"],
                  "Swap /k/ for /h/: c-at -> h-at = 'hat'."))
    qs.append(mcq("Change the last sound of 'pin' to /g/. What new word do you get?",
                  "pig", ["pit", "pan", "big"],
                  "Swap /n/ for /g/: pi-n -> pi-g = 'pig'."))
    qs.append(short("A CVC word has the pattern consonant-vowel-consonant. "
                    "Spell a CVC word that means a small furry pet that says 'meow'.",
                    "cat", "'cat' is c (consonant) - a (vowel) - t (consonant)."))
    return {"name": "Phonics — Short Vowels & Consonants (CVC)",
            "source": {"title": "Short vowels & consonants — knowledge base",
                       "content": (
        "# Grade 1 ELA — Phonics: Short Vowels & Consonants\n\n"
        "**Standard: RF.1.3 (a, b).** Matching letters to sounds to read and spell "
        "simple words.\n\n"
        "## Big ideas\n"
        "- The **five vowels** are a, e, i, o, u. Every other letter is a "
        "**consonant**.\n"
        "- A **CVC word** is consonant-vowel-consonant: c-a-t, d-o-g, s-u-n.\n"
        "- **Short vowel sounds:** a as in cat, e as in bed, i as in pig, o as in "
        "dog, u as in cup.\n"
        "- To read a word, say each letter sound and **blend** them: /s/ /u/ /n/ "
        "-> 'sun'.\n"
        "- **Changing one sound** makes a new word: cat -> hat -> hit -> hip.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Foundational Skills (Phonics).\n"
        "- Common Core State Standards for ELA, Grade 1 (RF.1.3).\n")},
            "questions": qs}


# --- Chapter 4: Phonics — Long Vowels, Silent e, Vowel Teams ----------------
def ch_phonics_long():
    qs = [
        mcq("The 'magic e' (silent e) at the end of a word makes the vowel say "
            "its ____.", "name (long sound)", ["short sound", "first letter",
            "nothing at all"],
            "A silent e makes the vowel long: cap -> cape, kit -> kite."),
        mcq("Add a silent 'e' to 'cap'. What new word do you get?", "cape",
            ["caps", "cup", "clap"],
            "cap (short a) + e -> cape (long a). The 'e' is silent."),
        mcq("Add a silent 'e' to 'kit'. What new word do you get?", "kite",
            ["kid", "kitt", "cut"],
            "kit (short i) + e -> kite (long i)."),
        mcq("Add a silent 'e' to 'hop'. What new word do you get?", "hope",
            ["hops", "hoop", "hip"],
            "hop (short o) + e -> hope (long o)."),
        mcq("Which word has a LONG 'a' sound?", "rain", ["ran", "rag", "ram"],
            "'rain' has long /A/ (the vowel team 'ai'). The others are short a."),
        mcq("Which word has a LONG 'e' sound?", "feet", ["fed", "fan", "fox"],
            "'feet' has long /E/ from the vowel team 'ee'."),
        mcq("Which word has a LONG 'o' sound?", "boat", ["bot", "bat", "bus"],
            "'boat' has long /O/ from the vowel team 'oa'."),
        mcq("The letters 'ai' in 'rain' and 'ay' in 'play' both make which sound?",
            "long a", ["long e", "short a", "long i"],
            "'ai' and 'ay' are vowel teams that say long /A/."),
        mcq("The letters 'ee' in 'tree' and 'ea' in 'leaf' both make which sound?",
            "long e", ["short e", "long a", "long o"],
            "'ee' and 'ea' are vowel teams that say long /E/."),
        mcq("Which word has a vowel team that says long 'o'?", "snow",
            ["sock", "sun", "stop"],
            "'ow' in 'snow' says long /O/ (like 'oa' in boat)."),
        mcq("Which word has the long 'i' sound?", "pie", ["pin", "pig", "pit"],
            "'pie' has long /I/. The 'ie' here says long i."),
        tf("In the word 'cake', you hear the letter e at the end.",
           False, "The 'e' in 'cake' is SILENT — you don't say it. It just makes "
           "the 'a' long."),
        tf("'bee' and 'tree' both have the long e sound.",
           True, "Both use the vowel team 'ee' for long /E/."),
        short("What is the word: long-a spelled with 'ai', meaning water that falls "
              "from clouds? (3 letters + the team)", "rain",
              "r-ai-n = 'rain', with the 'ai' vowel team for long a."),
        mcq("Sort this word by its vowel sound — is 'note' long or short?",
            "long o", ["short o", "long e", "short u"],
            "'note' has a silent e, so the 'o' is long: /O/."),
    ]
    kb = (
        "# Grade 1 ELA — Long Vowels, Silent e & Vowel Teams\n\n"
        "**Standard: RF.1.3 (c, e).** Reading words where the vowel says its **name** "
        "(its long sound).\n\n"
        "## Big ideas\n"
        "- A **long vowel** says its own name: a (cake), e (bee), i (kite), o (boat), "
        "u (mule).\n"
        "- **Silent e ('magic e')** at the end makes the vowel long and is not said: "
        "cap -> cape, kit -> kite, hop -> hope.\n"
        "- **Vowel teams** are two vowels working together for one long sound:\n"
        "  - long a: **ai** (rain), **ay** (play)\n"
        "  - long e: **ee** (tree), **ea** (leaf)\n"
        "  - long o: **oa** (boat), **ow** (snow)\n"
        "  - long i: **ie** (pie), **igh** (night)\n"
        "- 'When two vowels go walking, the first one does the talking' is a clue (it "
        "is not always true, but it helps).\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Foundational Skills (Phonics).\n"
        "- Common Core State Standards for ELA, Grade 1 (RF.1.3c, RF.1.3e).\n"
    )
    return {"name": "Phonics — Long Vowels, Silent e & Vowel Teams",
            "source": {"title": "Long vowels & vowel teams — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 5: Phonics — Digraphs & Blends ---------------------------------
def ch_phonics_digraphs():
    qs = [
        mcq("A DIGRAPH is two letters that make ONE new sound. Which word begins "
            "with the digraph 'sh'?", "ship", ["sip", "snip", "step"],
            "'sh' in 'ship' makes one sound: /sh/."),
        mcq("Which word begins with the 'ch' sound?", "chair",
            ["car", "cat", "clap"],
            "'ch' in 'chair' makes one sound: /ch/."),
        mcq("Which word begins with the 'th' sound?", "thumb",
            ["tub", "top", "trip"],
            "'th' in 'thumb' makes one sound: /th/."),
        mcq("Which word begins with the 'wh' sound?", "whale",
            ["wag", "win", "well"],
            "'wh' in 'whale' makes the /wh/ sound."),
        mcq("What sound does 'ck' make in 'duck'?", "/k/", ["/d/", "/s/", "/ch/"],
            "'ck' makes the /k/ sound, usually at the end of short words: duck, sock."),
        mcq("Which word ENDS with the 'sh' sound?", "fish", ["fit", "fin", "fox"],
            "'fish' ends with the digraph 'sh' = /sh/."),
        mcq("Which word ENDS with the 'ch' sound?", "lunch",
            ["luck", "lump", "list"],
            "'lunch' ends with 'ch' = /ch/."),
        mcq("A BLEND is two letters whose sounds you BOTH hear, quickly together. "
            "Which word begins with the blend 'st'?", "stop",
            ["sit", "top", "sun"],
            "'st' in 'stop' blends /s/ and /t/ — you hear both."),
        mcq("Which word begins with the blend 'bl'?", "blue",
            ["bug", "ball", "bun"],
            "'bl' in 'blue' blends /b/ and /l/ — you hear both sounds."),
        mcq("Which word begins with the blend 'tr'?", "tree",
            ["tea", "top", "ten"],
            "'tr' in 'tree' blends /t/ and /r/."),
        mcq("Which word begins with the blend 'fr'?", "frog",
            ["fog", "fan", "fin"],
            "'fr' in 'frog' blends /f/ and /r/."),
        mcq("What is the difference between a blend and a digraph?",
            "In a blend you hear both letter sounds; in a digraph two letters make "
            "one new sound",
            ["They are exactly the same", "A blend is always at the end",
             "A digraph has three letters"],
            "Blend = both sounds heard (st, bl, tr). Digraph = one new sound "
            "(sh, ch, th, wh)."),
        tf("'sh', 'ch', 'th', and 'wh' are digraphs (two letters, one sound).",
           True, "Yes — each pair makes a single new sound."),
        tf("In the blend 'st', you only hear the /t/ sound.",
           False, "In a blend you hear BOTH sounds: /s/ AND /t/."),
        short("Name the digraph (two letters) at the start of 'shell'.", "sh",
              "'shell' begins with the digraph 'sh' = /sh/."),
    ]
    kb = (
        "# Grade 1 ELA — Digraphs & Blends\n\n"
        "**Standard: RF.1.3 (b).** Two-letter teams at the start or end of words.\n\n"
        "## Big ideas\n"
        "- A **digraph** is two letters that make **one new sound**: **sh** (ship), "
        "**ch** (chair), **th** (thumb), **wh** (whale), **ck** (duck = /k/).\n"
        "- A **blend** is two letters next to each other where you hear **both** "
        "sounds quickly together: **bl** (blue), **st** (stop), **tr** (tree), "
        "**fr** (frog), **gr**, **sn**, **cl**, **pl**.\n"
        "- The big difference: **digraph = one sound**, **blend = two sounds you "
        "still hear**.\n"
        "- Digraphs can come at the **end** too: fish (sh), lunch (ch), bath (th).\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Foundational Skills (Phonics).\n"
        "- Common Core State Standards for ELA, Grade 1 (RF.1.3b).\n"
    )
    return {"name": "Phonics — Digraphs & Blends",
            "source": {"title": "Digraphs & blends — knowledge base",
                       "content": kb},
            "questions": qs}


# --- Chapter 6: Word Families, Endings, R-controlled & Syllables -------------
def ch_word_parts():
    qs = []
    # Word families (onset-rime).
    fam = [
        ("-at", "cat", ["cap", "can", "cab"]),
        ("-an", "pan", ["pat", "pad", "pal"]),
        ("-ig", "big", ["bit", "bib", "bin"]),
        ("-op", "mop", ["mob", "mom", "mod"]),
        ("-un", "run", ["rug", "rub", "rut"]),
    ]
    for rime, ans, wrong in fam:
        qs.append(mcq(f"Which word belongs to the '{rime}' word family?", ans, wrong,
                      f"The '{rime}' family all end the same way; '{ans}' fits."))
    # Inflectional endings -s, -ing, -ed.
    qs.append(mcq("To make 'cat' mean more than one, add which ending?", "-s",
                  ["-ing", "-ed", "-er"], "cat + s = cats (more than one)."))
    qs.append(mcq("'The dog is jumping.' Which ending was added to 'jump'?", "-ing",
                  ["-ed", "-s", "-ly"], "jump + ing = jumping (happening now)."))
    qs.append(mcq("'Yesterday I jumped.' Which ending shows it ALREADY happened?",
                  "-ed", ["-ing", "-s", "-er"],
                  "jump + ed = jumped (it happened in the past)."))
    qs.append(mcq("Add -ing to 'play'. What is the new word?", "playing",
                  ["plaing", "plays", "played"],
                  "play + ing = playing."))
    qs.append(mcq("Add -ed to 'walk'. What is the new word?", "walked",
                  ["walking", "walks", "walkd"],
                  "walk + ed = walked (past tense)."))
    # R-controlled vowels.
    qs.append(mcq("In 'car', the letters 'ar' make which sound?", "/ar/ (like in 'far')",
                  ["short a", "long a", "/or/"],
                  "'r' changes the vowel: 'ar' says /ar/ as in car, star, far."))
    qs.append(mcq("Which word has the 'or' sound, like in 'corn'?", "fork",
                  ["fan", "far", "fun"],
                  "'or' in 'fork' says /or/, the same as in corn and storm."))
    qs.append(mcq("'her', 'bird', and 'fur' all have which sound?", "/er/",
                  ["long e", "short i", "/ar/"],
                  "er, ir, and ur all make the same /er/ sound."))
    # Syllable splitting / compound words.
    qs.append(mcq("How many syllables are in 'sunset'? (sun-set)", "2",
                  ["1", "3", "4"], "sun-set has 2 beats; it is a compound word."))
    qs.append(mcq("A COMPOUND word is two small words joined. Which is a compound "
                  "word?", "rainbow", ["rabbit", "happy", "yellow"],
                  "rain + bow = rainbow. Two words make one."))
    qs.append(mcq("What two words make the compound word 'cupcake'?",
                  "cup + cake", ["cu + pcake", "cup + ake", "c + upcake"],
                  "cupcake = cup + cake."))
    qs.append(short("Make a compound word: 'fire' + 'fighter' = ?", "firefighter",
                    "fire + fighter = firefighter."))
    qs.append(tf("Adding '-s' to 'book' makes 'books', which means more than one.",
                 True, "The -s ending makes a plural: one book, two books."))
    return {"name": "Word Families, Endings, R-Controlled & Syllables",
            "source": {"title": "Word parts & endings — knowledge base",
                       "content": (
        "# Grade 1 ELA — Word Families, Endings & Syllables\n\n"
        "**Standards: RF.1.3 (d, e, f, g), L.1.4c.** Building and breaking words by "
        "their parts.\n\n"
        "## Big ideas\n"
        "- A **word family** shares an ending chunk: -at (cat, hat, sat), -ig "
        "(pig, wig, dig). Change the first sound to make a new word.\n"
        "- **Endings (inflections)** change a word's job:\n"
        "  - **-s** makes more than one: cat -> cats.\n"
        "  - **-ing** means happening now: jump -> jumping.\n"
        "  - **-ed** means it already happened: jump -> jumped.\n"
        "- **R-controlled vowels:** the 'r' bends the vowel — **ar** (car), **or** "
        "(corn), and **er/ir/ur** all say /er/ (her, bird, fur).\n"
        "- **Syllables** are word beats; **compound words** are two small words "
        "joined: sun+set=sunset, cup+cake=cupcake, rain+bow=rainbow.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Foundational Skills (Phonics, "
        "Word Recognition).\n"
        "- Common Core State Standards for ELA, Grade 1 (RF.1.3d-g, L.1.4c).\n")},
            "questions": qs}


# --- Chapter 7: Sight Words / High-Frequency Words --------------------------
def ch_sight_words():
    qs = []
    # Recognition / meaning-in-context for common Dolch grade-1 words.
    qs += [
        mcq("Fill the blank: 'I ____ to the store.' (a word that means 'go in the "
            "past')", "went", ["want", "with", "when"],
            "'went' is the past of 'go': I went to the store."),
        mcq("Which word completes: 'This is ____ book, not yours.'?", "my",
            ["me", "may", "many"],
            "'my' shows it belongs to me."),
        mcq("Which word completes: 'They ____ happy.' (right now)?", "are",
            ["am", "is", "was"],
            "Use 'are' with 'they': They are happy."),
        mcq("Which word completes: 'She has ____ apples than me.' (a bigger number)?",
            "more", ["most", "mine", "many"],
            "'more' compares two amounts: she has more than me."),
        mcq("Which word completes: 'Please ____ down.'?", "sit",
            ["set", "saw", "say"],
            "'sit' means to take a seat."),
        mcq("Which word means the opposite of 'come'?", "go", ["good", "get", "give"],
            "'go' is the opposite of 'come'."),
        mcq("Which word completes: '____ you like to play?' (an asking word)?", "Do",
            ["Doe", "Down", "Day"],
            "'Do' starts an asking sentence: Do you like to play?"),
        mcq("Which spelling of the 'reason' word is correct? (as in 'I stayed home "
            "____ I was sick')", "because", ["becuz", "becos", "becuse"],
            "'because' is a tricky sight word — learn it by sight."),
        mcq("Which spelling is correct for a person you like to play with?",
            "friend", ["frend", "freind", "frind"],
            "'friend' is spelled f-r-i-e-n-d (a sight word to memorize)."),
        mcq("Which spelling is correct for the past of 'say' (as in 'she ____ "
            "hello')?", "said", ["sed", "sayd", "saed"],
            "'said' is a sight word — it does not sound the way it is spelled."),
        mcq("Which spelling is correct for the word meaning more than one person "
            "('___ are here')?", "they", ["thay", "thei", "dey"],
            "'they' is spelled t-h-e-y."),
        mcq("Which spelling is correct for the asking word about a place?",
            "where", ["wher", "were", "whair"],
            "'where' asks about a place: Where is it?"),
    ]
    # Quick yes/no and short for super-common words.
    qs += [
        tf("'the', 'and', 'is', 'you', and 'was' are all sight words we should know "
           "by heart.", True,
           "Sight words appear so often that we learn them instantly, without "
           "sounding them out."),
        tf("Sight words should always be sounded out slowly, letter by letter.",
           False, "Many sight words don't follow the rules (said, was, of), so we "
           "learn them by sight instead."),
        short("Spell the word that means the opposite of 'no' (a sight word).",
              "yes", "'yes' is a common sight word, the opposite of 'no'."),
        short("Fill the blank with a sight word: 'I ____ a dog.' (showing you own "
              "one, right now)", "have",
              "'have' shows you own something: I have a dog."),
    ]
    return {"name": "Sight Words & High-Frequency Words",
            "source": {"title": "Sight words — knowledge base", "content": (
        "# Grade 1 ELA — Sight Words (High-Frequency Words)\n\n"
        "**Standard: RF.1.3g.** Reading common words quickly and correctly.\n\n"
        "## Big ideas\n"
        "- **Sight words** are words we see so often that we should know them "
        "**instantly**, without sounding them out.\n"
        "- Many of them **break the phonics rules** (the, was, said, of, you, "
        "they, are, have, where, because, friend), so we **memorize** them.\n"
        "- Knowing sight words makes reading **faster and smoother** (more fluent), "
        "so the reader can think about the meaning.\n"
        "- First-grade lists (Dolch / Fry) include: a, and, the, to, is, in, it, "
        "you, that, was, for, on, are, as, with, his, they, at, be, this, have, "
        "from, said, what, were, when, your, can, there, more, go, my, do, no, "
        "yes, said, because, friend.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Foundational Skills (Word "
        "Recognition).\n"
        "- Dolch and Fry high-frequency word lists (Grade 1).\n")},
            "questions": qs}


# --- Chapter 8: Reading Comprehension — Stories (Literature) ----------------
def ch_comprehension_lit():
    # Each item carries its short passage INLINE so it is self-contained.
    p1 = ("Read the story:\n\n"
          "\"Mia had a red kite. One windy day she ran to the park. She let the "
          "kite go up, up, up into the sky. The kite flew high above the trees. "
          "Mia laughed and held on tight.\"\n\n")
    p2 = ("Read the story:\n\n"
          "\"Sam could not find his shoe. He looked under the bed. He looked in "
          "the closet. At last he found it in the dog's basket! The puppy had "
          "taken it to chew. Sam laughed and gave the puppy a toy instead.\"\n\n")
    p3 = ("Read the story:\n\n"
          "\"It was raining, so Ana could not play outside. She felt sad. Then "
          "Dad got out the paints. They painted a big picture together. Soon Ana "
          "was smiling. Rainy days can be fun too!\"\n\n")
    qs = [
        # Passage 1
        mcq(p1 + "Who is the story mostly about?", "Mia",
            ["Dad", "a puppy", "Sam"],
            "The story follows Mia and her kite, so Mia is the main character."),
        mcq(p1 + "What color was the kite?", "red", ["blue", "green", "yellow"],
            "The story says 'a red kite'."),
        mcq(p1 + "Where did Mia run?", "to the park",
            ["to school", "to the store", "to the beach"],
            "'she ran to the park.'"),
        mcq(p1 + "Why could the kite fly so well that day?", "It was windy",
            ["It was sunny", "It was raining", "It was snowing"],
            "It says 'One windy day' — wind helps a kite fly."),
        mcq(p1 + "How did Mia feel at the end?", "happy",
            ["angry", "scared", "tired"],
            "'Mia laughed' — laughing shows she felt happy."),
        # Passage 2
        mcq(p2 + "What was Sam looking for?", "his shoe",
            ["his dog", "his toy", "his hat"],
            "'Sam could not find his shoe.'"),
        mcq(p2 + "Where did Sam finally find it?", "in the dog's basket",
            ["under the bed", "in the closet", "in the park"],
            "'At last he found it in the dog's basket!'"),
        mcq(p2 + "Who took the shoe?", "the puppy",
            ["Sam", "Dad", "Mia"],
            "'The puppy had taken it to chew.'"),
        mcq(p2 + "Put these in order. What did Sam do FIRST?",
            "looked under the bed", ["looked in the closet",
            "found the shoe", "gave the puppy a toy"],
            "He looked under the bed first, then the closet, then found it."),
        mcq(p2 + "What lesson does the puppy's part teach?",
            "Pets sometimes take things to chew",
            ["Shoes are bad", "Sam is mean", "Beds are messy"],
            "The puppy chewed the shoe — that's why it was missing."),
        # Passage 3
        mcq(p3 + "Why couldn't Ana play outside?", "It was raining",
            ["It was night", "She was sick", "She was busy"],
            "'It was raining, so Ana could not play outside.'"),
        mcq(p3 + "How did Ana feel at the BEGINNING?", "sad",
            ["happy", "angry", "sleepy"],
            "'She felt sad.'"),
        mcq(p3 + "What did Ana and Dad do together?", "painted a picture",
            ["watched TV", "baked a cake", "read a book"],
            "'They painted a big picture together.'"),
        mcq(p3 + "How did Ana's feelings change by the end?",
            "from sad to happy", ["from happy to sad", "she stayed sad",
            "from scared to brave"],
            "She was sad, then 'Ana was smiling' — sad changed to happy."),
        mcq(p3 + "What is the lesson (message) of this story?",
            "You can have fun even on a rainy day",
            ["Rain is dangerous", "Never paint", "Dads don't help"],
            "The last line says 'Rainy days can be fun too!'"),
        # General story-structure concepts (no passage needed)
        mcq("In a story, WHERE and WHEN it happens is called the ____.",
            "setting", ["character", "problem", "title"],
            "The setting is where and when a story takes place."),
        mcq("The people or animals a story is about are the ____.",
            "characters", ["setting", "ending", "title"],
            "Characters are who the story is about."),
        tf("A story usually has a beginning, a middle, and an end.",
           True, "Stories are told in order: beginning, middle, end."),
        short("What do we call the lesson or big idea a story teaches you?",
              "the message", "The lesson of a story is called its message (or "
              "moral / central message)."),
    ]
    return {"name": "Reading Comprehension — Stories",
            "source": {"title": "Reading stories — knowledge base", "content": (
        "# Grade 1 ELA — Reading Comprehension: Stories\n\n"
        "**Standards: RL.1.1, RL.1.2, RL.1.3, RL.1.7.** Understanding a story you "
        "read.\n\n"
        "## Big ideas\n"
        "- **Ask and answer questions** about the story: **who, what, where, when, "
        "why, how**.\n"
        "- **Characters** are who the story is about; the **setting** is where and "
        "when it happens.\n"
        "- A story has a **beginning, middle, and end** — events happen in **order**.\n"
        "- **Retell** the key details in your own words.\n"
        "- Many stories teach a **lesson or message** (the big idea).\n"
        "- Notice how characters **feel** and how their feelings **change**.\n\n"
        "## How to read a comprehension question\n"
        "Read the little story first. Then find the part that answers the question. "
        "The answer is usually right there in the words ('text evidence').\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Literature.\n"
        "- Common Core State Standards for ELA, Grade 1 (RL.1).\n")},
            "questions": qs}


# --- Chapter 9: Reading Comprehension — Informational Text ------------------
def ch_comprehension_info():
    p1 = ("Read about frogs:\n\n"
          "\"Frogs are animals that live near water. A baby frog is called a "
          "tadpole. Tadpoles live in the water and have tails. As they grow, they "
          "get legs and lose their tails. Then they can hop on land. Frogs eat "
          "bugs.\"\n\n")
    p2 = ("Read about the sun:\n\n"
          "\"The sun is a giant star. It gives us light and heat. We see the sun "
          "in the daytime. The sun helps plants grow. Without the sun, Earth would "
          "be cold and dark.\"\n\n")
    qs = [
        mcq(p1 + "What is this text mostly about?", "frogs",
            ["water", "bugs", "tails"],
            "Every sentence tells about frogs — that is the main topic."),
        mcq(p1 + "What is a baby frog called?", "a tadpole",
            ["a puppy", "a chick", "a calf"],
            "'A baby frog is called a tadpole.'"),
        mcq(p1 + "What happens to a tadpole's tail as it grows?",
            "it loses the tail", ["it grows longer", "it turns red",
            "nothing changes"],
            "'they get legs and lose their tails.'"),
        mcq(p1 + "What do frogs eat?", "bugs", ["grass", "fish", "leaves"],
            "'Frogs eat bugs.'"),
        mcq(p1 + "Where do tadpoles live?", "in the water",
            ["in a nest", "in the sky", "under a rock"],
            "'Tadpoles live in the water.'"),
        mcq(p2 + "What is the main topic of this text?", "the sun",
            ["the moon", "plants", "the night"],
            "The whole text is about the sun."),
        mcq(p2 + "The sun is a giant ____.", "star", ["planet", "cloud", "rock"],
            "'The sun is a giant star.'"),
        mcq(p2 + "Two things the sun gives us are ____.", "light and heat",
            ["rain and snow", "wind and sound", "food and water"],
            "'It gives us light and heat.'"),
        mcq(p2 + "When do we see the sun?", "in the daytime",
            ["at night", "only in winter", "never"],
            "'We see the sun in the daytime.'"),
        mcq(p2 + "How does the sun help plants?", "it helps them grow",
            ["it waters them", "it cuts them", "it eats them"],
            "'The sun helps plants grow.'"),
        # Text features
        mcq("Where would you look at the FRONT of a nonfiction book to find what "
            "is inside and which page to turn to?", "the table of contents",
            ["the glossary", "the back cover", "the title"],
            "The table of contents lists the parts and page numbers."),
        mcq("A list at the BACK of a book that tells you what hard words mean is "
            "called a ____.", "glossary", ["title", "heading", "index"],
            "A glossary is like a little dictionary for the book."),
        mcq("The big words above a part of the text that tell you what that part is "
            "about are called ____.", "headings", ["captions", "labels", "footers"],
            "Headings tell you the topic of each section."),
        mcq("Words under a picture that tell you about it are called a ____.",
            "caption", ["heading", "glossary", "title"],
            "A caption explains a picture or photo."),
        tf("Nonfiction (informational) text gives us true facts and information.",
           True, "Informational text teaches real facts, unlike a made-up story."),
        tf("A story about a talking dragon who grants wishes is nonfiction.",
           False, "That is fiction (made up). Nonfiction tells true facts."),
        mcq("Which would be NONFICTION (informational)?",
            "A book about how bees make honey",
            ["A fairy tale about a princess", "A poem about a silly cat",
             "A story about a flying car"],
            "A book of real facts about bees is informational (nonfiction)."),
        short("What do we call the most important idea a nonfiction text is about?",
              "the main topic", "The main topic (main idea) is what the whole text "
              "is mostly about."),
    ]
    return {"name": "Reading Comprehension — Informational Text",
            "source": {"title": "Informational text — knowledge base", "content": (
        "# Grade 1 ELA — Reading Comprehension: Informational Text\n\n"
        "**Standards: RI.1.1, RI.1.2, RI.1.5, RI.1.6, RI.1.7.** Understanding "
        "true-fact (nonfiction) text.\n\n"
        "## Big ideas\n"
        "- **Informational (nonfiction)** text gives **true facts**, not a made-up "
        "story.\n"
        "- Find the **main topic** (what it is mostly about) and the **key details** "
        "(important facts that tell about the topic).\n"
        "- Ask and answer **who/what/where/when/why/how** about the facts.\n"
        "- **Text features** help you find information:\n"
        "  - **Table of contents** (front) — lists parts and page numbers.\n"
        "  - **Headings** — tell the topic of each section.\n"
        "  - **Glossary** (back) — meanings of hard words.\n"
        "  - **Captions / labels** — explain pictures and diagrams.\n"
        "- **Fiction vs nonfiction:** fiction is made up (fairy tales, talking "
        "animals); nonfiction is real and true.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Reading: Informational Text.\n"
        "- Common Core State Standards for ELA, Grade 1 (RI.1).\n")},
            "questions": qs}


# --- Chapter 10: Grammar — Nouns --------------------------------------------
def ch_nouns():
    qs = [
        mcq("A NOUN is a word for a person, place, animal, or thing. Which word is "
            "a noun?", "dog", ["run", "happy", "quickly"],
            "'dog' names an animal, so it is a noun. run is an action; happy "
            "describes."),
        mcq("Which word is a noun (a thing)?", "table", ["jump", "blue", "fast"],
            "'table' names a thing."),
        mcq("Which word names a PLACE?", "school", ["sing", "soft", "she"],
            "'school' is a place, so it is a noun."),
        mcq("A PROPER noun names a SPECIAL person, place, or thing and starts with "
            "a capital letter. Which is a proper noun?", "Maryland",
            ["state", "city", "country"],
            "'Maryland' is the special name of a place, so it is capitalized."),
        mcq("Which is a proper noun?", "Sarah", ["girl", "kid", "she"],
            "'Sarah' is a special person's name — proper nouns are capitalized."),
        mcq("Which is a COMMON noun (a regular, not-special name)?", "city",
            ["Baltimore", "Tuesday", "Max"],
            "'city' is a common noun; Baltimore is a special (proper) name."),
        mcq("To make most nouns mean MORE THAN ONE (plural), you add ____.", "-s",
            ["-ing", "-ed", "-ly"], "one cat -> two cats: add -s for plural."),
        mcq("What is the plural of 'box'?", "boxes", ["boxs", "box", "boxies"],
            "Words ending in x add -es: box -> boxes (also s, ss, sh, ch)."),
        mcq("What is the plural of 'baby'?", "babies", ["babys", "babyes", "baby"],
            "A word ending in a consonant + y: change y to i and add -es: "
            "baby -> babies."),
        mcq("Some plurals are special. What is the plural of 'child'?", "children",
            ["childs", "childes", "childrens"],
            "'child' has an irregular plural: children (not childs)."),
        mcq("What is the plural of 'mouse'?", "mice", ["mouses", "mices", "mouse"],
            "'mouse' -> 'mice' is an irregular plural."),
        mcq("What is the plural of 'foot'?", "feet", ["foots", "feets", "footes"],
            "'foot' -> 'feet' is irregular."),
        mcq("To show something belongs to Sam, we write 'Sam___ hat'. What goes in "
            "the blank?", "'s (apostrophe s)", ["s only", "es", "z"],
            "Add apostrophe + s to show belonging: Sam's hat."),
        tf("'happiness', 'love', and 'fun' can be nouns even though you can't touch "
           "them.", True,
           "Nouns can be ideas/feelings too, not just things you can touch."),
        tf("Proper nouns like names of people and places start with a capital "
           "letter.", True, "Yes — Sarah, Maryland, Monday all start with capitals."),
        short("Write the plural of 'dog' (more than one).", "dogs",
              "Add -s: dog -> dogs."),
        short("Is the word 'Monday' a common noun or a proper noun?",
              "proper noun", "Days of the week are special names, so they are "
              "proper nouns and are capitalized."),
    ]
    return {"name": "Grammar — Nouns (Common, Proper, Plural)",
            "source": {"title": "Nouns — knowledge base", "content": (
        "# Grade 1 ELA — Nouns\n\n"
        "**Standards: L.1.1b, L.1.1c.** Naming words.\n\n"
        "## Big ideas\n"
        "- A **noun** names a **person, place, animal, thing, or idea**: girl, "
        "park, dog, table, love.\n"
        "- A **common noun** is a regular name: dog, city, day.\n"
        "- A **proper noun** is a special name and is **capitalized**: Max, "
        "Baltimore, Monday, Maryland.\n"
        "- **Plural** means more than one. Add **-s** (cat -> cats), or **-es** "
        "after s, x, ss, sh, ch (box -> boxes). Change **y to i + es** after a "
        "consonant (baby -> babies).\n"
        "- Some plurals are **irregular** (you just learn them): child -> children, "
        "mouse -> mice, foot -> feet, man -> men, tooth -> teeth.\n"
        "- Show **belonging** with **'s**: Sam's hat, the dog's bone.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Language (Conventions).\n"
        "- Common Core State Standards for ELA, Grade 1 (L.1.1b-c).\n")},
            "questions": qs}


# --- Chapter 11: Grammar — Verbs, Adjectives, Pronouns & Connectors ---------
def ch_verbs_adj():
    qs = [
        mcq("A VERB is an action word. Which word is a verb?", "jump",
            ["chair", "green", "slowly"],
            "'jump' is an action you can do, so it is a verb."),
        mcq("Which word is a verb (an action)?", "swim", ["water", "wet", "fish"],
            "'swim' is an action."),
        mcq("Find the verb: 'The bird sings a song.'", "sings",
            ["bird", "song", "the"],
            "'sings' is the action the bird does."),
        mcq("Which sentence is about the PAST (already happened)?",
            "She walked to school.", ["She walks to school.",
            "She will walk to school.", "She is walking to school."],
            "'walked' (with -ed) shows it already happened."),
        mcq("Which sentence is about the FUTURE (will happen later)?",
            "I will eat lunch.", ["I ate lunch.", "I eat lunch.",
            "I am eating lunch."],
            "'will' shows the future — it has not happened yet."),
        mcq("Choose the right verb: 'He ____ a book every night.'", "reads",
            ["read", "reading", "readed"],
            "With 'he', use 'reads' for something he does each night."),
        mcq("An ADJECTIVE describes a noun (tells more about it). Which word is an "
            "adjective?", "soft", ["pillow", "sleep", "run"],
            "'soft' tells what something is like, so it describes — an adjective."),
        mcq("Find the adjective: 'The tall man waved.'", "tall",
            ["man", "waved", "the"],
            "'tall' describes the man, so it is an adjective."),
        mcq("Which adjective tells about color?", "yellow",
            ["loud", "round", "tiny"],
            "'yellow' is a color word describing a noun."),
        mcq("A PRONOUN takes the place of a noun. In 'Sara is nice. ___ is my "
            "friend,' which pronoun fits?", "She", ["He", "It", "They"],
            "'She' replaces 'Sara' (a girl)."),
        mcq("Which pronoun replaces 'the dog'?", "it", ["he", "she", "they"],
            "An animal or thing can be 'it': The dog ran. It ran."),
        mcq("Which pronoun replaces 'Tom and I'?", "we", ["he", "she", "it"],
            "'Tom and I' = 'we' (the group that includes me)."),
        mcq("A word that JOINS two ideas, like 'and', 'but', or 'so', is called a "
            "____.", "conjunction (joining word)", ["noun", "verb", "adjective"],
            "Joining words (and, but, or, so, because) connect ideas."),
        mcq("Choose the joining word that fits: 'I was tired, ____ I went to "
            "bed.'", "so", ["but", "or", "because"],
            "'so' shows the result: I was tired, SO I went to bed. 'but' and 'or' "
            "don't fit, and 'because' would reverse the reason."),
        mcq("A word that tells WHERE something is, like 'in', 'on', 'under', is a "
            "____.", "preposition (position word)", ["verb", "adjective", "pronoun"],
            "Position words (in, on, under, over, by) tell where."),
        mcq("Fill in the position word: 'The cat is ____ the box.' (it is inside)",
            "in", ["run", "happy", "blue"],
            "'in' tells where — the cat is inside the box."),
        tf("In 'The red ball bounced,' the word 'red' is an adjective.",
           True, "'red' describes the ball (its color)."),
        tf("'run', 'jump', and 'eat' are all naming words (nouns).",
           False, "They are ACTION words — verbs, not nouns."),
        short("What part of speech is the word 'happy' (it describes how someone "
              "feels)?", "adjective", "'happy' describes a noun, so it is an "
              "adjective."),
        short("Change 'play' to show it ALREADY happened (past tense).", "played",
              "Add -ed for the past: play -> played."),
    ]
    return {"name": "Grammar — Verbs, Adjectives, Pronouns & Connectors",
            "source": {"title": "Verbs, adjectives & pronouns — knowledge base",
                       "content": (
        "# Grade 1 ELA — Verbs, Adjectives, Pronouns & Connectors\n\n"
        "**Standards: L.1.1e, L.1.1f, L.1.1d, L.1.1g, L.1.1h, L.1.1i.** The other "
        "parts of speech.\n\n"
        "## Big ideas\n"
        "- A **verb** is an **action** word: run, jump, sing, eat. It tells what "
        "someone does.\n"
        "- **Verb tense** tells WHEN: **past** (walked), **now/present** (walks), "
        "**future** (will walk).\n"
        "- An **adjective** **describes** a noun — its size, color, shape, or "
        "feeling: big, red, round, happy.\n"
        "- A **pronoun** takes the place of a noun: **he, she, it, we, they, I, "
        "you**. (Sara -> she; the dog -> it; Tom and I -> we.)\n"
        "- **Conjunctions** join ideas: **and, but, or, so, because**.\n"
        "- **Prepositions** tell **where/when**: in, on, under, over, by, after.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Language (Conventions).\n"
        "- Common Core State Standards for ELA, Grade 1 (L.1.1d-i).\n")},
            "questions": qs}


# --- Chapter 12: Capitalization, Punctuation & Spelling Rules ---------------
def ch_caps_punct():
    qs = [
        mcq("Which word should ALWAYS be capitalized, no matter where it is in a "
            "sentence?", "names of people (like Emma)",
            ["happy words", "long words", "action words"],
            "Names of people are proper nouns and are always capitalized."),
        mcq("Which is written correctly?", "We play on Monday.",
            ["We play on monday.", "we play on Monday.", "We Play On Monday."],
            "Capitalize the first word AND the day name 'Monday'."),
        mcq("The word 'I' (meaning yourself) should be written as a ____.",
            "capital I", ["small i", "number 1", "letter e"],
            "The word 'I' is always a capital letter."),
        mcq("Which holiday/month is capitalized correctly?", "July",
            ["july", "JULY?", "Jully"],
            "Months are proper nouns: capitalize the first letter — July."),
        mcq("A comma ( , ) goes between the day and year in a date. Which is "
            "correct?", "May 5, 2026", ["May 5 2026", "May, 5 2026",
            "May 5. 2026"],
            "Put a comma between the day and the year: May 5, 2026."),
        mcq("Which list uses commas correctly?",
            "I like apples, grapes, and pears.",
            ["I like apples grapes and pears.", "I like apples, grapes and, pears.",
             "I like, apples grapes pears."],
            "Use a comma between items in a list (a series)."),
        mcq("A CONTRACTION joins two words with an apostrophe. 'do not' becomes "
            "____.", "don't", ["dont", "donot", "do'nt"],
            "do + not = don't; the apostrophe takes the place of the missing 'o'."),
        mcq("What two words make the contraction 'I'm'?", "I am", ["I will",
            "I have", "I was"], "I + am = I'm."),
        mcq("What two words make the contraction 'can't'?", "can not",
            ["can it", "can to", "could not"],
            "can + not = can't."),
        mcq("Which is the correct contraction for 'it is'?", "it's",
            ["its", "its'", "it'is"],
            "it + is = it's (the apostrophe replaces the 'i' in is)."),
        mcq("Pick the correct sentence:", "My friend and I went to the zoo.",
            ["my friend and i went to the zoo.",
             "My friend and i went to the zoo.",
             "my friend and I went to the zoo."],
            "Capitalize the first word 'My' and always capitalize 'I'."),
        tf("Days of the week (Monday, Friday) start with a capital letter.",
           True, "Days are proper nouns, so they are capitalized."),
        tf("The word 'i' (meaning me) can be written with a small letter.",
           False, "The word 'I' is always capitalized."),
        short("Write the contraction for 'is not'.", "isn't",
              "is + not = isn't."),
        short("Add the missing punctuation mark to the end: 'Are you ready' — what "
              "mark belongs there?", "question mark",
              "It is a question, so it ends with a question mark ( ? )."),
    ]
    return {"name": "Capitalization, Punctuation & Contractions",
            "source": {"title": "Capitalization & punctuation — knowledge base",
                       "content": (
        "# Grade 1 ELA — Capitalization, Punctuation & Contractions\n\n"
        "**Standards: L.1.2a, L.1.2b, L.1.2c, L.1.2d.** Writing rules.\n\n"
        "## Big ideas\n"
        "- **Capitalize:** the **first word** of a sentence, the word **I**, "
        "**people's names**, **days**, **months**, and **place names**.\n"
        "- **End marks:** period ( . ) for telling, question mark ( ? ) for asking, "
        "exclamation mark ( ! ) for strong feeling.\n"
        "- **Commas:** between the **day and year** in a date (May 5, 2026) and "
        "between **items in a list** (apples, grapes, and pears).\n"
        "- **Contractions** squeeze two words into one with an **apostrophe** that "
        "stands for the missing letters: do not -> don't, I am -> I'm, can not -> "
        "can't, it is -> it's, is not -> isn't.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Language (Conventions).\n"
        "- Common Core State Standards for ELA, Grade 1 (L.1.2).\n")},
            "questions": qs}


# --- Chapter 13: Vocabulary — Word Meaning ----------------------------------
def ch_vocabulary():
    qs = []
    # Antonyms (opposites).
    ant = [("hot", "cold", ["warm", "wet", "big"]),
           ("up", "down", ["over", "tall", "in"]),
           ("happy", "sad", ["glad", "fast", "soft"]),
           ("big", "small", ["huge", "long", "round"]),
           ("fast", "slow", ["quick", "loud", "near"]),
           ("day", "night", ["sun", "noon", "week"])]
    for w, a, wrong in ant:
        qs.append(mcq(f"What is the OPPOSITE (antonym) of '{w}'?", a, wrong,
                      f"The opposite of '{w}' is '{a}'."))
    # Synonyms (same meaning).
    syn = [("big", "large", ["tiny", "blue", "fast"]),
           ("happy", "glad", ["angry", "sleepy", "tall"]),
           ("little", "small", ["huge", "loud", "wet"]),
           ("fast", "quick", ["slow", "soft", "cold"])]
    for w, s, wrong in syn:
        qs.append(mcq(f"Which word means almost the SAME as '{w}' (a synonym)?",
                      s, wrong, f"'{w}' and '{s}' mean about the same thing."))
    # Prefixes / suffixes.
    qs.append(mcq("The prefix 'un-' means 'not' or 'the opposite'. What does "
                  "'unhappy' mean?", "not happy", ["very happy", "happy again",
                  "almost happy"], "un- + happy = not happy."))
    qs.append(mcq("What does 'redo' mean? (prefix re- means 'again')",
                  "do again", ["do not", "do well", "stop doing"],
                  "re- + do = do again."))
    qs.append(mcq("The suffix '-ful' means 'full of'. What does 'helpful' mean?",
                  "full of help", ["without help", "a little help",
                  "help later"], "help + ful = full of help."))
    qs.append(mcq("What does 'unlock' mean?", "to open (the opposite of lock)",
                  ["to lock hard", "to lock again", "to lose a lock"],
                  "un- means the opposite, so unlock = the opposite of lock."))
    # Context clues.
    qs.append(mcq("Use the sentence to find the meaning: 'The tiny ant was so "
                  "small I could barely see it.' What does 'tiny' mean?",
                  "very small", ["very big", "very fast", "very loud"],
                  "The clue 'so small' tells you 'tiny' means very small."))
    qs.append(mcq("'The soup was so hot it burned my tongue.' What does 'hot' mean "
                  "here?", "very warm", ["spicy and red", "cold",
                  "a popular thing"], "The clue 'burned my tongue' shows hot = very "
                  "warm here."))
    # Multiple-meaning words.
    qs.append(mcq("The word 'bat' can mean two things. Which two?",
                  "a flying animal AND a stick for hitting a ball",
                  ["a fruit AND a color", "a number AND a day",
                   "a shoe AND a hat"],
                  "'bat' is a multiple-meaning word: the animal and the baseball "
                  "bat."))
    qs.append(mcq("In 'I will park the car,' what does 'park' mean?",
                  "to stop and leave a car", ["a place to play",
                  "to run fast", "a kind of food"],
                  "'park' has more than one meaning; here it means to stop the car."))
    # Categories / sorting.
    qs.append(mcq("Which word belongs in the group: apple, banana, grape, ____?",
                  "orange", ["chair", "shoe", "truck"],
                  "They are all fruits; 'orange' is a fruit too."))
    qs.append(mcq("Which word does NOT belong with the others?", "table",
                  ["dog", "cat", "rabbit"],
                  "dog, cat, and rabbit are animals; a table is not."))
    qs.append(mcq("Dogs, cats, and cows are all kinds of ____.", "animals",
                  ["food", "toys", "colors"],
                  "They all fit the category 'animals'."))
    # Shades of meaning.
    qs.append(mcq("Which word shows the BIGGEST feeling of being happy?",
                  "thrilled", ["okay", "fine", "glad"],
                  "thrilled is the strongest — okay/fine are small, glad is medium."))
    qs.append(short("What do we call two words that mean the OPPOSITE, like "
                    "'hot' and 'cold'?", "antonyms",
                    "Opposite words are antonyms."))
    qs.append(short("What do we call two words that mean almost the SAME, like "
                    "'big' and 'large'?", "synonyms",
                    "Same-meaning words are synonyms."))
    return {"name": "Vocabulary — Word Meaning",
            "source": {"title": "Vocabulary — knowledge base", "content": (
        "# Grade 1 ELA — Vocabulary (Word Meaning)\n\n"
        "**Standards: L.1.4, L.1.5, L.1.6.** Figuring out and using word "
        "meanings.\n\n"
        "## Big ideas\n"
        "- **Antonyms** are **opposites**: hot/cold, up/down, big/small, day/night.\n"
        "- **Synonyms** mean **almost the same**: big/large, happy/glad, "
        "little/small.\n"
        "- **Prefixes** go in front and change meaning: **un-** = not/opposite "
        "(unhappy, unlock), **re-** = again (redo, refill).\n"
        "- **Suffixes** go at the end: **-ful** = full of (helpful), **-less** = "
        "without (helpless).\n"
        "- **Context clues:** other words in the sentence help you guess what a "
        "new word means ('tiny... so small' -> tiny means very small).\n"
        "- **Multiple-meaning words** have more than one meaning: bat (animal / "
        "baseball bat), park (a place / to stop a car).\n"
        "- **Categories:** group words that go together (apple, banana = fruits; "
        "dog, cat = animals).\n"
        "- **Shades of meaning:** glad < happy < thrilled show feelings getting "
        "bigger.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Language (Vocabulary Acquisition).\n"
        "- Common Core State Standards for ELA, Grade 1 (L.1.4-6).\n")},
            "questions": qs}


# --- Chapter 14: Writing -----------------------------------------------------
def ch_writing():
    qs = [
        mcq("There are three kinds of writing in first grade. Which one tells what "
            "you THINK and gives a reason?", "an opinion piece",
            ["an information piece", "a story (narrative)", "a spelling list"],
            "An opinion piece shares what you think, with a reason ('because...')."),
        mcq("Which kind of writing TEACHES facts about a topic?",
            "an information (explaining) piece", ["an opinion piece",
            "a make-believe story", "a poem about feelings"],
            "Informative/explanatory writing gives facts about a real topic."),
        mcq("Which kind of writing TELLS a story about things that happened, in "
            "order?", "a narrative", ["an opinion piece",
            "an information piece", "a grocery list"],
            "A narrative tells events in order (first, next, then, last)."),
        mcq("Which sentence is a good OPINION sentence?",
            "I think dogs are the best pets because they are friendly.",
            ["Dogs have four legs.", "A dog is an animal.",
             "Dogs can bark."],
            "It says what you think AND gives a reason ('because they are "
            "friendly')."),
        mcq("Which word helps you give a REASON for your opinion?", "because",
            ["and", "the", "very"],
            "'because' introduces a reason: I like it BECAUSE..."),
        mcq("Which words help tell a story in ORDER?", "first, next, then, last",
            ["big, small, round", "red, blue, green", "happy, sad, mad"],
            "Order/sequence words (first, next, then, last) show what happens "
            "in order."),
        mcq("When you START writing a sentence, the first letter should be ____.",
            "a capital letter", ["a small letter", "a number", "underlined"],
            "Every sentence begins with a capital letter."),
        mcq("Your story should have a ____ that tells what it is about.",
            "title", ["price", "phone number", "map"],
            "A title names the topic of your writing."),
        mcq("After you write, you should ____ to fix mistakes.",
            "check (edit) your work", ["throw it away", "hide it",
            "leave the periods out"],
            "Editing means rereading and fixing capitals, spelling, and "
            "punctuation."),
        tf("A good piece of writing has a beginning, a middle, and an end.",
           True, "Like stories, writing is organized with a beginning, middle, "
           "and end."),
        tf("It is fine to leave the period off the end of every sentence.",
           False, "Telling sentences need an end mark (a period)."),
        tf("Adding details (more describing words) makes your writing clearer and "
           "more interesting.", True,
           "Details help the reader picture what you mean."),
        short("What joining word do you use to give a reason for your opinion?",
              "because", "Use 'because' to give a reason."),
        short("Name one order word you can use to tell what happens next in a "
              "story.", "next",
              "Order words include first, next, then, after, and last."),
    ]
    return {"name": "Writing — Opinion, Information & Stories",
            "source": {"title": "Writing — knowledge base", "content": (
        "# Grade 1 ELA — Writing\n\n"
        "**Standards: W.1.1, W.1.2, W.1.3, W.1.5.** Putting ideas on paper.\n\n"
        "## Big ideas\n"
        "- Three kinds of writing:\n"
        "  - **Opinion:** tells what you **think** and gives a **reason** "
        "('I like... because...').\n"
        "  - **Information (explaining):** teaches **facts** about a real topic.\n"
        "  - **Narrative (story):** tells events **in order** (first, next, then, "
        "last).\n"
        "- Every sentence starts with a **capital letter** and ends with the right "
        "**mark** ( . ? ! ).\n"
        "- Good writing has a **beginning, middle, and end**, a **title**, and "
        "**details** that make it clear.\n"
        "- Use **because** to give a reason, and **order words** (first, next, "
        "then, last) to tell a story.\n"
        "- **Edit:** reread and fix capitals, spelling, and punctuation.\n\n"
        "## Sources\n"
        "- MSDE *Grade 1 ELA Framework* — Writing.\n"
        "- Common Core State Standards for ELA, Grade 1 (W.1).\n")},
            "questions": qs}


def build():
    chapters = [
        ch_sentences(), ch_phonological(), ch_phonics_short(), ch_phonics_long(),
        ch_phonics_digraphs(), ch_word_parts(), ch_sight_words(),
        ch_comprehension_lit(), ch_comprehension_info(), ch_nouns(),
        ch_verbs_adj(), ch_caps_punct(), ch_vocabulary(), ch_writing(),
    ]
    bank = {
        "subject": {
            "name": "Grade 1 Reading & Language Arts (Anne Arundel County)",
            "description": "Comprehensive first-grade English Language Arts, aligned "
                           "to the Maryland College and Career-Ready Standards (the "
                           "standards AACPS teaches to): phonics & word study, "
                           "reading comprehension, grammar & conventions, "
                           "vocabulary, and writing. The non-math half of a "
                           "grade-acceleration review set.",
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
