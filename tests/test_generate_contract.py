"""Admin generate → review → save round trip, with the model mocked.

The save payload uses the exact field names review.html renders (count, keep_N,
type_N, prompt_N, choices_N, answer_N, explanation_N) — the form↔route contract."""
import pytest

from app import ai, db

FAKE_RESULT = {
    "ok": True,
    "questions": [
        {"type": "mcq", "prompt": "What color is the sky?",
         "choices": ["Blue", "Green", "Red"], "answer": "Blue",
         "explanation": "Rayleigh scattering."},
        {"type": "short", "prompt": "Name the closest star.",
         "choices": [], "answer": "The Sun", "explanation": ""},
    ],
    "dropped": [],
    "error": None,
}


@pytest.fixture
def mock_generate(monkeypatch):
    calls = []

    def fake(mode, topic, source_text, num_questions, difficulty, types):
        calls.append({"mode": mode, "topic": topic, "num": num_questions,
                      "difficulty": difficulty, "types": types})
        return FAKE_RESULT

    monkeypatch.setattr(ai, "generate_questions", fake)
    return calls


def test_generate_renders_review(client, admin, bank, mock_generate):
    node = bank["chapters"]["Chapter One"]
    r = client.post(f"/nodes/{node}/generate", headers=admin,
                    data={"mode": "topic", "topic": "the sky", "num_questions": 2,
                          "difficulty": "easy", "types": ["mcq", "short"]})
    assert r.status_code == 200
    assert "What color is the sky?" in r.text
    assert mock_generate[0]["types"] == ["mcq", "short"]


def test_generate_is_admin_only(client, admin, kid, mock_generate):
    with db.get_conn() as conn:
        node = conn.execute("SELECT id FROM chapters LIMIT 1").fetchone()
    if node is None:  # no bank fixture here — make a bare topic
        r = client.post("/topics", headers=admin, data={"name": "T"})
        with db.get_conn() as conn:
            node = conn.execute("SELECT id FROM chapters LIMIT 1").fetchone()
    r = client.post(f"/nodes/{node['id']}/generate", headers=kid,
                    data={"mode": "topic", "topic": "x"})
    assert "Editors only" in r.text
    assert mock_generate == []


def test_review_save_keeps_only_checked(client, admin, bank, mock_generate):
    node = bank["chapters"]["Chapter Two"]
    before = _count(node)
    # Field names copied from review.html — keep q0, drop q1, tweak q0's answer.
    r = client.post(f"/nodes/{node}/generate/save", headers=admin, data={
        "count": "2",
        "keep_0": "on",
        "type_0": "mcq", "prompt_0": "What color is the sky?",
        "choices_0": "Blue\nGreen\nRed", "answer_0": "Blue",
        "explanation_0": "Rayleigh scattering.",
        "type_1": "short", "prompt_1": "Name the closest star.",
        "choices_1": "", "answer_1": "The Sun", "explanation_1": "",
    })
    assert r.status_code == 303
    with db.get_conn() as conn:
        rows = [dict(x) for x in conn.execute(
            "SELECT * FROM questions WHERE chapter_id = ? ORDER BY id", (node,)).fetchall()]
    assert len(rows) == before + 1
    saved = rows[-1]
    assert saved["prompt"] == "What color is the sky?"
    assert saved["answer"] == "Blue"


def _count(node_id):
    with db.get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM questions WHERE chapter_id = ?",
                            (node_id,)).fetchone()[0]
