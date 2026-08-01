"""Study guides: whole-topic learning material a learner can read, then mark
learned. Guide content comes from TWO places, merged into one catalog:

- **Files** (``app/study/*.md``): Claude-authored markdown baked into the image —
  a guide ships with the code, no DB write. The gold standard.
- **DB drafts** (``guide_drafts``, status ``published``): guides drafted by the
  local model from a learner's request (jobs.py ``write_guide``) and approved by
  an admin on the Review page. These live in the DB because the container
  filesystem is rebuilt on every deploy. A file wins any slug collision.

The DB additionally holds a per-user "learned" flag (keyed by slug, same for both
kinds) and the request inbox; see db.py.

A guide file is plain markdown. An optional leading ``---`` frontmatter block may
set ``title``/``summary``/``order``/``audience``; everything is graceful — a file
that just starts with ``# Heading`` (like the existing research KBs) parses fine,
taking its title from that first H1 and falling back to the prettified filename.

``audience`` is the guide's DEFAULT visibility: a comma-separated list of user
names (or email local parts), matched case-insensitively. Empty/absent means
everyone. It only applies to a user with no ``study_progress`` row for the slug —
any recorded decision (the admin audience editor, a personal dismiss) wins, so
curation in the UI is never fought by a redeploy.
"""
import os
import re
from functools import lru_cache

import markdown as _md

STUDY_DIR = os.path.join(os.path.dirname(__file__), "study")

# Tables are the whole point (the KBs are table-heavy), so `tables` is essential.
# `fenced_code`/`sane_lists` cover the rest of the KB markdown; `toc` + `attr_list`
# are harmless niceties. New md.Markdown per render (the converter is stateful).
_MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "toc", "attr_list"]


def _slug(filename):
    return os.path.splitext(filename)[0]


def _prettify(slug):
    """Filename stem -> human title fallback: 'a-electricity-basics' -> 'A
    Electricity Basics'. Leading 'NN-' ordering prefixes are dropped."""
    s = slug
    if "-" in s and s.split("-", 1)[0].isdigit():
        s = s.split("-", 1)[1]
    return s.replace("-", " ").replace("_", " ").strip().title()


def _parse_frontmatter(text):
    """Split an OPTIONAL leading ``---`` frontmatter block off the body. Returns
    (meta: dict, body: str). No YAML dep — just ``key: value`` lines, which is all
    a guide needs. A file with no frontmatter returns ({}, whole text)."""
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end].strip()
            body = text[end + 4:].lstrip("\n")
            for line in block.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip()
            return meta, body
    return meta, text


def _parse_audience(value):
    """'Jessica, ben' -> ('jessica', 'ben'). Empty/absent -> () = everyone."""
    return tuple(t.strip().lower() for t in (value or "").split(",") if t.strip())


def audience_match(audience, user):
    """Does the guide's file-declared audience include this user? An empty
    audience means everyone. Matches the user's name or email local part,
    case-insensitively, so 'jessica' covers both the picker profile name and a
    jessica@… Cloudflare identity."""
    if not audience:
        return True
    name = (user.get("name") or "").strip().lower()
    local = (user.get("email") or "").split("@")[0].strip().lower()
    return name in audience or (bool(local) and local in audience)


def _first_h1(body):
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _read(filename):
    path = os.path.join(STUDY_DIR, filename)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    slug = _slug(filename)
    meta, body = _parse_frontmatter(text)
    title = meta.get("title") or _first_h1(body) or _prettify(slug)
    # Order: explicit frontmatter wins; else a leading 'NN-' on the filename; else
    # large so unordered files sort after ordered ones, then alphabetically.
    try:
        order = int(meta["order"])
    except (KeyError, ValueError):
        head = slug.split("-", 1)[0]
        order = int(head) if head.isdigit() else 10_000
    return {
        "slug": slug,
        "title": title,
        "summary": meta.get("summary", ""),
        "order": order,
        "audience": _parse_audience(meta.get("audience")),
        "body": body,
    }


@lru_cache(maxsize=1)
def _catalog():
    """All guides, sorted (order, title). Cached — the files are baked into the
    image and never change at runtime; a process restart (every deploy) clears it."""
    if not os.path.isdir(STUDY_DIR):
        return []
    guides = []
    for fn in os.listdir(STUDY_DIR):
        if fn.endswith(".md") and not fn.startswith("."):
            try:
                g = _read(fn)
            except OSError:
                continue
            guides.append({k: g[k] for k in
                           ("slug", "title", "summary", "order", "audience")})
    guides.sort(key=lambda g: (g["order"], g["title"].lower()))
    return guides


def list_guides(conn=None):
    """Lightweight catalog for the index (no rendered HTML): file guides plus,
    when a conn is given, published model drafts. A file wins a slug collision."""
    guides = [dict(g) for g in _catalog()]
    if conn is not None:
        file_slugs = {g["slug"] for g in guides}
        for r in conn.execute(
                "SELECT slug, title, summary FROM guide_drafts "
                "WHERE status = 'published'"):
            if r["slug"] not in file_slugs:
                guides.append({"slug": r["slug"], "title": r["title"],
                               "summary": r["summary"], "order": 10_000,
                               "audience": ()})
        guides.sort(key=lambda g: (g["order"], g["title"].lower()))
    return guides


def get_guide(slug, conn=None):
    """Full guide with rendered HTML, or None. Files first (guards path traversal
    — slug must be a bare stem we actually have), then published DB drafts."""
    if slug in {g["slug"] for g in _catalog()}:
        g = _read(slug + ".md")
        g["html"] = render_html(g["body"])
        return g
    if conn is not None:
        r = conn.execute(
            "SELECT slug, title, summary, body FROM guide_drafts "
            "WHERE slug = ? AND status = 'published'", (slug,)).fetchone()
        if r:
            g = dict(r)
            g["html"] = render_html(g["body"])
            return g
    return None


# --------------------------------------------------------------------------
# Model-drafted guides (the write_guide job) — sanitising raw model output
# --------------------------------------------------------------------------
# Reasoning models leak their scratchpad in tags that vary by model/template
# (<think>, <thinking>, …); strip any such leading block. Also unwrap a whole-
# document ```markdown fence, another common way models disobey "markdown only".
_REASONING_RE = re.compile(r"<think[a-z]*>.*?</think[a-z]*>\s*",
                           re.DOTALL | re.IGNORECASE)


def parse_draft(text, fallback_title):
    """Raw model output -> {title, summary, body} with the reasoning block and
    frontmatter stripped. The body is stored WITHOUT frontmatter — title/summary
    live in dedicated columns, so rendering never re-parses model formatting.
    Returns None if nothing usable is left."""
    text = _REASONING_RE.sub("", text or "").strip()
    fence = re.match(r"^```(?:markdown|md)?\s*\n(.*)\n```\s*$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    meta, body = _parse_frontmatter(text)
    body = body.strip()
    if not body:
        return None
    title = meta.get("title") or _first_h1(body) or fallback_title
    return {"title": title.strip(), "summary": meta.get("summary", "").strip(),
            "body": body}


def slugify(title, taken=()):
    """Title -> a catalog-safe slug, uniquified against file guides, the given
    set (e.g. existing draft slugs), and emptiness."""
    base = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", title.lower())).strip("-")
    base = base[:60].rstrip("-") or "guide"
    existing = {g["slug"] for g in _catalog()} | set(taken)
    slug, n = base, 2
    while slug in existing:
        slug, n = f"{base}-{n}", n + 1
    return slug


def render_html(text):
    """Markdown -> HTML. Content is Claude-authored and trusted (not learner
    input), so we don't sanitise; the template marks it safe."""
    return _md.markdown(text, extensions=_MD_EXTENSIONS, output_format="html5")
