"""Family-scale auth.

Two identity sources, in priority order:
  1. Cloudflare Access header `Cf-Access-Authenticated-User-Email` — set when the
     app is reached through a Cloudflare tunnel + Access policy in front of it.
     We trust it for *identity convenience only*.
  2. A signed `quiz_user` cookie chosen via the family profile picker — for when
     the app is hit directly on the LAN with no CF Access in front.

SECURITY NOTE (documented, intentional): the CF header is spoofable by anything
that can reach the container directly on the LAN, and the profile picker has no
password. This is fine for a family study app — nothing destructive or sensitive
is gated on identity. Do NOT reuse this pattern for anything that matters.

Admins (can generate/edit/delete content) are determined by the ADMIN_EMAILS env
var (comma-separated) or the is_admin flag. If no admin exists yet, the first
user created is made admin so the app is usable out of the box.
"""
import os

from itsdangerous import BadSignature, URLSafeSerializer

from .db import get_conn

SECRET_KEY = os.environ.get("QUIZ_SECRET_KEY", "dev-insecure-change-me")
ADMIN_EMAILS = {
    e.strip().lower() for e in os.environ.get("ADMIN_EMAILS", "").split(",") if e.strip()
}
COOKIE_NAME = "quiz_user"
_signer = URLSafeSerializer(SECRET_KEY, salt="quiz-user")


def sign_user_id(user_id: int) -> str:
    return _signer.dumps(user_id)


def _unsign(value: str):
    try:
        return _signer.loads(value)
    except (BadSignature, Exception):  # noqa: BLE001 - any tampering -> no user
        return None


def get_or_create_user_by_email(email: str):
    email = email.strip().lower()
    name = email.split("@")[0]
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            return dict(row)
        is_admin = _should_be_admin(conn, email)
        cur = conn.execute(
            "INSERT INTO users (name, email, is_admin) VALUES (?, ?, ?)",
            (name, email, 1 if is_admin else 0),
        )
        return {"id": cur.lastrowid, "name": name, "email": email, "is_admin": int(is_admin)}


def create_user(name: str, email: str | None = None):
    with get_conn() as conn:
        is_admin = _should_be_admin(conn, (email or "").lower())
        cur = conn.execute(
            "INSERT INTO users (name, email, is_admin) VALUES (?, ?, ?)",
            (name.strip(), (email or "").strip().lower() or None, 1 if is_admin else 0),
        )
        return {"id": cur.lastrowid, "name": name.strip(), "email": email, "is_admin": int(is_admin)}


def _should_be_admin(conn, email: str) -> bool:
    if email and email in ADMIN_EMAILS:
        return True
    # Bootstrap: first user ever is admin.
    count = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    return count == 0


def list_users():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM users ORDER BY name")]


def get_user(user_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def current_user(request):
    """Resolve the current user from CF Access header or signed cookie."""
    email = request.headers.get("Cf-Access-Authenticated-User-Email")
    if email:
        return get_or_create_user_by_email(email)
    cookie = request.cookies.get(COOKIE_NAME)
    if cookie:
        uid = _unsign(cookie)
        if uid is not None:
            return get_user(uid)
    return None
