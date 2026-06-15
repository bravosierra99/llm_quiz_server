"""Shared question-bank import logic.

Used by both the `/import` admin endpoint (app.main) and the `import_bank.py`
CLI. Loads a parsed bank dict (subject -> chapters -> questions) into the DB:
idempotent (skips a question whose prompt already exists in that chapter),
validates/normalises each question, and attaches each chapter's knowledge base
as a `source` so imported questions stay traceable.

Bank JSON schema:
{
  "subject": {"name": "...", "description": "..."},
  "chapters": [
    {"name": "...",
     "source": {"title": "...", "content": "...markdown KB..."},   # optional
     "questions": [
       {"type": "mcq", "prompt": "...", "choices": ["A","B","C","D"],
        "answer": "B", "explanation": "..."},
       {"type": "truefalse", "prompt": "...", "answer": "True", "explanation": "..."},
       {"type": "short", "prompt": "...", "answer": "...", "explanation": "..."}
     ]}
  ]
}
"""
import json

from .db import get_conn

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
            answer = match if match else (choices.append(answer) or answer)
    else:  # short
        choices = []
    return {
        "type": qtype, "prompt": prompt, "choices": choices,
        "answer": answer, "explanation": str(q.get("explanation", "")).strip(),
    }, None


def import_bank_data(data):
    """Import a parsed bank dict into the DB (schema must already exist — the app
    runs init_db at startup; the CLI calls it first). Returns a stats dict
    including the subject id/name. Raises KeyError/TypeError on a malformed top
    level so callers can show a friendly error."""
    subj = data["subject"]
    chapters = data["chapters"]
    if not isinstance(chapters, list):
        raise TypeError("'chapters' must be a list")
    stats = {"subject": subj["name"], "subject_id": None, "chapters": 0,
             "questions": 0, "skipped_dupe": 0, "rejected": 0, "sources": 0}

    with get_conn() as conn:
        row = conn.execute("SELECT id FROM subjects WHERE name = ?", (subj["name"],)).fetchone()
        if row:
            subject_id = row["id"]
        else:
            subject_id = conn.execute(
                "INSERT INTO subjects (name, description) VALUES (?, ?)",
                (subj["name"], subj.get("description", "")),
            ).lastrowid
        stats["subject_id"] = subject_id

        for pos, ch in enumerate(chapters):
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
                q, _reason = _normalise(raw)
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

    return stats
