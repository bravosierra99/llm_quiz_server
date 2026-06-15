"""In-process background LLM jobs (generate-more, flag-fix).

A single daemon worker thread drains a queue and runs jobs one at a time (the
local model is single-stream). Jobs are persisted in the `jobs` table and
requeued on startup. Every job produces zero or more `proposals` that an admin
approves before anything touches the question bank.

Connection discipline (critical): SQLite is single-writer, so the worker NEVER
holds a DB connection across the slow LLM/search call. The pattern is:
  open conn -> claim job (running) -> close;  search + LLM with NO conn held;
  open conn -> write proposals + mark done -> close.

Assumes exactly ONE uvicorn worker process (see Dockerfile CMD). With multiple
workers each process would start its own worker + requeue and double-run jobs.
"""
import json
import os
import queue
import threading

from . import ai, search, sources
from .db import get_conn, jloads

_Q = queue.Queue()
_started = False
_lock = threading.Lock()


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def enqueue(kind, user_id, question_id):
    """Create a job and queue it. Deduped: if a pending/running job of the same
    kind already exists for this question, return that one instead."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM jobs WHERE question_id = ? AND kind = ? AND status IN ('pending','running')",
            (question_id, kind)).fetchone()
        if existing:
            return existing["id"]
        jid = conn.execute(
            "INSERT INTO jobs (kind, user_id, question_id) VALUES (?, ?, ?)",
            (kind, user_id, question_id)).lastrowid
    _Q.put(jid)
    return jid


def start_worker():
    """Start the worker thread once (idempotent). Resets orphaned 'running' jobs
    (e.g. killed by a deploy) back to 'pending' and requeues all pending jobs.
    Skipped when QUIZ_DISABLE_WORKER is set (tests call run_job directly)."""
    global _started
    if os.environ.get("QUIZ_DISABLE_WORKER"):
        return
    with _lock:
        if _started:
            return
        _started = True
    with get_conn() as conn:
        conn.execute("UPDATE jobs SET status = 'pending' WHERE status = 'running'")
        pending = [r["id"] for r in conn.execute(
            "SELECT id FROM jobs WHERE status = 'pending' ORDER BY id")]
    for jid in pending:
        _Q.put(jid)
    threading.Thread(target=_loop, daemon=True, name="quiz-jobs").start()


def _loop():
    while True:
        jid = _Q.get()
        try:
            run_job(jid)
        except Exception:  # never let the worker thread die
            pass
        finally:
            _Q.task_done()


# --------------------------------------------------------------------------
# Job execution
# --------------------------------------------------------------------------
def run_job(jid):
    """Claim and run one job. Safe to call directly (tests do)."""
    with get_conn() as conn:
        job = conn.execute("SELECT * FROM jobs WHERE id = ?", (jid,)).fetchone()
        if not job or job["status"] != "pending":
            return
        conn.execute("UPDATE jobs SET status = 'running' WHERE id = ?", (jid,))
        job = dict(job)
    try:
        if job["kind"] == "generate_more":
            _run_generate_more(job)
        elif job["kind"] == "flag_fix":
            _run_flag_fix(job)
        else:
            _finish(jid, "error", f"unknown kind {job['kind']}")
    except Exception as e:  # noqa: BLE001
        _finish(jid, "error", f"job crashed: {e}")


def _finish(jid, status, message):
    with get_conn() as conn:
        conn.execute(
            "UPDATE jobs SET status = ?, message = ?, finished_at = datetime('now') WHERE id = ?",
            (status, str(message)[:500], jid))


def _load_context(qid):
    """Short DB read: the seed/flagged question + its chapter, subject and KB.
    Returns None if the question is gone."""
    with get_conn() as conn:
        q = conn.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone()
        if not q:
            return None
        q = dict(q)
        q["choices"] = jloads(q["choices"])
        chapter = dict(conn.execute("SELECT * FROM chapters WHERE id = ?", (q["chapter_id"],)).fetchone())
        subject = dict(conn.execute(
            "SELECT s.* FROM subjects s JOIN chapters c ON c.subject_id = s.id WHERE c.id = ?",
            (q["chapter_id"],)).fetchone())
        src = sources.get(conn, q["source_id"]) if q["source_id"] else None
        kb = sources.text_for_generation(src) if src else ""
    return q, chapter, subject, kb, q["source_id"]


def _subject_context(subject, chapter):
    ctx = f"Subject/library: {subject['name']}."
    if subject.get("description"):
        ctx += f" The point of this subject: {subject['description']}."
    return ctx + f" Chapter: {chapter['name']}."


def _run_generate_more(job):
    ctx = _load_context(job["question_id"])
    if not ctx:
        _finish(job["id"], "error", "seed question no longer exists")
        return
    q, chapter, subject, kb, source_id = ctx
    results, serr = search.web_search(f"{subject['name']} {chapter['name']} {q['prompt']}")
    topic = (f"{_subject_context(subject, chapter)} Write more questions in the same style "
             f"and difficulty as this one, on closely related material (do NOT duplicate it): "
             f"\"{q['prompt']}\".\n\nReference these web search results for accuracy:\n"
             f"{search.format_results(results)}")
    result = ai.generate_questions("source" if kb else "topic", topic, kb or "", 5, "medium", [q["type"]])
    if not result["ok"]:
        _finish(job["id"], "error", (result["error"] or "generation failed") + _suffix(serr))
        return
    n = 0
    with get_conn() as conn:
        existing = {r["prompt"] for r in conn.execute(
            "SELECT prompt FROM questions WHERE chapter_id = ?", (q["chapter_id"],))}
        existing |= {r["prompt"] for r in conn.execute(
            "SELECT prompt FROM proposals WHERE chapter_id = ? AND status = 'pending'", (q["chapter_id"],))}
        for raw in result["questions"]:
            if raw["prompt"] in existing:
                continue
            conn.execute(
                """INSERT INTO proposals (job_id, kind, chapter_id, type, prompt, choices, answer, explanation, source_id, rationale)
                   VALUES (?, 'add', ?, ?, ?, ?, ?, ?, ?, ?)""",
                (job["id"], q["chapter_id"], raw["type"], raw["prompt"], json.dumps(raw["choices"]),
                 raw["answer"], raw["explanation"], source_id, "Generated from a similar question."))
            existing.add(raw["prompt"])
            n += 1
    _finish(job["id"], "done", f"proposed {n} new question(s)" + _suffix(serr))


def _run_flag_fix(job):
    ctx = _load_context(job["question_id"])
    if not ctx:
        _finish(job["id"], "error", "flagged question no longer exists")
        return
    q, chapter, subject, kb, source_id = ctx
    results, serr = search.web_search(f"{subject['name']} {q['prompt']} {q['answer']}")
    try:
        fix = ai.verify_and_fix(q, _subject_context(subject, chapter), kb, search.format_results(results))
    except Exception as e:  # connection or parse failure
        _finish(job["id"], "error", f"verify failed: {e}" + _suffix(serr))
        return
    if not fix.get("needs_fix"):
        _finish(job["id"], "done", "verified — no change needed" + _suffix(serr))
        return
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO proposals (job_id, kind, chapter_id, question_id, type, prompt, choices, answer, explanation, source_id, rationale)
               VALUES (?, 'edit', ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (job["id"], q["chapter_id"], q["id"], fix.get("type", q["type"]),
             str(fix.get("prompt", q["prompt"])), json.dumps(fix.get("choices") or []),
             str(fix.get("answer", q["answer"])), str(fix.get("explanation", "")),
             source_id, str(fix.get("rationale", ""))))
    _finish(job["id"], "done", "proposed a correction" + _suffix(serr))


def _suffix(serr):
    return f" · search: {serr}" if serr else ""
