---
title: "From Telegram Chaos to Project Memory"
slug: "telegram-chaos-to-project-memory"
description: "How Maximus Studio built Mess-to-Memo to turn noisy Telegram project chats into reviewable, Notion-ready team memory."
author: "maximus-studio"
author_name: "Maximus Studio"
language: "en_US"
date: "2026-07-06"
updated: "2026-07-07"
category: "Tools"
tags:
  - telegram
  - knowledge-management
  - notion
  - ai
  - documentation
  - codex
difficulty: "All Levels"
estimated_reading_time: "5 min"
canonical_url: "https://maximus.pro"
---

# From Telegram Chaos to Project Memory: How We Built Mess-to-Memo at Maximus Studio

Most teams do not lose knowledge because nobody wrote it down. They lose it because it was written in the worst possible place to reuse later.

For a lot of product teams, that place is Telegram. Fast? Yes. Convenient? Also yes. Great as a long-term memory system? Not even a little.

You see the same loop on a lot of teams. Someone answers an important question in chat, everyone moves on, and two weeks later the same question comes back like nobody settled it. API behavior, onboarding rules, release caveats, UI decisions, edge cases. The answer exists. Good luck finding it when you need it.

That pattern pushed us to build **Mess-to-Memo**.

Mess-to-Memo is a Codex-ready workflow that takes a Telegram export and turns it into a compact, reviewable documentation package. It keeps the parts that should still matter next week. We built it for anyone who needs this problem solved, and we made it free. You can grab it on GitHub at [Mr-Curious-Dev/mess-to-memo](https://github.com/Mr-Curious-Dev/mess-to-memo).

## The problem was never "too much chat"

The lazy idea is to dump chat history into AI and ask for a summary. In practice, that gives you polished mush. Very readable. Not very useful.

Project chat is full of noise: acknowledgements, repeated reminders, random links, half-replies, service messages, and context that only made sense for five minutes. Buried inside that noise is the actual signal: what the backend really does, why Android behaves differently, what the PM already approved, what still needs review, and which workaround is temporary but somehow survived three releases.

The workflow started making sense once we treated the input like raw project material that needed filtering, structure, and human review.

## What Mess-to-Memo actually does

The workflow looks like this:

`Telegram export -> preprocessing -> knowledge dataset -> Notion-ready package`

Mess-to-Memo accepts either a native Telegram `result.json` export or a Toon-style `result_toon.md` file. Then it runs a local preprocessing step before any higher-level extraction starts.

```bash
python3 scripts/normalize_telegram_export.py \
  --input /path/to/result_toon.md \
  --output /path/to/preprocessed \
  --project-name "Project Name" \
  --notion-output /path/to/notion-ready
```

Here, **preprocessing** means deterministic cleanup done locally first: parse the export, normalize the messages, group related discussion, preserve useful links, and throw away obvious junk.

That step gives you artifacts you can inspect: normalized messages, grouped conversation chunks, candidate knowledge items, a `knowledge_dataset.json`, a **redaction report** that lists sensitive or risky content, and category summaries for review. The **knowledge dataset** is the compact working set with reusable facts minus routine chat clutter.

You should not have to trust one magical summarization blob. You can look at the result, diff it, review it, and decide what deserves a place in the knowledge base.

## Why preprocessing comes before AI

This is the important bit.

Before anything becomes documentation, the workflow does the boring production work locally. Yes, the demo skips this part. The script cleans the export, reduces noise, groups related messages, and flags sensitive data early.

Language models handle shaped material better than raw chat dumps. Feed them 1,000 messy chat messages and you get a polite blur. Feed them clustered discussions, a knowledge dataset, and a redaction report, and you get something a team can review.

The time-saver shows up in the review step. The workflow makes that step smaller, clearer, and repeatable instead of betting on "one prompt magic happens."

## Built for review, not blind publishing

Another rule was non-negotiable: this thing should prepare documentation, not publish it like some overexcited AI bro discovering markdown for the first time.

Mess-to-Memo generates a local `notion-ready/` package instead of pushing straight to publish. It can produce category pages, a processing report, and a publish manifest so the team can see what it extracted, what it redacted, and what still looks uncertain.

That safety layer does the real job.

Chat exports can contain personal data, token-like strings, internal URLs, message IDs, and all sorts of lovely surprises nobody wants copied into shared docs. So the workflow explicitly flags risky content and avoids exposing Telegram message IDs in user-facing outputs.

To make the handoff concrete, the companion kit includes `code/examples/chat-to-memory-workflow.mmd`, `code/templates/project-memory-review-template.md`, and `code/examples/notion-ready-package-outline.md`.

## Why we built it this way

If you build real products, you know how this goes. Important decisions do not wait for a clean Confluence page. Your team makes them in chat while people clarify requirements, compare options, patch edge cases, and answer "one small question" that somehow affects three screens and two backend rules.

Teams work like this every day.

We did not try to replace chat. We built a repeatable way to capture the useful part of it. Keep the speed. Keep the messy collaboration. Then turn the signal into something reviewable before it becomes project memory.

## The bigger lesson

AI workflows work better when you respect the shape of the source material.

Do not ask one giant model call to rescue your entire communication history. Break the problem down. Normalize the data. Separate signal from noise. Keep the intermediate outputs visible. Put review and safety in the middle, not at the end.

That work turned Mess-to-Memo into a tool you can run on your own project without paying for access to some random neuro-slop SaaS.
