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
# Uploaded reference files live next to the DB, on the same persistent volume.
SOURCES_DIR = str(Path(DB_PATH).parent / "sources")

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

-- Which subjects a user has added to their personal learning area. The library
-- and quiz setup show only a user's enrolled subjects; everyone curates their
-- own list (e.g. Arduino for one person, WSET for another). Pure UI scoping for
-- this family LAN app — not a security boundary.
CREATE TABLE IF NOT EXISTS user_subjects (
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, subject_id)
);

-- Reference material a question can be traced back to: a pasted passage, an
-- uploaded file (saved on the /data volume), or a URL. Provenance so the admin
-- can verify/curate a question against where it came from.
CREATE TABLE IF NOT EXISTS sources (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id  INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    kind        TEXT NOT NULL CHECK (kind IN ('text','file','url')),
    url         TEXT NOT NULL DEFAULT '',     -- kind='url'
    file_path   TEXT NOT NULL DEFAULT '',     -- kind='file' (absolute path under SOURCES_DIR)
    filename    TEXT NOT NULL DEFAULT '',     -- kind='file' (original name, for display/download)
    content     TEXT NOT NULL DEFAULT '',     -- kind='text', or extracted text cache for files
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id  INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    type        TEXT NOT NULL CHECK (type IN ('mcq','truefalse','short')),
    prompt      TEXT NOT NULL,
    choices     TEXT NOT NULL DEFAULT '[]',   -- JSON list (mcq only)
    answer      TEXT NOT NULL,                -- canonical correct answer text
    explanation TEXT NOT NULL DEFAULT '',
    source_id   INTEGER REFERENCES sources(id) ON DELETE SET NULL,
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

-- A user can flag a question for review (confusing, looks wrong, etc.). One
-- active flag per (question, user); resolving sets resolved_at. Surfaced to the
-- admin in Analytics.
CREATE TABLE IF NOT EXISTS question_flags (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    note        TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at TEXT,
    UNIQUE (question_id, user_id)
);

-- Background LLM tasks (run by an in-process worker thread). A job produces
-- zero or more `proposals` that an admin reviews before anything hits the bank.
CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    -- `kind` is code-controlled (set by enqueue() call sites, never user input)
    -- and dispatched in jobs.run_job, so we deliberately keep NO CHECK enum here:
    -- a hard-coded list forced a full table rebuild for every new job kind (SQLite
    -- can't ALTER a CHECK). See _relax_jobs_kind_check for the one-time migration.
    kind        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','running','done','error')),
    user_id     INTEGER REFERENCES users(id) ON DELETE SET NULL,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    message     TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT
);

-- A proposed change to the bank, pending admin approval. 'add' = a new question
-- (question_id NULL); 'edit' = a corrected version of an existing question.
CREATE TABLE IF NOT EXISTS proposals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id      INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    kind        TEXT NOT NULL CHECK (kind IN ('add','edit')),
    chapter_id  INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    type        TEXT NOT NULL DEFAULT 'mcq',
    prompt      TEXT NOT NULL DEFAULT '',
    choices     TEXT NOT NULL DEFAULT '[]',
    answer      TEXT NOT NULL DEFAULT '',
    explanation TEXT NOT NULL DEFAULT '',
    source_id   INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    rationale   TEXT NOT NULL DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','approved','rejected')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- A learner's tutor chat, grounded per question. One ongoing thread per
-- (user, question); the LLM context (teaching notes + chapter KB + the question)
-- is rebuilt from live data each turn, so only the conversation lives here.
CREATE TABLE IF NOT EXISTS tutor_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    role        TEXT NOT NULL CHECK (role IN ('user','assistant')),
    content     TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_chapters_subject ON chapters(subject_id);
CREATE INDEX IF NOT EXISTS idx_user_subjects_user ON user_subjects(user_id);
CREATE INDEX IF NOT EXISTS idx_tutor_user_q ON tutor_messages(user_id, question_id, id);
CREATE INDEX IF NOT EXISTS idx_flags_question ON question_flags(question_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON proposals(status);
CREATE INDEX IF NOT EXISTS idx_questions_chapter ON questions(chapter_id);
CREATE INDEX IF NOT EXISTS idx_answers_session ON answers(session_id);
CREATE INDEX IF NOT EXISTS idx_answers_question ON answers(question_id);
CREATE INDEX IF NOT EXISTS idx_review_user ON review_state(user_id);
CREATE INDEX IF NOT EXISTS idx_review_question ON review_state(question_id);
"""


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(SOURCES_DIR).mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        _migrate_legacy_queue(conn)
        _add_column_if_missing(conn, "questions", "source_id",
                               "INTEGER REFERENCES sources(id) ON DELETE SET NULL")
        _add_column_if_missing(conn, "quiz_sessions", "endless",
                               "INTEGER NOT NULL DEFAULT 0")
        _add_column_if_missing(conn, "subjects", "teaching_notes",
                               "TEXT NOT NULL DEFAULT ''")
        _relax_jobs_kind_check(conn)


def _relax_jobs_kind_check(conn):
    """Drop the obsolete CHECK enum on jobs.kind by rebuilding the table once.

    The original `CHECK (kind IN (...))` had to be widened by hand every time a job
    kind was added — SQLite can't ALTER a CHECK, only rebuild the table. Job kinds
    are code-controlled and dispatched in jobs.run_job, so the enum bought no real
    safety. Idempotent: runs only while the old constraint is still in the schema.

    Foreign keys are toggled OFF for the swap so DROP TABLE jobs doesn't cascade
    into `proposals` (which references jobs(id) ON DELETE CASCADE). Ids are
    preserved, so proposals' references stay valid after the rename."""
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='jobs'").fetchone()
    if not row or "CHECK (kind IN" not in (row["sql"] or ""):
        return
    conn.commit()  # leave any open transaction so PRAGMA foreign_keys can change
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.executescript("""
        CREATE TABLE jobs_new (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            kind        TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending','running','done','error')),
            user_id     INTEGER REFERENCES users(id) ON DELETE SET NULL,
            question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
            message     TEXT NOT NULL DEFAULT '',
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            finished_at TEXT
        );
        INSERT INTO jobs_new (id, kind, status, user_id, question_id, message, created_at, finished_at)
            SELECT id, kind, status, user_id, question_id, message, created_at, finished_at FROM jobs;
        DROP TABLE jobs;
        ALTER TABLE jobs_new RENAME TO jobs;
    """)
    conn.execute("PRAGMA foreign_keys = ON")


def _add_column_if_missing(conn, table, column, decl):
    """Idempotent ALTER TABLE ADD COLUMN. Needed because CREATE TABLE IF NOT
    EXISTS won't add a new column to a table that already exists in a deployed
    DB. SQLite allows a REFERENCES clause on an added column only when its
    default is NULL — which it is here."""
    cols = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


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
    # WAL lets readers proceed while a writer is mid-transaction (default rollback
    # journal blocks them), so a quiz GET never stalls behind a background LLM job's
    # write or another learner's answer. journal_mode persists in the DB file; we
    # set it per-connection because it's a cheap no-op once already WAL.
    # synchronous=NORMAL is the standard WAL pairing: durable across app crashes,
    # and at worst loses the last transaction on a full OS/power crash (never
    # corrupts) — an easy trade for a family study app.
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
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
