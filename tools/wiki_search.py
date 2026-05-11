#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
WORD_RE = re.compile(r"[\wčšžćđČŠŽĆĐ]+", re.UNICODE)


@dataclass
class Hit:
    path: Path
    score: int
    title: str
    excerpt: str


def terms(query: str) -> list[str]:
    return [t.lower() for t in WORD_RE.findall(query) if len(t) > 1]


def read_title(text: str, fallback: str) -> str:
    # Prefer frontmatter title, then first markdown H1, then filename.
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r'^#\s+(.+?)\s*$', text, re.M)
    if m:
        return m.group(1).strip()
    return fallback


def make_excerpt(text: str, ts: list[str], width: int = 360) -> str:
    lower = text.lower()
    pos = -1
    for t in ts:
        pos = lower.find(t)
        if pos >= 0:
            break
    if pos < 0:
        pos = 0
    start = max(0, pos - width // 3)
    end = min(len(text), start + width)
    out = re.sub(r"\s+", " ", text[start:end]).strip()
    if start > 0:
        out = "... " + out
    if end < len(text):
        out += " ..."
    return out


def search(query: str, limit: int = 10) -> list[Hit]:
    ts = terms(query)
    if not ts:
        return []
    hits: list[Hit] = []
    for path in WIKI.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        score = 0
        for t in ts:
            c = lower.count(t)
            score += c * (3 if t in path.stem.lower() else 1)
        if score:
            hits.append(Hit(path=path, score=score, title=read_title(text, path.stem), excerpt=make_excerpt(text, ts)))
    hits.sort(key=lambda h: (-h.score, str(h.path)))
    return hits[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the persistent LLM Wiki markdown pages.")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    hits = search(args.query, args.limit)
    if not hits:
        print("No wiki matches found. Search the source corpus with tools/search.py next.")
        return
    for i, hit in enumerate(hits, 1):
        rel = hit.path.relative_to(ROOT)
        print(f"{i}. {hit.title} [{rel}] score={hit.score}")
        print(f"   {hit.excerpt}")


if __name__ == "__main__":
    main()
