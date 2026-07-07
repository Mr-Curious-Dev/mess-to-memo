# From Telegram Chaos to Project Memory: How We Built Mess-to-Memo at Maximus Studio

A team solves something important in Telegram. The backend rule gets clarified. The Android edge case gets explained. Someone drops the Figma link, the API detail, and the workaround.

Three weeks later, somebody asks the same question again. The answer exists. It is buried under stickers, "ok got it," and one heroic message that starts with "guys quick question" and ends with a pricing rule.

That problem is why we built **Mess-to-Memo**.

Mess-to-Memo is a free GitHub tool that turns a Telegram export into a reviewable documentation package. You can get it here: [Mr-Curious-Dev/mess-to-memo](https://github.com/Mr-Curious-Dev/mess-to-memo).

Keep the signal. Drop the noise. Give the team something they can review before it lands in a knowledge base.

## Most chat summaries are fake useful

Let’s be honest. The default AI-bro move is to throw the whole export into a model and ask for a summary. Then you get five paragraphs of polished nothing.

You know the style. "The team discussed various implementation considerations." Amazing. Thank you, machine. We definitely needed a prettier way to say "people sent messages."

Project chat does contain knowledge. It also contains service messages, repeated acknowledgements, partial replies, emoji-only reactions, random links, and context that expired before the coffee got cold. If you do not clean the material first, the model spends part of its budget summarizing junk.

The real win starts before the LLM step.

## What the preprocessor actually does

The repo has a local Python script, `scripts/normalize_telegram_export.py`, and this part matters because the demo skips it.

It accepts either a native Telegram `result.json` export or a Toon-style `result_toon.md`. Then it runs a plain, inspectable preprocessing pass before any higher-level extraction begins:

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed \
  --project-name "Project Name" \
  --notion-output /path/to/notion-ready
```

In practice, **preprocessing** here means a few specific things.

The script parses both export formats, flattens Telegram text blocks into normal text, normalizes whitespace, and redacts emails, phone numbers, token-like strings, and Telegram message IDs. It keeps URLs by default because Figma files, specs, Postman collections, and tickets often are the useful part. If the links are sensitive, you can pass `--redact-urls`.

Then it filters obvious junk. A record counts as noise if it is not a real `message`, if it has no text, if it is too short, or if it has no letter characters at all. So yes, the fire emoji reaction is safe. It will not become "institutional knowledge."

After that, the script groups useful messages into chunks. It starts a new chunk when the time gap passes 30 minutes, when the group hits 25 messages, or when reply continuity and shared keywords break down. That last part matters. The script does not just chop the export into fixed-size slices like some low-effort "AI pipeline" tutorial that forgot conversations have shape.

Then it assigns heuristic categories such as Backend, Mobile, UI, Business Logic, Security Notes, API Reference, and Solved Issues. It also tags candidate types like decision, issue, task, reference, or question-answer. Confidence stays simple: longer text, more messages, and stronger signals push the item from low to high.

The outputs stay small and reviewable:

- `messages_normalized.jsonl`
- `conversation_chunks.jsonl`
- `knowledge_candidates.jsonl`
- `knowledge_dataset.json`
- `redaction_report.json`
- `category_summary.json`

That **knowledge dataset** is the compact handoff set with facts worth review. The **redaction report** gives you counts for emails, phones, tokens, URLs, and message IDs so you can check the intermediate data before anyone publishes anything.

## Is the preprocessing efficient?

Short version: yes, in the way that matters.

This is not "we deployed nine agents and a quantum vector cloud ate the chat." It is a standard-library Python script doing deterministic cleanup before the expensive reasoning step. That is why it is useful.

The repo benchmark shows the effect on chats:

- raw export around `1,000+` messages and `500 KB` of chat text
- useful messages after preprocessing around `20-25%`
- noise filtered out around `75-80%`
- final compression from raw chat to reusable project memory can reach `98%+`

Those are benchmark numbers, not magic promises. Chat quality changes from team to team. Still, the direction is obvious. Cut the junk first and you reduce review load, token waste, and one more pile of neuro-slop.

That is where the time-saver lives.

## Built for review, because autopublish is how teams create new problems

Mess-to-Memo does not pretend raw extraction should go straight into Notion like a sacred truth descended from the GPU heavens.

It builds a local `notion-ready/` package instead. That package can include category pages, a processing report, and a publish manifest. You may look at the result, check redactions, review candidates, and decide what deserves to become project memory.

That review step is the product. Without it, you are not preserving knowledge. You are automating confusion.

## Why this matters

If you build real products, you know where the hard part starts. It starts after the screenshot, after the quick demo, after the "AI can summarize everything now" pitch. Real product work lives in business logic, handoff details, edge cases, and the weird little decisions teams make while trying to ship something sellable.

Chat is where a lot of that truth leaks out in plain text.

Mess-to-Memo gives you a repeatable way to catch it before it disappears. Free, local-first, and reviewable. Which is a lot more useful than one more miraculous SaaS that promises to save time right up until you start reading what it wrote.
