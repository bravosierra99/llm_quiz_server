"""Read-only smokes against the DEPLOYED app through Cloudflare Access.

Opt-in and read-only: nothing runs unless RUN_PROD_SMOKE=1, and every request
is a GET — this suite must stay safe to point at the live family database.

One-time setup (Cloudflare dashboard):
  1. Zero Trust → Access → Service Auth → create a service token.
  2. Add a "Service Auth" policy for that token to the quiz application.

Then:
  RUN_PROD_SMOKE=1 PROD_SMOKE_URL=https://quiz.example.com \
  CF_ACCESS_CLIENT_ID=<id>.access CF_ACCESS_CLIENT_SECRET=<secret> \
  uv run --with-requirements requirements.txt --with pytest pytest tests/test_prod_smoke.py -q
"""
import os

import httpx
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PROD_SMOKE") != "1",
    reason="prod smoke is opt-in: RUN_PROD_SMOKE=1 + PROD_SMOKE_URL + CF_ACCESS_CLIENT_ID/SECRET")


@pytest.fixture(scope="module")
def prod():
    need = {name: os.environ.get(name) for name in
            ("PROD_SMOKE_URL", "CF_ACCESS_CLIENT_ID", "CF_ACCESS_CLIENT_SECRET")}
    missing = [k for k, v in need.items() if not v]
    if missing:
        pytest.fail(f"RUN_PROD_SMOKE=1 but missing env: {', '.join(missing)}")
    with httpx.Client(base_url=need["PROD_SMOKE_URL"].rstrip("/"),
                      follow_redirects=False, timeout=15,
                      headers={"CF-Access-Client-Id": need["CF_ACCESS_CLIENT_ID"],
                               "CF-Access-Client-Secret": need["CF_ACCESS_CLIENT_SECRET"]}) as c:
        yield c


def test_tunnel_accepts_service_token_and_app_answers(prod):
    """Proof-of-life through the tunnel: OUR app answered, not CF's login page.
    A service token carries no user email, so the app's signed-out 303 to the CF
    logout URL is just as much proof as a rendered 200."""
    r = prod.get("/")
    # A 302 to <team>.cloudflareaccess.com means Access rejected the token.
    assert "cloudflareaccess.com" not in r.headers.get("location", ""), (
        "Cloudflare Access bounced the service token to its login page. Fix: the "
        "quiz Access application needs a policy with action 'Service Auth' (not "
        "Allow) whose include rule is this service token.")
    assert r.status_code in (200, 303), r.status_code
    if r.status_code == 303:
        assert r.headers["location"] == "/cdn-cgi/access/logout"
    else:
        assert "FleetQuiz" in r.text


def test_static_pipeline_serves_current_js(prod):
    """The deploy-verification curl, as a test: the running container serves the
    current tutor module (never trust the version string)."""
    r = prod.get("/static/js/tutor.js")
    assert r.status_code == 200
    assert "tutor-form" in r.text


def test_stylesheet_is_served(prod):
    assert prod.get("/static/style.css").status_code == 200
