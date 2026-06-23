"""FleetQuiz — a family self-study quiz app.

Server-rendered FastAPI + Jinja2. The whole UI is plain HTML forms so it works
on any device with no build step. Routes are grouped: identity, library
(an arbitrary-depth node tree + per-person collections), questions, AI
generation, and the quiz loop.
"""
import json
import os
import random
from datetime import date, datetime, timedelta, timezone
from urllib.parse import quote, urlencode

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import (FileResponse, HTMLResponse, JSONResponse,
                               PlainTextResponse, RedirectResponse)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import ai, auth, db, importer, jobs, scheduler, sources, version
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
    info = auth.resolve(request)
    ctx.setdefault("user", info["effective"])
    ctx.setdefault("acting", info["acting"])
    ctx.setdefault("real_user", info["real"])
    ctx.setdefault("app_version", version.VERSION)
    ctx["request"] = request
    return templates.TemplateResponse(template, ctx)


def require_user(request):
    """Returns user dict or a RedirectResponse to the picker."""
    user = auth.current_user(request)
    if not user:
        return None, RedirectResponse("/cdn-cgi/access/logout", status_code=303)
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
        return None, RedirectResponse("/cdn-cgi/access/logout", status_code=303)
    if not user.get("is_admin"):
        return None, render(request, "forbidden.html", user=user)
    return user, None


# --------------------------------------------------------------------------
# Identity
# --------------------------------------------------------------------------
# Identity is established by Cloudflare Access (trusted email header) in front of
# the app — see auth.py. There is deliberately no in-app profile picker / switcher:
# behind the tunnel the CF header always wins over any cookie, so a picker can only
# mislead. New profiles are created from the Admin console; an admin views a child's
# account via Admin → "Act as". To change *who you are*, log out of Cloudflare.
@app.get("/logout")
def logout():
    """Real logout = ending the Cloudflare Access session. Clear our own cookies
    (so any 'act as' is dropped), then hand off to Cloudflare's edge logout
    endpoint, which re-prompts the CF login on the next visit. On a bare-LAN hit
    with no CF Access in front, the cookie clear is the meaningful part and the
    redirect simply 404s harmlessly."""
    resp = RedirectResponse("/cdn-cgi/access/logout", status_code=303)
    resp.delete_cookie(auth.COOKIE_NAME)
    resp.delete_cookie(auth.ACT_COOKIE)
    return resp


# --------------------------------------------------------------------------
# Dashboard + library
# --------------------------------------------------------------------------
def _study_streak(days: set) -> int:
    """Consecutive calendar days (UTC) ending today with at least one finished
    quiz. A quiz today *or* yesterday keeps the streak alive; the first gap ends
    it. Bucketed on the same UTC date the rest of the app displays."""
    if not days:
        return 0
    today = datetime.now(timezone.utc).date()
    cur = today if today in days else today - timedelta(days=1)
    if cur not in days:
        return 0
    streak = 0
    while cur in days:
        streak += 1
        cur -= timedelta(days=1)
    return streak


# --- node-tree view helpers ----------------------------------------------

def _node_card(conn, node):
    """Decorate a node row (dict-able) with subtree rollups for a listing card:
    question_count (whole subtree) and child_count (descendant nodes)."""
    ids = db.subtree_ids(conn, [node["id"]])
    ph = ",".join("?" for _ in ids)
    qn = conn.execute(
        f"SELECT COUNT(*) AS n FROM questions WHERE chapter_id IN ({ph})", ids).fetchone()["n"]
    d = dict(node)
    d["question_count"] = qn
    d["child_count"] = len(ids) - 1
    return d


def _root_topics(conn):
    """All root topics (parent_id IS NULL), each decorated with subtree counts."""
    rows = conn.execute(
        "SELECT * FROM chapters WHERE parent_id IS NULL ORDER BY name").fetchall()
    return [_node_card(conn, r) for r in rows]


def _user_collections(conn, user_id):
    """A user's collections, each with its member nodes decorated as cards."""
    colls = conn.execute(
        "SELECT * FROM collections WHERE user_id = ? ORDER BY name", (user_id,)).fetchall()
    out = []
    for c in colls:
        members = conn.execute(
            """SELECT ch.* FROM collection_nodes cn JOIN chapters ch ON ch.id = cn.node_id
               WHERE cn.collection_id = ? ORDER BY cn.position, ch.name""", (c["id"],)).fetchall()
        out.append({**dict(c), "nodes": [_node_card(conn, m) for m in members]})
    return out


def _node_children(conn, parent_id, user_id):
    """Immediate children of a node, each with a subtree question count and the
    per-user mastery rollup for its badge."""
    rows = conn.execute(
        "SELECT * FROM chapters WHERE parent_id = ? ORDER BY position, id", (parent_id,)).fetchall()
    out = []
    for r in rows:
        card = _node_card(conn, r)
        card["progress"] = scheduler.chapter_progress(conn, user_id, r["id"])
        out.append(card)
    return out


def _node_ancestors(conn, node_id):
    """Breadcrumb trail from root → node (inclusive), ordered root-first."""
    rows = conn.execute("""
        WITH RECURSIVE anc(id, parent_id, name, depth) AS (
            SELECT id, parent_id, name, 0 FROM chapters WHERE id = ?
            UNION ALL
            SELECT c.id, c.parent_id, c.name, anc.depth + 1
            FROM chapters c JOIN anc ON c.id = anc.parent_id
        )
        SELECT id, name FROM anc ORDER BY depth DESC
    """, (node_id,)).fetchall()
    return [dict(r) for r in rows]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Home dashboard: what to do next and how you're doing. Subject management
    lives on /library."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        recent = [dict(r) for r in conn.execute("""
            SELECT * FROM quiz_sessions WHERE user_id = ? AND finished_at IS NOT NULL
            ORDER BY finished_at DESC LIMIT 8
        """, (user["id"],))]
        totals = conn.execute("""
            SELECT COUNT(*) AS quizzes, COALESCE(SUM(correct), 0) AS correct,
                   COALESCE(SUM(total), 0) AS answered
            FROM quiz_sessions WHERE user_id = ? AND finished_at IS NOT NULL
        """, (user["id"],)).fetchone()
        days = [r[0] for r in conn.execute(
            "SELECT DISTINCT substr(finished_at, 1, 10) FROM quiz_sessions "
            "WHERE user_id = ? AND finished_at IS NOT NULL", (user["id"],))]
        has_content = conn.execute(
            """SELECT 1 FROM collection_nodes cn JOIN collections c ON c.id = cn.collection_id
               WHERE c.user_id = ? LIMIT 1""", (user["id"],)).fetchone()
    summary = dict(totals)
    summary["pct"] = (round(summary["correct"] / summary["answered"] * 100)
                      if summary["answered"] else None)
    streak = _study_streak({date.fromisoformat(d) for d in days})
    return render(request, "home.html", recent=recent, summary=summary,
                  streak=streak, has_subjects=bool(has_content))


@app.get("/library", response_class=HTMLResponse)
def library(request: Request):
    """Study material: the learner's collections (personal bundles of topics/nodes)
    plus every root topic, for browsing and — for admins — curation."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        collections = _user_collections(conn, user["id"])
        topics = _root_topics(conn)
    return render(request, "library.html", collections=collections, topics=topics,
                  is_admin=bool(user.get("is_admin")))


# --------------------------------------------------------------------------
# Collections — a learner's personal, named bundles of nodes, cross-cutting the
# strict content tree (the same node can sit in several collections). Replaces
# the old flat per-user enrollment.
# --------------------------------------------------------------------------
@app.post("/collections")
def create_collection(request: Request, name: str = Form(...)):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    name = name.strip()
    if name:
        with get_conn() as conn:
            conn.execute("INSERT INTO collections (user_id, name) VALUES (?, ?)",
                         (user["id"], name))
    return RedirectResponse("/library", status_code=303)


@app.post("/collections/{cid}/delete")
def delete_collection(request: Request, cid: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:  # owner-scoped: only your own collection
        conn.execute("DELETE FROM collections WHERE id = ? AND user_id = ?", (cid, user["id"]))
    return RedirectResponse("/library", status_code=303)


@app.post("/collections/{cid}/nodes")
def add_collection_node(request: Request, cid: int, node_id: int = Form(...),
                        back: str = Form("/library")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        if conn.execute("SELECT 1 FROM collections WHERE id = ? AND user_id = ?",
                        (cid, user["id"])).fetchone():
            conn.execute(
                "INSERT OR IGNORE INTO collection_nodes (collection_id, node_id) VALUES (?, ?)",
                (cid, node_id))
    return RedirectResponse(_safe_back(back), status_code=303)


@app.post("/collections/{cid}/nodes/{node_id}/delete")
def remove_collection_node(request: Request, cid: int, node_id: int,
                           back: str = Form("/library")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        if conn.execute("SELECT 1 FROM collections WHERE id = ? AND user_id = ?",
                        (cid, user["id"])).fetchone():
            conn.execute("DELETE FROM collection_nodes WHERE collection_id = ? AND node_id = ?",
                         (cid, node_id))
    return RedirectResponse(_safe_back(back), status_code=303)


# --------------------------------------------------------------------------
# Content tree — arbitrary-depth nodes. A root node (parent_id NULL) is a
# "topic"; any node may hold child nodes AND/OR questions. Selecting a node for
# a quiz sweeps its whole subtree (see scheduler).
# --------------------------------------------------------------------------
@app.post("/topics")
def create_topic(request: Request, name: str = Form(...), description: str = Form("")):
    """Admin: create a new root topic and drop it into the creator's library."""
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    name = name.strip()
    if not name:
        return RedirectResponse("/library", status_code=303)
    with get_conn() as conn:
        node_id = conn.execute(
            "INSERT INTO chapters (parent_id, name, description) VALUES (NULL, ?, ?)",
            (name, description.strip())).lastrowid
        coll = conn.execute(
            "SELECT id FROM collections WHERE user_id = ? ORDER BY id LIMIT 1", (user["id"],)).fetchone()
        coll_id = coll["id"] if coll else conn.execute(
            "INSERT INTO collections (user_id, name) VALUES (?, 'My Library')", (user["id"],)).lastrowid
        conn.execute("INSERT OR IGNORE INTO collection_nodes (collection_id, node_id) VALUES (?, ?)",
                     (coll_id, node_id))
    return RedirectResponse(f"/nodes/{node_id}", status_code=303)


@app.post("/nodes/{parent_id}/children")
def create_child(request: Request, parent_id: int, name: str = Form(...), position: int = Form(0)):
    """Admin: add a child node under any node (nesting is unlimited)."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    name = name.strip()
    if name:
        with get_conn() as conn:
            if conn.execute("SELECT 1 FROM chapters WHERE id = ?", (parent_id,)).fetchone():
                conn.execute("INSERT INTO chapters (parent_id, name, position) VALUES (?, ?, ?)",
                             (parent_id, name, position))
    return RedirectResponse(f"/nodes/{parent_id}", status_code=303)


@app.post("/nodes/{node_id}/move")
def move_node(request: Request, node_id: int, parent_id: str = Form("")):
    """Admin: re-parent a node. Empty/0 parent makes it a root topic. Rejects a
    move into the node's own subtree — that would create a cycle."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    new_parent = int(parent_id) if str(parent_id).strip() not in ("", "0") else None
    with get_conn() as conn:
        if new_parent is not None and (
                new_parent == node_id or db.is_descendant(conn, new_parent, node_id)):
            return RedirectResponse(f"/nodes/{node_id}?move_error=1", status_code=303)
        conn.execute("UPDATE chapters SET parent_id = ? WHERE id = ?", (new_parent, node_id))
    return RedirectResponse(f"/nodes/{node_id}", status_code=303)


@app.post("/nodes/{node_id}/delete")
def delete_node(request: Request, node_id: int):
    """Admin: delete a node and its whole subtree (ON DELETE CASCADE)."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        parent = conn.execute("SELECT parent_id FROM chapters WHERE id = ?", (node_id,)).fetchone()
        conn.execute("DELETE FROM chapters WHERE id = ?", (node_id,))
    dest = f"/nodes/{parent['parent_id']}" if parent and parent["parent_id"] else "/library"
    return RedirectResponse(dest, status_code=303)


@app.get("/nodes/{node_id}", response_class=HTMLResponse)
def view_node(request: Request, node_id: int):
    """Unified node page: breadcrumb, child nodes, questions on this node, and (at
    the topic root) reference sources + teaching notes."""
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM chapters WHERE id = ?", (node_id,)).fetchone()
        if not row:
            return RedirectResponse("/library", status_code=303)
        node = dict(row)
        ancestors = _node_ancestors(conn, node_id)
        children = _node_children(conn, node_id, user["id"])
        questions = [dict(r) for r in conn.execute("""
            SELECT q.*, src.title AS source_title, src.kind AS source_kind,
                   src.filename AS source_filename, src.url AS source_url
            FROM questions q LEFT JOIN sources src ON q.source_id = src.id
            WHERE q.chapter_id = ? ORDER BY q.id
        """, (node_id,))]
        root_id = db.node_root_id(conn, node_id)
        source_list = sources.list_for_subject(conn, root_id) if root_id else []
        progress = scheduler.chapter_progress(conn, user["id"], node_id)
        my_collections = [dict(r) for r in conn.execute(
            "SELECT id, name FROM collections WHERE user_id = ? ORDER BY name", (user["id"],))]
        move_targets = []
        if user.get("is_admin"):  # candidate parents = every node outside this subtree
            subtree = set(db.subtree_ids(conn, [node_id]))
            move_targets = [dict(r) for r in conn.execute(
                "SELECT id, name, parent_id FROM chapters ORDER BY name")
                if r["id"] not in subtree]
    for q in questions:
        q["choices"] = jloads(q["choices"])
        q["source_label"] = sources.label(
            {"kind": q["source_kind"], "title": q["source_title"],
             "filename": q["source_filename"], "url": q["source_url"]}
        ) if q["source_id"] else ""
    return render(request, "node.html", node=node, ancestors=ancestors, children=children,
                  questions=questions, sources=source_list, progress=progress,
                  is_root=node["parent_id"] is None, move_targets=move_targets,
                  my_collections=my_collections, is_admin=bool(user.get("is_admin")))


# Back-compat redirects for old subject/chapter URLs (history, bookmarks).
@app.get("/subjects/{node_id}")
def _old_subject_url(node_id: int):
    return RedirectResponse(f"/nodes/{node_id}", status_code=307)


@app.get("/chapters/{node_id}")
def _old_chapter_url(node_id: int):
    return RedirectResponse(f"/nodes/{node_id}", status_code=307)


# --------------------------------------------------------------------------
# Reference material (sources) — provenance a question can be traced back to
# --------------------------------------------------------------------------
@app.post("/nodes/{node_id}/sources")
async def add_source(request: Request, node_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    form = await request.form()
    title = (form.get("title") or "").strip()
    url = (form.get("url") or "").strip()
    content = (form.get("content") or "").strip()
    upload = form.get("file")
    with get_conn() as conn:
        # Sources live at the topic (root) level so they're shared across the whole
        # subtree; a node anywhere in the tree resolves up to its root.
        root_id = db.node_root_id(conn, node_id)
        # Priority: an uploaded file, else a URL, else pasted text.
        if upload is not None and getattr(upload, "filename", ""):
            data = await upload.read()
            if data:
                sources.save_file(conn, root_id, title, upload.filename, data)
        elif url:
            sources.create_url(conn, root_id, title, url)
        elif content:
            sources.create_text(conn, root_id, title, content)
    return RedirectResponse(f"/nodes/{node_id}", status_code=303)


@app.post("/sources/{source_id}/delete")
def delete_source(request: Request, source_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        src = sources.get(conn, source_id)
        sources.delete(conn, source_id)
    dest = f"/nodes/{src['subject_id']}" if src and src["subject_id"] else "/library"
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
@app.get("/nodes/{node_id}/questions/new", response_class=HTMLResponse)
def new_question(request: Request, node_id: int):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (node_id,)).fetchone()
        source_list = sources.list_for_subject(conn, db.node_root_id(conn, node_id))
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
        source_list = sources.list_for_subject(conn, db.node_root_id(conn, q["chapter_id"]))
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


@app.post("/nodes/{node_id}/questions")
def save_new_question(request: Request, node_id: int, type: str = Form(...),
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
                        VALUES (?, ?, ?, ?, ?, ?, ?)""", (node_id, type, p, ch, a, e, sid))
    return RedirectResponse(f"/nodes/{node_id}", status_code=303)


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
    return RedirectResponse(f"/nodes/{cid['chapter_id']}", status_code=303)


@app.post("/questions/{question_id}/delete")
def delete_question(request: Request, question_id: int, back: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        cid = conn.execute("SELECT chapter_id FROM questions WHERE id = ?", (question_id,)).fetchone()
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    # `back` lets the quiz screens send you somewhere sensible; the node view is
    # the default for the content-management delete.
    dest = _safe_back(back) if back else (f"/nodes/{cid['chapter_id']}" if cid else "/")
    return RedirectResponse(dest, status_code=303)


# --------------------------------------------------------------------------
# AI generation  ->  review  ->  bulk save
# --------------------------------------------------------------------------
@app.get("/nodes/{node_id}/generate", response_class=HTMLResponse)
def generate_form(request: Request, node_id: int):
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (node_id,)).fetchone()
        source_list = sources.list_for_subject(conn, db.node_root_id(conn, node_id))
    return render(request, "generate.html", chapter=dict(chapter),
                  ai_base=ai.AI_BASE_URL, ai_model=ai.AI_MODEL, sources=source_list)


@app.post("/nodes/{node_id}/generate", response_class=HTMLResponse)
async def generate_run(request: Request, node_id: int):
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
        chapter = dict(conn.execute("SELECT * FROM chapters WHERE id = ?", (node_id,)).fetchone())
        root_id = db.node_root_id(conn, node_id)
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
                source_id = sources.save_file(conn, root_id, title, upload.filename, data)
                source_text = sources.text_for_generation(sources.get(conn, source_id))
            elif pasted:
                source_id = sources.create_text(conn, root_id, title, pasted)
                source_text = pasted
    # AI call is slow — do it outside the DB connection.
    result = ai.generate_questions(mode, topic, source_text, num_questions, difficulty, types)
    return render(request, "review.html", chapter=chapter, result=result, source_id=source_id)


@app.post("/nodes/{node_id}/generate/save")
async def generate_save(request: Request, node_id: int):
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
                         (node_id, qtype, prompt, json.dumps(choices), answer, explanation, sid))
            saved += 1
    return RedirectResponse(f"/nodes/{node_id}?saved={saved}", status_code=303)


# --------------------------------------------------------------------------
# Quiz loop
# --------------------------------------------------------------------------
def _quiz_tree(conn, node_id, user_id):
    """Nested, quizzable view of a node's subtree: each node carries its subtree
    question_count, mastery progress, and children. Nodes whose subtree has no
    questions are pruned (nothing to quiz). Picking any node quizzes its subtree."""
    ids = db.subtree_ids(conn, [node_id])
    ph = ",".join("?" for _ in ids)
    qcount = conn.execute(
        f"SELECT COUNT(*) AS n FROM questions WHERE chapter_id IN ({ph})", ids).fetchone()["n"]
    if qcount == 0:
        return None
    row = conn.execute("SELECT id, name FROM chapters WHERE id = ?", (node_id,)).fetchone()
    children = []
    for ch in conn.execute(
            "SELECT id FROM chapters WHERE parent_id = ? ORDER BY position, id", (node_id,)):
        sub = _quiz_tree(conn, ch["id"], user_id)
        if sub:
            children.append(sub)
    return {"id": row["id"], "name": row["name"], "question_count": qcount,
            "progress": scheduler.chapter_progress(conn, user_id, node_id),
            "children": children}


@app.get("/quiz", response_class=HTMLResponse)
def quiz_setup(request: Request):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        # Quizzable scope = the nodes in the learner's collections, each shown as a
        # tree so any node (and its whole subtree) can be picked.
        colls = conn.execute(
            "SELECT id, name FROM collections WHERE user_id = ? ORDER BY name", (user["id"],)).fetchall()
        groups = []
        for c in colls:
            members = conn.execute(
                """SELECT ch.id FROM collection_nodes cn JOIN chapters ch ON ch.id = cn.node_id
                   WHERE cn.collection_id = ? ORDER BY cn.position, ch.name""", (c["id"],)).fetchall()
            trees = [t for t in (_quiz_tree(conn, m["id"], user["id"]) for m in members) if t]
            if trees:
                groups.append({"id": c["id"], "name": c["name"], "nodes": trees})
    return render(request, "quiz_setup.html", collections=groups)


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
                answer: str = Form(""), self_correct: str = Form(""),
                dont_know: str = Form("")):
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
        if dont_know == "1":
            # "I don't know": grade as a miss outright — no guess, no chance of an
            # accidental correct. Routes to the feedback screen (correct answer +
            # explanation) like any other miss.
            is_correct = 0
            user_answer = answer.strip()
        elif q["type"] == "short":
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
                # Append AFTER the highest existing position, not at len(qids):
                # deleting a question mid-session cascade-removes its row and
                # leaves a hole, so len(qids) can collide with a surviving
                # position. MAX(position)+1 stays unique regardless of holes.
                next_pos = conn.execute(
                    "SELECT COALESCE(MAX(position), -1) + 1 FROM session_questions WHERE session_id = ?",
                    (session_id,)).fetchone()[0]
                conn.execute(
                    "INSERT INTO session_questions (session_id, position, question_id) VALUES (?, ?, ?)",
                    (session_id, next_pos, nxt[0]))
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
    # htmx fast path: render the destination screen in THIS response instead of
    # bouncing through a 303 + follow-up GET. The grading transaction above has
    # already committed (the `with` block closed), so reusing the GET view here
    # sees the just-recorded answer. htmx hx-selects #quiz-stage out of the page;
    # HX-Push-Url keeps the address bar (and refresh/back) on a real URL. Non-htmx
    # clients fall through to the classic PRG redirect — the no-JS path and the
    # browser-back resubmit handling above both depend on that staying put.
    if request.headers.get("HX-Request") == "true":
        if is_correct and has_next:
            resp = quiz_question(request, session_id, idx + 1)
        elif is_correct:
            resp = quiz_results(request, session_id)
        else:
            resp = quiz_feedback(request, session_id, idx)
        resp.headers["HX-Push-Url"] = dest
        return resp
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


# --------------------------------------------------------------------------
# Tutor — a grounded, per-question chat that explains the answer or the topic.
# Thin generic system prompt; the per-subject teaching notes + chapter KB do the
# steering (see ai.TUTOR_SYSTEM). LLM calls happen OUTSIDE any open connection.
# --------------------------------------------------------------------------
TUTOR_HISTORY_LIMIT = 16  # messages of context sent to the model
TUTOR_INTENTS = {
    "why_wrong": "I got this question wrong. Why is my answer not right, and how "
                 "should I think about it?",
    "teach": "Can you teach me about this topic?",
}


def _tutor_context_row(conn, question_id):
    row = conn.execute("""
        SELECT q.id, q.type, q.prompt, q.answer, q.explanation,
               c.id AS chapter_id, c.name AS chapter,
               src.content AS kb
        FROM questions q
        JOIN chapters c ON q.chapter_id = c.id
        LEFT JOIN sources src ON q.source_id = src.id
        WHERE q.id = ?""", (question_id,)).fetchone()
    if not row:
        return None
    d = dict(row)
    # "Subject" + teaching notes come from the question's root topic; the chapter
    # is the node it's filed under (which may be nested several levels deep).
    root_id = db.node_root_id(conn, d["chapter_id"])
    root = conn.execute("SELECT name, teaching_notes FROM chapters WHERE id = ?",
                        (root_id,)).fetchone() if root_id else None
    d["subject"] = root["name"] if root else d["chapter"]
    d["notes"] = root["teaching_notes"] if root else ""
    return d


def _tutor_context_block(ctx, learner_answer=None):
    kb = (ctx.get("kb") or "").strip()
    if len(kb) > ai.TUTOR_KB_CHARS:
        kb = kb[:ai.TUTOR_KB_CHARS] + "\n…(material truncated)"
    notes = (ctx.get("notes") or "").strip() or \
        "(none provided — judge the right level from the subject and topic names)"
    parts = [
        f"LEARNER NOTES (how to teach this person): {notes}",
        f"SUBJECT: {ctx['subject']}",
        f"TOPIC (chapter): {ctx['chapter']}",
        f"STUDY MATERIAL:\n{kb or '(none)'}",
        f"THE QUESTION THEY ARE WORKING ON:\n{ctx['prompt']}\nCorrect answer: "
        f"{ctx['answer']}" + (f"\nExplanation: {ctx['explanation']}"
                              if ctx['explanation'] else ""),
    ]
    if learner_answer:
        parts.append(f"The learner's answer was: {learner_answer!r} — which is INCORRECT.")
    return "\n\n".join(parts)


def _tutor_call(block, history, user_message):
    """Run one tutor turn, degrading to a friendly message on any failure so the
    chat thread stays consistent."""
    try:
        return ai.tutor(block, history[-TUTOR_HISTORY_LIMIT:], user_message) \
            or "(The tutor didn't say anything — try asking again.)"
    except Exception:  # noqa: BLE001 - connection/HTTP/parse all degrade the same
        return "I couldn't reach the tutor right now. Please try again in a moment."


def _store_tutor(conn, user_id, qid, user_msg, assistant_msg):
    conn.execute("INSERT INTO tutor_messages (user_id, question_id, role, content) "
                 "VALUES (?, ?, 'user', ?)", (user_id, qid, user_msg))
    conn.execute("INSERT INTO tutor_messages (user_id, question_id, role, content) "
                 "VALUES (?, ?, 'assistant', ?)", (user_id, qid, assistant_msg))


def _tutor_url(question_id, back=""):
    url = f"/tutor/{question_id}"
    b = _safe_back(back) if back else ""
    if b and b != "/":
        url += "?back=" + quote(b, safe="/")
    return url


@app.post("/nodes/{node_id}/teaching-notes")
def save_teaching_notes(request: Request, node_id: int,
                        teaching_notes: str = Form(""), back: str = Form("")):
    """Admin: free-text notes that steer the tutor's level/tone for this topic."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("UPDATE chapters SET teaching_notes = ? WHERE id = ?",
                     (teaching_notes.strip(), node_id))
    return RedirectResponse(_safe_back(back) if back else f"/nodes/{node_id}",
                            status_code=303)


@app.post("/questions/{question_id}/tutor")
def tutor_start(request: Request, question_id: int, mode: str = Form("teach"),
                session_id: str = Form(""), back: str = Form("/"),
                inline: str = Form("")):
    """Seed a tutor thread from a quiz screen ('Why was I wrong?' / 'Teach me').

    The seed runs a slow (~1-2 min) model call. A full-page POST that blocks that
    long is fragile on mobile — backgrounding the app kills the in-flight navigation
    and a Safari reload then GETs this POST-only URL (405). So the default path
    redirects to the thread INSTANTLY and lets the page fire the seed via fetch
    (Accept: application/json), exactly like the follow-up `ask` does. The blocking
    seed still happens for that fetch and for the no-JS <noscript> fallback (inline=1).
    """
    user, redirect = require_user(request)
    if redirect:
        return redirect
    wants_json = "application/json" in request.headers.get("accept", "")
    intent = TUTOR_INTENTS.get(mode, TUTOR_INTENTS["teach"])
    with get_conn() as conn:  # load + CLOSE before the slow model call
        ctx = _tutor_context_row(conn, question_id)
        if not ctx:
            if wants_json:
                return JSONResponse({"ok": False, "error": "question not found"},
                                    status_code=404)
            return RedirectResponse(_safe_back(back), status_code=303)
        learner_answer = None
        if mode == "why_wrong" and session_id.isdigit():
            a = conn.execute(
                "SELECT user_answer FROM answers WHERE session_id = ? AND question_id = ?",
                (int(session_id), question_id)).fetchone()
            learner_answer = a["user_answer"] if a else None
        has_thread = conn.execute(
            "SELECT 1 FROM tutor_messages WHERE user_id = ? AND question_id = ? LIMIT 1",
            (user["id"], question_id)).fetchone() is not None

    # Default full-page submit (from a quiz screen): bounce straight to the thread —
    # no model call on this hop — and let the page seed via fetch. If a thread already
    # exists, just open it (no `seed` param, no re-seed).
    if not wants_json and not inline:
        dest = _tutor_url(question_id, back)
        if not has_thread:
            params = {"seed": mode}
            if session_id.isdigit():
                params["session_id"] = session_id
            dest += ("&" if "?" in dest else "?") + urlencode(params)
        return RedirectResponse(dest, status_code=303)

    # Actually run the seed (the thread page's fetch, or the no-JS inline form). If a
    # thread already exists, don't stack another canned intro or fire a second call —
    # follow-ups happen in the chat itself.
    if has_thread:
        if wants_json:
            return JSONResponse({"ok": True, "skipped": True})
        return RedirectResponse(_tutor_url(question_id, back), status_code=303)
    block = _tutor_context_block(ctx, learner_answer)
    reply = _tutor_call(block, [], intent)
    with get_conn() as conn:
        _store_tutor(conn, user["id"], question_id, intent, reply)
    if wants_json:
        return JSONResponse({"ok": True, "user": intent, "reply": reply})
    return RedirectResponse(_tutor_url(question_id, back), status_code=303)


@app.get("/questions/{question_id}/tutor")
def tutor_start_get(request: Request, question_id: int):
    """A GET here means a stale reload of the POST-only seed URL (e.g. Safari
    re-issuing the navigation after the app was backgrounded). Never 405 — just open
    the thread, which the original POST has very likely already seeded."""
    return RedirectResponse(
        _tutor_url(question_id, request.query_params.get("back", "")), status_code=303)


@app.get("/tutor/{question_id}", response_class=HTMLResponse)
def tutor_thread(request: Request, question_id: int):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        ctx = _tutor_context_row(conn, question_id)
        if not ctx:
            return RedirectResponse("/", status_code=303)
        messages = [dict(r) for r in conn.execute(
            "SELECT role, content FROM tutor_messages WHERE user_id = ? AND question_id = ? "
            "ORDER BY id", (user["id"], question_id))]
    # An empty thread reached with ?seed=<mode> should auto-seed via fetch (set up by
    # the instant redirect in tutor_start). Hand the template the mode, the matching
    # canned intent text (so it can echo the 'You' bubble to match a reload render),
    # and any session_id the why_wrong seed needs.
    seed_mode = request.query_params.get("seed") if not messages else None
    return render(request, "tutor.html", q=ctx, messages=messages,
                  question_id=question_id, back=request.query_params.get("back", ""),
                  is_admin=bool(user.get("is_admin")),
                  queued=request.query_params.get("queued") == "1",
                  seed_mode=seed_mode if seed_mode in TUTOR_INTENTS else None,
                  seed_intent=TUTOR_INTENTS.get(seed_mode),
                  seed_session_id=request.query_params.get("session_id", ""))


@app.post("/tutor/{question_id}/ask")
def tutor_ask(request: Request, question_id: int, message: str = Form(""),
              back: str = Form("")):
    user, redirect = require_user(request)
    if redirect:
        return redirect
    wants_json = "application/json" in request.headers.get("accept", "")
    msg = message.strip()
    if not msg:
        if wants_json:
            return JSONResponse({"ok": False, "error": "empty message"}, status_code=400)
        return RedirectResponse(_tutor_url(question_id, back), status_code=303)
    with get_conn() as conn:  # load + CLOSE before the model call
        ctx = _tutor_context_row(conn, question_id)
        if not ctx:
            if wants_json:
                return JSONResponse({"ok": False, "error": "question not found"}, status_code=404)
            return RedirectResponse("/", status_code=303)
        history = [dict(r) for r in conn.execute(
            "SELECT role, content FROM tutor_messages WHERE user_id = ? AND question_id = ? "
            "ORDER BY id", (user["id"], question_id))]
    # Synchronous LLM call (same exposure as the live path — see note above). The
    # browser's fetch awaits it just like the full-page POST does; we just return
    # the reply as JSON so the page can swap it in without a reload. If a reply ever
    # breaches the front proxy window you'll see 524s in `logs errors` — that's the
    # signal to move THIS one call to an enqueue+poll job, not before.
    reply = _tutor_call(_tutor_context_block(ctx), history, msg)
    with get_conn() as conn:
        _store_tutor(conn, user["id"], question_id, msg, reply)
    if wants_json:
        return JSONResponse({"ok": True, "user": msg, "reply": reply})
    return RedirectResponse(_tutor_url(question_id, back), status_code=303)


@app.post("/tutor/{question_id}/generate")
def tutor_generate(request: Request, question_id: int, back: str = Form("")):
    """Admin-only: queue a job that turns THIS tutor conversation into practice —
    it feeds the whole thread (+ chapter KB) to the generator and PROPOSES new
    questions in the question's chapter. Non-blocking; approve on the Review page.
    Lands back on the tutor thread with a 'queued' flash."""
    user, redirect = require_admin(request)
    if redirect:
        return redirect
    jobs.enqueue("generate_from_chat", user["id"], question_id)
    dest = _tutor_url(question_id, back)
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
        # Summary is over ALL finished quizzes, not just the 50 most recent we list.
        totals = conn.execute("""
            SELECT COUNT(*) AS quizzes, COALESCE(SUM(correct), 0) AS correct,
                   COALESCE(SUM(total), 0) AS answered
            FROM quiz_sessions WHERE user_id = ? AND finished_at IS NOT NULL
        """, (user["id"],)).fetchone()
    summary = dict(totals)
    summary["pct"] = (round(summary["correct"] / summary["answered"] * 100)
                      if summary["answered"] else None)

    # Bucket each session by a time label so the page reads as grouped runs
    # instead of one undifferentiated list. Bucket on the SAME (UTC) date we
    # display (finished_at[:10]) so the header can never disagree with the row.
    today = datetime.now(timezone.utc).date()
    for s in sessions:
        d = date.fromisoformat(s["finished_at"][:10])
        delta = (today - d).days
        if delta <= 0:
            s["bucket"] = "Today"
        elif delta == 1:
            s["bucket"] = "Yesterday"
        elif delta < 7:
            s["bucket"] = "Earlier this week"
        elif d.year == today.year and d.month == today.month:
            s["bucket"] = "Earlier this month"
        else:
            s["bucket"] = d.strftime("%B %Y")
    return render(request, "history.html", sessions=sessions, summary=summary)


# --------------------------------------------------------------------------
# Admin analytics  (Phase 3)  +  optional AI review  (Phase 4)
# --------------------------------------------------------------------------
def _question_stats(conn, user_id=None):
    """Per-question performance grouped by subject/chapter. Pass `user_id` to
    scope attempts/correct to one learner (answers link to a user only through
    `quiz_sessions`, so we filter on the answer's session owner); omit it for the
    whole-fleet view. Every row in `answers` is a real attempt now, so no
    placeholder filtering is needed.

    Returns (subjects, weak): `subjects` is a nested subject→chapter→question
    structure carrying chapter- and subject-level rollups for the collapsible
    view; `weak` is the flat, worst-first list of struggle questions."""
    # Scope the answer join to one learner's sessions when asked. Keeping it in
    # the JOIN's ON (not a WHERE) preserves the LEFT JOIN so a question this user
    # has never attempted still shows with attempts=0.
    if user_id is None:
        scope = ""
        params = ()
    else:
        scope = "AND a.session_id IN (SELECT id FROM quiz_sessions WHERE user_id = ?)"
        params = (user_id,)
    rows = [dict(r) for r in conn.execute(f"""
        SELECT c.name AS chapter, c.id AS chapter_id, c.position AS cpos,
               q.id AS qid, q.prompt AS prompt, q.type AS type, q.answer AS answer,
               q.source_id AS source_id, src.title AS source_title, src.kind AS source_kind,
               src.filename AS source_filename, src.url AS source_url,
               COUNT(a.id) AS attempts,
               COALESCE(SUM(a.is_correct), 0) AS correct
        FROM questions q
        JOIN chapters c ON q.chapter_id = c.id
        LEFT JOIN answers a ON a.question_id = q.id {scope}
        LEFT JOIN sources src ON q.source_id = src.id
        GROUP BY q.id
    """, params)]
    # The bank is grouped as topic → node → questions. With arbitrary depth, a
    # question's "subject" is its root topic (resolved per node, cached); the
    # "chapter" is the exact node it's filed under. Sorted in Python afterwards.
    _root_id, _root_name = {}, {}
    for r in rows:
        nid = r["chapter_id"]
        if nid not in _root_id:
            rid = db.node_root_id(conn, nid)
            _root_id[nid] = rid
            if rid is not None and rid not in _root_name:
                rr = conn.execute("SELECT name FROM chapters WHERE id = ?", (rid,)).fetchone()
                _root_name[rid] = rr["name"] if rr else ""
        r["subject_id"] = _root_id[nid]
        r["subject"] = _root_name.get(_root_id[nid], "")
    rows.sort(key=lambda r: (r["subject"].lower(), r["cpos"], r["chapter_id"], r["qid"]))
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

    # Roll chapter and subject summaries up from the question rows, so the
    # collapsed view can show "how's this chapter doing" without expanding it.
    for s in subjects:
        s_att = s_cor = 0
        for c in s["chapters"]:
            c["total_q"] = len(c["questions"])
            c["attempts"] = sum(q["attempts"] for q in c["questions"])
            c["correct"] = sum(q["correct"] for q in c["questions"])
            c["weak_count"] = sum(1 for q in c["questions"] if q["weak"])
            c["pct"] = round(100 * c["correct"] / c["attempts"]) if c["attempts"] else None
            s_att += c["attempts"]
            s_cor += c["correct"]
        s["attempts"] = s_att
        s["correct"] = s_cor
        s["pct"] = round(100 * s_cor / s_att) if s_att else None

    weak = sorted((r for r in rows if r["weak"]), key=lambda r: r["pct"])
    return subjects, weak


def _progress_shape(d):
    """Fill a counts dict (total/not_started/struggling/mastered) with the derived
    buckets and the stacked-bar segment widths. Buckets, by SM-2 state:
      not_started — never attempted (reps IS NULL)
      struggling  — a row exists but reps == 0: the last answer was wrong and it's
                    relearning (also a once-mastered card that lapsed when it came due)
      learning    — answered right at least once (reps >= 1) but not over the bar
      mastered    — cleared the bar (reps >= LEARNED_REPS AND interval >= 21d)
    `pct` is mastery (mastered/total) — the headline "how close am I". The w_* are
    exact (unrounded) %% widths so the stacked segments never sum past 100."""
    total = d["total"]
    d["seen"] = total - d["not_started"]
    d["learning"] = d["seen"] - d["struggling"] - d["mastered"]
    d["pct"] = round(100 * d["mastered"] / total) if total else 0
    span = total or 1
    d["w_mastered"] = 100 * d["mastered"] / span
    d["w_learning"] = 100 * d["learning"] / span
    d["w_struggling"] = 100 * d["struggling"] / span
    return d


def _subject_progress(conn, user_id):
    """Per-topic learning journey for ONE learner, over the arbitrary-depth node
    tree. Mastery is the SAME predicate as scheduler.chapter_progress, and every
    node's numbers are a rollup over its WHOLE subtree — so a topic's bar, an
    intermediate node's bar and the mastery badges on the quiz-setup screen all
    agree. Each node carries the four-bucket breakdown from _progress_shape and a
    `children` list (nested to any depth). Nodes whose subtree has no questions
    are pruned: there is nothing to master there.

    Returns the list of root topics, each a nested dict {id, name, children:[...],
    + breakdown fields}."""
    # Direct (own) counts per node — questions attached to that exact node.
    direct = {r["node_id"]: r for r in conn.execute(
        """SELECT q.chapter_id AS node_id,
                  COUNT(q.id) AS total,
                  SUM(CASE WHEN r.reps IS NULL THEN 1 ELSE 0 END) AS not_started,
                  SUM(CASE WHEN r.reps = 0 THEN 1 ELSE 0 END) AS struggling,
                  SUM(CASE WHEN r.reps >= ? AND COALESCE(r.interval_days, 0) >= ?
                           THEN 1 ELSE 0 END) AS mastered
           FROM questions q
           LEFT JOIN review_state r ON r.question_id = q.id AND r.user_id = ?
           GROUP BY q.chapter_id""",
        (scheduler.LEARNED_REPS, scheduler.MASTERED_INTERVAL_DAYS, user_id),
    )}
    nodes = {r["id"]: {"id": r["id"], "name": r["name"], "parent_id": r["parent_id"],
                       "position": r["position"], "children": [],
                       "total": 0, "not_started": 0, "struggling": 0, "mastered": 0}
             for r in conn.execute("SELECT id, parent_id, name, position FROM chapters")}
    for nid, d in direct.items():
        n = nodes.get(nid)
        if n:
            for k in ("total", "not_started", "struggling", "mastered"):
                n[k] += d[k] or 0
    # Link children to parents; collect roots.
    roots = []
    for n in nodes.values():
        parent = nodes.get(n["parent_id"]) if n["parent_id"] is not None else None
        (parent["children"] if parent else roots).append(n)
    for n in nodes.values():
        n["children"].sort(key=lambda c: (c["position"], c["id"]))
    roots.sort(key=lambda c: c["name"].lower())

    def rollup(n):  # post-order: add each subtree's counts up into its ancestors
        for c in n["children"]:
            rollup(c)
            for k in ("total", "not_started", "struggling", "mastered"):
                n[k] += c[k]
    for r in roots:
        rollup(r)

    def finalize(n):  # prune empty subtrees, then compute bar widths bottom-up
        n["children"] = [finalize(c) for c in n["children"] if c["total"] > 0]
        return _progress_shape(n)
    return [finalize(r) for r in roots if r["total"] > 0]


def _user_rollups(conn):
    """One summary card per user for the fleet analytics page: attempts, accuracy,
    questions mastered, and last activity. Drives the 'run analytics for them'
    drill-down links."""
    rows = [dict(r) for r in conn.execute(
        """SELECT u.id AS id, u.name AS name, u.is_admin AS is_admin,
                  COUNT(a.id) AS attempts,
                  COALESCE(SUM(a.is_correct), 0) AS correct,
                  MAX(a.answered_at) AS last_active,
                  (SELECT COUNT(*) FROM review_state r
                     WHERE r.user_id = u.id AND r.reps >= ? AND r.interval_days >= ?) AS mastered
           FROM users u
           LEFT JOIN quiz_sessions s ON s.user_id = u.id
           LEFT JOIN answers a ON a.session_id = s.id
           GROUP BY u.id
           ORDER BY u.name""",
        (scheduler.LEARNED_REPS, scheduler.MASTERED_INTERVAL_DAYS),
    )]
    for r in rows:
        r["pct"] = round(100 * r["correct"] / r["attempts"]) if r["attempts"] else None
    return rows


def _analytics_context(conn, viewer, scope_user=None):
    """Assemble everything analytics.html needs.

    Two scopes are decoupled here on purpose. The Overview tab is a personal
    *learning journey* — per-topic mastery — and mastery only means anything per
    user, so it's scoped to `scope_user or viewer` (the admin's own progress by
    default, a learner's when drilled in). The curation tools (struggle questions,
    question bank) stay fleet-wide on the default page and scope to the learner on
    a drill-down. The flagged queue and per-user roster are fleet-only."""
    progress = _subject_progress(conn, (scope_user or viewer)["id"])
    cur_uid = scope_user["id"] if scope_user else None
    subjects, weak = _question_stats(conn, cur_uid)
    ctx = {"progress": progress, "subjects": subjects, "weak": weak,
           "scope_user": scope_user}
    if scope_user is None:
        ctx["flagged"] = _flagged_questions(conn)
        ctx["users"] = _user_rollups(conn)
    else:
        ctx["flagged"] = None
        ctx["users"] = None
    return ctx


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
    admin, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        ctx = _analytics_context(conn, admin)
    return render(request, "analytics.html", ai_review=None, **ctx)


@app.get("/analytics/user/{user_id}", response_class=HTMLResponse)
def analytics_user(request: Request, user_id: int):
    """Same analytics page, scoped to one learner — 'run analytics for them'
    without becoming them. Read-only oversight; account actions live in the admin
    console (Phase 2)."""
    admin, redirect = require_admin(request)
    if redirect:
        return redirect
    target = auth.get_user(user_id)
    if not target:
        return render(request, "forbidden.html", user=admin)
    with get_conn() as conn:
        ctx = _analytics_context(conn, admin, scope_user=target)
    return render(request, "analytics.html", ai_review=None, **ctx)


@app.post("/analytics/ai-review", response_class=HTMLResponse)
def analytics_ai_review(request: Request):
    """Admin-triggered LLM pass over the struggle questions. The scheduler
    (deterministic SM-2) decides what to show; this is a SEPARATE, optional tool
    that gives qualitative curation advice ('this prompt is ambiguous', 'the
    answer key looks wrong'). Nothing is changed automatically."""
    admin, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        ctx = _analytics_context(conn, admin)
    ai_review = ai.review_results(ctx["weak"])
    return render(request, "analytics.html", ai_review=ai_review, **ctx)


# --------------------------------------------------------------------------
# Admin console — manage people, act as them, reset/delete their data
# --------------------------------------------------------------------------
# Identity model note: on the bare-LAN profile picker anyone could already pick
# an admin profile (no passwords — see auth.py). So these controls are not a
# security boundary; the safety here is the "are you sure" confirm gate the user
# asked for, plus server-side guards against footguns (last admin, self-delete).
@app.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request):
    admin, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        users = _user_rollups(conn)
        admin_count = conn.execute(
            "SELECT COUNT(*) AS c FROM users WHERE is_admin = 1").fetchone()["c"]
    return render(request, "admin_users.html", users=users, admin_count=admin_count)


@app.post("/admin/users/new")
def admin_new_user(request: Request, name: str = Form(...), email: str = Form(""),
                   make_admin: str = Form("")):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    if name.strip():
        u = auth.create_user(name, email or None)
        if make_admin == "1" and not u["is_admin"]:
            with get_conn() as conn:
                conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (u["id"],))
    return RedirectResponse("/admin/users", status_code=303)


@app.post("/admin/users/{user_id}/rename")
def admin_rename_user(request: Request, user_id: int, name: str = Form(...)):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    name = name.strip()
    if name:
        with get_conn() as conn:
            conn.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    return RedirectResponse("/admin/users", status_code=303)


@app.post("/admin/users/{user_id}/toggle-admin")
def admin_toggle_admin(request: Request, user_id: int):
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        target = conn.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
        if target:
            if target["is_admin"]:
                # Never strip the last admin — it would lock everyone out of admin.
                cnt = conn.execute(
                    "SELECT COUNT(*) AS c FROM users WHERE is_admin = 1").fetchone()["c"]
                if cnt > 1:
                    conn.execute("UPDATE users SET is_admin = 0 WHERE id = ?", (user_id,))
            else:
                conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (user_id,))
    return RedirectResponse("/admin/users", status_code=303)


@app.post("/admin/users/{user_id}/reset")
def admin_reset_user(request: Request, user_id: int):
    """Wipe a learner's STUDY state (sessions, answers, recall, flags, tutor
    chats) but keep their profile and subject enrollment. Sessions cascade to
    answers + session_questions via FK (foreign_keys=ON in get_conn)."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    with get_conn() as conn:
        conn.execute("DELETE FROM quiz_sessions WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM review_state WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM question_flags WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM tutor_messages WHERE user_id = ?", (user_id,))
    return RedirectResponse("/admin/users", status_code=303)


@app.post("/admin/users/{user_id}/delete")
def admin_delete_user(request: Request, user_id: int):
    """Remove a profile entirely. One DELETE — `users` FK cascades wipe their
    sessions, answers, recall state, flags and tutor chats."""
    _, redirect = require_admin(request)
    if redirect:
        return redirect
    # Guard against the REAL signed-in admin, not the effective user — otherwise
    # an admin who is "acting as" a fellow admin could delete their own account.
    real = auth.resolve(request)["real"]
    resp = RedirectResponse("/admin/users", status_code=303)
    if real and user_id == real["id"]:
        return resp  # never delete yourself
    with get_conn() as conn:
        target = conn.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
        if target:
            if target["is_admin"]:
                cnt = conn.execute(
                    "SELECT COUNT(*) AS c FROM users WHERE is_admin = 1").fetchone()["c"]
                if cnt <= 1:
                    return resp  # don't delete the last admin
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    resp.delete_cookie(auth.ACT_COOKIE)  # in case we were acting as them
    return resp


@app.post("/admin/act-as/{user_id}")
def admin_act_as(request: Request, user_id: int):
    """Become another user — every page then renders as them, with a banner to
    return. Reuses the whole app rather than building per-user control forms."""
    admin, redirect = require_admin(request)
    if redirect:
        return redirect
    target = auth.get_user(user_id)
    resp = RedirectResponse("/", status_code=303)
    if target and target["id"] != admin["id"]:
        resp.set_cookie(auth.ACT_COOKIE, auth.sign_act_as(user_id),
                        max_age=60 * 60 * 8, httponly=True, samesite="lax")
    return resp


@app.post("/admin/stop-acting")
def admin_stop_acting(request: Request):
    """Drop impersonation and return to the admin's own identity. Not admin-gated:
    it only clears the act-as cookie (the real admin cookie is untouched), so it
    works even while the effective user is the non-admin being impersonated."""
    resp = RedirectResponse("/admin/users", status_code=303)
    resp.delete_cookie(auth.ACT_COOKIE)
    return resp


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
    return render(request, "review_queue.html", proposals=proposals)


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
                      error=f"Bad bank structure (need topic/subject + children/chapters): {e}")
    return render(request, "import.html", result=result, error=None)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": version.VERSION}
