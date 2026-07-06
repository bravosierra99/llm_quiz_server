"""Three browser smokes over the assembled system — uvicorn + templates +
static JS + the htmx swap flow — the layer the unit suites can't see.
Selectors are stable ids / form-field names, never UI copy.
"""
import re

from playwright.sync_api import expect


def test_full_quiz_loop_in_browser(kid_page, server):
    """Setup form → every question type → results, all in-place via htmx (and
    identically via the native form fallback if the CDN is down). One question
    is missed ON PURPOSE: only wrong answers show the feedback screen, so that's
    the only way to walk the feedback → advance path."""
    page = kid_page
    page.goto("/quiz")
    page.check(f'input[name="chapter_ids"][value="{server.root_id}"]')
    page.fill('input[name="num_questions"]', "4")
    page.uncheck('input[name="endless"]')
    page.select_option('select[name="order"]', "ordered")  # deterministic: all 4 types
    page.locator("#start-quiz").click()
    expect(page).to_have_url(re.compile(r"/quiz/\d+/q/0$"))

    # Q0 (MCQ), answered wrong → feedback screen → advance.
    page.check('input[name="answer"][value="Wrong A"]')
    page.locator("#submit-answer").click()
    expect(page).to_have_url(re.compile(r"/quiz/\d+/f/0$"))
    page.locator("#advance").click()
    expect(page).to_have_url(re.compile(r"/quiz/\d+/q/1$"))

    # Q1 (MCQ) and Q2 (true/false), correct → straight to the next question.
    page.check('input[name="answer"][value="Right"]')
    page.locator("#submit-answer").click()
    expect(page).to_have_url(re.compile(r"/quiz/\d+/q/2$"))
    page.check('input[name="answer"][value="True"]')
    page.locator("#submit-answer").click()
    expect(page).to_have_url(re.compile(r"/quiz/\d+/q/3$"))

    # Q3 (short): type, reveal, self-grade (quiz.js) → results.
    page.fill('textarea[name="answer"]', "Blue")
    page.locator("#reveal-btn").click()
    page.locator("#grade-got-it").click()
    expect(page).to_have_url(re.compile(r"/quiz/\d+/results$"))
    expect(page.locator("#score")).to_have_text("3/4")


def test_theme_toggle_survives_reload(kid_page):
    """theme.js: toggle stores the choice; the synchronous <head> script must
    re-apply it on the next load (the no-flash guarantee)."""
    page = kid_page
    page.goto("/")
    assert page.get_attribute("html", "data-theme") is None  # nothing stored yet
    page.locator("#theme-toggle").click()
    # Headless Chromium reports a light OS scheme, so the first flip is to dark.
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    page.reload()
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    page.locator("#theme-toggle").click()
    expect(page.locator("html")).to_have_attribute("data-theme", "light")


def test_tutor_ask_round_trip_degrades_gracefully(kid_page, server):
    """tutor.js fetch round-trip against the dead AI endpoint: the thread gains
    the user bubble plus a resolved (non-pending) assistant bubble, and the form
    re-arms for the next question."""
    page = kid_page
    page.goto(f"/tutor/{server.first_question_id}?back=/quiz")
    page.fill('textarea[name="message"]', "Why is that the answer?")
    page.locator('#tutor-form button[type="submit"]').click()
    expect(page.locator(".tutor-msg.tutor-user")).to_have_count(1)
    expect(page.locator(".tutor-msg.tutor-assistant")).to_have_count(1)
    expect(page.locator(".tutor-pending")).to_have_count(0)  # not stuck on Thinking…
    expect(page.locator(".tutor-empty")).to_be_hidden()
    expect(page.locator('#tutor-form button[type="submit"]')).to_be_enabled()
