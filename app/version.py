"""The running app's version, resolved once at import.

Release flow (see scripts/version-bump.sh): the source of truth is `version` in
pyproject.toml; a bump captures it — plus git commit info — into app/version.json
via scripts/generate-version.sh, and that JSON is COMMITTED. The production image
has no .git and does not copy pyproject.toml (`COPY app ./app` only), so the
container reads the committed app/version.json. Locally, with no version.json yet,
we fall back to a live `git describe`, then to "dev".
"""
import json
import subprocess
from pathlib import Path

_VERSION_FILE = Path(__file__).with_name("version.json")


def _from_git():
    """Best-effort version/commit from git, for local dev before any bump."""
    info = {"version": "dev", "commit_short": "unknown", "branch": "unknown",
            "clean": None, "commit_message": "", "commit_date": None,
            "build_date": None}
    try:
        info["version"] = subprocess.check_output(
            ["git", "describe", "--tags", "--always"],
            stderr=subprocess.DEVNULL, text=True, cwd=_VERSION_FILE.parent
        ).strip().lstrip("v")
        info["commit_short"] = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL, text=True, cwd=_VERSION_FILE.parent
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return info


def _load():
    if _VERSION_FILE.exists():
        try:
            data = json.loads(_VERSION_FILE.read_text())
            if data.get("version"):
                return data
        except (json.JSONDecodeError, OSError):
            pass  # fall through to git
    return _from_git()


INFO = _load()
VERSION = INFO.get("version", "dev")
