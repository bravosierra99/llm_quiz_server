"""Web search for the quiz app — a thin gate over the shared `websearch` package.

The keyless DuckDuckGo helper lives in one place now (the `websearch` package,
github.com/bravosierra99/websearch, pinned in requirements.txt). This module adds
only the quiz-specific `QUIZ_SEARCH_ENABLED` kill-switch and default result count;
the actual search + the stable {title, url, snippet} contract come from there.
Do NOT re-vendor ddgs glue here.
"""
import os

from websearch import format_results, web_search as _web_search

__all__ = ["web_search", "format_results", "SEARCH_ENABLED", "MAX_RESULTS"]

# Allow turning search off entirely via env without touching code.
SEARCH_ENABLED = os.environ.get("QUIZ_SEARCH_ENABLED", "1") not in ("0", "false", "")
MAX_RESULTS = int(os.environ.get("QUIZ_SEARCH_MAX_RESULTS", "8"))


def web_search(query, max_results=None):
    """Return (results, error) — same contract as websearch.web_search, with the
    quiz's env kill-switch and default count applied. Fully degrading."""
    if not SEARCH_ENABLED:
        return [], "search disabled"
    return _web_search(query, max_results or MAX_RESULTS)
