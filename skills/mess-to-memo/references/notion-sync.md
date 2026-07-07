# Notion Sync

Use this when the user wants a local Notion-ready package or Notion publication.

When the skill is installed into Codex, run the bundled helper scripts from the installed skill directory.

## Workflow

1. Prepare local dataset or collect user-authored Markdown pages.
2. Prepare a local `notion-ready/` package.
3. Review the local files.
4. Publish only if requested.
5. Save page IDs and URLs in `publish-manifest.json`.

## Supported Entry Paths

### Path A: Telegram export to Notion-ready package

Use this when the input starts from `result.json` or `result_toon.md` and the user wants local Notion files:

```bash
python3 <mess-to-memo-skill-dir>/scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed \
  --project-name "Project Name" \
  --notion-output /path/to/notion-ready
```

This command writes the intermediate preprocessing files and a reviewable `notion-ready/` folder.

### Path B: User-authored Markdown pages

Use this when the user already prepared Markdown files in the intended Notion page structure:

```bash
python3 <mess-to-memo-skill-dir>/scripts/build_notion_package.py \
  --pages-dir /path/to/notion-pages \
  --output /path/to/notion-ready \
  --project-name "Project Name" \
  --source-export manual-pages
```

The script copies the pages into the final package and generates `processing-report.md` and `publish-manifest.json`.

## Required Local Output Structure

Create this structure for Notion-ready output:

```text
notion-ready/
├── Onboarding.md
├── Backend.md
├── Business-Logic.md
├── Mobile.md
├── UI.md
├── API-Reference.md
├── Solved-Issues.md
├── Known-Problems.md
├── Internal-Links.md
├── Questions-Answered-Before.md
├── Security-Notes.md
├── processing-report.md
└── publish-manifest.json
```

Only include category pages that have useful content. Always include `processing-report.md` and `publish-manifest.json`.

## Page Format

Use compact markdown that maps to Notion blocks:

- `# Project Name: Category`
- `## Knowledge Item Title`
- Type, status, confidence, platforms, and source metadata
- Summary
- Why it matters
- Action
- Related links or related knowledge items, when useful

Do not put raw Telegram message IDs in pages. Use human-readable source ranges only.

## Publish Manifest

`publish-manifest.json` is the handoff contract for later sync. It must include:

- project name, source export, and processed date;
- target Notion parent fields, initially null when not published;
- one `pages[]` entry per local page;
- page title, filename, category, item count, local status, and placeholder Notion page ID/URL fields.

Example page entry:

```json
{
  "title": "Backend",
  "file": "Backend.md",
  "category": "Backend",
  "item_count": 8,
  "notion_page_id": null,
  "notion_page_url": null,
  "status": "local_ready"
}
```

## Helper Script

Build a local package from an existing structured dataset:

```bash
python3 <mess-to-memo-skill-dir>/scripts/build_notion_package.py \
  --dataset /path/to/knowledge_dataset.json \
  --output /path/to/notion-ready \
  --project-name "Project Name" \
  --source-export result_toon.md
```

## Suggested Pages

- Onboarding
- Backend
- Business Logic
- Mobile
- UI

Optional:

- API Reference
- Solved Issues
- Known Problems
- Internal Links
- Questions Answered Before
- Security Notes
- Processing Report
