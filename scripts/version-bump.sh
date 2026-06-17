#!/usr/bin/env bash
# Unified version bump for FleetQuiz — keeps pyproject.toml, app/version.json, and
# the git tag in lockstep, then pushes so `ops/prod.sh update` (reset --hard
# origin/main + rebuild) ships the tagged version.
#
# Usage:
#   ./scripts/version-bump.sh patch              # 0.1.0 -> 0.1.1
#   ./scripts/version-bump.sh minor              # 0.1.0 -> 0.2.0
#   ./scripts/version-bump.sh major              # 0.1.0 -> 1.0.0
#   ./scripts/version-bump.sh 1.2.3              # set an explicit version
#   ./scripts/version-bump.sh --dry-run patch    # preview, no changes
#   ./scripts/version-bump.sh --yes patch        # skip the confirm prompt
#   ./scripts/version-bump.sh --skip-tests patch # emergency hotfix: skip the gate
#
# A release runs a pre-release gate (syntax + template parse; plus pytest/ruff if
# present) BEFORE committing/tagging/pushing. A red build never ships unless you
# pass --skip-tests.
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

cd "$(dirname "$0")/.."

DRY_RUN=false; YES=false; SKIP_TESTS=false; BUMP_TYPE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run|-n) DRY_RUN=true; shift ;;
        --yes|-y)     YES=true; shift ;;
        --skip-tests) SKIP_TESTS=true; shift ;;
        *)            BUMP_TYPE="$1"; shift ;;
    esac
done

if [ -z "$BUMP_TYPE" ]; then
    echo -e "${RED}Error: must specify a bump type or version${NC}"
    echo "Usage: $0 [--dry-run] [--yes] [--skip-tests] <patch|minor|major|X.Y.Z>"
    exit 1
fi

# Releases live on main: commit, tag, and `git push origin main` all assume it.
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
    echo -e "${RED}Error: releases run on main, but you're on '${BRANCH}'.${NC}"
    echo -e "${YELLOW}Merge into main, then re-run from main.${NC}"
    exit 1
fi

CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\([^"]*\)".*/\1/')
echo -e "${BLUE}Current version: ${CURRENT_VERSION}${NC}"

if [[ "$BUMP_TYPE" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    NEW_VERSION="$BUMP_TYPE"
else
    IFS='.' read -r -a P <<< "$CURRENT_VERSION"
    MAJOR="${P[0]}"; MINOR="${P[1]}"; PATCH="${P[2]}"
    case "$BUMP_TYPE" in
        major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
        minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
        patch) PATCH=$((PATCH + 1)) ;;
        *) echo -e "${RED}Error: invalid bump type '$BUMP_TYPE' (use patch|minor|major|X.Y.Z)${NC}"; exit 1 ;;
    esac
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
fi
echo -e "${GREEN}New version: ${NEW_VERSION}${NC}"

if git rev-parse "v$NEW_VERSION" >/dev/null 2>&1; then
    echo -e "${RED}Error: tag v$NEW_VERSION already exists${NC}"; exit 1
fi

if [ "$DRY_RUN" = true ]; then
    echo -e "\n${YELLOW}DRY RUN — would:${NC}"
    echo "  1. pyproject.toml version -> $NEW_VERSION"
    echo "  2. regenerate app/version.json"
    echo "  3. commit 'Bump version to $NEW_VERSION'"
    echo "  4. tag v$NEW_VERSION and push main + tags"
    echo -e "${YELLOW}Note: --dry-run does NOT run the pre-release gate.${NC}"
    exit 0
fi

echo -e "\n${YELLOW}This will commit + tag v$NEW_VERSION and push main + tags to origin.${NC}"
if [ "$YES" != "true" ]; then
    read -p "Continue? [y/N] " -n 1 -r; echo
    [[ $REPLY =~ ^[Yy]$ ]] || { echo -e "${YELLOW}Aborted${NC}"; exit 0; }
fi

# --- Pre-release gate (after confirm, before any mutation) ---
RUN="uv run --with-requirements requirements.txt"
if [ "$SKIP_TESTS" = true ]; then
    echo -e "\n${YELLOW}⚠ --skip-tests: skipping the gate. Shipping UNVERIFIED.${NC}"
else
    echo -e "\n${BLUE}Pre-release gate...${NC}"
    echo -e "${BLUE}  → byte-compile app/${NC}"
    $RUN python -m compileall -q app \
        || { echo -e "${RED}✗ Syntax error in app/ — aborting (override: --skip-tests).${NC}"; exit 1; }
    echo -e "${BLUE}  → parse templates${NC}"
    $RUN python - <<'PY' \
        || { echo -e "\033[0;31m✗ A Jinja template failed to parse — aborting.\033[0m"; exit 1; }
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("app/templates"))
for t in sorted(Path("app/templates").glob("*.html")):
    env.get_template(t.name)
print("  templates ok")
PY
    if [ -d tests ]; then
        echo -e "${BLUE}  → pytest${NC}"
        $RUN --with pytest pytest -q \
            || { echo -e "${RED}✗ Tests failed — aborting (override: --skip-tests).${NC}"; exit 1; }
    else
        echo -e "${YELLOW}  → no tests/ dir — skipping pytest${NC}"
    fi
    if [ -f ruff.toml ] || grep -q '^\[tool.ruff' pyproject.toml 2>/dev/null; then
        echo -e "${BLUE}  → ruff${NC}"
        uvx ruff check app \
            || { echo -e "${RED}✗ Lint failed — aborting (override: --skip-tests).${NC}"; exit 1; }
    else
        echo -e "${YELLOW}  → no ruff config — skipping lint${NC}"
    fi
    echo -e "${GREEN}✓ Gate passed${NC}"
fi

echo -e "\n${BLUE}Updating pyproject.toml...${NC}"
sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
CHECK=$(grep '^version = ' pyproject.toml | sed 's/version = "\([^"]*\)".*/\1/')
[ "$CHECK" = "$NEW_VERSION" ] || { echo -e "${RED}Error: pyproject.toml update failed${NC}"; git checkout pyproject.toml; exit 1; }

echo -e "${BLUE}Regenerating app/version.json...${NC}"
./scripts/generate-version.sh

echo -e "${BLUE}Committing + tagging...${NC}"
git add pyproject.toml app/version.json
git commit -q -m "Bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo -e "${BLUE}Pushing to origin...${NC}"
git push -q origin main
git push -q origin --tags

echo -e "\n${GREEN}=== Released v${NEW_VERSION} ===${NC}  (${CURRENT_VERSION} -> ${NEW_VERSION})"
echo -e "${YELLOW}Deploy it:${NC} ./ops/prod.sh update   # reset --hard origin/main + rebuild carries version.json in"
