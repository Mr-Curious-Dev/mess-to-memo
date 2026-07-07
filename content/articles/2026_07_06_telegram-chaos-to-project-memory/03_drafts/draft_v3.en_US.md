# From Telegram Chaos to Project Memory: How We Built Mess-to-Memo at Maximus Studio

Most teams do not lose knowledge because nobody wrote it down. They lose it because the knowledge was written down in the wrong place.

For many product teams, that place is Telegram. It is fast, informal, and perfect for daily coordination. It is also where important decisions quietly disappear: API rules, onboarding notes, release caveats, bug fixes, UI choices, and all the little operational truths that keep a project moving.

At Maximus Studio, we build mobile and web products, and we kept seeing the same pattern. The team would solve a problem in chat, move on, and then solve the same problem again two weeks later because nobody could reliably find the original answer.

That is why we built **Mess-to-Memo**.

Mess-to-Memo is a small Codex-ready workflow that takes a Telegram export and turns it into a compact, reviewable documentation package built to keep only the parts that deserve to survive.

## The problem was never "too much chat"

The obvious mistake is to treat chat history like a document and ask AI to summarize it from top to bottom. In practice, that creates soft, generic output full of things nobody needs.

Project chat is noisy by nature. It contains acknowledgements, partial replies, service messages, repeated reminders, random links, and context that only made sense for five minutes. Hidden inside that noise are the durable facts teams actually care about: how login works, which endpoint is deprecated, why a screen behaves differently on Android, and what still needs review.

The real win was to stop thinking about summarization first and start thinking about **filtering, structuring, and review** first.

## What Mess-to-Memo actually does

The workflow is simple:

`Telegram export -> preprocessing -> knowledge dataset -> Notion-ready package`

Mess-to-Memo accepts either a native Telegram `result.json` export or a Toon-style `result_toon.md` file. From there, it runs a local preprocessing step that cleans and groups the material before any higher-level extraction happens.

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed \
  --project-name "Project Name" \
  --notion-output /path/to/notion-ready
```

That preprocessing stage produces a small set of useful artifacts:

- normalized messages;
- grouped conversation chunks;
- candidate knowledge items;
- a compact `knowledge_dataset.json`;
- a redaction report;
- category summaries for review.

Those outputs matter because they give the team something inspectable. Instead of asking someone to trust an opaque summarization step, we give them a trail they can review, diff, and refine.

## Why preprocessing comes before AI

This is the part we care about most.

Before anything gets turned into documentation, the tool does deterministic work locally. It parses the export, filters obvious noise, groups related messages, preserves useful links, and flags sensitive material early. In the repo, this is the preprocessing stage: a cleanup pass that makes the input smaller, clearer, and safer to reason about.

That matters because large language models are much better when the raw material already has shape. If you feed an assistant 1,000 messy chat messages, you get a polite blur. If you feed it clustered conversations, candidate knowledge items, and a redaction report, you get something much closer to publishable documentation.

In practice, the project benchmarks show why this matters. A noisy chat can shrink dramatically before the final review step, leaving a much smaller set of reusable knowledge items for humans to verify.

## Built for review, not blind publishing

Another design decision was non-negotiable: the output has to be reviewable before anyone pushes it into a knowledge base.

Mess-to-Memo generates a local `notion-ready/` package rather than pretending publication should happen automatically. It can create category pages, a processing report, and a publish manifest so a team can see what was extracted, redacted, or still uncertain.

That safety layer is not a nice extra. It is the product.

Chat exports often contain personal data, token-like strings, message IDs, internal URLs, and context that should never be copied straight into shared documentation. So the workflow explicitly flags redactions and avoids exposing Telegram message IDs in user-facing outputs.

To make that review story concrete, the companion kit for this article includes a workflow diagram in `code/examples/chat-to-memory-workflow.mmd`, a review checklist in `code/templates/project-memory-review-template.md`, and a sample package outline in `code/examples/notion-ready-package-outline.md`.

## Why we built it this way at Maximus Studio

Maximus Studio has spent years shipping mobile and web products, and one thing becomes clear on real teams: valuable decisions do not always arrive in formal documents. Quite often, they take shape in regular team chat while people are clarifying requirements, comparing options, and solving day-to-day product problems.

That is not a failure of documentation. It is simply how product work happens. Fast conversations are where context forms, tradeoffs get tested, and practical decisions become clear.

We built Mess-to-Memo to help teams preserve those moments when they become important. Keep using chat for speed and collaboration, then run a workflow that captures the signal, removes the routine noise, and prepares the useful parts for human review before they become shared memory.

## The bigger lesson

If there is one lesson in this project, it is that AI workflows get better when you respect the shape of the source material.

Do not ask one giant model call to rescue an entire communication history. Break the problem down. Normalize the data. Separate transient coordination from reusable knowledge. Keep the intermediate outputs visible. Treat safety and review as first-class features.

That is what turned Mess-to-Memo from a clever prompt into a tool we would actually want on a real team.
