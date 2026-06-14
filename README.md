# FleetQuiz

A small, self-hosted **family study-quiz app**. Organize material into
**subjects → chapters → questions**, generate questions with any
OpenAI-compatible AI from a topic prompt *or* pasted source material, then quiz
one or several chapters at a time. Runs as a single Docker container.

> Example: your kid does Arduino experiments. Ask the AI to "generate questions a
> 10-year-old should learn from experiments 1–3," review/edit them, save them to
> a chapter, and quiz them — chapter by chapter or across several at once.

## What it does

- **Library**: subjects → chapters → questions. Manual question CRUD plus AI generation.
- **AI generation** (any OpenAI-compatible endpoint — LM Studio, Ollama, vLLM,
  llama.cpp, OpenAI, …): from a **topic prompt** or from **pasted source
  material**. Output is validated, malformed items are dropped, and everything
  lands in a **review/edit step before saving** — so a flaky local model degrades
  to "fewer questions," never garbage in a quiz.
- **Quiz loop**: pick one or multiple chapters, choose count + order. MCQ and
  True/False auto-grade; short-answer is **self-graded flashcard style** (type,
  reveal, "got it / missed it"). Results page + **retry the ones you missed**.
- **Family profiles + roles**: lightweight per-person profiles with quiz history.
  **Admins** can add/edit/generate/delete content; **non-admin profiles are
  quiz-only** (every mutation + generation route is gated by `require_admin`).
  Admin status comes from an email matching `ADMIN_EMAILS`, or the bootstrap rule
  (first profile created is admin).

Question types: `mcq`, `truefalse`, `short` — three question types, three
template files, one SQLite file. Deliberately small.

## Stack

FastAPI + Jinja2 (server-rendered, no JS build) + SQLite. One container, one
volume for the DB (`/data/quiz.db`).

## Run it

```bash
cp .env.example .env        # then edit — see Configuration below
docker compose up -d --build
# open http://localhost:8080
```

On first boot it **seeds a sample "Arduino Experiments" subject** (2 chapters,
~7 questions) so the quiz loop works immediately — even before the AI is wired
up. Seeding is idempotent (skips if the subject already exists).

To run without Docker (dev):

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
QUIZ_DB_PATH=./data/quiz.db python -m seed
QUIZ_DB_PATH=./data/quiz.db uvicorn app.main:app --reload --port 8080
```

## Configuration (env / `.env`)

| Var | Default | Purpose |
|-----|---------|---------|
| `AI_BASE_URL` | `http://localhost:1234/v1` | OpenAI-compatible endpoint. Keep the `/v1`. In Docker, use `http://host.docker.internal:1234/v1` to reach a server on the host. |
| `AI_MODEL` | `local-model` | Model id as served by the endpoint. Set this to match what's loaded. |
| `AI_API_KEY` | *(empty)* | API token for the endpoint, if it requires one. |
| `AI_TIMEOUT` | `180` | Seconds to wait on a generation call. Local models can run 1–2 min/batch. |
| `QUIZ_SECRET_KEY` | `dev-insecure-change-me` | Signs the profile cookie. Set to `openssl rand -hex 32`. |
| `ADMIN_EMAILS` | *(empty)* | Comma-separated emails that become admins. |
| `QUIZ_DB_PATH` | `/data/quiz.db` | SQLite path (inside the container). |

## Authentication & security model

This is a **family-scale** app and its auth is deliberately lightweight. Read
this before exposing it beyond your LAN.

Two identity sources, in priority order:

1. **Cloudflare Access header** (`Cf-Access-Authenticated-User-Email`) — set when
   you put a Cloudflare tunnel + Access policy in front of the app. The app
   auto-creates a profile for the authenticated email and marks it admin iff the
   email is in `ADMIN_EMAILS`.
2. **Signed `quiz_user` cookie** via the profile picker — for when the app is hit
   directly on the LAN with no SSO in front.

**Caveats (intentional, family-stakes — do not reuse this pattern for anything
sensitive):**

- The Cloudflare header is spoofable by anything that can reach the container
  directly, so the admin gate is only truly enforced *behind* Access.
- The bare-LAN profile picker has **no passwords** — anyone on the LAN can pick
  any profile, including an admin one. The `require_admin` gate's real job here
  is to stop a kid's profile from *accidentally* deleting content.

If you want a hard admin boundary, run the app only behind an authenticating
reverse proxy (Cloudflare Access or equivalent) and don't expose the bare port.

## Deployment notes

- The app listens on **8080** inside the container; map it to whatever host port
  you like.
- The DB is a single `quiz.db` file on the `/data` volume — trivial to back up.
  Bind-mount `/data` to a backed-up path if you want it in your backups.
- To use roles meaningfully, front the app with an authenticating reverse proxy
  and set `ADMIN_EMAILS` to the admins' email addresses.

## License

MIT — see [LICENSE](LICENSE).
