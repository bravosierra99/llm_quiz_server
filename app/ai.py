"""AI question generation against an OpenAI-compatible endpoint (LM Studio).

The LLM -> questions JSON contract is the riskiest part of the app: local
models emit malformed JSON far more often than frontier models. So we:
  1. Instruct the exact schema in the prompt and ask for JSON only.
  2. Parse defensively (strip code fences, find the outer JSON array).
  3. Validate every question; drop/clean bad ones rather than trusting blindly.
  4. Retry once on a hard parse failure.
Whatever survives goes to the admin REVIEW step before it is saved — so flaky
generation degrades to "fewer/edited questions", never "garbage in the quiz".
"""
import json
import os
import re

import httpx

AI_BASE_URL = os.environ.get("AI_BASE_URL", "http://localhost:1234/v1").rstrip("/")
AI_MODEL = os.environ.get("AI_MODEL", "local-model")
AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_TIMEOUT = float(os.environ.get("AI_TIMEOUT", "180"))  # local models run ~1-2 min/batch

VALID_TYPES = {"mcq", "truefalse", "short"}

SYSTEM_PROMPT = """You are a quiz author for a family study app. \
You write clear, factually accurate study questions for the requested topic and \
difficulty. You output ONLY a JSON array — no prose, no markdown, no code fences.

Each array element is an object with EXACTLY these keys:
  "type": one of "mcq", "truefalse", "short"
  "prompt": the question text (string)
  "choices": for "mcq" a list of 3-5 distinct answer strings; for "truefalse" \
the list ["True","False"]; for "short" an empty list []
  "answer": the exact correct answer. For "mcq" it MUST be one of the choices \
verbatim. For "truefalse" it MUST be "True" or "False". For "short" a concise \
canonical answer.
  "explanation": one or two sentences explaining why the answer is correct.

Rules:
- Output a single JSON array and nothing else.
- Make questions self-contained (do not say "in the experiment above").
- Prefer a mix of the requested question types.
- No duplicate questions."""


def _build_user_prompt(mode, topic, source_text, num_questions, difficulty, types):
    types_str = ", ".join(types)
    head = (
        f"Generate {num_questions} {difficulty} study questions. "
        f"Use only these question types: {types_str}.\n"
    )
    if mode == "source":
        return (
            head
            + "Base the questions strictly on the following source material. "
            + "Do not introduce facts that are not supported by it:\n\n"
            + "=== SOURCE MATERIAL START ===\n"
            + source_text.strip()
            + "\n=== SOURCE MATERIAL END ==="
        )
    return head + f"Topic: {topic.strip()}"


def _extract_json_array(text):
    """Pull a JSON array out of a model response that may be wrapped in prose
    or ```json fences. Returns the parsed list or raises ValueError."""
    if not text:
        raise ValueError("empty response")
    # Strip code fences.
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    text = text.strip()
    # Fast path.
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "questions" in data:
            return data["questions"]
    except json.JSONDecodeError:
        pass
    # Fallback: grab the outermost [...] span.
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        data = json.loads(text[start : end + 1])
        if isinstance(data, list):
            return data
    raise ValueError("no JSON array found in model output")


def _clean_question(raw):
    """Validate and normalize one question dict. Returns (question, None) or
    (None, reason)."""
    if not isinstance(raw, dict):
        return None, "not an object"
    qtype = str(raw.get("type", "")).strip().lower()
    if qtype not in VALID_TYPES:
        return None, f"bad type {qtype!r}"
    prompt = str(raw.get("prompt", "")).strip()
    if not prompt:
        return None, "empty prompt"
    answer = str(raw.get("answer", "")).strip()
    if not answer:
        return None, "empty answer"
    choices = raw.get("choices", [])
    if not isinstance(choices, list):
        choices = []
    choices = [str(c).strip() for c in choices if str(c).strip()]

    if qtype == "truefalse":
        choices = ["True", "False"]
        answer = "True" if answer.lower().startswith("t") else "False"
    elif qtype == "mcq":
        if len(choices) < 2:
            return None, "mcq needs >=2 choices"
        # Ensure the answer is present verbatim among the choices.
        if answer not in choices:
            match = next((c for c in choices if c.lower() == answer.lower()), None)
            if match:
                answer = match
            else:
                choices.append(answer)
    else:  # short
        choices = []

    return {
        "type": qtype,
        "prompt": prompt,
        "choices": choices,
        "answer": answer,
        "explanation": str(raw.get("explanation", "")).strip(),
    }, None


def _chat(messages):
    headers = {"Content-Type": "application/json"}
    if AI_API_KEY:
        headers["Authorization"] = f"Bearer {AI_API_KEY}"
    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 4096,
    }
    with httpx.Client(timeout=AI_TIMEOUT) as client:
        resp = client.post(f"{AI_BASE_URL}/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def generate_questions(mode, topic, source_text, num_questions, difficulty, types):
    """Returns dict: {ok, questions, dropped, error}.
    Never raises for content problems — only connection/HTTP errors surface in
    `error` so the route can show a friendly message."""
    types = [t for t in types if t in VALID_TYPES] or ["mcq"]
    user_prompt = _build_user_prompt(mode, topic, source_text, num_questions, difficulty, types)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw_text = None
    last_err = None
    for attempt in range(2):  # one retry on hard parse failure
        try:
            raw_text = _chat(messages)
        except (httpx.HTTPError, KeyError, IndexError) as e:
            return {"ok": False, "questions": [], "dropped": [], "error": f"AI request failed: {e}"}
        try:
            items = _extract_json_array(raw_text)
            break
        except ValueError as e:
            last_err = e
            messages.append({"role": "assistant", "content": raw_text})
            messages.append({
                "role": "user",
                "content": "That was not valid JSON. Reply with ONLY the JSON array, "
                           "no prose and no code fences.",
            })
    else:
        return {
            "ok": False,
            "questions": [],
            "dropped": [],
            "error": f"Model did not return valid JSON after retry ({last_err}). "
                     f"Raw start: {(raw_text or '')[:160]}",
        }

    questions, dropped = [], []
    for item in items:
        q, reason = _clean_question(item)
        if q:
            questions.append(q)
        else:
            dropped.append(reason)

    return {
        "ok": bool(questions),
        "questions": questions,
        "dropped": dropped,
        "error": "" if questions else "No usable questions were produced. Try again or adjust the prompt.",
    }


REVIEW_SYSTEM_PROMPT = """You are helping an admin improve a family study-quiz. \
You are shown the questions that learners get wrong most often, with how many \
attempts and how many were correct. For each, judge the most likely cause:
  - ambiguous or confusingly worded prompt
  - the answer key looks wrong or incomplete
  - genuinely hard but fair (leave it)
  - a knowledge gap that needs an easier foundational question first

Be concise and concrete. Use short bullets grouped by chapter. Suggest a fix \
only when you actually suspect a problem with the question — do not rewrite fair \
questions. Plain text, no markdown headers."""


def review_results(weak_rows):
    """Qualitative LLM review of the struggle questions. `weak_rows` is the list
    of per-question stat dicts (prompt/type/answer/attempts/correct/pct/chapter).
    Returns {ok, text, error}. Never raises — connection errors surface in
    `error` so the route can show a friendly message."""
    if not weak_rows:
        return {"ok": True, "text": "No questions have enough wrong answers yet to review. "
                                    "Come back once there's more quiz history.", "error": ""}
    lines = []
    for r in weak_rows:
        lines.append(
            f'- [{r["chapter"]}] {r["type"]} — {r["correct"]}/{r["attempts"]} correct '
            f'({r["pct"]}%): "{r["prompt"]}" (answer key: "{r["answer"]}")'
        )
    user_prompt = "These questions are missed most often:\n\n" + "\n".join(lines)
    messages = [
        {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    try:
        text = _chat(messages)
    except (httpx.HTTPError, KeyError, IndexError) as e:
        return {"ok": False, "text": "", "error": f"AI request failed: {e}"}
    return {"ok": True, "text": (text or "").strip(), "error": ""}
