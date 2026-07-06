"""Playwright e2e smokes: a real browser against a real uvicorn subprocess.

Opt-in by dependency: this whole directory auto-skips unless pytest-playwright
is installed, so the fast unit suite stays browser-free. Run it with

    uv run --with-requirements requirements.txt --with pytest \
        --with pytest-playwright pytest tests/e2e -q

The server gets its own DB (seeded by _seed.py in a subprocess) and a DEAD
AI endpoint on purpose — the tutor smoke asserts the degraded path, so no test
ever needs (or waits on) a real LLM. Identity rides the Cloudflare Access
header on the browser context, exactly like production behind Access.
"""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx
import pytest

pytest.importorskip("pytest_playwright",
                    reason="e2e needs pytest-playwright (see README: Tests & lint)")

ROOT = Path(__file__).resolve().parent.parent.parent
CF_HEADER = "Cf-Access-Authenticated-User-Email"

# Small on purpose: with order="ordered" and num_questions=4, the quiz smoke
# deterministically walks every question type (radio MCQs, true/false, and the
# short-answer reveal/self-grade flow).
E2E_BANK = {
    "topic": {"name": "E2E Topic", "description": "For browser smokes"},
    "children": [
        {"name": "Chapter One", "questions": [
            {"type": "mcq", "prompt": "MCQ one?", "answer": "Right",
             "choices": ["Right", "Wrong A", "Wrong B"], "explanation": "Because."},
            {"type": "mcq", "prompt": "MCQ two?", "answer": "Right",
             "choices": ["Right", "Wrong A", "Wrong B"], "explanation": ""},
            {"type": "truefalse", "prompt": "TF: water is wet?", "answer": "True",
             "explanation": ""},
            {"type": "short", "prompt": "Name a color.", "answer": "Blue",
             "explanation": "Any color works."},
        ]},
    ],
}


class Server:
    def __init__(self, url, seeded):
        self.url = url
        self.root_id = seeded["root_id"]
        self.first_question_id = seeded["first_question_id"]


@pytest.fixture(scope="session")
def server():
    tmp = tempfile.mkdtemp(prefix="fleetquiz-e2e-",
                           dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    env = {**os.environ,
           "PYTHONPATH": str(ROOT),  # _seed.py runs by path; `app` must resolve
           "QUIZ_DB_PATH": str(Path(tmp) / "e2e.db"),
           "QUIZ_SECRET_KEY": "e2e-secret",
           # The app's own port with a bogus path: an INSTANT 404 on every AI
           # call. (A closed port is not reliably instant — WSL2's localhost
           # relay can sit on the connect until the timeout.)
           "AI_BASE_URL": f"http://127.0.0.1:{port}/not-an-llm/v1",
           "AI_TIMEOUT": "5"}
    env.pop("ADMIN_EMAILS", None)

    seed = subprocess.run([sys.executable, str(Path(__file__).parent / "_seed.py")],
                          input=json.dumps(E2E_BANK), capture_output=True,
                          text=True, env=env, cwd=ROOT)
    assert seed.returncode == 0, seed.stderr
    seeded = json.loads(seed.stdout)

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning"],
        env=env, cwd=ROOT)
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 30
    while True:
        try:
            if httpx.get(f"{url}/static/style.css", timeout=1).status_code == 200:
                break
        except httpx.HTTPError:
            pass
        if time.time() > deadline or proc.poll() is not None:
            proc.terminate()
            raise RuntimeError("e2e uvicorn did not come up")
        time.sleep(0.15)
    yield Server(url, seeded)
    proc.terminate()
    proc.wait(timeout=10)


@pytest.fixture
def kid_page(browser, server):
    """A page authenticated as the non-admin learner via the CF header."""
    ctx = browser.new_context(base_url=server.url,
                              extra_http_headers={CF_HEADER: "kid@e2e.local"})
    yield ctx.new_page()
    ctx.close()
