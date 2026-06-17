#!/usr/bin/env bash
# Write app/version.json from the current version + git state.
#
# Why this file is COMMITTED (unlike a typical build-time artifact): FleetQuiz
# deploys via `ops/prod.sh update`, which runs `git reset --hard origin/main` +
# `docker compose build` on the server through a locked allowlist gate we can't
# extend with a pre-build step. The image also doesn't copy .git (.dockerignore)
# or pyproject.toml (`COPY app ./app` only). So the running container reads its
# version from this committed JSON. scripts/version-bump.sh regenerates and
# commits it as part of every release.
#
# Source of truth for the number is pyproject.toml's `version` (NOT a git tag),
# because a bump runs this BEFORE creating the tag.
set -euo pipefail

cd "$(dirname "$0")/.."
VERSION_FILE="app/version.json"

VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\([^"]*\)".*/\1/')
[ -n "$VERSION" ] || { echo "ERROR: no version in pyproject.toml" >&2; exit 1; }

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    COMMIT=$(git rev-parse HEAD)
    COMMIT_SHORT=$(git rev-parse --short HEAD)
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    COMMIT_MESSAGE=$(git log -1 --pretty=%B | head -n1)
    COMMIT_DATE=$(git log -1 --format=%ai)
    [ -z "$(git status --porcelain)" ] && CLEAN="true" || CLEAN="false"
else
    COMMIT="unknown"; COMMIT_SHORT="unknown"; BRANCH="unknown"
    COMMIT_MESSAGE="Built outside git repository"; COMMIT_DATE="null"; CLEAN="null"
fi

# JSON-escape the commit message via python (handles quotes/backslashes).
MSG_JSON=$(printf '%s' "$COMMIT_MESSAGE" | python3 -c 'import sys, json; print(json.dumps(sys.stdin.read().strip()))')

cat > "$VERSION_FILE" <<EOF
{
  "version": "$VERSION",
  "commit": "$COMMIT",
  "commit_short": "$COMMIT_SHORT",
  "branch": "$BRANCH",
  "clean": $CLEAN,
  "commit_message": $MSG_JSON,
  "commit_date": "$COMMIT_DATE",
  "build_date": "$(date -Iseconds)"
}
EOF

echo "✓ Wrote $VERSION_FILE  (version $VERSION, commit $COMMIT_SHORT, clean=$CLEAN)"
