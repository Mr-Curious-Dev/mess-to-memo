#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT/README.md"
test -f "$ROOT/docs/preprocessing-pipeline.md"
test -f "$ROOT/scripts/build_notion_package.py"
test -f "$ROOT/scripts/normalize_telegram_export.py"
test -f "$ROOT/skills/mess-to-memo/SKILL.md"
test -f "$ROOT/skills/mess-to-memo/agents/openai.yaml"
test -f "$ROOT/skills/mess-to-memo/scripts/build_notion_package.py"
test -f "$ROOT/skills/mess-to-memo/scripts/normalize_telegram_export.py"
test -f "$ROOT/skills/mess-to-memo/references/preprocessing-pipeline.md"
test -f "$ROOT/skills/mess-to-memo/references/prompt-set.md"
test -f "$ROOT/skills/mess-to-memo/references/dataset-format.md"
test -f "$ROOT/skills/mess-to-memo/references/notion-sync.md"
test -f "$ROOT/skills/mess-to-memo/references/safety-checklist.md"
cmp -s "$ROOT/scripts/build_notion_package.py" "$ROOT/skills/mess-to-memo/scripts/build_notion_package.py"
cmp -s "$ROOT/scripts/normalize_telegram_export.py" "$ROOT/skills/mess-to-memo/scripts/normalize_telegram_export.py"

echo "Repository structure looks valid."
