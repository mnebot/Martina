#!/usr/bin/env bash
# Script to create branch, commit, push and create PR (if gh is available)
# Run this from git-bash in Windows: ./push_and_create_pr.sh

set -euo pipefail
REPO_DIR="/c/Users/mnebo/repos/Martina"
BRANCH="feature/ci-pipelines"
COMMIT_MSG="chore(ci): add packaging, CI build/publish and deploy workflows; add config example and .gitignore"
PR_TITLE="Add packaging and CI pipelines"
PR_BODY_FILE="PR_BODY.md"

cd "$REPO_DIR"

# Ensure git is available
if ! command -v git >/dev/null 2>&1; then
  echo "git not found in PATH. Please install git or run these steps manually."
  exit 1
fi

# Create branch
git checkout -b "$BRANCH"

# Stage and commit
git add -A
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "$COMMIT_MSG"
fi

# Push branch
git push -u origin "$BRANCH"

# Create PR if gh is available
if command -v gh >/dev/null 2>&1; then
  if [ -f "$PR_BODY_FILE" ]; then
    gh pr create --title "$PR_TITLE" --body-file "$PR_BODY_FILE" --base master --head "$BRANCH"
  else
    gh pr create --title "$PR_TITLE" --body "See PR_BODY.md in the branch for details." --base master --head "$BRANCH"
  fi
else
  echo "gh CLI not found. You can create a PR in the browser:" 
  echo "https://github.com/mnebot/Martina/compare/master...$BRANCH?expand=1"
fi

echo "Done."
