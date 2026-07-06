"""Bank import: tree building, idempotency, normalisation, the /import route."""
import json

from app import db, importer
from tests.conftest import BANK, KID_H


def test_import_builds_tree_and_questions(bank):
    s = bank["stats"]
    assert s["subject"] == "Test Topic"
    assert s["chapters"] == 2
    assert s["questions"] == 20
    assert s["rejected"] == 0
    assert s["sources"] == 1
    assert "Chapter One" in bank["chapters"] and "Chapter Two" in bank["chapters"]


def test_reimport_is_idempotent(bank):
    again = importer.import_bank_data(BANK)
    assert again["questions"] == 0
    assert again["skipped_dupe"] == 20
    with db.get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM questions").fetchone()["n"]
    assert n == 20


def test_normalisation_rules():
    clean, err = importer._normalise(
        {"type": "truefalse", "prompt": "P?", "answer": "t"})
    assert err is None and clean["answer"] == "True" and clean["choices"] == ["True", "False"]
    clean, err = importer._normalise(
        {"type": "mcq", "prompt": "P?", "choices": ["Alpha", "Beta"], "answer": "alpha"})
    assert err is None and clean["answer"] == "Alpha"  # case-matched to the choice
    clean, err = importer._normalise({"type": "mcq", "prompt": "P?", "choices": ["One"],
                                      "answer": "One"})
    assert clean is None and "choices" in err
    clean, err = importer._normalise({"type": "essay", "prompt": "P?", "answer": "A"})
    assert clean is None


def test_import_route_accepts_pasted_json(client, admin):
    r = client.post("/import", headers=admin, data={"json": json.dumps(BANK)})
    assert r.status_code == 200
    assert "Test Topic" in r.text
    with db.get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM questions").fetchone()["n"]
    assert n == 20


def test_import_route_rejects_bad_json_and_structure(client, admin):
    r = client.post("/import", headers=admin, data={"json": "{not json"})
    assert r.status_code == 200 and "Invalid JSON" in r.text
    r = client.post("/import", headers=admin, data={"json": json.dumps({"nope": 1})})
    assert r.status_code == 200 and "Bad bank structure" in r.text


def test_import_route_is_admin_only(client, admin, kid):
    r = client.post("/import", headers=KID_H, data={"json": json.dumps(BANK)})
    assert "Editors only" in r.text
    with db.get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM questions").fetchone()["n"]
    assert n == 0
