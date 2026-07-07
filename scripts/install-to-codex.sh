#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_SKILL="$REPO_ROOT/skills/mess-to-memo"
TARGET_DIR="${HOME}/.codex/skills"

mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR/mess-to-memo"
cp -R "$SOURCE_SKILL" "$TARGET_DIR/"

echo "Installed mess-to-memo to $TARGET_DIR"
