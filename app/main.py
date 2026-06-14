"""FleetQuiz — a family self-study quiz app.

Server-rendered FastAPI + Jinja2. The whole UI is plain HTML forms so it works
on any device with no build step. Routes are grouped: identity, library
(subjects/chapters/questions), AI generation, and the quiz loop.
"""
import json
import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import ai, auth, scheduler
from .db import get_conn, init_db, jloads

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI(title="FleetQuiz")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.on_event("startup")
def _startup():
    init_db()


def render(request, template, **ctx):
    ctx.setdefault("user", auth.current_user(request))
    ctx["request"] = request
    return templates.TemplateResponse(template, ctx)


def require_user(request):
    """Returns user dict or a RedirectResponse to the picker."""
    user = auth.current_user(request)
    if not user:
        return None, RedirectResponse("/who", status_code=303)
    return user, None


def require_admin(request):
    """Returns (user, None) for admins, else (None, response) — a redirect to the
    picker if signed out, or a 403 page if a non-admin profile tries to edit.

    Caveat: this only truly bites behind Cloudflare Access (trusted email ->
    is_admin). On the bare-LAN profile picker anyone can pick an admin profile,
    since profiles have no password. Its real job here is to stop a kid's profile
    from accidentally deleting content. See auth.py for the full security note."""
    user = auth.current_user(request)
    if not user:
        return None, RedirectResponse("/who", status_code=303)
    if not user.get("is_admin"):
        return None, render(request, "forbidden.html", user=user)
    return user, None


# --------------------------------------------------------------------------
# Identity
# --------------------------------------------------------------------------
@app.get("/who", response_class=HTMLResponse)
def who(request: Request):
    return render(request, "who.html", users=auth.list_users())


@app.post("/who/pick")
def who_pick(request: Request, user_id: int = Form(...)):
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie(auth.COOKIE_NAME, auth.sign_user_id(user_id), max_age=60 * 60 * 24 * 365,
                    httponly=True, samesite="lax")
    return resp


@app.post("/who/new")
def who_new(request: Request, name: str = Form(...), email: str = Form("")):
    u = auth.create_user(name, email or None)
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie(auth.COOKIE_NAME, auth.sign_user_id(u["id"]), max_age=60 * 60 * 24 * 365,
                    httponly=True, samesite="lax")
    return resp


@app.get("/logout")
def logout():
    resp = RedirectResponse("/who", status_code=303)
    resp.delete_cookie(auth.COOKIE_NAME)
    return resp


# --------------------------------------------------------------------------
# Dashboard + library
# --------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subjects = [dict(r) for r in conn.execute("""
            SELECT s.*,
                   (SELECT COUNT(*) FROM chapters c WHERE c.subject_id = s.id) AS chapter_count,
                   (SELECT COUNT(*) FROM questions q JOIN chapters c ON q.chapter_id = c.id
                      WHERE c.subject_id = s.id) AS question_count
            FROM subjects s ORDER BY s.name
        """)]
        recent = [dict(r) for r in conn.execute("""
            SELECT * FROM quiz_sessions WHERE user_id = ? AND finished_at IS NOT NULL
            ORDER BY finished_at DESC LIMIT 8
        """, (user["id"],))]
    return render(request, "index.html", subjects=subjects, recent=recent)


@app.post("/subjects")
def create_subject(request: Request, name: str = Form(...), description: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("INSERT INTO subjects (name, description) VALUES (?, ?)",
                     (name.strip(), description.strip()))
    return RedirectResponse("/", status_code=303)


@app.get("/subjects/{subject_id}", response_class=HTMLResponse)
def view_subject(request: Request, subject_id: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subject = conn.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
        if not subject:
            return RedirectResponse("/", status_code=303)
        chapters = [dict(r) for r in conn.execute("""
            SELECT c.*, (SELECT COUNT(*) FROM questions q WHERE q.chapter_id = c.id) AS question_count
            FROM chapters c WHERE c.subject_id = ? ORDER BY c.position, c.id
        """, (subject_id,))]
        for c in chapters:
            c["progress"] = scheduler.chapter_progress(conn, user["id"], c["id"])
    return render(request, "subject.html", subject=dict(subject), chapters=chapters)


@app.post("/subjects/{subject_id}/chapters")
def create_chapter(request: Request, subject_id: int, name: str = Form(...), position: int = Form(0)):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("INSERT INTO chapters (subject_id, name, position) VALUES (?, ?, ?)",
                     (subject_id, name.strip(), position))
    return RedirectResponse(f"/subjects/{subject_id}", status_code=303)


@app.post("/subjects/{subject_id}/delete")
def delete_subject(request: Request, subject_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    return RedirectResponse("/", status_code=303)


@app.get("/chapters/{chapter_id}", response_class=HTMLResponse)
def view_chapter(request: Request, chapter_id: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        chapter = conn.execute("""
            SELECT c.*, s.name AS subject_name FROM chapters c
            JOIN subjects s ON c.subject_id = s.id WHERE c.id = ?
        """, (chapter_id,)).fetchone()
        if not chapter:
            return RedirectResponse("/", status_code=303)
        questions = [dict(r) for r in conn.execute(
            "SELECT * FROM questions WHERE chapter_id = ? ORDER BY id", (chapter_id,))]
    for q in questions:
        q["choices"] = jloads(q["choices"])
    return render(request, "chapter.html", chapter=dict(chapter), questions=questions)


@app.post("/chapters/{chapter_id}/delete")
def delete_chapter(request: Request, chapter_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subj = conn.execute("SELECT subject_id FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
        conn.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    return RedirectResponse(f"/subjects/{subj['subject_id']}" if subj else "/", status_code=303)


# --------------------------------------------------------------------------
# Manual question CRUD  (the LLM-free path — also the app's test path)
# --------------------------------------------------------------------------
@app.get("/chapters/{chapter_id}/questions/new", response_class=HTMLResponse)
def new_question(request: Request, chapter_id: int):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
    return render(request, "question_edit.html", chapter=dict(chapter), q=None)


@app.get("/questions/{question_id}/edit", response_class=HTMLResponse)
def edit_question(request: Request, question_id: int):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        q = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
        if not q:
            return RedirectResponse("/", status_code=303)
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (q["chapter_id"],)).fetchone()
    q = dict(q)
    q["choices"] = jloads(q["choices"])
    return render(request, "question_edit.html", chapter=dict(chapter), q=q)


def _parse_question_form(qtype, prompt, choices_text, answer, explanation):
    choices = [c.strip() for c in choices_text.splitlines() if c.strip()]
    if qtype == "truefalse":
        choices = ["True", "False"]
        answer = "True" if answer.strip().lower().startswith("t") else "False"
    elif qtype == "short":
        choices = []
    return prompt.strip(), json.dumps(choices), answer.strip(), explanation.strip()


@app.post("/chapters/{chapter_id}/questions")
def save_new_question(request: Request, chapter_id: int, type: str = Form(...),
                      prompt: str = Form(...), choices: str = Form(""),
                      answer: str = Form(...), explanation: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    p, ch, a, e = _parse_question_form(type, prompt, choices, answer, explanation)
    with get_conn() as conn:
        conn.execute("""INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation)
                        VALUES (?, ?, ?, ?, ?, ?)""", (chapter_id, type, p, ch, a, e))
    return RedirectResponse(f"/chapters/{chapter_id}", status_code=303)


@app.post("/questions/{question_id}")
def update_question(request: Request, question_id: int, type: str = Form(...),
                    prompt: str = Form(...), choices: str = Form(""),
                    answer: str = Form(...), explanation: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    p, ch, a, e = _parse_question_form(type, prompt, choices, answer, explanation)
    with get_conn() as conn:
        conn.execute("""UPDATE questions SET type=?, prompt=?, choices=?, answer=?, explanation=?
                        WHERE id=?""", (type, p, ch, a, e, question_id))
        cid = conn.execute("SELECT chapter_id FROM questions WHERE id = ?", (question_id,)).fetchone()
    return RedirectResponse(f"/chapters/{cid['chapter_id']}", status_code=303)


@app.post("/questions/{question_id}/delete")
def delete_question(request: Request, question_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        cid = conn.execute("SELECT chapter_id FROM questions WHERE id = ?", (question_id,)).fetchone()
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    return RedirectResponse(f"/chapters/{cid['chapter_id']}" if cid else "/", status_code=303)


# --------------------------------------------------------------------------
# AI generation  ->  review  ->  bulk save
# --------------------------------------------------------------------------
@app.get("/chapters/{chapter_id}/generate", response_class=HTMLResponse)
def generate_form(request: Request, chapter_id: int):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
    return render(request, "generate.html", chapter=dict(chapter),
                  ai_base=ai.AI_BASE_URL, ai_model=ai.AI_MODEL)


@app.post("/chapters/{chapter_id}/generate", response_class=HTMLResponse)
def generate_run(request: Request, chapter_id: int, mode: str = Form("topic"),
                 topic: str = Form(""), source_text: str = Form(""),
                 num_questions: int = Form(8), difficulty: str = Form("medium"),
                 types: list[str] = Form(default=["mcq", "truefalse", "short"])):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    result = ai.generate_questions(mode, topic, source_text, num_questions, difficulty, types)
    with get_conn() as conn:
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
    return render(request, "review.html", chapter=dict(chapter), result=result)


@app.post("/chapters/{chapter_id}/generate/save")
async def generate_save(request: Request, chapter_id: int):
    """Save the (possibly admin-edited) reviewed questions. The review form posts
    arrays indexed per question; we reconstruct and insert the kept ones."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    form = await request.form()
    n = int(form.get("count", 0))
    saved = 0
    with get_conn() as conn:
        for i in range(n):
            if form.get(f"keep_{i}") != "on":
                continue
            qtype = form.get(f"type_{i}", "short")
            prompt = (form.get(f"prompt_{i}") or "").strip()
            answer = (form.get(f"answer_{i}") or "").strip()
            if not prompt or not answer:
                continue
            choices_raw = form.get(f"choices_{i}", "")
            choices = [c.strip() for c in choices_raw.splitlines() if c.strip()]
            if qtype == "truefalse":
                choices = ["True", "False"]
            elif qtype == "short":
                choices = []
            explanation = (form.get(f"explanation_{i}") or "").strip()
            conn.execute("""INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                         (chapter_id, qtype, prompt, json.dumps(choices), answer, explanation))
            saved += 1
    return RedirectResponse(f"/chapters/{chapter_id}?saved={saved}", status_code=303)


# --------------------------------------------------------------------------
# Quiz loop
# --------------------------------------------------------------------------
@app.get("/quiz", response_class=HTMLResponse)
def quiz_setup(request: Request):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subjects = [dict(r) for r in conn.execute("SELECT * FROM subjects ORDER BY name")]
        chapters = [dict(r) for r in conn.execute("""
            SELECT c.*, s.name AS subject_name,
                   (SELECT COUNT(*) FROM questions q WHERE q.chapter_id = c.id) AS question_count
            FROM chapters c JOIN subjects s ON c.subject_id = s.id
            ORDER BY s.name, c.position, c.id
        """)]
        for c in chapters:
            # Surface the mastery recommendation right where chapters are picked.
            c["progress"] = scheduler.chapter_progress(conn, user["id"], c["id"])
    return render(request, "quiz_setup.html", subjects=subjects, chapters=chapters)


@app.post("/quiz/start")
def quiz_start(request: Request, chapter_ids: list[int] = Form(default=[]),
               num_questions: int = Form(10), order: str = Form("adaptive")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    if not chapter_ids:
        return RedirectResponse("/quiz", status_code=303)
    placeholders = ",".join("?" for _ in chapter_ids)
    with get_conn() as conn:
        # Adaptive (default) selection: due > new > not-yet-due. See scheduler.
        qids = scheduler.select_question_ids(conn, user["id"], chapter_ids, num_questions, order)
        if not qids:
            return RedirectResponse("/quiz", status_code=303)
        names = conn.execute(
            f"SELECT name FROM chapters WHERE id IN ({placeholders})", chapter_ids).fetchall()
        label = ", ".join(n["name"] for n in names)
        cur = conn.execute(
            "INSERT INTO quiz_sessions (user_id, chapter_ids, label, total) VALUES (?, ?, ?, ?)",
            (user["id"], json.dumps(chapter_ids), label, len(qids)),
        )
        session_id = cur.lastrowid
        # The queue lives in session_questions — NOT in answers — so an abandoned
        # session contributes nothing to analytics or recall state.
        for pos, qid in enumerate(qids):
            conn.execute(
                "INSERT INTO session_questions (session_id, position, question_id) VALUES (?, ?, ?)",
                (session_id, pos, qid))
    return RedirectResponse(f"/quiz/{session_id}/q/0", status_code=303)


def _session_question_ids(conn, session_id):
    return [r["question_id"] for r in conn.execute(
        "SELECT question_id FROM session_questions WHERE session_id = ? ORDER BY position",
        (session_id,))]


@app.get("/quiz/{session_id}/q/{idx}", response_class=HTMLResponse)
def quiz_question(request: Request, session_id: int, idx: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        session = conn.execute("SELECT * FROM quiz_sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            return RedirectResponse("/quiz", status_code=303)
        qids = _session_question_ids(conn, session_id)
        if idx >= len(qids):
            return RedirectResponse(f"/quiz/{session_id}/results", status_code=303)
        q = dict(conn.execute("SELECT * FROM questions WHERE id = ?", (qids[idx],)).fetchone())
    q["choices"] = jloads(q["choices"])
    return render(request, "quiz.html", session=dict(session), q=q, idx=idx, total=len(qids))


@app.post("/quiz/{session_id}/q/{idx}")
def quiz_answer(request: Request, session_id: int, idx: int,
                answer: str = Form(""), self_correct: str = Form("")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        session = conn.execute("SELECT * FROM quiz_sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            return RedirectResponse("/quiz", status_code=303)
        qids = _session_question_ids(conn, session_id)
        if idx >= len(qids):
            return RedirectResponse(f"/quiz/{session_id}/results", status_code=303)
        q = dict(conn.execute("SELECT * FROM questions WHERE id = ?", (qids[idx],)).fetchone())
        if q["type"] == "short":
            # Self-graded flashcard style: the form already revealed the answer.
            is_correct = 1 if self_correct == "yes" else 0
            user_answer = answer.strip()
        else:
            is_correct = 1 if answer.strip() == q["answer"].strip() else 0
            user_answer = answer.strip()

        existing = conn.execute(
            "SELECT id FROM answers WHERE session_id = ? AND question_id = ?",
            (session_id, q["id"])).fetchone()
        if existing:
            # Resubmit (e.g. browser back). Record the latest answer but DON'T
            # re-grade — first retrieval is the real signal and re-grading would
            # double-count reps/lapses.
            conn.execute(
                "UPDATE answers SET user_answer = ?, is_correct = ?, answered_at = datetime('now') "
                "WHERE id = ?",
                (user_answer, is_correct, existing["id"]))
        else:
            conn.execute(
                "INSERT INTO answers (session_id, question_id, user_answer, is_correct) VALUES (?, ?, ?, ?)",
                (session_id, q["id"], user_answer, is_correct))
            # Grade the SESSION OWNER (profiles are switchable on the bare LAN),
            # once, on this first attempt.
            scheduler.grade(conn, session["user_id"], q["id"], bool(is_correct))
    return RedirectResponse(f"/quiz/{session_id}/q/{idx + 1}", status_code=303)


@app.get("/quiz/{session_id}/results", response_class=HTMLResponse)
def quiz_results(request: Request, session_id: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        session = conn.execute("SELECT * FROM quiz_sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            return RedirectResponse("/quiz", status_code=303)
        rows = [dict(r) for r in conn.execute("""
            SELECT sq.question_id AS question_id, q.prompt, q.type, q.answer, q.explanation, q.choices,
                   a.user_answer AS user_answer, a.is_correct AS is_correct,
                   (a.id IS NOT NULL) AS answered
            FROM session_questions sq
            JOIN questions q ON sq.question_id = q.id
            LEFT JOIN answers a ON a.session_id = sq.session_id AND a.question_id = sq.question_id
            WHERE sq.session_id = ? ORDER BY sq.position
        """, (session_id,))]
        correct = sum(1 for r in rows if r["is_correct"])
        conn.execute("UPDATE quiz_sessions SET correct = ?, finished_at = datetime('now') WHERE id = ?",
                     (correct, session_id))
    for r in rows:
        r["choices"] = jloads(r["choices"])
    missed_ids = [r["question_id"] for r in rows if r["answered"] and not r["is_correct"]]
    return render(request, "results.html", session=dict(session), rows=rows,
                  correct=correct, total=len(rows), missed_ids=missed_ids)


@app.post("/quiz/retry-missed")
def quiz_retry_missed(request: Request, question_ids: str = Form(...), label: str = Form("Retry")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    qids = [int(x) for x in question_ids.split(",") if x.strip().isdigit()]
    if not qids:
        return RedirectResponse("/", status_code=303)
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO quiz_sessions (user_id, chapter_ids, label, total) VALUES (?, '[]', ?, ?)",
            (user["id"], f"{label} (missed)", len(qids)))
        session_id = cur.lastrowid
        for pos, qid in enumerate(qids):
            conn.execute(
                "INSERT INTO session_questions (session_id, position, question_id) VALUES (?, ?, ?)",
                (session_id, pos, qid))
    return RedirectResponse(f"/quiz/{session_id}/q/0", status_code=303)


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        sessions = [dict(r) for r in conn.execute("""
            SELECT * FROM quiz_sessions WHERE user_id = ? AND finished_at IS NOT NULL
            ORDER BY finished_at DESC LIMIT 50
        """, (user["id"],))]
    return render(request, "history.html", sessions=sessions)


# --------------------------------------------------------------------------
# Admin analytics  (Phase 3)  +  optional AI review  (Phase 4)
# --------------------------------------------------------------------------
def _question_stats(conn):
    """Per-question performance across all users, grouped by subject/chapter.
    Every row in `answers` is a real attempt now, so no placeholder filtering is
    needed. Returns (subjects, weak) where subjects is a nested structure for
    rendering and weak is the flat list of struggle questions."""
    rows = [dict(r) for r in conn.execute("""
        SELECT s.name AS subject, s.id AS subject_id,
               c.name AS chapter, c.id AS chapter_id, c.position AS cpos,
               q.id AS qid, q.prompt AS prompt, q.type AS type, q.answer AS answer,
               COUNT(a.id) AS attempts,
               COALESCE(SUM(a.is_correct), 0) AS correct
        FROM questions q
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects s ON c.subject_id = s.id
        LEFT JOIN answers a ON a.question_id = q.id
        GROUP BY q.id
        ORDER BY s.name, c.position, c.id, q.id
    """)]
    for r in rows:
        r["pct"] = round(100 * r["correct"] / r["attempts"]) if r["attempts"] else None
        # "Weak" = enough data to trust, and missed more often than not.
        r["weak"] = r["attempts"] >= 3 and r["pct"] is not None and r["pct"] < 60

    subjects = []
    for r in rows:
        if not subjects or subjects[-1]["id"] != r["subject_id"]:
            subjects.append({"id": r["subject_id"], "name": r["subject"], "chapters": []})
        chapters = subjects[-1]["chapters"]
        if not chapters or chapters[-1]["id"] != r["chapter_id"]:
            chapters.append({"id": r["chapter_id"], "name": r["chapter"], "questions": []})
        chapters[-1]["questions"].append(r)

    weak = sorted((r for r in rows if r["weak"]), key=lambda r: r["pct"])
    return subjects, weak


@app.get("/analytics", response_class=HTMLResponse)
def analytics(request: Request):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subjects, weak = _question_stats(conn)
    return render(request, "analytics.html", subjects=subjects, weak=weak, ai_review=None)


@app.post("/analytics/ai-review", response_class=HTMLResponse)
def analytics_ai_review(request: Request):
    """Admin-triggered LLM pass over the struggle questions. The scheduler
    (deterministic SM-2) decides what to show; this is a SEPARATE, optional tool
    that gives qualitative curation advice ('this prompt is ambiguous', 'the
    answer key looks wrong'). Nothing is changed automatically."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subjects, weak = _question_stats(conn)
    ai_review = ai.review_results(weak)
    return render(request, "analytics.html", subjects=subjects, weak=weak, ai_review=ai_review)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
