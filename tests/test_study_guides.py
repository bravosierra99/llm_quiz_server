"""The write_guide loop: request -> job -> sanitised draft -> admin review ->
published in the study library. AI + web search are mocked (the fast suite never
talks to a model); run_job is called directly (the worker thread never starts
under TestClient without startup)."""
import pytest

from app import ai, db, jobs, search, study

# What a reasoning model actually emits: a leaked scratchpad tag (the 27B used
# <thinking>, not <think>), then frontmatter whose title contains a colon.
RAW_DRAFT = """<thinking>
Let me plan the guide...
</thinking>

---
title: Parts of Speech: Every Word Has a Job
summary: What each kind of word does.
---

# Parts of Speech

A **noun** names a thing.

## Self-check

1. Is "dog" a noun?
"""


@pytest.fixture
def request_id(client, kid):
    client.post("/study/request", headers=kid,
                data={"topic": "What are parts of speech?", "note": "for grade 1"})
    with db.get_conn() as conn:
        return conn.execute("SELECT id FROM study_requests").fetchone()["id"]


def _draft(monkeypatch, request_id, text=RAW_DRAFT, ok=True):
    """Run the write_guide job against a canned model reply."""
    monkeypatch.setattr(search, "web_search", lambda q: ([], None))
    monkeypatch.setattr(ai, "write_guide", lambda *a: {
        "ok": ok, "text": text, "error": None if ok else "boom"})
    with db.get_conn() as conn:
        jid = conn.execute("SELECT id FROM jobs WHERE request_id = ?",
                           (request_id,)).fetchone()["id"]
    jobs.run_job(jid)
    return jid


# --- capture + job ----------------------------------------------------------
def test_request_queues_a_write_guide_job(client, kid, request_id):
    with db.get_conn() as conn:
        job = conn.execute("SELECT * FROM jobs WHERE kind = 'write_guide'").fetchone()
    assert job and job["request_id"] == request_id and job["status"] == "pending"
    # Re-submitting the same ask doesn't stack jobs (enqueue dedupes on request).
    jobs.enqueue("write_guide", 1, None, request_id=request_id)
    with db.get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) n FROM jobs WHERE kind = 'write_guide'").fetchone()["n"]
    assert n == 1


def test_job_produces_a_sanitised_pending_draft(client, kid, request_id, monkeypatch):
    _draft(monkeypatch, request_id)
    with db.get_conn() as conn:
        d = dict(conn.execute("SELECT * FROM guide_drafts").fetchone())
        job = conn.execute("SELECT * FROM jobs WHERE kind = 'write_guide'").fetchone()
    assert job["status"] == "done"
    assert d["status"] == "pending"
    assert d["title"] == "Parts of Speech: Every Word Has a Job"  # colon survives
    assert "<thinking>" not in d["body"] and "---" not in d["body"].split("\n")[0]
    assert d["request_id"] == request_id
    # Pending means NOT in the study library yet.
    r = client.get("/study", headers=kid)
    assert d["title"] not in r.text


def test_failed_model_call_marks_job_errored(client, kid, request_id, monkeypatch):
    _draft(monkeypatch, request_id, ok=False)
    with db.get_conn() as conn:
        assert conn.execute("SELECT COUNT(*) n FROM guide_drafts").fetchone()["n"] == 0
        job = conn.execute("SELECT * FROM jobs WHERE kind = 'write_guide'").fetchone()
    assert job["status"] == "error"


# --- review -----------------------------------------------------------------
def test_approve_publishes_and_fulfils_the_request(client, admin, kid, request_id, monkeypatch):
    _draft(monkeypatch, request_id)
    with db.get_conn() as conn:
        d = dict(conn.execute("SELECT * FROM guide_drafts").fetchone())
    assert d["title"] in client.get("/review", headers=admin).text
    client.post(f"/guide-drafts/{d['id']}/approve", headers=admin)
    with db.get_conn() as conn:
        assert conn.execute("SELECT status FROM guide_drafts WHERE id = ?",
                            (d["id"],)).fetchone()["status"] == "published"
        assert conn.execute("SELECT fulfilled_at FROM study_requests WHERE id = ?",
                            (request_id,)).fetchone()["fulfilled_at"]
    # Published guide is readable and learnable like a file guide.
    assert d["title"] in client.get("/study", headers=kid).text
    page = client.get(f"/study/{d['slug']}", headers=kid)
    assert "noun" in page.text
    client.post(f"/study/{d['slug']}/learned", headers=kid, data={"learned": "1"})
    with db.get_conn() as conn:
        assert conn.execute("SELECT learned_at FROM study_progress WHERE slug = ?",
                            (d["slug"],)).fetchone()["learned_at"]


def test_reject_keeps_request_open_and_admin_can_redraft(client, admin, kid, request_id, monkeypatch):
    _draft(monkeypatch, request_id)
    with db.get_conn() as conn:
        d = dict(conn.execute("SELECT * FROM guide_drafts").fetchone())
    client.post(f"/guide-drafts/{d['id']}/reject", headers=admin)
    with db.get_conn() as conn:
        assert conn.execute("SELECT status FROM guide_drafts WHERE id = ?",
                            (d["id"],)).fetchone()["status"] == "rejected"
        assert not conn.execute("SELECT fulfilled_at FROM study_requests WHERE id = ?",
                                (request_id,)).fetchone()["fulfilled_at"]
    assert d["title"] not in client.get("/study", headers=kid).text
    # The study page offers the admin a redraft, and the route queues a new job.
    assert f"/study/requests/{request_id}/draft" in client.get("/study", headers=admin).text
    client.post(f"/study/requests/{request_id}/draft", headers=admin)
    with db.get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) n FROM jobs WHERE kind = 'write_guide' "
                         "AND status = 'pending'").fetchone()["n"]
    assert n == 1


def test_review_actions_are_admin_gated(client, admin, kid, request_id, monkeypatch):
    _draft(monkeypatch, request_id)
    with db.get_conn() as conn:
        gid = conn.execute("SELECT id FROM guide_drafts").fetchone()["id"]
    client.post(f"/guide-drafts/{gid}/approve", headers=kid)
    client.post(f"/study/requests/{request_id}/draft", headers=kid)
    with db.get_conn() as conn:
        assert conn.execute("SELECT status FROM guide_drafts WHERE id = ?",
                            (gid,)).fetchone()["status"] == "pending"


# --- sanitiser unit coverage --------------------------------------------------
def test_parse_draft_strips_think_variants_and_fences():
    for tag in ("think", "thinking"):
        got = study.parse_draft(f"<{tag}>secret plan</{tag}>\n# Title\n\nBody.", "fb")
        assert got["title"] == "Title" and "secret" not in got["body"]
    fenced = study.parse_draft("```markdown\n# Fenced\n\nBody.\n```", "fb")
    assert fenced["title"] == "Fenced" and "```" not in fenced["body"]


def test_parse_draft_fallbacks():
    assert study.parse_draft("Just prose, no heading.", "The Topic")["title"] == "The Topic"
    assert study.parse_draft("<think>only thoughts</think>", "t") is None
    assert study.parse_draft("", "t") is None


def test_slugify_avoids_file_and_draft_collisions():
    assert study.slugify("Parts of Speech!") == "parts-of-speech-2"  # file exists
    assert study.slugify("Brand New Topic") == "brand-new-topic"
    assert study.slugify("Brand New Topic", taken={"brand-new-topic"}) == "brand-new-topic-2"
