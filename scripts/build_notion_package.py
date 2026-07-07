#!/usr/bin/env python3
"""Build a Notion-ready markdown package from a dataset or existing pages."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


DEFAULT_PAGE_ORDER = [
    "Onboarding",
    "Backend",
    "Business Logic",
    "Mobile",
    "UI",
    "API Reference",
    "Solved Issues",
    "Known Problems",
    "Internal Links",
    "Questions Answered Before",
    "Security Notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Notion-ready markdown pages and a publish manifest."
    )
    parser.add_argument("--dataset", help="Path to knowledge dataset JSON or JSONL")
    parser.add_argument(
        "--pages-dir",
        help="Directory containing user-authored Markdown files already prepared for Notion",
    )
    parser.add_argument("--output", required=True, help="Output notion-ready directory")
    parser.add_argument("--project-name", required=True, help="Project display name")
    parser.add_argument("--source-export", default=None, help="Source export filename or folder")
    args = parser.parse_args()
    if bool(args.dataset) == bool(args.pages_dir):
        parser.error("Provide exactly one of --dataset or --pages-dir")
    return args


def slugify_page_name(name: str) -> str:
    return (
        name.replace(" ", "-")
        .replace("/", "-")
        .replace("_", "-")
        .strip("-")
    )


def load_dataset(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        items: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("Expected every JSONL line to be a knowledge item object")
                items.append(record)
        return items

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Expected dataset JSON to be a list of knowledge items")
    return data


def group_by_category(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        category = str(item.get("category") or "Uncategorized")
        grouped[category].append(item)
    return dict(grouped)


def sorted_categories(grouped: dict[str, list[dict[str, Any]]]) -> list[str]:
    known = [category for category in DEFAULT_PAGE_ORDER if category in grouped]
    extra = sorted(category for category in grouped if category not in DEFAULT_PAGE_ORDER)
    return known + extra


def item_to_markdown(item: dict[str, Any]) -> str:
    lines = [
        f"## {item.get('title', 'Untitled')}",
        "",
        f"- Type: `{item.get('type', 'note')}`",
        f"- Status: `{item.get('status', 'needs_review')}`",
        f"- Confidence: `{item.get('confidence', 'unknown')}`",
        f"- Platforms: {', '.join(item.get('platforms') or ['General'])}",
        f"- Source: {item.get('source', 'Unknown')}",
        "",
        "### Summary",
        "",
        str(item.get("summary") or "").strip(),
        "",
        "### Why It Matters",
        "",
        str(item.get("why_it_matters") or "").strip(),
        "",
        "### Action",
        "",
        str(item.get("action") or "").strip(),
    ]

    related = item.get("related")
    if related:
        lines.extend(["", "### Related", ""])
        if isinstance(related, list):
            lines.extend(f"- {entry}" for entry in related)
        else:
            lines.append(str(related))

    lines.append("")
    return "\n".join(lines)


def build_page(project_name: str, category: str, items: list[dict[str, Any]]) -> str:
    lines = [
        f"# {project_name}: {category}",
        "",
        f"Items: {len(items)}",
        "",
    ]
    for item in items:
        lines.append(item_to_markdown(item))
    return "\n".join(lines).rstrip() + "\n"


def build_processing_report(project_name: str, source_export: str | None, items: list[dict[str, Any]]) -> str:
    category_counts = Counter(str(item.get("category") or "Uncategorized") for item in items)
    status_counts = Counter(str(item.get("status") or "unknown") for item in items)
    confidence_counts = Counter(str(item.get("confidence") or "unknown") for item in items)

    lines = [
        "# Processing Report",
        "",
        "## Inputs",
        "",
        f"- Project: {project_name}",
        f"- Source export: {source_export or 'not specified'}",
        f"- Date processed: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Items extracted: {len(items)}",
        f"- Categories created: {len(category_counts)}",
        "",
        "## Category Counts",
        "",
    ]
    lines.extend(f"- {category}: {count}" for category, count in sorted(category_counts.items()))
    lines.extend(["", "## Status Counts", ""])
    lines.extend(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    lines.extend(["", "## Confidence Counts", ""])
    lines.extend(f"- {confidence}: {count}" for confidence, count in sorted(confidence_counts.items()))
    lines.extend(
        [
            "",
            "## Human Review Needed",
            "",
            "- Review all `needs_review` items before publishing.",
            "- Check source references for participant-name exposure if output will be shared externally.",
            "",
            "## Redactions",
            "",
            "- Do not include raw credentials, tokens, phone numbers, emails, or Telegram message IDs.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_manifest(
    project_name: str,
    source_export: str | None,
    page_records: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "project": {
            "name": project_name,
            "source_export": source_export,
            "processed_date": date.today().isoformat(),
        },
        "notion": {
            "parent_page_id": None,
            "parent_page_url": None,
            "parent_title": f"{project_name} Project Memory",
        },
        "pages": page_records,
    }


def count_markdown_items(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("## "))


def infer_category_from_filename(path: Path) -> str:
    stem = path.stem.replace("-", " ").replace("_", " ").strip()
    return " ".join(part.capitalize() for part in stem.split()) or "Uncategorized"


def write_manifest(output_dir: Path, manifest: dict[str, Any]) -> None:
    with (output_dir / "publish-manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_package_from_dataset(
    items: list[dict[str, Any]],
    output_dir: Path,
    project_name: str,
    source_export: str | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    grouped = group_by_category(items)

    page_records: list[dict[str, Any]] = []
    for category in sorted_categories(grouped):
        filename = f"{slugify_page_name(category)}.md"
        page_path = output_dir / filename
        page_path.write_text(build_page(project_name, category, grouped[category]), encoding="utf-8")
        page_records.append(
            {
                "title": category,
                "file": filename,
                "category": category,
                "item_count": len(grouped[category]),
                "notion_page_id": None,
                "notion_page_url": None,
                "status": "local_ready",
            }
        )

    report_file = "processing-report.md"
    (output_dir / report_file).write_text(
        build_processing_report(project_name, source_export, items),
        encoding="utf-8",
    )
    page_records.append(
        {
            "title": "Processing Report",
            "file": report_file,
            "category": "Processing Report",
            "item_count": 1,
            "notion_page_id": None,
            "notion_page_url": None,
            "status": "local_ready",
        }
    )

    write_manifest(output_dir, build_manifest(project_name, source_export, page_records))


def build_package_from_pages_dir(
    pages_dir: Path,
    output_dir: Path,
    project_name: str,
    source_export: str | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    page_records: list[dict[str, Any]] = []
    for page_path in sorted(pages_dir.glob("*.md")):
        if page_path.name == "processing-report.md":
            continue
        shutil.copyfile(page_path, output_dir / page_path.name)
        category = infer_category_from_filename(page_path)
        page_records.append(
            {
                "title": category,
                "file": page_path.name,
                "category": category,
                "item_count": count_markdown_items(page_path.read_text(encoding="utf-8")),
                "notion_page_id": None,
                "notion_page_url": None,
                "status": "local_ready",
            }
        )

    report_file = "processing-report.md"
    existing_report = pages_dir / report_file
    if existing_report.exists():
        shutil.copyfile(existing_report, output_dir / report_file)
    else:
        report_items = [
            {
                "category": record["category"],
                "status": record["status"],
                "confidence": "unknown",
            }
            for record in page_records
        ]
        (output_dir / report_file).write_text(
            build_processing_report(project_name, source_export, report_items),
            encoding="utf-8",
        )

    page_records.append(
        {
            "title": "Processing Report",
            "file": report_file,
            "category": "Processing Report",
            "item_count": 1,
            "notion_page_id": None,
            "notion_page_url": None,
            "status": "local_ready",
        }
    )

    write_manifest(output_dir, build_manifest(project_name, source_export, page_records))


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.dataset:
        build_package_from_dataset(
            load_dataset(Path(args.dataset)),
            output_dir,
            args.project_name,
            args.source_export,
        )
    else:
        build_package_from_pages_dir(
            Path(args.pages_dir),
            output_dir,
            args.project_name,
            args.source_export,
        )


if __name__ == "__main__":
    main()
