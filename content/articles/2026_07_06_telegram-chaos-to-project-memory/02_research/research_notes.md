# Research Notes

## Session 1: 2026-07-06

**Focus:** understand the product story behind Mess-to-Memo and verify current Maximus Studio positioning.

**Web research performed**

1. Opened `https://maximus.pro/`
   - Confirmed current positioning around mobile and web development
   - Captured official numbers and technology claims for context
2. Opened `https://maximus.pro/about`
   - Confirmed studio history and the stack listed on the official site

**Local research performed**

1. Read repo `README.md`
   - Confirmed the practical path from Telegram export to local Notion-ready package
2. Read `docs/preprocessing-pipeline.md`
   - Confirmed why preprocessing is a first-class step
3. Read `skills/mess-to-memo/SKILL.md`
   - Confirmed safety rules, categories, and expected outputs

**Key findings**

1. The tool solves a concrete documentation problem, not a vague summarization problem.
2. The strongest differentiator is deterministic local preprocessing before AI reasoning.
3. Reviewability and safety are central to the workflow: redaction reports, compact datasets, and human review before publication.
4. A good article angle is not "AI summarizes chats" but "teams need durable memory from operational chat noise."

**Article decisions**

1. Write in English.
2. Use a Medium-style narrative voice with practical specificity.
3. Add a lightweight document companion kit instead of a fake runnable code demo.
4. Keep the article around 800 words, with one command snippet and references to the companion files.
