#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
INDEX = WIKI / "index.md"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"\'')
    return data


def title_for(path: Path, text: str) -> str:
    fm = parse_frontmatter(text)
    if fm.get("title"):
        return fm["title"]
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else path.stem


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate a compact wiki/index.md from frontmatter.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    groups: dict[str, list[tuple[str, Path]]] = defaultdict(list)
    for path in sorted(WIKI.rglob("*.md")):
        if path == INDEX:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        typ = fm.get("type", "uncategorized")
        groups[typ].append((title_for(path, text), path))

    lines = [
        "---",
        "title: Wiki index",
        "type: index",
        "status: active",
        "last_updated: 2026-05-11",
        "---",
        "",
        "# Wiki index",
        "",
        "Generated from wiki page frontmatter. For richer comments, edit manually after generation.",
        "",
    ]
    for typ in sorted(groups):
        lines.append(f"## {typ}")
        lines.append("")
        for title, path in groups[typ]:
            rel = path.relative_to(WIKI)
            lines.append(f"- [{title}]({rel.as_posix()})")
        lines.append("")

    out = "\n".join(lines)
    if args.dry_run:
        print(out)
    else:
        INDEX.write_text(out, encoding="utf-8")
        print(f"Updated {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
