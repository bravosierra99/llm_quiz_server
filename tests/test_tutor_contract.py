"""Frontend↔backend contract for the tutor fetch calls.

The payloads here are COPIED FROM app/templates/tutor.html's JS (URLSearchParams
bodies + Accept: application/json), not from the route signatures — if either
side drifts, these fail. The JS reads `data.reply` and `data.skipped`; those
exact keys are asserted."""
import pytest

from app import ai, db

JS_HEADERS = {"Accept": "application/json",
              "Content-Type": "application/x-www-form-urlencoded"}


@pytest.fixture
def mock_tutor(monkeypatch):
    calls = []

    def fake_tutor(context_block, history, user_message):
        calls.append({"context": context_block, "history": history,
                      "message": user_message})
        return "Here is a mocked explanation."

    monkeypatch.setattr(ai, "tutor", fake_tutor)
    return calls


def _ask(client, headers, qid, message, back="/quiz"):
    # Mirrors tutor.html: body.set('message', msg); body.set('back', ...)
    return client.post(f"/tutor/{qid}/ask", headers={**headers, **JS_HEADERS},
                       content=f"message={message}&back={back}")


def test_ask_returns_reply_json(client, kid, bank, mock_tutor):
    qid = bank["questions"][0]["id"]
    r = _ask(client, kid, qid, "why?")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["reply"] == "Here is a mocked explanation."  # JS reads data.reply
    assert data["user"] == "why?"
    # Both sides of the exchange are persisted for the thread.
    with db.get_conn() as conn:
        roles = [r["role"] for r in conn.execute(
            "SELECT role FROM tutor_messages ORDER BY id").fetchall()]
    assert roles == ["user", "assistant"]


def test_ask_empty_message_is_400(client, kid, bank, mock_tutor):
    qid = bank["questions"][0]["id"]
    r = _ask(client, kid, qid, "")
    assert r.status_code == 400
    assert r.json()["ok"] is False
    assert mock_tutor == []  # no model call burned


def test_ask_unknown_question_is_404(client, kid, mock_tutor):
    r = _ask(client, kid, 99999, "hello")
    assert r.status_code == 404


def test_ask_degrades_when_model_unreachable(client, kid, bank, monkeypatch):
    def boom(*a, **kw):
        raise RuntimeError("connection refused")
    monkeypatch.setattr(ai, "tutor", boom)
    qid = bank["questions"][0]["id"]
    r = _ask(client, kid, qid, "help")
    assert r.status_code == 200  # the chat thread stays consistent
    assert "couldn't reach the tutor" in r.json()["reply"]


def test_seed_then_reseed_is_skipped(client, kid, bank, mock_tutor):
    """Mirrors the auto-seed fetch: sbody.set('mode', ...); sbody.set('back', ...).
    A second seed must not stack another canned intro — JS reads data.skipped."""
    qid = bank["questions"][0]["id"]
    r = client.post(f"/questions/{qid}/tutor", headers={**kid, **JS_HEADERS},
                    content="mode=teach&back=/quiz")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True and data["reply"]
    r2 = client.post(f"/questions/{qid}/tutor", headers={**kid, **JS_HEADERS},
                     content="mode=teach&back=/quiz")
    assert r2.json().get("skipped") is True
    assert len(mock_tutor) == 1


def test_seed_full_page_post_redirects_instantly(client, kid, bank, mock_tutor):
    """The no-fetch path must NOT run the model call — it bounces to the thread
    and lets the page seed via fetch (the mobile-Safari 405 fix)."""
    qid = bank["questions"][0]["id"]
    r = client.post(f"/questions/{qid}/tutor", headers=kid,
                    data={"mode": "teach", "back": "/quiz"})
    assert r.status_code == 303
    assert r.headers["location"].startswith(f"/tutor/{qid}")
    assert "seed=teach" in r.headers["location"]
    assert mock_tutor == []  # no blocking model call on the full-page hop
