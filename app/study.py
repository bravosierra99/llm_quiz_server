"""Study guides: whole-topic learning material a learner can read, then mark
learned. The CONTENT lives as Claude-authored markdown files baked into the image
(``app/study/*.md``) — the filesystem is the catalog, so a guide ships with the
code and the code-only deploy carries it with no DB write. The DB only holds a
per-user "learned" flag (keyed by the file's slug) and a request inbox; see db.py.

A guide file is plain markdown. An optional leading ``---`` frontmatter block may
set ``title``/``summary``/``order``; everything is graceful — a file that just
starts with ``# Heading`` (like the existing research KBs) parses fine, taking its
title from that first H1 and falling back to the prettified filename.
"""
import os
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
            guides.append({k: g[k] for k in ("slug", "title", "summary", "order")})
    guides.sort(key=lambda g: (g["order"], g["title"].lower()))
    return guides


def list_guides():
    """Lightweight list for the index (no rendered HTML)."""
    return [dict(g) for g in _catalog()]


def get_guide(slug):
    """Full guide with rendered HTML, or None if the slug isn't a real file.
    Guards against path traversal — slug must be a bare stem we actually have."""
    if slug not in {g["slug"] for g in _catalog()}:
        return None
    g = _read(slug + ".md")
    g["html"] = render_html(g["body"])
    return g


def render_html(text):
    """Markdown -> HTML. Content is Claude-authored and trusted (not learner
    input), so we don't sanitise; the template marks it safe."""
    return _md.markdown(text, extensions=_MD_EXTENSIONS, output_format="html5")
