# Preprocessing Pipeline

Mess-to-Memo uses a local Python preprocessing step to turn raw Telegram exports into a reviewable dataset before extraction and Notion packaging.

Preprocessing gives you:

- smaller inputs for review;
- deterministic chunking and categorization;
- early redaction reports;
- `knowledge_dataset.json` for the Notion package builder.

## Why Preprocess First

Raw chat exports are noisy. They often include:

- service messages;
- repeated acknowledgements;
- emoji-only reactions;
- partial replies without context;
- links, code blocks, and files mixed into free-form text;
- personal data that should be reviewed or redacted early.

The preprocessing step handles parsing, noise filtering, chunking, and first-pass redaction. Codex can then focus on deciding which facts belong in project memory.

## Inputs

The normalizer supports:

- Telegram export JSON with a top-level `messages` array;
- Toon-style markdown exports such as `result_toon.md` with line-based message records.

Typical supported fields:

- `id`
- `type`
- `date`
- `date_unixtime`
- `from`
- `from_id`
- `reply_to_message_id`
- `text`
- `media_type`
- `file`

## Outputs

The script writes a small dataset folder containing:

- `messages_normalized.jsonl`
- `conversation_chunks.jsonl`
- `knowledge_candidates.jsonl`
- `knowledge_dataset.json`
- `redaction_report.json`
- `category_summary.json`

## Output Roles

`messages_normalized.jsonl`

- one cleaned message per line;
- stable IDs and timestamps;
- cleaned text with sensitive values redacted;
- URLs preserved by default because project links are often reusable knowledge;
- basic metadata such as sender, reply target, attachment flags, and heuristic category hints.

`conversation_chunks.jsonl`

- short groups of related messages;
- grouped by time proximity and reply continuity;
- useful for review, clustering, or later summarization.

`knowledge_candidates.jsonl`

- chunk-level candidate knowledge units;
- includes heuristic type, category, confidence, and supporting source references;
- designed to be the best handoff point for the skill or a later LLM pass.

`knowledge_dataset.json`

- JSON list version of the candidate dataset;
- feeds the Notion package builder;
- makes the one-step export-to-Notion flow easier to automate.

`redaction_report.json`

- counts of redacted emails, phones, token-like strings, message IDs, detected URLs, and redacted URLs;
- helps audit whether the intermediate dataset is publication-safe.

## URL Handling

URLs are preserved by default because Figma, docs, Postman, tickets, specs, and internal references are often part of the useful project memory.

Use `--redact-urls` only when links themselves are sensitive:

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed \
  --redact-urls
```

`category_summary.json`

- quick counts by detected category and candidate type;
- useful for high-level triage before deeper review.

## Suggested Workflow

1. Export Telegram data.
2. Run the Python normalizer.
3. Inspect redactions and category distribution.
4. Review the candidate dataset.
5. Run the skill or a later LLM refinement step only on the cleaned candidate data.
6. Build `notion-ready/` from `knowledge_dataset.json`.

## Example Commands

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result.json \
  --output /path/to/preprocessed
```

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed
```

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed \
  --project-name "Project Name" \
  --notion-output /path/to/notion-ready
```

## Language Support

The normalizer preserves Unicode text and can parse Telegram exports in any language supported by the input format.

Heuristic categorization and candidate typing include keyword support for:

- English;
- Ukrainian;
- Spanish;
- Portuguese;
- French;
- German;
- Polish;
- Turkish;
- Arabic;
- Hindi;
- Indonesian;
- Vietnamese.

Other languages stay in the output. Category detection may fall back to `General`.

## Example Impact

On a representative project chat export, preprocessing produced this kind of reduction:

- Raw export: about `1,000+` messages and `500 KB` of chat text.
- Useful messages after preprocessing: about `20-25%` of total messages.
- Noise filtered out: about `75-80%` of raw messages.
- Conversation chunks: dozens of candidate discussions.
- Candidate knowledge units: one per chunk before final review.
- Final reusable knowledge items: a compact set of verified or needs-review records.
- Redactions: phones, token-like values, URLs, emails, and Telegram message IDs can be counted early.
- Final safety target: no Telegram message IDs in user-facing outputs.
- Compression from raw chat to final project memory can reach `98%+` for noisy chats.

Treat these as benchmark numbers, not guarantees. They show why local preprocessing should run before LLM-based extraction.

## Design Notes

- The script uses Python standard library only.
- Categorization uses conservative heuristics.
- Output records stay small and explicit so they can be diffed, filtered, and reprocessed easily.
- The preprocessing layer is not a replacement for human review or final knowledge extraction.
