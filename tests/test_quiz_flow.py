"""The core product flow over real HTTP: start a quiz, answer, see feedback,
finish, and confirm grading side-effects — the class of thing template greps
and unit tests can't prove."""
import re

from app import db
from tests.conftest import user_id_for


def _start_quiz(client, headers, chapter_id, n=3, **extra):
    r = client.post("/quiz/start", headers=headers,
                    data={"chapter_ids": [chapter_id], "num_questions": n,
                          "order": "adaptive", **extra})
    assert r.status_code == 303
    m = re.match(r"/quiz/(\d+)/q/0$", r.headers["location"])
    assert m, r.headers["location"]
    return int(m.group(1))


def _question_at(session_id, idx):
    with db.get_conn() as conn:
        qid = conn.execute(
            "SELECT question_id FROM session_questions WHERE session_id = ? "
            "ORDER BY position LIMIT 1 OFFSET ?", (session_id, idx)).fetchone()[0]
        return dict(conn.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone())


def _correct_answer_form(q):
    """The form payload that grades as correct for any question type. Short
    questions are self-graded flashcards: the form reveals the answer and posts
    self_correct=yes."""
    if q["type"] == "short":
        return {"answer": q["answer"], "self_correct": "yes"}
    return {"answer": q["answer"]}


def test_full_quiz_correct_path(client, kid, bank):
    sid = _start_quiz(client, kid, bank["chapters"]["Chapter One"], n=2)
    assert client.get(f"/quiz/{sid}/q/0", headers=kid).status_code == 200

    q0 = _question_at(sid, 0)
    r = client.post(f"/quiz/{sid}/q/0", headers=kid, data=_correct_answer_form(q0))
    assert r.status_code == 303
    assert r.headers["location"] == f"/quiz/{sid}/q/1"

    q1 = _question_at(sid, 1)
    r = client.post(f"/quiz/{sid}/q/1", headers=kid, data=_correct_answer_form(q1))
    assert r.headers["location"] == f"/quiz/{sid}/results"
    assert client.get(f"/quiz/{sid}/results", headers=kid).status_code == 200

    uid = user_id_for("kid@test.local")
    with db.get_conn() as conn:
        n_correct = conn.execute(
            "SELECT COUNT(*) FROM answers WHERE session_id = ? AND is_correct = 1",
            (sid,)).fetchone()[0]
        reps = conn.execute(
            "SELECT reps FROM review_state WHERE user_id = ? AND question_id = ?",
            (uid, q0["id"])).fetchone()["reps"]
    assert n_correct == 2
    assert reps == 1


def test_wrong_answer_goes_to_feedback(client, kid, bank):
    sid = _start_quiz(client, kid, bank["chapters"]["Chapter One"], n=2)
    r = client.post(f"/quiz/{sid}/q/0", headers=kid,
                    data={"answer": "definitely not the answer"})
    assert r.headers["location"] == f"/quiz/{sid}/f/0"
    fb = client.get(f"/quiz/{sid}/f/0", headers=kid)
    assert fb.status_code == 200
    q0 = _question_at(sid, 0)
    assert q0["answer"] in fb.text  # feedback shows the correct answer


def test_dont_know_grades_as_miss(client, kid, bank):
    sid = _start_quiz(client, kid, bank["chapters"]["Chapter One"], n=1)
    r = client.post(f"/quiz/{sid}/q/0", headers=kid, data={"dont_know": "1"})
    assert r.headers["location"] == f"/quiz/{sid}/f/0"
    q0 = _question_at(sid, 0)
    uid = user_id_for("kid@test.local")
    with db.get_conn() as conn:
        row = conn.execute(
            "SELECT reps, lapses FROM review_state WHERE user_id = ? AND question_id = ?",
            (uid, q0["id"])).fetchone()
    assert row["reps"] == 0 and row["lapses"] == 1


def test_resubmit_does_not_double_grade(client, kid, bank):
    sid = _start_quiz(client, kid, bank["chapters"]["Chapter One"], n=2)
    q0 = _question_at(sid, 0)
    client.post(f"/quiz/{sid}/q/0", headers=kid, data=_correct_answer_form(q0))
    client.post(f"/quiz/{sid}/q/0", headers=kid, data=_correct_answer_form(q0))  # browser back
    uid = user_id_for("kid@test.local")
    with db.get_conn() as conn:
        reps = conn.execute(
            "SELECT reps FROM review_state WHERE user_id = ? AND question_id = ?",
            (uid, q0["id"])).fetchone()["reps"]
        n_rows = conn.execute(
            "SELECT COUNT(*) FROM answers WHERE session_id = ? AND question_id = ?",
            (sid, q0["id"])).fetchone()[0]
    assert reps == 1  # not 2
    assert n_rows == 1


def test_endless_appends_next_question(client, kid, bank):
    sid = _start_quiz(client, kid, bank["chapters"]["Chapter One"], n=1, endless="on")
    with db.get_conn() as conn:
        seeded = conn.execute(
            "SELECT COUNT(*) FROM session_questions WHERE session_id = ?",
            (sid,)).fetchone()[0]
    assert seeded == 1  # endless seeds one question, grows per answer
    q0 = _question_at(sid, 0)
    r = client.post(f"/quiz/{sid}/q/0", headers=kid, data=_correct_answer_form(q0))
    assert r.headers["location"] == f"/quiz/{sid}/q/1"  # a next question was appended
    with db.get_conn() as conn:
        queued = conn.execute(
            "SELECT COUNT(*) FROM session_questions WHERE session_id = ?",
            (sid,)).fetchone()[0]
    assert queued == 2


def test_htmx_answer_renders_next_screen_inline(client, kid, bank):
    sid = _start_quiz(client, kid, bank["chapters"]["Chapter One"], n=2)
    q0 = _question_at(sid, 0)
    r = client.post(f"/quiz/{sid}/q/0", headers={**kid, "HX-Request": "true"},
                    data=_correct_answer_form(q0))
    assert r.status_code == 200  # rendered inline, not a 303 bounce
    assert r.headers["HX-Push-Url"] == f"/quiz/{sid}/q/1"
