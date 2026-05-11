#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "index" / "search.sqlite"


def build_query(q: str, operator: str = "and") -> str:
    tokens = re.findall(r"[\wčšžćđČŠŽĆĐ]+", q, flags=re.UNICODE)
    tokens = [t for t in tokens if len(t) > 1]
    if not tokens:
        return '""'
    sep = " AND " if operator == "and" else " OR "
    return sep.join(tokens)


def get_rows(query: str, limit: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = """
        SELECT p.id, p.source_id, p.short_title, p.source_kind, p.page_number, p.path, p.quality_flags, p.text,
               bm25(pages_fts) AS rank
        FROM pages_fts
        JOIN pages p ON p.id = pages_fts.rowid
        WHERE pages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """
    rows = cur.execute(sql, [build_query(query, "and"), limit]).fetchall()
    if not rows:
        rows = cur.execute(sql, [build_query(query, "or"), limit]).fetchall()
    conn.close()
    return rows


def excerpt(text: str, query: str, width: int = 900) -> str:
    tokens = [t.lower() for t in re.findall(r"[\wčšžćđČŠŽĆĐ]+", query, flags=re.UNICODE) if len(t) > 1]
    lower = text.lower()
    pos = -1
    for tok in tokens:
        pos = lower.find(tok)
        if pos >= 0:
            break
    if pos < 0:
        pos = 0
    start = max(0, pos - width // 3)
    end = min(len(text), start + width)
    out = text[start:end]
    out = re.sub(r"\s+", " ", out).strip()
    if start > 0:
        out = "... " + out
    if end < len(text):
        out += " ..."
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an LLM context pack from local corpus search results.")
    parser.add_argument("question")
    parser.add_argument("--limit", type=int, default=6)
    args = parser.parse_args()
    rows = get_rows(args.question, args.limit)
    print(f"# Context pack\n\nQuestion: {args.question}\n")
    if not rows:
        print("No local matches found. Try fewer words or a synonym.")
        return
    for i, row in enumerate(rows, 1):
        print(f"## Source {i}: {row['short_title']}, PDF page {row['page_number']}\n")
        print(f"- Source ID: `{row['source_id']}`")
        print(f"- Kind: `{row['source_kind']}`")
        print(f"- Markdown path: `{row['path']}`")
        if row['quality_flags'] != "[]":
            print(f"- Quality flags: `{row['quality_flags']}`")
        print("\n> " + textwrap.fill(excerpt(row['text'], args.question), width=100, subsequent_indent="> "))
        print()
    print("## Instruction for answer\n")
    print("Answer from these sources only. Give the practical rule first, then explanation, and cite PDF page plus Markdown path.")


if __name__ == "__main__":
    main()
