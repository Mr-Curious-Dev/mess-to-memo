# Overview

Mess-to-Memo turns Telegram project chats into a reviewed knowledge dataset and a local Notion-ready documentation package.

The repo ships an installable Codex skill plus the scripts and references needed to run the full path:

`install skill -> provide result.json or result_toon.md -> receive notion-ready/`

## Design Goals

- keep the installable skill itself compact;
- keep long operating instructions in reference files;
- include scripts that work inside the repo and inside the installed skill;
- produce local files that a human can review before Notion publication.

## Core Workflow

1. Define the input scope.
2. Preprocess the raw Telegram export into a local intermediate dataset.
3. Extract reusable knowledge.
4. Structure it into a dataset.
5. Prepare compact pages from the dataset or from user-authored Markdown pages.
6. Review for safety and quality.
7. Produce a local Notion-ready package and sync to Notion if requested.

## Production Files

The shipped skill needs more than `SKILL.md` because the Notion flow uses local processing and review artifacts:

- install instructions;
- Notion-ready workflow documentation;
- example layouts;
- helper scripts;
- preprocessing utilities;
- templates;
- repo-level documentation.
