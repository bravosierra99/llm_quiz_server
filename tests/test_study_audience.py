"""File-declared guide audiences (`audience:` frontmatter) and the
recency-ordered analytics topic lists.

The audience tests lean on the real shipped grade2-*.md guides, which carry
`audience: jessica` — the first real use of the feature."""
from app import db, importer, study
from tests.conftest import ADMIN_H

JESS_H = {"Cf-Access-Authenticated-User-Email": "jessica@test.local"}

A_GUIDE = "Grade 2 — Word Detective (Vocabulary)"


# --- unit: matching ---------------------------------------------------------
def test_audience_match_rules():
    assert study.audience_match((), {"name": "anyone", "email": ""})
    aud = study._parse_audience("Jessica, ben@example.com")
    assert aud == ("jessica", "ben@example.com")
    # Email is the identity: a bare token matches the local part of ANY domain;
    # an @-token must match the whole address. Names never match (they drift).
    assert study.audience_match(aud, {"name": "x", "email": "Jessica@y.com"})
    assert study.audience_match(aud, {"name": "x", "email": "ben@example.com"})
    assert not study.audience_match(aud, {"name": "x", "email": "ben@other.com"})
    assert not study.audience_match(aud, {"name": "Jessica", "email": ""})
    assert not study.audience_match(aud, {"name": "kid", "email": "kid@x.com"})


def test_grade2_guides_declare_jessica_audience():
    g = study.get_guide("grade2-vowels")
    assert g["audience"] == ("jessica",)


# --- the study list ---------------------------------------------------------
def test_scoped_guide_hidden_from_other_learners(client, kid):
    r = client.get("/study", headers=kid)
    assert A_GUIDE not in r.text


def test_scoped_guide_visible_to_named_learner(client, admin):
    client.get("/", headers=JESS_H)  # creates the 'jessica' user
    r = client.get("/study", headers=JESS_H)
    assert A_GUIDE in r.text
    assert "Scoped to others" not in r.text


def test_admin_sees_scoped_section_not_personal_list(client, admin):
    r = client.get("/study", headers=ADMIN_H)
    assert "Scoped to others" in r.text
    # The guide is in the collapsed admin section, after the <hr> boundary —
    # not in the personal "To read" list, which renders before it.
    assert r.text.index(A_GUIDE) > r.text.index("Scoped to others")


def test_admin_curation_overrides_file_audience(client, admin, kid):
    client.get("/", headers=JESS_H)
    with db.get_conn() as conn:
        kid_id = conn.execute("SELECT id FROM users WHERE email = ?",
                              ("kid@test.local",)).fetchone()["id"]
    # Admin hands the guide to kid only: rows are written for EVERY user, so
    # the file default stops applying to anyone.
    r = client.post("/study/grade2-vocabulary/audience", headers=ADMIN_H,
                    data={"visible_ids": [str(kid_id)]})
    assert r.status_code == 303
    assert A_GUIDE in client.get("/study", headers=kid).text
    # For jessica the admin's uncheck lands as a real hidden row — the guide
    # drops to her collapsed Dismissed section (the documented UI behavior),
    # out of her To-read list.
    jess = client.get("/study", headers=JESS_H).text
    assert jess.index(A_GUIDE) > jess.index("Dismissed")


def test_dismiss_still_works_for_audience_member(client, admin):
    client.get("/", headers=JESS_H)
    client.post("/study/grade2-vowels/hidden", headers=JESS_H,
                data={"hidden": "1", "back": "/study"})
    r = client.get("/study", headers=JESS_H)
    # Moved to her Dismissed section (a DB row now records her choice).
    assert r.text.index("Grade 2 — Long Vowels") > r.text.index("Dismissed")


# --- analytics: last-interacted topic first ---------------------------------
def _bank(name):
    return {"topic": {"name": name}, "children": [
        {"name": "Ch", "questions": [
            {"type": "mcq", "prompt": f"{name} q?", "choices": ["a", "b"],
             "answer": "a", "explanation": ""}]}]}


def test_analytics_orders_topics_by_viewer_recency(client, admin):
    importer.import_bank_data(_bank("Alpha Topic"))
    importer.import_bank_data(_bank("Zulu Topic"))
    with db.get_conn() as conn:
        uid = conn.execute("SELECT id FROM users WHERE email = ?",
                           ("parent@test.local",)).fetchone()["id"]
        qid = conn.execute(
            """SELECT q.id FROM questions q JOIN chapters c
               ON q.chapter_id = c.id WHERE q.prompt = 'Zulu Topic q?'"""
        ).fetchone()["id"]
        sid = conn.execute(
            "INSERT INTO quiz_sessions (user_id) VALUES (?)", (uid,)).lastrowid
        conn.execute(
            "INSERT INTO answers (session_id, question_id, is_correct) "
            "VALUES (?, ?, 1)", (sid, qid))
    html = client.get("/analytics", headers=ADMIN_H).text
    # Zulu (recently quizzed) sorts before the untouched, alphabetically-first
    # Alpha in both the Overview progress list and the question-bank tree.
    assert html.index("Zulu Topic") < html.index("Alpha Topic")


def test_analytics_untouched_topics_stay_alphabetical(client, admin):
    importer.import_bank_data(_bank("Alpha Topic"))
    importer.import_bank_data(_bank("Zulu Topic"))
    html = client.get("/analytics", headers=ADMIN_H).text
    assert html.index("Alpha Topic") < html.index("Zulu Topic")
