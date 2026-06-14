"""SQLite access layer. No ORM — plain sqlite3 with row factory.

The whole app is family-scale (a handful of users, a few thousand questions),
so a single SQLite file on a mounted volume is the right amount of database.
"""
import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.environ.get("QUIZ_DB_PATH", "/data/quiz.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE,
    is_admin   INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS subjects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chapters (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    name       TEXT NOT NULL,
    position   INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id  INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    type        TEXT NOT NULL CHECK (type IN ('mcq','truefalse','short')),
    prompt      TEXT NOT NULL,
    choices     TEXT NOT NULL DEFAULT '[]',   -- JSON list (mcq only)
    answer      TEXT NOT NULL,                -- canonical correct answer text
    explanation TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS quiz_sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_ids TEXT NOT NULL DEFAULT '[]',   -- JSON list
    label       TEXT NOT NULL DEFAULT '',
    total       INTEGER NOT NULL DEFAULT 0,
    correct     INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT
);

-- The ordered question queue for a session. This is the source of truth for
-- "which questions, in what order" — kept SEPARATE from `answers` so an
-- abandoned session leaves NO rows in `answers`. That means every row in
-- `answers` is a real, graded attempt and analytics never has to filter out
-- placeholders. (Before this table, the queue was faked with empty `answers`
-- rows, which polluted every "how often missed" stat.)
CREATE TABLE IF NOT EXISTS session_questions (
    session_id  INTEGER NOT NULL REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    PRIMARY KEY (session_id, position)
);

CREATE TABLE IF NOT EXISTS answers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    user_answer TEXT NOT NULL DEFAULT '',
    is_correct  INTEGER NOT NULL DEFAULT 0,
    answered_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Per-(user, question) spaced-repetition state (SM-2 lite). One row appears the
-- first time a user is graded on a question; selection and mastery read from it.
CREATE TABLE IF NOT EXISTS review_state (
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id   INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    ease          REAL    NOT NULL DEFAULT 2.5,   -- SM-2 easiness factor (>= 1.3)
    interval_days REAL    NOT NULL DEFAULT 0,      -- current spacing interval
    reps          INTEGER NOT NULL DEFAULT 0,      -- consecutive correct recalls
    lapses        INTEGER NOT NULL DEFAULT 0,      -- total times forgotten
    due_at        TEXT    NOT NULL DEFAULT (datetime('now')),
    last_reviewed TEXT,
    PRIMARY KEY (user_id, question_id)
);

CREATE INDEX IF NOT EXISTS idx_chapters_subject ON chapters(subject_id);
CREATE INDEX IF NOT EXISTS idx_questions_chapter ON questions(chapter_id);
CREATE INDEX IF NOT EXISTS idx_answers_session ON answers(session_id);
CREATE INDEX IF NOT EXISTS idx_answers_question ON answers(question_id);
CREATE INDEX IF NOT EXISTS idx_review_user ON review_state(user_id);
CREATE INDEX IF NOT EXISTS idx_review_question ON review_state(question_id);
"""


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        _migrate_legacy_queue(conn)


def _migrate_legacy_queue(conn):
    """One-time data migration from the old model, where `answers` held a
    placeholder row per selected question (used as the queue) and abandoned
    sessions left those placeholders looking like wrong answers.

    Runs only when `session_questions` is still empty but `answers` has rows —
    i.e. the first boot of the new code on a pre-existing DB. Idempotent: once
    `session_questions` is populated it never runs again.

      1. Rebuild each session's queue into `session_questions` (row order = id).
      2. Delete never-answered placeholders from `answers` so historical
         analytics are trustworthy. A placeholder is exactly user_answer='' AND
         is_correct=0. The one known false-positive — a short answer left blank
         and self-marked "missed" — is rare, low-stakes, and historical only.
    """
    have_queue = conn.execute("SELECT 1 FROM session_questions LIMIT 1").fetchone()
    have_answers = conn.execute("SELECT 1 FROM answers LIMIT 1").fetchone()
    if have_queue or not have_answers:
        return
    conn.execute("""
        INSERT INTO session_questions (session_id, position, question_id)
        SELECT session_id,
               ROW_NUMBER() OVER (PARTITION BY session_id ORDER BY id) - 1,
               question_id
        FROM answers
    """)
    conn.execute("DELETE FROM answers WHERE user_answer = '' AND is_correct = 0")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # Two family members answering at once can collide on a write; wait rather
    # than throwing "database is locked".
    conn.execute("PRAGMA busy_timeout = 5000")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# --- small helpers so routes stay readable -------------------------------

def jloads(s, default=None):
    try:
        return json.loads(s) if s else (default if default is not None else [])
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else []


def rows_to_dicts(rows):
    return [dict(r) for r in rows]
