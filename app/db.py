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

-- The content tree. ONE self-referential table holds the whole hierarchy at
-- ARBITRARY depth: a row with parent_id IS NULL is a root "topic" (what used to
-- be a `subject`); any other row is a child node (what used to be a `chapter`,
-- but nesting is now unlimited). Questions hang off any node (questions.chapter_id),
-- and a quiz over a node sweeps that node's whole subtree (see scheduler).
-- Kept named `chapters` so questions.chapter_id / proposals.chapter_id /
-- quiz_sessions.chapter_ids stay valid without rewriting those tables.
CREATE TABLE IF NOT EXISTS chapters (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id      INTEGER REFERENCES chapters(id) ON DELETE CASCADE,  -- NULL = root topic
    name           TEXT NOT NULL,
    description    TEXT NOT NULL DEFAULT '',
    teaching_notes TEXT NOT NULL DEFAULT '',
    position       INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

-- A named, per-person bundle of nodes — the cross-cutting layer over the strict
-- containment tree. "Jessica's 2nd Grade" can gather the 2nd-grade nodes from
-- across several root topics; content still lives in exactly one place in the
-- tree, a collection just points at it. Replaces the old flat `user_subjects`
-- (which was effectively one implicit collection per user). Pure UI scoping for
-- this family LAN app — not a security boundary.
CREATE TABLE IF NOT EXISTS collections (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS collection_nodes (
    collection_id INTEGER NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    node_id       INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    position      INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (collection_id, node_id)
);

-- Reference material a question can be traced back to: a pasted passage, an
-- uploaded file (saved on the /data volume), or a URL. Provenance so the admin
-- can verify/curate a question against where it came from.
CREATE TABLE IF NOT EXISTS sources (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id  INTEGER REFERENCES chapters(id) ON DELETE CASCADE,  -- a ROOT topic node
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

-- Whole-topic study guides ("teach me the whole topic, save it so I can read it,
-- let me mark it learned"). The GUIDE CONTENT is NOT in the DB: guides are
-- Claude-authored markdown files baked into the image at app/study/*.md, so the
-- filesystem is the catalog and a guide ships with the code (see app/study.py).
-- Only two things are per-DB: a learner's "I've learned this" flag (keyed by the
-- file's stable slug, mirroring review_state's per-user shape) and a lightweight
-- inbox of topics a learner asked Claude to write up.
CREATE TABLE IF NOT EXISTS study_progress (
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    slug       TEXT NOT NULL,            -- study guide filename stem (stable key)
    learned_at TEXT,
    PRIMARY KEY (user_id, slug)
);

-- A dumb capture inbox: a learner names a topic they want taught (often straight
-- off a quiz question they never learned). Claude reads these via db-pull and
-- fulfils them by committing a new app/study/*.md file; there is deliberately NO
-- automatic request->guide matching. fulfilled_at lets a row be dismissed by hand.
CREATE TABLE IF NOT EXISTS study_requests (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    topic        TEXT NOT NULL,
    note         TEXT NOT NULL DEFAULT '',
    user_id      INTEGER REFERENCES users(id) ON DELETE SET NULL,
    question_id  INTEGER REFERENCES questions(id) ON DELETE SET NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    fulfilled_at TEXT
);

"""

# Indexes are created AFTER table DDL and AFTER migrations (see init_db), because
# some reference columns (e.g. chapters.parent_id) that only exist on a legacy DB
# once _migrate_to_node_tree has rebuilt the table.
INDEXES = """
CREATE INDEX IF NOT EXISTS idx_chapters_parent ON chapters(parent_id);
CREATE INDEX IF NOT EXISTS idx_collection_nodes_coll ON collection_nodes(collection_id);
CREATE INDEX IF NOT EXISTS idx_collections_user ON collections(user_id);
CREATE INDEX IF NOT EXISTS idx_tutor_user_q ON tutor_messages(user_id, question_id, id);
CREATE INDEX IF NOT EXISTS idx_flags_question ON question_flags(question_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON proposals(status);
CREATE INDEX IF NOT EXISTS idx_questions_chapter ON questions(chapter_id);
CREATE INDEX IF NOT EXISTS idx_answers_session ON answers(session_id);
CREATE INDEX IF NOT EXISTS idx_answers_question ON answers(question_id);
CREATE INDEX IF NOT EXISTS idx_review_user ON review_state(user_id);
CREATE INDEX IF NOT EXISTS idx_review_question ON review_state(question_id);
CREATE INDEX IF NOT EXISTS idx_study_progress_user ON study_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_study_requests_open ON study_requests(fulfilled_at);
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
        # Legacy subjects.teaching_notes — only matters so the value carries over
        # when _migrate_to_node_tree folds subjects into the node table below.
        _add_column_if_missing(conn, "subjects", "teaching_notes",
                               "TEXT NOT NULL DEFAULT ''")
        _relax_jobs_kind_check(conn)
        _migrate_to_node_tree(conn)
        conn.executescript(INDEXES)


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


def _migrate_to_node_tree(conn):
    """One-time migration from the old fixed two-level model (subjects → chapters)
    to a single arbitrary-depth node tree, plus per-person collections.

    Runs only while the legacy `subjects` table still exists; idempotent once it's
    gone. The whole point is to PRESERVE STATISTICS: `questions`, `answers`,
    `review_state`, `session_questions` and `quiz_sessions` are NEVER rewritten.
    We achieve that by rebuilding `chapters` IN PLACE (same trick as
    _relax_jobs_kind_check) so every existing chapter KEEPS ITS ID — meaning
    questions.chapter_id, proposals.chapter_id and the quiz_sessions.chapter_ids
    JSON all stay valid byte-for-byte.

      * Former subjects become ROOT nodes (parent_id NULL). To guarantee their
        ids can't collide with any existing chapter id, each root gets
        id = subject_id + OFFSET, where OFFSET = max existing chapter id.
      * Existing chapters keep their id; parent_id = their subject's new root id.
      * `sources.subject_id` (the only other FK into subjects) is repointed to the
        matching root node id; the small `sources` table is rebuilt for the FK.
      * `user_subjects` becomes one default collection per enrolled user
        ("My Library") whose members are that user's subjects' root nodes.
      * subjects + user_subjects are dropped.

    Foreign keys are OFF for the swap so DROP TABLE doesn't cascade into
    questions/proposals/sources; ids are preserved, so every reference stays valid.
    """
    legacy = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='subjects'").fetchone()
    if not legacy:
        return
    offset = conn.execute("SELECT COALESCE(MAX(id), 0) FROM chapters").fetchone()[0]
    conn.commit()  # leave any open transaction so PRAGMA foreign_keys can change
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.executescript(f"""
        -- Rebuild chapters in place as the node tree (ids preserved).
        CREATE TABLE chapters_new (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id      INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
            name           TEXT NOT NULL,
            description    TEXT NOT NULL DEFAULT '',
            teaching_notes TEXT NOT NULL DEFAULT '',
            position       INTEGER NOT NULL DEFAULT 0,
            created_at     TEXT NOT NULL DEFAULT (datetime('now'))
        );
        -- Former subjects → root nodes (offset ids, can't collide with chapters).
        INSERT INTO chapters_new (id, parent_id, name, description, teaching_notes, position, created_at)
            SELECT id + {offset}, NULL, name, description, teaching_notes, id, created_at
            FROM subjects;
        -- Existing chapters keep their id; parent is the subject's new root id.
        INSERT INTO chapters_new (id, parent_id, name, description, teaching_notes, position, created_at)
            SELECT id, subject_id + {offset}, name, '', '', position, created_at
            FROM chapters;
        DROP TABLE chapters;
        ALTER TABLE chapters_new RENAME TO chapters;

        -- Rebuild sources to repoint subject_id at the new root node id.
        CREATE TABLE sources_new (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id  INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
            title       TEXT NOT NULL,
            kind        TEXT NOT NULL CHECK (kind IN ('text','file','url')),
            url         TEXT NOT NULL DEFAULT '',
            file_path   TEXT NOT NULL DEFAULT '',
            filename    TEXT NOT NULL DEFAULT '',
            content     TEXT NOT NULL DEFAULT '',
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );
        INSERT INTO sources_new (id, subject_id, title, kind, url, file_path, filename, content, created_at)
            SELECT id,
                   CASE WHEN subject_id IS NULL THEN NULL ELSE subject_id + {offset} END,
                   title, kind, url, file_path, filename, content, created_at
            FROM sources;
        DROP TABLE sources;
        ALTER TABLE sources_new RENAME TO sources;

        -- user_subjects → one default "My Library" collection per enrolled user.
        INSERT INTO collections (user_id, name)
            SELECT DISTINCT user_id, 'My Library' FROM user_subjects;
        INSERT INTO collection_nodes (collection_id, node_id, position)
            SELECT c.id, us.subject_id + {offset}, 0
            FROM user_subjects us
            JOIN collections c ON c.user_id = us.user_id AND c.name = 'My Library';

        DROP TABLE user_subjects;
        DROP TABLE subjects;
    """)
    conn.execute("PRAGMA foreign_keys = ON")


def _add_column_if_missing(conn, table, column, decl):
    """Idempotent ALTER TABLE ADD COLUMN. Needed because CREATE TABLE IF NOT
    EXISTS won't add a new column to a table that already exists in a deployed
    DB. SQLite allows a REFERENCES clause on an added column only when its
    default is NULL — which it is here. No-ops if the table doesn't exist (a
    fresh install may never have created a now-removed legacy table)."""
    cols = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
    if not cols:  # table doesn't exist
        return
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


# --- node tree helpers ----------------------------------------------------
# The content hierarchy lives in one self-referential `chapters` table
# (parent_id, NULL = root topic). These are the ONE place subtree math is
# expressed, so selection, the mastery badge and analytics all roll up the same
# way. UNION (not UNION ALL) makes the recursion self-terminating even if bad
# data ever introduced a parent cycle.

def subtree_ids(conn, root_ids):
    """All node ids in the subtrees rooted at `root_ids`, INCLUDING the roots
    themselves. De-duplicated. Empty input → []. This is what makes "pick a node
    for a quiz" sweep everything beneath it."""
    roots = list({int(r) for r in root_ids})
    if not roots:
        return []
    ph = ",".join("?" for _ in roots)
    rows = conn.execute(f"""
        WITH RECURSIVE sub(id) AS (
            SELECT id FROM chapters WHERE id IN ({ph})
            UNION
            SELECT c.id FROM chapters c JOIN sub ON c.parent_id = sub.id
        )
        SELECT id FROM sub
    """, roots).fetchall()
    return [r["id"] for r in rows]


def node_root_id(conn, node_id):
    """Walk up to the root topic (parent_id IS NULL) that contains `node_id`.
    Returns node_id's own id if it is already a root; None if it doesn't exist.
    Sources attach at the root, so deep nodes resolve their topic through this."""
    row = conn.execute("""
        WITH RECURSIVE anc(id, parent_id) AS (
            SELECT id, parent_id FROM chapters WHERE id = ?
            UNION ALL
            SELECT c.id, c.parent_id FROM chapters c JOIN anc ON c.id = anc.parent_id
        )
        SELECT id FROM anc WHERE parent_id IS NULL LIMIT 1
    """, (node_id,)).fetchone()
    return row["id"] if row else None


def is_descendant(conn, node_id, ancestor_id):
    """True if `node_id` is `ancestor_id` itself or anywhere in its subtree.
    Re-parent guard: rejecting parent moves where this is True prevents cycles."""
    return int(node_id) in set(subtree_ids(conn, [ancestor_id]))
