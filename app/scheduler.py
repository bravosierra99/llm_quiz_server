"""Spaced-repetition engine — SM-2 *lite*.

Deterministic arithmetic, no LLM. Two jobs:

  * `grade()` — update a user's recall state for one question after an attempt.
  * `select_question_ids()` — choose which questions a quiz should contain.
    Coverage-first: never-seen questions lead and fill the quiz before any
    already-seen card is re-served; reviews (due, then not-yet-due) fill the
    remainder. A freshly-missed card is held out by intervening volume so it
    never leads (see RELEARN_*).

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

from . import db

EASE_START = 2.5
EASE_FLOOR = 1.3
EASE_PENALTY = 0.2          # ease lost on a miss

# A missed card must relearn, but NOT within the same study sitting — and the
# thing that should bring it back is intervening *work*, not elapsed time. (Time
# gets it wrong both ways: grind 200 questions in an hour and a time gate still
# hides it; idle a week studying nothing and a time gate resurfaces it as if
# earned.) So a lapsed card stays out until you've answered a volume of OTHER
# questions since the miss, gated as a fraction of the unseen pool still in
# scope. This auto-adapts: lots unseen → long wait (coverage mode); pool nearly
# exhausted → short wait (drill mode). See `select_question_ids`.
RELEARN_FRACTION = 0.4   # come back after seeing ~40% of the still-unseen pool
RELEARN_FLOOR = 15       # ...but never within ~a session, even when little is unseen
RELEARN_CAP = 200        # ...and never buried forever on a huge bank

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
        interval = 0.0   # relearning: reps=0 + interval 0 is how selection spots a lapse

    now = _now()
    # due_at is the raw SM-2 time. For a lapse that's `now`, but selection does NOT
    # treat a lapsed card as due on time alone — it holds it out until enough OTHER
    # questions have been answered since `last_reviewed` (the volume gate below).
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


def mark_mastered(conn, user_id, question_id):
    """Force a question to 'mastered' for this user — for an 'it's too easy'
    button. Sets enough reps and a long interval (so chapter_progress counts it
    mastered) and pushes due_at out by that interval so it won't resurface soon."""
    now = _now()
    due = now + timedelta(days=MASTERED_INTERVAL_DAYS)
    conn.execute(
        """INSERT INTO review_state
               (user_id, question_id, ease, interval_days, reps, lapses, due_at, last_reviewed)
           VALUES (?, ?, ?, ?, ?, 0, ?, ?)
           ON CONFLICT(user_id, question_id) DO UPDATE SET
               interval_days=excluded.interval_days,
               reps=MAX(review_state.reps, excluded.reps),
               due_at=excluded.due_at, last_reviewed=excluded.last_reviewed""",
        (user_id, question_id, EASE_START, float(MASTERED_INTERVAL_DAYS),
         LEARNED_REPS, _fmt(due), _fmt(now)),
    )


# --------------------------------------------------------------------------
# Selection
# --------------------------------------------------------------------------
def select_question_ids(conn, user_id, chapter_ids, limit, order="adaptive", exclude=None):
    """Return up to `limit` question ids from the chosen nodes AND everything in
    their subtrees (picking a parent topic sweeps up all its children's questions).

    order="adaptive" (default) is the science-backed path: due questions first,
    then a capped number of never-seen questions, then not-yet-due ones if room
    remains. Within each of those tiers the order is RANDOMISED, which spreads a
    quiz across the selected chapters in proportion to each chapter's size (a
    random sample favours bigger chapters) and stops the same questions leading
    every time. "shuffle" and "ordered" are escape hatches that ignore recall state.

    `exclude` is a set/iterable of question ids to skip — used by endless mode to
    avoid re-serving questions already shown in the current session."""
    if not chapter_ids:
        return []
    # Expand each selected node to its whole subtree, so a quiz over a topic
    # includes questions filed under any descendant node, at any depth.
    chapter_ids = db.subtree_ids(conn, chapter_ids)
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
        f"""SELECT q.id AS id, r.due_at AS due_at, r.reps AS reps,
                   r.last_reviewed AS last_reviewed
            FROM questions q
            LEFT JOIN review_state r ON r.question_id = q.id AND r.user_id = ?
            WHERE q.chapter_id IN ({ph})""",
        (user_id, *chapter_ids),
    ).fetchall()
    now = _fmt(_now())
    # A reviewed card with reps==0 is in *relearning* (freshly missed or never
    # passed). It is NOT served on time alone — it waits behind a volume of other
    # questions answered since the miss (see RELEARN_* and `_relearn_ready`). The
    # rest is classic SM-2: due-by-time first, then new, then not-yet-due.
    due, new, future, relearn = [], [], [], []
    for r in rows:
        if r["id"] in exclude:
            continue
        if r["due_at"] is None:
            new.append(r["id"])
        elif r["reps"] == 0:
            relearn.append(r)            # keep the row; needs last_reviewed below
        elif r["due_at"] <= now:
            due.append(r["id"])
        else:
            future.append(r["id"])

    # Volume gate width scales to how much of the in-scope pool is still unseen:
    # plenty unseen → wait long (stay in coverage mode); little unseen → short
    # wait (drill the misses). Floor keeps a miss out of the same sitting; cap
    # stops it being buried on a huge bank.
    gap = max(RELEARN_FLOOR, min(RELEARN_CAP, round(RELEARN_FRACTION * len(new))))
    relearn_ready, relearn_waiting = [], []
    for r in relearn:
        (relearn_ready if _relearn_ready(conn, user_id, r["last_reviewed"], gap)
         else relearn_waiting).append(r["id"])

    # Randomise within each tier: a random sample across the pooled chapters is
    # drawn in proportion to each chapter's question count, and the lead-off
    # questions vary from quiz to quiz. A relearn card that has served its gap
    # rejoins the due tier; one still waiting is held to the very back — a last
    # resort that only gets served if there's genuinely nothing fresh left to ask.
    due += relearn_ready
    random.shuffle(due)
    random.shuffle(new)
    random.shuffle(future)
    random.shuffle(relearn_waiting)
    # COVERAGE-FIRST ordering: never-seen questions lead and fill the quiz before
    # ANY already-seen card is re-served, so you work through the whole bank once
    # before reviews begin. (This deliberately overrides classic SRS "due-first":
    # appending new *after* due let a review backlog the size of a quiz bury every
    # new card, so fresh material never appeared.) Reviews — due, then not-yet-due
    # — fill whatever room is left after new is exhausted; relearn-waiting misses
    # stay dead last so a miss still never leads (see RELEARN_*). No per-session
    # new-card cap: in coverage mode a cap would just re-bury new behind reviews.
    ordered = new + due + future + relearn_waiting
    return ordered[:limit]


def _relearn_ready(conn, user_id, last_reviewed, gap):
    """True once at least `gap` questions have been answered (by this user, across
    any session) since `last_reviewed` — the miss that put this card in relearning.
    Counts intervening *work*, not elapsed time, so cramming brings a miss back and
    idle time never does. `> last_reviewed` excludes the lapsing answer itself."""
    if last_reviewed is None:
        return True
    n = conn.execute(
        """SELECT COUNT(*) FROM answers a
           JOIN quiz_sessions s ON s.id = a.session_id
           WHERE s.user_id = ? AND a.answered_at > ?""",
        (user_id, last_reviewed),
    ).fetchone()[0]
    return n >= gap


# --------------------------------------------------------------------------
# Mastery / progress (Phase 2)
# --------------------------------------------------------------------------
def chapter_progress(conn, user_id, chapter_id):
    """Per-user progress for one node, rolled up over its WHOLE subtree, for the
    mastery badge.

    A single, consistent signal: how many of the node's (and descendants')
    questions this user has *mastered* — i.e. cleared the SM-2 bar (survived
    LEARNED_REPS recalls AND reached the MASTERED_INTERVAL_DAYS interval). A
    mastered question that has since come due still counts; "mastered" is about
    having learned it, not about whether it's due right now. Label is always
    "<mastered>/<total> mastered". The subtree rollup uses the SAME descendants
    set as selection and analytics, so badges and the journey page agree.

    Returns a dict with counts and a status one of: empty | partial | mastered."""
    ids = db.subtree_ids(conn, [chapter_id])
    if not ids:
        return {"total": 0, "seen": 0, "mastered": 0, "status": "empty", "label": ""}
    ph = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"""SELECT r.reps AS reps, r.interval_days AS interval_days
           FROM questions q
           LEFT JOIN review_state r ON r.question_id = q.id AND r.user_id = ?
           WHERE q.chapter_id IN ({ph})""",
        (user_id, *ids),
    ).fetchall()
    total = len(rows)
    if total == 0:
        return {"total": 0, "seen": 0, "mastered": 0, "status": "empty", "label": ""}

    seen = mastered = 0
    for r in rows:
        if r["reps"] is None:
            continue  # never attempted by this user
        seen += 1
        if r["reps"] >= LEARNED_REPS and (r["interval_days"] or 0) >= MASTERED_INTERVAL_DAYS:
            mastered += 1

    status = "mastered" if mastered == total else "partial"
    return {"total": total, "seen": seen, "mastered": mastered,
            "status": status, "label": f"{mastered}/{total} mastered"}
