"""Bulk-import a question bank (subject -> chapters -> questions) into FleetQuiz.

This is the ingestion glue for the research -> question-writing pipeline: a
quiz-writer produces a JSON file in the schema below, and this script loads it
into the same DB the app uses (QUIZ_DB_PATH). It mirrors seed.py but is driven
by data, idempotent, and attaches each chapter's knowledge base as a `source`
so every imported question is traceable.

Schema (JSON):
{
  "subject": {"name": "...", "description": "..."},
  "chapters": [
    {
      "name": "Chapter 1 — ...",
      "source": {"title": "...", "content": "...markdown KB..."},   # optional
      "questions": [
        {"type": "mcq",        "prompt": "...", "choices": ["A","B","C","D"],
         "answer": "B", "explanation": "..."},
        {"type": "truefalse",  "prompt": "...", "answer": "True",  "explanation": "..."},
        {"type": "short",      "prompt": "...", "answer": "...",   "explanation": "..."}
      ]
    }
  ]
}

Run:  QUIZ_DB_PATH=./data/quiz.db python -m import_bank path/to/bank.json
Idempotent: re-running skips a question if one with the same prompt already
exists in that chapter, so you can append to a bank without duplicating.
"""
import json
import sys

from app.db import get_conn, init_db

VALID_TYPES = {"mcq", "truefalse", "short"}


def _normalise(q):
    """Validate + clean one question dict. Returns (clean, None) or (None, reason)."""
    qtype = str(q.get("type", "")).strip().lower()
    if qtype not in VALID_TYPES:
        return None, f"bad type {qtype!r}"
    prompt = str(q.get("prompt", "")).strip()
    answer = str(q.get("answer", "")).strip()
    if not prompt or not answer:
        return None, "empty prompt or answer"
    choices = q.get("choices") or []
    choices = [str(c).strip() for c in choices if str(c).strip()]
    if qtype == "truefalse":
        choices = ["True", "False"]
        answer = "True" if answer.lower().startswith("t") else "False"
    elif qtype == "mcq":
        if len(choices) < 2:
            return None, "mcq needs >=2 choices"
        if answer not in choices:  # ensure the answer is present verbatim
            match = next((c for c in choices if c.lower() == answer.lower()), None)
            if match:
                answer = match
            else:
                choices.append(answer)
    else:  # short
        choices = []
    return {
        "type": qtype, "prompt": prompt, "choices": choices,
        "answer": answer, "explanation": str(q.get("explanation", "")).strip(),
    }, None


def import_bank(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subj = data["subject"]
    stats = {"chapters": 0, "questions": 0, "skipped_dupe": 0, "rejected": 0, "sources": 0}
    init_db()
    with get_conn() as conn:
        row = conn.execute("SELECT id FROM subjects WHERE name = ?", (subj["name"],)).fetchone()
        if row:
            subject_id = row["id"]
        else:
            subject_id = conn.execute(
                "INSERT INTO subjects (name, description) VALUES (?, ?)",
                (subj["name"], subj.get("description", "")),
            ).lastrowid

        for pos, ch in enumerate(data["chapters"]):
            crow = conn.execute(
                "SELECT id FROM chapters WHERE subject_id = ? AND name = ?",
                (subject_id, ch["name"]),
            ).fetchone()
            if crow:
                chapter_id = crow["id"]
            else:
                chapter_id = conn.execute(
                    "INSERT INTO chapters (subject_id, name, position) VALUES (?, ?, ?)",
                    (subject_id, ch["name"], pos),
                ).lastrowid
                stats["chapters"] += 1

            # Attach the chapter's knowledge base as a reusable source (once).
            source_id = None
            src = ch.get("source")
            if src and src.get("content"):
                existing_src = conn.execute(
                    "SELECT id FROM sources WHERE subject_id = ? AND title = ? AND kind = 'text'",
                    (subject_id, src.get("title", ch["name"])),
                ).fetchone()
                if existing_src:
                    source_id = existing_src["id"]
                else:
                    source_id = conn.execute(
                        "INSERT INTO sources (subject_id, title, kind, content) VALUES (?, ?, 'text', ?)",
                        (subject_id, src.get("title", ch["name"]), src["content"]),
                    ).lastrowid
                    stats["sources"] += 1

            existing_prompts = {
                r["prompt"] for r in conn.execute(
                    "SELECT prompt FROM questions WHERE chapter_id = ?", (chapter_id,))
            }
            for raw in ch.get("questions", []):
                q, reason = _normalise(raw)
                if not q:
                    stats["rejected"] += 1
                    continue
                if q["prompt"] in existing_prompts:
                    stats["skipped_dupe"] += 1
                    continue
                conn.execute(
                    """INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation, source_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (chapter_id, q["type"], q["prompt"], json.dumps(q["choices"]),
                     q["answer"], q["explanation"], source_id),
                )
                existing_prompts.add(q["prompt"])
                stats["questions"] += 1

    print(f"Imported into subject '{subj['name']}': "
          f"+{stats['chapters']} chapters, +{stats['questions']} questions, "
          f"+{stats['sources']} sources "
          f"({stats['skipped_dupe']} dupes skipped, {stats['rejected']} rejected).")
    return stats


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m import_bank <bank.json>", file=sys.stderr)
        sys.exit(2)
    import_bank(sys.argv[1])
