"""FleetQuiz — a family self-study quiz app.

Server-rendered FastAPI + Jinja2. The whole UI is plain HTML forms so it works
on any device with no build step. Routes are grouped: identity, library
(subjects/chapters/questions), AI generation, and the quiz loop.
"""
import json
import os
import random

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import ai, auth, importer, jobs, scheduler, sources
from .db import get_conn, init_db, jloads
from .importer import import_bank_data


def _safe_back(path):
    """Only allow same-site redirect targets from form fields (no open redirect)."""
    return path if path.startswith("/") and not path.startswith("//") else "/"

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI(title="FleetQuiz")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.on_event("startup")
def _startup():
    init_db()
    jobs.start_worker()


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
    counts = """SELECT s.*,
                   (SELECT COUNT(*) FROM chapters c WHERE c.subject_id = s.id) AS chapter_count,
                   (SELECT COUNT(*) FROM questions q JOIN chapters c ON q.chapter_id = c.id
                      WHERE c.subject_id = s.id) AS question_count
            FROM subjects s"""
    with get_conn() as conn:
        # A user's library is the subjects they've added to their area; the rest
        # are offered under "add to your area".
        enrolled = [dict(r) for r in conn.execute(
            counts + " JOIN user_subjects us ON us.subject_id = s.id AND us.user_id = ?"
            " ORDER BY s.name", (user["id"],))]
        available = [dict(r) for r in conn.execute(
            counts + " WHERE s.id NOT IN (SELECT subject_id FROM user_subjects WHERE user_id = ?)"
            " ORDER BY s.name", (user["id"],))]
        recent = [dict(r) for r in conn.execute("""
            SELECT * FROM quiz_sessions WHERE user_id = ? AND finished_at IS NOT NULL
            ORDER BY finished_at DESC LIMIT 8
        """, (user["id"],))]
    return render(request, "index.html", subjects=enrolled, available=available, recent=recent)


@app.post("/subjects")
def create_subject(request: Request, name: str = Form(...), description: str = Form("")):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO subjects (name, description) VALUES (?, ?)",
                           (name.strip(), description.strip()))
        # The creator gets it in their own area straight away.
        conn.execute("INSERT OR IGNORE INTO user_subjects (user_id, subject_id) VALUES (?, ?)",
                     (user["id"], cur.lastrowid))
    return RedirectResponse("/", status_code=303)


@app.post("/subjects/{subject_id}/enroll")
def enroll_subject(request: Request, subject_id: int):
    """Add a subject to the current user's learning area."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO user_subjects (user_id, subject_id) VALUES (?, ?)",
                     (user["id"], subject_id))
    return RedirectResponse("/", status_code=303)


@app.post("/subjects/{subject_id}/unenroll")
def unenroll_subject(request: Request, subject_id: int):
    """Remove a subject from the current user's learning area (content untouched)."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("DELETE FROM user_subjects WHERE user_id = ? AND subject_id = ?",
                     (user["id"], subject_id))
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
        source_list = sources.list_for_subject(conn, subject_id)
    return render(request, "subject.html", subject=dict(subject), chapters=chapters,
                  sources=source_list, is_admin=bool(user.get("is_admin")))


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
        questions = [dict(r) for r in conn.execute("""
            SELECT q.*, src.title AS source_title, src.kind AS source_kind,
                   src.filename AS source_filename, src.url AS source_url
            FROM questions q LEFT JOIN sources src ON q.source_id = src.id
            WHERE q.chapter_id = ? ORDER BY q.id
        """, (chapter_id,))]
    for q in questions:
        q["choices"] = jloads(q["choices"])
        q["source_label"] = sources.label(
            {"kind": q["source_kind"], "title": q["source_title"],
             "filename": q["source_filename"], "url": q["source_url"]}
        ) if q["source_id"] else ""
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
# Reference material (sources) — provenance a question can be traced back to
# --------------------------------------------------------------------------
@app.post("/subjects/{subject_id}/sources")
async def add_source(request: Request, subject_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    form = await request.form()
    title = (form.get("title") or "").strip()
    url = (form.get("url") or "").strip()
    content = (form.get("content") or "").strip()
    upload = form.get("file")
    with get_conn() as conn:
        # Priority: an uploaded file, else a URL, else pasted text.
        if upload is not None and getattr(upload, "filename", ""):
            data = await upload.read()
            if data:
                sources.save_file(conn, subject_id, title, upload.filename, data)
        elif url:
            sources.create_url(conn, subject_id, title, url)
        elif content:
            sources.create_text(conn, subject_id, title, content)
    return RedirectResponse(f"/subjects/{subject_id}", status_code=303)


@app.post("/sources/{source_id}/delete")
def delete_source(request: Request, source_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        src = sources.get(conn, source_id)
        sources.delete(conn, source_id)
    dest = f"/subjects/{src['subject_id']}" if src and src["subject_id"] else "/"
    return RedirectResponse(dest, status_code=303)


@app.get("/sources/{source_id}")
def view_source(request: Request, source_id: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        src = sources.get(conn, source_id)
    if not src:
        return RedirectResponse("/", status_code=303)
    if src["kind"] == "url":
        return RedirectResponse(src["url"], status_code=303)
    if src["kind"] == "file" and src["file_path"] and os.path.exists(src["file_path"]):
        # Serve by the path stored in the DB (never a user-supplied path).
        # Display inline (PDFs/text render in the browser tab) rather than forcing
        # a download — the point is to eyeball the source while troubleshooting.
        return FileResponse(src["file_path"], content_disposition_type="inline",
                            filename=src["filename"] or "source")
    # Pasted text, or a file whose bytes are gone — show whatever text we have.
    return PlainTextResponse(src["content"] or "(no content)")


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
        source_list = sources.list_for_subject(conn, chapter["subject_id"])
    return render(request, "question_edit.html", chapter=dict(chapter), q=None, sources=source_list)


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
        source_list = sources.list_for_subject(conn, chapter["subject_id"])
    q = dict(q)
    q["choices"] = jloads(q["choices"])
    return render(request, "question_edit.html", chapter=dict(chapter), q=q, sources=source_list)


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
                      answer: str = Form(...), explanation: str = Form(""),
                      source_id: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    p, ch, a, e = _parse_question_form(type, prompt, choices, answer, explanation)
    sid = int(source_id) if source_id.isdigit() else None
    with get_conn() as conn:
        conn.execute("""INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation, source_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""", (chapter_id, type, p, ch, a, e, sid))
    return RedirectResponse(f"/chapters/{chapter_id}", status_code=303)


@app.post("/questions/{question_id}")
def update_question(request: Request, question_id: int, type: str = Form(...),
                    prompt: str = Form(...), choices: str = Form(""),
                    answer: str = Form(...), explanation: str = Form(""),
                    source_id: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    p, ch, a, e = _parse_question_form(type, prompt, choices, answer, explanation)
    sid = int(source_id) if source_id.isdigit() else None
    with get_conn() as conn:
        conn.execute("""UPDATE questions SET type=?, prompt=?, choices=?, answer=?, explanation=?, source_id=?
                        WHERE id=?""", (type, p, ch, a, e, sid, question_id))
        cid = conn.execute("SELECT chapter_id FROM questions WHERE id = ?", (question_id,)).fetchone()
    return RedirectResponse(f"/chapters/{cid['chapter_id']}", status_code=303)


@app.post("/questions/{question_id}/delete")
def delete_question(request: Request, question_id: int, back: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        cid = conn.execute("SELECT chapter_id FROM questions WHERE id = ?", (question_id,)).fetchone()
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    # `back` lets the quiz screens send you somewhere sensible; chapter view is
    # the default for the content-management delete.
    dest = _safe_back(back) if back else (f"/chapters/{cid['chapter_id']}" if cid else "/")
    return RedirectResponse(dest, status_code=303)


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
        source_list = sources.list_for_subject(conn, chapter["subject_id"])
    return render(request, "generate.html", chapter=dict(chapter),
                  ai_base=ai.AI_BASE_URL, ai_model=ai.AI_MODEL, sources=source_list)


@app.post("/chapters/{chapter_id}/generate", response_class=HTMLResponse)
async def generate_run(request: Request, chapter_id: int):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    form = await request.form()
    mode = form.get("mode", "topic")
    topic = form.get("topic", "")
    num_questions = int(form.get("num_questions") or 8)
    difficulty = form.get("difficulty", "medium")
    types = form.getlist("types") or ["mcq", "truefalse", "short"]

    # In source mode, resolve the source the questions are drawn from — an
    # existing one, an inline upload, or pasted text — and save it so every
    # generated question keeps a traceable link to its material.
    source_id, source_text = None, ""
    with get_conn() as conn:
        chapter = dict(conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone())
        if mode == "source":
            existing = form.get("existing_source_id", "")
            upload = form.get("source_file")
            pasted = (form.get("source_text") or "").strip()
            title = (form.get("source_title") or "").strip()
            if existing.isdigit():
                src = sources.get(conn, int(existing))
                if src:
                    source_id, source_text = src["id"], sources.text_for_generation(src)
            elif upload is not None and getattr(upload, "filename", ""):
                data = await upload.read()
                source_id = sources.save_file(conn, chapter["subject_id"], title, upload.filename, data)
                source_text = sources.text_for_generation(sources.get(conn, source_id))
            elif pasted:
                source_id = sources.create_text(conn, chapter["subject_id"], title, pasted)
                source_text = pasted
    # AI call is slow — do it outside the DB connection.
    result = ai.generate_questions(mode, topic, source_text, num_questions, difficulty, types)
    return render(request, "review.html", chapter=chapter, result=result, source_id=source_id)


@app.post("/chapters/{chapter_id}/generate/save")
async def generate_save(request: Request, chapter_id: int):
    """Save the (possibly admin-edited) reviewed questions. The review form posts
    arrays indexed per question; we reconstruct and insert the kept ones."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    form = await request.form()
    n = int(form.get("count", 0))
    sid_raw = form.get("source_id", "")
    sid = int(sid_raw) if sid_raw.isdigit() else None
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
            conn.execute("""INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation, source_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                         (chapter_id, qtype, prompt, json.dumps(choices), answer, explanation, sid))
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
        # Only the user's enrolled subjects are quizzable; chapters are grouped
        # under each so the page can offer a per-subject "select all".
        subject_rows = conn.execute("""
            SELECT s.id, s.name FROM subjects s
            JOIN user_subjects us ON us.subject_id = s.id AND us.user_id = ?
            ORDER BY s.name
        """, (user["id"],)).fetchall()
        groups = []
        for s in subject_rows:
            chapters = [dict(r) for r in conn.execute("""
                SELECT c.*, (SELECT COUNT(*) FROM questions q WHERE q.chapter_id = c.id) AS question_count
                FROM chapters c WHERE c.subject_id = ? ORDER BY c.position, c.id
            """, (s["id"],))]
            for c in chapters:
                # Surface the mastery count right where chapters are picked.
                c["progress"] = scheduler.chapter_progress(conn, user["id"], c["id"])
            groups.append({"id": s["id"], "name": s["name"], "chapters": chapters})
    return render(request, "quiz_setup.html", subjects=groups)


@app.post("/quiz/start")
def quiz_start(request: Request, chapter_ids: list[int] = Form(default=[]),
               num_questions: int = Form(10), order: str = Form("adaptive"),
               endless: str = Form("")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    if not chapter_ids:
        return RedirectResponse("/quiz", status_code=303)
    is_endless = endless == "on"
    placeholders = ",".join("?" for _ in chapter_ids)
    with get_conn() as conn:
        # Endless seeds just the first question; the queue grows on each answer
        # (see quiz_answer). Fixed-length seeds the whole adaptive batch.
        seed_n = 1 if is_endless else num_questions
        qids = scheduler.select_question_ids(conn, user["id"], chapter_ids, seed_n, order)
        if not qids:
            return RedirectResponse("/quiz", status_code=303)
        # Selection stays adaptive (which questions), but for a fixed quiz we
        # shuffle the presentation order so it doesn't always lead with the ones
        # you missed. Endless serves most-due first (one at a time).
        if not is_endless and order == "adaptive":
            random.shuffle(qids)
        names = conn.execute(
            f"SELECT name FROM chapters WHERE id IN ({placeholders})", chapter_ids).fetchall()
        label = ", ".join(n["name"] for n in names)
        if is_endless:
            label += " · endless"
        cur = conn.execute(
            "INSERT INTO quiz_sessions (user_id, chapter_ids, label, total, endless) VALUES (?, ?, ?, ?, ?)",
            (user["id"], json.dumps(chapter_ids), label, len(qids), 1 if is_endless else 0),
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
        if session["finished_at"]:
            return RedirectResponse(f"/quiz/{session_id}/results", status_code=303)
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
        # Endless: once the last queued question is answered, append the next
        # adaptive question (excluding ones already served this session). When the
        # pool is exhausted, nothing is appended and we fall through to results.
        # The append lives here in the POST so GET stays read-only.
        appended = False
        if session["endless"] and not session["finished_at"] and idx == len(qids) - 1:
            nxt = scheduler.select_question_ids(
                conn, session["user_id"], jloads(session["chapter_ids"]), 1, "adaptive",
                exclude=set(qids))
            if nxt:
                conn.execute(
                    "INSERT INTO session_questions (session_id, position, question_id) VALUES (?, ?, ?)",
                    (session_id, len(qids), nxt[0]))
                appended = True
    has_next = (idx + 1) < len(qids) or appended
    # PRG (all targets survive refresh). Get-it-right: don't interrupt — go
    # straight to the next question; the question screen offers a "previous
    # question" button to flag / generate-more on the one just answered. Miss it:
    # stop on the feedback screen so the correct answer is seen.
    if is_correct:
        dest = f"/quiz/{session_id}/q/{idx + 1}" if has_next else f"/quiz/{session_id}/results"
    else:
        dest = f"/quiz/{session_id}/f/{idx}"
    return RedirectResponse(dest, status_code=303)


@app.get("/quiz/{session_id}/f/{idx}", response_class=HTMLResponse)
def quiz_feedback(request: Request, session_id: int, idx: int):
    """On-the-spot feedback after answering: right/wrong, the correct answer and
    explanation, plus flag / generate-more / next / end-quiz actions."""
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
        qid = qids[idx]
        q = dict(conn.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone())
        ans = conn.execute(
            "SELECT * FROM answers WHERE session_id = ? AND question_id = ?",
            (session_id, qid)).fetchone()
        flagged = conn.execute(
            "SELECT 1 FROM question_flags WHERE question_id = ? AND user_id = ? AND resolved_at IS NULL",
            (qid, user["id"])).fetchone() is not None
    q["choices"] = jloads(q["choices"])
    return render(request, "quiz_feedback.html", session=dict(session), q=q,
                  answer=dict(ans) if ans else None, idx=idx, total=len(qids),
                  has_next=(idx + 1) < len(qids), flagged=flagged,
                  is_admin=bool(user.get("is_admin")),
                  queued=request.query_params.get("queued"))


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
        answered = [r for r in rows if r["answered"]]
        correct = sum(1 for r in answered if r["is_correct"])
        # Score on what was actually answered, so ending early / skipping doesn't
        # drag the percentage. Unanswered questions still appear in the review.
        conn.execute("UPDATE quiz_sessions SET correct = ?, total = ?, finished_at = datetime('now') WHERE id = ?",
                     (correct, len(answered), session_id))
    for r in rows:
        r["choices"] = jloads(r["choices"])
    # Sort wrong-first: answered-incorrect, then answered-correct, then unanswered.
    # Python's sort is stable, so position order is preserved within each group.
    rows.sort(key=lambda r: (2 if not r["answered"] else (0 if not r["is_correct"] else 1)))
    missed_ids = [r["question_id"] for r in rows if r["answered"] and not r["is_correct"]]
    unanswered = sum(1 for r in rows if not r["answered"])
    is_admin = bool(user.get("is_admin"))
    with get_conn() as conn:
        flagged_ids = {r["question_id"] for r in conn.execute(
            "SELECT question_id FROM question_flags WHERE user_id = ? AND resolved_at IS NULL",
            (user["id"],))}
        pending_review = conn.execute(
            "SELECT COUNT(*) n FROM proposals WHERE status = 'pending'").fetchone()["n"] if is_admin else 0
        active_jobs = conn.execute(
            "SELECT COUNT(*) n FROM jobs WHERE status IN ('pending','running')").fetchone()["n"] if is_admin else 0
    return render(request, "results.html", session=dict(session), rows=rows,
                  correct=correct, total=len(answered), unanswered=unanswered,
                  missed_ids=missed_ids, is_admin=is_admin, flagged_ids=flagged_ids,
                  pending_review=pending_review, active_jobs=active_jobs,
                  queued=request.query_params.get("queued"))


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


# --------------------------------------------------------------------------
# Per-question actions: flag for review  +  generate more like this
# --------------------------------------------------------------------------
@app.post("/questions/{question_id}/flag")
def flag_question(request: Request, question_id: int,
                  back: str = Form("/"), note: str = Form("")):
    """Toggle a review flag for the current user on this question (flag if not
    flagged, unflag if already flagged). One active flag per person per question;
    surfaced to the admin in Analytics."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        active = conn.execute(
            "SELECT id FROM question_flags WHERE question_id = ? AND user_id = ? AND resolved_at IS NULL",
            (question_id, user["id"])).fetchone()
        if active:
            conn.execute("UPDATE question_flags SET resolved_at = datetime('now') WHERE id = ?",
                         (active["id"],))
            flagged_on = False
        else:
            conn.execute(
                """INSERT INTO question_flags (question_id, user_id, note) VALUES (?, ?, ?)
                   ON CONFLICT(question_id, user_id) DO UPDATE SET
                       resolved_at = NULL, created_at = datetime('now'), note = excluded.note""",
                (question_id, user["id"], note.strip()))
            flagged_on = True
    if flagged_on:
        # Kick off a background "verify & propose a fix" pass (deduped per question).
        jobs.enqueue("flag_fix", user["id"], question_id)
    return RedirectResponse(_safe_back(back), status_code=303)


@app.post("/questions/{question_id}/flag/resolve")
def resolve_flag(request: Request, question_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute(
            "UPDATE question_flags SET resolved_at = datetime('now') "
            "WHERE question_id = ? AND resolved_at IS NULL", (question_id,))
    return RedirectResponse("/analytics", status_code=303)


@app.post("/questions/{question_id}/master")
def master_question(request: Request, question_id: int, back: str = Form("/")):
    """Mark a question 'mastered' for the current user — an 'it's too easy' button.
    Per-user (just suppresses it from your own future quizzes), so any profile may
    do it; nothing about the question itself changes."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        scheduler.mark_mastered(conn, user["id"], question_id)
    return RedirectResponse(_safe_back(back), status_code=303)


@app.post("/questions/{question_id}/generate-more")
def generate_more(request: Request, question_id: int, back: str = Form("/")):
    """Admin-only: queue a background job that seeds the LLM (with web search +
    the chapter's knowledge base) from this question and PROPOSES ~5 similar ones.
    Non-blocking — keep quizzing; approve the proposals on the Review page."""
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    jobs.enqueue("generate_more", user["id"], question_id)
    dest = _safe_back(back)
    sep = "&" if "?" in dest else "?"
    return RedirectResponse(f"{dest}{sep}queued=1", status_code=303)


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
               q.source_id AS source_id, src.title AS source_title, src.kind AS source_kind,
               src.filename AS source_filename, src.url AS source_url,
               COUNT(a.id) AS attempts,
               COALESCE(SUM(a.is_correct), 0) AS correct
        FROM questions q
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects s ON c.subject_id = s.id
        LEFT JOIN answers a ON a.question_id = q.id
        LEFT JOIN sources src ON q.source_id = src.id
        GROUP BY q.id
        ORDER BY s.name, c.position, c.id, q.id
    """)]
    for r in rows:
        r["source_label"] = sources.label(
            {"kind": r["source_kind"], "title": r["source_title"],
             "filename": r["source_filename"], "url": r["source_url"]}
        ) if r["source_id"] else ""
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


def _flagged_questions(conn):
    """Questions with at least one unresolved user flag, for admin review."""
    return [dict(r) for r in conn.execute("""
        SELECT q.id AS qid, q.prompt, q.type, c.name AS chapter,
               COUNT(f.id) AS flags,
               GROUP_CONCAT(NULLIF(f.note, ''), ' · ') AS notes
        FROM question_flags f
        JOIN questions q ON f.question_id = q.id
        JOIN chapters c ON q.chapter_id = c.id
        WHERE f.resolved_at IS NULL
        GROUP BY q.id
        ORDER BY flags DESC, q.id
    """)]


@app.get("/analytics", response_class=HTMLResponse)
def analytics(request: Request):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        subjects, weak = _question_stats(conn)
        flagged = _flagged_questions(conn)
    return render(request, "analytics.html", subjects=subjects, weak=weak,
                  flagged=flagged, ai_review=None)


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
        flagged = _flagged_questions(conn)
    ai_review = ai.review_results(weak)
    return render(request, "analytics.html", subjects=subjects, weak=weak,
                  flagged=flagged, ai_review=ai_review)


# --------------------------------------------------------------------------
# Review queue (admin) — approve/reject LLM proposals (generate-more, flag-fix)
# --------------------------------------------------------------------------
@app.get("/review", response_class=HTMLResponse)
def review(request: Request):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        proposals = [dict(r) for r in conn.execute("""
            SELECT p.*, c.name AS chapter_name, j.kind AS job_kind,
                   q.prompt AS cur_prompt, q.choices AS cur_choices, q.answer AS cur_answer,
                   q.explanation AS cur_explanation, q.type AS cur_type
            FROM proposals p
            JOIN chapters c ON p.chapter_id = c.id
            LEFT JOIN jobs j ON p.job_id = j.id
            LEFT JOIN questions q ON p.question_id = q.id
            WHERE p.status = 'pending'
            ORDER BY p.created_at, p.id
        """)]
        for p in proposals:
            p["choices"] = jloads(p["choices"])
            p["cur_choices"] = jloads(p["cur_choices"]) if p["cur_choices"] else []
        recent_jobs = [dict(r) for r in conn.execute("""
            SELECT j.*, q.prompt AS qprompt
            FROM jobs j LEFT JOIN questions q ON j.question_id = q.id
            ORDER BY j.id DESC LIMIT 25
        """)]
    return render(request, "review_queue.html", proposals=proposals, jobs=recent_jobs)


@app.post("/proposals/{pid}/approve")
def approve_proposal(request: Request, pid: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        p = conn.execute("SELECT * FROM proposals WHERE id = ? AND status = 'pending'", (pid,)).fetchone()
        if not p:
            return RedirectResponse("/review", status_code=303)
        p = dict(p)
        # Re-validate the proposal like any untrusted generated question.
        norm, _reason = importer._normalise({
            "type": p["type"], "prompt": p["prompt"], "choices": jloads(p["choices"]),
            "answer": p["answer"], "explanation": p["explanation"]})
        if not norm:
            conn.execute("UPDATE proposals SET status = 'rejected' WHERE id = ?", (pid,))
            return RedirectResponse("/review", status_code=303)
        if p["kind"] == "add":
            conn.execute(
                """INSERT INTO questions (chapter_id, type, prompt, choices, answer, explanation, source_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (p["chapter_id"], norm["type"], norm["prompt"], json.dumps(norm["choices"]),
                 norm["answer"], norm["explanation"], p["source_id"]))
        else:  # edit — apply only if the original question still exists
            if conn.execute("SELECT 1 FROM questions WHERE id = ?", (p["question_id"],)).fetchone():
                conn.execute(
                    """UPDATE questions SET type = ?, prompt = ?, choices = ?, answer = ?, explanation = ?
                       WHERE id = ?""",
                    (norm["type"], norm["prompt"], json.dumps(norm["choices"]), norm["answer"],
                     norm["explanation"], p["question_id"]))
        conn.execute("UPDATE proposals SET status = 'approved' WHERE id = ?", (pid,))
    return RedirectResponse("/review", status_code=303)


@app.post("/proposals/{pid}/reject")
def reject_proposal(request: Request, pid: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("UPDATE proposals SET status = 'rejected' WHERE id = ? AND status = 'pending'", (pid,))
    return RedirectResponse("/review", status_code=303)


# --------------------------------------------------------------------------
# Knowledge import  (admin only) — bulk-load a question-bank JSON
# --------------------------------------------------------------------------
# Admin-gated like every other mutation. This is no more privileged than the
# existing AI-generate / delete routes; the hard network boundary (LAN / SSO)
# remains the reverse proxy's job — see the README security model.
@app.get("/import", response_class=HTMLResponse)
def import_form(request: Request):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    return render(request, "import.html", result=None, error=None)


@app.post("/import", response_class=HTMLResponse)
async def import_run(request: Request):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    form = await request.form()
    upload = form.get("file")
    raw = None
    if upload is not None and getattr(upload, "filename", ""):
        raw = await upload.read()
    elif (form.get("json") or "").strip():
        raw = form.get("json").encode("utf-8")
    if not raw:
        return render(request, "import.html", result=None,
                      error="Upload a bank JSON file or paste JSON.")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return render(request, "import.html", result=None, error=f"Invalid JSON: {e}")
    try:
        result = import_bank_data(data)
    except (KeyError, TypeError) as e:
        return render(request, "import.html", result=None,
                      error=f"Bad bank structure (need subject + chapters): {e}")
    return render(request, "import.html", result=result, error=None)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
