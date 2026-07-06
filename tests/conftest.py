"""Shared fixtures for the fast FleetQuiz suite.

Isolation model: `QUIZ_DB_PATH` is pointed at a throwaway temp directory BEFORE
any `app.*` import (db.py reads the env var at import time), and an autouse
fixture rebuilds a fresh schema for every test. No test ever touches /data or a
real LLM — AI calls are monkeypatched per test; the only exception is the
opt-in `requires_lm_studio` marker, which auto-skips when no endpoint is up.
"""
import os
import shutil
import tempfile
from pathlib import Path

import httpx
import pytest

# tmpfs when available (WSL/Linux): SQLite fsyncs are free there, which is most
# of the suite's runtime on a VHD-backed filesystem.
_TMP = tempfile.mkdtemp(prefix="fleetquiz-test-",
                        dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
os.environ["QUIZ_DB_PATH"] = str(Path(_TMP) / "quiz.db")
os.environ["QUIZ_SECRET_KEY"] = "test-secret"
os.environ.pop("ADMIN_EMAILS", None)  # first-created user becomes admin

from fastapi.testclient import TestClient  # noqa: E402

from app import ai, db, importer  # noqa: E402
from app.main import app  # noqa: E402

# Identity comes from the Cloudflare Access header (auth.py trusts it and
# auto-creates the user). The FIRST user created in a fresh DB is admin.
ADMIN_H = {"Cf-Access-Authenticated-User-Email": "parent@test.local"}
KID_H = {"Cf-Access-Authenticated-User-Email": "kid@test.local"}

BANK = {
    "topic": {"name": "Test Topic", "description": "For tests",
              "teaching_notes": "Keep it simple."},
    "children": [
        {
            "name": "Chapter One",
            "source": {"title": "KB One", "content": "The sky is blue."},
            "questions": (
                [{"type": "mcq", "prompt": f"MCQ number {i}?",
                  "choices": ["Right", "Wrong A", "Wrong B"],
                  "answer": "Right", "explanation": "Because tests."}
                 for i in range(1, 18)]
                + [{"type": "truefalse", "prompt": "TF: the sky is blue?",
                    "answer": "True", "explanation": "It is."},
                   {"type": "short", "prompt": "Name a color.",
                    "answer": "Blue", "explanation": "Any color works."}]
            ),
        },
        {"name": "Chapter Two", "questions": [
            {"type": "mcq", "prompt": "Chapter two question?",
             "choices": ["Yes", "No"], "answer": "Yes", "explanation": ""}]},
    ],
}


_TEMPLATE_DB = str(Path(_TMP) / "template.db")


@pytest.fixture(scope="session", autouse=True)
def _schema_template():
    """Run init_db (schema + migrations) once and keep a pristine copy."""
    db.init_db()
    with db.get_conn() as conn:  # checkpoint WAL so the copy is self-contained
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    shutil.copyfile(db.DB_PATH, _TEMPLATE_DB)


@pytest.fixture(autouse=True)
def fresh_db(_schema_template):
    """Brand-new DB per test: clone the pristine template (much faster than
    re-running the schema script, which fsyncs every statement)."""
    for suffix in ("-wal", "-shm"):
        p = Path(db.DB_PATH + suffix)
        if p.exists():
            p.unlink()
    shutil.copyfile(_TEMPLATE_DB, db.DB_PATH)
    yield


@pytest.fixture
def client():
    # No context manager: startup (init_db + jobs worker thread) stays un-run, so
    # nothing drains the job queue against a real LLM. fresh_db handles the schema.
    return TestClient(app, follow_redirects=False)


@pytest.fixture
def admin(client):
    """Ensure the admin user exists FIRST (first user in a fresh DB is admin)."""
    client.get("/", headers=ADMIN_H)
    return ADMIN_H


@pytest.fixture
def kid(client, admin):
    """A non-admin learner (created after the admin, so no bootstrap promotion)."""
    client.get("/", headers=KID_H)
    return KID_H


@pytest.fixture
def bank():
    """Import the sample bank; return handy ids and rows."""
    stats = importer.import_bank_data(BANK)
    with db.get_conn() as conn:
        chapters = {r["name"]: r["id"] for r in conn.execute(
            "SELECT id, name FROM chapters").fetchall()}
        questions = [dict(r) for r in conn.execute(
            "SELECT * FROM questions ORDER BY id").fetchall()]
    return {"stats": stats, "chapters": chapters, "questions": questions,
            "root_id": stats["subject_id"]}


def user_id_for(email):
    with db.get_conn() as conn:
        return conn.execute("SELECT id FROM users WHERE email = ?",
                            (email,)).fetchone()["id"]


# --- requires_lm_studio: live-LLM tests skip when no endpoint is reachable ---
_lm_status = None


def _lm_studio_available():
    global _lm_status
    if _lm_status is None:
        headers = {"Authorization": f"Bearer {ai.AI_API_KEY}"} if ai.AI_API_KEY else {}
        try:
            r = httpx.get(f"{ai.AI_BASE_URL}/models", headers=headers, timeout=2)
            _lm_status = r.status_code < 400
        except Exception:
            _lm_status = False
    return _lm_status


def pytest_runtest_setup(item):
    if item.get_closest_marker("requires_lm_studio") and not _lm_studio_available():
        pytest.skip("LM Studio endpoint unreachable — skipping live-LLM test")
