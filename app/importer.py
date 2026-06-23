"""Shared question-bank import logic.

Used by both the `/import` admin endpoint (app.main) and the `import_bank.py`
CLI. Loads a parsed bank dict (a root topic -> a tree of nodes -> questions) into
the DB: idempotent (skips a question whose prompt already exists on that node),
validates/normalises each question, and attaches a node's knowledge base as a
`source` (at the topic root) so imported questions stay traceable.

Bank JSON schema — arbitrary depth via recursive `children`:
{
  "topic": {"name": "...", "description": "...", "teaching_notes": "..."},
  "children": [
    {"name": "...",
     "source": {"title": "...", "content": "...markdown KB..."},   # optional
     "questions": [
       {"type": "mcq", "prompt": "...", "choices": ["A","B","C","D"],
        "answer": "B", "explanation": "..."},
       {"type": "truefalse", "prompt": "...", "answer": "True", "explanation": "..."},
       {"type": "short", "prompt": "...", "answer": "...", "explanation": "..."}
     ],
     "children": [ ...recurse to any depth... ]}    # optional
  ]
}

Back-compat: the original flat shape — {"subject": {...}, "chapters": [...]} — is
still accepted; `subject`==`topic` and `chapters`==`children`.
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
    including the topic (root) id/name. Raises KeyError/TypeError on a malformed
    top level so callers can show a friendly error.

    `chapters` in the stats counts every node CREATED across the whole tree."""
    root_spec = data.get("topic") or data.get("subject")
    if not root_spec or "name" not in root_spec:
        raise KeyError("topic")
    children = data.get("children")
    if children is None:
        children = data.get("chapters", [])
    if not isinstance(children, list):
        raise TypeError("'children'/'chapters' must be a list")
    stats = {"subject": root_spec["name"], "subject_id": None, "chapters": 0,
             "questions": 0, "skipped_dupe": 0, "rejected": 0, "sources": 0}

    with get_conn() as conn:
        # Find or create the ROOT topic node (parent_id IS NULL).
        row = conn.execute(
            "SELECT id FROM chapters WHERE name = ? AND parent_id IS NULL",
            (root_spec["name"],)).fetchone()
        if row:
            root_id = row["id"]
        else:
            root_id = conn.execute(
                "INSERT INTO chapters (parent_id, name, description, teaching_notes) "
                "VALUES (NULL, ?, ?, ?)",
                (root_spec["name"], root_spec.get("description", ""),
                 root_spec.get("teaching_notes", "")),
            ).lastrowid
        stats["subject_id"] = root_id
        _import_nodes(conn, root_id, root_id, children, stats)

    return stats


def _import_nodes(conn, parent_id, root_id, nodes, stats):
    """Recursively import a list of child nodes under `parent_id`. KB sources are
    attached at the topic `root_id` (sources are topic-level)."""
    for pos, node in enumerate(nodes):
        crow = conn.execute(
            "SELECT id FROM chapters WHERE parent_id = ? AND name = ?",
            (parent_id, node["name"]),
        ).fetchone()
        if crow:
            node_id = crow["id"]
        else:
            node_id = conn.execute(
                "INSERT INTO chapters (parent_id, name, position) VALUES (?, ?, ?)",
                (parent_id, node["name"], pos),
            ).lastrowid
            stats["chapters"] += 1

        # Attach the node's knowledge base as a reusable source (once), at the root.
        source_id = None
        src = node.get("source")
        if src and src.get("content"):
            existing_src = conn.execute(
                "SELECT id FROM sources WHERE subject_id = ? AND title = ? AND kind = 'text'",
                (root_id, src.get("title", node["name"])),
            ).fetchone()
            if existing_src:
                source_id = existing_src["id"]
            else:
                source_id = conn.execute(
                    "INSERT INTO sources (subject_id, title, kind, content) VALUES (?, ?, 'text', ?)",
                    (root_id, src.get("title", node["name"]), src["content"]),
                ).lastrowid
                stats["sources"] += 1

        existing_prompts = {
            r["prompt"] for r in conn.execute(
                "SELECT prompt FROM questions WHERE chapter_id = ?", (node_id,))
        }
        for raw in node.get("questions", []):
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
                (node_id, q["type"], q["prompt"], json.dumps(q["choices"]),
                 q["answer"], q["explanation"], source_id),
            )
            existing_prompts.add(q["prompt"])
            stats["questions"] += 1

        # Recurse into nested children (arbitrary depth).
        sub = node.get("children")
        if sub:
            _import_nodes(conn, node_id, root_id, sub, stats)
