"""CLI to bulk-import a question bank JSON into FleetQuiz (dev/local use).

The import logic lives in app/importer.py so it's shared with the `/import`
admin endpoint (and ships inside the app package). This is just a thin wrapper
that reads a file and prints a summary.

Run:  QUIZ_DB_PATH=./data/quiz.db python -m import_bank path/to/bank.json
Idempotent: re-running skips a question if one with the same prompt already
exists in that chapter.
"""
import json
import sys

from app.db import init_db
from app.importer import import_bank_data


def import_bank(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    init_db()
    stats = import_bank_data(data)
    print(f"Imported into subject '{stats['subject']}': "
          f"+{stats['chapters']} chapters, +{stats['questions']} questions, "
          f"+{stats['sources']} sources "
          f"({stats['skipped_dupe']} dupes skipped, {stats['rejected']} rejected).")
    return stats


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m import_bank <bank.json>", file=sys.stderr)
        sys.exit(2)
    import_bank(sys.argv[1])
