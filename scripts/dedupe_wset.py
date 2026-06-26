#!/usr/bin/env python3
"""De-duplicate the WSET Level 1 question bank.

Background: the WSET banks (chapters 4-11) were authored with the same fact
reworded many times. Some of those rewordings are *same-format* near-clones
(e.g. two MCQs that both ask "Barolo is made from which grape? -> Nebbiolo"),
which add no learning value and make quizzes feel repetitive. This script
removes the redundant clones, keeping ONE question per dup group.

What it does NOT touch (deliberately):
  * Same stem, DIFFERENT correct answer (e.g. "Which is a sparkling wine?" ->
    Prosecco vs -> Champagne) -- that's useful option-coverage variation.
  * Cross-format pairs (an MCQ and a short-answer testing the same fact) --
    the user explicitly wants to keep those.
  * Genuinely different facts that merely share vocabulary (cool- vs hot-climate).

Which member of a dup group is KEPT is recomputed from live answer history at
run time (NOT hardcoded), per the user's rule:
    keep the one with the most practice value -> any-wrong > any-right > never,
    so never-answered clones are deleted first and a question you've gotten
    wrong is preserved for more practice.
answers / session_questions rows cascade-delete with the question (FK ON DELETE
CASCADE), so deleting a never-answered clone loses no history.

Usage:
    python3 scripts/dedupe_wset.py [--db prod_snapshot.db]        # dry-run plan
    python3 scripts/dedupe_wset.py --db prod_snapshot.db --emit-sql deletes.sql
    python3 scripts/dedupe_wset.py ... --include-borderline       # +1 borderline group

The emitted SQL (deletes.sql) is what you apply to the live prod DB with your
own operator tooling. This script never writes to prod itself.
"""
import argparse
import sqlite3
import sys

# Same-format reword clones. Each inner list is one "same fact, same answer,
# same question type" group; all but the kept member get deleted.
DUP_GROUPS = [
    [58, 134, 186],   # mcq: where red wine colour comes from -> (grape) skins
    [251, 474],       # short: NZ region famous for Sauvignon Blanc -> Marlborough
    [290, 402],       # mcq: Northern Rhone reds -> Syrah
    [346, 390],       # truefalse: Beaujolais is made from Gamay
    [340, 370],       # mcq: Bordeaux Left Bank / Medoc -> Cabernet Sauvignon
    [341, 371],       # mcq: Bordeaux Right Bank -> Merlot
    [12, 169],        # mcq: yeast converts sugar -> alcohol + carbon dioxide
    [534, 914],       # short: serving temp of medium/full red -> ~15-18C
    [327, 482],       # mcq: Pinotage signature grape of -> South Africa
    [343, 421],       # mcq: Barolo -> Nebbiolo
    [483, 726],       # truefalse: Pinotage = SA crossing of Pinot Noir x Cinsault
    [15, 171],        # short: process yeast->alcohol -> Fermentation
    [74, 231],        # short: wine with no oak -> Unoaked
    [75, 224],        # mcq: flavours oak adds -> vanilla / toast / spice
    [254, 393],       # mcq: Pouilly-Fume -> Sauvignon Blanc
    [344, 438],       # mcq: Rioja red -> Tempranillo
]

# Same format but subtly different wording; lower confidence. Off by default.
BORDERLINE_GROUPS = [
    [17, 206],        # truefalse: trapped CO2 -> sparkling wine
]


def stats(conn, qid):
    r = conn.execute(
        "SELECT COUNT(*) n, COALESCE(SUM(is_correct),0) c FROM answers WHERE question_id=?",
        (qid,)).fetchone()
    n, c = r[0], r[1]
    return {"n": n, "right": c, "wrong": n - c}


def pick_keep(conn, group):
    """Keep priority: any-wrong > any-right > never-answered, then lowest id."""
    def key(qid):
        s = stats(conn, qid)
        return (s["wrong"] > 0, s["right"] > 0, -qid)  # max() picks best
    return max(group, key=key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="prod_snapshot.db")
    ap.add_argument("--emit-sql", metavar="PATH")
    ap.add_argument("--include-borderline", action="store_true")
    args = ap.parse_args()

    groups = list(DUP_GROUPS)
    if args.include_borderline:
        groups += BORDERLINE_GROUPS

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    # Guard: every id must still exist and live in chapters 4-11 (WSET).
    valid = {r["id"] for r in conn.execute(
        "SELECT id FROM questions WHERE chapter_id BETWEEN 4 AND 11")}
    to_delete = []
    print(f"DB: {args.db}\n")
    for g in groups:
        missing = [q for q in g if q not in valid]
        if missing:
            print(f"  ! group {g}: ids not found in WSET ({missing}); skipping")
            continue
        keep = pick_keep(conn, g)
        for qid in g:
            row = conn.execute("SELECT type, prompt FROM questions WHERE id=?", (qid,)).fetchone()
            s = stats(conn, qid)
            hist = f"answered {s['n']}x (right {s['right']}, wrong {s['wrong']})" if s["n"] else "never answered"
            mark = "KEEP  " if qid == keep else "DELETE"
            if qid != keep:
                to_delete.append(qid)
            print(f"  {mark} #{qid:<4} [{row['type']:<9}] {hist:<38} {row['prompt'][:60]}")
        print()

    to_delete.sort()
    print(f"Total: {len(to_delete)} questions to delete -> {to_delete}")

    if args.emit_sql:
        ids = ",".join(str(i) for i in to_delete)
        # Every table below has an ON DELETE CASCADE FK to questions, but the
        # sqlite3 CLI runs with foreign_keys=OFF by default, so cascade would
        # NOT fire and we'd orphan child rows. Delete children explicitly so the
        # SQL is correct no matter how it's applied; the PRAGMA is belt-and-braces.
        children = ["answers", "session_questions", "review_state",
                    "question_flags", "proposals", "tutor_messages", "jobs"]
        with open(args.emit_sql, "w") as fh:
            fh.write("-- WSET dedupe: delete redundant same-format reword clones,\n")
            fh.write("-- plus their cascade children (FK cascade is not honoured by\n")
            fh.write("-- the sqlite3 CLI, so children are removed explicitly).\n")
            fh.write("PRAGMA foreign_keys=ON;\n")
            fh.write("BEGIN;\n")
            for tbl in children:
                fh.write(f"DELETE FROM {tbl} WHERE question_id IN ({ids});\n")
            fh.write(f"DELETE FROM questions WHERE id IN ({ids});\n")
            fh.write("COMMIT;\n")
        print(f"\nWrote {args.emit_sql}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
