"""Keyless web search via DuckDuckGo (the `ddgs` package).

Mirrors the approach in the reserve automation project: no API key, no cost —
just outbound HTTPS to DuckDuckGo. Everything here degrades to empty results on
any failure (no network egress, ddgs not installed, rate-limited, timeout) and
reports the reason, so a job can record "search unavailable" rather than crash.
"""
import os

# Allow turning search off entirely via env without touching code.
SEARCH_ENABLED = os.environ.get("QUIZ_SEARCH_ENABLED", "1") not in ("0", "false", "")
MAX_RESULTS = int(os.environ.get("QUIZ_SEARCH_MAX_RESULTS", "8"))


def web_search(query, max_results=None):
    """Return (results, error). `results` is a list of {title, url, snippet};
    `error` is "" on success or a short reason string on failure (results=[])."""
    query = (query or "").strip()
    if not query:
        return [], "empty query"
    if not SEARCH_ENABLED:
        return [], "search disabled"
    try:
        from ddgs import DDGS
    except Exception as e:  # package missing
        return [], f"ddgs unavailable: {e}"
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=max_results or MAX_RESULTS))
        return [{"title": r.get("title", ""), "url": r.get("href", ""),
                 "snippet": r.get("body", "")} for r in raw], ""
    except Exception as e:  # network/egress/rate-limit/etc.
        return [], f"search failed: {e}"


def format_results(results):
    """Readable block to embed in an LLM prompt."""
    if not results:
        return "No web search results available."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r.get('title', '')}\n    {r.get('url', '')}\n    {r.get('snippet', '')}")
    return "\n".join(lines)
