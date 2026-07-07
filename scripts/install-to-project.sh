#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <project-directory>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_SKILL="$REPO_ROOT/skills/mess-to-memo"
PROJECT_DIR="$1"
TARGET_DIR="$PROJECT_DIR/.agents/skills"

mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR/mess-to-memo"
cp -R "$SOURCE_SKILL" "$TARGET_DIR/"

echo "Installed mess-to-memo to $TARGET_DIR"
