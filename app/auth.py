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
# Admin "act as" (impersonation): a SEPARATE signed cookie holding the user id an
# admin is currently acting as. Its own salt means it can never be swapped for an
# identity cookie, and — critically — it is only ever honoured when the REAL user
# (resolved the normal way) is an admin. So setting it alone grants nothing.
ACT_COOKIE = "quiz_act_as"
_signer = URLSafeSerializer(SECRET_KEY, salt="quiz-user")
_act_signer = URLSafeSerializer(SECRET_KEY, salt="quiz-act-as")


def sign_user_id(user_id: int) -> str:
    return _signer.dumps(user_id)


def sign_act_as(user_id: int) -> str:
    return _act_signer.dumps(user_id)


def _unsign(value: str):
    try:
        return _signer.loads(value)
    except (BadSignature, Exception):  # noqa: BLE001 - any tampering -> no user
        return None


def _unsign_act_as(value: str):
    try:
        return _act_signer.loads(value)
    except (BadSignature, Exception):  # noqa: BLE001 - any tampering -> no impersonation
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


def _resolve_real(request):
    """The REAL signed-in identity — CF Access header first, then the signed
    profile cookie. This is the only place identity is established; impersonation
    layers on top of it and never replaces it."""
    email = request.headers.get("Cf-Access-Authenticated-User-Email")
    if email:
        return get_or_create_user_by_email(email)
    cookie = request.cookies.get(COOKIE_NAME)
    if cookie:
        uid = _unsign(cookie)
        if uid is not None:
            return get_user(uid)
    return None


def resolve(request):
    """Resolve identity into {real, effective, acting}.

    `effective` is who the app should behave as — the impersonated target when an
    admin is acting as someone, otherwise the real user. The act-as cookie is
    honoured ONLY when the real user is an admin, so a non-admin who plants the
    cookie gets nothing. The app uses `effective` everywhere (so every existing
    page just works as the target), while admin gating still flows through
    `effective` too — meaning an admin who acts as a non-admin lives that
    non-admin's restricted experience until they return."""
    real = _resolve_real(request)
    effective, acting = real, False
    if real and real.get("is_admin"):
        cookie = request.cookies.get(ACT_COOKIE)
        if cookie:
            tid = _unsign_act_as(cookie)
            if tid is not None and tid != real["id"]:
                target = get_user(tid)
                if target:
                    effective, acting = target, True
    return {"real": real, "effective": effective, "acting": acting}


def current_user(request):
    """The effective user (impersonated target if an admin is acting as someone,
    else the real user). Existing call sites get impersonation for free."""
    return resolve(request)["effective"]
