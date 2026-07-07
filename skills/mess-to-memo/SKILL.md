---
name: mess-to-memo
description: Use when converting Telegram exports, Toon markdown exports, copied discussions, screenshots, or project notes into a compact knowledge dataset and Notion-ready documentation package.
---

# Mess-to-Memo

Use this skill when the user wants to:

- analyze Telegram exports, Toon markdown exports, or copied discussions;
- preprocess Telegram `result.json` or Toon-style `result_toon.md` exports;
- extract reusable project knowledge from chat history;
- build `knowledge_dataset.json`;
- generate `notion-ready/` pages, `processing-report.md`, and `publish-manifest.json`;
- review chat-derived knowledge before Notion publication.

## Workflow

1. Define scope and available inputs.
2. Preprocess raw exports when available.
3. Extract reusable knowledge only.
4. Structure extracted items into a compact dataset.
5. Generate compact page outputs and, when the user wants a handoff package, create `notion-ready/` with a publish manifest. The default path is: install the skill, provide Telegram `result.json` or Toon-style `result_toon.md`, produce a local Notion-ready package.
6. Run safety and quality checks.
7. Prepare or publish to Notion if requested.

## Rules

- Keep the output small enough to review.
- Do not summarize every message.
- Keep only reusable project knowledge.
- Remove noise, temporary coordination, and duplicates.
- Keep the language of the source material unless the user requests translation.
- Do not expose Telegram message IDs in user-facing outputs.
- When preparing Notion-ready output, create category pages, `processing-report.md`, and `publish-manifest.json`.
- Use the one-step flow from Telegram export to local `notion-ready/` output when the user asks for a practical handoff package.
- Redact tokens, passwords, credentials, phone numbers, emails, personal data, and similar sensitive values.
- Mark uncertain or conflicting information for review.
- Prefer the latest explicit project decision over older documentation, but flag conflicts for review.

## Default Categories

- Onboarding
- Backend
- Business Logic
- Mobile
- UI

Optional categories:

- API Reference
- Solved Issues
- Known Problems
- Internal Links
- Questions Answered Before
- Security Notes

## Source Reference Format

- Single message: `Sender Name - DD.MM.YYYY HH:MM:SS`
- Discussion range: `First Sender - DD.MM.YYYY HH:MM:SS to Last Sender - DD.MM.YYYY HH:MM:SS`

## Read Only What You Need

- Preprocessing workflow: [references/preprocessing-pipeline.md](references/preprocessing-pipeline.md)
- Overall workflow: [references/prompt-set.md](references/prompt-set.md)
- Dataset shape: [references/dataset-format.md](references/dataset-format.md)
- Notion workflow: [references/notion-sync.md](references/notion-sync.md)
- Safety review: [references/safety-checklist.md](references/safety-checklist.md)
