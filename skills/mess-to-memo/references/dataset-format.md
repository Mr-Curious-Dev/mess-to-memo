# Dataset Format

Each knowledge item should include:

- `title`
- `type`
- `category`
- `platforms`
- `status`
- `confidence`
- `summary`
- `why_it_matters`
- `action`
- `related`
- `source`

## Status

- `needs_review`
- `verified`
- `outdated`

## Confidence

- `high`
- `medium`
- `low`

## Cross-Link Rule

If one item affects multiple areas:

- store it once in the most natural category;
- reference it from related categories;
- avoid duplicating the full text.

The Notion package builder uses this shape to group items into category pages.
