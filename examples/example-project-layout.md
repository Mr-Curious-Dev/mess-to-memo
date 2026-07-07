# Example Project Layout

Mess-to-Memo produces this layout when you process a Telegram `result.json` or Toon `result_toon.md` export into a local Notion-ready package.

```text
project_example_ChatExport_YYYY-MM-DD/
├── result.json
├── result_toon.md
├── photos/
├── preprocessed/
│   ├── messages_normalized.jsonl
│   ├── conversation_chunks.jsonl
│   ├── knowledge_candidates.jsonl
│   ├── knowledge_dataset.json
│   ├── redaction_report.json
│   └── category_summary.json
└── notion-ready/
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
