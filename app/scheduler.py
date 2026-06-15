"""Spaced-repetition engine — SM-2 *lite*.

Deterministic arithmetic, no LLM. Two jobs:

  * `grade()` — update a user's recall state for one question after an attempt.
  * `select_question_ids()` — choose which questions a quiz should contain,
    prioritising what's due over what's new over what's not yet due.

We use a binary signal (correct / incorrect) rather than SM-2's 0–5 quality
scale, because the app only ever knows "got it" or "missed it". That's the
"lite" part: a correct recall is treated as quality 4 (ease unchanged); a miss
drops the ease and resets the interval. The interval ladder (1 day → 6 days →
I·ease) is classic SM-2.

All timestamps are UTC text in SQLite's `datetime('now')` format, so plain
string comparison on `due_at` is also chronological comparison.
"""
import math
import random
from datetime import datetime, timedelta

EASE_START = 2.5
EASE_FLOOR = 1.3
EASE_PENALTY = 0.2          # ease lost on a miss

# How many brand-new questions to introduce in a single quiz. Without a cap, a
# fresh chapter would dump dozens of new cards at once and nothing would get the
# spaced repetition that makes any of this work.
NEW_CARDS_PER_SESSION = 20

# A question counts as "learned"/mastered for a user once it has survived a
# couple of recalls AND reached a long interval.
LEARNED_REPS = 2
MASTERED_INTERVAL_DAYS = 21

_TS_FMT = "%Y-%m-%d %H:%M:%S"


def _now():
    return datetime.utcnow()


def _fmt(dt):
    return dt.strftime(_TS_FMT)


# --------------------------------------------------------------------------
# Grading
# --------------------------------------------------------------------------
def grade(conn, user_id, question_id, correct):
    """Apply one SM-2-lite update for (user, question). Call this EXACTLY once
    per attempt — on the first time a question is answered in a session — so a
    browser back-and-resubmit can't double-count reps/lapses. Pass the session
    OWNER's user_id, not the request user (profiles are switchable on the LAN)."""
    row = conn.execute(
        "SELECT ease, interval_days, reps, lapses FROM review_state "
        "WHERE user_id = ? AND question_id = ?",
        (user_id, question_id),
    ).fetchone()
    if row:
        ease, interval, reps, lapses = row["ease"], row["interval_days"], row["reps"], row["lapses"]
    else:
        ease, interval, reps, lapses = EASE_START, 0.0, 0, 0

    if correct:
        reps += 1
        if reps == 1:
            interval = 1.0
        elif reps == 2:
            interval = 6.0
        else:
            interval = float(math.ceil(interval * ease))
        # ease unchanged — a plain correct recall is treated as SM-2 quality 4.
    else:
        reps = 0
        lapses += 1
        ease = max(EASE_FLOOR, ease - EASE_PENALTY)
        interval = 0.0   # relearn: due again right away

    now = _now()
    due = now + timedelta(days=interval)
    conn.execute(
        """INSERT INTO review_state
               (user_id, question_id, ease, interval_days, reps, lapses, due_at, last_reviewed)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(user_id, question_id) DO UPDATE SET
               ease=excluded.ease, interval_days=excluded.interval_days,
               reps=excluded.reps, lapses=excluded.lapses,
               due_at=excluded.due_at, last_reviewed=excluded.last_reviewed""",
        (user_id, question_id, ease, interval, reps, lapses, _fmt(due), _fmt(now)),
    )


# --------------------------------------------------------------------------
# Selection
# --------------------------------------------------------------------------
def select_question_ids(conn, user_id, chapter_ids, limit, order="adaptive", exclude=None):
    """Return up to `limit` question ids from the chosen chapters.

    order="adaptive" (default) is the science-backed path: due questions first
    (most overdue first), then a capped number of never-seen questions, then
    not-yet-due ones if room remains. "shuffle" and "ordered" are escape hatches
    that ignore recall state.

    `exclude` is a set/iterable of question ids to skip — used by endless mode to
    avoid re-serving questions already shown in the current session."""
    if not chapter_ids:
        return []
    exclude = set(exclude or ())
    ph = ",".join("?" for _ in chapter_ids)

    if order == "ordered":
        rows = conn.execute(
            f"SELECT id FROM questions WHERE chapter_id IN ({ph}) ORDER BY chapter_id, id LIMIT ?",
            (*chapter_ids, limit),
        ).fetchall()
        return [r["id"] for r in rows]

    if order == "shuffle":
        rows = conn.execute(
            f"SELECT id FROM questions WHERE chapter_id IN ({ph}) ORDER BY RANDOM() LIMIT ?",
            (*chapter_ids, limit),
        ).fetchall()
        return [r["id"] for r in rows]

    # Adaptive.
    rows = conn.execute(
        f"""SELECT q.id AS id, r.due_at AS due_at
            FROM questions q
            LEFT JOIN review_state r ON r.question_id = q.id AND r.user_id = ?
            WHERE q.chapter_id IN ({ph})""",
        (user_id, *chapter_ids),
    ).fetchall()
    now = _fmt(_now())
    due, new, future = [], [], []
    for r in rows:
        if r["id"] in exclude:
            continue
        if r["due_at"] is None:
            new.append(r["id"])
        elif r["due_at"] <= now:
            due.append((r["due_at"], r["id"]))
        else:
            future.append((r["due_at"], r["id"]))
    due.sort()
    future.sort()
    random.shuffle(new)
    ordered = [i for _, i in due] + new[:NEW_CARDS_PER_SESSION] + [i for _, i in future]
    return ordered[:limit]


# --------------------------------------------------------------------------
# Mastery / progress (Phase 2)
# --------------------------------------------------------------------------
def chapter_progress(conn, user_id, chapter_id):
    """Per-user progress for one chapter, for the mastery badge.

    Returns a dict with counts and a status one of:
      empty | new | review | learning | mastered."""
    rows = conn.execute(
        """SELECT r.reps AS reps, r.interval_days AS interval_days, r.due_at AS due_at
           FROM questions q
           LEFT JOIN review_state r ON r.question_id = q.id AND r.user_id = ?
           WHERE q.chapter_id = ?""",
        (user_id, chapter_id),
    ).fetchall()
    total = len(rows)
    if total == 0:
        return {"total": 0, "seen": 0, "learned": 0, "due": 0,
                "status": "empty", "label": ""}

    now = _fmt(_now())
    seen = learned = due = 0
    for r in rows:
        if r["reps"] is None:
            continue  # never attempted by this user
        seen += 1
        if r["due_at"] and r["due_at"] <= now:
            due += 1
        if r["reps"] >= LEARNED_REPS and (r["interval_days"] or 0) >= MASTERED_INTERVAL_DAYS:
            learned += 1

    if learned == total and due == 0:
        status, label = "mastered", "Mastered ✓"
    elif due > 0:
        status, label = "review", f"{due} due"
    elif seen == 0:
        status, label = "new", "Not started"
    else:
        status, label = "learning", f"{learned}/{total} learned"
    return {"total": total, "seen": seen, "learned": learned, "due": due,
            "status": status, "label": label}
