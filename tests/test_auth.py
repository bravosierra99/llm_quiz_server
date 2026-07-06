"""Identity: CF-header auto-creation, admin bootstrap, cookie tampering."""
from app import auth, db
from tests.conftest import ADMIN_H, KID_H


def test_anonymous_is_redirected_to_login(client):
    r = client.get("/")
    assert r.status_code == 303
    assert r.headers["location"] == "/cdn-cgi/access/logout"


def test_first_cf_user_becomes_admin(client):
    r = client.get("/", headers=ADMIN_H)
    assert r.status_code == 200
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = 'parent@test.local'").fetchone()
    assert row["is_admin"] == 1
    # Admin console renders for them.
    assert client.get("/admin/users", headers=ADMIN_H).status_code == 200


def test_second_user_is_not_admin(client, admin, kid):
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = 'kid@test.local'").fetchone()
    assert row["is_admin"] == 0
    r = client.get("/import", headers=KID_H)
    assert r.status_code == 200
    assert "Editors only" in r.text  # forbidden.html, not the import form
    assert "Paste JSON" not in r.text


def test_tampered_cookie_is_anonymous(client, admin):
    client.cookies.set(auth.COOKIE_NAME, "1.forged-signature")
    r = client.get("/")
    assert r.status_code == 303  # bounced to login, not signed in as user 1


def test_healthz_is_public(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
