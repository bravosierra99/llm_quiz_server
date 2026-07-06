"""Seed the e2e server's database. Runs as a SUBPROCESS with QUIZ_DB_PATH
pointing at the e2e DB (app.db reads the env var at import time, so this can't
run inside the pytest process — its app.db is bound to the unit-suite DB).

Reads the bank JSON on stdin; prints the ids the smokes need as JSON on stdout.
"""
import json
import sys

from app import db, importer


def main():
    bank = json.load(sys.stdin)
    db.init_db()
    stats = importer.import_bank_data(bank)
    with db.get_conn() as conn:
        # Direct inserts (bootstrap-admin logic is unit-tested in test_auth):
        # the smokes need a known admin + a known non-admin learner.
        conn.execute("INSERT INTO users (name, email, is_admin) VALUES (?, ?, 1)",
                     ("parent", "parent@e2e.local"))
        kid = conn.execute("INSERT INTO users (name, email, is_admin) VALUES (?, ?, 0)",
                           ("kid", "kid@e2e.local")).lastrowid
        # Quiz setup only offers collections the user owns.
        cid = conn.execute("INSERT INTO collections (user_id, name) VALUES (?, ?)",
                           (kid, "E2E Study")).lastrowid
        conn.execute("INSERT INTO collection_nodes (collection_id, node_id) VALUES (?, ?)",
                     (cid, stats["subject_id"]))
        qid = conn.execute("SELECT id FROM questions ORDER BY id").fetchone()["id"]
    print(json.dumps({"root_id": stats["subject_id"], "first_question_id": qid}))


if __name__ == "__main__":
    main()
