"""Every /static/... path referenced by a template must exist on disk, and the
app must actually serve it. Catches a typo'd <script src> that would silently
strip a page's JS (the fallback markup still renders, so nothing else fails)."""
import re
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "app" / "templates"
STATIC = Path(__file__).resolve().parent.parent / "app" / "static"


def _referenced_paths():
    refs = set()
    for t in TEMPLATES.glob("*.html"):
        refs.update(re.findall(r'(?:src|href)="/static/([^"?]+)', t.read_text()))
    return sorted(refs)


def test_templates_reference_only_existing_static_files():
    refs = _referenced_paths()
    assert refs, "expected at least style.css and the js modules"
    missing = [r for r in refs if not (STATIC / r).is_file()]
    assert missing == []


def test_static_js_is_served(client):
    for ref in _referenced_paths():
        r = client.get(f"/static/{ref}")
        assert r.status_code == 200, ref
