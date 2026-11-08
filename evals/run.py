"""FleetQuiz model eval suite (model-eval contract 1).

The household runs several apps on one shared LM Studio box; `model-eval run
<model>` (workbench) calls this suite, and every other app's, to decide whether
a model is better or worse *for this app* than the one it uses today. The
contract lives in proxmox/model-eval/README.md. This file owns quiz's side:

- It drives the app's REAL LLM functions in app/ai.py (generate_questions,
  verify_and_fix, tutor, review_results, write_guide), with the app's own
  prompts and request parameters. No DB, no routes.
- Fixtures are small, fixed and non-personal (below), so outputs may be shown
  to the Claude judge.
- Each case gets deterministic checks; generative cases also hand the judge an
  input excerpt + the output. Speed and token counts are measured by the
  model-eval proxy, not here.

Run it through model-eval (it needs the proxy's env):
    model-eval run <model> --apps quiz [--cases generate/source-wine]
"""
import json
import os
import re
import sys
import time
import traceback
import urllib.request

if "MODEL_EVAL_BASE_URL" not in os.environ:
    sys.exit("run this through `model-eval run <model> --apps quiz` (it sets MODEL_EVAL_*)")

# app.ai reads its endpoint at import time, so point it at the proxy first.
os.environ["AI_BASE_URL"] = os.environ["MODEL_EVAL_BASE_URL"]
os.environ["AI_MODEL"] = os.environ.get("MODEL_EVAL_MODEL", "model-eval")
os.environ["AI_GUIDE_MODEL"] = os.environ["AI_MODEL"]
os.environ["AI_API_KEY"] = os.environ.get("MODEL_EVAL_API_KEY", "")

from app import ai

from . import fixtures as fx

CONTROL = os.environ["MODEL_EVAL_CONTROL"]
OUT = os.environ["MODEL_EVAL_OUT"]
ONLY = set(filter(None, os.environ.get("MODEL_EVAL_CASES", "").split(",")))


def mark(workflow, case):
    req = urllib.request.Request(f"{CONTROL}/_case", data=json.dumps({"workflow": workflow, "case": case}).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    urllib.request.urlopen(req, timeout=30).read()


def score(checks, critical):
    vals = [bool(v) for v in checks.values()]
    return (all(checks.get(k) for k in critical), round(sum(vals) / len(vals), 3) if vals else 0.0)


def qs_text(questions):
    lines = []
    for i, q in enumerate(questions, 1):
        ch = f" choices={q['choices']}" if q.get("choices") else ""
        lines.append(f"{i}. [{q['type']}] {q['prompt']}{ch} -> {q['answer']} ({q.get('explanation', '')})")
    return "\n".join(lines)


def has_markdown(text):
    return bool(re.search(r"(^|\n)\s*#{1,6}\s|\*\*|```|^\s*[-*]\s", text or ""))


# ---------------------------------------------------------------- workflows

def wf_generate(case):
    r = ai.generate_questions(case["mode"], case["topic"], case.get("source", ""), case["n"],
                              case["difficulty"], case["types"])
    qs = r.get("questions") or []
    prompts = [q["prompt"].strip().lower() for q in qs]
    checks = {
        "ok": r.get("ok", False),
        "enough_questions": len(qs) >= case["n"] - 1,
        "none_dropped": not r.get("dropped"),
        "types_as_asked": all(q["type"] in case["types"] for q in qs),
        "no_duplicates": len(set(prompts)) == len(prompts),
        "has_explanations": all((q.get("explanation") or "").strip() for q in qs),
    }
    ok, sc = score(checks, ["ok", "enough_questions"])
    judge = {"input": f"Request: {case['n']} {case['difficulty']} questions, types {case['types']}, "
                      f"mode={case['mode']}, topic={case['topic']!r}\n\nSOURCE:\n{case.get('source', '(none)')}",
             "output": qs_text(qs) or f"(no questions; error: {r.get('error')})"}
    return {"ok": ok, "score": sc, "checks": checks, "judge": judge, "error": r.get("error") or None}


def wf_verify(case):
    try:
        out = ai.verify_and_fix(case["question"], case["context"], fx.WINE_KB, "")
    except Exception as e:  # noqa: BLE001 (a suite scores failures, never crashes)
        return {"ok": False, "score": 0.0, "checks": {"parsed": False}, "error": f"{type(e).__name__}: {e}"}
    ans = str(out.get("answer", "")).strip().lower()
    exp = case["expect_answer"].lower()
    checks = {
        "parsed": True,
        "needs_fix_right": bool(out.get("needs_fix")) == case["expect_fix"],
        "answer_right": exp in ans or ans in exp and len(ans) > 2,
        "mcq_answer_in_choices": (out.get("type") != "mcq") or out.get("answer") in (out.get("choices") or []),
        "has_rationale": bool((out.get("rationale") or "").strip()),
    }
    ok, sc = score(checks, ["parsed", "needs_fix_right", "answer_right"])
    return {"ok": ok, "score": sc, "checks": checks}


def wf_tutor(case):
    try:
        reply = ai.tutor(case["context"], case["history"], case["message"])
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "score": 0.0, "checks": {"replied": False}, "error": f"{type(e).__name__}: {e}"}
    checks = {
        "replied": bool(reply.strip()),
        "plain_text": not has_markdown(reply),
        "short": len(reply) <= case.get("max_chars", 1200),
    }
    ok, sc = score(checks, ["replied"])
    judge = {"input": f"{case['context']}\n\nHISTORY: {case['history']}\n\nLEARNER: {case['message']}",
             "output": reply}
    return {"ok": ok, "score": sc, "checks": checks, "judge": judge}


def wf_review(case):
    r = ai.review_results(case["rows"])
    text = r.get("text") or ""
    checks = {
        "ok": r.get("ok", False),
        "no_headers": not re.search(r"(^|\n)\s*#{1,6}\s", text),
        "flags_planted_bad_key": bool(re.search(case["must_flag"], text, re.IGNORECASE)),
    }
    ok, sc = score(checks, ["ok", "flags_planted_bad_key"])
    judge = {"input": "Weak questions:\n" + "\n".join(
        f"- {r_['prompt']} (key: {r_['answer']}) {r_['correct']}/{r_['attempts']}" for r_ in case["rows"]),
        "output": text}
    return {"ok": ok, "score": sc, "checks": checks, "judge": judge, "error": r.get("error") or None}


def wf_guide(case):
    r = ai.write_guide(case["topic"], case["note"], case["kb"], "")
    t = (r.get("text") or "").strip()
    checks = {
        "ok": r.get("ok", False),
        "frontmatter": bool(re.match(r"---\s*\n.*?title:.*?\n.*?summary:.*?\n.*?---", t, re.DOTALL)),
        "one_h1": len(re.findall(r"(?m)^# ", t)) == 1,
        "sections": len(re.findall(r"(?m)^## ", t)) >= 2,
        "self_check": bool(re.search(r"(?mi)^##+ .*(self.?check|check yourself|quiz yourself|try it)", t)),
        "bold_terms": t.count("**") >= 4,
    }
    ok, sc = score(checks, ["ok", "frontmatter", "sections"])
    judge = {"input": f"Topic: {case['topic']}\nNote: {case['note']}\nKB:\n{case['kb']}", "output": t}
    return {"ok": ok, "score": sc, "checks": checks, "judge": judge, "error": r.get("error") or None}


WORKFLOWS = [
    {"id": "generate", "title": "Admin question generation", "fn": wf_generate, "timeout_s": 180,
     "cases": fx.GENERATE,
     "judge_rubric": "Quiz questions for a family study app. Score: factual accuracy (most important); "
                     "for source mode, grounded in the SOURCE; exactly one clearly correct answer; plausible "
                     "distractors; clear wording; difficulty and audience as requested."},
    {"id": "verify", "title": "Fact-check one question", "fn": wf_verify, "timeout_s": 180,
     "cases": fx.VERIFY},
    {"id": "tutor", "title": "Tutor turn", "fn": wf_tutor, "timeout_s": 180, "cases": fx.TUTOR,
     "judge_rubric": "A tutor reply to one learner. Score: accurate; pitched at the learner described in "
                     "LEARNER NOTES; encouraging; short and to the point; plain text, no markdown."},
    {"id": "review", "title": "Admin review of weak questions", "fn": wf_review, "timeout_s": 180,
     "cases": fx.REVIEW,
     "judge_rubric": "An admin-facing review of often-missed quiz questions. Score: correctly spots the "
                     "question whose answer key is wrong; does not rewrite fair questions; concise, concrete."},
    {"id": "guide", "title": "Study guide (background job)", "fn": wf_guide, "timeout_s": 1800,
     "cases": fx.GUIDE,
     "judge_rubric": "A study guide in markdown. Score: factual accuracy (most important); reading level "
                     "fits the stated audience; concepts shown working inside example sentences; follows "
                     "the format (frontmatter, one H1, ## sections, self-check)."},
]


def main():
    out = {"contract": 1, "app": "quiz", "suite_version": "1", "workflows": []}
    for wf in WORKFLOWS:
        w = {k: wf[k] for k in ("id", "title", "timeout_s") if k in wf}
        if wf.get("judge_rubric"):
            w["judge_rubric"] = wf["judge_rubric"]
        w["requires"] = {"vision": False}
        w["cases"] = []
        for case in wf["cases"]:
            if ONLY and f"{wf['id']}/{case['id']}" not in ONLY:
                continue
            mark(wf["id"], case["id"])
            t0 = time.time()
            try:
                res = wf["fn"](case)
            except Exception as e:  # noqa: BLE001
                res = {"ok": False, "score": 0.0, "checks": {}, "error": f"{type(e).__name__}: {e}",
                       "trace": traceback.format_exc()[-800:]}
            res["id"] = case["id"]
            res["wall_s"] = round(time.time() - t0, 2)
            w["cases"].append(res)
            print(f"{wf['id']}/{case['id']}: {'ok' if res['ok'] else 'FAIL'} score={res['score']} "
                  f"{res['wall_s']}s {res.get('error') or ''}", flush=True)
        if w["cases"]:
            out["workflows"].append(w)
    mark(None, None)
    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
