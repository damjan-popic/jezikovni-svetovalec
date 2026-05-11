#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
REQUIRED = {"title", "type", "status", "last_updated"}
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")


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


def wiki_stems(files: list[Path]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for f in files:
        out[f.stem.lower()] = f
        # Obsidian-style links sometimes use title text; add frontmatter title aliases.
        fm = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        if fm.get("title"):
            out[fm["title"].lower()] = f
    return out


def target_exists(from_file: Path, link: str, stems: dict[str, Path]) -> bool:
    link = link.split("#", 1)[0]
    if link.startswith("http://") or link.startswith("https://"):
        return True
    if link.endswith(".md"):
        return (from_file.parent / link).resolve().exists()
    return link.lower() in stems


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint the persistent LLM Wiki.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as errors.")
    args = parser.parse_args()

    if not WIKI.exists():
        print("ERROR: wiki/ does not exist")
        sys.exit(2)

    files = sorted(WIKI.rglob("*.md"))
    errors: list[str] = []
    warnings: list[str] = []

    for required in [WIKI / "index.md", WIKI / "log.md"]:
        if not required.exists():
            errors.append(f"Missing required file: {required.relative_to(ROOT)}")

    stems = wiki_stems(files)
    inbound: dict[Path, int] = {f: 0 for f in files}

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        missing = REQUIRED - set(fm)
        if missing:
            warnings.append(f"{f.relative_to(ROOT)} missing frontmatter keys: {', '.join(sorted(missing))}")

        for link in WIKILINK_RE.findall(text):
            if not target_exists(f, link, stems):
                warnings.append(f"{f.relative_to(ROOT)} has missing wikilink [[{link}]]")
            else:
                target = stems.get(link.lower())
                if target in inbound:
                    inbound[target] += 1

        for link in MD_LINK_RE.findall(text):
            target_part = link.split("#", 1)[0]
            target = (f.parent / target_part).resolve()
            if not target.exists():
                warnings.append(f"{f.relative_to(ROOT)} has missing markdown link ({link})")
            else:
                try:
                    t = target.relative_to(ROOT)
                    p = ROOT / t
                    if p in inbound:
                        inbound[p] += 1
                except ValueError:
                    pass

    # Treat pages as sufficiently reachable if index links to them; index/log and maintenance reports are exempt.
    for f, n in inbound.items():
        rel = f.relative_to(ROOT)
        if rel.as_posix() in {"wiki/index.md", "wiki/log.md"}:
            continue
        if "maintenance/" in rel.as_posix():
            continue
        if n == 0:
            warnings.append(f"Possible orphan page: {rel}")

    print(f"Wiki files checked: {len(files)}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"- {e}")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")
    if not errors and not warnings:
        print("No wiki lint issues found.")

    if errors or (args.strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
