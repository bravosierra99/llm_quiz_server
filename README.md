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
- **Adaptive scheduling (spaced repetition)**: within the chapters you pick,
  question selection is **smart by default** — it uses a per-person, per-question
  **SM-2-lite** scheduler (the spaced-repetition math behind Anki) to show what
  you're **due** to review first, introduce new questions at a measured pace, and
  push back questions you've reliably recalled. Each chapter shows a **mastery
  badge** (Not started / N due / N learned / Mastered). `Shuffle` and `In order`
  remain as non-adaptive escape hatches. No LLM in this loop — it's deterministic
  and instant.
- **Admin analytics + optional AI review**: an admin-only **Analytics** page
  reports per-question and per-chapter performance and flags "struggle" questions
  (answered ≥3 times, <60% correct). One button kicks off an **optional** LLM pass
  that suggests *why* a question is missed (ambiguous wording, wrong answer key,
  needs a foundational question) — curation advice only; nothing changes
  automatically.
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

## Deployment

The app is one container; how you expose it is up to you. A few patterns, in
rough order of how much you're exposing:

**LAN only.** Run `docker compose up -d` and hit `http://<host>:8080` from your
network. Profiles have no passwords, so treat everyone on the LAN as trusted.
Fine for a single household, no SSO needed.

**Behind a reverse proxy (TLS + a nice hostname).** Put something like
[Nginx Proxy Manager](https://nginxproxymanager.com/), [Traefik](https://traefik.io/),
or [Caddy](https://caddyserver.com/) in front, terminate TLS, and route
`quiz.example.com` → the container's port 8080. Still no real auth — anyone who
can reach the hostname can pick any profile.

**Behind an authenticating proxy (recommended if it's reachable off-LAN).**
Add an SSO/identity layer that injects the authenticated user's email as the
`Cf-Access-Authenticated-User-Email` request header. The app trusts that header
to identify the user and grants admin iff the email is in `ADMIN_EMAILS`. Options:

- **[Cloudflare Tunnel + Access](https://developers.cloudflare.com/cloudflare-one/applications/)**
  — Access sets that exact header for you; define a policy per group
  (e.g. admins vs. everyone else).
- **[Authelia](https://www.authelia.com/) / [authentik](https://goauthentik.io/) /
  [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/)** — configure the
  proxy to forward the verified email under that header name.

> ⚠️ The header is **only trustworthy if the container is unreachable except
> through the proxy.** Anything that can hit `:8080` directly can forge it. Don't
> publish the bare port. See [Authentication & security model](#authentication--security-model).

**Storage / backups.** The entire state is one `quiz.db` file on the `/data`
volume. Bind-mount `/data` to a path that's in your backup rotation (NAS, a
backed-up host directory, etc.) and you're covered — copy the file to restore.

**AI endpoint.** Point `AI_BASE_URL` at any OpenAI-compatible server. For a
local model server (LM Studio, Ollama, vLLM, llama.cpp) running on the Docker
host, use `http://host.docker.internal:1234/v1`; for one elsewhere on the LAN,
use its address. Set `AI_MODEL` to the exact id the server advertises, and bump
`AI_TIMEOUT` if your model is slow (local models often need 1–2 min/batch).

> Keeping your own deployment notes? Drop them in a `*.local.md` file — those are
> gitignored so your hostnames, IPs, and policy details stay out of git.

## License

MIT — see [LICENSE](LICENSE).
