"""Proof that the subjects/chapters → node-tree migration preserves ALL stats.

Builds a throwaway DB on the OLD (pre-node-tree) schema, fills it with
representative data (users, subjects, nested-to-be chapters, questions, finished
quiz sessions with chapter_ids JSON, session_questions, graded answers,
review_state, sources, enrollments, a proposal), SNAPSHOTS every stat that must
survive, runs the real app.db.init_db() (which fires _migrate_to_node_tree), then
asserts ZERO drift and that the new tree/collections are correct.

Run:  python -m scripts.verify_node_migration   (from repo root)
Exits 0 on success, 1 on any failed assertion.
"""
import os
import sqlite3
import sys
import tempfile

# --- OLD schema (only what the migration touches / depends on) ----------------
LEGACY_DDL = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE,
    is_admin INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '', teaching_notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    name TEXT NOT NULL, position INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE user_subjects (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')), PRIMARY KEY (user_id, subject_id));
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
    title TEXT NOT NULL, kind TEXT NOT NULL CHECK (kind IN ('text','file','url')),
    url TEXT NOT NULL DEFAULT '', file_path TEXT NOT NULL DEFAULT '',
    filename TEXT NOT NULL DEFAULT '', content TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    type TEXT NOT NULL, prompt TEXT NOT NULL, choices TEXT NOT NULL DEFAULT '[]',
    answer TEXT NOT NULL, explanation TEXT NOT NULL DEFAULT '',
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE quiz_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_ids TEXT NOT NULL DEFAULT '[]', label TEXT NOT NULL DEFAULT '',
    total INTEGER NOT NULL DEFAULT 0, correct INTEGER NOT NULL DEFAULT 0,
    endless INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')), finished_at TEXT);
CREATE TABLE session_questions (
    session_id INTEGER NOT NULL REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    PRIMARY KEY (session_id, position));
CREATE TABLE answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    user_answer TEXT NOT NULL DEFAULT '', is_correct INTEGER NOT NULL DEFAULT 0,
    answered_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE review_state (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    ease REAL NOT NULL DEFAULT 2.5, interval_days REAL NOT NULL DEFAULT 0,
    reps INTEGER NOT NULL DEFAULT 0, lapses INTEGER NOT NULL DEFAULT 0,
    due_at TEXT NOT NULL DEFAULT (datetime('now')), last_reviewed TEXT,
    PRIMARY KEY (user_id, question_id));
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', user_id INTEGER, question_id INTEGER,
    message TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT);
CREATE TABLE proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    kind TEXT NOT NULL, chapter_id INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    type TEXT NOT NULL DEFAULT 'mcq', prompt TEXT NOT NULL DEFAULT '',
    choices TEXT NOT NULL DEFAULT '[]', answer TEXT NOT NULL DEFAULT '',
    explanation TEXT NOT NULL DEFAULT '', source_id INTEGER,
    rationale TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE tutor_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, question_id INTEGER NOT NULL,
    role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (datetime('now')));
"""


def build_legacy_db(path):
    conn = sqlite3.connect(path)
    conn.executescript(LEGACY_DDL)
    cur = conn.cursor()
    # users
    cur.executemany("INSERT INTO users (id, name, email, is_admin) VALUES (?,?,?,?)",
                    [(1, "Ben", "ben@x", 1), (2, "Jessica", "jess@x", 0)])
    # 2 subjects, each with chapters
    cur.executemany("INSERT INTO subjects (id, name, description, teaching_notes) VALUES (?,?,?,?)",
                    [(1, "Math", "math desc", "math notes"), (2, "Reading", "read desc", "")])
    cur.executemany("INSERT INTO chapters (id, subject_id, name, position) VALUES (?,?,?,?)",
                    [(1, 1, "Addition", 0), (2, 1, "Subtraction", 1), (3, 2, "Phonics", 0)])
    # sources at subject level
    cur.executemany("INSERT INTO sources (id, subject_id, title, kind, content) VALUES (?,?,?,'text',?)",
                    [(1, 1, "Math KB", "1+1=2"), (2, 2, "Reading KB", "cat")])
    # questions across chapters
    qs = [(1, 1, "2+2?", "4"), (2, 1, "3+1?", "4"), (3, 2, "5-2?", "3"),
          (4, 3, "sound of c?", "k")]
    cur.executemany("INSERT INTO questions (id, chapter_id, type, prompt, answer, source_id) "
                    "VALUES (?,?,'short',?,?,NULL)", [(i, c, p, a) for (i, c, p, a) in qs])
    # finished quiz sessions referencing chapter_ids JSON
    cur.executemany("INSERT INTO quiz_sessions (id, user_id, chapter_ids, label, total, correct, finished_at) "
                    "VALUES (?,?,?,?,?,?,?)",
                    [(1, 1, "[1, 2]", "Math quiz", 3, 2, "2026-06-01T10:00:00"),
                     (2, 2, "[3]", "Reading", 1, 1, "2026-06-02T10:00:00")])
    cur.executemany("INSERT INTO session_questions (session_id, position, question_id) VALUES (?,?,?)",
                    [(1, 0, 1), (1, 1, 2), (1, 2, 3), (2, 0, 4)])
    cur.executemany("INSERT INTO answers (session_id, question_id, user_answer, is_correct, answered_at) "
                    "VALUES (?,?,?,?,?)",
                    [(1, 1, "4", 1, "2026-06-01T10:00:01"), (1, 2, "5", 0, "2026-06-01T10:00:02"),
                     (1, 3, "3", 1, "2026-06-01T10:00:03"), (2, 4, "k", 1, "2026-06-02T10:00:01")])
    cur.executemany("INSERT INTO review_state (user_id, question_id, reps, interval_days, due_at) "
                    "VALUES (?,?,?,?,?)",
                    [(1, 1, 3, 30, "2026-07-01"), (1, 2, 0, 0, "2026-06-01"), (2, 4, 1, 1, "2026-06-03")])
    cur.execute("INSERT INTO user_subjects (user_id, subject_id) VALUES (1,1),(1,2),(2,2)")
    cur.execute("INSERT INTO proposals (id, kind, chapter_id, prompt, answer) VALUES (1,'add',2,'7+1?','8')")
    conn.commit()
    conn.close()


def snapshot(path):
    """All the stat-bearing facts that MUST be identical after migration."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    g = lambda sql: conn.execute(sql).fetchall()
    snap = {
        "answers": [tuple(r) for r in g(
            "SELECT id, session_id, question_id, user_answer, is_correct, answered_at FROM answers ORDER BY id")],
        "review_state": [tuple(r) for r in g(
            "SELECT user_id, question_id, ease, interval_days, reps, lapses, due_at, last_reviewed "
            "FROM review_state ORDER BY user_id, question_id")],
        "session_questions": [tuple(r) for r in g(
            "SELECT session_id, position, question_id FROM session_questions ORDER BY session_id, position")],
        "quiz_sessions": [tuple(r) for r in g(
            "SELECT id, user_id, chapter_ids, label, total, correct, finished_at FROM quiz_sessions ORDER BY id")],
        "questions": [tuple(r) for r in g(
            "SELECT id, chapter_id, type, prompt, answer FROM questions ORDER BY id")],
        "proposals": [tuple(r) for r in g("SELECT id, chapter_id, prompt, answer FROM proposals ORDER BY id")],
        # per-question accuracy rollup — the literal "my statistics"
        "per_q": [tuple(r) for r in g(
            "SELECT question_id, COUNT(*) n, SUM(is_correct) c FROM answers GROUP BY question_id ORDER BY question_id")],
    }
    conn.close()
    return snap


FAILS = []


def check(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def main():
    tmp = tempfile.mkdtemp()
    db_path = os.path.join(tmp, "quiz.db")
    build_legacy_db(db_path)
    before = snapshot(db_path)

    # Run the REAL migration via the app's own init_db.
    os.environ["QUIZ_DB_PATH"] = db_path
    from app import db as appdb
    appdb.init_db()

    after = snapshot(db_path)

    print("\n== stats preserved (zero drift) ==")
    for key in before:
        check(before[key] == after[key], f"{key} identical before/after")

    print("\n== tree shape correct ==")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    tbls = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    check("subjects" not in tbls, "subjects table dropped")
    check("user_subjects" not in tbls, "user_subjects table dropped")
    check("collections" in tbls and "collection_nodes" in tbls, "collections tables exist")
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(chapters)")}
    check("parent_id" in cols and "subject_id" not in cols, "chapters has parent_id, no subject_id")

    roots = conn.execute("SELECT id, name FROM chapters WHERE parent_id IS NULL ORDER BY name").fetchall()
    check(len(roots) == 2, f"2 root topics (got {len(roots)})")
    root_by_name = {r["name"]: r["id"] for r in roots}
    # offset = max chapter id (3); subject 1 -> root id 4, subject 2 -> root id 5
    check(root_by_name.get("Math") == 1 + 3 and root_by_name.get("Reading") == 2 + 3,
          "roots got collision-proof offset ids")
    # chapters keep ids and point at the right root
    ch = {r["id"]: r["parent_id"] for r in conn.execute(
        "SELECT id, parent_id FROM chapters WHERE parent_id IS NOT NULL")}
    check(ch == {1: 4, 2: 4, 3: 5}, f"chapter ids preserved & re-parented (got {ch})")
    # root carries former-subject metadata
    math = conn.execute("SELECT description, teaching_notes FROM chapters WHERE id=4").fetchone()
    check(math["description"] == "math desc" and math["teaching_notes"] == "math notes",
          "root inherited subject description + teaching_notes")

    print("\n== sources repointed ==")
    src = {r["id"]: r["subject_id"] for r in conn.execute("SELECT id, subject_id FROM sources")}
    check(src == {1: 4, 2: 5}, f"sources subject_id repointed to root nodes (got {src})")

    print("\n== collections migrated from enrollments ==")
    colls = conn.execute("SELECT id, user_id, name FROM collections ORDER BY user_id").fetchall()
    check(len(colls) == 2, f"one default collection per enrolled user (got {len(colls)})")
    members = {}
    for c in colls:
        nodes = {r["node_id"] for r in conn.execute(
            "SELECT node_id FROM collection_nodes WHERE collection_id=?", (c["id"],))}
        members[c["user_id"]] = nodes
    # user 1 enrolled subjects 1,2 -> roots 4,5 ; user 2 enrolled subject 2 -> root 5
    check(members.get(1) == {4, 5}, f"Ben's collection = roots {{4,5}} (got {members.get(1)})")
    check(members.get(2) == {5}, f"Jessica's collection = root {{5}} (got {members.get(2)})")

    print("\n== new nodes insert cleanly on the migrated table ==")
    # Roots were inserted with inflated ids (subject_id + offset), so the rebuilt
    # AUTOINCREMENT table must keep counting ABOVE them — else the next insert
    # collides. (sqlite_sequence has to survive the table rename.)
    existing = {r["id"] for r in conn.execute("SELECT id FROM chapters")}
    new_id = conn.execute(
        "INSERT INTO chapters (parent_id, name) VALUES (NULL, 'Fresh Topic')").lastrowid
    check(new_id not in existing, f"new node id {new_id} doesn't collide with {sorted(existing)}")
    conn.execute("DELETE FROM chapters WHERE id = ?", (new_id,))
    conn.commit()

    print("\n== migration is idempotent (second init_db is a no-op) ==")
    appdb.init_db()
    check(snapshot(db_path) == after, "second init_db leaves everything unchanged")
    conn.close()

    print()
    if FAILS:
        print(f"FAILED: {len(FAILS)} assertion(s)")
        sys.exit(1)
    print("ALL CHECKS PASSED — stats preserved, tree + collections correct.")


if __name__ == "__main__":
    main()
