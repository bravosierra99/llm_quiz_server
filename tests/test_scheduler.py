"""SM-2-lite grading and the relearn volume gate (a miss never leads the next
quiz; it comes back after intervening WORK, not elapsed time)."""
from app import db, scheduler
from tests.conftest import user_id_for


def _uid(client, headers, email):
    client.get("/", headers=headers)
    return user_id_for(email)


def test_grade_ladder_and_lapse(client, admin, bank):
    uid = _uid(client, admin, "parent@test.local")
    qid = bank["questions"][0]["id"]
    with db.get_conn() as conn:
        scheduler.grade(conn, uid, qid, True)
        row = conn.execute("SELECT * FROM review_state WHERE user_id=? AND question_id=?",
                           (uid, qid)).fetchone()
        assert row["reps"] == 1 and row["interval_days"] == 1.0
        scheduler.grade(conn, uid, qid, True)
        row = conn.execute("SELECT * FROM review_state WHERE user_id=? AND question_id=?",
                           (uid, qid)).fetchone()
        assert row["reps"] == 2 and row["interval_days"] == 6.0
        ease_before = row["ease"]
        scheduler.grade(conn, uid, qid, False)  # lapse
        row = conn.execute("SELECT * FROM review_state WHERE user_id=? AND question_id=?",
                           (uid, qid)).fetchone()
        assert row["reps"] == 0 and row["lapses"] == 1
        assert row["interval_days"] == 0.0
        assert row["ease"] < ease_before


def test_missed_question_never_leads(client, kid, bank):
    uid = _uid(client, kid, "kid@test.local")
    ch1 = bank["chapters"]["Chapter One"]
    with db.get_conn() as conn:
        all_ids = scheduler.select_question_ids(conn, uid, [ch1], 100)
        missed = all_ids[0]
        scheduler.grade(conn, uid, missed, False)
        # A short quiz right after the miss must not include it at all...
        soon = scheduler.select_question_ids(conn, uid, [ch1], 5)
        assert missed not in soon
        # ...and even sweeping the whole pool, it's dead last, never leading.
        full = scheduler.select_question_ids(conn, uid, [ch1], 100)
        assert full[-1] == missed


def test_relearn_gap_is_volume_not_time(client, kid, bank):
    uid = _uid(client, kid, "kid@test.local")
    ch1 = bank["chapters"]["Chapter One"]
    with db.get_conn() as conn:
        qid = scheduler.select_question_ids(conn, uid, [ch1], 1)[0]
        scheduler.grade(conn, uid, qid, False)
        last = conn.execute(
            "SELECT last_reviewed FROM review_state WHERE user_id=? AND question_id=?",
            (uid, qid)).fetchone()["last_reviewed"]
        assert not scheduler._relearn_ready(conn, uid, last, gap=15)
        # Simulate 15 intervening answers (any session, later than the miss).
        sid = conn.execute(
            "INSERT INTO quiz_sessions (user_id, chapter_ids, label, total) "
            "VALUES (?, '[]', 'sim', 15)", (uid,)).lastrowid
        for i, q in enumerate(bank["questions"][1:16]):
            conn.execute(
                "INSERT INTO answers (session_id, question_id, user_answer, is_correct, "
                "answered_at) VALUES (?, ?, 'x', 1, datetime(?, '+' || ? || ' seconds'))",
                (sid, q["id"], last, i + 1))
        assert scheduler._relearn_ready(conn, uid, last, gap=15)


def test_mark_mastered_counts_toward_progress(client, kid, bank):
    uid = _uid(client, kid, "kid@test.local")
    ch1 = bank["chapters"]["Chapter One"]
    with db.get_conn() as conn:
        qid = bank["questions"][0]["id"]
        before = scheduler.chapter_progress(conn, uid, ch1)
        scheduler.mark_mastered(conn, uid, qid)
        after = scheduler.chapter_progress(conn, uid, ch1)
    assert after["mastered"] == before["mastered"] + 1
